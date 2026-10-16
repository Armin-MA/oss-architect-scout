"""Unit tests for src/contracts/i_github_client.py."""
import pytest
from typing import List, Any
from src.contracts.i_github_client import IGitHubClient


class DummyGitHubClient(IGitHubClient):
    """Concrete implementation of IGitHubClient for testing."""

    def search_repositories(self, query: str, limit: int = 50) -> List[Any]:
        if limit <= 0:
            return []
        return [{"full_name": f"mock/{query}", "stars": 100}]

    def get_repository_tree(self, full_name: str) -> List[str]:
        if not full_name:
            return []
        return ["README.md", "src/main.py"]

    def get_file_content(self, full_name: str, path: str) -> str:
        return f"# Content of {path} in {full_name}"

    def check_ci_status(self, full_name: str) -> str:
        return "SUCCESS"


class IncompleteGitHubClient(IGitHubClient):
    """Subclass that deliberately misses abstract methods."""

    def search_repositories(self, query: str, limit: int = 50) -> List[Any]:
        return []


def test_i_github_client_happy_path():
    """Verify concrete subclass successfully implements contract methods."""
    client = DummyGitHubClient()
    assert isinstance(client, IGitHubClient)

    repos = client.search_repositories("test-repo", limit=10)
    assert len(repos) == 1
    assert repos[0]["full_name"] == "mock/test-repo"

    tree = client.get_repository_tree("owner/repo")
    assert "src/main.py" in tree

    content = client.get_file_content("owner/repo", "README.md")
    assert "README.md" in content

    ci_status = client.check_ci_status("owner/repo")
    assert ci_status == "SUCCESS"


def test_i_github_client_edge_cases():
    """Verify boundary conditions such as zero limit and empty inputs."""
    client = DummyGitHubClient()

    # Zero limit
    assert client.search_repositories("test-repo", limit=0) == []

    # Empty full_name
    assert client.get_repository_tree("") == []


def test_i_github_client_failure_states():
    """Verify abstract class cannot be instantiated directly or with missing methods."""
    with pytest.raises(TypeError):
        IGitHubClient()  # type: ignore

    with pytest.raises(TypeError):
        IncompleteGitHubClient()  # type: ignore
