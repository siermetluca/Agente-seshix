from __future__ import annotations

from agente_seshix.application.connector_port import ConnectorPort
from agente_seshix.domain.capability import CapabilityRequest


class ConnectorUnavailable(LookupError):
    pass


class ConnectorResolver:
    def __init__(self, connectors: tuple[ConnectorPort, ...]) -> None:
        registry: dict[tuple[str, str], ConnectorPort] = {}
        for connector in connectors:
            if not connector.provider.strip():
                raise ValueError("connector provider must not be empty")
            for capability in connector.capabilities:
                key = (connector.provider, capability)
                if key in registry:
                    raise ValueError(f"duplicate connector registration: {key}")
                registry[key] = connector
        self._registry = registry

    def resolve(self, request: CapabilityRequest) -> ConnectorPort:
        connector = self._registry.get((request.provider, request.capability))
        if connector is None:
            raise ConnectorUnavailable(
                f"no connector for provider={request.provider!r} capability={request.capability!r}"
            )
        return connector
