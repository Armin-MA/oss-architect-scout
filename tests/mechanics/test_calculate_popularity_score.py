"""Unit tests for calculate_popularity_score pure mechanics."""
import pytest

from src.mechanics.calculate_popularity_score import calculate_popularity_score


class TestCalculatePopularityScore:
    """Test suite for calculate_popularity_score."""

    def test_happy_path_standard_repository(self):
        """Verify standard popularity calculation with logarithmic scaling."""
        score = calculate_popularity_score(stars=1000, forks=100)
        assert isinstance(score, float)
        assert 50.0 <= score <= 65.0

    def test_happy_path_top_tier_adoption(self):
        """Verify massive projects reach maximum score 100.0."""
        score = calculate_popularity_score(stars=100000, forks=10000)
        assert score == 100.0

    def test_edge_case_zero_stars(self):
        """Verify zero stars results in score 0.0 regardless of forks."""
        assert calculate_popularity_score(stars=0, forks=0) == 0.0
        assert calculate_popularity_score(stars=0, forks=500) == 0.0

    def test_edge_case_single_star_zero_forks(self):
        """Verify log10(1) = 0 produces score 0.0."""
        assert calculate_popularity_score(stars=1, forks=0) == 0.0

    def test_edge_case_overflow_clamping(self):
        """Verify scores beyond benchmark are clamped to 100.0."""
        assert calculate_popularity_score(stars=500000, forks=100000) == 100.0

    def test_failure_negative_stars(self):
        """Verify ValueError is raised on negative stars."""
        with pytest.raises(ValueError, match="stars cannot be negative"):
            calculate_popularity_score(stars=-1, forks=10)

    def test_failure_negative_forks(self):
        """Verify ValueError is raised on negative forks."""
        with pytest.raises(ValueError, match="forks cannot be negative"):
            calculate_popularity_score(stars=100, forks=-5)

    @pytest.mark.parametrize("invalid_val", ["100", 12.5, None, True, False])
    def test_failure_invalid_types_stars(self, invalid_val):
        """Verify ValueError is raised on non-integer stars."""
        with pytest.raises(ValueError, match="stars must be a non-negative integer"):
            calculate_popularity_score(stars=invalid_val, forks=10)  # type: ignore

    @pytest.mark.parametrize("invalid_val", ["50", 5.5, None, True, False])
    def test_failure_invalid_types_forks(self, invalid_val):
        """Verify ValueError is raised on non-integer forks."""
        with pytest.raises(ValueError, match="forks must be a non-negative integer"):
            calculate_popularity_score(stars=100, forks=invalid_val)  # type: ignore
