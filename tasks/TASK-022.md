# TASK-022: Implement generate_adapter_scaffold pure mechanics

## 1. Scope & Single Responsibility
- **Target File Path:** `src/mechanics/generate_adapter_scaffold.py`
- **Action Type:** Implement Pure Code Generator Function
- **Responsibility:** Generate Python DTO and interface adapter code templates for the shortlisted repository.
- **GitHub Issue:** #22
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `None (Pure Function)`
- **Allowed Imports:** `typing, src.entities.candidate_repo.CandidateRepo, src.entities.host_profile.HostProfile`
- **Forbidden Imports:** `database, ui, disk I/O`

## 3. Technical Contract
- **Input Parameters:** repo: CandidateRepo, host: HostProfile, module_name: str
- **Deterministic Output:** Dict[str, str] mapping relative file path to scaffolded code string
- **Error Handling:** Deterministic string generation

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/mechanics/test_generate_adapter_scaffold.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(mechanics): implement generate_adapter_scaffold.py [TASK-022] (Closes #22)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
