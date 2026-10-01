from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from agente_seshix.domain.task_context import ContextSection, Task, TaskContextRequirements


class MissingRequiredContext(LookupError):
    def __init__(self, missing_sections: tuple[ContextSection, ...]) -> None:
        self.missing_sections = missing_sections
        names = ", ".join(section.value for section in missing_sections)
        super().__init__(f"missing required context: {names}")


class TaskContextRequirementsMismatch(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ResolvedContextSection:
    section: ContextSection
    value: Any


@dataclass(frozen=True, slots=True)
class TaskContextPackage:
    task: Task
    sections: tuple[ResolvedContextSection, ...]

    def get(self, section: ContextSection) -> Any | None:
        for item in self.sections:
            if item.section is section:
                return item.value
        return None


class TaskContextResolver:
    def resolve(
        self,
        task: Task,
        requirements: TaskContextRequirements,
        available_context: Mapping[ContextSection, Any],
    ) -> TaskContextPackage:
        if requirements.task_id != task.task_id:
            raise TaskContextRequirementsMismatch(
                f"requirements task_id {requirements.task_id!r} does not match task {task.task_id!r}"
            )

        missing = tuple(
            section
            for section in requirements.required_sections
            if section not in available_context
        )
        if missing:
            raise MissingRequiredContext(missing)

        requested = requirements.required_sections + requirements.optional_sections
        resolved = tuple(
            ResolvedContextSection(section=section, value=available_context[section])
            for section in requested
            if section in available_context
        )
        return TaskContextPackage(task=task, sections=resolved)
