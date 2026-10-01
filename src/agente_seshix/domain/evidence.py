from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SourceReference:
    source_ref: str

    def __post_init__(self) -> None:
        if not self.source_ref.strip():
            raise ValueError("source_ref must not be empty")


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    claim: str
    evidence: Any
    source: SourceReference
    version: str

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id must not be empty")
        if not self.claim.strip():
            raise ValueError("claim must not be empty")
        if not self.version.strip():
            raise ValueError("version must not be empty")
