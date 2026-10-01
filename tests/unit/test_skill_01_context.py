import unittest

from agente_seshix.application.context_repository import PrimaryContextRepository
from agente_seshix.application.evidence_repository import EvidenceRepository
from agente_seshix.application.skill_01_context import (
    Skill01ContextCommand,
    Skill01ContextRuntime,
    Skill01ContextStatus,
)
from agente_seshix.application.update_primary_context import EvidenceNotFound
from agente_seshix.domain.context_evidence import EvidenceClassification
from agente_seshix.domain.evidence import Evidence, SourceReference
from agente_seshix.domain.primary_context import PrimaryContextVersion


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


class Skill01ContextRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.context_repository = InMemoryPrimaryContextRepository()
        self.evidence_repository = InMemoryEvidenceRepository()
        self.assertIsInstance(self.context_repository, PrimaryContextRepository)
        self.assertIsInstance(self.evidence_repository, EvidenceRepository)

        self.base = PrimaryContextVersion(version_id="PCV-0", records=())
        self.context_repository.save(self.base)
        self.evidence = Evidence(
            evidence_id="EV-1",
            claim="The company has six employees.",
            evidence={"employees": 6},
            source=SourceReference("source://user/company-profile"),
            version="1",
        )

        self.evidence_repository.save(self.evidence)
        self.runtime = Skill01ContextRuntime(
            self.context_repository,
            self.evidence_repository,
        )

    def test_fact_uses_registered_evidence_payload(self) -> None:
        result = self.runtime.execute(
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-1",
                key="company.employees",
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id="EV-1",
            )
        )
        record = result.context_version.records[0]
        self.assertEqual(result.status, Skill01ContextStatus.WRITTEN)
        self.assertEqual(record.value.value, {"employees": 6})
        self.assertEqual(record.value.classification, EvidenceClassification.FATTO)
        self.assertEqual(record.value.provenance[0].evidence_id, "EV-1")
        self.assertEqual(result.context_version.previous_version_id, "PCV-0")


    def test_fact_cannot_accept_caller_replacement_value(self) -> None:
        with self.assertRaises(ValueError):
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-1",
                key="company.employees",
                classification=EvidenceClassification.FATTO,
                context_value_version="1",
                evidence_id="EV-1",
                proposed_value=999,
            )

    def test_hypothesis_remains_hypothesis(self) -> None:
        result = self.runtime.execute(
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-2",
                key="company.growth_hypothesis",
                classification=EvidenceClassification.IPOTESI,
                context_value_version="1",
                evidence_id="EV-1",
                proposed_value="Hiring may be needed.",
            )
        )

        record = result.context_version.records[0]
        self.assertEqual(record.value.value, "Hiring may be needed.")
        self.assertEqual(record.value.classification, EvidenceClassification.IPOTESI)
        self.assertEqual(record.value.provenance[0].evidence_id, "EV-1")

    def test_required_unknown_returns_waiting_hitl_and_does_not_write(self) -> None:
        result = self.runtime.execute(
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-3",
                key="company.revenue",
                classification=EvidenceClassification.UNKNOWN,
                context_value_version="1",
                required=True,
            )
        )
        self.assertEqual(result.status, Skill01ContextStatus.WAITING_HITL)
        self.assertIsNone(result.context_version)
        self.assertIsNone(self.context_repository.get("PCV-1"))

    def test_non_required_unknown_does_not_write(self) -> None:
        result = self.runtime.execute(
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-4",
                key="company.optional_note",

                classification=EvidenceClassification.UNKNOWN,
                context_value_version="1",
                required=False,
            )
        )
        self.assertEqual(result.status, Skill01ContextStatus.UNKNOWN)
        self.assertIsNone(result.context_version)
        self.assertIsNone(self.context_repository.get("PCV-1"))

    def test_missing_evidence_blocks_written_update(self) -> None:
        with self.assertRaises(EvidenceNotFound):
            self.runtime.execute(
                Skill01ContextCommand(
                    base_version_id="PCV-0",
                    new_version_id="PCV-1",
                    record_id="CTX-5",
                    key="company.employees",
                    classification=EvidenceClassification.FATTO,
                    context_value_version="1",
                    evidence_id="EV-MISSING",
                )
            )
        self.assertIsNone(self.context_repository.get("PCV-1"))


    def test_unknown_cannot_assert_concrete_value(self) -> None:
        with self.assertRaises(ValueError):
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-6",
                key="company.revenue",
                classification=EvidenceClassification.UNKNOWN,
                context_value_version="1",
                proposed_value=100000,
            )

    def test_hypothesis_requires_explicit_proposed_value(self) -> None:
        with self.assertRaises(ValueError):
            Skill01ContextCommand(
                base_version_id="PCV-0",
                new_version_id="PCV-1",
                record_id="CTX-7",
                key="company.hypothesis",
                classification=EvidenceClassification.IPOTESI,
                context_value_version="1",
                evidence_id="EV-1",
            )


if __name__ == "__main__":
    unittest.main()
