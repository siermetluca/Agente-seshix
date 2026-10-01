from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any


@dataclass(frozen=True, slots=True)
class DependencyReference:
    dependency_id: str
    version_ref: str

    def __post_init__(self) -> None:
        if not self.dependency_id.strip():
            raise ValueError("dependency_id must not be empty")
        if not self.version_ref.strip():
            raise ValueError("version_ref must not be empty")


@dataclass(frozen=True, slots=True)
class DerivedState:
    state_id: str
    value: Any
    dependencies: tuple[DependencyReference, ...]
    stale: bool = False

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must not be empty")

    def mark_stale(self) -> "DerivedState":
        if self.stale:
            return self
        return replace(self, stale=True)
