"""Database isolation layer for MySQL storage and DTO abstractions."""

from src.database.dto.evaluation_record_dto import EvaluationRecordDTO
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
from src.database.repositories.mysql_scout_repository import (
    DatabaseConnectionError,
    DatabaseQueryError,
    MySQLScoutRepository,
    RepositoryError,
)

__all__ = [
    "EvaluationRecordDTO",
    "MySQLScoutRepository",
    "RepositoryError",
    "DatabaseConnectionError",
    "DatabaseQueryError",
    "CREATE_TABLES_SQL",
    "CREATE_SCOUT_RUNS_TABLE_SQL",
    "CREATE_CANDIDATE_EVALUATIONS_TABLE_SQL",
    "TABLE_CREATION_STATEMENTS",
    "INSERT_RUN_SQL",
    "INSERT_CANDIDATE_SQL",
    "INSERT_EVAL_SQL",
    "SELECT_HISTORY_SQL",
    "SELECT_RUN_BY_ID_SQL",
    "SELECT_EVALUATIONS_BY_RUN_ID_SQL",
]
