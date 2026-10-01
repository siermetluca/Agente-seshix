import unittest

from agente_seshix.application.evidence_repository import EvidenceRepository
from agente_seshix.domain.evidence import Evidence, SourceReference


class InMemoryEvidenceRepository:
    def __init__(self) -> None:
        self._evidence: dict[str, Evidence] = {}

    def save(self, evidence: Evidence) -> None:
        self._evidence[evidence.evidence_id] = evidence

    def get(self, evidence_id: str) -> Evidence | None:
        return self._evidence.get(evidence_id)


class EvidenceRepositoryPortTests(unittest.TestCase):
    def test_in_memory_repository_satisfies_port(self) -> None:
        repository = InMemoryEvidenceRepository()
        self.assertIsInstance(repository, EvidenceRepository)

    def test_save_and_get_round_trip(self) -> None:
        repository = InMemoryEvidenceRepository()
        evidence = Evidence(
            evidence_id="EV-0001",
            claim="The company is registered.",
            evidence={"registration_number": "123"},
            source=SourceReference("source://company-register"),
            version="1",
        )
        repository.save(evidence)
        self.assertEqual(repository.get("EV-0001"), evidence)

    def test_missing_evidence_returns_none(self) -> None:
        repository = InMemoryEvidenceRepository()
        self.assertIsNone(repository.get("EV-MISSING"))


if __name__ == "__main__":
    unittest.main()
