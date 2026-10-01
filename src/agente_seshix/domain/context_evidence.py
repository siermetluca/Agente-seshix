from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EvidenceClassification(str, Enum):
    FATTO = "FATTO"
    IPOTESI = "IPOTESI"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class Provenance:
    source_ref: str

    def __post_init__(self) -> None:
        if not self.source_ref.strip():
            raise ValueError("source_ref must not be empty")


@dataclass(frozen=True, slots=True)
class ContextValue:
    value: Any
    classification: EvidenceClassification
    provenance: tuple[Provenance, ...]
    version: str

    def __post_init__(self) -> None:
        if not self.version.strip():
            raise ValueError("version must not be empty")

        if self.classification is EvidenceClassification.FATTO and not self.provenance:
            raise ValueError("FATTO requires at least one provenance reference")

        if self.classification is EvidenceClassification.UNKNOWN and self.value is not None:
            raise ValueError("UNKNOWN must not assert a concrete value")
