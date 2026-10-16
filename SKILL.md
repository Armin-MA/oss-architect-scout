---
name: oss-architect-scout
description: Automated open-source repository evaluation, ranking, and architectural adaptation engine. Discovers GitHub projects, executes a 3-stage pruning funnel, evaluates candidates across 5 engineering dimensions, enforces hard veto gates, and generates modular adapter scaffolds.
---

# OSS Architect Scout (`oss-architect-scout`)

An autonomous open-source repository evaluation, ranking, and architectural adaptation engine designed for Antigravity, Cursor, Claude Code, and Codex.

## Core Capabilities
1. **Host Architecture Profiler:** Dynamically scans the host repository's active skills (e.g. `Architect`), directory conventions (`src/modules`, `contracts`), and rule files (`.cursorrules`, `rules/`) to construct a `HostProfile`.
2. **3-Stage Pruning Funnel:**
   - **Stage 1 (Metadata & Veto Gate):** Rapid filtering via GitHub API metadata (stars, license, update recency) in < 2s.
   - **Stage 2 (Heuristics & CI):** Deterministic inspection of CI build status, test directory presence, issue resolution velocity, and dependency trees in < 5s.
   - **Stage 3 (Deep Code & Malleability Inspection):** Structural analysis of core mechanics and contract compatibility on top finalists in < 10s.
3. **5-Factor Balanced Scoring Matrix (from 100):**
   - **Architectural Standardization & Malleability:** 25%
   - **Code Cleanliness & Test Coverage:** 25%
   - **Community Health & Issue Resolution:** 25%
   - **Popularity & Trust:** 15%
   - **Dependency Hygiene & Compliance:** 10%
4. **Hard Veto Gate:** Immediate binary elimination of candidates with viral copyleft licenses (AGPL/GPL when commercial use is required) or critical vulnerabilities.
5. **Zero-Sycophancy & Tri-State Intent Handling:** Objective, data-driven technical pushback and consequence forecasting without blindly rubber-stamping bad choices.
6. **Zero Friction UX:** Concise single-turn visual markdown reports with Shields.io badges, Mermaid integration flowcharts, comparison matrix tables, and collapsible details.
7. **Automated Blending & Adapter Scaffolding:** Generates clean DTO and interface adapter templates for shortlisted code.

## Quick CLI Usage

```bash
# Basic evaluation of open-source projects for an auth module
python -m src.ui.cli_controller --query "authentication jwt oauth2" --path "."

# Allow copyleft licenses (e.g. for non-commercial projects)
python -m src.ui.cli_controller --query "fast vector search" --allow-copyleft

# View historical evaluation runs from MySQL repository
python -m src.ui.cli_controller --history --limit 10
```

## Running the Test Suite

```bash
python -m pytest -v
```
All 306 unit tests strictly enforce layered architecture isolation and deterministic purity.
