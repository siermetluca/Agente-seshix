from __future__ import annotations

from typing import Protocol, runtime_checkable

from agente_seshix.domain.evidence import Evidence


@runtime_checkable
class EvidenceRepository(Protocol):
    def save(self, evidence: Evidence) -> None:
        ...

    def get(self, evidence_id: str) -> Evidence | None:
        ...
