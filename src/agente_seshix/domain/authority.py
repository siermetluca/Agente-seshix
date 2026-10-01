from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AuthorityOutcome(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRES_HITL = "REQUIRES_HITL"


@dataclass(frozen=True, slots=True)
class AuthorityDecision:
    decision_id: str
    actor_id: str
    action: str
    outcome: AuthorityOutcome
    policy_version: str
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.decision_id.strip():
            raise ValueError("decision_id must not be empty")
        if not self.actor_id.strip():
            raise ValueError("actor_id must not be empty")
        if not self.action.strip():
            raise ValueError("action must not be empty")
        if not self.policy_version.strip():
            raise ValueError("policy_version must not be empty")
        if self.reason is not None and not self.reason.strip():
            raise ValueError("reason must not be empty when provided")
