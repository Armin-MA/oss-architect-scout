"""Unit tests for src/contracts/i_scoring_engine.py."""
import pytest
from typing import Any
from src.contracts.i_scoring_engine import IScoringEngine


class DummyScoringEngine(IScoringEngine):
    """Concrete implementation of IScoringEngine for testing."""

    def score_candidate(self, repo: Any, host: Any) -> Any:
        return {
            "repo": repo,
            "architecture_score": 85.0,
            "cleanliness_score": 90.0,
            "community_score": 75.0,
            "popularity_score": 80.0,
            "hygiene_score": 95.0,
            "final_score": 84.5,
        }


class IncompleteScoringEngine(IScoringEngine):
    """Subclass without implementing score_candidate."""
    pass


def test_i_scoring_engine_happy_path():
    """Verify concrete subclass successfully scores candidates."""
    engine = DummyScoringEngine()
    assert isinstance(engine, IScoringEngine)

    result = engine.score_candidate({"name": "fastapi"}, {"architecture_type": "layered"})
    assert result["final_score"] == 84.5
    assert result["cleanliness_score"] == 90.0


def test_i_scoring_engine_edge_cases():
    """Verify boundary handling for null/empty candidate."""
    engine = DummyScoringEngine()
    result = engine.score_candidate({}, {})
    assert result is not None
    assert "final_score" in result


def test_i_scoring_engine_failure_states():
    """Verify abstract class cannot be instantiated directly or without implementation."""
    with pytest.raises(TypeError):
        IScoringEngine()  # type: ignore

    with pytest.raises(TypeError):
        IncompleteScoringEngine()  # type: ignore
