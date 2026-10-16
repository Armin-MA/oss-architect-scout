# OSS Architect Scout 🚀

[![CI](https://img.shields.io/badge/tests-306%20passed-brightgreen)](https://github.com/Armin-MA/oss-architect-scout)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Architecture: Layered](https://img.shields.io/badge/architecture-layered-blueviolet)](https://github.com/Armin-MA/oss-architect-scout/blob/main/specs/ARCHITECTURE.md)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)

An automated open-source repository evaluation, ranking, and architectural adaptation engine for AI-assisted software development environments (Antigravity, Cursor, Claude Code, Codex).

---

## 🏗️ Architecture Blueprint

Strictly governed by the `interactive-architect-gatekeeper` layered architecture contract:

```text
src/
├── contracts/     # Pure abstract interfaces/protocols (ZERO runtime execution logic)
├── config/        # Immutable settings and environment constants
├── core/          # Inversion of Control (IoC) container & scout orchestrator
├── entities/      # Pure domain models (CandidateRepo, HostProfile, EvaluationScore, VetoResult)
├── mechanics/     # Deterministic business algorithms (One file, one logical action)
├── database/      # Total MySQL isolation (models, DTOs, parameterized queries, repository)
├── ui/            # Presenter markdown formatting & CLI presentation entrypoint
└── utils/         # Cross-cutting utilities (GitHub REST API client, visual formatter, license classifier)
```

---

## ⚡ The 5-Factor Scoring Model

1. **Architectural Standardization & Malleability (25%):** Structural elasticity, modularity, and friction of wrapping into host architecture.
2. **Code Cleanliness & Test Coverage (25%):** CI status, test suite presence, strict typing, and linter configurations.
3. **Community Health & Activity (25%):** Issue velocity, resolution rate, and commit recency.
4. **Popularity & Trust (15%):** Normalized star and fork velocity.
5. **Dependency Hygiene & Compliance (10%):** Dependency tree lightness and license nuance.

*Note: Hard Veto Gate permanently eliminates repos with viral copyleft licenses or critical CVEs before scoring.*

---

## 🧪 Verification

Run the full test suite with pytest:

```bash
python -m pytest -v
```

**Status:** 306/306 tests passing (100% pass rate).
