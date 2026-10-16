# TASK-002: Define IGitHubClient abstract contract

## 1. Scope & Single Responsibility
- **Target File Path:** `src/contracts/i_github_client.py`
- **Action Type:** Define Abstract Interface
- **Responsibility:** Declare contract for interacting with GitHub REST/GraphQL API without implementation logic.
- **GitHub Issue:** #2
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `abc.ABC`
- **Allowed Imports:** `abc, typing, src.entities.candidate_repo.CandidateRepo`
- **Forbidden Imports:** `requests, httpx, mechanics, database, ui`

## 3. Technical Contract
- **Input Parameters:** Query strings, repository full names, file paths
- **Deterministic Output:** List[CandidateRepo], List[str], str
- **Error Handling:** Pure protocol (no runtime execution)

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/contracts/test_i_github_client.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(contracts): implement i_github_client.py [TASK-002] (Closes #2)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
