# TASK-028: Implement ScoutOrchestrator in Core

## 1. Scope & Single Responsibility
- **Target File Path:** `src/core/scout_orchestrator.py`
- **Action Type:** Implement Orchestrator Class
- **Responsibility:** Orchestrate end-to-end workflow: Host profiling -> GitHub search -> 3-stage funnel -> Scoring -> Persistence -> Presentation.
- **GitHub Issue:** #28
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Application Service)`
- **Allowed Imports:** `typing, src.contracts, src.entities, src.mechanics`
- **Forbidden Imports:** `database drivers, terminal/UI libraries`

## 3. Technical Contract
- **Input Parameters:** query: str, project_path: str, allow_copyleft: bool
- **Deterministic Output:** Formatted markdown report and candidate scores
- **Error Handling:** Propagate domain errors cleanly

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/core/test_scout_orchestrator.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(core): implement scout_orchestrator.py [TASK-028] (Closes #28)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
