"""Unit tests for calculate_community_score pure mechanics."""
from datetime import datetime, timezone, timedelta
import pytest

from src.entities.candidate_repo import CandidateRepo
from src.mechanics.calculate_community_score import calculate_community_score


@pytest.fixture
def baseline_date():
    return datetime(2026, 10, 16, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def make_repo():
    def _make(updated_at, stars=500, forks=100, open_issues=10):
        return CandidateRepo(
            name="test-repo",
            full_name="org/test-repo",
            stars=stars,
            forks=forks,
            license_spdx="MIT",
            open_issues=open_issues,
            default_branch="main",
            updated_at=updated_at,
            description="Sample repository",
        )
    return _make


class TestCalculateCommunityScore:
    """Test suite for calculate_community_score."""

    def test_happy_path_fresh_active_repo(self, baseline_date, make_repo):
        """Verify active repo updated today with low issues gets a near-perfect score."""
        updated = baseline_date.isoformat()
        repo = make_repo(updated_at=updated, stars=1000, forks=200, open_issues=0)
        score = calculate_community_score(repo, baseline_date)

        assert isinstance(score, float)
        assert score == 100.0

    def test_happy_path_moderate_activity(self, baseline_date, make_repo):
        """Verify repo updated ~6 months ago gets a moderate score."""
        updated = (baseline_date - timedelta(days=180)).isoformat()
        repo = make_repo(updated_at=updated, stars=1000, forks=200, open_issues=20)
        score = calculate_community_score(repo, baseline_date)

        assert 50.0 <= score <= 90.0

    def test_edge_case_abandoned_over_one_year(self, baseline_date, make_repo):
        """Verify repo not updated for > 365 days receives score 0.0."""
        updated = (baseline_date - timedelta(days=366)).isoformat()
        repo = make_repo(updated_at=updated, stars=50000, forks=10000, open_issues=0)
        score = calculate_community_score(repo, baseline_date)

        assert score == 0.0

    def test_edge_case_boundary_365_days(self, baseline_date, make_repo):
        """Verify repo at exactly 365 days is not abandoned yet."""
        updated = (baseline_date - timedelta(days=365)).isoformat()
        repo = make_repo(updated_at=updated, stars=1000, forks=200, open_issues=0)
        score = calculate_community_score(repo, baseline_date)

        assert score > 0.0

    def test_edge_case_empty_or_malformed_updated_at(self, baseline_date, make_repo):
        """Verify empty or invalid date string returns 0.0."""
        repo_empty = make_repo(updated_at="")
        assert calculate_community_score(repo_empty, baseline_date) == 0.0

        repo_invalid = make_repo(updated_at="not-a-real-date")
        assert calculate_community_score(repo_invalid, baseline_date) == 0.0

    def test_edge_case_naive_and_aware_datetimes(self, make_repo):
        """Verify comparison works seamlessly when one datetime is naive and other aware."""
        naive_baseline = datetime(2026, 10, 16, 12, 0, 0)
        aware_updated = "2026-10-15T12:00:00Z"
        repo = make_repo(updated_at=aware_updated, stars=100, forks=20, open_issues=0)

        score = calculate_community_score(repo, naive_baseline)
        assert score > 90.0

    def test_edge_case_future_date(self, baseline_date, make_repo):
        """Verify future date is clamped to 0 days elapsed."""
        future_updated = (baseline_date + timedelta(days=10)).isoformat()
        repo = make_repo(updated_at=future_updated, stars=500, forks=100, open_issues=0)
        score = calculate_community_score(repo, baseline_date)

        assert score == 100.0

    def test_edge_case_zero_stars_and_forks(self, baseline_date, make_repo):
        """Verify zero engagement repo with 0 issues evaluates correctly."""
        updated = baseline_date.isoformat()
        repo = make_repo(updated_at=updated, stars=0, forks=0, open_issues=0)
        score = calculate_community_score(repo, baseline_date)
        assert score == 100.0

        repo_busy = make_repo(updated_at=updated, stars=0, forks=0, open_issues=20)
        score_busy = calculate_community_score(repo_busy, baseline_date)
        assert score_busy < score

    def test_failure_invalid_repo_type(self, baseline_date):
        """Verify ValueError is raised if repo is not CandidateRepo."""
        with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
            calculate_community_score(None, baseline_date)  # type: ignore

        with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
            calculate_community_score("invalid-repo", baseline_date)  # type: ignore

    def test_failure_invalid_reference_date_type(self, make_repo):
        """Verify ValueError is raised if reference_date is not datetime."""
        repo = make_repo(updated_at="2026-10-15T00:00:00Z")
        with pytest.raises(ValueError, match="reference_date must be an instance of datetime"):
            calculate_community_score(repo, "2026-10-16")  # type: ignore
