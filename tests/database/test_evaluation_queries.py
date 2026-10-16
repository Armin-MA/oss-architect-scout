"""Unit tests for EvaluationQueries (TASK-024)."""

import pytest

from src.database.queries.evaluation_queries import (
    CREATE_CANDIDATE_EVALUATIONS_TABLE_SQL,
    CREATE_SCOUT_RUNS_TABLE_SQL,
    CREATE_TABLES_SQL,
    INSERT_CANDIDATE_SQL,
    INSERT_EVAL_SQL,
    INSERT_RUN_SQL,
    SELECT_EVALUATIONS_BY_RUN_ID_SQL,
    SELECT_HISTORY_SQL,
    SELECT_RUN_BY_ID_SQL,
    TABLE_CREATION_STATEMENTS,
)


def test_happy_path_constants_exist_and_non_empty() -> None:
    """Verify expected deterministic SQL statement constants exist and are non-empty."""
    assert isinstance(CREATE_TABLES_SQL, str) and len(CREATE_TABLES_SQL.strip()) > 0
    assert isinstance(CREATE_SCOUT_RUNS_TABLE_SQL, str) and len(CREATE_SCOUT_RUNS_TABLE_SQL.strip()) > 0
    assert isinstance(CREATE_CANDIDATE_EVALUATIONS_TABLE_SQL, str) and len(CREATE_CANDIDATE_EVALUATIONS_TABLE_SQL.strip()) > 0
    assert isinstance(INSERT_RUN_SQL, str) and len(INSERT_RUN_SQL.strip()) > 0
    assert isinstance(INSERT_CANDIDATE_SQL, str) and len(INSERT_CANDIDATE_SQL.strip()) > 0
    assert isinstance(INSERT_EVAL_SQL, str) and len(INSERT_EVAL_SQL.strip()) > 0
    assert isinstance(SELECT_HISTORY_SQL, str) and len(SELECT_HISTORY_SQL.strip()) > 0
    assert isinstance(SELECT_RUN_BY_ID_SQL, str) and len(SELECT_RUN_BY_ID_SQL.strip()) > 0
    assert isinstance(SELECT_EVALUATIONS_BY_RUN_ID_SQL, str) and len(SELECT_EVALUATIONS_BY_RUN_ID_SQL.strip()) > 0


def test_happy_path_table_creation_statements() -> None:
    """Verify table creation statements have required engines, encodings, and constraints."""
    assert len(TABLE_CREATION_STATEMENTS) == 2
    runs_ddl, evals_ddl = TABLE_CREATION_STATEMENTS

    assert "scout_runs" in runs_ddl
    assert "ENGINE=InnoDB" in runs_ddl
    assert "utf8mb4" in runs_ddl

    assert "candidate_evaluations" in evals_ddl
    assert "FOREIGN KEY (run_id) REFERENCES scout_runs(id) ON DELETE CASCADE" in evals_ddl
    assert "ENGINE=InnoDB" in evals_ddl
    assert "utf8mb4" in evals_ddl


def test_happy_path_insert_statements_placeholders() -> None:
    """Verify parameterized placeholder count for run and candidate insertions."""
    # INSERT_RUN_SQL inserts: id, query, host_architecture, total_candidates, finalists_count
    assert INSERT_RUN_SQL.count("%s") == 5
    assert "scout_runs" in INSERT_RUN_SQL

    # INSERT_CANDIDATE_SQL inserts 14 fields
    assert INSERT_CANDIDATE_SQL.count("%s") == 14
    assert "candidate_evaluations" in INSERT_CANDIDATE_SQL
    assert INSERT_EVAL_SQL == INSERT_CANDIDATE_SQL


def test_happy_path_select_statements() -> None:
    """Verify select queries utilize correct column projections and ordering."""
    assert "SELECT run_id, repo_full_name, stars, license_type, final_score, created_at" in SELECT_HISTORY_SQL
    assert "ORDER BY created_at DESC" in SELECT_HISTORY_SQL
    assert "LIMIT %s" in SELECT_HISTORY_SQL

    assert "WHERE id = %s" in SELECT_RUN_BY_ID_SQL
    assert "WHERE run_id = %s" in SELECT_EVALUATIONS_BY_RUN_ID_SQL


def test_edge_case_placeholder_syntax_consistency() -> None:
    """Verify that only standard MySQL %s parameter placeholders are used (no raw '?' or ':name')."""
    for query in (
        INSERT_RUN_SQL,
        INSERT_CANDIDATE_SQL,
        SELECT_HISTORY_SQL,
        SELECT_RUN_BY_ID_SQL,
        SELECT_EVALUATIONS_BY_RUN_ID_SQL,
    ):
        assert "?" not in query, f"Unexpected SQLite/JDBC placeholder '?' in {query}"
        assert ":id" not in query, f"Unexpected named placeholder in {query}"
        assert "%s" in query, f"Expected MySQL placeholder '%s' in {query}"


def test_failure_state_immutable_constants() -> None:
    """Verify pure SQL constants cannot be mutated or confused with non-string types."""
    import src.database.queries.evaluation_queries as eq

    with pytest.raises(TypeError):
        eq.INSERT_RUN_SQL[0] = "X"  # Strings in Python are immutable
