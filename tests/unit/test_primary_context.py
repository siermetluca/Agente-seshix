import unittest

from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)
from agente_seshix.domain.primary_context import (
    PrimaryContextRecord,
    PrimaryContextVersion,
)


class PrimaryContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.value = ContextValue(
            value="ACME SRL",
            classification=EvidenceClassification.FATTO,
            provenance=(Provenance("source://company-register"),),
            version="1",
        )

    def test_valid_primary_context_record(self) -> None:
        record = PrimaryContextRecord(
            record_id="CTX-0001",
            key="company.legal_name",
            value=self.value,
        )
        self.assertEqual(record.key, "company.legal_name")

    def test_empty_record_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PrimaryContextRecord("", "company.legal_name", self.value)

    def test_empty_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PrimaryContextRecord("CTX-0001", "   ", self.value)

    def test_valid_initial_version(self) -> None:
        record = PrimaryContextRecord("CTX-0001", "company.legal_name", self.value)
        version = PrimaryContextVersion(
            version_id="PCV-0001",
            records=(record,),
        )
        self.assertIsNone(version.previous_version_id)

    def test_valid_next_version(self) -> None:
        version = PrimaryContextVersion(
            version_id="PCV-0002",
            records=(),
            previous_version_id="PCV-0001",
        )
        self.assertEqual(version.previous_version_id, "PCV-0001")

    def test_empty_version_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PrimaryContextVersion(version_id="", records=())

    def test_blank_previous_version_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PrimaryContextVersion(
                version_id="PCV-0002",
                records=(),
                previous_version_id="   ",
            )


if __name__ == "__main__":
    unittest.main()
