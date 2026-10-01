from __future__ import annotations

from dataclasses import dataclass

from agente_seshix.application.context_repository import PrimaryContextRepository
from agente_seshix.domain.primary_context import PrimaryContextRecord, PrimaryContextVersion


class BaseContextVersionNotFound(LookupError):
    pass


@dataclass(frozen=True, slots=True)
class UpdatePrimaryContextCommand:
    base_version_id: str
    new_version_id: str
    record: PrimaryContextRecord

    def __post_init__(self) -> None:
        if not self.base_version_id.strip():
            raise ValueError("base_version_id must not be empty")
        if not self.new_version_id.strip():
            raise ValueError("new_version_id must not be empty")


class UpdatePrimaryContextUseCase:
    def __init__(self, repository: PrimaryContextRepository) -> None:
        self._repository = repository

    def execute(self, command: UpdatePrimaryContextCommand) -> PrimaryContextVersion:
        base = self._repository.get(command.base_version_id)
        if base is None:
            raise BaseContextVersionNotFound(command.base_version_id)

        records = list(base.records)
        replacement_index = next(
            (index for index, record in enumerate(records) if record.key == command.record.key),
            None,
        )

        if replacement_index is None:
            records.append(command.record)
        else:
            records[replacement_index] = command.record

        new_version = PrimaryContextVersion(
            version_id=command.new_version_id,
            records=tuple(records),
            previous_version_id=base.version_id,
        )
        self._repository.save(new_version)
        return new_version
