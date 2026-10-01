from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from agente_seshix.domain.context_evidence import EvidenceClassification


class SemanticOutputValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class SemanticModelRequest:
    request_id: str
    source_text: str
    purpose: str
    schema_version: str

    def __post_init__(self) -> None:
        for name, value in (
            ("request_id", self.request_id),
            ("source_text", self.source_text),
            ("purpose", self.purpose),
            ("schema_version", self.schema_version),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class RawSemanticCandidate:
    key: Any
    claim: Any
    classification: Any
    value: Any = None


@dataclass(frozen=True, slots=True)
class RawSemanticOutput:
    candidates: tuple[RawSemanticCandidate, ...]


@runtime_checkable
class SemanticModelPort(Protocol):
    def generate(self, request: SemanticModelRequest) -> RawSemanticOutput:
        ...
@dataclass(frozen=True, slots=True)
class SemanticCandidate:
    key: str
    claim: str
    classification: EvidenceClassification
    value: Any


@dataclass(frozen=True, slots=True)
class SemanticOutput:
    request_id: str
    schema_version: str
    validator_version: str
    candidates: tuple[SemanticCandidate, ...]


class SemanticOutputValidator:
    VERSION = "1"

    _KEY_RE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*$")
    _URI_ONLY_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://\S+$")
    _CONTROL_TOKENS = frozenset(
        {
            "READY",
            "RUNNING",
            "WAITING_HITL",
            "PASSED",
            "BLOCKED",
            "FAILED",
            "ALLOW",
            "DENY",
            "REQUIRES_HITL",
            "DRAFT",
            "TESTING",
            "ACTIVE",
            "DEPRECATED",
            "DISABLED",
        }
    )

    def validate(
        self,
        request: SemanticModelRequest,
        raw: RawSemanticOutput,
    ) -> SemanticOutput:
        if not isinstance(raw, RawSemanticOutput):
            raise SemanticOutputValidationError(
                "provider output must be RawSemanticOutput"
            )

        validated = tuple(
            self._validate_candidate(candidate)
            for candidate in raw.candidates
        )
        return SemanticOutput(
            request_id=request.request_id,
            schema_version=request.schema_version,
            validator_version=self.VERSION,
            candidates=validated,
        )
    def _validate_candidate(
        self,
        raw: RawSemanticCandidate,
    ) -> SemanticCandidate:
        if not isinstance(raw, RawSemanticCandidate):
            raise SemanticOutputValidationError(
                "candidate must be RawSemanticCandidate"
            )

        if not isinstance(raw.key, str) or not raw.key.strip():
            raise SemanticOutputValidationError("candidate key must be non-empty string")
        key = raw.key.strip()
        if not self._KEY_RE.fullmatch(key):
            raise SemanticOutputValidationError(
                f"invalid semantic key: {key!r}"
            )
        if key.upper() in self._CONTROL_TOKENS:
            raise SemanticOutputValidationError(
                f"runtime control token cannot be semantic key: {key!r}"
            )

        if not isinstance(raw.claim, str) or not raw.claim.strip():
            raise SemanticOutputValidationError(
                "candidate claim must be non-empty string"
            )
        claim = raw.claim.strip()
        if self._URI_ONLY_RE.fullmatch(claim):
            raise SemanticOutputValidationError(
                "candidate claim cannot be only a source URI"
            )

        classification = self._classification(raw.classification)
        value = raw.value

        if classification is EvidenceClassification.UNKNOWN:
            if value is not None:
                raise SemanticOutputValidationError(
                    "UNKNOWN candidate must not assert a concrete value"
                )
        else:
            if value is None:
                raise SemanticOutputValidationError(
                    f"{classification.value} candidate requires a value"
                )
            self._validate_business_value(value)

        return SemanticCandidate(
            key=key,
            claim=claim,
            classification=classification,
            value=value,
        )
    def _classification(self, value: Any) -> EvidenceClassification:
        if isinstance(value, EvidenceClassification):
            return value
        if not isinstance(value, str):
            raise SemanticOutputValidationError(
                "classification must be a canonical string"
            )
        try:
            return EvidenceClassification(value.strip())
        except ValueError as error:
            raise SemanticOutputValidationError(
                f"unknown classification: {value!r}"
            ) from error

    def _validate_business_value(self, value: Any) -> None:
        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                raise SemanticOutputValidationError(
                    "business value must not be blank"
                )
            if normalized.upper() in self._CONTROL_TOKENS:
                raise SemanticOutputValidationError(
                    f"runtime control token cannot be business value: {value!r}"
                )


class StructuredSemanticService:
    def __init__(
        self,
        model: SemanticModelPort,
        validator: SemanticOutputValidator | None = None,
    ) -> None:
        if not isinstance(model, SemanticModelPort):
            raise TypeError("model must implement SemanticModelPort")
        self._model = model
        self._validator = validator or SemanticOutputValidator()

    def execute(self, request: SemanticModelRequest) -> SemanticOutput:
        raw = self._model.generate(request)
        return self._validator.validate(request, raw)
