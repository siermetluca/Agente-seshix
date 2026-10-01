from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ContextSection(str, Enum):
    POLICY = "POLICY"
    STATE = "STATE"
    DATA_EVIDENCE = "DATA_EVIDENCE"
    CAPABILITIES = "CAPABILITIES"
    AUTHORITY = "AUTHORITY"


@dataclass(frozen=True, slots=True)
class Task:
    task_id: str
    task_type: str
    objective: str

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")
        if not self.task_type.strip():
            raise ValueError("task_type must not be empty")
        if not self.objective.strip():
            raise ValueError("objective must not be empty")


@dataclass(frozen=True, slots=True)
class TaskContextRequirements:
    task_id: str
    required_sections: tuple[ContextSection, ...]
    optional_sections: tuple[ContextSection, ...] = ()

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")

        if len(set(self.required_sections)) != len(self.required_sections):
            raise ValueError("required_sections must not contain duplicates")

        if len(set(self.optional_sections)) != len(self.optional_sections):
            raise ValueError("optional_sections must not contain duplicates")

        overlap = set(self.required_sections) & set(self.optional_sections)
        if overlap:
            raise ValueError("required_sections and optional_sections must not overlap")
