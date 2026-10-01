import unittest

from agente_seshix.application.context_repository import PrimaryContextRepository
from agente_seshix.application.evidence_repository import EvidenceRepository
from agente_seshix.application.update_primary_context import (
    BaseContextVersionNotFound,
    EvidenceNotFound,
    UpdatePrimaryContextCommand,
    UpdatePrimaryContextUseCase,
)
from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)
from agente_seshix.domain.evidence import Evidence, SourceReference
from agente_seshix.domain.primary_context import PrimaryContextRecord, PrimaryContextVersion


class InMemoryPrimaryContextRepository:
    def __init__(self) -> None:
        self._versions: dict[str, PrimaryContextVersion] = {}

    def save(self, version: PrimaryContextVersion) -> None:
        self._versions[version.version_id] = version

    def get(self, version_id: str) -> PrimaryContextVersion | None:
        return self._versions.get(version_id)


class InMemoryEvidenceRepository:
    def __init__(self) -> None:
        self._evidence: dict[str, Evidence] = {}

    def save(self, evidence: Evidence) -> None:
        self._evidence[evidence.evidence_id] = evidence

    def get(self, evidence_id: str) -> Evidence | None:
        return self._evidence.get(evidence_id)


def make_record(record_id: str, key: str, value: str, version: str) -> PrimaryContextRecord:
    return PrimaryContextRecord(
        record_id=record_id,
        key=key,
        value=ContextValue(
            value=value,
            classification=EvidenceClassification.FATTO,
            provenance=(Provenance("source://caller-unverified"),),
            version=version,
        ),
    )


class UpdatePrimaryContextUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryPrimaryContextRepository()
        self.evidence_repository = InMemoryEvidenceRepository()
        self.assertIsInstance(self.repository, PrimaryContextRepository)
        self.assertIsInstance(self.evidence_repository, EvidenceRepository)
        self.base_record = make_record("CTX-1", "company.name", "ACME", "1")
        self.base = PrimaryContextVersion(
            version_id="PCV-1",
            records=(self.base_record,),
        )
        self.repository.save(self.base)
        self.evidence = Evidence(
            evidence_id="EV-1",
            claim="Company legal name is ACME SRL",
            evidence={"legal_name": "ACME SRL"},
            source=SourceReference("source://company-register"),
            version="1",
        )
        self.evidence_repository.save(self.evidence)
        self.use_case = UpdatePrimaryContextUseCase(
            self.repository,
            self.evidence_repository,
        )

    def command(self, record: PrimaryContextRecord) -> UpdatePrimaryContextCommand:
        return UpdatePrimaryContextCommand("PCV-1", "PCV-2", record, ("EV-1",))

    def test_replaces_existing_key_and_creates_new_version(self) -> None:
        updated = make_record("CTX-2", "company.name", "ACME SRL", "2")
        result = self.use_case.execute(self.command(updated))
        self.assertEqual(result.records[0].value.value, "ACME SRL")
        self.assertEqual(result.previous_version_id, "PCV-1")
        self.assertEqual(self.repository.get("PCV-2"), result)

    def test_appends_new_key(self) -> None:
        new_record = make_record("CTX-2", "company.country", "IT", "1")
        result = self.use_case.execute(self.command(new_record))
        self.assertEqual(len(result.records), 2)
        self.assertEqual(result.records[1].key, "company.country")

    def test_base_version_is_not_mutated(self) -> None:
        updated = make_record("CTX-2", "company.name", "ACME SRL", "2")
        self.use_case.execute(self.command(updated))
        self.assertEqual(self.base.records, (self.base_record,))
        self.assertIs(self.repository.get("PCV-1"), self.base)

    def test_missing_base_version_is_rejected(self) -> None:
        record = make_record("CTX-2", "company.name", "ACME", "1")
        with self.assertRaises(BaseContextVersionNotFound):
            self.use_case.execute(
                UpdatePrimaryContextCommand("PCV-MISSING", "PCV-2", record, ("EV-1",))
            )

    def test_missing_evidence_blocks_update_before_save(self) -> None:
        record = make_record("CTX-2", "company.name", "ACME SRL", "2")
        with self.assertRaises(EvidenceNotFound) as error:
            self.use_case.execute(
                UpdatePrimaryContextCommand("PCV-1", "PCV-2", record, ("EV-MISSING",))
            )
        self.assertEqual(error.exception.evidence_id, "EV-MISSING")
        self.assertIsNone(self.repository.get("PCV-2"))

    def test_verified_provenance_uses_resolved_evidence(self) -> None:
        updated = make_record("CTX-2", "company.name", "ACME SRL", "2")
        result = self.use_case.execute(self.command(updated))
        provenance = result.records[0].value.provenance
        self.assertEqual(
            provenance,
            (Provenance("source://company-register", evidence_id="EV-1"),),
        )

    def test_caller_supplied_unverified_provenance_is_replaced(self) -> None:
        updated = make_record("CTX-2", "company.name", "ACME SRL", "2")
        result = self.use_case.execute(self.command(updated))
        self.assertNotIn(
            Provenance("source://caller-unverified"),
            result.records[0].value.provenance,
        )

    def test_empty_base_version_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UpdatePrimaryContextCommand("", "PCV-2", self.base_record, ("EV-1",))

    def test_empty_new_version_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UpdatePrimaryContextCommand("PCV-1", "", self.base_record, ("EV-1",))

    def test_empty_evidence_ids_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UpdatePrimaryContextCommand("PCV-1", "PCV-2", self.base_record, ())

    def test_duplicate_evidence_ids_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UpdatePrimaryContextCommand(
                "PCV-1",
                "PCV-2",
                self.base_record,
                ("EV-1", "EV-1"),
            )


if __name__ == "__main__":
    unittest.main()
