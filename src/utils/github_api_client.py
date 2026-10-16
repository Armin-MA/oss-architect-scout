"""GitHub API client utility executing HTTP requests with authentication and timeouts."""

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from src.entities.candidate_repo import CandidateRepo

try:
    from src.contracts.i_github_client import IGitHubClient
except (ImportError, ModuleNotFoundError):
    from abc import ABC, abstractmethod

    class IGitHubClient(ABC):  # type: ignore[no-redef]
        """Fallback interface for GitHub client when contracts layer is unlinked."""

        @abstractmethod
        def search_repositories(self, query: str, limit: int = 10) -> List[CandidateRepo]:
            """Search GitHub repositories by query string."""
            pass

        @abstractmethod
        def get_repository_tree(self, full_name: str) -> List[str]:
            """Retrieve recursive file paths in repository."""
            pass

        @abstractmethod
        def get_file_content(self, full_name: str, path: str) -> str:
            """Fetch raw text content of a file in the repository."""
            pass

        @abstractmethod
        def check_ci_status(self, full_name: str) -> str:
            """Check recent CI workflow conclusion."""
            pass


class GitHubAPIClient(IGitHubClient):
    """Network client for GitHub API v3 using standard library urllib."""

    def __init__(
        self,
        auth_token: Optional[str] = None,
        base_url: str = "https://api.github.com",
        timeout: float = 10.0,
    ) -> None:
        self.auth_token = auth_token
        self.base_url = base_url.rstrip("/")
        self.timeout = float(timeout) if timeout > 0 else 10.0

    def _build_request(self, endpoint: str, extra_headers: Optional[Dict[str, str]] = None) -> urllib.request.Request:
        """Construct an HTTP request with authentication and standard GitHub headers."""
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}/{endpoint.lstrip('/')}"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "OSS-Architect-Scout")
        req.add_header("Accept", "application/vnd.github.v3+json")

        if self.auth_token:
            req.add_header("Authorization", f"Bearer {self.auth_token}")

        if extra_headers:
            for k, v in extra_headers.items():
                req.add_header(k, v)

        return req

    def _execute_request(self, req: urllib.request.Request) -> Optional[bytes]:
        """Execute request and handle network and HTTP errors cleanly without crashing."""
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                return response.read()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
            return None

    def search_repositories(self, query: str, limit: int = 10) -> List[CandidateRepo]:
        """Search repositories using GitHub Search API.

        Args:
            query: Search query string (e.g. 'clean architecture stars:>100')
            limit: Maximum items to return (capped to [1, 100])

        Returns:
            List of parsed CandidateRepo instances.
        """
        if not query or not query.strip():
            return []

        limit = max(1, min(100, int(limit)))
        encoded_query = urllib.parse.quote_plus(query.strip())
        endpoint = f"search/repositories?q={encoded_query}&per_page={limit}&sort=stars&order=desc"
        req = self._build_request(endpoint)

        raw_data = self._execute_request(req)
        if not raw_data:
            return []

        try:
            payload = json.loads(raw_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return []

        items = payload.get("items", [])
        candidates: List[CandidateRepo] = []

        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            full_name = item.get("full_name")
            if not name or not full_name:
                continue

            stars = item.get("stargazers_count", 0)
            forks = item.get("forks_count", 0)
            license_data = item.get("license")
            license_spdx = (
                license_data.get("spdx_id")
                if isinstance(license_data, dict)
                else None
            )
            open_issues = item.get("open_issues_count", 0)
            default_branch = item.get("default_branch") or "main"
            updated_at = item.get("updated_at") or ""
            description = item.get("description") or ""

            try:
                candidate = CandidateRepo(
                    name=str(name),
                    full_name=str(full_name),
                    stars=max(0, int(stars)),
                    forks=max(0, int(forks)),
                    license_spdx=license_spdx,
                    open_issues=max(0, int(open_issues)),
                    default_branch=str(default_branch),
                    updated_at=str(updated_at),
                    description=str(description),
                )
                candidates.append(candidate)
            except ValueError:
                continue

        return candidates[:limit]

    def get_repository_tree(self, full_name: str) -> List[str]:
        """Retrieve recursive tree paths for repository.

        Args:
            full_name: Repository name with owner (e.g. 'tiangolo/fastapi')

        Returns:
            List of file paths relative to repository root.
        """
        if not full_name or "/" not in full_name:
            return []

        endpoint = f"repos/{full_name}/git/trees/HEAD?recursive=1"
        req = self._build_request(endpoint)
        raw_data = self._execute_request(req)
        if not raw_data:
            return []

        try:
            payload = json.loads(raw_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return []

        tree_items = payload.get("tree", [])
        paths: List[str] = []
        for entry in tree_items:
            if isinstance(entry, dict) and "path" in entry:
                paths.append(str(entry["path"]))

        return paths

    def get_file_content(self, full_name: str, path: str) -> str:
        """Fetch content of a file in the repository.

        Args:
            full_name: Repository owner/name
            path: Relative path to file

        Returns:
            Decoded string content of file, or empty string if not found.
        """
        if not full_name or not path:
            return ""

        clean_path = path.lstrip("/")
        endpoint = f"repos/{full_name}/contents/{clean_path}"
        req = self._build_request(
            endpoint,
            extra_headers={"Accept": "application/vnd.github.v3.raw"},
        )
        raw_data = self._execute_request(req)
        if not raw_data:
            return ""

        try:
            return raw_data.decode("utf-8")
        except UnicodeDecodeError:
            # Fallback in case raw returned base64-json representation
            try:
                payload = json.loads(raw_data.decode("latin1"))
                if isinstance(payload, dict) and payload.get("encoding") == "base64":
                    content_bytes = base64.b64decode(payload.get("content", ""))
                    return content_bytes.decode("utf-8", errors="replace")
            except Exception:
                pass
            return ""

    def check_ci_status(self, full_name: str) -> str:
        """Check the latest CI workflow conclusion for the repository.

        Args:
            full_name: Repository owner/name

        Returns:
            Conclusion status: 'success', 'failure', 'pending', or 'unknown'
        """
        if not full_name or "/" not in full_name:
            return "unknown"

        endpoint = f"repos/{full_name}/actions/runs?per_page=1"
        req = self._build_request(endpoint)
        raw_data = self._execute_request(req)
        if not raw_data:
            return "unknown"

        try:
            payload = json.loads(raw_data.decode("utf-8"))
            runs = payload.get("workflow_runs", [])
            if runs and isinstance(runs[0], dict):
                conclusion = runs[0].get("conclusion")
                status = runs[0].get("status")
                if conclusion:
                    return str(conclusion).lower()
                if status:
                    return str(status).lower()
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

        return "unknown"
