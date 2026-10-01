import unittest

from agente_seshix.application.authority_policy import (
    AuthorityEvaluationContext,
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.evidence_intake import (
    EvidenceIntakeCommand,
    EvidenceIntakeUseCase,
)
from agente_seshix.application.flow_execution import FlowExecutionEnvelope, FlowRunState
from agente_seshix.application.skill_01_context import (
    Skill01ContextCommand,
    Skill01ContextRuntime,
    Skill01ContextStatus,
)
from agente_seshix.application.skill_01_node import Skill01NodeCommand, Skill01NodeRuntime
from agente_seshix.application.skill_registry import (
    SkillRegistration,
    SkillRegistry,
)
from agente_seshix.application.task_context_resolver import TaskContextResolver
from agente_seshix.domain.context_evidence import EvidenceClassification
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import ContextSection, Task, TaskContextRequirements


class EvidenceRepo:
    def __init__(self) -> None:
        self.items: dict[str, Evidence] = {}

    def save(self, evidence: Evidence) -> None:
        self.items[evidence.evidence_id] = evidence

    def get(self, evidence_id: str) -> Evidence | None:
        return self.items.get(evidence_id)
class ContextRepo:
    def __init__(self) -> None:
        self.items: dict[str, PrimaryContextVersion] = {
            "PCV-0": PrimaryContextVersion("PCV-0", ())
        }

    def save(self, version: PrimaryContextVersion) -> None:
        self.items[version.version_id] = version

    def get(self, version_id: str) -> PrimaryContextVersion | None:
        return self.items.get(version_id)


def build_node(*, active: bool = True):
    evidence_repo = EvidenceRepo()
    context_repo = ContextRepo()
    registry = SkillRegistry()
    registry.register(
        SkillRegistration(
            skill_id="SKILL_01",
            version="0.1",
            domain="process.context",
            supported_task_types=("CONTEXT_BUILD", "CONTEXT_UPDATE"),
            compatibility=("foundation>=0.1",),
        )
    )
    if active:
        registry.start_testing("SKILL_01", "0.1")
        registry.activate("SKILL_01", "0.1", validation_passed=True)

    node = Skill01NodeRuntime(
        context_resolver=TaskContextResolver(),
        skill_registry=registry,
        authority_evaluator=AuthorityPolicyEvaluator(),
        evidence_intake=EvidenceIntakeUseCase(evidence_repo),
        skill_runtime=Skill01ContextRuntime(context_repo, evidence_repo),
        flow=FlowExecutionEnvelope(),
    )
    return node, evidence_repo, context_repo
class Skill01NodeStressTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Task("TASK-1", "CONTEXT_BUILD", "Build company context")
        self.requirements = TaskContextRequirements(task_id="TASK-1", required_sections=())

    def policy(self, expression: str = "ALLOW") -> AuthorityPolicy:
        return AuthorityPolicy(
            version="0.1",
            actors=("AGENT",),
            actions={"execute_skill": expression},
        )

    def fact(self, evidence_id: str, new_version: str = "PCV-1") -> Skill01ContextCommand:
        return Skill01ContextCommand(
            base_version_id="PCV-0",
            new_version_id=new_version,
            record_id=f"CTX-{new_version}",
            key="company.employees",
            classification=EvidenceClassification.FATTO,
            context_value_version="1",
            evidence_id=evidence_id,
        )

    def command(
        self,
        *,
        run_id: str,
        skill_command: Skill01ContextCommand,
        expression: str = "ALLOW",
        intake: EvidenceIntakeCommand | None = None,
        requirements: TaskContextRequirements | None = None,
        available_context=None,
    ) -> Skill01NodeCommand:
        return Skill01NodeCommand(
            run_id=run_id,
            task=self.task,
            context_requirements=requirements or self.requirements,
            available_context=available_context or {},
            skill_version="0.1",
            actor_id="AGENT",
            authority_action="execute_skill",
            authority_policy=self.policy(expression),
            skill_command=skill_command,
            evidence_intake=intake,
        )
    def intake(self, evidence_id: str, employees: int = 6) -> EvidenceIntakeCommand:
        return EvidenceIntakeCommand(
            evidence_id=evidence_id,
            source_ref=f"source://{evidence_id}",
            claim=f"Company has {employees} employees",
            evidence={"employees": employees},
            version="1",
        )

    def test_authority_resume_requires_explicit_human_approval(self) -> None:
        node, evidence_repo, context_repo = build_node()
        waiting = node.execute(
            self.command(
                run_id="RUN-HITL-STRICT",
                expression="REQUIRES_HITL",
                intake=self.intake("EV-HITL"),
                skill_command=self.fact("EV-HITL"),
            )
        )
        self.assertEqual(waiting.run.state, FlowRunState.WAITING_HITL)

        with self.assertRaises(ValueError):
            node.resume(waiting)

        self.assertIsNone(evidence_repo.get("EV-HITL"))
        self.assertIsNone(context_repo.get("PCV-1"))

    def test_inactive_skill_is_traceably_blocked(self) -> None:
        node, evidence_repo, context_repo = build_node(active=False)
        result = node.execute(
            self.command(
                run_id="RUN-INACTIVE",
                intake=self.intake("EV-INACTIVE"),
                skill_command=self.fact("EV-INACTIVE"),
            )
        )
        self.assertEqual(result.run.state, FlowRunState.BLOCKED)
        self.assertIn("active skill", result.run.stop_reason.lower())
        self.assertIsNone(evidence_repo.get("EV-INACTIVE"))
        self.assertIsNone(context_repo.get("PCV-1"))
    def test_missing_evidence_is_traceably_blocked(self) -> None:
        node, _, context_repo = build_node()
        result = node.execute(
            self.command(
                run_id="RUN-MISSING-EVIDENCE",
                skill_command=self.fact("EV-MISSING"),
            )
        )
        self.assertEqual(result.run.state, FlowRunState.BLOCKED)
        self.assertIn("evidence", result.run.stop_reason.lower())
        self.assertIsNone(context_repo.get("PCV-1"))

    def test_duplicate_evidence_does_not_overwrite_and_is_traceably_blocked(self) -> None:
        node, evidence_repo, context_repo = build_node()
        first = node.execute(
            self.command(
                run_id="RUN-FIRST",
                intake=self.intake("EV-DUP", employees=6),
                skill_command=self.fact("EV-DUP", "PCV-1"),
            )
        )
        self.assertEqual(first.run.state, FlowRunState.PASSED)

        duplicate = node.execute(
            self.command(
                run_id="RUN-DUPLICATE",
                intake=self.intake("EV-DUP", employees=99),
                skill_command=Skill01ContextCommand(
                    base_version_id="PCV-1",
                    new_version_id="PCV-2",
                    record_id="CTX-PCV-2",
                    key="company.employees",
                    classification=EvidenceClassification.FATTO,
                    context_value_version="2",
                    evidence_id="EV-DUP",
                ),
            )
        )
        self.assertEqual(duplicate.run.state, FlowRunState.BLOCKED)
        self.assertEqual(evidence_repo.get("EV-DUP").evidence, {"employees": 6})
        self.assertIsNone(context_repo.get("PCV-2"))
    def test_optional_unknown_completes_without_context_mutation(self) -> None:
        node, _, context_repo = build_node()
        before = dict(context_repo.items)
        result = node.execute(
            self.command(
                run_id="RUN-OPTIONAL-UNKNOWN",
                skill_command=Skill01ContextCommand(
                    base_version_id="PCV-0",
                    new_version_id="PCV-NO-WRITE",
                    record_id="CTX-UNKNOWN",
                    key="company.optional",
                    classification=EvidenceClassification.UNKNOWN,
                    context_value_version="1",
                    required=False,
                ),
            )
        )
        self.assertEqual(result.run.state, FlowRunState.PASSED)
        self.assertEqual(result.skill_result.status, Skill01ContextStatus.UNKNOWN)
        self.assertEqual(context_repo.items, before)

    def test_hypothesis_is_preserved_as_hypothesis(self) -> None:
        node, _, _ = build_node()
        result = node.execute(
            self.command(
                run_id="RUN-HYP",
                intake=self.intake("EV-HYP"),
                skill_command=Skill01ContextCommand(
                    base_version_id="PCV-0",
                    new_version_id="PCV-HYP",
                    record_id="CTX-HYP",
                    key="company.staffing_hypothesis",
                    classification=EvidenceClassification.IPOTESI,
                    context_value_version="1",
                    evidence_id="EV-HYP",
                    proposed_value="Hiring may be required",
                ),
            )
        )
        record = result.context_version.records[0]
        self.assertEqual(record.value.classification, EvidenceClassification.IPOTESI)
        self.assertEqual(record.value.value, "Hiring may be required")
    def test_repeated_fresh_runs_are_deterministic(self) -> None:
        snapshots = []
        for suffix in ("A", "B", "C"):
            node, _, _ = build_node()
            result = node.execute(
                self.command(
                    run_id=f"RUN-{suffix}",
                    intake=self.intake(f"EV-{suffix}"),
                    skill_command=self.fact(f"EV-{suffix}"),
                )
            )
            snapshots.append(
                (
                    result.run.state,
                    tuple(step.step_id for step in result.run.steps),
                    result.context_version.records[0].value.value,
                    result.context_version.previous_version_id,
                )
            )
        self.assertEqual(snapshots[0], snapshots[1])
        self.assertEqual(snapshots[1], snapshots[2])

    def test_repeated_versioned_updates_preserve_history(self) -> None:
        node, _, context_repo = build_node()
        first = node.execute(
            self.command(
                run_id="RUN-V1",
                intake=self.intake("EV-V1", 6),
                skill_command=self.fact("EV-V1", "PCV-1"),
            )
        )
        second = node.execute(
            self.command(
                run_id="RUN-V2",
                intake=self.intake("EV-V2", 8),
                skill_command=Skill01ContextCommand(
                    base_version_id="PCV-1",
                    new_version_id="PCV-2",
                    record_id="CTX-V2",
                    key="company.employees",
                    classification=EvidenceClassification.FATTO,
                    context_value_version="2",
                    evidence_id="EV-V2",
                ),
            )
        )
        self.assertEqual(first.context_version.records[0].value.value, {"employees": 6})
        self.assertEqual(second.context_version.records[0].value.value, {"employees": 8})
        self.assertEqual(context_repo.get("PCV-1").records[0].value.value, {"employees": 6})
        self.assertEqual(second.context_version.previous_version_id, "PCV-1")
    def test_context_hitl_can_repeat_until_valid_input_arrives(self) -> None:
        node, _, context_repo = build_node()
        unknown = Skill01ContextCommand(
            base_version_id="PCV-0",
            new_version_id="PCV-HITL",
            record_id="CTX-REV",
            key="company.revenue",
            classification=EvidenceClassification.UNKNOWN,
            context_value_version="1",
            required=True,
        )
        waiting = node.execute(
            self.command(run_id="RUN-CONTEXT-REPEAT", skill_command=unknown)
        )
        self.assertEqual(waiting.run.state, FlowRunState.WAITING_HITL)

        waiting_again = node.resume(waiting, skill_command=unknown)
        self.assertEqual(waiting_again.run.state, FlowRunState.WAITING_HITL)
        self.assertIsNone(context_repo.get("PCV-HITL"))

        completed = node.resume(
            waiting_again,
            evidence_intake=self.intake("EV-REV", 100000),
            skill_command=Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-HITL",
                record_id="CTX-REV",
                key="company.revenue",
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id="EV-REV",
            ),
        )
        self.assertEqual(completed.run.state, FlowRunState.PASSED)
        self.assertEqual(completed.context_version.records[0].value.value, {"employees": 100000})

    def test_unsupported_fact_value_is_rejected_before_any_run(self) -> None:
        with self.assertRaises(ValueError):
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-BAD",
                record_id="CTX-BAD",
                key="company.employees",
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id="EV-X",
                proposed_value=999,
            )
    def test_missing_required_task_context_is_traceably_blocked_without_mutation(self) -> None:
        node, evidence_repo, context_repo = build_node()
        requirements = TaskContextRequirements(
            task_id="TASK-1",
            required_sections=(ContextSection.POLICY,),
        )
        before_context = dict(context_repo.items)
        before_evidence = dict(evidence_repo.items)

        result = node.execute(
            self.command(
                run_id="RUN-MISSING-CONTEXT",
                requirements=requirements,
                available_context={},
                intake=self.intake("EV-NOT-USED"),
                skill_command=self.fact("EV-NOT-USED"),
            )
        )

        self.assertEqual(result.run.state, FlowRunState.BLOCKED)
        self.assertEqual(result.run.steps[-1].step_id, "CONTEXT")
        self.assertIn("missing required context", result.run.stop_reason.lower())
        self.assertEqual(context_repo.items, before_context)
        self.assertEqual(evidence_repo.items, before_evidence)


if __name__ == "__main__":
    unittest.main()
