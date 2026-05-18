# Skill Eval — s5-sast-lint — 2026-05-19

**File**: `skills/s5-sast-lint/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 122–127: `<supporting-info>` names downstream `/s5-audit-rules` and upstream "Stage 4 output", explains role as "unforgiving machine" in "SAST Mode" distinct from peer review auditor |
| 2 | 雙向阻斷 | ✅ | Line 8–14: `<HARD-GATE>` with "Do NOT hand off to `/s5-audit-rules` if there are CRITICAL linting errors, SAST findings (HIGH or CRITICAL severity), or formatting issues remaining"; Red Flags table (line 102–108) provides 3 concrete counter-examples (ignoring warnings, CI reliance, skipping formatter) |
| 3 | 輸入清洗 | ✅ | Inputs explicitly listed (line 24, 28): `RULES.md` configuration, source files. Failure scenarios: line 55 classifies CRITICAL/WARNING/INFO with actions (line 57); line 118 completion states include "NEEDS_CONTEXT — linter config not found in RULES.md; state what is missing." Handling defined for all failure paths. |
| 4 | 漸進披露 | ✅ | Largest inline blocks: Step 2–4 code examples (line 31–49): 19 lines total across 3 steps. Classification table (line 54–59): 7 lines. Red Flags table (line 102–108): 7 lines. Example report (line 78–98): 21 lines, <50 limit. All inline blocks <50 lines. |
| 5 | 優雅降級 | ⚠️ | External dependencies: linter/formatter/SAST tool invocation (execute), `RULES.md` read. Step 1 (line 24) loads `RULES.md` with no fallback if file missing. Completion state "NEEDS_CONTEXT" (line 118) exists but workflow has no early BLOCKED check if `RULES.md` not found. |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` directory referenced anywhere in SKILL.md. No linter config samples, SAST findings examples, or test case set mentioned. Criterion 6 FAIL. |

**Total**: 4/6 PASS — DRAFT

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Line 23–29 (Step 1 in `<what-to-do>`)
- **Gap**: "Read `RULES.md` from Stage 1" (line 24) assumes file exists. No fallback if `RULES.md` is missing. Completion state "NEEDS_CONTEXT" (line 118) exists but Step 1 has no explicit BLOCKED label or early failure path.
- **Impact**: If `RULES.md` is missing, skill cannot identify linter/formatter/SAST tools or forbidden patterns. Steps 2–6 proceed with undefined configuration, producing invalid lint report. Should BLOCKED immediately if `RULES.md` not found.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Entire SKILL.md
- **Defect**: No reference to `tests/fixtures/` directory. No linter config samples, SAST findings, or test codebase examples mentioned for drift monitoring.
- **Impact**: Cannot verify skill consistency. Skill's linting and SAST strategy changes silently with model updates; no offline eval set exists to detect regressions in classification accuracy, auto-fix behavior, or CRITICAL vs. WARNING distinction.

## Recommended Next Step

Create `tests/fixtures/` directory with sample SAST findings, linter configurations, and codebase samples (e.g., `tests/fixtures/2026-05-19-sast-samples/`) for drift monitoring. Add explicit BLOCKED check at Step 1 if `RULES.md` is not found or cannot be parsed.
