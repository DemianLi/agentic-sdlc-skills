# Trials Index

Research trials that validate the skill system. Each trial targets a specific hypothesis about the pipeline; full artifacts live in the `research` branch under `test_projects/`.

---

| Trial | Date | Project | Skills exercised | Hypothesis | Result |
|-------|------|---------|-----------------|------------|--------|
| [07](TRIAL_07_REPORT.md) | 2026-05-16 | Temperature converter (Python lib) | s1 → s2 → s4 | Three-layer execution model (Role / Workflow / HARD-GATE) produces working code end-to-end | ✅ PASS |
| [08](TRIAL_08_REPORT.md) | 2026-05-16 | String Stats Library | s1 → s2 → s4 | P1–P4 pipeline improvements (TDD discipline, artifact chain) hold under real TDD | ✅ PASS |
| [09](TRIAL_09_REPORT.md) | 2026-05-16 | String Stats Library (audit) | s5 (sast-lint, audit-rules, pr-review) | s5 Code Auditor pipeline can validate a real library with 100% coverage | ✅ PASS |
| [10](TRIAL_10_REPORT.md) | 2026-05-16 | String Stats API (FastAPI) | s6 (test-integration → verify-release) | s6 QA pipeline produces a machine-generated `test-results.json` gate | ✅ PASS |
| [11](TRIAL_11_REPORT.md) | 2026-05-16 | String Stats API (release) | s7 (build-artifact → telemetry) | s7 Release Manager pipeline can build, deploy (dry-run), and capture telemetry | ✅ DONE_WITH_CONCERNS — s7 skills rewritten to fix pipeline order and simulation_mode |
| [12](TRIAL_12_REPORT.md) | 2026-05-16 | String Stats API (cycle 2) | s7 + next_cycle_inputs | trial-11 MEDIUM-priority findings (warmup, SLO-headroom anomaly) are addressable within the skill framework | ✅ PASS |
| [13](TRIAL_13_REPORT.md) | 2026-05-16 | x402 platform (brainstorm) + token-optimizer hook (trace-feature) | s0-brainstorm, s0-trace-feature | Standalone s0 skills produce usable artifacts outside the s1–s7 pipeline | ✅ PASS |
| [14](TRIAL_14_REPORT.md) | 2026-05-16 | mdtoc CLI (Markdown TOC generator) | s1 → s7 (full pipeline) | Full s1→s7 chain health: each stage starts from upstream artifacts without re-querying the user | ✅ DONE_WITH_CONCERNS — HARD-GATE bypass identified as primary finding; led to trial-15 |
| [15](TRIAL_15_REPORT.md) | 2026-05-17 | slugify CLI | s4 → s7 (3 gate transitions) | Sub-agent isolation enforces HARD-GATEs: cold-start agents complete stages from artifact paths alone | ✅ PASS — 3/3 gates held (s2→s3, s3→s4, s6→s7) |
| [16](TRIAL_16_REPORT.md) | 2026-05-17 | changelog-checker CLI | s1 → s7 (full pipeline) | Gate language robustness: 4 bypass rationalizations (G1–G4) cannot circumvent HARD-GATE wording | ✅ PASS — 0/4 bypasses succeeded; C2 artifact-chain + Iron Law + assertion/artifact distinction identified as 3 structural blocking mechanisms |

---

## Cumulative findings

| Finding | First observed | Resolution |
|---------|---------------|------------|
| s7 pipeline order incorrect in stubs | trial-11 | Skills rewritten in trial-11 |
| Agent can self-approve gate if not explicitly blocked | trial-14 | Led to trial-15 sub-agent isolation design |
| C2 artifact-chain is strongest structural gate | trial-16 | Documented in TRIAL_16_REPORT.md |
| Iron Law requires terminal output paste (not claim) | trial-16 | Core to G2 blocking mechanism |
| Previous trial CHANGELOGs non-compliant | trial-16 | Identified by changelog-checker self-scan; trials 7–15 pre-date the tool |

---

## How to access trial artifacts

Full code, tests, and build artifacts are in the `research` branch:

```bash
git checkout research
ls test_projects/
```

Reports for each trial remain in `docs/` on `main` for discoverability.
