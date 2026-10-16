# TASK-018: Implement calculate_popularity_score pure mechanics

## 1. Scope & Single Responsibility
- **Target File Path:** `src/mechanics/calculate_popularity_score.py`
- **Action Type:** Implement Pure Calculation Function
- **Responsibility:** Compute normalized popularity score (0-100) from stars, forks, and watcher ratio.
- **GitHub Issue:** #18
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Pure Function)`
- **Allowed Imports:** `math, typing, src.entities.candidate_repo.CandidateRepo`
- **Forbidden Imports:** `database, ui`

## 3. Technical Contract
- **Input Parameters:** stars: int, forks: int
- **Deterministic Output:** float score between 0.0 and 100.0 (logarithmic scaling)
- **Error Handling:** Zero stars yields minimum score 0.0

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/mechanics/test_calculate_popularity_score.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(mechanics): implement calculate_popularity_score.py [TASK-018] (Closes #18)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
