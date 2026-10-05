import os
import unittest

from agente_seshix.application.skill_02_company_analysis import (
    AnalysisCategory,
    Skill02CompanyAnalysisRuntime,
)
from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)
from agente_seshix.domain.primary_context import (
    PrimaryContextRecord,
    PrimaryContextVersion,
)
from agente_seshix.infrastructure.ollama_company_analysis import OllamaCompanyAnalysis


def fact(value, evidence_id):
    return ContextValue(
        value=value,
        classification=EvidenceClassification.FATTO,
        provenance=(Provenance("human://owner", evidence_id),),
        version="1",
    )


@unittest.skipUnless(
    os.environ.get("AGENTE_SESHIX_RUN_OLLAMA_TESTS") == "1",
    "real Ollama integration is opt-in",
)
class Skill02ValidationTests(unittest.TestCase):
    def test_neutral_company_context_does_not_become_direct_negative_analysis(self):
        primary = PrimaryContextVersion(
            version_id="PCV-VALIDATION",
            records=(
                PrimaryContextRecord(
                    "R1",
                    "company.activities",
                    fact(["impianti elettrici e tecnologici"], "EV-1"),
                ),
                PrimaryContextRecord(
                    "R2",
                    "company.employees",
                    fact(6, "EV-2"),
                ),
                PrimaryContextRecord(
                    "R3",
                    "company.country",
                    fact("Italia", "EV-3"),
                ),
            ),
        )
        runtime = Skill02CompanyAnalysisRuntime(
            OllamaCompanyAnalysis(
                model=os.environ.get(
                    "AGENTE_SESHIX_ANALYSIS_MODEL",
                    "qwen2.5:3b",
                )
            )
        )
        result = runtime.analyze(
            analysis_id="SKILL02-REAL-VALIDATION",
            primary_context=primary,
        )

        forbidden_direct = {
            AnalysisCategory.CRITICITA,
            AnalysisCategory.INEFFICIENZA,
            AnalysisCategory.GAP,
            AnalysisCategory.IMPROVEMENT_AREA,
            AnalysisCategory.RISK,
        }
        for finding in result.baseline.findings:
            self.assertNotIn(finding.category, forbidden_direct)
            for key in finding.basis_keys:
                self.assertIn(
                    key,
                    {"company.activities", "company.employees", "company.country"},
                )

        self.assertEqual(
            result.derived_state.dependencies[0].version_ref,
            "PCV-VALIDATION",
        )


if __name__ == "__main__":
    unittest.main()
