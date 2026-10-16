# TASK-020: Implement calculate_final_score pure mechanics

## 1. Scope & Single Responsibility
- **Target File Path:** `src/mechanics/calculate_final_score.py`
- **Action Type:** Implement Pure Calculation Function
- **Responsibility:** Calculate weighted aggregate score from the 5 dimensions.
- **GitHub Issue:** #20
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Pure Function)`
- **Allowed Imports:** `typing, Dict[str, float]`
- **Forbidden Imports:** `database, ui`

## 3. Technical Contract
- **Input Parameters:** sub_scores: Dict[str, float], weights: Dict[str, float]
- **Deterministic Output:** float final_score rounded to 2 decimal places
- **Error Handling:** Raise ValueError if weights do not sum to 1.0 or 100.0

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/mechanics/test_calculate_final_score.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(mechanics): implement calculate_final_score.py [TASK-020] (Closes #20)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
