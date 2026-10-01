import unittest

from agente_seshix.application.authority_policy import (
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.evidence_intake import EvidenceIntakeUseCase
from agente_seshix.application.flow_execution import FlowExecutionEnvelope
from agente_seshix.application.semantic_model import (
    RawSemanticCandidate,
    RawSemanticOutput,
    StructuredSemanticService,
)
from agente_seshix.application.skill_01_context import Skill01ContextRuntime
from agente_seshix.application.skill_01_node import Skill01NodeRuntime
from agente_seshix.application.skill_01_semantic_intake import (
    Skill01SemanticIntakeError,
    Skill01SemanticIntakeService,
)
from agente_seshix.application.skill_registry import SkillRegistration, SkillRegistry
from agente_seshix.application.task_context_resolver import TaskContextResolver
from agente_seshix.domain.evidence import Evidence
from agente_seshix.domain.primary_context import PrimaryContextVersion
from agente_seshix.domain.task_context import Task, TaskContextRequirements


class FakeModel:
    def __init__(self, output):
        self.output = output
    def generate(self, request):
        return self.output


class EvidenceRepo:
    def __init__(self):
        self.items = {}
    def save(self, evidence: Evidence):
        self.items[evidence.evidence_id] = evidence
    def get(self, evidence_id: str):
        return self.items.get(evidence_id)


class ContextRepo:
    def __init__(self):
        self.items = {"PCV-0": PrimaryContextVersion("PCV-0", ())}
    def save(self, version):
        self.items[version.version_id] = version
    def get(self, version_id):
        return self.items.get(version_id)


def build_service(output):
    ev = EvidenceRepo()
    ctx = ContextRepo()
    registry = SkillRegistry()
    registry.register(SkillRegistration(
        skill_id="SKILL_01",
        version="0.1",
        domain="process.context",
        supported_task_types=("CONTEXT_BUILD",),
        compatibility=("foundation>=0.1",),
    ))
    registry.start_testing("SKILL_01", "0.1")
    registry.activate("SKILL_01", "0.1", validation_passed=True)
    node = Skill01NodeRuntime(
        context_resolver=TaskContextResolver(),
        skill_registry=registry,
        authority_evaluator=AuthorityPolicyEvaluator(),
        evidence_intake=EvidenceIntakeUseCase(ev),
        skill_runtime=Skill01ContextRuntime(ctx, ev),
        flow=FlowExecutionEnvelope(),
    )
    service = Skill01SemanticIntakeService(
        StructuredSemanticService(FakeModel(output)),
        node,
    )
    return service, ev, ctx


class Skill01SemanticIntakeTests(unittest.TestCase):
    def test_preview_has_zero_mutations(self):
        service, ev, ctx = build_service(RawSemanticOutput(candidates=(
            RawSemanticCandidate("company.name", "The company is Siermet SRLS.", "FATTO", "Siermet SRLS"),
            RawSemanticCandidate("company.employees", "The company has six employees.", "FATTO", 6),
        )))
        before_ev = dict(ev.items)
        before_ctx = dict(ctx.items)
        preview = service.analyze(
            request_id="SEM-A",
            source_text="Siermet SRLS ha 6 dipendenti.",
            source_ref="human://owner",
        )
        self.assertEqual(len(preview.accepted_candidates), 2)
        self.assertEqual(ev.items, before_ev)
        self.assertEqual(ctx.items, before_ctx)

    def test_unknown_becomes_clarification_and_is_not_accepted(self):
        service, _, _ = build_service(RawSemanticOutput(candidates=(
            RawSemanticCandidate("company.revenue", "Revenue is unavailable.", "UNKNOWN", None),
        )))
        preview = service.analyze(
            request_id="SEM-U",
            source_text="Non conosco il fatturato.",
            source_ref="human://owner",
        )
        self.assertEqual(preview.accepted_candidates, ())
        self.assertEqual(len(preview.clarification_questions), 1)
        self.assertIn("fatturato", preview.clarification_questions[0].lower())

    def test_empty_candidate_set_requests_clarification(self):
        service, ev, ctx = build_service(RawSemanticOutput(candidates=()))
        before_ev = dict(ev.items)
        before_ctx = dict(ctx.items)
        preview = service.analyze(
            request_id="SEM-EMPTY",
            source_text="impianti elettrici",
            source_ref="human://owner",
        )
        self.assertEqual(preview.accepted_candidates, ())
        self.assertEqual(len(preview.clarification_questions), 1)
        self.assertIn("impianti elettrici", preview.clarification_questions[0])
        self.assertEqual(ev.items, before_ev)
        self.assertEqual(ctx.items, before_ctx)

    def test_generic_company_name_is_not_accepted_as_fact(self):
        service, _, _ = build_service(RawSemanticOutput(candidates=(
            RawSemanticCandidate(
                "company.name",
                "La mia azienda",
                "FATTO",
                "La mia azienda",
            ),
            RawSemanticCandidate(
                "company.activities",
                "Installa impianti elettrici",
                "FATTO",
                ["installa impianti elettrici"],
            ),
        )))
        preview = service.analyze(
            request_id="SEM-GENERIC-NAME",
            source_text="La mia azienda installa impianti elettrici.",
            source_ref="human://owner",
        )
        self.assertEqual(
            tuple(c.key for c in preview.accepted_candidates),
            ("company.activities",),
        )
        self.assertTrue(
            any("nome" in q.lower() for q in preview.clarification_questions)
        )

    def test_model_generated_unknown_is_ignored_without_explicit_unknown_source(self):
        service, _, _ = build_service(RawSemanticOutput(candidates=(
            RawSemanticCandidate(
                "company.activities",
                "Installa impianti elettrici",
                "FATTO",
                ["installa impianti elettrici"],
            ),
            RawSemanticCandidate(
                "company.country",
                "Country is unavailable.",
                "UNKNOWN",
                None,
            ),
        )))
        preview = service.analyze(
            request_id="SEM-SPURIOUS-UNKNOWN",
            source_text="La mia azienda installa impianti elettrici.",
            source_ref="human://owner",
        )
        self.assertEqual(
            tuple(c.key for c in preview.accepted_candidates),
            ("company.activities",),
        )
        self.assertEqual(preview.clarification_questions, ())

    def test_out_of_catalog_key_is_rejected(self):
        service, _, _ = build_service(RawSemanticOutput(candidates=(
            RawSemanticCandidate("company.secret_magic", "Magic.", "FATTO", "x"),
        )))
        with self.assertRaises(Skill01SemanticIntakeError):
            service.analyze(
                request_id="SEM-X",
                source_text="Magic",
                source_ref="human://owner",
            )

    def test_commit_chains_versions_and_provenance(self):
        service, ev, ctx = build_service(RawSemanticOutput(candidates=(
            RawSemanticCandidate("company.name", "The company is Siermet SRLS.", "FATTO", "Siermet SRLS"),
            RawSemanticCandidate("company.employees", "The company has six employees.", "FATTO", 6),
        )))
        preview = service.analyze(
            request_id="SEM-C",
            source_text="Siermet SRLS ha 6 dipendenti.",
            source_ref="human://owner",
        )
        result = service.commit(
            preview,
            task=Task("T1", "CONTEXT_BUILD", "Build context"),
            context_requirements=TaskContextRequirements("T1", ()),
            available_context={},
            skill_version="0.1",
            actor_id="AGENT",
            authority_action="execute_skill",
            authority_policy=AuthorityPolicy(
                version="1",
                actors=("AGENT",),
                actions={"execute_skill": "ALLOW"},
            ),
        )
        self.assertEqual(result.final_context_version_id, "SEM-C:PCV:2")
        self.assertEqual(ctx.get("SEM-C:PCV:1").previous_version_id, "PCV-0")
        self.assertEqual(ctx.get("SEM-C:PCV:2").previous_version_id, "SEM-C:PCV:1")
        self.assertEqual(ev.get("SEM-C:EV:1").source.source_ref, "human://owner")
        self.assertEqual(ev.get("SEM-C:EV:2").evidence, 6)


if __name__ == "__main__":
    unittest.main()
