from __future__ import annotations

from typing import Protocol, runtime_checkable

from agente_seshix.domain.primary_context import PrimaryContextVersion


@runtime_checkable
class PrimaryContextRepository(Protocol):
    def save(self, version: PrimaryContextVersion) -> None:
        ...

    def get(self, version_id: str) -> PrimaryContextVersion | None:
        ...
