from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class CapabilityRequest:
    request_id: str
    actor_id: str
    capability: str
    provider: str
    resource: tuple[tuple[str, str], ...]
    parameters: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("request_id", self.request_id),
            ("actor_id", self.actor_id),
            ("capability", self.capability),
            ("provider", self.provider),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        self._validate_pairs("resource", self.resource, required=True)
        self._validate_pairs("parameters", self.parameters, required=False)

    @staticmethod
    def _validate_pairs(name: str, pairs: tuple[tuple[str, str], ...], *, required: bool) -> None:
        if required and not pairs:
            raise ValueError(f"{name} must not be empty")
        keys = [key for key, _ in pairs]
        if len(set(keys)) != len(keys):
            raise ValueError(f"{name} keys must be unique")
        for key, value in pairs:
            if not key.strip() or not value.strip():
                raise ValueError(f"{name} keys/values must not be empty")

    @classmethod
    def from_mappings(
        cls,
        *,
        request_id: str,
        actor_id: str,
        capability: str,
        provider: str,
        resource: Mapping[str, str],
        parameters: Mapping[str, str] | None = None,
    ) -> "CapabilityRequest":
        return cls(
            request_id=request_id,
            actor_id=actor_id,
            capability=capability,
            provider=provider,
            resource=tuple(sorted(resource.items())),
            parameters=tuple(sorted((parameters or {}).items())),
        )

    def resource_map(self) -> dict[str, str]:
        return dict(self.resource)

    def parameter_map(self) -> dict[str, str]:
        return dict(self.parameters)
