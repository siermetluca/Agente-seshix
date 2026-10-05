import unittest

from agente_seshix.application.authority_policy import AuthorityPolicy
from agente_seshix.application.connector_execution import ConnectorExecutionUseCase
from agente_seshix.application.connector_resolver import ConnectorResolver, ConnectorUnavailable
from agente_seshix.domain.capability import CapabilityRequest
from agente_seshix.domain.connector import ConnectorAudit, ConnectorResult, ConnectorResultState


class FakeConnector:
    provider = "github"
    capabilities = ("REPOSITORY_READ",)

    def __init__(self) -> None:
        self.calls = 0

    def execute(self, request: CapabilityRequest) -> ConnectorResult:
        self.calls += 1
        return ConnectorResult(
            state=ConnectorResultState.EXECUTED,
            audit=ConnectorAudit(
                request_id=request.request_id,
                provider=self.provider,
                capability=request.capability,
                provider_calls=self.calls,
                resource=request.resource,
            ),
            data={"ok": True},
        )


def make_request(repository: str = "siermetluca/Context-Siermet") -> CapabilityRequest:
    return CapabilityRequest.from_mappings(
        request_id="REQ-1",
        actor_id="DEV_AGENT",
        capability="REPOSITORY_READ",
        provider="github",
        resource={"repository": repository, "path": "README.md"},
    )


def make_policy(expression: str = "ALLOW") -> AuthorityPolicy:
    return AuthorityPolicy(
        version="0.1",
        actors=("DEV_AGENT",),
        actions={"read_repository": expression},
    )


class ConnectorRuntimeTests(unittest.TestCase):
    def test_capability_request_is_stable_and_exact(self) -> None:
        request = make_request()
        self.assertEqual(request.resource_map()["repository"], "siermetluca/Context-Siermet")
        self.assertEqual(request.capability, "REPOSITORY_READ")

    def test_request_rejects_duplicate_resource_keys(self) -> None:
        with self.assertRaises(ValueError):
            CapabilityRequest(
                request_id="REQ-1",
                actor_id="DEV_AGENT",
                capability="REPOSITORY_READ",
                provider="github",
                resource=(("repository", "a"), ("repository", "b")),
            )

    def test_resolver_matches_provider_and_capability(self) -> None:
        connector = FakeConnector()
        self.assertIs(ConnectorResolver((connector,)).resolve(make_request()), connector)

    def test_resolver_fails_closed_for_unknown_capability(self) -> None:
        connector = FakeConnector()
        request = CapabilityRequest.from_mappings(
            request_id="REQ-2",
            actor_id="DEV_AGENT",
            capability="FILE_UPDATE",
            provider="github",
            resource={"repository": "x", "path": "y"},
        )
        with self.assertRaises(ConnectorUnavailable):
            ConnectorResolver((connector,)).resolve(request)

    def test_authority_denial_stops_before_provider(self) -> None:
        connector = FakeConnector()
        decision, result = ConnectorExecutionUseCase(ConnectorResolver((connector,))).execute(
            request=make_request(),
            policy_action="read_repository",
            policy=make_policy("DENY"),
            authorized_resource={"repository": "siermetluca/Context-Siermet", "path": "README.md"},
        )
        self.assertEqual(decision.outcome.value, "DENY")
        self.assertEqual(result.state, ConnectorResultState.DENIED)
        self.assertEqual(result.audit.provider_calls, 0)
        self.assertEqual(connector.calls, 0)

    def test_resource_scope_mismatch_stops_before_provider(self) -> None:
        connector = FakeConnector()
        _, result = ConnectorExecutionUseCase(ConnectorResolver((connector,))).execute(
            request=make_request("siermetluca/OUTSIDE"),
            policy_action="read_repository",
            policy=make_policy(),
            authorized_resource={"repository": "siermetluca/Context-Siermet", "path": "README.md"},
        )
        self.assertEqual(result.state, ConnectorResultState.DENIED)
        self.assertEqual(result.audit.reason, "RESOURCE_SCOPE_MISMATCH")
        self.assertEqual(result.audit.provider_calls, 0)
        self.assertEqual(connector.calls, 0)

    def test_authorized_request_reaches_connector(self) -> None:
        connector = FakeConnector()
        decision, result = ConnectorExecutionUseCase(ConnectorResolver((connector,))).execute(
            request=make_request(),
            policy_action="read_repository",
            policy=make_policy(),
            authorized_resource={"repository": "siermetluca/Context-Siermet", "path": "README.md"},
        )
        self.assertEqual(decision.outcome.value, "ALLOW")
        self.assertEqual(result.state, ConnectorResultState.EXECUTED)
        self.assertEqual(connector.calls, 1)


if __name__ == "__main__":
    unittest.main()
