from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from agente_seshix.application.context_repository import PrimaryContextRepository
from agente_seshix.application.evidence_repository import EvidenceRepository
from agente_seshix.application.update_primary_context import (
    EvidenceNotFound,
    UpdatePrimaryContextCommand,
    UpdatePrimaryContextUseCase,
)
from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)
from agente_seshix.domain.primary_context import PrimaryContextRecord, PrimaryContextVersion


class Skill01ContextStatus(str, Enum):
    WRITTEN = "WRITTEN"
    WAITING_HITL = "WAITING_HITL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class Skill01ContextCommand:
    base_version_id: str
    new_version_id: str
    record_id: str
    key: str
    classification: EvidenceClassification
    context_value_version: str
    evidence_id: str | None = None
    proposed_value: Any = None
    required: bool = True

    def __post_init__(self) -> None:
        for name, value in (
            ("base_version_id", self.base_version_id),
            ("new_version_id", self.new_version_id),
            ("record_id", self.record_id),
            ("key", self.key),
            ("context_value_version", self.context_value_version),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if self.classification is EvidenceClassification.UNKNOWN:
            if self.proposed_value is not None:
                raise ValueError("UNKNOWN must not assert a concrete value")
            if self.evidence_id is not None:
                raise ValueError("UNKNOWN must not declare evidence_id in v1")
            return

        if self.evidence_id is None or not self.evidence_id.strip():
            raise ValueError("written FATTO/IPOTESI requires evidence_id")

        if self.classification is EvidenceClassification.FATTO and self.proposed_value is not None:
            raise ValueError("FATTO value must come directly from Evidence payload")

        if self.classification is EvidenceClassification.IPOTESI and self.proposed_value is None:
            raise ValueError("IPOTESI requires proposed_value")


@dataclass(frozen=True, slots=True)
class Skill01ContextResult:
    status: Skill01ContextStatus
    classification: EvidenceClassification
    context_version: PrimaryContextVersion | None = None
    stop_reason: str | None = None


class Skill01ContextRuntime:
    def __init__(
        self,
        context_repository: PrimaryContextRepository,
        evidence_repository: EvidenceRepository,
    ) -> None:
        self._evidence_repository = evidence_repository
        self._updater = UpdatePrimaryContextUseCase(
            context_repository,
            evidence_repository,
        )

    def execute(self, command: Skill01ContextCommand) -> Skill01ContextResult:
        if command.classification is EvidenceClassification.UNKNOWN:
            if command.required:
                return Skill01ContextResult(
                    status=Skill01ContextStatus.WAITING_HITL,
                    classification=command.classification,
                    stop_reason=f"required context missing: {command.key}",
                )
            return Skill01ContextResult(
                status=Skill01ContextStatus.UNKNOWN,
                classification=command.classification,
                stop_reason=f"context remains UNKNOWN: {command.key}",
            )

        evidence = self._evidence_repository.get(command.evidence_id or "")
        if evidence is None:
            raise EvidenceNotFound(command.evidence_id or "")

        if command.classification is EvidenceClassification.FATTO:
            value = evidence.evidence
        else:
            value = command.proposed_value

        record = PrimaryContextRecord(
            record_id=command.record_id,
            key=command.key,
            value=ContextValue(
                value=value,
                classification=command.classification,
                provenance=(
                    Provenance(
                        source_ref=evidence.source.source_ref,
                        evidence_id=evidence.evidence_id,
                    ),
                ),
                version=command.context_value_version,
            ),
        )
        context_version = self._updater.execute(
            UpdatePrimaryContextCommand(
                base_version_id=command.base_version_id,
                new_version_id=command.new_version_id,
                record=record,
                evidence_ids=(evidence.evidence_id,),
            )
        )
        return Skill01ContextResult(
            status=Skill01ContextStatus.WRITTEN,
            classification=command.classification,
            context_version=context_version,
        )
