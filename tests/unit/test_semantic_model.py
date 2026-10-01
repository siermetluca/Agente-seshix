import unittest

from agente_seshix.application.semantic_model import (
    RawSemanticCandidate,
    RawSemanticOutput,
    SemanticModelPort,
    SemanticModelRequest,
    SemanticOutputValidationError,
    StructuredSemanticService,
)
from agente_seshix.domain.context_evidence import EvidenceClassification


class FakeSemanticModel:
    def __init__(self, output):
        self.output = output
        self.requests = []

    def generate(self, request):
        self.requests.append(request)
        return self.output


class SemanticModelTests(unittest.TestCase):
    def request(self):
        return SemanticModelRequest(
            request_id="SEM-1",
            source_text="Siermet SRLS installa impianti elettrici.",
            purpose="extract_company_context",
            schema_version="1",
        )

    def test_fake_provider_satisfies_port(self):
        model = FakeSemanticModel(RawSemanticOutput(candidates=()))
        self.assertIsInstance(model, SemanticModelPort)

    def test_valid_fact_candidate_is_returned_only_after_validation(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.name",
                        claim="The company name is Siermet SRLS.",
                        classification="FATTO",
                        value="Siermet SRLS",
                    ),
                )
            )
        )
        result = StructuredSemanticService(model).execute(self.request())
        self.assertEqual(result.request_id, "SEM-1")
        self.assertEqual(result.validator_version, "1")
        self.assertEqual(result.candidates[0].classification, EvidenceClassification.FATTO)
        self.assertEqual(result.candidates[0].value, "Siermet SRLS")
    def test_valid_hypothesis_candidate_remains_hypothesis(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.hiring_need",
                        claim="The company may need another technician.",
                        classification="IPOTESI",
                        value="may need another technician",
                    ),
                )
            )
        )
        result = StructuredSemanticService(model).execute(self.request())
        self.assertEqual(
            result.candidates[0].classification,
            EvidenceClassification.IPOTESI,
        )

    def test_valid_unknown_has_no_value(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.revenue",
                        claim="Revenue is not available.",
                        classification="UNKNOWN",
                        value=None,
                    ),
                )
            )
        )
        result = StructuredSemanticService(model).execute(self.request())
        self.assertIsNone(result.candidates[0].value)

    def test_unknown_with_value_is_rejected(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.revenue",
                        claim="Revenue is unknown.",
                        classification="UNKNOWN",
                        value=100000,
                    ),
                )
            )
        )
        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(model).execute(self.request())
    def test_fact_without_value_is_rejected(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.name",
                        claim="The company has a name.",
                        classification="FATTO",
                        value=None,
                    ),
                )
            )
        )
        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(model).execute(self.request())

    def test_unknown_classification_is_rejected(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.name",
                        claim="The company name is Siermet.",
                        classification="CERTAIN",
                        value="Siermet",
                    ),
                )
            )
        )
        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(model).execute(self.request())

    def test_developer_value_cannot_be_used_as_semantic_key(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="Siermet SRLS",
                        claim="The company name is Siermet SRLS.",
                        classification="FATTO",
                        value="Siermet SRLS",
                    ),
                )
            )
        )
        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(model).execute(self.request())
    def test_source_uri_only_cannot_be_claim(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.name",
                        claim="human://owner",
                        classification="FATTO",
                        value="Siermet SRLS",
                    ),
                )
            )
        )
        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(model).execute(self.request())

    def test_waiting_hitl_cannot_be_business_value(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="company.revenue",
                        claim="Revenue is WAITING_HITL.",
                        classification="FATTO",
                        value="WAITING_HITL",
                    ),
                )
            )
        )
        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(model).execute(self.request())

    def test_requires_hitl_cannot_be_business_key(self):
        model = FakeSemanticModel(
            RawSemanticOutput(
                candidates=(
                    RawSemanticCandidate(
                        key="REQUIRES_HITL",
                        claim="This is a runtime token.",
                        classification="FATTO",
                        value="IT",
                    ),
                )
            )
        )
        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(model).execute(self.request())
    def test_non_raw_provider_output_is_rejected(self):
        class BadProvider:
            def generate(self, request):
                return {"company.name": "Siermet"}

        with self.assertRaises(SemanticOutputValidationError):
            StructuredSemanticService(BadProvider()).execute(self.request())

    def test_request_requires_non_empty_source_text(self):
        with self.assertRaises(ValueError):
            SemanticModelRequest(
                request_id="SEM-X",
                source_text=" ",
                purpose="extract_company_context",
                schema_version="1",
            )

    def test_service_calls_provider_once(self):
        model = FakeSemanticModel(RawSemanticOutput(candidates=()))
        request = self.request()
        StructuredSemanticService(model).execute(request)
        self.assertEqual(model.requests, [request])


if __name__ == "__main__":
    unittest.main()
