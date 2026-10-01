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
    SkillState,
)
from agente_seshix.application.task_context_resolver import TaskContextResolver
from agente_seshix.domain.authority import AuthorityOutcome
from agente_seshix.domain.context_evidence import EvidenceClassification
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import Task, TaskContextRequirements


class InMemoryEvidenceRepository:
    def __init__(self) -> None:
        self._items: dict[str, Evidence] = {}

    def save(self, evidence: Evidence) -> None:
        self._items[evidence.evidence_id] = evidence

    def get(self, evidence_id: str) -> Evidence | None:
        return self._items.get(evidence_id)
class InMemoryPrimaryContextRepository:
    def __init__(self) -> None:
        self._items: dict[str, PrimaryContextVersion] = {}

    def save(self, version: PrimaryContextVersion) -> None:
        self._items[version.version_id] = version

    def get(self, version_id: str) -> PrimaryContextVersion | None:
        return self._items.get(version_id)


class Skill01NodeRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evidence_repository = InMemoryEvidenceRepository()
        self.context_repository = InMemoryPrimaryContextRepository()
        self.context_repository.save(PrimaryContextVersion("PCV-0", ()))

        self.registry = SkillRegistry()
        self.registry.register(
            SkillRegistration(
                skill_id="SKILL_01",
                version="0.1",
                domain="process.context",
                supported_task_types=("CONTEXT_BUILD", "CONTEXT_UPDATE"),
                compatibility=("foundation>=0.1",),
            )
        )
        self.registry.start_testing("SKILL_01", "0.1")
        self.registry.activate("SKILL_01", "0.1", validation_passed=True)

        self.node = Skill01NodeRuntime(
            context_resolver=TaskContextResolver(),
            skill_registry=self.registry,
            authority_evaluator=AuthorityPolicyEvaluator(),
            evidence_intake=EvidenceIntakeUseCase(self.evidence_repository),
            skill_runtime=Skill01ContextRuntime(
                self.context_repository,
                self.evidence_repository,
            ),
            flow=FlowExecutionEnvelope(),
        )
        self.task = Task(
            task_id="TASK-CTX",
            task_type="CONTEXT_BUILD",
            objective="Build company context",
        )
        self.requirements = TaskContextRequirements(
            task_id="TASK-CTX",
            required_sections=(),
        )

    def policy(self, expression: str) -> AuthorityPolicy:
        return AuthorityPolicy(
            version="0.1",
            actors=("AGENT",),
            actions={"execute_skill": expression},
        )

    def command(
        self,
        *,
        run_id: str,
        expression: str = "ALLOW",
        skill_command: Skill01ContextCommand,
        intake: EvidenceIntakeCommand | None = None,
        authority_context: AuthorityEvaluationContext = AuthorityEvaluationContext(),
    ) -> Skill01NodeCommand:
        return Skill01NodeCommand(
            run_id=run_id,
            task=self.task,
            context_requirements=self.requirements,
            available_context={},
            skill_version="0.1",
            actor_id="AGENT",
            authority_action="execute_skill",
            authority_policy=self.policy(expression),
            authority_context=authority_context,
            evidence_intake=intake,
            skill_command=skill_command,
        )
    def fact_command(
        self,
        *,
        new_version_id: str,
        evidence_id: str,
        key: str = "company.employees",
    ) -> Skill01ContextCommand:
        return Skill01ContextCommand(
            base_version_id="PCV-0",
            new_version_id=new_version_id,
            record_id=f"CTX-{new_version_id}",
            key=key,
            classification=EvidenceClassification.FATTO,
            context_value_version="1",
            evidence_id=evidence_id,
        )

    def test_happy_path_runs_complete_node(self) -> None:
        result = self.node.execute(
            self.command(
                run_id="RUN-HAPPY",
                intake=EvidenceIntakeCommand(
                    evidence_id="EV-1",
                    source_ref="source://user/company",
                    claim="Company has six employees",
                    evidence={"employees": 6},
                    version="1",
                ),
                skill_command=self.fact_command(
                    new_version_id="PCV-1",
                    evidence_id="EV-1",
                ),
            )
        )

        self.assertEqual(result.run.state, FlowRunState.PASSED)
        self.assertEqual(result.skill_result.status, Skill01ContextStatus.WRITTEN)
        self.assertEqual(result.context_version.version_id, "PCV-1")
        self.assertEqual(
            tuple(step.step_id for step in result.run.steps),
            (
                "CONTEXT",
                "SKILL_RESOLUTION",
                "AUTHORITY",
                "EVIDENCE_INTAKE",
                "SKILL_EXECUTION",
            ),
        )
    def test_authority_deny_blocks_before_evidence_and_context_write(self) -> None:
        result = self.node.execute(
            self.command(
                run_id="RUN-DENY",
                expression="DENY",
                intake=EvidenceIntakeCommand(
                    evidence_id="EV-DENY",
                    source_ref="source://user/company",
                    claim="Company has six employees",
                    evidence={"employees": 6},
                    version="1",
                ),
                skill_command=self.fact_command(
                    new_version_id="PCV-DENY",
                    evidence_id="EV-DENY",
                ),
            )
        )

        self.assertEqual(result.run.state, FlowRunState.BLOCKED)
        self.assertEqual(
            result.run.steps[-1].authority_decision.outcome,
            AuthorityOutcome.DENY,
        )
        self.assertIsNone(self.evidence_repository.get("EV-DENY"))
        self.assertIsNone(self.context_repository.get("PCV-DENY"))

    def test_authority_hitl_resumes_and_completes(self) -> None:
        waiting = self.node.execute(
            self.command(
                run_id="RUN-AUTH-HITL",
                expression="REQUIRES_HITL",
                intake=EvidenceIntakeCommand(
                    evidence_id="EV-HITL",
                    source_ref="source://user/company",
                    claim="Company has six employees",
                    evidence={"employees": 6},
                    version="1",
                ),
                skill_command=self.fact_command(
                    new_version_id="PCV-HITL",
                    evidence_id="EV-HITL",
                ),
            )
        )

        self.assertEqual(waiting.run.state, FlowRunState.WAITING_HITL)
        self.assertIsNone(self.evidence_repository.get("EV-HITL"))
        resumed = self.node.resume(
            waiting,
            authority_context=AuthorityEvaluationContext(hitl_approved=True),
        )

        self.assertEqual(resumed.run.state, FlowRunState.PASSED)
        self.assertEqual(
            resumed.run.steps[2].authority_decision.outcome,
            AuthorityOutcome.ALLOW,
        )
        self.assertIsNotNone(self.evidence_repository.get("EV-HITL"))
        self.assertEqual(resumed.context_version.version_id, "PCV-HITL")

    def test_context_hitl_resumes_with_new_evidence_and_command(self) -> None:
        waiting = self.node.execute(
            self.command(
                run_id="RUN-CONTEXT-HITL",
                skill_command=Skill01ContextCommand(
                    base_version_id="PCV-0",
                    new_version_id="PCV-CONTEXT",
                    record_id="CTX-REVENUE",
                    key="company.revenue",
                    classification=EvidenceClassification.UNKNOWN,
                    context_value_version="1",
                    required=True,
                ),
            )
        )

        self.assertEqual(waiting.run.state, FlowRunState.WAITING_HITL)
        self.assertEqual(waiting.run.steps[-1].step_id, "SKILL_EXECUTION")

        resumed = self.node.resume(
            waiting,
            evidence_intake=EvidenceIntakeCommand(
                evidence_id="EV-REVENUE",
                source_ref="source://user/revenue",
                claim="Revenue supplied by owner",
                evidence={"revenue": 100000},
                version="1",
            ),
            skill_command=Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-CONTEXT",
                record_id="CTX-REVENUE",
                key="company.revenue",
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id="EV-REVENUE",
            ),
        )
        self.assertEqual(resumed.run.state, FlowRunState.PASSED)
        self.assertEqual(resumed.context_version.version_id, "PCV-CONTEXT")
        self.assertEqual(
            resumed.context_version.records[0].value.provenance[0].evidence_id,
            "EV-REVENUE",
        )
        self.assertEqual(resumed.ingested_evidence.evidence_id, "EV-REVENUE")

    def test_traceability_binds_skill_authority_evidence_and_context(self) -> None:
        result = self.node.execute(
            self.command(
                run_id="RUN-TRACE",
                intake=EvidenceIntakeCommand(
                    evidence_id="EV-TRACE",
                    source_ref="source://trace",
                    claim="Traceable company fact",
                    evidence={"employees": 7},
                    version="3",
                ),
                skill_command=self.fact_command(
                    new_version_id="PCV-TRACE",
                    evidence_id="EV-TRACE",
                ),
            )
        )

        skill_step = result.run.steps[1]
        authority_step = result.run.steps[2]
        self.assertEqual(skill_step.selected_skill_id, "SKILL_01")
        self.assertEqual(skill_step.selected_skill_version, "0.1")
        self.assertEqual(authority_step.authority_decision.policy_version, "0.1")
        self.assertEqual(result.ingested_evidence.evidence_id, "EV-TRACE")
        self.assertEqual(result.context_version.version_id, "PCV-TRACE")
        self.assertEqual(
            result.context_version.records[0].value.provenance[0].source_ref,
            "source://trace",
        )


if __name__ == "__main__":
    unittest.main()
