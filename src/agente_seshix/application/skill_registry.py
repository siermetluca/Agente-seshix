from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class SkillState(str, Enum):
    DRAFT = "DRAFT"
    TESTING = "TESTING"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    DISABLED = "DISABLED"


class SkillAlreadyRegistered(ValueError):
    pass


class SkillNotFound(LookupError):
    pass


class InvalidSkillTransition(ValueError):
    pass


class SkillValidationRequired(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class SkillRegistration:
    skill_id: str
    version: str
    domain: str
    supported_task_types: tuple[str, ...]
    compatibility: tuple[str, ...]
    state: SkillState = SkillState.DRAFT

    def __post_init__(self) -> None:
        if not self.skill_id.strip():
            raise ValueError("skill_id must not be empty")
        if not self.version.strip():
            raise ValueError("version must not be empty")
        if not self.domain.strip():
            raise ValueError("domain must not be empty")
        if len(set(self.supported_task_types)) != len(self.supported_task_types):
            raise ValueError("supported_task_types must not contain duplicates")
        if any(not item.strip() for item in self.supported_task_types):
            raise ValueError("supported_task_types must not contain empty values")
        if len(set(self.compatibility)) != len(self.compatibility):
            raise ValueError("compatibility must not contain duplicates")
        if any(not item.strip() for item in self.compatibility):
            raise ValueError("compatibility must not contain empty values")


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[tuple[str, str], SkillRegistration] = {}

    def register(self, registration: SkillRegistration) -> SkillRegistration:
        if registration.state is not SkillState.DRAFT:
            raise InvalidSkillTransition("new skill registrations must start in DRAFT")

        key = (registration.skill_id, registration.version)
        if key in self._skills:
            raise SkillAlreadyRegistered(f"skill already registered: {registration.skill_id}@{registration.version}")

        self._skills[key] = registration
        return registration

    def get(self, skill_id: str, version: str) -> SkillRegistration:
        key = (skill_id, version)
        try:
            return self._skills[key]
        except KeyError as error:
            raise SkillNotFound(f"skill not found: {skill_id}@{version}") from error

    def start_testing(self, skill_id: str, version: str) -> SkillRegistration:
        current = self.get(skill_id, version)
        if current.state is not SkillState.DRAFT:
            raise InvalidSkillTransition(f"cannot move {current.state.value} to TESTING")
        return self._replace_state(current, SkillState.TESTING)

    def activate(
        self,
        skill_id: str,
        version: str,
        *,
        validation_passed: bool,
    ) -> SkillRegistration:
        current = self.get(skill_id, version)
        if current.state is not SkillState.TESTING:
            raise InvalidSkillTransition(f"cannot move {current.state.value} to ACTIVE")
        if not validation_passed:
            raise SkillValidationRequired("validation_passed must be true before activation")
        return self._replace_state(current, SkillState.ACTIVE)

    def deprecate(self, skill_id: str, version: str) -> SkillRegistration:
        current = self.get(skill_id, version)
        if current.state is not SkillState.ACTIVE:
            raise InvalidSkillTransition(f"cannot move {current.state.value} to DEPRECATED")
        return self._replace_state(current, SkillState.DEPRECATED)

    def disable(self, skill_id: str, version: str) -> SkillRegistration:
        current = self.get(skill_id, version)
        if current.state is SkillState.DISABLED:
            raise InvalidSkillTransition("DISABLED is terminal")
        return self._replace_state(current, SkillState.DISABLED)

    def resolve_active(self, skill_id: str, version: str) -> SkillRegistration:
        current = self.get(skill_id, version)
        if current.state is not SkillState.ACTIVE:
            raise SkillNotFound(f"active skill not found: {skill_id}@{version}")
        return current

    def _replace_state(
        self,
        current: SkillRegistration,
        state: SkillState,
    ) -> SkillRegistration:
        updated = replace(current, state=state)
        self._skills[(current.skill_id, current.version)] = updated
        return updated
