# TASK-021: Implement detect_project_architecture pure mechanics

## 1. Scope & Single Responsibility
- **Target File Path:** `src/mechanics/detect_project_architecture.py`
- **Action Type:** Implement Pure Scanner Function
- **Responsibility:** Scan project directory paths and file indicators to construct a HostProfile.
- **GitHub Issue:** #21
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Pure Function)`
- **Allowed Imports:** `typing, List[str], src.entities.host_profile.HostProfile`
- **Forbidden Imports:** `database, ui, network`

## 3. Technical Contract
- **Input Parameters:** existing_file_paths: List[str]
- **Deterministic Output:** HostProfile entity
- **Error Handling:** Fallback to standard modular architecture if unmapped

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/mechanics/test_detect_project_architecture.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(mechanics): implement detect_project_architecture.py [TASK-021] (Closes #21)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
