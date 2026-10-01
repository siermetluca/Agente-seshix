import unittest

from agente_seshix.application.authority_policy import (
    AuthorityEvaluationContext,
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.domain.authority import AuthorityOutcome


def make_policy(**overrides: str) -> AuthorityPolicy:
    actions = {
        "read_repository": "ALLOW",
        "create_task_branch": "ALLOW_WITH_APPROVED_CHANGE_PLAN",
        "direct_write_main": "DENY",
        "merge_pull_request": "REQUIRES_RELEASE_GATE_AND_HITL",
        "destructive_operation": "REQUIRES_HITL",
    }
    actions.update(overrides)
    return AuthorityPolicy(
        version="0.1",
        actors=("HUMAN_OWNER", "DEV_AGENT"),
        actions=actions,
    )


class AuthorityPolicyEvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evaluator = AuthorityPolicyEvaluator()
        self.policy = make_policy()

    def evaluate(self, action: str, context: AuthorityEvaluationContext | None = None):
        return self.evaluator.evaluate(
            decision_id="AUTH-1",
            actor_id="DEV_AGENT",
            action=action,
            policy=self.policy,
            context=context,
        )

    def test_allow(self) -> None:
        self.assertEqual(self.evaluate("read_repository").outcome, AuthorityOutcome.ALLOW)

    def test_deny(self) -> None:
        self.assertEqual(self.evaluate("direct_write_main").outcome, AuthorityOutcome.DENY)

    def test_change_plan_rule_allows_when_approved(self) -> None:
        result = self.evaluate(
            "create_task_branch",
            AuthorityEvaluationContext(approved_change_plan=True),
        )
        self.assertEqual(result.outcome, AuthorityOutcome.ALLOW)

    def test_change_plan_rule_denies_without_approval(self) -> None:
        self.assertEqual(
            self.evaluate("create_task_branch").outcome,
            AuthorityOutcome.DENY,
        )

    def test_requires_hitl_without_approval(self) -> None:
        self.assertEqual(
            self.evaluate("destructive_operation").outcome,
            AuthorityOutcome.REQUIRES_HITL,
        )

    def test_requires_hitl_allows_after_approval(self) -> None:
        result = self.evaluate(
            "destructive_operation",
            AuthorityEvaluationContext(hitl_approved=True),
        )
        self.assertEqual(result.outcome, AuthorityOutcome.ALLOW)

    def test_release_rule_denies_before_release_gate(self) -> None:
        result = self.evaluate(
            "merge_pull_request",
            AuthorityEvaluationContext(hitl_approved=True),
        )
        self.assertEqual(result.outcome, AuthorityOutcome.DENY)

    def test_release_rule_requires_hitl_after_gate(self) -> None:
        result = self.evaluate(
            "merge_pull_request",
            AuthorityEvaluationContext(release_gate_pass=True),
        )
        self.assertEqual(result.outcome, AuthorityOutcome.REQUIRES_HITL)

    def test_release_rule_allows_when_gate_and_hitl_pass(self) -> None:
        result = self.evaluate(
            "merge_pull_request",
            AuthorityEvaluationContext(release_gate_pass=True, hitl_approved=True),
        )
        self.assertEqual(result.outcome, AuthorityOutcome.ALLOW)

    def test_unknown_actor_fails_closed(self) -> None:
        result = self.evaluator.evaluate(
            decision_id="AUTH-1",
            actor_id="UNKNOWN",
            action="read_repository",
            policy=self.policy,
        )
        self.assertEqual(result.outcome, AuthorityOutcome.DENY)

    def test_unknown_action_fails_closed(self) -> None:
        self.assertEqual(self.evaluate("unknown_action").outcome, AuthorityOutcome.DENY)

    def test_unknown_expression_fails_closed(self) -> None:
        policy = make_policy(read_repository="UNSUPPORTED")
        result = self.evaluator.evaluate(
            decision_id="AUTH-1",
            actor_id="DEV_AGENT",
            action="read_repository",
            policy=policy,
        )
        self.assertEqual(result.outcome, AuthorityOutcome.DENY)

    def test_decision_is_bound_to_policy_version(self) -> None:
        result = self.evaluate("read_repository")
        self.assertEqual(result.policy_version, "0.1")
        self.assertEqual(result.actor_id, "DEV_AGENT")
        self.assertEqual(result.action, "read_repository")


if __name__ == "__main__":
    unittest.main()
