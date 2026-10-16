# TASK-016: Implement calculate_community_score pure mechanics

## 1. Scope & Single Responsibility
- **Target File Path:** `src/mechanics/calculate_community_score.py`
- **Action Type:** Implement Pure Calculation Function
- **Responsibility:** Compute community health score (0-100) based on issue resolution velocity and commit recency.
- **GitHub Issue:** #16
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Pure Function)`
- **Allowed Imports:** `typing, datetime, src.entities.candidate_repo.CandidateRepo`
- **Forbidden Imports:** `database, ui, network drivers`

## 3. Technical Contract
- **Input Parameters:** repo: CandidateRepo, reference_date: datetime.datetime
- **Deterministic Output:** float score between 0.0 and 100.0
- **Error Handling:** Return 0.0 if abandoned (> 1 year without commit)

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/mechanics/test_calculate_community_score.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(mechanics): implement calculate_community_score.py [TASK-016] (Closes #16)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
