import json
import unittest
from unittest.mock import patch

from agente_seshix.application.skill_02_company_analysis import CompanyAnalysisRequest
from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)
from agente_seshix.domain.primary_context import PrimaryContextRecord, PrimaryContextVersion
from agente_seshix.infrastructure.ollama_company_analysis import OllamaCompanyAnalysis


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


def primary_context():
    return PrimaryContextVersion(
        version_id="PCV-1",
        records=(
            PrimaryContextRecord(
                "R1",
                "company.activities",
                ContextValue(
                    value=["impianti elettrici e tecnologici"],
                    classification=EvidenceClassification.FATTO,
                    provenance=(Provenance("human://owner", "EV-1"),),
                    version="1",
                ),
            ),
        ),
    )


class OllamaCompanyAnalysisTests(unittest.TestCase):
    def test_maps_structured_ollama_response(self):
        semantic = {
            "findings": [
                {
                    "finding_id": "F-1",
                    "category": "CAPABILITY",
                    "statement": "Le attività tecniche dichiarate costituiscono una capability.",
                    "basis_keys": ["company.activities"],
                    "verification_candidate_ids": [],
                }
            ],
            "context_change_candidates": [
                {
                    "candidate_id": "C-1",
                    "requested_information": "numero dipendenti",
                    "reason": "Serve per analizzare la capacità operativa.",
                    "requested_key": "company.employees",
                }
            ],
        }
        envelope = {"response": json.dumps(semantic)}
        with patch(
            "urllib.request.urlopen",
            return_value=FakeResponse(envelope),
        ):
            output = OllamaCompanyAnalysis().analyze(
                CompanyAnalysisRequest("A-1", primary_context())
            )

        self.assertEqual(output.findings[0].finding_id, "F-1")
        self.assertEqual(output.findings[0].basis_keys, ("company.activities",))
        self.assertEqual(
            output.context_change_candidates[0].requested_key,
            "company.employees",
        )

    def test_prompt_contains_only_context_and_internal_rules(self):
        adapter = OllamaCompanyAnalysis()
        prompt = adapter._prompt(CompanyAnalysisRequest("A-1", primary_context()))
        self.assertIn("company.activities", prompt)
        self.assertIn("PRIMARY_CONTEXT", prompt)
        self.assertIn("Do not use market knowledge", prompt)
        self.assertIn("use HYPOTHESIS", prompt)

    def test_schema_constrains_categories_for_neutral_context(self):
        schema = OllamaCompanyAnalysis()._response_schema(
            CompanyAnalysisRequest("A-1", primary_context())
        )
        finding_schema = schema["properties"]["findings"]["items"]
        categories = finding_schema["properties"]["category"]["enum"]
        self.assertIn("CAPABILITY", categories)
        self.assertIn("HYPOTHESIS", categories)
        self.assertNotIn("ASSET", categories)
        self.assertNotIn("RISK", categories)
        self.assertEqual(
            finding_schema["properties"]["basis_keys"]["items"]["enum"],
            ["company.activities"],
        )

    def test_schema_allows_negative_categories_only_with_negative_signal_key(self):
        negative_context = PrimaryContextVersion(
            version_id="PCV-RISK",
            records=(
                PrimaryContextRecord(
                    "R-RISK",
                    "company.constraints.capacity_risk",
                    ContextValue(
                        value="capacità insufficiente nei picchi",
                        classification=EvidenceClassification.FATTO,
                        provenance=(Provenance("human://owner", "EV-RISK"),),
                        version="1",
                    ),
                ),
            ),
        )
        schema = OllamaCompanyAnalysis()._response_schema(
            CompanyAnalysisRequest("A-RISK", negative_context)
        )
        categories = (
            schema["properties"]["findings"]["items"]
            ["properties"]["category"]["enum"]
        )
        self.assertIn("RISK", categories)

    def test_unsupported_direct_category_is_demoted_when_verifiable(self):
        adapter = OllamaCompanyAnalysis()
        finding = adapter._sanitize_finding(
            {
                "finding_id": "F-X",
                "category": "ASSET",
                "statement": "Una persona amministrativa rende la gestione efficiente.",
                "basis_keys": ["company.admin_staff"],
                "verification_candidate_ids": ["C-1"],
            },
            {"C-1"},
            set(),
        )
        self.assertIsNotNone(finding)
        self.assertEqual(finding.category, "HYPOTHESIS")
        self.assertEqual(
            finding.verification_candidate_ids,
            ("C-1",),
        )

    def test_unsupported_direct_category_without_verification_is_dropped(self):
        adapter = OllamaCompanyAnalysis()
        finding = adapter._sanitize_finding(
            {
                "finding_id": "F-X",
                "category": "ASSET",
                "statement": "Una persona amministrativa rende la gestione efficiente.",
                "basis_keys": ["company.admin_staff"],
                "verification_candidate_ids": [],
            },
            set(),
            set(),
        )
        self.assertIsNone(finding)

    def test_known_requested_key_is_normalized_to_unbound_candidate(self):
        semantic = {
            "findings": [],
            "context_change_candidates": [
                {
                    "candidate_id": "C-1",
                    "requested_information": "più dettagli sulle attività",
                    "reason": "Serve maggiore dettaglio.",
                    "requested_key": "company.activities",
                }
            ],
        }
        envelope = {"response": json.dumps(semantic)}
        with patch(
            "urllib.request.urlopen",
            return_value=FakeResponse(envelope),
        ):
            output = OllamaCompanyAnalysis().analyze(
                CompanyAnalysisRequest("A-2", primary_context())
            )
        self.assertIsNone(output.context_change_candidates[0].requested_key)


if __name__ == "__main__":
    unittest.main()
