# TASK-014: Implement VisualFormatter utility

## 1. Scope & Single Responsibility
- **Target File Path:** `src/utils/visual_formatter.py`
- **Action Type:** Implement String Formatting Functions
- **Responsibility:** Generate Shields.io Markdown badge strings and ASCII progress bars (e.g. ████████░░ 80%).
- **GitHub Issue:** #14
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Utility)`
- **Allowed Imports:** `typing`
- **Forbidden Imports:** `contracts, database, ui`

## 3. Technical Contract
- **Input Parameters:** label: str, value: str/float, color: str
- **Deterministic Output:** Formatted badge or progress bar string
- **Error Handling:** Clamp score percentage to [0, 100]

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/utils/test_visual_formatter.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(utils): implement visual_formatter.py [TASK-014] (Closes #14)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
