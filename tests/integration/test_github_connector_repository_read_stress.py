import os
import unittest

from agente_seshix.application.authority_policy import AuthorityPolicy
from agente_seshix.application.connector_execution import ConnectorExecutionUseCase
from agente_seshix.application.connector_resolver import ConnectorResolver
from agente_seshix.domain.capability import CapabilityRequest
from agente_seshix.domain.connector import ConnectorResultState
from agente_seshix.infrastructure.github_connector import GitHubConnectorAdapter

TOKEN = os.environ.get("SIERMET_GITHUB_TOKEN")


def make_policy():
    return AuthorityPolicy(version="0.1", actors=("DEV_AGENT",), actions={"read_repository": "ALLOW"})


def make_request(path: str):
    return CapabilityRequest.from_mappings(
        request_id=f"REQ-STRESS-{path}",
        actor_id="DEV_AGENT",
        capability="REPOSITORY_READ",
        provider="github",
        resource={"repository": "siermetluca/Context-Siermet", "path": path},
    )


@unittest.skipUnless(TOKEN, "SIERMET_GITHUB_TOKEN not available")
class GitHubConnectorRepositoryReadStressIntegrationTests(unittest.TestCase):
    def test_missing_file_maps_to_resource_not_found(self):
        request = make_request("__SIERMET_CONNECTOR_MISSING_FILE__")
        adapter = GitHubConnectorAdapter(token=TOKEN)
        _, result = ConnectorExecutionUseCase(ConnectorResolver((adapter,))).execute(
            request=request,
            policy_action="read_repository",
            policy=make_policy(),
            authorized_resource=request.resource_map(),
        )
        self.assertEqual(result.state, ConnectorResultState.FAILED)
        self.assertEqual(result.audit.reason, "RESOURCE_NOT_FOUND")
        self.assertEqual(result.audit.provider_calls, 3)

    def test_invalid_credential_maps_to_auth_required(self):
        request = make_request("README.md")
        adapter = GitHubConnectorAdapter(token="definitely-invalid-siermet-token")
        _, result = ConnectorExecutionUseCase(ConnectorResolver((adapter,))).execute(
            request=request,
            policy_action="read_repository",
            policy=make_policy(),
            authorized_resource=request.resource_map(),
        )
        self.assertEqual(result.state, ConnectorResultState.FAILED)
        self.assertIn(result.audit.reason, {"AUTH_REQUIRED", "ACCESS_DENIED"})
        self.assertEqual(result.audit.provider_calls, 1)


if __name__ == "__main__":
    unittest.main()
