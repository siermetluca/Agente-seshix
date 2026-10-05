from __future__ import annotations

from typing import Mapping

from agente_seshix.application.authority_policy import (
    AuthorityEvaluationContext,
    AuthorityPolicy,
    AuthorityPolicyEvaluator,
)
from agente_seshix.application.connector_resolver import ConnectorResolver, ConnectorUnavailable
from agente_seshix.domain.authority import AuthorityDecision, AuthorityOutcome
from agente_seshix.domain.capability import CapabilityRequest
from agente_seshix.domain.connector import ConnectorAudit, ConnectorResult, ConnectorResultState


class ConnectorExecutionUseCase:
    def __init__(self, resolver: ConnectorResolver, evaluator: AuthorityPolicyEvaluator | None = None) -> None:
        self._resolver = resolver
        self._evaluator = evaluator or AuthorityPolicyEvaluator()

    def execute(
        self,
        *,
        request: CapabilityRequest,
        policy_action: str,
        policy: AuthorityPolicy,
        authorized_resource: Mapping[str, str],
        authority_context: AuthorityEvaluationContext | None = None,
    ) -> tuple[AuthorityDecision, ConnectorResult]:
        decision = self._evaluator.evaluate(
            decision_id=f"AUTH-{request.request_id}",
            actor_id=request.actor_id,
            action=policy_action,
            policy=policy,
            context=authority_context,
        )

        if decision.outcome is not AuthorityOutcome.ALLOW:
            return decision, self._local_result(
                request,
                ConnectorResultState.DENIED,
                "AUTHORITY_DENIED",
            )

        if request.resource_map() != dict(authorized_resource):
            return decision, self._local_result(
                request,
                ConnectorResultState.DENIED,
                "RESOURCE_SCOPE_MISMATCH",
            )

        try:
            connector = self._resolver.resolve(request)
        except ConnectorUnavailable:
            return decision, self._local_result(
                request,
                ConnectorResultState.FAILED,
                "CONNECTOR_UNAVAILABLE",
            )

        return decision, connector.execute(request)

    @staticmethod
    def _local_result(
        request: CapabilityRequest,
        state: ConnectorResultState,
        reason: str,
    ) -> ConnectorResult:
        return ConnectorResult(
            state=state,
            audit=ConnectorAudit(
                request_id=request.request_id,
                provider=request.provider,
                capability=request.capability,
                provider_calls=0,
                resource=request.resource,
                reason=reason,
            ),
        )
