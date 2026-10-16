"""Unit tests for MySQLScoutRepository (TASK-025)."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, call
import pytest

from src.database.dto.evaluation_record_dto import EvaluationRecordDTO
from src.database.queries.evaluation_queries import (
    INSERT_CANDIDATE_SQL,
    INSERT_RUN_SQL,
    SELECT_HISTORY_SQL,
    TABLE_CREATION_STATEMENTS,
)
from src.database.repositories.mysql_scout_repository import (
    DatabaseConnectionError,
    DatabaseQueryError,
    MySQLScoutRepository,
    RepositoryError,
)


@pytest.fixture
def mock_db():
    """Create a mock database connection and cursor."""
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


def test_happy_path_save_evaluation_run_dict(mock_db) -> None:
    """Verify persisting evaluation run from dictionary data."""
    conn, cursor = mock_db
    repo = MySQLScoutRepository(connection=conn)

    run_data = {
        "id": "run-001",
        "query": "jwt authentication",
        "host_architecture": "Layered",
        "total_candidates": 45,
        "finalists": [
            {
                "id": "eval-001",
                "repo_full_name": "authlib/authlib",
                "stars": 4200,
                "license_type": "BSD-3-Clause",
                "veto_passed": True,
                "community_score": 85.0,
                "cleanliness_score": 90.0,
                "architecture_score": 88.0,
                "popularity_score": 75.0,
                "hygiene_score": 80.0,
                "final_score": 85.5,
                "strengths": ["Well documented", "Active maintainers"],
                "weaknesses": ["Complex API"],
            }
        ],
    }

    result_run_id = repo.save_evaluation_run(run_data)

    assert result_run_id == "run-001"
    conn.commit.assert_called_once()
    cursor.close.assert_called_once()

    # Check cursor.execute calls
    calls = cursor.execute.call_args_list
    assert len(calls) == 2

    # Check scout_runs insert
    run_call = calls[0]
    assert run_call[0][0] == INSERT_RUN_SQL
    assert run_call[0][1] == ("run-001", "jwt authentication", "Layered", 45, 1)

    # Check candidate_evaluations insert
    cand_call = calls[1]
    assert cand_call[0][0] == INSERT_CANDIDATE_SQL
    params = cand_call[0][1]
    assert params[0] == "eval-001"
    assert params[1] == "run-001"
    assert params[2] == "authlib/authlib"
    assert params[3] == 4200
    assert params[4] == "BSD-3-Clause"
    assert params[5] is True
    assert params[11] == 85.5
    assert "Well documented" in params[12]
    assert "Complex API" in params[13]


def test_happy_path_save_evaluation_run_object(mock_db) -> None:
    """Verify persisting evaluation run from duck-typed object/entity."""
    conn, cursor = mock_db
    repo = MySQLScoutRepository(connection=conn)

    class DummyEvaluation:
        id = "eval-obj-1"
        repo_full_name = "tiangolo/sqlmodel"
        stars = 12000
        license_type = "MIT"
        veto_passed = True
        community_score = 92.0
        cleanliness_score = 94.0
        architecture_score = 91.0
        popularity_score = 88.0
        hygiene_score = 89.0
        final_score = 91.5
        strengths = ["FastAPI integration"]
        weaknesses = []

    class DummyRun:
        id = "run-obj-100"
        query = "orm layer"
        host_architecture = "Clean Architecture"
        total_candidates = 10
        finalists = [DummyEvaluation()]

    run_id = repo.save_evaluation_run(DummyRun())
    assert run_id == "run-obj-100"
    conn.commit.assert_called_once()


def test_happy_path_get_evaluation_history(mock_db) -> None:
    """Verify retrieving evaluation history as EvaluationRecordDTO list."""
    conn, cursor = mock_db
    repo = MySQLScoutRepository(connection=conn)

    created_at = datetime(2026, 10, 16, 21, 0, 0, tzinfo=timezone.utc)
    # Cursor returns rows as tuples: (run_id, repo_full_name, stars, license_type, final_score, created_at)
    cursor.fetchall.return_value = [
        ("run-1", "fastapi/fastapi", 75000, "MIT", 95.0, created_at),
        ("run-2", "encode/starlette", 10000, "BSD-3-Clause", 88.5, created_at),
    ]

    records = repo.get_evaluation_history(limit=5)

    cursor.execute.assert_called_once_with(SELECT_HISTORY_SQL, (5,))
    cursor.close.assert_called_once()
    assert len(records) == 2
    assert isinstance(records[0], EvaluationRecordDTO)
    assert records[0].run_id == "run-1"
    assert records[0].repo_full_name == "fastapi/fastapi"
    assert records[0].stars == 75000
    assert records[0].license_type == "MIT"
    assert records[0].final_score == 95.0
    assert records[0].created_at == created_at

    assert records[1].run_id == "run-2"
    assert records[1].repo_full_name == "encode/starlette"


def test_happy_path_get_evaluation_history_dict_rows(mock_db) -> None:
    """Verify retrieving history when cursor returns dictionary rows (DictCursor)."""
    conn, cursor = mock_db
    repo = MySQLScoutRepository(connection=conn)

    cursor.fetchall.return_value = [
        {
            "run_id": "run-dict",
            "repo_full_name": "psf/requests",
            "stars": 50000,
            "license_type": "Apache-2.0",
            "final_score": 90.0,
            "created_at": "2026-10-16T21:00:00",
        }
    ]

    records = repo.get_evaluation_history(limit=1)
    assert len(records) == 1
    assert records[0].run_id == "run-dict"
    assert records[0].repo_full_name == "psf/requests"


def test_happy_path_create_tables(mock_db) -> None:
    """Verify create_tables executes all DDL statements and commits."""
    conn, cursor = mock_db
    repo = MySQLScoutRepository(connection=conn)

    repo.create_tables()

    assert cursor.execute.call_count == len(TABLE_CREATION_STATEMENTS)
    for i, statement in enumerate(TABLE_CREATION_STATEMENTS):
        assert cursor.execute.call_args_list[i][0][0] == statement

    conn.commit.assert_called_once()
    cursor.close.assert_called_once()


def test_happy_path_context_manager(mock_db) -> None:
    """Verify context manager calls close on connection."""
    conn, _ = mock_db
    with MySQLScoutRepository(connection=conn) as repo:
        assert repo is not None

    conn.close.assert_called_once()


def test_edge_case_empty_run_evaluations(mock_db) -> None:
    """Verify persisting a run with zero candidates/finalists."""
    conn, cursor = mock_db
    repo = MySQLScoutRepository(connection=conn)

    run_data = {
        "id": "run-empty",
        "query": "non-existent-lib-query",
        "host_architecture": "Hexagonal",
        "total_candidates": 0,
        "finalists": [],
    }

    run_id = repo.save_evaluation_run(run_data)
    assert run_id == "run-empty"
    # Only scout_runs should be inserted
    assert cursor.execute.call_count == 1
    conn.commit.assert_called_once()


def test_edge_case_connection_factory() -> None:
    """Verify repository accepts and calls connection_factory callable."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    factory = MagicMock(return_value=mock_conn)

    repo = MySQLScoutRepository(connection_factory=factory)
    mock_cursor.fetchall.return_value = []
    results = repo.get_evaluation_history(limit=10)

    factory.assert_called_once()
    assert results == []


def test_failure_state_missing_connection_params() -> None:
    """Verify DatabaseConnectionError is raised when no connection or params provided."""
    repo = MySQLScoutRepository()
    with pytest.raises(DatabaseConnectionError, match="Cannot connect: No database connection"):
        repo.get_evaluation_history(limit=5)


def test_failure_state_connection_factory_error() -> None:
    """Verify DatabaseConnectionError is raised when connection factory throws."""
    def broken_factory():
        raise RuntimeError("Network timeout")

    repo = MySQLScoutRepository(connection_factory=broken_factory)
    with pytest.raises(DatabaseConnectionError, match="Failed to create connection via factory"):
        repo.get_evaluation_history(limit=5)


def test_failure_state_save_evaluation_run_none() -> None:
    """Verify ValueError is raised when run data is None."""
    repo = MySQLScoutRepository(connection=MagicMock())
    with pytest.raises(ValueError, match="Evaluation run data cannot be None"):
        repo.save_evaluation_run(None)


@pytest.mark.parametrize("invalid_limit", [0, -1, -100, "10", None, False, True])
def test_failure_state_invalid_limit(invalid_limit, mock_db) -> None:
    """Verify ValueError is raised on non-positive or non-integer limit."""
    conn, _ = mock_db
    repo = MySQLScoutRepository(connection=conn)
    with pytest.raises(ValueError, match="limit must be a positive integer"):
        repo.get_evaluation_history(limit=invalid_limit)  # type: ignore


def test_failure_state_query_error_triggers_rollback(mock_db) -> None:
    """Verify query failure triggers rollback and raises DatabaseQueryError."""
    conn, cursor = mock_db
    cursor.execute.side_effect = RuntimeError("Deadlock encountered")
    repo = MySQLScoutRepository(connection=conn)

    run_data = {
        "id": "run-fail",
        "query": "query",
        "host_architecture": "Clean",
        "total_candidates": 1,
        "finalists": [],
    }

    with pytest.raises(DatabaseQueryError, match="Failed to persist evaluation run"):
        repo.save_evaluation_run(run_data)

    conn.rollback.assert_called_once()
