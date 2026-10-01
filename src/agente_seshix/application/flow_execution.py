from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any

from agente_seshix.application.skill_registry import SkillRegistration
from agente_seshix.application.task_context_resolver import TaskContextPackage
from agente_seshix.domain.authority import AuthorityDecision
from agente_seshix.domain.task_context import Task


class FlowRunState(str, Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING_HITL = "WAITING_HITL"
    PASSED = "PASSED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class FlowStepState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING_HITL = "WAITING_HITL"
    PASSED = "PASSED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class InvalidFlowTransition(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FlowStep:
    step_id: str
    name: str
    state: FlowStepState = FlowStepState.PENDING
    selected_skill_id: str | None = None
    selected_skill_version: str | None = None
    authority_decision: AuthorityDecision | None = None
    result: Any = None
    stop_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.step_id.strip():
            raise ValueError("step_id must not be empty")
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if (self.selected_skill_id is None) != (self.selected_skill_version is None):
            raise ValueError("selected skill id/version must be provided together")
        if self.selected_skill_id is not None and not self.selected_skill_id.strip():
            raise ValueError("selected_skill_id must not be empty when provided")
        if self.selected_skill_version is not None and not self.selected_skill_version.strip():
            raise ValueError("selected_skill_version must not be empty when provided")
        if self.stop_reason is not None and not self.stop_reason.strip():
            raise ValueError("stop_reason must not be empty when provided")


@dataclass(frozen=True, slots=True)
class FlowRun:
    run_id: str
    task: Task
    context_package: TaskContextPackage
    state: FlowRunState = FlowRunState.READY
    steps: tuple[FlowStep, ...] = ()
    result: Any = None
    stop_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.run_id.strip():
            raise ValueError("run_id must not be empty")
        if self.context_package.task.task_id != self.task.task_id:
            raise ValueError("context package task must match run task")
        if self.stop_reason is not None and not self.stop_reason.strip():
            raise ValueError("stop_reason must not be empty when provided")


class FlowExecutionEnvelope:
    _TERMINAL_RUN_STATES = {
        FlowRunState.PASSED,
        FlowRunState.BLOCKED,
        FlowRunState.FAILED,
    }

    def start(self, run: FlowRun) -> FlowRun:
        if run.state is not FlowRunState.READY:
            raise InvalidFlowTransition(f"cannot start run from {run.state.value}")
        return replace(run, state=FlowRunState.RUNNING)

    def begin_step(self, run: FlowRun, step_id: str, name: str) -> FlowRun:
        self._require_running(run)
        if any(step.step_id == step_id for step in run.steps):
            raise InvalidFlowTransition(f"duplicate step_id: {step_id}")
        if run.steps and run.steps[-1].state not in {FlowStepState.PASSED}:
            raise InvalidFlowTransition("previous step must pass before starting next step")
        step = FlowStep(step_id=step_id, name=name, state=FlowStepState.RUNNING)
        return replace(run, steps=run.steps + (step,))

    def select_skill(self, run: FlowRun, skill: SkillRegistration) -> FlowRun:
        index, step = self._current_running_step(run)
        updated = replace(
            step,
            selected_skill_id=skill.skill_id,
            selected_skill_version=skill.version,
        )
        return self._replace_step(run, index, updated)

    def record_authority(self, run: FlowRun, decision: AuthorityDecision) -> FlowRun:
        index, step = self._current_running_step(run)
        updated = replace(step, authority_decision=decision)
        return self._replace_step(run, index, updated)

    def pass_step(self, run: FlowRun, result: Any = None) -> FlowRun:
        index, step = self._current_running_step(run)
        updated = replace(step, state=FlowStepState.PASSED, result=result)
        return self._replace_step(run, index, updated)

    def wait_for_hitl(self, run: FlowRun, reason: str) -> FlowRun:
        index, step = self._current_running_step(run)
        if not reason.strip():
            raise ValueError("reason must not be empty")
        updated = replace(
            step,
            state=FlowStepState.WAITING_HITL,
            stop_reason=reason,
        )
        run = self._replace_step(run, index, updated)
        return replace(run, state=FlowRunState.WAITING_HITL, stop_reason=reason)

    def resume_after_hitl(self, run: FlowRun) -> FlowRun:
        if run.state is not FlowRunState.WAITING_HITL:
            raise InvalidFlowTransition("run is not waiting for HITL")
        if not run.steps or run.steps[-1].state is not FlowStepState.WAITING_HITL:
            raise InvalidFlowTransition("current step is not waiting for HITL")
        step = replace(
            run.steps[-1],
            state=FlowStepState.RUNNING,
            stop_reason=None,
        )
        return replace(
            self._replace_step(run, len(run.steps) - 1, step),
            state=FlowRunState.RUNNING,
            stop_reason=None,
        )

    def block(self, run: FlowRun, reason: str) -> FlowRun:
        return self._stop_terminal(run, FlowRunState.BLOCKED, FlowStepState.BLOCKED, reason)

    def fail(self, run: FlowRun, reason: str) -> FlowRun:
        return self._stop_terminal(run, FlowRunState.FAILED, FlowStepState.FAILED, reason)

    def complete(self, run: FlowRun, result: Any = None) -> FlowRun:
        self._require_running(run)
        if not run.steps:
            raise InvalidFlowTransition("run cannot complete without steps")
        if run.steps[-1].state is not FlowStepState.PASSED:
            raise InvalidFlowTransition("last step must pass before run completion")
        return replace(run, state=FlowRunState.PASSED, result=result)

    def _stop_terminal(
        self,
        run: FlowRun,
        run_state: FlowRunState,
        step_state: FlowStepState,
        reason: str,
    ) -> FlowRun:
        self._require_running(run)
        if not reason.strip():
            raise ValueError("reason must not be empty")
        if not run.steps or run.steps[-1].state is not FlowStepState.RUNNING:
            raise InvalidFlowTransition("no running step to stop")
        step = replace(run.steps[-1], state=step_state, stop_reason=reason)
        run = self._replace_step(run, len(run.steps) - 1, step)
        return replace(run, state=run_state, stop_reason=reason)

    def _require_running(self, run: FlowRun) -> None:
        if run.state in self._TERMINAL_RUN_STATES:
            raise InvalidFlowTransition(f"run is terminal: {run.state.value}")
        if run.state is not FlowRunState.RUNNING:
            raise InvalidFlowTransition(f"run must be RUNNING, got {run.state.value}")

    def _current_running_step(self, run: FlowRun) -> tuple[int, FlowStep]:
        self._require_running(run)
        if not run.steps or run.steps[-1].state is not FlowStepState.RUNNING:
            raise InvalidFlowTransition("no running step")
        return len(run.steps) - 1, run.steps[-1]

    def _replace_step(self, run: FlowRun, index: int, step: FlowStep) -> FlowRun:
        steps = list(run.steps)
        steps[index] = step
        return replace(run, steps=tuple(steps))
