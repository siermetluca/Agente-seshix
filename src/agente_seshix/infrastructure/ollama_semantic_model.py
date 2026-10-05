from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from agente_seshix.application.semantic_model import (
    RawSemanticCandidate,
    RawSemanticOutput,
    SemanticModelRequest,
)


class OllamaSemanticModelError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class OllamaSemanticModel:
    model: str = "llama3.1:8b"
    endpoint: str = "http://127.0.0.1:11434"
    timeout_seconds: float = 120.0

    def generate(self, request: SemanticModelRequest) -> RawSemanticOutput:
        payload = {
            "model": self.model,
            "stream": False,
            "format": self._response_schema(),
            "options": {"temperature": 0},
            "prompt": self._prompt(request),
        }
        http_request = urllib.request.Request(
            f"{self.endpoint.rstrip('/')}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                http_request,
                timeout=self.timeout_seconds,
            ) as response:
                envelope = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            raise OllamaSemanticModelError(
                f"Ollama request failed: {error}"
            ) from error

        raw_text = envelope.get("response")
        if not isinstance(raw_text, str) or not raw_text.strip():
            raise OllamaSemanticModelError(
                "Ollama response did not contain structured response text"
            )
        try:
            decoded = json.loads(raw_text)
        except json.JSONDecodeError as error:
            raise OllamaSemanticModelError(
                "Ollama semantic response is not valid JSON"
            ) from error

        candidates = decoded.get("candidates")
        if not isinstance(candidates, list):
            raise OllamaSemanticModelError(
                "Ollama semantic response must contain candidates list"
            )

        return RawSemanticOutput(
            candidates=tuple(
                RawSemanticCandidate(
                    key=item.get("key"),
                    claim=item.get("claim"),
                    classification=item.get("classification"),
                    value=item.get("value"),
                )
                for item in candidates
                if isinstance(item, dict)
            )
        )

    def _candidate_schema(
        self,
        classification: str,
        *,
        allow_null: bool,
    ) -> dict:
        value_schema = {"type": "null"} if allow_null else {
            "type": ["string", "number", "integer", "boolean", "array", "object"]
        }
        return {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "enum": [
                        "company.name",
                        "company.activities",
                        "company.employees",
                        "company.owner_count",
                        "company.admin_staff",
                        "company.country",
                        "company.revenue",
                    ],
                },
                "claim": {"type": "string"},
                "classification": {"const": classification},
                "value": value_schema,
            },
            "required": [
                "key",
                "claim",
                "classification",
                "value",
            ],
            "additionalProperties": False,
        }

    def _response_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "candidates": {
                    "type": "array",
                    "items": {
                        "oneOf": [
                            self._candidate_schema("FATTO", allow_null=False),
                            self._candidate_schema("IPOTESI", allow_null=False),
                            self._candidate_schema("UNKNOWN", allow_null=True),
                        ]
                    },
                }
            },
            "required": ["candidates"],
            "additionalProperties": False,
        }

    def _prompt(self, request: SemanticModelRequest) -> str:
        return f"""You are a constrained semantic extractor for company context.
Return JSON only, with exactly this top-level shape:
{{"candidates":[{{"key":"...","claim":"...","classification":"FATTO|IPOTESI|UNKNOWN","value":...}}]}}

Allowed keys:
- company.name
- company.activities
- company.employees
- company.owner_count
- company.admin_staff
- company.country
- company.revenue

Rules:
- Understand the user's intended semantics even when Source contains spelling mistakes, missing punctuation, informal grammar, abbreviations, or poorly formed phrases.
- Extract only information supported by the source text. Semantic understanding may choose the correct allowed key, but it must never invent a fact that is not supported.
- FATTO must be extractive in meaning: never add actions, services, capabilities or qualifiers absent from the source.
- For FATTO string values, prefer the user's source wording. You may normalize an obvious spelling/grammar error only when the intended meaning is unambiguous; the deterministic caller will rebind the interpreted value to an exact source span before accepting it as evidence.
- For company.activities, choose the complete activity phrase by meaning. Do not invent missing business meaning merely to make the sentence grammatical.
- If the intended meaning is genuinely ambiguous or two materially different interpretations are plausible, do not guess and do not emit that FATTO candidate. The caller will ask the user for clarification.
- For company.activities, preserve coordinated phrases as complete source phrases instead of splitting a modifier into a standalone activity.
- FATTO: explicitly stated information.
- IPOTESI: interpretation explicitly signaled as uncertain/possible.
- UNKNOWN: relevant information explicitly missing or unavailable; value must be null.
- Never create a candidate merely because an allowed key exists.
- Never use runtime/control words such as WAITING_HITL, REQUIRES_HITL, ALLOW, DENY as business values.
- For company.employees, company.owner_count and company.admin_staff, return the explicit quantity as a JSON integer, never as a phrase such as "6 dipendenti".
- Preserve other clearly numeric values as JSON numbers when the source explicitly states them.
- company.activities may be a JSON list of strings.
- claim must be a short natural-language statement grounded in the source.
- Do not add explanations outside the JSON.

Purpose: {request.purpose}
Source:
{request.source_text}
"""
