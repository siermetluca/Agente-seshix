import unittest

from agente_seshix.application.evidence_intake import (
    EvidenceAlreadyExists,
    EvidenceIntakeCommand,
    EvidenceIntakeUseCase,
)
from agente_seshix.application.evidence_repository import EvidenceRepository
from agente_seshix.domain.evidence import Evidence


class InMemoryEvidenceRepository:
    def __init__(self) -> None:
        self._evidence: dict[str, Evidence] = {}

    def save(self, evidence: Evidence) -> None:
        self._evidence[evidence.evidence_id] = evidence

    def get(self, evidence_id: str) -> Evidence | None:
        return self._evidence.get(evidence_id)


class EvidenceIntakeUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryEvidenceRepository()
        self.assertIsInstance(self.repository, EvidenceRepository)
        self.use_case = EvidenceIntakeUseCase(self.repository)

    def test_source_input_is_persisted_as_evidence(self) -> None:
        command = EvidenceIntakeCommand(
            evidence_id="EV-100",
            source_ref="source://user/company-profile",
            claim="The company installs electrical systems.",
            evidence={"activity": "electrical systems installation"},
            version="1",
        )

        result = self.use_case.execute(command)

        self.assertEqual(result.evidence_id, "EV-100")
        self.assertEqual(result.source.source_ref, "source://user/company-profile")
        self.assertEqual(self.repository.get("EV-100"), result)

    def test_payload_is_preserved(self) -> None:
        payload = {"employees": 6, "owner": 1, "admin": 1}
        result = self.use_case.execute(
            EvidenceIntakeCommand(
                evidence_id="EV-101",
                source_ref="source://user/company-profile",
                claim="The company has six employees.",
                evidence=payload,
                version="1",
            )
        )
        self.assertIs(result.evidence, payload)

    def test_duplicate_evidence_id_is_rejected_without_overwrite(self) -> None:
        first = EvidenceIntakeCommand(
            evidence_id="EV-102",
            source_ref="source://first",
            claim="First claim",
            evidence={"value": 1},
            version="1",
        )
        second = EvidenceIntakeCommand(
            evidence_id="EV-102",
            source_ref="source://second",
            claim="Second claim",
            evidence={"value": 2},
            version="2",
        )
        original = self.use_case.execute(first)

        with self.assertRaises(EvidenceAlreadyExists):
            self.use_case.execute(second)

        self.assertEqual(self.repository.get("EV-102"), original)

    def test_empty_evidence_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            EvidenceIntakeCommand("", "source://x", "claim", {}, "1")

    def test_empty_source_ref_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            EvidenceIntakeCommand("EV-1", "   ", "claim", {}, "1")

    def test_empty_claim_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            EvidenceIntakeCommand("EV-1", "source://x", "", {}, "1")

    def test_empty_version_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            EvidenceIntakeCommand("EV-1", "source://x", "claim", {}, "")


if __name__ == "__main__":
    unittest.main()
