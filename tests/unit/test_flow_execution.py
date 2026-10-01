import unittest

from agente_seshix.application.flow_execution import (
    FlowExecutionEnvelope,
    FlowRun,
    FlowRunState,
    FlowStepState,
    InvalidFlowTransition,
)
from agente_seshix.application.skill_registry import SkillRegistration, SkillState
from agente_seshix.application.task_context_resolver import TaskContextPackage
from agente_seshix.domain.authority import AuthorityDecision, AuthorityOutcome
from agente_seshix.domain.task_context import Task


def make_run() -> FlowRun:
    task = Task("TASK-1", "CONTEXT_BUILD", "Build company context")
    package = TaskContextPackage(task=task, sections=())
    return FlowRun(run_id="RUN-1", task=task, context_package=package)


def make_active_skill() -> SkillRegistration:
    return SkillRegistration(
        skill_id="SKILL_01",
        version="0.1",
        domain="process.context",
        supported_task_types=("CONTEXT_BUILD",),
        compatibility=("foundation>=0.1",),
        state=SkillState.ACTIVE,
    )


def make_authority(outcome: AuthorityOutcome = AuthorityOutcome.ALLOW) -> AuthorityDecision:
    return AuthorityDecision(
        decision_id="AUTH-1",
        actor_id="AGENT",
        action="execute_skill",
        outcome=outcome,
        policy_version="0.1",
        reason="test decision",
    )


class FlowExecutionEnvelopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.envelope = FlowExecutionEnvelope()

    def test_happy_path_is_ordered_and_traceable(self) -> None:
        run = self.envelope.start(make_run())
        run = self.envelope.begin_step(run, "STEP-1", "resolve skill")
        run = self.envelope.select_skill(run, make_active_skill())
        run = self.envelope.record_authority(run, make_authority())
        run = self.envelope.pass_step(run, result={"resolved": True})
        run = self.envelope.begin_step(run, "STEP-2", "execute skill")
        run = self.envelope.pass_step(run, result={"output": "context"})
        run = self.envelope.complete(run, result={"status": "done"})

        self.assertEqual(run.state, FlowRunState.PASSED)
        self.assertEqual(tuple(step.step_id for step in run.steps), ("STEP-1", "STEP-2"))
        self.assertEqual(run.steps[0].selected_skill_id, "SKILL_01")
        self.assertEqual(run.steps[0].authority_decision.outcome, AuthorityOutcome.ALLOW)
        self.assertEqual(run.result, {"status": "done"})

    def test_run_must_start_from_ready(self) -> None:
        run = self.envelope.start(make_run())
        with self.assertRaises(InvalidFlowTransition):
            self.envelope.start(run)

    def test_next_step_requires_previous_step_passed(self) -> None:
        run = self.envelope.start(make_run())
        run = self.envelope.begin_step(run, "STEP-1", "first")
        with self.assertRaises(InvalidFlowTransition):
            self.envelope.begin_step(run, "STEP-2", "second")

    def test_duplicate_step_id_is_rejected(self) -> None:
        run = self.envelope.start(make_run())
        run = self.envelope.begin_step(run, "STEP-1", "first")
        run = self.envelope.pass_step(run)
        with self.assertRaises(InvalidFlowTransition):
            self.envelope.begin_step(run, "STEP-1", "again")

    def test_waiting_hitl_stops_run_and_is_explicitly_resumable(self) -> None:
        run = self.envelope.start(make_run())
        run = self.envelope.begin_step(run, "STEP-1", "authority")
        run = self.envelope.record_authority(run, make_authority(AuthorityOutcome.REQUIRES_HITL))
        run = self.envelope.wait_for_hitl(run, "human approval required")
        self.assertEqual(run.state, FlowRunState.WAITING_HITL)
        self.assertEqual(run.steps[-1].state, FlowStepState.WAITING_HITL)
        with self.assertRaises(InvalidFlowTransition):
            self.envelope.pass_step(run)

        run = self.envelope.resume_after_hitl(run)
        self.assertEqual(run.state, FlowRunState.RUNNING)
        self.assertEqual(run.steps[-1].state, FlowStepState.RUNNING)
        run = self.envelope.pass_step(run)
        run = self.envelope.complete(run)
        self.assertEqual(run.state, FlowRunState.PASSED)

    def test_block_is_terminal(self) -> None:
        run = self.envelope.start(make_run())
        run = self.envelope.begin_step(run, "STEP-1", "validate context")
        run = self.envelope.block(run, "required context missing")
        self.assertEqual(run.state, FlowRunState.BLOCKED)
        self.assertEqual(run.steps[-1].state, FlowStepState.BLOCKED)
        with self.assertRaises(InvalidFlowTransition):
            self.envelope.begin_step(run, "STEP-2", "should not run")

    def test_fail_is_terminal(self) -> None:
        run = self.envelope.start(make_run())
        run = self.envelope.begin_step(run, "STEP-1", "execute")
        run = self.envelope.fail(run, "unexpected execution error")
        self.assertEqual(run.state, FlowRunState.FAILED)
        self.assertEqual(run.steps[-1].state, FlowStepState.FAILED)
        with self.assertRaises(InvalidFlowTransition):
            self.envelope.complete(run)

    def test_complete_requires_passed_step(self) -> None:
        run = self.envelope.start(make_run())
        run = self.envelope.begin_step(run, "STEP-1", "execute")
        with self.assertRaises(InvalidFlowTransition):
            self.envelope.complete(run)

    def test_context_package_must_match_task(self) -> None:
        task = Task("TASK-1", "TYPE", "one")
        other = Task("TASK-2", "TYPE", "two")
        with self.assertRaises(ValueError):
            FlowRun(
                run_id="RUN-1",
                task=task,
                context_package=TaskContextPackage(task=other, sections=()),
            )


if __name__ == "__main__":
    unittest.main()
