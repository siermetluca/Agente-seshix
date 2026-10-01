from __future__ import annotations

from dataclasses import dataclass

from agente_seshix.application.context_repository import PrimaryContextRepository
from agente_seshix.application.evidence_repository import EvidenceRepository
from agente_seshix.domain.context_evidence import ContextValue, Provenance
from agente_seshix.domain.primary_context import PrimaryContextRecord, PrimaryContextVersion


class BaseContextVersionNotFound(LookupError):
    pass


class EvidenceNotFound(LookupError):
    def __init__(self, evidence_id: str) -> None:
        self.evidence_id = evidence_id
        super().__init__(evidence_id)


@dataclass(frozen=True, slots=True)
class UpdatePrimaryContextCommand:
    base_version_id: str
    new_version_id: str
    record: PrimaryContextRecord
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.base_version_id.strip():
            raise ValueError("base_version_id must not be empty")
        if not self.new_version_id.strip():
            raise ValueError("new_version_id must not be empty")
        if not self.evidence_ids:
            raise ValueError("evidence_ids must not be empty")
        if any(not evidence_id.strip() for evidence_id in self.evidence_ids):
            raise ValueError("evidence_ids must not contain empty values")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("evidence_ids must not contain duplicates")


class UpdatePrimaryContextUseCase:
    def __init__(
        self,
        repository: PrimaryContextRepository,
        evidence_repository: EvidenceRepository,
    ) -> None:
        self._repository = repository
        self._evidence_repository = evidence_repository

    def execute(self, command: UpdatePrimaryContextCommand) -> PrimaryContextVersion:
        base = self._repository.get(command.base_version_id)
        if base is None:
            raise BaseContextVersionNotFound(command.base_version_id)

        resolved_evidence = []
        for evidence_id in command.evidence_ids:
            evidence = self._evidence_repository.get(evidence_id)
            if evidence is None:
                raise EvidenceNotFound(evidence_id)
            resolved_evidence.append(evidence)

        verified_value = ContextValue(
            value=command.record.value.value,
            classification=command.record.value.classification,
            provenance=tuple(
                Provenance(
                    source_ref=evidence.source.source_ref,
                    evidence_id=evidence.evidence_id,
                )
                for evidence in resolved_evidence
            ),
            version=command.record.value.version,
        )
        verified_record = PrimaryContextRecord(
            record_id=command.record.record_id,
            key=command.record.key,
            value=verified_value,
        )

        records = list(base.records)
        replacement_index = next(
            (index for index, record in enumerate(records) if record.key == verified_record.key),
            None,
        )

        if replacement_index is None:
            records.append(verified_record)
        else:
            records[replacement_index] = verified_record

        new_version = PrimaryContextVersion(
            version_id=command.new_version_id,
            records=tuple(records),
            previous_version_id=base.version_id,
        )
        self._repository.save(new_version)
        return new_version
