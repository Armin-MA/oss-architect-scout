"""Unit tests for src/contracts/i_pruning_funnel.py."""
import pytest
from typing import Any, List
from src.contracts.i_pruning_funnel import IPruningFunnel
from src.contracts.i_github_client import IGitHubClient


class DummyFunnel(IPruningFunnel):
    """Concrete implementation of IPruningFunnel for testing."""

    def prune_stage1_metadata(self, repos: List[Any]) -> List[Any]:
        return [r for r in repos if r.get("stars", 0) > 10]

    def prune_stage2_heuristics(self, repos: List[Any], client: IGitHubClient) -> List[Any]:
        return repos[:3]

    def prune_stage3_deep(self, repos: List[Any], host: Any) -> List[Any]:
        return repos[:1]


class IncompleteFunnel(IPruningFunnel):
    """Subclass that misses some abstract methods."""

    def prune_stage1_metadata(self, repos: List[Any]) -> List[Any]:
        return repos


class MockGitHubClient(IGitHubClient):
    """Dummy client for passing into stage 2."""

    def search_repositories(self, query: str, limit: int = 50) -> List[Any]:
        return []

    def get_repository_tree(self, full_name: str) -> List[str]:
        return []

    def get_file_content(self, full_name: str, path: str) -> str:
        return ""

    def check_ci_status(self, full_name: str) -> str:
        return "SUCCESS"


def test_i_pruning_funnel_happy_path():
    """Verify concrete subclass successfully executes all three pruning stages."""
    funnel = DummyFunnel()
    client = MockGitHubClient()
    assert isinstance(funnel, IPruningFunnel)

    sample_repos = [
        {"name": "repo1", "stars": 5},
        {"name": "repo2", "stars": 50},
        {"name": "repo3", "stars": 100},
        {"name": "repo4", "stars": 200},
    ]

    s1 = funnel.prune_stage1_metadata(sample_repos)
    assert len(s1) == 3

    s2 = funnel.prune_stage2_heuristics(s1, client)
    assert len(s2) == 3

    s3 = funnel.prune_stage3_deep(s2, host={"architecture_type": "layered"})
    assert len(s3) == 1


def test_i_pruning_funnel_edge_cases():
    """Verify boundary condition handling for empty repository lists."""
    funnel = DummyFunnel()
    client = MockGitHubClient()

    assert funnel.prune_stage1_metadata([]) == []
    assert funnel.prune_stage2_heuristics([], client) == []
    assert funnel.prune_stage3_deep([], host=None) == []


def test_i_pruning_funnel_failure_states():
    """Verify abstract class cannot be instantiated directly or with missing methods."""
    with pytest.raises(TypeError):
        IPruningFunnel()  # type: ignore

    with pytest.raises(TypeError):
        IncompleteFunnel()  # type: ignore
