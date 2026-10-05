from __future__ import annotations

import base64
import hashlib
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from agente_seshix.domain.capability import CapabilityRequest
from agente_seshix.domain.connector import ConnectorAudit, ConnectorResult, ConnectorResultState


class GitHubConnectorAdapter:
    provider = "github"
    capabilities = ("REPOSITORY_READ",)

    def __init__(self, *, token: str, api_base: str = "https://api.github.com", timeout_seconds: float = 30.0) -> None:
        if not token.strip():
            raise ValueError("token must not be empty")
        self._token = token
        self._api_base = api_base.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._provider_calls = 0

    def execute(self, request: CapabilityRequest) -> ConnectorResult:
        if request.provider != self.provider or request.capability not in self.capabilities:
            return self._failure(request, "CONNECTOR_REQUEST_MISMATCH")

        resource = request.resource_map()
        repository = resource.get("repository")
        path = resource.get("path")
        if not repository or not path:
            return self._failure(request, "INVALID_RESOURCE")

        try:
            repo = self._get_json(f"/repos/{quote(repository, safe='/')}")
            default_branch = repo["default_branch"]
            commit = self._get_json(
                f"/repos/{quote(repository, safe='/')}/commits/{quote(default_branch, safe='')}"
            )
            commit_sha = commit["sha"]
            item = self._get_json(
                f"/repos/{quote(repository, safe='/')}/contents/{quote(path, safe='/')}?ref={commit_sha}"
            )
            content = base64.b64decode(item["content"].replace("\n", ""))
        except HTTPError as exc:
            return self._failure(request, self._http_reason(exc.code))
        except (URLError, TimeoutError):
            return self._failure(request, "PROVIDER_UNAVAILABLE")
        except (KeyError, ValueError, TypeError, json.JSONDecodeError):
            return self._failure(request, "RESPONSE_INVALID")

        return ConnectorResult(
            state=ConnectorResultState.EXECUTED,
            audit=ConnectorAudit(
                request_id=request.request_id,
                provider=self.provider,
                capability=request.capability,
                provider_calls=self._provider_calls,
                resource=request.resource,
            ),
            data={
                "repository": repository,
                "path": path,
                "default_branch": default_branch,
                "commit_sha": commit_sha,
                "blob_sha": item["sha"],
                "content_sha256": hashlib.sha256(content).hexdigest(),
                "byte_count": len(content),
            },
        )

    def _get_json(self, path: str) -> dict:
        self._provider_calls += 1
        request = Request(
            f"{self._api_base}{path}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self._token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "Agente-seshix-connector-runtime-v1",
            },
            method="GET",
        )
        with urlopen(request, timeout=self._timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))

    def _failure(self, request: CapabilityRequest, reason: str) -> ConnectorResult:
        return ConnectorResult(
            state=ConnectorResultState.FAILED,
            audit=ConnectorAudit(
                request_id=request.request_id,
                provider=self.provider,
                capability=request.capability,
                provider_calls=self._provider_calls,
                resource=request.resource,
                reason=reason,
            ),
        )

    @staticmethod
    def _http_reason(status: int) -> str:
        if status == 401:
            return "AUTH_REQUIRED"
        if status == 403:
            return "ACCESS_DENIED"
        if status == 404:
            return "RESOURCE_NOT_FOUND"
        if status == 429:
            return "RATE_LIMITED"
        return "PROVIDER_REQUEST_FAILED"
