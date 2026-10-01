from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agente_seshix.application.authority_policy import (
    AuthorityEvaluationContext,
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.evidence_intake import (
    EvidenceIntakeCommand,
    EvidenceIntakeUseCase,
)
from agente_seshix.application.flow_execution import FlowExecutionEnvelope
from agente_seshix.application.skill_01_context import (
    Skill01ContextCommand,
    Skill01ContextRuntime,
)
from agente_seshix.application.skill_01_node import (
    Skill01NodeCommand,
    Skill01NodeResult,
    Skill01NodeRuntime,
)
from agente_seshix.application.skill_registry import (
    SkillRegistration,
    SkillRegistry,
)
from agente_seshix.application.task_context_resolver import TaskContextResolver
from agente_seshix.domain.context_evidence import EvidenceClassification
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import Task, TaskContextRequirements


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
@dataclass
class Harness:
    node: Skill01NodeRuntime
    evidence_repo: EvidenceRepo
    context_repo: ContextRepo
    task: Task
    requirements: TaskContextRequirements


def build_harness() -> Harness:
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

    task = Task(
        task_id="HUMAN-TEST-TASK",
        task_type="CONTEXT_BUILD",
        objective="Human acceptance test of SKILL_01",
    )
    requirements = TaskContextRequirements(
        task_id=task.task_id,
        required_sections=(),
    )
    return Harness(node, evidence_repo, context_repo, task, requirements)


def policy(expression: str) -> AuthorityPolicy:
    return AuthorityPolicy(
        version="human-test-0.1",
        actors=("HUMAN_TEST_AGENT",),
        actions={"execute_skill": expression},
    )
def show_run(result: Skill01NodeResult) -> None:
    print("\n=== FLOW RUN ===")
    print(f"run_id       : {result.run.run_id}")
    print(f"run_state    : {result.run.state.value}")
    print(f"stop_reason  : {result.run.stop_reason or '-'}")
    print("\nSTEPS:")
    for index, step in enumerate(result.run.steps, start=1):
        skill = (
            f"{step.selected_skill_id}@{step.selected_skill_version}"
            if step.selected_skill_id
            else "-"
        )
        authority = (
            step.authority_decision.outcome.value
            if step.authority_decision
            else "-"
        )
        print(
            f"{index:02d}. {step.step_id:<18} "
            f"state={step.state.value:<12} "
            f"skill={skill:<16} authority={authority}"
        )

    if result.ingested_evidence is not None:
        ev = result.ingested_evidence
        print("\nEVIDENCE:")
        print(f"  evidence_id : {ev.evidence_id}")
        print(f"  source_ref  : {ev.source.source_ref}")
        print(f"  claim       : {ev.claim}")
        print(f"  payload     : {ev.evidence!r}")

    if result.context_version is not None:
        ctx = result.context_version
        print("\nPRIMARY_CONTEXT:")
        print(f"  version_id          : {ctx.version_id}")
        print(f"  previous_version_id : {ctx.previous_version_id}")
        for record in ctx.records:
            print(f"  key                 : {record.key}")
            print(f"  classification      : {record.value.classification.value}")
            print(f"  value               : {record.value.value!r}")
            for prov in record.value.provenance:
                print(
                    "  provenance          : "
                    f"source={prov.source_ref} evidence_id={prov.evidence_id}"
                )
    print("=== END RUN ===\n")


def ask(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{label}{suffix}: ").strip()
    if value:
        return value
    if default is not None:
        return default
    raise ValueError(f"{label} non può essere vuoto")
def make_node_command(
    h: Harness,
    *,
    run_id: str,
    expression: str,
    skill_command: Skill01ContextCommand,
    intake: EvidenceIntakeCommand | None = None,
) -> Skill01NodeCommand:
    return Skill01NodeCommand(
        run_id=run_id,
        task=h.task,
        context_requirements=h.requirements,
        available_context={},
        skill_version="0.1",
        actor_id="HUMAN_TEST_AGENT",
        authority_action="execute_skill",
        authority_policy=policy(expression),
        skill_command=skill_command,
        evidence_intake=intake,
    )


def scenario_fact() -> None:
    print("\n--- SCENARIO 1: FACT NORMALE ---")
    h = build_harness()
    key = ask("Context key", "company.name")
    value = ask("Valore reale da registrare", "Siermet SRLS")
    claim = ask("Claim", f"{key} = {value}")
    source = ask("Source ref", "human://owner")
    evidence_id = "HAT-EV-FACT"

    result = h.node.execute(
        make_node_command(
            h,
            run_id="HAT-RUN-FACT",
            expression="ALLOW",
            intake=EvidenceIntakeCommand(
                evidence_id=evidence_id,
                source_ref=source,
                claim=claim,
                evidence=value,
                version="1",
            ),
            skill_command=Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="HAT-CTX-FACT",
                key=key,
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id=evidence_id,
            ),
        )
    )
    show_run(result)
def scenario_context_hitl() -> None:
    print("\n--- SCENARIO 2: UNKNOWN → HITL → RESUME ---")
    h = build_harness()
    key = ask("Dato richiesto ma inizialmente UNKNOWN", "company.revenue")

    waiting = h.node.execute(
        make_node_command(
            h,
            run_id="HAT-RUN-CONTEXT-HITL",
            expression="ALLOW",
            skill_command=Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="HAT-CTX-HITL",
                key=key,
                classification=EvidenceClassification.UNKNOWN,
                context_value_version="1",
                required=True,
            ),
        )
    )
    show_run(waiting)

    if waiting.run.state.value != "WAITING_HITL":
        print("ERRORE: il nodo non è entrato in WAITING_HITL.")
        return

    print("Ora sei tu a fornire il dato mancante.")
    value = ask("Valore fornito dall'HITL", "100000")
    claim = ask("Claim", f"{key} = {value}")
    source = ask("Source ref", "human://owner")
    evidence_id = "HAT-EV-HITL"

    resumed = h.node.resume(
        waiting,
        evidence_intake=EvidenceIntakeCommand(
            evidence_id=evidence_id,
            source_ref=source,
            claim=claim,
            evidence=value,
            version="1",
        ),
        skill_command=Skill01ContextCommand(
            base_version_id="PCV-0",
            new_version_id="PCV-1",
            record_id="HAT-CTX-HITL",
            key=key,
            classification=EvidenceClassification.FATTO,
            context_value_version="1",
            evidence_id=evidence_id,
        ),
    )
    show_run(resumed)
def scenario_authority_hitl() -> None:
    print("\n--- SCENARIO 3: AUTHORITY HITL ---")
    h = build_harness()
    key = ask("Context key", "company.country")
    value = ask("Valore", "IT")
    claim = ask("Claim", f"{key} = {value}")
    source = ask("Source ref", "human://owner")
    evidence_id = "HAT-EV-AUTH"

    waiting = h.node.execute(
        make_node_command(
            h,
            run_id="HAT-RUN-AUTH-HITL",
            expression="REQUIRES_HITL",
            intake=EvidenceIntakeCommand(
                evidence_id=evidence_id,
                source_ref=source,
                claim=claim,
                evidence=value,
                version="1",
            ),
            skill_command=Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="HAT-CTX-AUTH",
                key=key,
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id=evidence_id,
            ),
        )
    )
    show_run(waiting)

    approved = input("Approvi esplicitamente l'esecuzione? [s/N]: ").strip().lower()
    if approved not in {"s", "si", "sì", "y", "yes"}:
        print("\nNON APPROVATO: nessun resume, nessuna Evidence/context write.")
        print(f"Evidence presente? {h.evidence_repo.get(evidence_id) is not None}")
        print(f"PCV-1 presente?   {h.context_repo.get('PCV-1') is not None}")
        return

    resumed = h.node.resume(
        waiting,
        authority_context=AuthorityEvaluationContext(hitl_approved=True),
    )
    show_run(resumed)
def main() -> None:
    print("==============================================")
    print(" SKILL_01 HUMAN ACCEPTANCE TEST")
    print("==============================================")
    print("1 - FACT normale")
    print("2 - UNKNOWN -> HITL -> resume")
    print("3 - Authority HITL")
    print("4 - Esegui tutti e tre")
    choice = input("Scelta [4]: ").strip() or "4"

    actions = {
        "1": [scenario_fact],
        "2": [scenario_context_hitl],
        "3": [scenario_authority_hitl],
        "4": [scenario_fact, scenario_context_hitl, scenario_authority_hitl],
    }
    if choice not in actions:
        raise SystemExit("Scelta non valida")

    for action in actions[choice]:
        action()

    print("Test locale terminato.")
    print("L'esito HUMAN_ACCEPTANCE resta PENDING finché non lo approvi esplicitamente.")


if __name__ == "__main__":
    main()
