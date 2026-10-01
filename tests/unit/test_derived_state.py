import unittest

from agente_seshix.domain.derived_state import DependencyReference, DerivedState


class DerivedStateTests(unittest.TestCase):
    def test_valid_dependency_reference(self) -> None:
        dependency = DependencyReference("CTX-0001", "PCV-0001")
        self.assertEqual(dependency.version_ref, "PCV-0001")

    def test_empty_dependency_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            DependencyReference("", "PCV-0001")

    def test_empty_version_ref_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            DependencyReference("CTX-0001", "   ")

    def test_valid_derived_state_is_fresh_by_default(self) -> None:
        dependency = DependencyReference("CTX-0001", "PCV-0001")
        state = DerivedState(
            state_id="DER-0001",
            value={"analysis": "candidate"},
            dependencies=(dependency,),
        )
        self.assertFalse(state.stale)

    def test_empty_state_id_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            DerivedState(state_id="", value=None, dependencies=())

    def test_mark_stale_returns_new_instance(self) -> None:
        state = DerivedState("DER-0001", "value", ())
        stale = state.mark_stale()
        self.assertFalse(state.stale)
        self.assertTrue(stale.stale)
        self.assertIsNot(state, stale)

    def test_mark_stale_is_idempotent(self) -> None:
        state = DerivedState("DER-0001", "value", (), stale=True)
        self.assertIs(state.mark_stale(), state)


if __name__ == "__main__":
    unittest.main()
