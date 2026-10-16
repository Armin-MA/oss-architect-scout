# Work Breakdown Structure (WBS): OSS Architect Scout

**Project Name:** `oss-architect-scout`  
**Governing Skill:** `interactive-architect-gatekeeper`  
**Milestone:** Milestone 4: Core Implementation & Testing  
**Total Development Units:** 29 Atomic Tasks  

---

## 1. Layer-by-Layer Task Breakdown

### Layer 1: Configuration & Abstract Contracts (`src/config/`, `src/contracts/`)
* [ ] [TASK-001](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-001.md): `src/config/settings.py` (Closes [#1](https://github.com/Armin-MA/oss-architect-scout/issues/1))
* [ ] [TASK-002](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-002.md): `src/contracts/i_github_client.py` (Closes [#2](https://github.com/Armin-MA/oss-architect-scout/issues/2))
* [ ] [TASK-003](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-003.md): `src/contracts/i_architecture_profiler.py` (Closes [#3](https://github.com/Armin-MA/oss-architect-scout/issues/3))
* [ ] [TASK-004](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-004.md): `src/contracts/i_pruning_funnel.py` (Closes [#4](https://github.com/Armin-MA/oss-architect-scout/issues/4))
* [ ] [TASK-005](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-005.md): `src/contracts/i_scoring_engine.py` (Closes [#5](https://github.com/Armin-MA/oss-architect-scout/issues/5))
* [ ] [TASK-006](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-006.md): `src/contracts/i_scout_repository.py` (Closes [#6](https://github.com/Armin-MA/oss-architect-scout/issues/6))
* [ ] [TASK-007](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-007.md): `src/contracts/i_ui_presenter.py` (Closes [#7](https://github.com/Armin-MA/oss-architect-scout/issues/7))

### Layer 2: Pure Domain Entities & Utilities (`src/entities/`, `src/utils/`)
* [ ] [TASK-008](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-008.md): `src/entities/candidate_repo.py` (Closes [#8](https://github.com/Armin-MA/oss-architect-scout/issues/8))
* [ ] [TASK-009](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-009.md): `src/entities/host_profile.py` (Closes [#9](https://github.com/Armin-MA/oss-architect-scout/issues/9))
* [ ] [TASK-010](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-010.md): `src/entities/evaluation_score.py` (Closes [#10](https://github.com/Armin-MA/oss-architect-scout/issues/10))
* [ ] [TASK-011](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-011.md): `src/entities/veto_result.py` (Closes [#11](https://github.com/Armin-MA/oss-architect-scout/issues/11))
* [ ] [TASK-012](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-012.md): `src/utils/license_classifier.py` (Closes [#12](https://github.com/Armin-MA/oss-architect-scout/issues/12))
* [ ] [TASK-013](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-013.md): `src/utils/github_api_client.py` (Closes [#13](https://github.com/Armin-MA/oss-architect-scout/issues/13))
* [ ] [TASK-014](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-014.md): `src/utils/visual_formatter.py` (Closes [#14](https://github.com/Armin-MA/oss-architect-scout/issues/14))

### Layer 3: Pure Business Mechanics (`src/mechanics/`)
* [ ] [TASK-015](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-015.md): `src/mechanics/filter_veto_gate.py` (Closes [#15](https://github.com/Armin-MA/oss-architect-scout/issues/15))
* [ ] [TASK-016](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-016.md): `src/mechanics/calculate_community_score.py` (Closes [#16](https://github.com/Armin-MA/oss-architect-scout/issues/16))
* [ ] [TASK-017](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-017.md): `src/mechanics/calculate_code_cleanliness_score.py` (Closes [#17](https://github.com/Armin-MA/oss-architect-scout/issues/17))
* [ ] [TASK-018](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-018.md): `src/mechanics/calculate_popularity_score.py` (Closes [#18](https://github.com/Armin-MA/oss-architect-scout/issues/18))
* [ ] [TASK-019](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-019.md): `src/mechanics/calculate_malleability_score.py` (Closes [#19](https://github.com/Armin-MA/oss-architect-scout/issues/19))
* [ ] [TASK-020](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-020.md): `src/mechanics/calculate_final_score.py` (Closes [#20](https://github.com/Armin-MA/oss-architect-scout/issues/20))
* [ ] [TASK-021](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-021.md): `src/mechanics/detect_project_architecture.py` (Closes [#21](https://github.com/Armin-MA/oss-architect-scout/issues/21))
* [ ] [TASK-022](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-022.md): `src/mechanics/generate_adapter_scaffold.py` (Closes [#22](https://github.com/Armin-MA/oss-architect-scout/issues/22))

### Layer 4: MySQL Database Isolation (`src/database/`)
* [ ] [TASK-023](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-023.md): `src/database/dto/evaluation_record_dto.py` (Closes [#23](https://github.com/Armin-MA/oss-architect-scout/issues/23))
* [ ] [TASK-024](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-024.md): `src/database/queries/evaluation_queries.py` (Closes [#24](https://github.com/Armin-MA/oss-architect-scout/issues/24))
* [ ] [TASK-025](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-025.md): `src/database/repositories/mysql_scout_repository.py` (Closes [#25](https://github.com/Armin-MA/oss-architect-scout/issues/25))

### Layer 5: Presentation & Core Application (`src/ui/`, `src/core/`)
* [ ] [TASK-026](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-026.md): `src/ui/markdown_presenter.py` (Closes [#26](https://github.com/Armin-MA/oss-architect-scout/issues/26))
* [ ] [TASK-027](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-027.md): `src/core/container.py` (Closes [#27](https://github.com/Armin-MA/oss-architect-scout/issues/27))
* [ ] [TASK-028](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-028.md): `src/core/scout_orchestrator.py` (Closes [#28](https://github.com/Armin-MA/oss-architect-scout/issues/28))
* [ ] [TASK-029](file:///D:/small%20projects%20antigraviti/oss-architect-scout/tasks/TASK-029.md): `src/ui/cli_controller.py` (Closes [#29](https://github.com/Armin-MA/oss-architect-scout/issues/29))

---

## 2. Execution Discipline & Progression Rules
1. **One File, One Logical Action:** Each task corresponds strictly to one file path and one unit test file path.
2. **Atomic Commits:** Each task must be committed individually with conventional format:
   ```text
   feat([layer]): implement [filename] [TASK-XXX] (Closes #[IssueNumber])
   ```
3. **Rollback on Test Failure:** If unit tests fail, dirty changes must be rolled back (`git checkout -- .`) and diagnosed cleanly.
