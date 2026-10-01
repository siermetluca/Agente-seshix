from __future__ import annotations

import os

from agente_seshix.application.authority_policy import (
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.evidence_intake import EvidenceIntakeUseCase
from agente_seshix.application.flow_execution import FlowExecutionEnvelope
from agente_seshix.application.semantic_model import StructuredSemanticService
from agente_seshix.application.skill_01_context import Skill01ContextRuntime
from agente_seshix.application.skill_01_node import Skill01NodeRuntime
from agente_seshix.application.skill_01_semantic_intake import (
    Skill01SemanticIntakeService,
)
from agente_seshix.application.skill_registry import SkillRegistration, SkillRegistry
from agente_seshix.application.task_context_resolver import TaskContextResolver
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import Task, TaskContextRequirements
from agente_seshix.infrastructure.ollama_semantic_model import (
    OllamaSemanticModel,
    OllamaSemanticModelError,
)


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
def build_service():
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

    model_name = os.environ.get(
        "AGENTE_SESHIX_SEMANTIC_MODEL",
        "qwen2.5:3b",
    )
    semantic = StructuredSemanticService(
        OllamaSemanticModel(model=model_name)
    )
    service = Skill01SemanticIntakeService(semantic, node)
    return service, evidence_repo, context_repo, model_name


def show_preview(preview) -> None:
    print("\n=== INTERPRETAZIONE PROPOSTA ===")
    if not preview.accepted_candidates:
        print("Nessun dato aziendale concreto estratto.")
    for index, candidate in enumerate(preview.accepted_candidates, start=1):
        print(f"{index:02d}. {candidate.key}")
        print(f"    classificazione : {candidate.classification.value}")
        print(f"    valore          : {candidate.value!r}")
        print(f"    claim           : {candidate.claim}")
    if preview.clarification_questions:
        print("\nCHIARIMENTI RICHIESTI:")
        for question in preview.clarification_questions:
            print(f"- {question}")
    print("=== FINE PREVIEW ===\n")
def show_commit(result, context_repo) -> None:
    print("\n=== COMMIT SKILL_01 ===")
    for node_result in result.node_results:
        print(
            f"{node_result.run.run_id}: "
            f"state={node_result.run.state.value} "
            f"context_version="
            f"{node_result.context_version.version_id if node_result.context_version else '-'}"
        )
    print("\nPRIMARY_CONTEXT VERSIONI:")
    for version_id, version in context_repo.items.items():
        print(f"\n{version_id}  previous={version.previous_version_id}")
        for record in version.records:
            print(
                f"  {record.key} = {record.value.value!r} "
                f"[{record.value.classification.value}]"
            )
            for provenance in record.value.provenance:
                print(
                    "    provenance: "
                    f"{provenance.source_ref} / {provenance.evidence_id}"
                )
    print("=== FINE COMMIT ===\n")


def main() -> None:
    service, evidence_repo, context_repo, model_name = build_service()
    print("==============================================")
    print(" SKILL_01 HUMAN ACCEPTANCE TEST v2")
    print("==============================================")
    print(f"Semantic model locale: {model_name}")
    print()
    print("Descrivi la tua azienda in linguaggio naturale.")
    print("Non usare key, claim o classificazioni interne.")
    print("Esempio:")
    print(
        "  Siermet SRLS installa impianti elettrici e tecnologici. "
        "Ha 6 dipendenti, 1 titolare e 1 amministrativa. Opera in Italia."
    )
    print()
    source_text = input("Descrizione azienda: ").strip()
    if not source_text:
        raise SystemExit("Descrizione vuota: test annullato.")

    print("\nAnalisi semantica locale in corso...")
    try:
        preview = service.analyze(
            request_id="HUMAN-V2",
            source_text=source_text,
            source_ref="human://owner",
        )
    except (ValueError, OllamaSemanticModelError) as error:
        print(f"ANALISI BLOCCATA: {error}")
        raise SystemExit(2)

    show_preview(preview)
    if preview.clarification_questions:
        print(
            "Il sistema ha individuato informazioni mancanti. "
            "Puoi rispondere ora oppure lasciare vuoto."
        )
        additions = []
        for question in preview.clarification_questions:
            answer = input(f"{question} ").strip()
            if answer:
                additions.append(f"{question} Risposta: {answer}")
        if additions:
            enriched_text = source_text + "\n" + "\n".join(additions)
            print("\nRianalisi con i chiarimenti...")
            preview = service.analyze(
                request_id="HUMAN-V2-CLARIFIED",
                source_text=enriched_text,
                source_ref="human://owner",
            )
            show_preview(preview)

    if not preview.accepted_candidates:
        print("Nessun candidato scrivibile. Nessuna mutazione eseguita.")
        return

    decision = input(
        "Confermi che questa interpretazione rispecchia ciò che hai scritto? [s/N]: "
    ).strip().lower()
    if decision not in {"s", "si", "sì", "y", "yes"}:
        print("NON CONFERMATO: nessuna Evidence e nessun PRIMARY_CONTEXT scritto.")
        print(f"Evidence count: {len(evidence_repo.items)}")
        print(f"Context versions: {tuple(context_repo.items)}")
        return

    task = Task(
        "HUMAN-V2-TASK",
        "CONTEXT_BUILD",
        "Build company context from human natural-language input",
    )
    requirements = TaskContextRequirements(task.task_id, ())
    result = service.commit(
        preview,
        task=task,
        context_requirements=requirements,
        available_context={},
        skill_version="0.1",
        actor_id="HUMAN_TEST_AGENT",
        authority_action="execute_skill",
        authority_policy=AuthorityPolicy(
            version="human-v2",
            actors=("HUMAN_TEST_AGENT",),
            actions={"execute_skill": "ALLOW"},
        ),
    )
    show_commit(result, context_repo)
    print(
        "Il test tecnico è terminato. "
        "SKILL_01_HUMAN_ACCEPTANCE resta PENDING finché non la approvi "
        "esplicitamente nella conversazione."
    )


if __name__ == "__main__":
    main()
