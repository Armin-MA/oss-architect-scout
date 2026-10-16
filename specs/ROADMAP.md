# Project Roadmap & System Mind Map: OSS Architect Scout

## 1. System Mind Map

```mermaid
mindmap
  root((oss-architect-scout))
    UI Layer
      Presenter Markdown Engine
      Terminal Score Visualizer
      Badge & Shields Generator
    Business Mechanics
      Discovery Profiler
      3-Stage Pruning Funnel
      Veto Gate Validator
      5-Factor Scoring Calculator
      Malleability Analyzer
      Blending & Packaging Engine
    Contracts & Interfaces
      HostArchitectureContract
      GitHubClientContract
      EvaluationEngineContract
      RepositoryStorageContract
    Domain Entities
      CandidateRepository
      EvaluationScoreCard
      HostProjectProfile
      VetoStatus
    Database & Storage Layer
      EvaluationHistoryModel
      EvaluationHistoryDTO
      EvaluationQueries
      EvaluationRepository
    Cross-Cutting Utils
      GitHubAPIClient
      LicensingTaxonomy
      LoggerFormatter
```

---

## 2. Component Implementation Status

```mermaid
flowchart TD
    classDef done fill:#2ea44f,stroke:#22863a,color:#fff
    classDef active fill:#e36209,stroke:#b04100,color:#fff
    classDef pending fill:#6a737d,stroke:#444d56,color:#fff

    subgraph Phase0["Phase 0: Git & GitHub Setup"]
        P0["Git Init & Remote Connection"]:::done
    end

    subgraph Phase1["Phase 1: PRD & Visual Mind Map"]
        P1["PRD & ROADMAP Creation"]:::done
    end

    subgraph Phase2["Phase 2: Architecture & Contracts"]
        P2["Layered Contracts & Schema Design"]:::done
    end

    subgraph Phase3["Phase 3: WBS & Zero-Context Tasks"]
        P3["Task Breakdown & GitHub Issues Sync"]:::active
    end

    subgraph Phase4["Phase 4: Implementation"]
        T1["Contracts & Config"]:::pending
        T2["Domain Entities & Utils"]:::pending
        T3["Mechanics & Funnel Engine"]:::pending
        T4["Database & Repository Isolation"]:::pending
        T5["UI Presenter & CLI Bootstrap"]:::pending
    end

    Phase0 --> Phase1 --> Phase2 --> Phase3 --> Phase4
```

---

## 3. High-Level Milestone Progress

- [x] **Milestone 0:** Git Initialized & GitHub Remote Connected (`Armin-MA/oss-architect-scout`)
- [x] **Milestone 1:** Scope & PRD Finalized (`specs/PRD.md` & `specs/ROADMAP.md` at Gate 1)
- [x] **Milestone 2:** Architecture & Contracts Locked (`specs/ARCHITECTURE.md` at Gate 2)
- [ ] **Milestone 3:** WBS, Zero-Context Tasks & GitHub Issues Synced (`specs/WBS.md` at Gate 3)
- [ ] **Milestone 4:** Gated Implementation & Verification (`START_IMPLEMENTATION`)
  - [ ] Layer 1: Contracts & Config
  - [ ] Layer 2: Entities & Utils
  - [ ] Layer 3: Pure Mechanics (Funnel & Scoring)
  - [ ] Layer 4: Database & Encapsulation
  - [ ] Layer 5: UI & Presentation
