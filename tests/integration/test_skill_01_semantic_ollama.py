import os
import unittest

from agente_seshix.application.semantic_model import StructuredSemanticService
from agente_seshix.application.skill_01_semantic_intake import Skill01SemanticIntakeService
from agente_seshix.infrastructure.ollama_semantic_model import OllamaSemanticModel


@unittest.skipUnless(
    os.environ.get("AGENTE_SESHIX_RUN_OLLAMA_TESTS") == "1",
    "real Ollama integration is opt-in",
)
class Skill01SemanticOllamaTests(unittest.TestCase):
    def test_real_local_model_extracts_expected_company_facts(self):
        class NoopNode:
            pass

        service = Skill01SemanticIntakeService(
            StructuredSemanticService(
                OllamaSemanticModel(
                    model=os.environ.get(
                        "AGENTE_SESHIX_SEMANTIC_MODEL",
                        "qwen2.5:3b",
                    )
                )
            ),
            NoopNode(),
        )
        preview = service.analyze(
            request_id="OLLAMA-SMOKE",
            source_text=(
                "Siermet SRLS installa impianti elettrici e tecnologici. "
                "Ha 6 dipendenti, 1 titolare e 1 persona amministrativa. "
                "Opera in Italia."
            ),
            source_ref="human://owner",
        )
        by_key = {candidate.key: candidate for candidate in preview.accepted_candidates}
        self.assertEqual(by_key["company.name"].value, "Siermet SRLS")
        self.assertEqual(by_key["company.employees"].value, 6)
        self.assertEqual(by_key["company.owner_count"].value, 1)
        self.assertEqual(by_key["company.admin_staff"].value, 1)
        self.assertIn("company.activities", by_key)
        self.assertIn("company.country", by_key)

    def test_real_local_model_preserves_typo_verbatim_for_grounded_fact(self):
        class NoopNode:
            pass

        source_text = (
            "azienda di installazione di impianti tecnologici e elttrici, "
            "con integrazione di sviluppo software settoriali"
        )
        service = Skill01SemanticIntakeService(
            StructuredSemanticService(
                OllamaSemanticModel(
                    model=os.environ.get(
                        "AGENTE_SESHIX_SEMANTIC_MODEL",
                        "qwen2.5:3b",
                    )
                )
            ),
            NoopNode(),
        )
        preview = service.analyze(
            request_id="OLLAMA-TYPO-GROUNDING",
            source_text=source_text,
            source_ref="human://owner",
        )
        by_key = {candidate.key: candidate for candidate in preview.accepted_candidates}
        self.assertIn("company.activities", by_key)
        activities = by_key["company.activities"].value
        self.assertTrue(activities)
        for activity in activities:
            self.assertIn(activity, source_text)
        self.assertTrue(any("elttrici" in activity for activity in activities))
        self.assertFalse(any("elettrici" in activity for activity in activities))


if __name__ == "__main__":
    unittest.main()
