"""MySQL repository implementation for persisting scout runs and candidate evaluations."""

import uuid
from typing import Any, Callable, Dict, List, Optional, Union

try:
    from src.contracts.i_scout_repository import IScoutRepository
except ImportError:
    from abc import ABC, abstractmethod

    class IScoutRepository(ABC):  # type: ignore
        """Fallback interface for IScoutRepository."""

        @abstractmethod
        def save_evaluation_run(self, run: Any) -> str:
            """Persist evaluation run and return its unique identifier."""
            pass

        @abstractmethod
        def get_evaluation_history(self, limit: int = 10) -> List[Any]:
            """Retrieve history of evaluated repositories."""
            pass

from src.database.dto.evaluation_record_dto import EvaluationRecordDTO
from src.database.queries.evaluation_queries import (
    INSERT_CANDIDATE_SQL,
    INSERT_RUN_SQL,
    SELECT_HISTORY_SQL,
    TABLE_CREATION_STATEMENTS,
)


class RepositoryError(Exception):
    """Base exception for database repository operations."""
    pass


class DatabaseConnectionError(RepositoryError):
    """Raised when connecting to the database fails."""
    pass


class DatabaseQueryError(RepositoryError):
    """Raised when a database query execution fails."""
    pass


class MySQLScoutRepository(IScoutRepository):
    """MySQL implementation of IScoutRepository.

    Encapsulates all database interactions, parameterized SQL statements,
    and connection management without leaking drivers outside this layer.
    """

    def __init__(
        self,
        db_connection_params: Optional[Dict[str, Any]] = None,
        connection: Optional[Any] = None,
        connection_factory: Optional[Callable[[], Any]] = None,
    ) -> None:
        """Initialize repository with connection parameters, direct connection, or factory.

        Args:
            db_connection_params: Dictionary of connection parameters (host, user, etc.).
            connection: Pre-configured mock or live database connection.
            connection_factory: Callable returning an active database connection.
        """
        self._db_params = db_connection_params
        self._connection = connection
        self._connection_factory = connection_factory

    def _get_connection(self) -> Any:
        """Retrieve or create an active database connection."""
        if self._connection is not None:
            return self._connection

        if self._connection_factory is not None:
            try:
                self._connection = self._connection_factory()
                return self._connection
            except Exception as exc:
                raise DatabaseConnectionError(
                    f"Failed to create connection via factory: {exc}"
                ) from exc

        if self._db_params is not None:
            try:
                import pymysql

                self._connection = pymysql.connect(**self._db_params)
                return self._connection
            except Exception as exc:
                raise DatabaseConnectionError(
                    f"Failed to connect to MySQL database: {exc}"
                ) from exc

        raise DatabaseConnectionError(
            "Cannot connect: No database connection, factory, or parameters configured."
        )

    def create_tables(self) -> None:
        """Execute DDL statements to ensure required tables and indexes exist."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                for statement in TABLE_CREATION_STATEMENTS:
                    cursor.execute(statement)
                conn.commit()
            finally:
                cursor.close()
        except DatabaseConnectionError:
            raise
        except Exception as exc:
            raise DatabaseQueryError(f"Failed to create database tables: {exc}") from exc

    def save_evaluation_run(self, run: Any) -> str:
        """Persist a scout evaluation run and its candidate evaluations.

        Args:
            run: ScoutRun entity, dict, or object containing run details and evaluations.

        Returns:
            The persistent run ID string.

        Raises:
            ValueError: If run data is missing or invalid.
            DatabaseConnectionError: If connection to database cannot be established.
            DatabaseQueryError: If query execution or transaction fails.
        """
        if run is None:
            raise ValueError("Evaluation run data cannot be None")

        # Extract run header attributes
        run_id = (
            getattr(run, "id", None)
            or getattr(run, "run_id", None)
            or (run.get("id") if isinstance(run, dict) else None)
            or (run.get("run_id") if isinstance(run, dict) else None)
            or str(uuid.uuid4())
        )

        query = (
            getattr(run, "query", None)
            or (run.get("query") if isinstance(run, dict) else "")
            or ""
        )

        host_architecture = (
            getattr(run, "host_architecture", None)
            or (run.get("host_architecture") if isinstance(run, dict) else "unknown")
            or "unknown"
        )

        total_candidates = (
            getattr(run, "total_candidates", None)
            if getattr(run, "total_candidates", None) is not None
            else (run.get("total_candidates", 0) if isinstance(run, dict) else 0)
        )

        finalists = (
            getattr(run, "finalists", None)
            or getattr(run, "evaluations", None)
            or (run.get("finalists") if isinstance(run, dict) else None)
            or (run.get("evaluations") if isinstance(run, dict) else None)
            or []
        )

        finalists_count = (
            getattr(run, "finalists_count", None)
            if getattr(run, "finalists_count", None) is not None
            else (
                run.get("finalists_count")
                if isinstance(run, dict) and "finalists_count" in run
                else len(finalists)
            )
        )

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Insert run record
            cursor.execute(
                INSERT_RUN_SQL,
                (run_id, query, host_architecture, int(total_candidates), int(finalists_count)),
            )

            # Insert individual candidate evaluations
            for item in finalists:
                eval_id = (
                    getattr(item, "id", None)
                    or (item.get("id") if isinstance(item, dict) else None)
                    or str(uuid.uuid4())
                )

                repo = (
                    getattr(item, "repo", None)
                    or (item.get("repo") if isinstance(item, dict) else None)
                )

                repo_full_name = (
                    getattr(item, "repo_full_name", None)
                    or (item.get("repo_full_name") if isinstance(item, dict) else None)
                )
                if not repo_full_name and repo:
                    repo_full_name = (
                        getattr(repo, "full_name", None)
                        or (repo.get("full_name") if isinstance(repo, dict) else str(repo))
                    )
                repo_full_name = repo_full_name or "unknown/repo"

                stars = (
                    getattr(item, "stars", None)
                    or (getattr(repo, "stars", None) if repo else None)
                    or (item.get("stars") if isinstance(item, dict) else None)
                    or 0
                )

                license_type = (
                    getattr(item, "license_type", None)
                    or (getattr(repo, "license", None) if repo else None)
                    or (getattr(repo, "license_type", None) if repo else None)
                    or (item.get("license_type") if isinstance(item, dict) else None)
                    or "Unknown"
                )

                veto_passed = (
                    getattr(item, "veto_passed", True)
                    if not isinstance(item, dict)
                    else item.get("veto_passed", True)
                )

                community_score = float(
                    getattr(item, "community_score", None)
                    or (item.get("community_score") if isinstance(item, dict) else 0.0)
                    or 0.0
                )
                cleanliness_score = float(
                    getattr(item, "cleanliness_score", None)
                    or (item.get("cleanliness_score") if isinstance(item, dict) else 0.0)
                    or 0.0
                )
                architecture_score = float(
                    getattr(item, "architecture_score", None)
                    or (item.get("architecture_score") if isinstance(item, dict) else 0.0)
                    or 0.0
                )
                popularity_score = float(
                    getattr(item, "popularity_score", None)
                    or (item.get("popularity_score") if isinstance(item, dict) else 0.0)
                    or 0.0
                )
                hygiene_score = float(
                    getattr(item, "hygiene_score", None)
                    or (item.get("hygiene_score") if isinstance(item, dict) else 0.0)
                    or 0.0
                )
                final_score = float(
                    getattr(item, "final_score", None)
                    or (item.get("final_score") if isinstance(item, dict) else 0.0)
                    or 0.0
                )

                raw_strengths = (
                    getattr(item, "strengths", None)
                    or (item.get("strengths") if isinstance(item, dict) else None)
                    or []
                )
                strengths_str = (
                    ", ".join(raw_strengths)
                    if isinstance(raw_strengths, list)
                    else str(raw_strengths)
                )

                raw_weaknesses = (
                    getattr(item, "weaknesses", None)
                    or (item.get("weaknesses") if isinstance(item, dict) else None)
                    or []
                )
                weaknesses_str = (
                    ", ".join(raw_weaknesses)
                    if isinstance(raw_weaknesses, list)
                    else str(raw_weaknesses)
                )

                cursor.execute(
                    INSERT_CANDIDATE_SQL,
                    (
                        eval_id,
                        run_id,
                        str(repo_full_name),
                        int(stars),
                        str(license_type),
                        bool(veto_passed),
                        community_score,
                        cleanliness_score,
                        architecture_score,
                        popularity_score,
                        hygiene_score,
                        final_score,
                        strengths_str,
                        weaknesses_str,
                    ),
                )

            if hasattr(conn, "commit"):
                conn.commit()

            return run_id
        except DatabaseConnectionError:
            raise
        except Exception as exc:
            if hasattr(conn, "rollback"):
                try:
                    conn.rollback()
                except Exception:
                    pass
            raise DatabaseQueryError(f"Failed to persist evaluation run: {exc}") from exc
        finally:
            cursor.close()

    def get_evaluation_history(self, limit: int = 10) -> List[EvaluationRecordDTO]:
        """Retrieve recent evaluation records ordered by creation date descending.

        Args:
            limit: Maximum number of records to retrieve (must be positive integer).

        Returns:
            List of EvaluationRecordDTO instances.

        Raises:
            ValueError: If limit is invalid (non-positive or not an integer).
            DatabaseConnectionError: If connection cannot be established.
            DatabaseQueryError: If query execution fails.
        """
        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            raise ValueError("limit must be a positive integer")

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(SELECT_HISTORY_SQL, (limit,))
            rows = cursor.fetchall()
            records: List[EvaluationRecordDTO] = []

            for row in rows:
                if isinstance(row, dict):
                    records.append(
                        EvaluationRecordDTO(
                            run_id=row["run_id"],
                            repo_full_name=row["repo_full_name"],
                            stars=int(row["stars"]),
                            license_type=str(row["license_type"]),
                            final_score=float(row["final_score"]),
                            created_at=row.get("created_at"),
                        )
                    )
                else:
                    # Tuple/sequence row: (run_id, repo_full_name, stars, license_type, final_score, created_at)
                    records.append(
                        EvaluationRecordDTO(
                            run_id=row[0],
                            repo_full_name=row[1],
                            stars=int(row[2]),
                            license_type=str(row[3]),
                            final_score=float(row[4]),
                            created_at=row[5] if len(row) > 5 else None,
                        )
                    )

            return records
        except DatabaseConnectionError:
            raise
        except Exception as exc:
            raise DatabaseQueryError(
                f"Failed to retrieve evaluation history: {exc}"
            ) from exc
        finally:
            cursor.close()

    def close(self) -> None:
        """Close connection if active."""
        if self._connection is not None and hasattr(self._connection, "close"):
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None

    def __enter__(self) -> "MySQLScoutRepository":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager and close connection."""
        self.close()
