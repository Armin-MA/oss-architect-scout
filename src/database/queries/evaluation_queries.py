"""Parameterized SQL queries and DDL for MySQL database isolation."""

from typing import Tuple

CREATE_SCOUT_RUNS_TABLE_SQL: str = """
CREATE TABLE IF NOT EXISTS scout_runs (
    id VARCHAR(36) PRIMARY KEY,
    query VARCHAR(255) NOT NULL,
    host_architecture VARCHAR(100) NOT NULL,
    total_candidates INT NOT NULL,
    finalists_count INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_scout_query (query),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""".strip()

CREATE_CANDIDATE_EVALUATIONS_TABLE_SQL: str = """
CREATE TABLE IF NOT EXISTS candidate_evaluations (
    id VARCHAR(36) PRIMARY KEY,
    run_id VARCHAR(36) NOT NULL,
    repo_full_name VARCHAR(150) NOT NULL,
    stars INT NOT NULL,
    license_type VARCHAR(50) NOT NULL,
    veto_passed BOOLEAN NOT NULL,
    community_score DECIMAL(5,2) NOT NULL,
    cleanliness_score DECIMAL(5,2) NOT NULL,
    architecture_score DECIMAL(5,2) NOT NULL,
    popularity_score DECIMAL(5,2) NOT NULL,
    hygiene_score DECIMAL(5,2) NOT NULL,
    final_score DECIMAL(5,2) NOT NULL,
    strengths TEXT,
    weaknesses TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES scout_runs(id) ON DELETE CASCADE,
    INDEX idx_repo_score (repo_full_name, final_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""".strip()

TABLE_CREATION_STATEMENTS: Tuple[str, str] = (
    CREATE_SCOUT_RUNS_TABLE_SQL,
    CREATE_CANDIDATE_EVALUATIONS_TABLE_SQL,
)

CREATE_TABLES_SQL: str = f"{CREATE_SCOUT_RUNS_TABLE_SQL}\n\n{CREATE_CANDIDATE_EVALUATIONS_TABLE_SQL}"

INSERT_RUN_SQL: str = """
INSERT INTO scout_runs (id, query, host_architecture, total_candidates, finalists_count)
VALUES (%s, %s, %s, %s, %s);
""".strip()

INSERT_CANDIDATE_SQL: str = """
INSERT INTO candidate_evaluations (
    id, run_id, repo_full_name, stars, license_type, veto_passed,
    community_score, cleanliness_score, architecture_score,
    popularity_score, hygiene_score, final_score, strengths, weaknesses
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""".strip()

# Alias for compatibility with task spec
INSERT_EVAL_SQL: str = INSERT_CANDIDATE_SQL

SELECT_HISTORY_SQL: str = """
SELECT run_id, repo_full_name, stars, license_type, final_score, created_at
FROM candidate_evaluations
ORDER BY created_at DESC
LIMIT %s;
""".strip()

SELECT_RUN_BY_ID_SQL: str = """
SELECT id, query, host_architecture, total_candidates, finalists_count, created_at
FROM scout_runs
WHERE id = %s;
""".strip()

SELECT_EVALUATIONS_BY_RUN_ID_SQL: str = """
SELECT run_id, repo_full_name, stars, license_type, final_score, created_at
FROM candidate_evaluations
WHERE run_id = %s
ORDER BY final_score DESC;
""".strip()
