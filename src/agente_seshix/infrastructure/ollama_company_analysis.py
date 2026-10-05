from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from agente_seshix.application.skill_02_company_analysis import (
    CompanyAnalysisRequest,
    RawAnalysisFinding,
    RawCompanyAnalysisOutput,
    RawContextChangeCandidate,
)


class OllamaCompanyAnalysisError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class OllamaCompanyAnalysis:
    model: str = "qwen2.5:3b"
    endpoint: str = "http://127.0.0.1:11434"
    timeout_seconds: float = 120.0

    def analyze(self, request: CompanyAnalysisRequest) -> RawCompanyAnalysisOutput:
        payload = {
            "model": self.model,
            "stream": False,
            "format": self._response_schema(request),
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
            raise OllamaCompanyAnalysisError(
                f"Ollama company analysis request failed: {error}"
            ) from error

        raw_text = envelope.get("response")
        if not isinstance(raw_text, str) or not raw_text.strip():
            raise OllamaCompanyAnalysisError(
                "Ollama response did not contain analysis JSON"
            )
        try:
            decoded = json.loads(raw_text)
        except json.JSONDecodeError as error:
            raise OllamaCompanyAnalysisError(
                "Ollama analysis response is not valid JSON"
            ) from error

        findings = decoded.get("findings")
        candidates = decoded.get("context_change_candidates")
        if not isinstance(findings, list) or not isinstance(candidates, list):
            raise OllamaCompanyAnalysisError(
                "analysis response requires findings and context_change_candidates lists"
            )

        present_keys = {
            record.key for record in request.primary_context.records
        }
        hypothesis_basis_keys = {
            record.key
            for record in request.primary_context.records
            if record.value.classification.value == "IPOTESI"
        }

        sanitized_candidates = tuple(
            self._sanitize_candidate(item, present_keys)
            for item in candidates
            if isinstance(item, dict)
        )
        candidate_ids = {
            candidate.candidate_id
            for candidate in sanitized_candidates
            if isinstance(candidate.candidate_id, str)
            and candidate.candidate_id.strip()
        }

        sanitized_findings = []
        for item in findings:
            if not isinstance(item, dict):
                continue
            finding = self._sanitize_finding(
                item,
                candidate_ids,
                hypothesis_basis_keys,
            )
            if finding is not None:
                sanitized_findings.append(finding)

        return RawCompanyAnalysisOutput(
            findings=tuple(sanitized_findings),
            context_change_candidates=sanitized_candidates,
        )

    def _dedupe_values(self, values) -> tuple:
        unique = []
        for value in values:
            if value not in unique:
                unique.append(value)
        return tuple(unique)

    def _sanitize_candidate(
        self,
        item: dict,
        present_keys: set[str],
    ) -> RawContextChangeCandidate:
        requested_information = item.get("requested_information")
        requested_key = self._normalize_requested_key(
            requested_information,
            item.get("requested_key"),
            present_keys,
        )
        reason = item.get("reason")
        if isinstance(requested_information, str) and requested_information.strip():
            reason = (
                "Dato richiesto da SKILL_02 per verificare l'analisi "
                "senza assumere informazioni mancanti: "
                f"{requested_information.strip()}"
            )
        return RawContextChangeCandidate(
            candidate_id=item.get("candidate_id"),
            requested_information=requested_information,
            reason=reason,
            requested_key=requested_key,
        )

    def _normalize_requested_key(
        self,
        requested_information,
        requested_key,
        present_keys: set[str],
    ):
        if not isinstance(requested_key, str) or not requested_key.strip():
            return None
        requested_key = requested_key.strip()
        if requested_key in present_keys:
            return None
        if not isinstance(requested_information, str):
            return None

        markers = {
            "company.name": ("nome", "ragione sociale", "name"),
            "company.activities": ("attivit", "activity", "activities"),
            "company.employees": ("dipendent", "personale", "employee", "staff"),
            "company.owner_count": ("titol", "soci", "owner"),
            "company.admin_staff": ("amministr", "admin"),
            "company.country": ("paese", "country", "nazione"),
            "company.revenue": ("fattur", "ricav", "revenue"),
        }
        allowed_markers = markers.get(requested_key)
        if allowed_markers is None:
            return None

        normalized = requested_information.lower()
        if any(marker in normalized for marker in allowed_markers):
            return requested_key
        return None

    def _sanitize_finding(
        self,
        item: dict,
        valid_candidate_ids: set[str],
        hypothesis_basis_keys: set[str],
    ) -> RawAnalysisFinding | None:
        basis_keys = self._dedupe_values(item.get("basis_keys", ()))
        verification_candidate_ids = tuple(
            value
            for value in self._dedupe_values(
                item.get("verification_candidate_ids", ())
            )
            if value in valid_candidate_ids
        )
        category = item.get("category")
        statement = item.get("statement")

        supported = True
        if category == "CAPABILITY":
            supported = any(self._is_capability_key(key) for key in basis_keys)
        elif category == "ASSET":
            supported = any(self._is_asset_key(key) for key in basis_keys)
        elif category in {
            "CRITICITA",
            "INEFFICIENZA",
            "GAP",
            "IMPROVEMENT_AREA",
            "RISK",
        }:
            supported = any(
                self._is_negative_signal_key(key)
                for key in basis_keys
            )

        if not supported:
            category = "HYPOTHESIS"

        if category == "HYPOTHESIS":
            inherited_hypothesis = any(
                key in hypothesis_basis_keys
                for key in basis_keys
            )
            if not verification_candidate_ids and not inherited_hypothesis:
                return None
        else:
            verification_candidate_ids = ()

        return RawAnalysisFinding(
            finding_id=item.get("finding_id"),
            category=category,
            statement=statement,
            basis_keys=basis_keys,
            verification_candidate_ids=verification_candidate_ids,
        )

    def _response_schema(self, request: CompanyAnalysisRequest) -> dict:
        categories = ["HYPOTHESIS"]
        if any(
            self._is_capability_key(record.key)
            for record in request.primary_context.records
        ):
            categories.append("CAPABILITY")
        if any(
            self._is_asset_key(record.key)
            for record in request.primary_context.records
        ):
            categories.append("ASSET")
        if any(
            self._is_negative_signal_key(record.key)
            for record in request.primary_context.records
        ):
            categories.extend([
                "CRITICITA",
                "INEFFICIENZA",
                "GAP",
                "IMPROVEMENT_AREA",
                "RISK",
            ])

        all_keys = [
            record.key
            for record in request.primary_context.records
            if record.value.classification.value != "UNKNOWN"
        ]
        canonical_v1_keys = {
            "company.name",
            "company.activities",
            "company.employees",
            "company.owner_count",
            "company.admin_staff",
            "company.country",
            "company.revenue",
        }
        present_keys = {record.key for record in request.primary_context.records}
        missing_keys = sorted(canonical_v1_keys - present_keys)
        requested_key_schema = (
            {
                "anyOf": [
                    {"type": "string", "enum": missing_keys},
                    {"type": "null"},
                ]
            }
            if missing_keys
            else {"type": "null"}
        )

        return {
            "type": "object",
            "properties": {
                "findings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "finding_id": {"type": "string"},
                            "category": {
                                "type": "string",
                                "enum": categories,
                            },
                            "statement": {"type": "string"},
                            "basis_keys": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": all_keys,
                                },
                                "minItems": 1,
                                "uniqueItems": True,
                            },
                            "verification_candidate_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "uniqueItems": True,
                            },
                        },
                        "required": [
                            "finding_id",
                            "category",
                            "statement",
                            "basis_keys",
                            "verification_candidate_ids",
                        ],
                        "additionalProperties": False,
                    },
                },
                "context_change_candidates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "candidate_id": {"type": "string"},
                            "requested_information": {"type": "string"},
                            "reason": {"type": "string"},
                            "requested_key": requested_key_schema,
                        },
                        "required": [
                            "candidate_id",
                            "requested_information",
                            "reason",
                            "requested_key",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["findings", "context_change_candidates"],
            "additionalProperties": False,
        }

    def _is_capability_key(self, key: str) -> bool:
        normalized = key.lower()
        return any(
            marker in normalized
            for marker in (
                "activities",
                "activity",
                "capabil",
                "competenc",
                "skill",
                "service",
                "product",
            )
        )

    def _is_asset_key(self, key: str) -> bool:
        normalized = key.lower()
        return any(
            marker in normalized
            for marker in (
                "asset",
                "hardware",
                "software",
                "equipment",
                "tool",
                "certification",
                "license",
                "vehicle",
                "machine",
                "property",
            )
        )

    def _is_negative_signal_key(self, key: str) -> bool:
        normalized = key.lower()
        return any(
            marker in normalized
            for marker in (
                "critical",
                "critic",
                "inefficien",
                "gap",
                "risk",
                "constraint",
                "problem",
                "issue",
                "bottleneck",
                "limitation",
            )
        )

    def _prompt(self, request: CompanyAnalysisRequest) -> str:
        rows = []
        for record in request.primary_context.records:
            rows.append(
                {
                    "key": record.key,
                    "classification": record.value.classification.value,
                    "value": record.value.value,
                }
            )
        context_json = json.dumps(rows, ensure_ascii=False, indent=2)
        return f"""You are SKILL_02, an internal company analysis engine.
Analyze ONLY the validated PRIMARY_CONTEXT below.
Do not use market knowledge, typical-company assumptions, external benchmarks, or unstated facts.

Return JSON only.

Rules:
- Every finding must cite one or more exact basis_keys present in PRIMARY_CONTEXT.
- ASSET and CAPABILITY may directly describe explicit positive facts/capabilities in the context.
- Do NOT conclude CRITICITA, INEFFICIENZA, GAP, RISK or IMPROVEMENT_AREA from neutral facts such as employee count, country, company name, or activity alone.
- A direct negative category is allowed only when a cited context key itself explicitly represents a problem, constraint, risk, gap, inefficiency, limitation or criticality.
- If a possible problem is merely plausible but not demonstrated, use HYPOTHESIS.
- Every HYPOTHESIS based on FATTO context MUST list one or more verification_candidate_ids referencing context_change_candidates that specify the missing data needed to verify it. If no such missing data can be named, omit the hypothesis.
- Direct findings must use an empty verification_candidate_ids array.
- If important company information is missing for a conclusion, create a context_change_candidate instead of inventing the conclusion.
- context_change_candidate requested_information must name the concrete missing company datum. Its reason must not assert that a problem already exists.
- requested_key may be null for a new/refined context field. Never reuse an already-present key merely to ask for more detail.
- UNKNOWN context cannot support a finding.
- IPOTESI context may support only HYPOTHESIS.
- Keep statements in Italian.
- Do not request external market, competitor, pricing or demand data here; those belong to later skills.
- Use concise deterministic ids such as F-1 and C-1.

PRIMARY_CONTEXT version: {request.primary_context.version_id}
PRIMARY_CONTEXT:
{context_json}
"""
