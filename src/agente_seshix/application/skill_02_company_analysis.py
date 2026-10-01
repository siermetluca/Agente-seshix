from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from agente_seshix.domain.context_evidence import EvidenceClassification
from agente_seshix.domain.derived_state import DependencyReference, DerivedState
from agente_seshix.domain.primary_context import PrimaryContextVersion


class CompanyAnalysisValidationError(ValueError):
    pass


class AnalysisCategory(str, Enum):
    CRITICITA = "CRITICITA"
    INEFFICIENZA = "INEFFICIENZA"
    ASSET = "ASSET"
    CAPABILITY = "CAPABILITY"
    GAP = "GAP"
    IMPROVEMENT_AREA = "IMPROVEMENT_AREA"
    RISK = "RISK"
    HYPOTHESIS = "HYPOTHESIS"


class CompanyAnalysisStatus(str, Enum):
    ANALYZED = "ANALYZED"
    PARTIAL_NEEDS_CONTEXT = "PARTIAL_NEEDS_CONTEXT"
    NEEDS_CONTEXT = "NEEDS_CONTEXT"
    NO_FINDINGS = "NO_FINDINGS"


@dataclass(frozen=True, slots=True)
class CompanyAnalysisRequest:
    analysis_id: str
    primary_context: PrimaryContextVersion

    def __post_init__(self) -> None:
        if not self.analysis_id.strip():
            raise ValueError("analysis_id must not be empty")
@dataclass(frozen=True, slots=True)
class RawAnalysisFinding:
    finding_id: Any
    category: Any
    statement: Any
    basis_keys: Any


@dataclass(frozen=True, slots=True)
class RawContextChangeCandidate:
    candidate_id: Any
    requested_information: Any
    reason: Any
    requested_key: Any = None


@dataclass(frozen=True, slots=True)
class RawCompanyAnalysisOutput:
    findings: tuple[RawAnalysisFinding, ...]
    context_change_candidates: tuple[RawContextChangeCandidate, ...] = ()


@runtime_checkable
class CompanyAnalysisPort(Protocol):
    def analyze(self, request: CompanyAnalysisRequest) -> RawCompanyAnalysisOutput:
        ...


@dataclass(frozen=True, slots=True)
class AnalysisFinding:
    finding_id: str
    category: AnalysisCategory
    statement: str
    basis_keys: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ContextChangeCandidate:
    candidate_id: str
    source_skill: str
    requested_information: str
    reason: str
    requested_key: str | None = None
@dataclass(frozen=True, slots=True)
class CompanyAnalysisBaseline:
    analysis_id: str
    primary_context_version_id: str
    status: CompanyAnalysisStatus
    findings: tuple[AnalysisFinding, ...]
    context_change_candidates: tuple[ContextChangeCandidate, ...]


@dataclass(frozen=True, slots=True)
class Skill02CompanyAnalysisResult:
    baseline: CompanyAnalysisBaseline
    derived_state: DerivedState


class CompanyAnalysisValidator:
    def validate(
        self,
        request: CompanyAnalysisRequest,
        raw: RawCompanyAnalysisOutput,
    ) -> CompanyAnalysisBaseline:
        if not isinstance(raw, RawCompanyAnalysisOutput):
            raise CompanyAnalysisValidationError(
                "analysis provider output must be RawCompanyAnalysisOutput"
            )

        context_by_key = {
            record.key: record.value
            for record in request.primary_context.records
        }

        findings = tuple(
            self._validate_finding(item, context_by_key)
            for item in raw.findings
        )
        candidates = tuple(
            self._validate_context_candidate(item, context_by_key)
            for item in raw.context_change_candidates
        )
        self._require_unique_ids(findings, candidates)

        return CompanyAnalysisBaseline(
            analysis_id=request.analysis_id,
            primary_context_version_id=request.primary_context.version_id,
            status=self._status(findings, candidates),
            findings=findings,
            context_change_candidates=candidates,
        )
    def _validate_finding(
        self,
        raw: RawAnalysisFinding,
        context_by_key: dict[str, Any],
    ) -> AnalysisFinding:
        if not isinstance(raw, RawAnalysisFinding):
            raise CompanyAnalysisValidationError(
                "finding must be RawAnalysisFinding"
            )
        finding_id = self._required_text(raw.finding_id, "finding_id")
        statement = self._required_text(raw.statement, "statement")

        try:
            category = (
                raw.category
                if isinstance(raw.category, AnalysisCategory)
                else AnalysisCategory(self._required_text(raw.category, "category"))
            )
        except ValueError as error:
            raise CompanyAnalysisValidationError(
                f"unsupported analysis category: {raw.category!r}"
            ) from error

        if not isinstance(raw.basis_keys, (tuple, list)):
            raise CompanyAnalysisValidationError(
                "basis_keys must be a tuple/list"
            )
        basis_keys = tuple(
            self._required_text(key, "basis_key")
            for key in raw.basis_keys
        )
        if not basis_keys:
            raise CompanyAnalysisValidationError(
                "every finding requires at least one PRIMARY_CONTEXT basis key"
            )
        if len(set(basis_keys)) != len(basis_keys):
            raise CompanyAnalysisValidationError(
                "basis_keys must not contain duplicates"
            )

        for key in basis_keys:
            if key not in context_by_key:
                raise CompanyAnalysisValidationError(
                    f"finding references unsupported context key: {key}"
                )
            value = context_by_key[key]
            if value.classification is EvidenceClassification.UNKNOWN:
                raise CompanyAnalysisValidationError(
                    f"UNKNOWN context cannot support finding: {key}"
                )
            if (
                value.classification is EvidenceClassification.IPOTESI
                and category is not AnalysisCategory.HYPOTHESIS
            ):
                raise CompanyAnalysisValidationError(
                    "IPOTESI context may only support HYPOTHESIS findings"
                )

        return AnalysisFinding(
            finding_id=finding_id,
            category=category,
            statement=statement,
            basis_keys=basis_keys,
        )
    def _validate_context_candidate(
        self,
        raw: RawContextChangeCandidate,
        context_by_key: dict[str, Any],
    ) -> ContextChangeCandidate:
        if not isinstance(raw, RawContextChangeCandidate):
            raise CompanyAnalysisValidationError(
                "context candidate must be RawContextChangeCandidate"
            )
        candidate_id = self._required_text(raw.candidate_id, "candidate_id")
        requested_information = self._required_text(
            raw.requested_information,
            "requested_information",
        )
        reason = self._required_text(raw.reason, "reason")

        requested_key = raw.requested_key
        if requested_key is not None:
            requested_key = self._required_text(requested_key, "requested_key")
            existing = context_by_key.get(requested_key)
            if (
                existing is not None
                and existing.classification is not EvidenceClassification.UNKNOWN
            ):
                raise CompanyAnalysisValidationError(
                    f"context candidate requests already known key: {requested_key}"
                )

        return ContextChangeCandidate(
            candidate_id=candidate_id,
            source_skill="SKILL_02",
            requested_information=requested_information,
            reason=reason,
            requested_key=requested_key,
        )

    def _require_unique_ids(
        self,
        findings: tuple[AnalysisFinding, ...],
        candidates: tuple[ContextChangeCandidate, ...],
    ) -> None:
        finding_ids = [item.finding_id for item in findings]
        if len(set(finding_ids)) != len(finding_ids):
            raise CompanyAnalysisValidationError("duplicate finding_id")
        candidate_ids = [item.candidate_id for item in candidates]
        if len(set(candidate_ids)) != len(candidate_ids):
            raise CompanyAnalysisValidationError("duplicate candidate_id")
    def _status(
        self,
        findings: tuple[AnalysisFinding, ...],
        candidates: tuple[ContextChangeCandidate, ...],
    ) -> CompanyAnalysisStatus:
        if findings and candidates:
            return CompanyAnalysisStatus.PARTIAL_NEEDS_CONTEXT
        if candidates:
            return CompanyAnalysisStatus.NEEDS_CONTEXT
        if findings:
            return CompanyAnalysisStatus.ANALYZED
        return CompanyAnalysisStatus.NO_FINDINGS

    def _required_text(self, value: Any, name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise CompanyAnalysisValidationError(
                f"{name} must be a non-empty string"
            )
        return value.strip()


class Skill02CompanyAnalysisRuntime:
    SKILL_ID = "SKILL_02"

    def __init__(
        self,
        provider: CompanyAnalysisPort,
        validator: CompanyAnalysisValidator | None = None,
    ) -> None:
        if not isinstance(provider, CompanyAnalysisPort):
            raise TypeError("provider must implement CompanyAnalysisPort")
        self._provider = provider
        self._validator = validator or CompanyAnalysisValidator()

    def analyze(
        self,
        *,
        analysis_id: str,
        primary_context: PrimaryContextVersion,
    ) -> Skill02CompanyAnalysisResult:
        request = CompanyAnalysisRequest(
            analysis_id=analysis_id,
            primary_context=primary_context,
        )

        if not primary_context.records:
            baseline = CompanyAnalysisBaseline(
                analysis_id=analysis_id,
                primary_context_version_id=primary_context.version_id,
                status=CompanyAnalysisStatus.NEEDS_CONTEXT,
                findings=(),
                context_change_candidates=(
                    ContextChangeCandidate(
                        candidate_id=f"{analysis_id}:CTX:1",
                        source_skill=self.SKILL_ID,
                        requested_information=(
                            "company context baseline sufficient for internal analysis"
                        ),
                        reason=(
                            "PRIMARY_CONTEXT contains no records; internal company "
                            "analysis would be unsupported"
                        ),
                    ),
                ),
            )
        else:
            raw = self._provider.analyze(request)
            baseline = self._validator.validate(request, raw)

        derived = DerivedState(
            state_id=f"{analysis_id}:ANALISI_AZIENDALE_BASELINE",
            value=baseline,
            dependencies=(
                DependencyReference(
                    dependency_id="PRIMARY_CONTEXT",
                    version_ref=primary_context.version_id,
                ),
            ),
        )
        return Skill02CompanyAnalysisResult(
            baseline=baseline,
            derived_state=derived,
        )
