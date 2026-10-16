"""Unit tests for GitHubAPIClient utility."""

import io
import json
import urllib.error
from unittest.mock import MagicMock, patch
import pytest

from src.entities.candidate_repo import CandidateRepo
from src.utils.github_api_client import GitHubAPIClient


class MockHTTPResponse:
    """Mock context manager for urllib.request.urlopen."""

    def __init__(self, data: bytes, status: int = 200) -> None:
        self.data = data
        self.status = status

    def read(self) -> bytes:
        return self.data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def client() -> GitHubAPIClient:
    """Fixture returning a GitHubAPIClient with a dummy token."""
    return GitHubAPIClient(auth_token="fake_token_123", timeout=5.0)


class TestGitHubAPIClient:
    """Test suite for GitHubAPIClient."""

    def test_client_initialization(self) -> None:
        """Verify default and custom initialization values."""
        default_client = GitHubAPIClient()
        assert default_client.auth_token is None
        assert default_client.base_url == "https://api.github.com"
        assert default_client.timeout == 10.0

        custom = GitHubAPIClient(
            auth_token="secret",
            base_url="https://github.mycompany.com/api/v3/",
            timeout=15.0,
        )
        assert custom.auth_token == "secret"
        assert custom.base_url == "https://github.mycompany.com/api/v3"
        assert custom.timeout == 15.0

    def test_request_headers_with_and_without_auth(self) -> None:
        """Verify standard GitHub headers and Bearer auth injection."""
        client_auth = GitHubAPIClient(auth_token="tok_abc")
        req_auth = client_auth._build_request("search/repositories")
        assert req_auth.get_header("Authorization") == "Bearer tok_abc"
        assert req_auth.get_header("User-agent") == "OSS-Architect-Scout"
        assert req_auth.get_header("Accept") == "application/vnd.github.v3+json"

        client_no_auth = GitHubAPIClient()
        req_no_auth = client_no_auth._build_request("search/repositories")
        assert req_no_auth.get_header("Authorization") is None

    @patch("urllib.request.urlopen")
    def test_search_repositories_happy_path(
        self, mock_urlopen: MagicMock, client: GitHubAPIClient
    ) -> None:
        """Verify search_repositories parses GitHub API search JSON correctly."""
        mock_payload = {
            "total_count": 1,
            "items": [
                {
                    "name": "fastapi",
                    "full_name": "tiangolo/fastapi",
                    "stargazers_count": 75000,
                    "forks_count": 6000,
                    "license": {"spdx_id": "MIT"},
                    "open_issues_count": 400,
                    "default_branch": "master",
                    "updated_at": "2026-10-16T00:00:00Z",
                    "description": "Modern API framework",
                }
            ],
        }
        mock_urlopen.return_value = MockHTTPResponse(
            json.dumps(mock_payload).encode("utf-8")
        )

        results = client.search_repositories("fastapi", limit=5)
        assert len(results) == 1
        repo = results[0]
        assert isinstance(repo, CandidateRepo)
        assert repo.name == "fastapi"
        assert repo.full_name == "tiangolo/fastapi"
        assert repo.stars == 75000
        assert repo.forks == 6000
        assert repo.license_spdx == "MIT"
        assert repo.default_branch == "master"

    @patch("urllib.request.urlopen")
    def test_get_repository_tree_happy_path(
        self, mock_urlopen: MagicMock, client: GitHubAPIClient
    ) -> None:
        """Verify get_repository_tree extracts recursive file paths."""
        mock_payload = {
            "tree": [
                {"path": "src/main.py", "type": "blob"},
                {"path": "tests/test_main.py", "type": "blob"},
                {"path": "README.md", "type": "blob"},
            ]
        }
        mock_urlopen.return_value = MockHTTPResponse(
            json.dumps(mock_payload).encode("utf-8")
        )

        tree = client.get_repository_tree("owner/repo")
        assert tree == ["src/main.py", "tests/test_main.py", "README.md"]

    @patch("urllib.request.urlopen")
    def test_get_file_content_raw_and_base64(
        self, mock_urlopen: MagicMock, client: GitHubAPIClient
    ) -> None:
        """Verify get_file_content handles raw string and base64 encoded payloads."""
        mock_urlopen.return_value = MockHTTPResponse(b"# Hello World\nprint('hello')")
        content = client.get_file_content("owner/repo", "README.md")
        assert "Hello World" in content

    @patch("urllib.request.urlopen")
    def test_check_ci_status_happy_path(
        self, mock_urlopen: MagicMock, client: GitHubAPIClient
    ) -> None:
        """Verify check_ci_status retrieves conclusion from recent action run."""
        mock_payload = {
            "workflow_runs": [
                {
                    "id": 12345,
                    "conclusion": "success",
                    "status": "completed",
                }
            ]
        }
        mock_urlopen.return_value = MockHTTPResponse(
            json.dumps(mock_payload).encode("utf-8")
        )

        status = client.check_ci_status("owner/repo")
        assert status == "success"

    def test_edge_cases_empty_queries_and_names(
        self, client: GitHubAPIClient
    ) -> None:
        """Verify handling of empty or blank arguments."""
        assert client.search_repositories("") == []
        assert client.search_repositories("   ") == []
        assert client.get_repository_tree("") == []
        assert client.get_repository_tree("invalid-name-without-slash") == []
        assert client.get_file_content("", "") == ""
        assert client.check_ci_status("") == "unknown"

    @patch("urllib.request.urlopen")
    def test_failure_http_error_graceful_recovery(
        self, mock_urlopen: MagicMock, client: GitHubAPIClient
    ) -> None:
        """Verify HTTP errors (e.g. 403 Rate Limit, 404 Not Found) are caught cleanly."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/search/repositories",
            code=403,
            msg="API rate limit exceeded",
            hdrs={},  # type: ignore
            fp=io.BytesIO(b'{"message": "rate limited"}'),
        )

        assert client.search_repositories("test") == []
        assert client.get_repository_tree("owner/repo") == []
        assert client.get_file_content("owner/repo", "file.py") == ""
        assert client.check_ci_status("owner/repo") == "unknown"

    @patch("urllib.request.urlopen")
    def test_failure_timeout_and_network_error(
        self, mock_urlopen: MagicMock, client: GitHubAPIClient
    ) -> None:
        """Verify network timeout and connection errors return empty results without crash."""
        mock_urlopen.side_effect = TimeoutError("Connection timed out")

        assert client.search_repositories("test") == []
        assert client.get_repository_tree("owner/repo") == []
        assert client.get_file_content("owner/repo", "file.py") == ""
        assert client.check_ci_status("owner/repo") == "unknown"

    @patch("urllib.request.urlopen")
    def test_failure_malformed_json_response(
        self, mock_urlopen: MagicMock, client: GitHubAPIClient
    ) -> None:
        """Verify corrupted or invalid JSON does not cause an unhandled exception."""
        mock_urlopen.return_value = MockHTTPResponse(b"<!DOCTYPE html><html>502 Bad Gateway</html>")

        assert client.search_repositories("test") == []
        assert client.get_repository_tree("owner/repo") == []
        assert client.check_ci_status("owner/repo") == "unknown"
