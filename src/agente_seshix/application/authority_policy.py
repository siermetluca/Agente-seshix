from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from agente_seshix.domain.authority import AuthorityDecision, AuthorityOutcome


@dataclass(frozen=True, slots=True)
class AuthorityPolicy:
    version: str
    actors: tuple[str, ...]
    actions: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.version.strip():
            raise ValueError("version must not be empty")
        if len(set(self.actors)) != len(self.actors):
            raise ValueError("actors must not contain duplicates")


@dataclass(frozen=True, slots=True)
class AuthorityEvaluationContext:
    approved_change_plan: bool = False
    release_gate_pass: bool = False
    hitl_approved: bool = False


class AuthorityPolicyEvaluator:
    def evaluate(
        self,
        *,
        decision_id: str,
        actor_id: str,
        action: str,
        policy: AuthorityPolicy,
        context: AuthorityEvaluationContext | None = None,
    ) -> AuthorityDecision:
        context = context or AuthorityEvaluationContext()

        if actor_id not in policy.actors:
            return AuthorityDecision(
                decision_id=decision_id,
                actor_id=actor_id,
                action=action,
                outcome=AuthorityOutcome.DENY,
                policy_version=policy.version,
                reason="unknown actor",
            )

        expression = policy.actions.get(action)
        if expression is None:
            return AuthorityDecision(
                decision_id=decision_id,
                actor_id=actor_id,
                action=action,
                outcome=AuthorityOutcome.DENY,
                policy_version=policy.version,
                reason="unknown action",
            )

        outcome, reason = self._evaluate_expression(expression, context)
        return AuthorityDecision(
            decision_id=decision_id,
            actor_id=actor_id,
            action=action,
            outcome=outcome,
            policy_version=policy.version,
            reason=reason,
        )

    def _evaluate_expression(
        self,
        expression: str,
        context: AuthorityEvaluationContext,
    ) -> tuple[AuthorityOutcome, str]:
        if expression == "ALLOW":
            return AuthorityOutcome.ALLOW, "policy allows action"

        if expression == "DENY":
            return AuthorityOutcome.DENY, "policy denies action"

        if expression == "ALLOW_WITH_APPROVED_CHANGE_PLAN":
            if context.approved_change_plan:
                return AuthorityOutcome.ALLOW, "approved change plan present"
            return AuthorityOutcome.DENY, "approved change plan required"

        if expression == "REQUIRES_HITL":
            if context.hitl_approved:
                return AuthorityOutcome.ALLOW, "required HITL approval present"
            return AuthorityOutcome.REQUIRES_HITL, "HITL approval required"

        if expression == "REQUIRES_RELEASE_GATE_AND_HITL":
            if not context.release_gate_pass:
                return AuthorityOutcome.DENY, "release gate must pass before HITL"
            if not context.hitl_approved:
                return AuthorityOutcome.REQUIRES_HITL, "release gate passed; HITL approval required"
            return AuthorityOutcome.ALLOW, "release gate and HITL approval satisfied"

        return AuthorityOutcome.DENY, "unknown policy expression"
