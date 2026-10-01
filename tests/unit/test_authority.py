import unittest

from agente_seshix.domain.authority import AuthorityDecision, AuthorityOutcome


class AuthorityDecisionTests(unittest.TestCase):
    def test_supported_outcomes_are_explicit(self) -> None:
        self.assertEqual(
            {item.value for item in AuthorityOutcome},
            {"ALLOW", "DENY", "REQUIRES_HITL"},
        )

    def test_valid_allow_decision(self) -> None:
        decision = AuthorityDecision(
            decision_id="AUTH-0001",
            actor_id="DEV_AGENT",
            action="read_repository",
            outcome=AuthorityOutcome.ALLOW,
            policy_version="0.1",
        )
        self.assertEqual(decision.outcome, AuthorityOutcome.ALLOW)

    def test_valid_hitl_decision(self) -> None:
        decision = AuthorityDecision(
            decision_id="AUTH-0002",
            actor_id="DEV_AGENT",
            action="merge_pull_request",
            outcome=AuthorityOutcome.REQUIRES_HITL,
            policy_version="0.1",
            reason="Human approval required by policy.",
        )
        self.assertEqual(decision.outcome, AuthorityOutcome.REQUIRES_HITL)

    def test_empty_decision_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AuthorityDecision("", "DEV_AGENT", "read_repository", AuthorityOutcome.ALLOW, "0.1")

    def test_empty_actor_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AuthorityDecision("AUTH-1", " ", "read_repository", AuthorityOutcome.ALLOW, "0.1")

    def test_empty_action_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AuthorityDecision("AUTH-1", "DEV_AGENT", " ", AuthorityOutcome.DENY, "0.1")

    def test_empty_policy_version_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AuthorityDecision("AUTH-1", "DEV_AGENT", "read_repository", AuthorityOutcome.ALLOW, "")

    def test_blank_optional_reason_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AuthorityDecision(
                "AUTH-1",
                "DEV_AGENT",
                "read_repository",
                AuthorityOutcome.ALLOW,
                "0.1",
                "   ",
            )


if __name__ == "__main__":
    unittest.main()
