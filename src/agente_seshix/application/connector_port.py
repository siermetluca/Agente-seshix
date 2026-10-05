from __future__ import annotations

from typing import Protocol, runtime_checkable

from agente_seshix.domain.capability import CapabilityRequest
from agente_seshix.domain.connector import ConnectorResult


@runtime_checkable
class ConnectorPort(Protocol):
    @property
    def provider(self) -> str:
        ...

    @property
    def capabilities(self) -> tuple[str, ...]:
        ...

    def execute(self, request: CapabilityRequest) -> ConnectorResult:
        ...
