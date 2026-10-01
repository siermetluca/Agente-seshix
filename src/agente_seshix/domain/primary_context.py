from __future__ import annotations

from dataclasses import dataclass

from .context_evidence import ContextValue


@dataclass(frozen=True, slots=True)
class PrimaryContextRecord:
    record_id: str
    key: str
    value: ContextValue

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id must not be empty")
        if not self.key.strip():
            raise ValueError("key must not be empty")


@dataclass(frozen=True, slots=True)
class PrimaryContextVersion:
    version_id: str
    records: tuple[PrimaryContextRecord, ...]
    previous_version_id: str | None = None

    def __post_init__(self) -> None:
        if not self.version_id.strip():
            raise ValueError("version_id must not be empty")
        if self.previous_version_id is not None and not self.previous_version_id.strip():
            raise ValueError("previous_version_id must not be empty when provided")
