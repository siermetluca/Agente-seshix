import unittest

from agente_seshix.domain.evidence import Evidence, SourceReference


class EvidenceTests(unittest.TestCase):
    def test_valid_source_reference(self) -> None:
        source = SourceReference("source://company-register")
        self.assertEqual(source.source_ref, "source://company-register")

    def test_empty_source_reference_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SourceReference("   ")

    def test_valid_evidence(self) -> None:
        item = Evidence(
            evidence_id="EV-0001",
            claim="The company is registered.",
            evidence={"registration_number": "123"},
            source=SourceReference("source://company-register"),
            version="1",
        )
        self.assertEqual(item.evidence_id, "EV-0001")

    def test_empty_evidence_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Evidence(
                evidence_id="",
                claim="Claim",
                evidence="data",
                source=SourceReference("source://example"),
                version="1",
            )

    def test_empty_claim_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Evidence(
                evidence_id="EV-0002",
                claim="   ",
                evidence="data",
                source=SourceReference("source://example"),
                version="1",
            )

    def test_empty_version_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Evidence(
                evidence_id="EV-0003",
                claim="Claim",
                evidence="data",
                source=SourceReference("source://example"),
                version="",
            )


if __name__ == "__main__":
    unittest.main()
