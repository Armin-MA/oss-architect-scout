# TASK-026: Implement MarkdownPresenter for UI

## 1. Scope & Single Responsibility
- **Target File Path:** `src/ui/markdown_presenter.py`
- **Action Type:** Implement Visual Presenter Class
- **Responsibility:** Render single-turn visual markdown report with shields badges, comparison table, Mermaid flowchart, and details.
- **GitHub Issue:** #26
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `src.contracts.i_ui_presenter.IUIPresenter`
- **Allowed Imports:** `typing, List[EvaluationScore], src.contracts.i_ui_presenter.IUIPresenter, src.utils.visual_formatter`
- **Forbidden Imports:** `database, mechanics`

## 3. Technical Contract
- **Input Parameters:** scores: List[EvaluationScore], host_profile: HostProfile
- **Deterministic Output:** Formatted markdown report string
- **Error Handling:** Handle empty list gracefully

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/ui/test_markdown_presenter.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(ui): implement markdown_presenter.py [TASK-026] (Closes #26)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
