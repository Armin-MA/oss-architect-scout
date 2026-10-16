"""Unit tests for src/contracts/i_scout_repository.py."""
import pytest
from typing import Any, List
from src.contracts.i_scout_repository import IScoutRepository


class DummyScoutRepository(IScoutRepository):
    """Concrete implementation of IScoutRepository for testing."""

    def __init__(self):
        self.records: List[Any] = []

    def save_evaluation_run(self, run: Any) -> str:
        run_id = "run-12345"
        self.records.append(run)
        return run_id

    def get_evaluation_history(self, limit: int = 10) -> List[Any]:
        if limit <= 0:
            return []
        return self.records[:limit]


class IncompleteScoutRepository(IScoutRepository):
    """Subclass without implementing required abstract methods."""

    def save_evaluation_run(self, run: Any) -> str:
        return "run-id"


def test_i_scout_repository_happy_path():
    """Verify concrete subclass successfully saves run and retrieves history."""
    repo = DummyScoutRepository()
    assert isinstance(repo, IScoutRepository)

    run_id = repo.save_evaluation_run({"query": "fastapi", "candidates": 3})
    assert run_id == "run-12345"

    history = repo.get_evaluation_history(limit=5)
    assert len(history) == 1


def test_i_scout_repository_edge_cases():
    """Verify boundary handling for zero limit and empty database."""
    repo = DummyScoutRepository()
    assert repo.get_evaluation_history(limit=0) == []
    assert repo.get_evaluation_history(limit=-1) == []


def test_i_scout_repository_failure_states():
    """Verify abstract class cannot be instantiated directly or with missing methods."""
    with pytest.raises(TypeError):
        IScoutRepository()  # type: ignore

    with pytest.raises(TypeError):
        IncompleteScoutRepository()  # type: ignore
