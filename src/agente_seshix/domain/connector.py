from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class ConnectorResultState(str, Enum):
    EXECUTED = "EXECUTED"
    DENIED = "DENIED"
    FAILED = "FAILED"


@dataclass(frozen=True, slots=True)
class ConnectorAudit:
    request_id: str
    provider: str
    capability: str
    provider_calls: int
    resource: tuple[tuple[str, str], ...]
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")
        if not self.provider.strip():
            raise ValueError("provider must not be empty")
        if not self.capability.strip():
            raise ValueError("capability must not be empty")
        if self.provider_calls < 0:
            raise ValueError("provider_calls must be >= 0")
        if self.reason is not None and not self.reason.strip():
            raise ValueError("reason must not be empty when provided")


@dataclass(frozen=True, slots=True)
class ConnectorResult:
    state: ConnectorResultState
    audit: ConnectorAudit
    data: Mapping[str, Any] | None = None
