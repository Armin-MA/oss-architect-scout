# TASK-015: Implement filter_veto_gate pure mechanics

## 1. Scope & Single Responsibility
- **Target File Path:** `src/mechanics/filter_veto_gate.py`
- **Action Type:** Implement Pure Validation Function
- **Responsibility:** Validate candidate repository against hard veto constraints (viral license, critical CVEs).
- **GitHub Issue:** #15
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Pure Function)`
- **Allowed Imports:** `typing, src.entities.candidate_repo.CandidateRepo, src.entities.veto_result.VetoResult, src.utils.license_classifier.classify_license`
- **Forbidden Imports:** `database, ui, os, sys`

## 3. Technical Contract
- **Input Parameters:** repo: CandidateRepo, allow_copyleft: bool = False
- **Deterministic Output:** VetoResult (passed=True/False with explanation)
- **Error Handling:** Deterministic boolean result

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/mechanics/test_filter_veto_gate.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(mechanics): implement filter_veto_gate.py [TASK-015] (Closes #15)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
