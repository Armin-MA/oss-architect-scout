# Product Requirements Document (PRD): OSS Architect Scout

**Project Name:** `oss-architect-scout`  
**Version:** `1.0.0`  
**Governing Skill:** `interactive-architect-gatekeeper`  
**Target Environment:** Antigravity / Cursor / Claude Code / Codex  

---

## 1. Executive Summary & Core Mission
`oss-architect-scout` is an intelligent, high-speed open-source repository evaluation, ranking, and architectural adaptation engine. When starting or expanding a software project, instead of reinventing existing components, the system searches GitHub, executes a multi-stage pruning funnel, evaluates candidate repositories across 5 rigorous engineering dimensions, filters out security and licensing risks via an absolute veto gate, and wraps selected components to blend seamlessly into the host project's architectural contracts.

---

## 2. Ubiquitous Language & Domain Glossary
* **Candidate Repository:** A public open-source Git repository retrieved from GitHub matching target technical keywords.
* **Hard Veto Gate (دروازه وتوی مطلق):** A non-negotiable binary filter eliminating repositories with viral copyleft licenses (e.g. AGPL/GPL when commercial use is required) or active Critical/High CVEs prior to any scoring.
* **Architecture Contract (قرارداد معماری میزبان):** The explicit structural conventions of the host repository (such as Layered Architecture, DTO boundaries, repository encapsulation, and pure business mechanics).
* **Code Malleability Index (شاخص چکش‌خواری کد):** The structural elasticity of a candidate repository's codebase; measures how easily its core mechanics can be decoupled, refactored, and blended into the host architecture with minimal friction.
* **Blending & Camouflage Engine (موتور همرنگ‌سازی):** The pipeline responsible for sanitizing banned libraries, wrapping inputs/outputs in DTOs, and establishing swappable module boundaries.
* **Zero-Sycophancy Protocol (پروتکل نفی تملق):** The engineering standard requiring the assistant to provide honest, data-driven technical pushback and consequence forecasting rather than passively agreeing with suboptimal operator decisions.
* **Tri-State Intent Model:** Classification of operator directives into:
  1. *Preference with Mitigation:* Operator prefers a tool but welcomes hardening and isolation.
  2. *Strong Pushback:* Operator pushes strongly, triggering a compromise bridge proposal.
  3. *Raw Definitive Directive:* Operator strictly demands raw integration, requiring explicit risk acknowledgement.
* **High-Threshold Warning Trigger:** Restricting blocking prompts and warnings strictly to catastrophic risks (security/license) to maintain developer velocity without nuisance.

---

## 3. System Scope & Boundaries

### 3.1 In-Scope
1. **Dynamic Architecture & Rule Profiling (Stage 0):** Automated scanning of the host project's active skills (e.g. `Architect`), directory conventions, linter/tsconfig files, and project rule documents (`.cursorrules`, `rules/`, `specs/`).
2. **3-Stage Pruning Funnel:**
   * *Stage 1 (Metadata & Veto Gate):* Rapid filtering via GitHub API metadata (stars, license, update recency, archived status) in < 2s.
   * *Stage 2 (Heuristics & Health):* Deterministic inspection of CI build status, test suite presence, issue resolution velocity, and dependency trees in < 5s.
   * *Stage 3 (Deep Code & Malleability Inspection):* Structural analysis of core mechanics and contract compatibility on top 3 finalists in < 10s.
3. **5-Factor Balanced Scoring Matrix (from 100):**
   * *Factor 1:* Architectural Standardization & Malleability (25%)
   * *Factor 2:* Code Cleanliness & Test Coverage (25%)
   * *Factor 3:* Community Health & Issue Resolution Velocity (25%)
   * *Factor 4:* Popularity, Adoption & Stars (15%)
   * *Factor 5:* Dependency Hygiene & Secondary Compliance (10%)
4. **Dual-Level Reporting:** Clear executive breakdown combining senior technical rationale with concise, intuitive analogies for rapid vibe-coding decisions.
5. **Architectural Standardization Pipeline:** Automated packaging of approved code into atomic, decoupled modules (`src/modules/[name]`) with explicit DTOs and repository abstraction.

### 3.2 Out-of-Scope
* Scraping or analyzing closed-source or private proprietary software.
* Automatically publishing modified modules to public registries (npm, PyPI) without explicit developer consent.
* Attempting real-time penetration testing or zero-day discovery on candidate repositories.

---

## 4. Architectural Invariants
1. **Zero Premature Code:** No operational application code is created before DoD Gate 3 sign-off and explicit `START_IMPLEMENTATION`.
2. **Deterministic Quality Verification:** Cleanliness and health scores must be grounded in observable artifacts (e.g., test directories, GitHub Actions statuses, type checking configs) rather than unanchored LLM hallucination.
3. **Hard Veto Invariance:** A repository failing the license compatibility or critical CVE gate receives an automatic score of `0` and is completely excluded from recommendations.
4. **Operator Sovereignty:** The human operator retains final authority over selections once risks have been explicitly acknowledged.
5. **Atomic Isolation:** Any code imported from an external repository must reside behind an abstract contract interface and never directly bind to host persistence or framework drivers.

---

## 5. Non-Functional Requirements & Performance Targets
* **End-to-End Evaluation Latency:** $\le 20\text{ seconds}$ for balanced mode.
* **Token Efficiency:** Multi-stage pruning must reduce raw context ingestion by at least $80\%$ compared to naive full-repo ingestion.
* **Zero Friction UX:** Standard evaluation presented in a single, visually structured message without circular back-and-forth prompts.
