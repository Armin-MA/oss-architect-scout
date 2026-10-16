# TASK-024: Define Parameterized EvaluationQueries for MySQL

## 1. Scope & Single Responsibility
- **Target File Path:** `src/database/queries/evaluation_queries.py`
- **Action Type:** Define Parameterized SQL Statements
- **Responsibility:** Store raw, prepared, and parameterized SQL statements for MySQL isolation.
- **GitHub Issue:** #24
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (SQL Constants)`
- **Allowed Imports:** `typing`
- **Forbidden Imports:** `mechanics, ui`

## 3. Technical Contract
- **Input Parameters:** None
- **Deterministic Output:** Constants CREATE_TABLES_SQL, INSERT_RUN_SQL, INSERT_EVAL_SQL, SELECT_HISTORY_SQL
- **Error Handling:** Pure SQL strings

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/database/test_evaluation_queries.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(database): implement evaluation_queries.py [TASK-024] (Closes #24)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
