from __future__ import annotations

import os

from agente_seshix.application.authority_policy import (
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.evidence_intake import EvidenceIntakeUseCase
from agente_seshix.application.flow_execution import FlowExecutionEnvelope
from agente_seshix.application.semantic_model import StructuredSemanticService
from agente_seshix.application.skill_01_context import Skill01ContextRuntime
from agente_seshix.application.skill_01_node import Skill01NodeRuntime
from agente_seshix.application.skill_01_semantic_intake import (
    Skill01SemanticIntakeService,
)
from agente_seshix.application.skill_02_company_analysis import (
    CompanyAnalysisValidationError,
    Skill02CompanyAnalysisRuntime,
)
from agente_seshix.application.skill_registry import SkillRegistration, SkillRegistry
from agente_seshix.application.task_context_resolver import TaskContextResolver
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import Task, TaskContextRequirements
from agente_seshix.infrastructure.ollama_company_analysis import (
    OllamaCompanyAnalysis,
    OllamaCompanyAnalysisError,
)
from agente_seshix.infrastructure.ollama_semantic_model import (
    OllamaSemanticModel,
    OllamaSemanticModelError,
)


class EvidenceRepo:
    def __init__(self) -> None:
        self.items: dict[str, Evidence] = {}

    def save(self, evidence: Evidence) -> None:
        self.items[evidence.evidence_id] = evidence

    def get(self, evidence_id: str) -> Evidence | None:
        return self.items.get(evidence_id)


class ContextRepo:
    def __init__(self) -> None:
        self.items: dict[str, PrimaryContextVersion] = {
            "PCV-0": PrimaryContextVersion("PCV-0", ())
        }

    def save(self, version: PrimaryContextVersion) -> None:
        self.items[version.version_id] = version

    def get(self, version_id: str) -> PrimaryContextVersion | None:
        return self.items.get(version_id)
def build_skill01():
    evidence_repo = EvidenceRepo()
    context_repo = ContextRepo()
    registry = SkillRegistry()
    registry.register(
        SkillRegistration(
            skill_id="SKILL_01",
            version="0.1",
            domain="process.context",
            supported_task_types=("CONTEXT_BUILD", "CONTEXT_UPDATE"),
            compatibility=("foundation>=0.1",),
        )
    )
    registry.start_testing("SKILL_01", "0.1")
    registry.activate("SKILL_01", "0.1", validation_passed=True)

    node = Skill01NodeRuntime(
        context_resolver=TaskContextResolver(),
        skill_registry=registry,
        authority_evaluator=AuthorityPolicyEvaluator(),
        evidence_intake=EvidenceIntakeUseCase(evidence_repo),
        skill_runtime=Skill01ContextRuntime(context_repo, evidence_repo),
        flow=FlowExecutionEnvelope(),
    )
    model = os.environ.get("AGENTE_SESHIX_SEMANTIC_MODEL", "qwen2.5:3b")
    service = Skill01SemanticIntakeService(
        StructuredSemanticService(OllamaSemanticModel(model=model)),
        node,
    )
    return service, context_repo


def show_skill01_preview(preview) -> None:
    print("\n=== PRIMARY_CONTEXT PREVIEW ===")
    for candidate in preview.accepted_candidates:
        print(
            f"- {candidate.key} = {candidate.value!r} "
            f"[{candidate.classification.value}]"
        )
    if preview.clarification_questions:
        print("Chiarimenti:")
        for question in preview.clarification_questions:
            print(f"- {question}")
    print("=== END PRIMARY_CONTEXT PREVIEW ===\n")


def analyze_skill01(service, source_text: str):
    try:
        return service.analyze(
            request_id="SKILL02-HUMAN-CONTEXT",
            source_text=source_text,
            source_ref="human://owner",
        )
    except (ValueError, OllamaSemanticModelError) as error:
        print(f"SKILL_01 ANALYSIS BLOCKED: {error}")
        return None
def build_context(service, context_repo, source_text: str):
    preview = analyze_skill01(service, source_text)
    if preview is None:
        return None

    enriched = source_text
    for round_index in range(1, 4):
        show_skill01_preview(preview)
        if not preview.clarification_questions:
            break
        additions = []
        for question in preview.clarification_questions:
            answer = input(f"{question} ").strip()
            if answer:
                additions.append(f"{question} Risposta: {answer}")
        if not additions:
            break
        enriched += "\n" + "\n".join(additions)
        preview = analyze_skill01(service, enriched)
        if preview is None:
            return None

    if not preview.accepted_candidates:
        print("Nessun PRIMARY_CONTEXT sufficiente per SKILL_02.")
        return None

    confirmed = input(
        "Confermi il PRIMARY_CONTEXT estratto prima dell'analisi aziendale? [s/N]: "
    ).strip().lower()
    if confirmed not in {"s", "si", "sì", "y", "yes"}:
        print("Contesto non confermato. Nessuna analisi SKILL_02 eseguita.")
        return None

    task = Task(
        "SKILL02-HUMAN-CONTEXT-TASK",
        "CONTEXT_BUILD",
        "Build context for SKILL_02 human validation",
    )
    result = service.commit(
        preview,
        task=task,
        context_requirements=TaskContextRequirements(task.task_id, ()),
        available_context={},
        skill_version="0.1",
        actor_id="HUMAN_TEST_AGENT",
        authority_action="execute_skill",
        authority_policy=AuthorityPolicy(
            version="human-skill02",
            actors=("HUMAN_TEST_AGENT",),
            actions={"execute_skill": "ALLOW"},
        ),
    )
    version_id = result.final_context_version_id
    if version_id is None:
        print("SKILL_01 non ha prodotto una versione di contesto.")
        return None
    return context_repo.get(version_id)
def show_analysis(result) -> None:
    baseline = result.baseline
    print("\n=== ANALISI_AZIENDALE_BASELINE ===")
    print(f"status                  : {baseline.status.value}")
    print(f"primary_context_version : {baseline.primary_context_version_id}")

    print("\nFINDINGS:")
    if not baseline.findings:
        print("- nessun finding")
    for finding in baseline.findings:
        print(f"- [{finding.category.value}] {finding.statement}")
        print(f"  basis_keys: {', '.join(finding.basis_keys)}")

    print("\nCONTEXT_CHANGE_CANDIDATES:")
    if not baseline.context_change_candidates:
        print("- nessun dato aggiuntivo richiesto")
    for candidate in baseline.context_change_candidates:
        print(f"- {candidate.requested_information}")
        print(f"  reason       : {candidate.reason}")
        print(f"  requested_key: {candidate.requested_key or '-'}")
        print(f"  route        : {candidate.source_skill} -> SKILL_01")

    print("\nDERIVED STATE:")
    print(f"- state_id    : {result.derived_state.state_id}")
    print(
        "- dependency  : "
        f"{result.derived_state.dependencies[0].dependency_id}"
        f"@{result.derived_state.dependencies[0].version_ref}"
    )
    print("=== END ANALYSIS ===\n")
def main() -> None:
    semantic_model = os.environ.get(
        "AGENTE_SESHIX_SEMANTIC_MODEL",
        "qwen2.5:3b",
    )
    analysis_model = os.environ.get(
        "AGENTE_SESHIX_ANALYSIS_MODEL",
        "qwen2.5:3b",
    )

    print("==============================================")
    print(" SKILL_02 HUMAN ACCEPTANCE TEST")
    print("==============================================")
    print(f"SKILL_01 semantic model : {semantic_model}")
    print(f"SKILL_02 analysis model : {analysis_model}")
    print()
    print("Descrivi l'azienda con fatti che conosci.")
    print("SKILL_02 deve analizzare solo ciò che entra nel PRIMARY_CONTEXT.")
    source_text = input("Descrizione azienda: ").strip()
    if not source_text:
        raise SystemExit("Descrizione vuota: test annullato.")

    skill01, context_repo = build_skill01()
    primary_context = build_context(
        skill01,
        context_repo,
        source_text,
    )
    if primary_context is None:
        return

    print("\nAnalisi SKILL_02 locale in corso...")
    runtime = Skill02CompanyAnalysisRuntime(
        OllamaCompanyAnalysis(model=analysis_model)
    )
    try:
        result = runtime.analyze(
            analysis_id="SKILL02-HUMAN",
            primary_context=primary_context,
        )
    except (CompanyAnalysisValidationError, OllamaCompanyAnalysisError) as error:
        print(f"SKILL_02 BLOCKED: {error}")
        print("Nessuna activation può avvenire.")
        return

    show_analysis(result)
    accepted = input(
        "L'analisi è coerente e non inventa problemi/dati? [s/N]: "
    ).strip().lower()
    if accepted not in {"s", "si", "sì", "y", "yes"}:
        print("HUMAN ACCEPTANCE NON APPROVATA.")
        return

    print("HUMAN TEST APPROVATO NELLA SESSIONE LOCALE.")
    print(
        "SKILL_02_ACTIVATION resta PENDING finché non confermi "
        "esplicitamente l'acceptance nella conversazione."
    )


if __name__ == "__main__":
    main()
