from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import re
from typing import Mapping

from agente_seshix.application.authority_policy import AuthorityPolicy
from agente_seshix.application.evidence_intake import EvidenceIntakeCommand
from agente_seshix.application.semantic_model import (
    SemanticCandidate,
    SemanticModelRequest,
    SemanticOutput,
    StructuredSemanticService,
)
from agente_seshix.application.skill_01_context import Skill01ContextCommand
from agente_seshix.application.skill_01_node import (
    Skill01NodeCommand,
    Skill01NodeResult,
    Skill01NodeRuntime,
)
from agente_seshix.domain.context_evidence import EvidenceClassification
from agente_seshix.domain.task_context import ContextSection, Task, TaskContextRequirements


class Skill01SemanticIntakeError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class SemanticFieldRule:
    key: str
    clarification_question: str


SEMANTIC_INTAKE_CATALOG_V1: Mapping[str, SemanticFieldRule] = {
    "company.name": SemanticFieldRule(
        "company.name",
        "Qual è il nome o la ragione sociale dell'azienda?",
    ),
    "company.activities": SemanticFieldRule(
        "company.activities",
        "Quali attività svolge concretamente l'azienda?",
    ),
    "company.employees": SemanticFieldRule(
        "company.employees",
        "Quanti dipendenti ha l'azienda?",
    ),
    "company.owner_count": SemanticFieldRule(
        "company.owner_count",
        "Quanti titolari/soci operativi sono presenti?",
    ),
    "company.admin_staff": SemanticFieldRule(
        "company.admin_staff",
        "Quante persone svolgono attività amministrativa?",
    ),
    "company.country": SemanticFieldRule(
        "company.country",
        "In quale paese opera principalmente l'azienda?",
    ),
    "company.revenue": SemanticFieldRule(
        "company.revenue",
        "Qual è il fatturato/ricavo dell'azienda per il periodo rilevante?",
    ),
}
@dataclass(frozen=True, slots=True)
class Skill01SemanticPreview:
    request_id: str
    source_text: str
    source_ref: str
    semantic_output: SemanticOutput
    accepted_candidates: tuple[SemanticCandidate, ...]
    clarification_questions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Skill01SemanticCommitResult:
    preview: Skill01SemanticPreview
    node_results: tuple[Skill01NodeResult, ...]

    @property
    def final_context_version_id(self) -> str | None:
        for result in reversed(self.node_results):
            if result.context_version is not None:
                return result.context_version.version_id
        return None


class Skill01SemanticIntakeService:
    _GENERIC_COMPANY_NAMES = frozenset(
        {
            "azienda",
            "l'azienda",
            "la mia azienda",
            "mia azienda",
            "the company",
            "my company",
            "company",
        }
    )
    _UNKNOWN_MARKERS = (
        "non so",
        "non conosco",
        "non noto",
        "non nota",
        "non disponibile",
        "non è disponibile",
        "sconosciuto",
        "sconosciuta",
        "unknown",
        "unavailable",
        "not known",
    )

    def __init__(
        self,
        semantic_service: StructuredSemanticService,
        node_runtime: Skill01NodeRuntime,
    ) -> None:
        self._semantic_service = semantic_service
        self._node_runtime = node_runtime

    def analyze(
        self,
        *,
        request_id: str,
        source_text: str,
        source_ref: str,
    ) -> Skill01SemanticPreview:
        if not source_ref.strip():
            raise Skill01SemanticIntakeError("source_ref must not be empty")

        output = self._semantic_service.execute(
            SemanticModelRequest(
                request_id=request_id,
                source_text=source_text,
                purpose="extract_company_context",
                schema_version="1",
            )
        )

        accepted: list[SemanticCandidate] = []
        questions: list[str] = []
        for candidate in output.candidates:
            rule = SEMANTIC_INTAKE_CATALOG_V1.get(candidate.key)
            if rule is None:
                raise Skill01SemanticIntakeError(
                    f"semantic key outside SKILL_01 intake catalog: {candidate.key}"
                )
            if candidate.classification is EvidenceClassification.UNKNOWN:
                if self._source_explicitly_marks_unknown(source_text):
                    questions.append(rule.clarification_question)
                continue

            if (
                candidate.key == "company.name"
                and isinstance(candidate.value, str)
                and candidate.value.strip().lower() in self._GENERIC_COMPANY_NAMES
            ):
                questions.append(rule.clarification_question)
                continue

            if candidate.classification is EvidenceClassification.FATTO:
                rebound = self._rebind_fact_candidate(candidate, source_text)
                if rebound is None:
                    questions.append(rule.clarification_question)
                    continue
                candidate = SemanticCandidate(
                    key=rebound.key,
                    claim=source_text.strip(),
                    classification=rebound.classification,
                    value=rebound.value,
                )
            self._validate_source_grounding(candidate, source_text)
            accepted.append(candidate)

        if not accepted and not questions:
            questions.append(
                "Non riesco a ricavare un fatto aziendale senza assumere. "
                "Chiarisci solo il punto principale, anche con parole semplici. "
                "Esempio: «installiamo impianti elettrici» oppure «sviluppiamo software per installatori»."
            )

        return Skill01SemanticPreview(
            request_id=request_id,
            source_text=source_text,
            source_ref=source_ref,
            semantic_output=output,
            accepted_candidates=tuple(accepted),
            clarification_questions=tuple(questions),
        )
    def _source_explicitly_marks_unknown(self, source_text: str) -> bool:
        normalized = source_text.strip().lower()
        return any(marker in normalized for marker in self._UNKNOWN_MARKERS)

    def _rebind_fact_candidate(
        self,
        candidate: SemanticCandidate,
        source_text: str,
    ) -> SemanticCandidate | None:
        value = candidate.value
        if isinstance(value, str):
            rebound = self._bounded_source_span(value, source_text)
            if rebound is None:
                return None
            value = rebound
        elif candidate.key == "company.activities" and isinstance(value, list):
            rebound_items: list[str] = []
            for item in value:
                if not isinstance(item, str):
                    raise Skill01SemanticIntakeError(
                        "company.activities items must be strings"
                    )
                normalized = " ".join(item.lower().split())
                if len(normalized.split()) < 2:
                    raise Skill01SemanticIntakeError(
                        f"activity is not a complete phrase: {item!r}"
                    )
                rebound = self._bounded_source_span(item, source_text)
                if rebound is None:
                    return None
                rebound_items.append(rebound)
            value = rebound_items

        return SemanticCandidate(
            key=candidate.key,
            claim=candidate.claim,
            classification=candidate.classification,
            value=value,
        )

    @staticmethod
    def _bounded_source_span(value: str, source_text: str) -> str | None:
        raw_value = value.strip()
        if not raw_value:
            return None

        lower_source = source_text.lower()
        exact_index = lower_source.find(raw_value.lower())
        if exact_index >= 0:
            return source_text[exact_index: exact_index + len(raw_value)]

        source_tokens = list(re.finditer(r"\b[\wÀ-ÿ'-]+\b", source_text, re.UNICODE))
        value_tokens = re.findall(r"\b[\wÀ-ÿ'-]+\b", raw_value, re.UNICODE)
        if not source_tokens or not value_tokens:
            return None

        target = " ".join(value_tokens).lower()
        target_len = len(value_tokens)
        candidates: list[tuple[float, str]] = []
        for window_len in range(max(1, target_len - 1), target_len + 2):
            if window_len > len(source_tokens):
                continue
            for start in range(0, len(source_tokens) - window_len + 1):
                end = start + window_len - 1
                span = source_text[
                    source_tokens[start].start(): source_tokens[end].end()
                ]
                normalized_span = " ".join(
                    match.group(0) for match in source_tokens[start:start + window_len]
                ).lower()
                ratio = SequenceMatcher(None, target, normalized_span).ratio()
                candidates.append((ratio, span))

        if not candidates:
            return None
        candidates.sort(key=lambda item: item[0], reverse=True)
        best_ratio, best_span = candidates[0]
        second_ratio = candidates[1][0] if len(candidates) > 1 else 0.0

        if best_ratio < 0.94:
            return None
        if second_ratio >= 0.94 and best_ratio - second_ratio < 0.02:
            return None
        return best_span

    def _validate_source_grounding(
        self,
        candidate: SemanticCandidate,
        source_text: str,
    ) -> None:
        if candidate.classification is not EvidenceClassification.FATTO:
            return

        source = " ".join(source_text.lower().split())

        value = candidate.value
        if isinstance(value, str):
            normalized = " ".join(value.lower().split())
            if normalized not in source:
                raise Skill01SemanticIntakeError(
                    f"FATTO value not grounded in source: {value!r}"
                )

        if candidate.key == "company.activities" and isinstance(value, list):
            for item in value:
                if not isinstance(item, str):
                    raise Skill01SemanticIntakeError(
                        "company.activities items must be strings"
                    )
                normalized = " ".join(item.lower().split())
                if normalized not in source:
                    raise Skill01SemanticIntakeError(
                        f"activity not grounded in source: {item!r}"
                    )
                if len(normalized.split()) < 2:
                    raise Skill01SemanticIntakeError(
                        f"activity is not a complete phrase: {item!r}"
                    )

    def commit(
        self,
        preview: Skill01SemanticPreview,
        *,
        task: Task,
        context_requirements: TaskContextRequirements,
        available_context: Mapping[ContextSection, object],
        skill_version: str,
        actor_id: str,
        authority_action: str,
        authority_policy: AuthorityPolicy,
        base_version_id: str = "PCV-0",
    ) -> Skill01SemanticCommitResult:
        current_base = base_version_id
        results: list[Skill01NodeResult] = []

        for index, candidate in enumerate(preview.accepted_candidates, start=1):
            evidence_id = f"{preview.request_id}:EV:{index}"
            new_version_id = f"{preview.request_id}:PCV:{index}"
            record_id = f"{preview.request_id}:CTX:{index}"

            skill_command = Skill01ContextCommand(
                base_version_id=current_base,
                new_version_id=new_version_id,
                record_id=record_id,
                key=candidate.key,
                classification=candidate.classification,
                context_value_version=str(index),
                evidence_id=evidence_id,
                proposed_value=(
                    candidate.value
                    if candidate.classification is EvidenceClassification.IPOTESI
                    else None
                ),
                required=True,
            )
            node_result = self._node_runtime.execute(
                Skill01NodeCommand(
                    run_id=f"{preview.request_id}:RUN:{index}",
                    task=task,
                    context_requirements=context_requirements,
                    available_context=available_context,
                    skill_version=skill_version,
                    actor_id=actor_id,
                    authority_action=authority_action,
                    authority_policy=authority_policy,
                    evidence_intake=EvidenceIntakeCommand(
                        evidence_id=evidence_id,
                        source_ref=preview.source_ref,
                        claim=candidate.claim,
                        evidence=candidate.value,
                        version=str(index),
                    ),
                    skill_command=skill_command,
                )
            )
            results.append(node_result)
            if node_result.context_version is None:
                break
            current_base = node_result.context_version.version_id

        return Skill01SemanticCommitResult(
            preview=preview,
            node_results=tuple(results),
        )
