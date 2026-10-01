import unittest

from agente_seshix.domain.task_context import ContextSection, Task, TaskContextRequirements


class TaskContextTests(unittest.TestCase):
    def test_valid_task(self) -> None:
        task = Task(
            task_id="TASK-0001",
            task_type="COMPANY_ANALYSIS",
            objective="Analyse the verified company context.",
        )
        self.assertEqual(task.task_type, "COMPANY_ANALYSIS")

    def test_empty_task_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Task("", "TYPE", "Objective")

    def test_empty_task_type_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Task("TASK-1", "   ", "Objective")

    def test_empty_objective_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Task("TASK-1", "TYPE", "")

    def test_context_sections_match_canonical_selectable_sections(self) -> None:
        self.assertEqual(
            {section.value for section in ContextSection},
            {"POLICY", "STATE", "DATA_EVIDENCE", "CAPABILITIES", "AUTHORITY"},
        )

    def test_valid_context_requirements(self) -> None:
        requirements = TaskContextRequirements(
            task_id="TASK-0001",
            required_sections=(ContextSection.STATE, ContextSection.DATA_EVIDENCE),
            optional_sections=(ContextSection.CAPABILITIES,),
        )
        self.assertIn(ContextSection.STATE, requirements.required_sections)

    def test_empty_requirements_task_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TaskContextRequirements("", ())

    def test_duplicate_required_section_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TaskContextRequirements(
                "TASK-1",
                (ContextSection.STATE, ContextSection.STATE),
            )

    def test_duplicate_optional_section_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TaskContextRequirements(
                "TASK-1",
                (),
                (ContextSection.AUTHORITY, ContextSection.AUTHORITY),
            )

    def test_required_optional_overlap_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TaskContextRequirements(
                "TASK-1",
                (ContextSection.POLICY,),
                (ContextSection.POLICY,),
            )


if __name__ == "__main__":
    unittest.main()
