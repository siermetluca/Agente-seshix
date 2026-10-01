import unittest

from agente_seshix.application.task_context_resolver import (
    MissingRequiredContext,
    TaskContextRequirementsMismatch,
    TaskContextResolver,
)
from agente_seshix.domain.task_context import ContextSection, Task, TaskContextRequirements


class TaskContextResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Task(
            task_id="TASK-0001",
            task_type="COMPANY_ANALYSIS",
            objective="Analyse company context.",
        )
        self.resolver = TaskContextResolver()

    def test_resolves_required_and_available_optional_sections(self) -> None:
        requirements = TaskContextRequirements(
            task_id="TASK-0001",
            required_sections=(ContextSection.STATE, ContextSection.DATA_EVIDENCE),
            optional_sections=(ContextSection.CAPABILITIES, ContextSection.AUTHORITY),
        )
        package = self.resolver.resolve(
            self.task,
            requirements,
            {
                ContextSection.STATE: "state",
                ContextSection.DATA_EVIDENCE: "evidence",
                ContextSection.CAPABILITIES: "capabilities",
            },
        )
        self.assertEqual(package.task, self.task)
        self.assertEqual(package.get(ContextSection.STATE), "state")
        self.assertEqual(package.get(ContextSection.DATA_EVIDENCE), "evidence")
        self.assertEqual(package.get(ContextSection.CAPABILITIES), "capabilities")
        self.assertIsNone(package.get(ContextSection.AUTHORITY))

    def test_missing_required_context_is_rejected(self) -> None:
        requirements = TaskContextRequirements(
            task_id="TASK-0001",
            required_sections=(ContextSection.STATE, ContextSection.AUTHORITY),
        )
        with self.assertRaises(MissingRequiredContext) as error:
            self.resolver.resolve(
                self.task,
                requirements,
                {ContextSection.STATE: "state"},
            )
        self.assertEqual(error.exception.missing_sections, (ContextSection.AUTHORITY,))

    def test_requirements_for_different_task_are_rejected(self) -> None:
        requirements = TaskContextRequirements(
            task_id="TASK-OTHER",
            required_sections=(),
        )
        with self.assertRaises(TaskContextRequirementsMismatch):
            self.resolver.resolve(self.task, requirements, {})

    def test_unrequested_available_context_is_excluded(self) -> None:
        requirements = TaskContextRequirements(
            task_id="TASK-0001",
            required_sections=(ContextSection.STATE,),
        )
        package = self.resolver.resolve(
            self.task,
            requirements,
            {
                ContextSection.STATE: "state",
                ContextSection.POLICY: "policy",
                ContextSection.AUTHORITY: "authority",
            },
        )
        self.assertEqual(len(package.sections), 1)
        self.assertEqual(package.sections[0].section, ContextSection.STATE)


if __name__ == "__main__":
    unittest.main()
