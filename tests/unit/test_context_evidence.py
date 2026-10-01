import unittest

from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)


class ContextEvidenceTests(unittest.TestCase):
    def test_valid_fact_requires_provenance(self) -> None:
        value = ContextValue(
            value="ACME SRL",
            classification=EvidenceClassification.FATTO,
            provenance=(Provenance("source://company-register"),),
            version="1",
        )
        self.assertEqual(value.classification, EvidenceClassification.FATTO)

    def test_fact_without_provenance_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ContextValue(
                value="ACME SRL",
                classification=EvidenceClassification.FATTO,
                provenance=(),
                version="1",
            )

    def test_hypothesis_may_exist_without_provenance(self) -> None:
        value = ContextValue(
            value="Potential growth constraint",
            classification=EvidenceClassification.IPOTESI,
            provenance=(),
            version="1",
        )
        self.assertEqual(value.classification, EvidenceClassification.IPOTESI)

    def test_unknown_requires_no_concrete_value(self) -> None:
        value = ContextValue(
            value=None,
            classification=EvidenceClassification.UNKNOWN,
            provenance=(),
            version="1",
        )
        self.assertIsNone(value.value)

    def test_unknown_with_value_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ContextValue(
                value="invented value",
                classification=EvidenceClassification.UNKNOWN,
                provenance=(),
                version="1",
            )

    def test_empty_provenance_reference_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Provenance("   ")

    def test_empty_version_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ContextValue(
                value="candidate",
                classification=EvidenceClassification.IPOTESI,
                provenance=(),
                version="",
            )


if __name__ == "__main__":
    unittest.main()
