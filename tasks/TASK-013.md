# TASK-013: Implement GitHubAPIClient utility

## 1. Scope & Single Responsibility
- **Target File Path:** `src/utils/github_api_client.py`
- **Action Type:** Implement Network Client Class
- **Responsibility:** Execute HTTP requests against GitHub API with authentication and timeout.
- **GitHub Issue:** #13
- **Milestone:** Phase 4: Core Implementation

## 2. Dependencies & Contracts
- **Interfaces to Implement / Consume:** `src.contracts.i_github_client.IGitHubClient`
- **Allowed Imports:** `urllib.request, json, typing, src.entities.candidate_repo.CandidateRepo`
- **Forbidden Imports:** `mechanics, database, ui`

## 3. Technical Contract
- **Input Parameters:** auth_token: str, base_url: str
- **Deterministic Output:** Structured responses and CandidateRepo lists
- **Error Handling:** Catch HTTP errors and network timeouts cleanly without crash

## 4. Acceptance Criteria & Test Contract
- **Test File Path:** `tests/utils/test_github_api_client.py`
- **Required Test Cases:**
  1. *Happy Path:* Verify expected deterministic behavior with valid input data.
  2. *Edge Case:* Verify proper boundary condition handling (empty, null, or extreme values).
  3. *Failure State:* Verify explicit exception raising or error result on invalid inputs.

## 5. Git & GitHub Progression Contract
- **Atomic Commit Message:** `feat(utils): implement github_api_client.py [TASK-013] (Closes #13)`
- **Verification Rule:** Commit and push occur ONLY after unit test suite passes 100%. If tests fail, rollback uncommitted changes.
