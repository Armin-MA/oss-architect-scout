"""Unit tests for CandidateRepo domain entity."""

from dataclasses import FrozenInstanceError
import pytest
from src.entities.candidate_repo import CandidateRepo


class TestCandidateRepo:
    """Test suite for CandidateRepo."""

    def test_happy_path_instantiation(self) -> None:
        """Verify successful instantiation with valid attributes."""
        repo = CandidateRepo(
            name="fastapi",
            full_name="tiangolo/fastapi",
            stars=75000,
            forks=6200,
            license_spdx="MIT",
            open_issues=450,
            default_branch="master",
            updated_at="2026-10-16T12:00:00Z",
            description="FastAPI framework, high performance",
        )
        assert repo.name == "fastapi"
        assert repo.full_name == "tiangolo/fastapi"
        assert repo.stars == 75000
        assert repo.forks == 6200
        assert repo.license_spdx == "MIT"
        assert repo.open_issues == 450
        assert repo.default_branch == "master"
        assert repo.updated_at == "2026-10-16T12:00:00Z"
        assert repo.description == "FastAPI framework, high performance"

    def test_defaults_and_edge_cases(self) -> None:
        """Verify boundary conditions: zero metrics, None description/license, extreme star count."""
        repo = CandidateRepo(
            name="min-repo",
            full_name="org/min-repo",
            stars=0,
            forks=0,
            license_spdx=None,
            open_issues=0,
            default_branch="main",
            updated_at="",
            description=None,
        )
        assert repo.stars == 0
        assert repo.forks == 0
        assert repo.license_spdx is None
        assert repo.open_issues == 0
        assert repo.default_branch == "main"
        assert repo.description is None

        mega_repo = CandidateRepo(
            name="linux",
            full_name="torvalds/linux",
            stars=2000000,
            forks=500000,
        )
        assert mega_repo.stars == 2000000

    def test_immutability(self) -> None:
        """Verify CandidateRepo is frozen and prevents field mutation."""
        repo = CandidateRepo(
            name="immutable-lib",
            full_name="owner/immutable-lib",
            stars=10,
        )
        with pytest.raises(FrozenInstanceError):
            repo.stars = 20  # type: ignore

    @pytest.mark.parametrize(
        "invalid_name",
        ["", "   ", None],
    )
    def test_failure_empty_name(self, invalid_name) -> None:
        """Verify ValueError is raised on empty or whitespace name."""
        with pytest.raises(ValueError, match="Repository name cannot be empty"):
            CandidateRepo(name=invalid_name, full_name="org/repo")

    @pytest.mark.parametrize(
        "invalid_full_name",
        ["", "   ", None],
    )
    def test_failure_empty_full_name(self, invalid_full_name) -> None:
        """Verify ValueError is raised on empty or whitespace full_name."""
        with pytest.raises(ValueError, match="Repository full_name cannot be empty"):
            CandidateRepo(name="repo", full_name=invalid_full_name)

    def test_failure_negative_stars(self) -> None:
        """Verify ValueError is raised when stars count is negative."""
        with pytest.raises(ValueError, match="stars cannot be negative"):
            CandidateRepo(name="repo", full_name="org/repo", stars=-1)

    def test_failure_negative_forks(self) -> None:
        """Verify ValueError is raised when forks count is negative."""
        with pytest.raises(ValueError, match="forks cannot be negative"):
            CandidateRepo(name="repo", full_name="org/repo", forks=-5)

    def test_failure_negative_open_issues(self) -> None:
        """Verify ValueError is raised when open_issues count is negative."""
        with pytest.raises(ValueError, match="open_issues cannot be negative"):
            CandidateRepo(name="repo", full_name="org/repo", open_issues=-10)

    @pytest.mark.parametrize(
        "invalid_branch",
        ["", "   "],
    )
    def test_failure_empty_default_branch(self, invalid_branch) -> None:
        """Verify ValueError is raised when default_branch is empty."""
        with pytest.raises(ValueError, match="default_branch cannot be empty"):
            CandidateRepo(name="repo", full_name="org/repo", default_branch=invalid_branch)
