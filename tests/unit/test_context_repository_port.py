import unittest

from agente_seshix.application.context_repository import PrimaryContextRepository
from agente_seshix.domain.primary_context import PrimaryContextVersion


class InMemoryPrimaryContextRepository:
    def __init__(self) -> None:
        self._versions: dict[str, PrimaryContextVersion] = {}

    def save(self, version: PrimaryContextVersion) -> None:
        self._versions[version.version_id] = version

    def get(self, version_id: str) -> PrimaryContextVersion | None:
        return self._versions.get(version_id)


class ContextRepositoryPortTests(unittest.TestCase):
    def test_in_memory_repository_satisfies_port(self) -> None:
        repository = InMemoryPrimaryContextRepository()
        self.assertIsInstance(repository, PrimaryContextRepository)

    def test_save_and_get_round_trip(self) -> None:
        repository = InMemoryPrimaryContextRepository()
        version = PrimaryContextVersion(version_id="PCV-0001", records=())
        repository.save(version)
        self.assertEqual(repository.get("PCV-0001"), version)

    def test_missing_version_returns_none(self) -> None:
        repository = InMemoryPrimaryContextRepository()
        self.assertIsNone(repository.get("PCV-MISSING"))


if __name__ == "__main__":
    unittest.main()
