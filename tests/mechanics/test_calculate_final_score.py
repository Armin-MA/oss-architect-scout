"""Unit tests for calculate_final_score pure mechanics."""
import pytest

from src.mechanics.calculate_final_score import calculate_final_score


class TestCalculateFinalScore:
    """Test suite for calculate_final_score."""

    def test_happy_path_default_weights(self):
        """Verify calculation with default weights across 5 dimensions."""
        sub_scores = {
            "architecture": 80.0,
            "cleanliness": 90.0,
            "community": 70.0,
            "popularity": 60.0,
            "hygiene": 85.0,
        }
        # 80*0.25 (20) + 90*0.25 (22.5) + 70*0.25 (17.5) + 60*0.15 (9.0) + 85*0.10 (8.5) = 77.5
        score = calculate_final_score(sub_scores)
        assert isinstance(score, float)
        assert score == 77.5

    def test_happy_path_suffix_score_keys(self):
        """Verify keys ending with _score are normalized transparently."""
        sub_scores = {
            "architecture_score": 100.0,
            "cleanliness_score": 100.0,
            "community_score": 100.0,
            "popularity_score": 100.0,
            "hygiene_score": 100.0,
        }
        assert calculate_final_score(sub_scores) == 100.0

    def test_happy_path_custom_weights_sum_to_one(self):
        """Verify custom weights summing to 1.0."""
        sub_scores = {"architecture": 90.0, "cleanliness": 70.0}
        weights = {"architecture": 0.6, "cleanliness": 0.4}
        # 90*0.6 (54) + 70*0.4 (28) = 82.0
        assert calculate_final_score(sub_scores, weights) == 82.0

    def test_happy_path_custom_weights_sum_to_hundred(self):
        """Verify custom weights summing to 100.0."""
        sub_scores = {"architecture": 90.0, "cleanliness": 70.0}
        weights = {"architecture": 60.0, "cleanliness": 40.0}
        assert calculate_final_score(sub_scores, weights) == 82.0

    def test_edge_case_missing_dimension_in_sub_scores(self):
        """Verify missing dimension defaults to 0.0 in calculation."""
        sub_scores = {"architecture": 100.0}
        weights = {"architecture": 0.5, "cleanliness": 0.5}
        # 100 * 0.5 + 0 * 0.5 = 50.0
        assert calculate_final_score(sub_scores, weights) == 50.0

    def test_edge_case_all_zeros(self):
        """Verify all zeros results in 0.0."""
        sub_scores = {"architecture": 0.0, "cleanliness": 0.0}
        weights = {"architecture": 0.5, "cleanliness": 0.5}
        assert calculate_final_score(sub_scores, weights) == 0.0

    def test_failure_invalid_weights_sum(self):
        """Verify ValueError is raised if weights do not sum to 1.0 or 100.0."""
        sub_scores = {"architecture": 80.0}
        with pytest.raises(ValueError, match="Weights must sum to 1.0 or 100.0"):
            calculate_final_score(sub_scores, {"architecture": 0.8})

        with pytest.raises(ValueError, match="Weights must sum to 1.0 or 100.0"):
            calculate_final_score(sub_scores, {"architecture": 75.0})

    def test_failure_empty_sub_scores(self):
        """Verify ValueError is raised on empty or None sub_scores."""
        with pytest.raises(ValueError, match="sub_scores must be a non-empty dictionary"):
            calculate_final_score({})

        with pytest.raises(ValueError, match="sub_scores must be a non-empty dictionary"):
            calculate_final_score(None)  # type: ignore

    def test_failure_score_out_of_range(self):
        """Verify ValueError is raised if any score is < 0 or > 100."""
        with pytest.raises(ValueError, match="must be between 0.0 and 100.0"):
            calculate_final_score({"architecture": -5.0})

        with pytest.raises(ValueError, match="must be between 0.0 and 100.0"):
            calculate_final_score({"architecture": 105.0})

    def test_failure_negative_weight(self):
        """Verify ValueError is raised if a weight is negative."""
        with pytest.raises(ValueError, match="cannot be negative"):
            calculate_final_score(
                {"architecture": 50.0, "cleanliness": 50.0},
                {"architecture": 1.2, "cleanliness": -0.2},
            )

    @pytest.mark.parametrize("invalid_val", [True, False, "80", None, [80]])
    def test_failure_invalid_score_types(self, invalid_val):
        """Verify non-numeric score values raise ValueError."""
        with pytest.raises(ValueError, match="must be a numeric value"):
            calculate_final_score({"architecture": invalid_val})  # type: ignore
