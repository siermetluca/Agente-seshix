import os
import unittest

from agente_seshix.application.authority_policy import AuthorityPolicy
from agente_seshix.application.connector_execution import ConnectorExecutionUseCase
from agente_seshix.application.connector_resolver import ConnectorResolver
from agente_seshix.application.flow_execution import FlowExecutionEnvelope, FlowRun, FlowRunState
from agente_seshix.application.task_context_resolver import TaskContextResolver
from agente_seshix.domain.capability import CapabilityRequest
from agente_seshix.domain.connector import ConnectorResultState
from agente_seshix.domain.task_context import ContextSection, Task, TaskContextRequirements
from agente_seshix.infrastructure.github_connector import GitHubConnectorAdapter


TOKEN = os.environ.get("SIERMET_GITHUB_TOKEN")


@unittest.skipUnless(TOKEN, "SIERMET_GITHUB_TOKEN not available")
class GitHubConnectorRuntimeIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.authorized_resource = {
            "repository": "siermetluca/Context-Siermet",
            "path": "README.md",
        }
        self.policy = AuthorityPolicy(
            version="0.1",
            actors=("DEV_AGENT",),
            actions={"read_repository": "ALLOW"},
        )

    def _package(self):
        task = Task("TASK-GH-READ-1", "REPOSITORY_READ", "Read exact repository file")
        requirements = TaskContextRequirements(
            task_id=task.task_id,
            required_sections=(ContextSection.CAPABILITIES, ContextSection.AUTHORITY),
        )
        package = TaskContextResolver().resolve(
            task,
            requirements,
            {
                ContextSection.CAPABILITIES: {"REPOSITORY_READ": {"provider": "github"}},
                ContextSection.AUTHORITY: {"authorized_resource": self.authorized_resource},
            },
        )
        return task, package

    def test_real_repository_read_traverses_core_runtime_components(self) -> None:
        task, package = self._package()
        flow = FlowExecutionEnvelope()
        run = flow.start(FlowRun(run_id="RUN-GH-READ-1", task=task, context_package=package))
        run = flow.begin_step(run, "STEP-GH-READ", "execute GitHub REPOSITORY_READ")

        request = CapabilityRequest.from_mappings(
            request_id="REQ-GH-READ-1",
            actor_id="DEV_AGENT",
            capability="REPOSITORY_READ",
            provider="github",
            resource=self.authorized_resource,
        )
        adapter = GitHubConnectorAdapter(token=TOKEN)
        decision, result = ConnectorExecutionUseCase(ConnectorResolver((adapter,))).execute(
            request=request,
            policy_action="read_repository",
            policy=self.policy,
            authorized_resource=package.get(ContextSection.AUTHORITY)["authorized_resource"],
        )
        run = flow.record_authority(run, decision)
        self.assertEqual(result.state, ConnectorResultState.EXECUTED)
        run = flow.pass_step(run, result=result.data)
        run = flow.complete(run, result=result.data)

        self.assertEqual(run.state, FlowRunState.PASSED)
        self.assertEqual(run.steps[-1].authority_decision.outcome.value, "ALLOW")
        self.assertEqual(result.audit.provider, "github")
        self.assertEqual(result.audit.capability, "REPOSITORY_READ")
        self.assertEqual(result.audit.provider_calls, 3)
        self.assertEqual(result.data["repository"], self.authorized_resource["repository"])
        self.assertEqual(result.data["path"], self.authorized_resource["path"])
        self.assertEqual(len(result.data["commit_sha"]), 40)
        self.assertEqual(len(result.data["blob_sha"]), 40)
        self.assertEqual(len(result.data["content_sha256"]), 64)
        self.assertGreater(result.data["byte_count"], 0)

    def test_out_of_scope_repository_is_denied_before_provider_call(self) -> None:
        _, package = self._package()
        request = CapabilityRequest.from_mappings(
            request_id="REQ-GH-READ-DENY",
            actor_id="DEV_AGENT",
            capability="REPOSITORY_READ",
            provider="github",
            resource={"repository": "siermetluca/OUTSIDE-AUTHORIZED-SCOPE", "path": "README.md"},
        )
        adapter = GitHubConnectorAdapter(token=TOKEN)
        _, result = ConnectorExecutionUseCase(ConnectorResolver((adapter,))).execute(
            request=request,
            policy_action="read_repository",
            policy=self.policy,
            authorized_resource=package.get(ContextSection.AUTHORITY)["authorized_resource"],
        )
        self.assertEqual(result.state, ConnectorResultState.DENIED)
        self.assertEqual(result.audit.reason, "RESOURCE_SCOPE_MISMATCH")
        self.assertEqual(result.audit.provider_calls, 0)


if __name__ == "__main__":
    unittest.main()
