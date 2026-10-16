# TASK-004: Define IPruningFunnel abstract contract

## 1. Scope & Single Responsibility
- **Target File Path:** `src/contracts/i_pruning_funnel.py`
- **Action Type:** Define Abstract Interface
- **Responsibility:** Declare contract for 3-stage pruning funnel operations.
- **GitHub Issue:** #4
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `abc.ABC`
- **Allowed Imports:** `abc, typing, src.entities.candidate_repo.CandidateRepo, src.entities.host_profile.HostProfile`
- **Forbidden Imports:** `mechanics, database, ui`

## 3. Technical Contract
- **Input Parameters:** List of CandidateRepo entities and HostProfile
- **Deterministic Output:** Pruned List of CandidateRepo entities
- **Error Handling:** Pure protocol

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/contracts/test_i_pruning_funnel.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(contracts): implement i_pruning_funnel.py [TASK-004] (Closes #4)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
