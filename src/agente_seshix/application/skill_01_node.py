from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from agente_seshix.application.authority_policy import (
    AuthorityEvaluationContext,
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.evidence_intake import (
    EvidenceAlreadyExists,
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
    Skill01ContextResult,
    Skill01ContextRuntime,
    Skill01ContextStatus,
)
from agente_seshix.application.update_primary_context import EvidenceNotFound
from agente_seshix.application.skill_registry import SkillNotFound, SkillRegistry
from agente_seshix.application.task_context_resolver import (
    TaskContextPackage,
    TaskContextResolver,
)
from agente_seshix.domain.authority import AuthorityOutcome
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import ContextSection, Task, TaskContextRequirements


@dataclass(frozen=True, slots=True)
class Skill01NodeCommand:
    run_id: str
    task: Task
    context_requirements: TaskContextRequirements
    available_context: Mapping[ContextSection, Any]
    skill_version: str
    actor_id: str
    authority_action: str
    authority_policy: AuthorityPolicy
    skill_command: Skill01ContextCommand
    authority_context: AuthorityEvaluationContext = AuthorityEvaluationContext()
    evidence_intake: EvidenceIntakeCommand | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("run_id", self.run_id),
            ("skill_version", self.skill_version),
            ("actor_id", self.actor_id),
            ("authority_action", self.authority_action),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
@dataclass(frozen=True, slots=True)
class Skill01NodeResult:
    run: FlowRun
    command: Skill01NodeCommand
    context_package: TaskContextPackage
    ingested_evidence: Evidence | None = None
    skill_result: Skill01ContextResult | None = None

    @property
    def context_version(self) -> PrimaryContextVersion | None:
        if self.skill_result is None:
            return None
        return self.skill_result.context_version


class Skill01NodeRuntime:
    SKILL_ID = "SKILL_01"

    def __init__(
        self,
        *,
        context_resolver: TaskContextResolver,
        skill_registry: SkillRegistry,
        authority_evaluator: AuthorityPolicyEvaluator,
        evidence_intake: EvidenceIntakeUseCase,
        skill_runtime: Skill01ContextRuntime,
        flow: FlowExecutionEnvelope,
    ) -> None:
        self._context_resolver = context_resolver
        self._skill_registry = skill_registry
        self._authority_evaluator = authority_evaluator
        self._evidence_intake = evidence_intake
        self._skill_runtime = skill_runtime
        self._flow = flow
    def execute(self, command: Skill01NodeCommand) -> Skill01NodeResult:
        package = self._context_resolver.resolve(
            command.task,
            command.context_requirements,
            command.available_context,
        )
        run = self._flow.start(
            FlowRun(
                run_id=command.run_id,
                task=command.task,
                context_package=package,
            )
        )

        run = self._flow.begin_step(run, "CONTEXT", "resolve task context")
        run = self._flow.pass_step(run, result=package)

        run = self._flow.begin_step(run, "SKILL_RESOLUTION", "resolve active SKILL_01")
        try:
            skill = self._skill_registry.resolve_active(
                self.SKILL_ID,
                command.skill_version,
            )
        except SkillNotFound as error:
            run = self._flow.block(run, str(error))
            return Skill01NodeResult(
                run=run,
                command=command,
                context_package=package,
            )
        run = self._flow.select_skill(run, skill)
        run = self._flow.pass_step(run, result=skill)

        run = self._flow.begin_step(run, "AUTHORITY", "evaluate execution authority")
        decision = self._authority_evaluator.evaluate(
            decision_id=f"{command.run_id}:AUTH",
            actor_id=command.actor_id,
            action=command.authority_action,
            policy=command.authority_policy,
            context=command.authority_context,
        )
        run = self._flow.record_authority(run, decision)
        if decision.outcome is AuthorityOutcome.DENY:
            run = self._flow.block(run, decision.reason or "authority denied")
            return Skill01NodeResult(
                run=run,
                command=command,
                context_package=package,
            )

        if decision.outcome is AuthorityOutcome.REQUIRES_HITL:
            run = self._flow.wait_for_hitl(
                run,
                decision.reason or "authority requires HITL",
            )
            return Skill01NodeResult(
                run=run,
                command=command,
                context_package=package,
            )

        run = self._flow.pass_step(run, result=decision)
        return self._continue_after_authority(
            run=run,
            command=command,
            package=package,
        )
    def resume(
        self,
        previous: Skill01NodeResult,
        *,
        authority_context: AuthorityEvaluationContext | None = None,
        skill_command: Skill01ContextCommand | None = None,
        evidence_intake: EvidenceIntakeCommand | None = None,
    ) -> Skill01NodeResult:
        run = previous.run
        if run.state is not FlowRunState.WAITING_HITL:
            raise ValueError("SKILL_01 node run is not waiting for HITL")

        waiting_step = run.steps[-1].step_id
        run = self._flow.resume_after_hitl(run)

        if waiting_step == "AUTHORITY":
            if authority_context is None:
                raise ValueError(
                    "authority_context with explicit HITL approval is required"
                )
            context = authority_context
            command = Skill01NodeCommand(
                run_id=previous.command.run_id,
                task=previous.command.task,
                context_requirements=previous.command.context_requirements,
                available_context=previous.command.available_context,
                skill_version=previous.command.skill_version,
                actor_id=previous.command.actor_id,
                authority_action=previous.command.authority_action,
                authority_policy=previous.command.authority_policy,
                skill_command=skill_command or previous.command.skill_command,
                authority_context=context,
                evidence_intake=evidence_intake or previous.command.evidence_intake,
            )
            decision = self._authority_evaluator.evaluate(
                decision_id=f"{command.run_id}:AUTH:RESUME",
                actor_id=command.actor_id,
                action=command.authority_action,
                policy=command.authority_policy,
                context=command.authority_context,
            )
            run = self._flow.record_authority(run, decision)
            if decision.outcome is AuthorityOutcome.DENY:
                run = self._flow.block(run, decision.reason or "authority denied")
                return Skill01NodeResult(run, command, previous.context_package)
            if decision.outcome is AuthorityOutcome.REQUIRES_HITL:
                run = self._flow.wait_for_hitl(
                    run,
                    decision.reason or "authority requires HITL",
                )
                return Skill01NodeResult(run, command, previous.context_package)

            run = self._flow.pass_step(run, result=decision)
            return self._continue_after_authority(
                run=run,
                command=command,
                package=previous.context_package,
            )

        if waiting_step == "SKILL_EXECUTION":
            if skill_command is None:
                raise ValueError("skill_command is required to resume context HITL")
            command = Skill01NodeCommand(
                run_id=previous.command.run_id,
                task=previous.command.task,
                context_requirements=previous.command.context_requirements,
                available_context=previous.command.available_context,
                skill_version=previous.command.skill_version,
                actor_id=previous.command.actor_id,
                authority_action=previous.command.authority_action,
                authority_policy=previous.command.authority_policy,
                skill_command=skill_command,
                authority_context=previous.command.authority_context,
                evidence_intake=evidence_intake,
            )
            return self._execute_skill_step(
                run=run,
                command=command,
                package=previous.context_package,
                evidence_intake=evidence_intake,
            )

        raise ValueError(f"unsupported HITL resume step: {waiting_step}")
    def _continue_after_authority(
        self,
        *,
        run: FlowRun,
        command: Skill01NodeCommand,
        package: TaskContextPackage,
    ) -> Skill01NodeResult:
        ingested = None
        if command.evidence_intake is not None:
            run = self._flow.begin_step(
                run,
                "EVIDENCE_INTAKE",
                "ingest explicit source evidence",
            )
            try:
                ingested = self._evidence_intake.execute(command.evidence_intake)
            except EvidenceAlreadyExists as error:
                run = self._flow.block(
                    run,
                    f"evidence already exists: {error}",
                )
                return Skill01NodeResult(
                    run=run,
                    command=command,
                    context_package=package,
                )
            run = self._flow.pass_step(run, result=ingested)

        return self._execute_skill_step(
            run=run,
            command=command,
            package=package,
            evidence_intake=None,
            ingested_evidence=ingested,
        )

    def _execute_skill_step(
        self,
        *,
        run: FlowRun,
        command: Skill01NodeCommand,
        package: TaskContextPackage,
        evidence_intake: EvidenceIntakeCommand | None,
        ingested_evidence: Evidence | None = None,
    ) -> Skill01NodeResult:
        if evidence_intake is not None:
            if run.steps and run.steps[-1].step_id == "SKILL_EXECUTION":
                try:
                    ingested_evidence = self._evidence_intake.execute(evidence_intake)
                except EvidenceAlreadyExists as error:
                    run = self._flow.block(
                        run,
                        f"evidence already exists: {error}",
                    )
                    return Skill01NodeResult(
                        run=run,
                        command=command,
                        context_package=package,
                    )
            else:
                run = self._flow.begin_step(
                    run,
                    "EVIDENCE_INTAKE_RESUME",
                    "ingest HITL evidence",
                )
                try:
                    ingested_evidence = self._evidence_intake.execute(evidence_intake)
                except EvidenceAlreadyExists as error:
                    run = self._flow.block(
                        run,
                        f"evidence already exists: {error}",
                    )
                    return Skill01NodeResult(
                        run=run,
                        command=command,
                        context_package=package,
                    )
                run = self._flow.pass_step(run, result=ingested_evidence)

        if not run.steps or run.steps[-1].step_id != "SKILL_EXECUTION":
            run = self._flow.begin_step(run, "SKILL_EXECUTION", "execute SKILL_01")
        try:
            skill_result = self._skill_runtime.execute(command.skill_command)
        except EvidenceNotFound as error:
            run = self._flow.block(
                run,
                f"evidence not found: {error}",
            )
            return Skill01NodeResult(
                run=run,
                command=command,
                context_package=package,
                ingested_evidence=ingested_evidence,
            )

        if skill_result.status is Skill01ContextStatus.WAITING_HITL:
            run = self._flow.wait_for_hitl(
                run,
                skill_result.stop_reason or "SKILL_01 requires HITL",
            )
            return Skill01NodeResult(
                run=run,
                command=command,
                context_package=package,
                ingested_evidence=ingested_evidence,
                skill_result=skill_result,
            )

        run = self._flow.pass_step(run, result=skill_result)
        run = self._flow.complete(run, result=skill_result)
        return Skill01NodeResult(
            run=run,
            command=command,
            context_package=package,
            ingested_evidence=ingested_evidence,
            skill_result=skill_result,
        )
