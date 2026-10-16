"""Unit tests for EvaluationScore domain entity."""

import pytest
from src.entities.candidate_repo import CandidateRepo
from src.entities.evaluation_score import EvaluationScore


@pytest.fixture
def sample_repo() -> CandidateRepo:
    """Fixture returning a valid CandidateRepo."""
    return CandidateRepo(
        name="test-lib",
        full_name="test-org/test-lib",
        stars=1200,
        forks=150,
        license_spdx="MIT",
    )


class TestEvaluationScore:
    """Test suite for EvaluationScore."""

    def test_happy_path_instantiation(self, sample_repo: CandidateRepo) -> None:
        """Verify successful instantiation with valid scores and attributes."""
        eval_score = EvaluationScore(
            repo=sample_repo,
            architecture_score=85.5,
            cleanliness_score=90.0,
            community_score=78.0,
            popularity_score=82.5,
            hygiene_score=95.0,
            final_score=85.2,
            strengths=["Clean architecture", "100% test coverage"],
            weaknesses=["High issue count"],
            vibe_analogy="A Swiss army knife with aerospace-grade durability",
        )
        assert eval_score.repo == sample_repo
        assert eval_score.architecture_score == 85.5
        assert eval_score.cleanliness_score == 90.0
        assert eval_score.community_score == 78.0
        assert eval_score.popularity_score == 82.5
        assert eval_score.hygiene_score == 95.0
        assert eval_score.final_score == 85.2
        assert len(eval_score.strengths) == 2
        assert len(eval_score.weaknesses) == 1
        assert "Swiss army knife" in eval_score.vibe_analogy

    def test_boundary_scores(self, sample_repo: CandidateRepo) -> None:
        """Verify exact boundary values 0.0 and 100.0 are accepted."""
        score_min = EvaluationScore(
            repo=sample_repo,
            architecture_score=0.0,
            cleanliness_score=0.0,
            community_score=0.0,
            popularity_score=0.0,
            hygiene_score=0.0,
            final_score=0.0,
        )
        assert score_min.final_score == 0.0
        assert score_min.strengths == []
        assert score_min.weaknesses == []
        assert score_min.vibe_analogy == ""

        score_max = EvaluationScore(
            repo=sample_repo,
            architecture_score=100.0,
            cleanliness_score=100.0,
            community_score=100.0,
            popularity_score=100.0,
            hygiene_score=100.0,
            final_score=100.0,
            strengths=None,  # type: ignore
            weaknesses=None,  # type: ignore
            vibe_analogy=None,  # type: ignore
        )
        assert score_max.final_score == 100.0
        assert score_max.strengths == []
        assert score_max.weaknesses == []
        assert score_max.vibe_analogy == ""

    def test_failure_invalid_repo(self) -> None:
        """Verify ValueError when repo is None or invalid type."""
        with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
            EvaluationScore(
                repo=None,  # type: ignore
                architecture_score=80.0,
                cleanliness_score=80.0,
                community_score=80.0,
                popularity_score=80.0,
                hygiene_score=80.0,
                final_score=80.0,
            )

    @pytest.mark.parametrize(
        "score_field,invalid_val",
        [
            ("architecture_score", -0.1),
            ("cleanliness_score", 100.1),
            ("community_score", -10.0),
            ("popularity_score", 150.0),
            ("hygiene_score", "ninety"),
            ("final_score", True),
        ],
    )
    def test_failure_out_of_range_or_type_scores(
        self, sample_repo: CandidateRepo, score_field: str, invalid_val
    ) -> None:
        """Verify ValueError is raised when any score is out of [0.0, 100.0] or non-numeric."""
        kwargs = {
            "repo": sample_repo,
            "architecture_score": 50.0,
            "cleanliness_score": 50.0,
            "community_score": 50.0,
            "popularity_score": 50.0,
            "hygiene_score": 50.0,
            "final_score": 50.0,
        }
        kwargs[score_field] = invalid_val
        with pytest.raises(ValueError):
            EvaluationScore(**kwargs)
