import unittest

from agente_seshix.application.context_repository import PrimaryContextRepository
from agente_seshix.application.update_primary_context import (
    BaseContextVersionNotFound,
    UpdatePrimaryContextCommand,
    UpdatePrimaryContextUseCase,
)
from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)
from agente_seshix.domain.primary_context import PrimaryContextRecord, PrimaryContextVersion


class InMemoryPrimaryContextRepository:
    def __init__(self) -> None:
        self._versions: dict[str, PrimaryContextVersion] = {}

    def save(self, version: PrimaryContextVersion) -> None:
        self._versions[version.version_id] = version

    def get(self, version_id: str) -> PrimaryContextVersion | None:
        return self._versions.get(version_id)


def make_record(record_id: str, key: str, value: str, version: str) -> PrimaryContextRecord:
    return PrimaryContextRecord(
        record_id=record_id,
        key=key,
        value=ContextValue(
            value=value,
            classification=EvidenceClassification.FATTO,
            provenance=(Provenance("source://test"),),
            version=version,
        ),
    )


class UpdatePrimaryContextUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryPrimaryContextRepository()
        self.assertIsInstance(self.repository, PrimaryContextRepository)
        self.base_record = make_record("CTX-1", "company.name", "ACME", "1")
        self.base = PrimaryContextVersion(
            version_id="PCV-1",
            records=(self.base_record,),
        )
        self.repository.save(self.base)
        self.use_case = UpdatePrimaryContextUseCase(self.repository)

    def test_replaces_existing_key_and_creates_new_version(self) -> None:
        updated = make_record("CTX-2", "company.name", "ACME SRL", "2")
        result = self.use_case.execute(
            UpdatePrimaryContextCommand("PCV-1", "PCV-2", updated)
        )
        self.assertEqual(result.records, (updated,))
        self.assertEqual(result.previous_version_id, "PCV-1")
        self.assertEqual(self.repository.get("PCV-2"), result)

    def test_appends_new_key(self) -> None:
        new_record = make_record("CTX-2", "company.country", "IT", "1")
        result = self.use_case.execute(
            UpdatePrimaryContextCommand("PCV-1", "PCV-2", new_record)
        )
        self.assertEqual(result.records, (self.base_record, new_record))

    def test_base_version_is_not_mutated(self) -> None:
        updated = make_record("CTX-2", "company.name", "ACME SRL", "2")
        self.use_case.execute(UpdatePrimaryContextCommand("PCV-1", "PCV-2", updated))
        self.assertEqual(self.base.records, (self.base_record,))
        self.assertIs(self.repository.get("PCV-1"), self.base)

    def test_missing_base_version_is_rejected(self) -> None:
        record = make_record("CTX-2", "company.name", "ACME", "1")
        with self.assertRaises(BaseContextVersionNotFound):
            self.use_case.execute(
                UpdatePrimaryContextCommand("PCV-MISSING", "PCV-2", record)
            )

    def test_empty_base_version_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UpdatePrimaryContextCommand("", "PCV-2", self.base_record)

    def test_empty_new_version_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UpdatePrimaryContextCommand("PCV-1", "", self.base_record)


if __name__ == "__main__":
    unittest.main()
