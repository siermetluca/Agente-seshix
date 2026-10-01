from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agente_seshix.application.evidence_repository import EvidenceRepository
from agente_seshix.domain.evidence import Evidence, SourceReference


class EvidenceAlreadyExists(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class EvidenceIntakeCommand:
    evidence_id: str
    source_ref: str
    claim: str
    evidence: Any
    version: str

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id must not be empty")
        if not self.source_ref.strip():
            raise ValueError("source_ref must not be empty")
        if not self.claim.strip():
            raise ValueError("claim must not be empty")
        if not self.version.strip():
            raise ValueError("version must not be empty")


class EvidenceIntakeUseCase:
    def __init__(self, repository: EvidenceRepository) -> None:
        self._repository = repository

    def execute(self, command: EvidenceIntakeCommand) -> Evidence:
        if self._repository.get(command.evidence_id) is not None:
            raise EvidenceAlreadyExists(command.evidence_id)

        evidence = Evidence(
            evidence_id=command.evidence_id,
            claim=command.claim,
            evidence=command.evidence,
            source=SourceReference(command.source_ref),
            version=command.version,
        )
        self._repository.save(evidence)
        return evidence
