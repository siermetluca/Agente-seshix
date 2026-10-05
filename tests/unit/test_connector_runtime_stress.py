import unittest
from urllib.error import URLError

from agente_seshix.application.authority_policy import AuthorityPolicy
from agente_seshix.application.connector_execution import ConnectorExecutionUseCase
from agente_seshix.application.connector_resolver import ConnectorResolver
from agente_seshix.domain.capability import CapabilityRequest
from agente_seshix.domain.connector import ConnectorResultState
from agente_seshix.infrastructure.github_connector import GitHubConnectorAdapter


class CountingConnector:
    provider = "github"
    capabilities = ("REPOSITORY_READ",)

    def __init__(self):
        self.calls = 0

    def execute(self, request):
        self.calls += 1
        raise AssertionError("provider must not be called")


class ProviderUnavailableAdapter(GitHubConnectorAdapter):
    def _get_json(self, path: str) -> dict:
        raise URLError("controlled provider unavailable")


class InvalidResponseAdapter(GitHubConnectorAdapter):
    def _get_json(self, path: str) -> dict:
        return {"unexpected": "shape"}


class ReusableSuccessAdapter(GitHubConnectorAdapter):
    def _get_json(self, path: str) -> dict:
        if "/contents/" in path:
            return {"sha": "b" * 40, "content": "aGVsbG8="}
        if "/commits/" in path:
            return {"sha": "a" * 40}
        return {"default_branch": "main"}


def request(*, capability="REPOSITORY_READ", repository="siermetluca/Context-Siermet", path="README.md"):
    return CapabilityRequest.from_mappings(
        request_id="REQ-STRESS",
        actor_id="DEV_AGENT",
        capability=capability,
        provider="github",
        resource={"repository": repository, "path": path},
    )


def policy(expression="ALLOW"):
    return AuthorityPolicy(
        version="0.1",
        actors=("DEV_AGENT",),
        actions={"read_repository": expression},
    )


AUTHORIZED = {"repository": "siermetluca/Context-Siermet", "path": "README.md"}


class ConnectorRuntimeStressTests(unittest.TestCase):
    def test_auth_deny_has_zero_provider_calls(self):
        connector = CountingConnector()
        decision, result = ConnectorExecutionUseCase(ConnectorResolver((connector,))).execute(
            request=request(),
            policy_action="read_repository",
            policy=policy("DENY"),
            authorized_resource=AUTHORIZED,
        )
        self.assertEqual(decision.outcome.value, "DENY")
        self.assertEqual(result.state, ConnectorResultState.DENIED)
        self.assertEqual(result.audit.reason, "AUTHORITY_DENIED")
        self.assertEqual(result.audit.provider_calls, 0)
        self.assertEqual(connector.calls, 0)

    def test_connector_absent_fails_closed_with_zero_provider_calls(self):
        _, result = ConnectorExecutionUseCase(ConnectorResolver(())).execute(
            request=request(),
            policy_action="read_repository",
            policy=policy(),
            authorized_resource=AUTHORIZED,
        )
        self.assertEqual(result.state, ConnectorResultState.FAILED)
        self.assertEqual(result.audit.reason, "CONNECTOR_UNAVAILABLE")
        self.assertEqual(result.audit.provider_calls, 0)

    def test_provider_unavailable_is_explicit_failure(self):
        adapter = ProviderUnavailableAdapter(token="controlled-token")
        _, result = ConnectorExecutionUseCase(ConnectorResolver((adapter,))).execute(
            request=request(),
            policy_action="read_repository",
            policy=policy(),
            authorized_resource=AUTHORIZED,
        )
        self.assertEqual(result.state, ConnectorResultState.FAILED)
        self.assertEqual(result.audit.reason, "PROVIDER_UNAVAILABLE")
        self.assertEqual(result.audit.provider_calls, 1)

    def test_invalid_provider_response_is_explicit_failure(self):
        adapter = InvalidResponseAdapter(token="controlled-token")
        _, result = ConnectorExecutionUseCase(ConnectorResolver((adapter,))).execute(
            request=request(),
            policy_action="read_repository",
            policy=policy(),
            authorized_resource=AUTHORIZED,
        )
        self.assertEqual(result.state, ConnectorResultState.FAILED)
        self.assertEqual(result.audit.reason, "RESPONSE_INVALID")
        self.assertEqual(result.audit.provider_calls, 1)

    def test_provider_call_audit_is_request_scoped_when_adapter_is_reused(self):
        adapter = ReusableSuccessAdapter(token="controlled-token")
        use_case = ConnectorExecutionUseCase(ConnectorResolver((adapter,)))

        _, first = use_case.execute(
            request=request(),
            policy_action="read_repository",
            policy=policy(),
            authorized_resource=AUTHORIZED,
        )
        _, second = use_case.execute(
            request=request(),
            policy_action="read_repository",
            policy=policy(),
            authorized_resource=AUTHORIZED,
        )

        self.assertEqual(first.state, ConnectorResultState.EXECUTED)
        self.assertEqual(second.state, ConnectorResultState.EXECUTED)
        self.assertEqual(first.audit.provider_calls, 3)
        self.assertEqual(second.audit.provider_calls, 3)


if __name__ == "__main__":
    unittest.main()
