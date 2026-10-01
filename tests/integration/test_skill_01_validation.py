import unittest

from agente_seshix.application.authority_policy import (
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.evidence_intake import (
    EvidenceIntakeCommand,
    EvidenceIntakeUseCase,
)
from agente_seshix.application.flow_execution import (
    FlowExecutionEnvelope,
    FlowRun,
    FlowRunState,
)
from agente_seshix.application.skill_01_context import (
    Skill01ContextCommand,
    Skill01ContextRuntime,
    Skill01ContextStatus,
)
from agente_seshix.application.skill_registry import (
    InvalidSkillTransition,
    SkillRegistration,
    SkillRegistry,
    SkillState,
    SkillValidationRequired,
)
from agente_seshix.application.task_context_resolver import TaskContextPackage
from agente_seshix.application.update_primary_context import EvidenceNotFound
from agente_seshix.domain.authority import AuthorityOutcome
from agente_seshix.domain.context_evidence import EvidenceClassification
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import Task


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
class Skill01ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evidence_repository = InMemoryEvidenceRepository()
        self.context_repository = InMemoryPrimaryContextRepository()
        self.context_repository.save(PrimaryContextVersion("PCV-0", ()))
        self.intake = EvidenceIntakeUseCase(self.evidence_repository)
        self.skill = Skill01ContextRuntime(
            self.context_repository,
            self.evidence_repository,
        )
        self.envelope = FlowExecutionEnvelope()
        self.authority = AuthorityPolicyEvaluator()
        self.task = Task(
            "TASK-CONTEXT",
            "CONTEXT_BUILD",
            "Build company context from verified evidence",
        )
        self.package = TaskContextPackage(task=self.task, sections=())

    def make_run(self, run_id: str) -> FlowRun:
        return FlowRun(
            run_id=run_id,
            task=self.task,
            context_package=self.package,
        )

    def active_skill(self) -> SkillRegistration:
        return SkillRegistration(
            skill_id="SKILL_01",
            version="0.1",
            domain="process.context",
            supported_task_types=("CONTEXT_BUILD", "CONTEXT_UPDATE"),
            compatibility=("foundation>=0.1",),
            state=SkillState.ACTIVE,
        )
    def policy(self, expression: str) -> AuthorityPolicy:
        return AuthorityPolicy(
            version="0.1",
            actors=("AGENT",),
            actions={"execute_skill": expression},
        )

    def intake_employee_evidence(
        self,
        *,
        evidence_id: str,
        employees: int,
        source_ref: str,
    ) -> Evidence:
        return self.intake.execute(
            EvidenceIntakeCommand(
                evidence_id=evidence_id,
                source_ref=source_ref,
                claim=f"The company has {employees} employees.",
                evidence={"employees": employees},
                version="1",
            )
        )

    def begin_authorized_step(
        self,
        *,
        run_id: str,
        expression: str,
    ):
        run = self.envelope.start(self.make_run(run_id))
        run = self.envelope.begin_step(run, "STEP-SKILL01", "execute SKILL_01")
        run = self.envelope.select_skill(run, self.active_skill())
        decision = self.authority.evaluate(
            decision_id=f"AUTH-{run_id}",
            actor_id="AGENT",
            action="execute_skill",
            policy=self.policy(expression),
        )
        run = self.envelope.record_authority(run, decision)
        return run, decision
    def test_happy_path_source_to_active_skill_to_primary_context(self) -> None:
        self.intake_employee_evidence(
            evidence_id="EV-1",
            employees=6,
            source_ref="source://user/company-profile",
        )
        run, decision = self.begin_authorized_step(
            run_id="RUN-HAPPY",
            expression="ALLOW",
        )
        self.assertEqual(decision.outcome, AuthorityOutcome.ALLOW)

        result = self.skill.execute(
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-EMPLOYEES",
                key="company.employees",
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id="EV-1",
            )
        )
        run = self.envelope.pass_step(run, result=result)
        run = self.envelope.complete(run, result=result.context_version)

        self.assertEqual(run.state, FlowRunState.PASSED)
        self.assertEqual(result.status, Skill01ContextStatus.WRITTEN)
        record = result.context_version.records[0]
        self.assertEqual(record.value.value, {"employees": 6})
        self.assertEqual(record.value.provenance[0].evidence_id, "EV-1")
    def test_authority_deny_prevents_skill_execution_and_write(self) -> None:
        self.intake_employee_evidence(
            evidence_id="EV-DENY",
            employees=6,
            source_ref="source://user/company-profile",
        )
        run, decision = self.begin_authorized_step(
            run_id="RUN-DENY",
            expression="DENY",
        )
        self.assertEqual(decision.outcome, AuthorityOutcome.DENY)
        run = self.envelope.block(run, "authority denied skill execution")

        self.assertEqual(run.state, FlowRunState.BLOCKED)
        self.assertIsNone(self.context_repository.get("PCV-DENY"))

    def test_authority_hitl_waits_and_does_not_write(self) -> None:
        self.intake_employee_evidence(
            evidence_id="EV-HITL",
            employees=6,
            source_ref="source://user/company-profile",
        )
        run, decision = self.begin_authorized_step(
            run_id="RUN-HITL",
            expression="REQUIRES_HITL",
        )
        self.assertEqual(decision.outcome, AuthorityOutcome.REQUIRES_HITL)
        run = self.envelope.wait_for_hitl(run, "human approval required")

        self.assertEqual(run.state, FlowRunState.WAITING_HITL)
        self.assertIsNone(self.context_repository.get("PCV-HITL"))
    def test_required_unknown_waits_for_hitl_without_write(self) -> None:
        result = self.skill.execute(
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-UNKNOWN",
                record_id="CTX-REVENUE",
                key="company.revenue",
                classification=EvidenceClassification.UNKNOWN,
                context_value_version="1",
                required=True,
            )
        )
        self.assertEqual(result.status, Skill01ContextStatus.WAITING_HITL)
        self.assertIsNone(self.context_repository.get("PCV-UNKNOWN"))

    def test_missing_evidence_blocks_context_write(self) -> None:
        with self.assertRaises(EvidenceNotFound):
            self.skill.execute(
                Skill01ContextCommand(
                    base_version_id="PCV-0",
                    new_version_id="PCV-MISSING",
                    record_id="CTX-EMPLOYEES",
                    key="company.employees",
                    classification=EvidenceClassification.FATTO,
                    context_value_version="1",
                    evidence_id="EV-MISSING",
                )
            )
        self.assertIsNone(self.context_repository.get("PCV-MISSING"))
    def test_conflicting_update_creates_new_version_without_silent_overwrite(self) -> None:
        self.intake_employee_evidence(
            evidence_id="EV-OLD",
            employees=6,
            source_ref="source://old/company-profile",
        )
        first = self.skill.execute(
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-EMPLOYEES-1",
                key="company.employees",
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id="EV-OLD",
            )
        )
        self.intake_employee_evidence(
            evidence_id="EV-NEW",
            employees=8,
            source_ref="source://new/company-profile",
        )
        second = self.skill.execute(
            Skill01ContextCommand(
                base_version_id="PCV-1",
                new_version_id="PCV-2",
                record_id="CTX-EMPLOYEES-2",
                key="company.employees",
                classification=EvidenceClassification.FATTO,
                context_value_version="2",
                evidence_id="EV-NEW",
            )
        )
        old_record = self.context_repository.get("PCV-1").records[0]
        new_record = self.context_repository.get("PCV-2").records[0]

        self.assertEqual(old_record.value.value, {"employees": 6})
        self.assertEqual(old_record.value.provenance[0].evidence_id, "EV-OLD")
        self.assertEqual(new_record.value.value, {"employees": 8})
        self.assertEqual(new_record.value.provenance[0].evidence_id, "EV-NEW")
        self.assertEqual(second.context_version.previous_version_id, "PCV-1")
        self.assertEqual(first.context_version.version_id, "PCV-1")

    def test_registry_activation_is_validation_gated(self) -> None:
        registry = SkillRegistry()
        draft = SkillRegistration(
            skill_id="SKILL_01",
            version="0.1",
            domain="process.context",
            supported_task_types=("CONTEXT_BUILD", "CONTEXT_UPDATE"),
            compatibility=("foundation>=0.1",),
        )
        registry.register(draft)

        with self.assertRaises(InvalidSkillTransition):
            registry.activate("SKILL_01", "0.1", validation_passed=True)

        testing = registry.start_testing("SKILL_01", "0.1")
        self.assertEqual(testing.state, SkillState.TESTING)
        with self.assertRaises(SkillValidationRequired):
            registry.activate("SKILL_01", "0.1", validation_passed=False)

        active = registry.activate(
            "SKILL_01",
            "0.1",
            validation_passed=True,
        )
        self.assertEqual(active.state, SkillState.ACTIVE)
        self.assertEqual(
            registry.resolve_active("SKILL_01", "0.1").state,
            SkillState.ACTIVE,
        )


if __name__ == "__main__":
    unittest.main()
