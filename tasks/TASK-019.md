# TASK-019: Implement calculate_malleability_score pure mechanics

## 1. Scope & Single Responsibility
- **Target File Path:** `src/mechanics/calculate_malleability_score.py`
- **Action Type:** Implement Pure Calculation Function
- **Responsibility:** Compute architectural malleability and refactoring friction (0-100).
- **GitHub Issue:** #19
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Pure Function)`
- **Allowed Imports:** `typing, List[str], src.entities.host_profile.HostProfile`
- **Forbidden Imports:** `database, ui`

## 3. Technical Contract
- **Input Parameters:** repo_tree_paths: List[str], host_profile: HostProfile
- **Deterministic Output:** float score between 0.0 and 100.0 (high score = easily decoupled and wrapped)
- **Error Handling:** Clamp score between 0.0 and 100.0

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/mechanics/test_calculate_malleability_score.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(mechanics): implement calculate_malleability_score.py [TASK-019] (Closes #19)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
