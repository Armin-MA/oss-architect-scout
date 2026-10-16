# TASK-012: Implement LicenseClassifier utility

## 1. Scope & Single Responsibility
- **Target File Path:** `src/utils/license_classifier.py`
- **Action Type:** Implement Deterministic Classifier Function
- **Responsibility:** Classify SPDX license identifiers into Permissive, Copyleft, Commercial-Restricted, or Unknown.
- **GitHub Issue:** #12
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Utility)`
- **Allowed Imports:** `typing`
- **Forbidden Imports:** `contracts, database, ui`

## 3. Technical Contract
- **Input Parameters:** spdx_id: str
- **Deterministic Output:** classification: str ('PERMISSIVE', 'COPYLEFT_VIRAL', 'COMMERCIAL_RESTRICTED', 'UNKNOWN')
- **Error Handling:** Return 'UNKNOWN' on unmapped or null license identifiers

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/utils/test_license_classifier.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(utils): implement license_classifier.py [TASK-012] (Closes #12)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
