import unittest

from agente_seshix.application.skill_registry import (
    InvalidSkillTransition,
    SkillAlreadyRegistered,
    SkillNotFound,
    SkillRegistration,
    SkillRegistry,
    SkillState,
    SkillValidationRequired,
)


def make_skill(*, state: SkillState = SkillState.DRAFT) -> SkillRegistration:
    return SkillRegistration(
        skill_id="SKILL_01",
        version="0.1",
        domain="process.context",
        supported_task_types=("CONTEXT_BUILD", "CONTEXT_UPDATE"),
        compatibility=("foundation>=0.1",),
        state=state,
    )


class SkillRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SkillRegistry()

    def test_new_registration_is_draft(self) -> None:
        result = self.registry.register(make_skill())
        self.assertEqual(result.state, SkillState.DRAFT)

    def test_registration_cannot_start_active(self) -> None:
        with self.assertRaises(InvalidSkillTransition):
            self.registry.register(make_skill(state=SkillState.ACTIVE))

    def test_duplicate_registration_is_rejected(self) -> None:
        self.registry.register(make_skill())
        with self.assertRaises(SkillAlreadyRegistered):
            self.registry.register(make_skill())

    def test_draft_moves_to_testing(self) -> None:
        self.registry.register(make_skill())
        result = self.registry.start_testing("SKILL_01", "0.1")
        self.assertEqual(result.state, SkillState.TESTING)

    def test_direct_draft_to_active_is_rejected(self) -> None:
        self.registry.register(make_skill())
        with self.assertRaises(InvalidSkillTransition):
            self.registry.activate("SKILL_01", "0.1", validation_passed=True)

    def test_testing_without_validation_cannot_activate(self) -> None:
        self.registry.register(make_skill())
        self.registry.start_testing("SKILL_01", "0.1")
        with self.assertRaises(SkillValidationRequired):
            self.registry.activate("SKILL_01", "0.1", validation_passed=False)

    def test_testing_with_validation_can_activate(self) -> None:
        self.registry.register(make_skill())
        self.registry.start_testing("SKILL_01", "0.1")
        result = self.registry.activate("SKILL_01", "0.1", validation_passed=True)
        self.assertEqual(result.state, SkillState.ACTIVE)

    def test_active_can_be_deprecated(self) -> None:
        self.registry.register(make_skill())
        self.registry.start_testing("SKILL_01", "0.1")
        self.registry.activate("SKILL_01", "0.1", validation_passed=True)
        result = self.registry.deprecate("SKILL_01", "0.1")
        self.assertEqual(result.state, SkillState.DEPRECATED)

    def test_non_disabled_skill_can_be_disabled(self) -> None:
        self.registry.register(make_skill())
        result = self.registry.disable("SKILL_01", "0.1")
        self.assertEqual(result.state, SkillState.DISABLED)

    def test_disabled_state_is_terminal(self) -> None:
        self.registry.register(make_skill())
        self.registry.disable("SKILL_01", "0.1")
        with self.assertRaises(InvalidSkillTransition):
            self.registry.disable("SKILL_01", "0.1")
        with self.assertRaises(InvalidSkillTransition):
            self.registry.start_testing("SKILL_01", "0.1")

    def test_resolve_active_rejects_non_active(self) -> None:
        self.registry.register(make_skill())
        with self.assertRaises(SkillNotFound):
            self.registry.resolve_active("SKILL_01", "0.1")

    def test_resolve_active_returns_exact_version(self) -> None:
        self.registry.register(make_skill())
        self.registry.start_testing("SKILL_01", "0.1")
        self.registry.activate("SKILL_01", "0.1", validation_passed=True)
        result = self.registry.resolve_active("SKILL_01", "0.1")
        self.assertEqual((result.skill_id, result.version), ("SKILL_01", "0.1"))

    def test_multiple_versions_are_distinct_registrations(self) -> None:
        self.registry.register(make_skill())
        second = SkillRegistration(
            skill_id="SKILL_01",
            version="0.2",
            domain="process.context",
            supported_task_types=("CONTEXT_BUILD",),
            compatibility=("foundation>=0.1",),
        )
        self.registry.register(second)
        self.assertEqual(self.registry.get("SKILL_01", "0.1").version, "0.1")
        self.assertEqual(self.registry.get("SKILL_01", "0.2").version, "0.2")

    def test_skill_metadata_validation_rejects_duplicate_task_types(self) -> None:
        with self.assertRaises(ValueError):
            SkillRegistration(
                skill_id="SKILL_X",
                version="1",
                domain="domain",
                supported_task_types=("A", "A"),
                compatibility=(),
            )


if __name__ == "__main__":
    unittest.main()
