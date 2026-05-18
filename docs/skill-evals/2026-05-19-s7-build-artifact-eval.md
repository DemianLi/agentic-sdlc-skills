# Skill Eval — s7-build-artifact — 2026-05-19

**File**: `skills/s7-build-artifact/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 15, 138–145: Names 3 adjacent skills (`/s7-deploy`, `/s7-release-notes`, `/s7-telemetry`) with clear pipeline boundary — build phase produces artifact, deploy phase consumes it |
| 2 | 雙向阻斷 | ✅ | Lines 8–11, 74, 98: 4+ negative triggers ("Do NOT proceed if test-results.json missing", "Do NOT push tag", "Do NOT attempt to push to registry", "release_gate is not PASS") with concrete scenarios |
| 3 | 輸入清洗 | ✅ | Lines 28–33: Pre-flight Check table lists 4 explicit inputs (`test-results.json`, `release_gate`, version, build tool) with defined failure behaviors (NEEDS_CONTEXT / BLOCKED / error) |
| 4 | 漸進披露 | ✅ | Largest code block: 16 lines (lines 149–166, process flow diagram); largest table: 9 rows (lines 83–91); all under 50-line threshold |
| 5 | 優雅降級 | ⚠️ | Lines 50–72: Build command step has no fallback if `python -m build` fails (line 33 mentions "Report specific error" but no fallback action defined); git operations unconditional without retry |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` reference found in SKILL.md; no fixture directory exists for s7-build-artifact |

**Total**: 4/6 PASS — NEAR READY

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級
- **Location**: Lines 49–75 (Step 2 & 3)
- **Gap**: Build step (python -m build / npm pack / docker build) has no fallback. If build fails mid-process, skill only says "Report specific error" (line 33) but no retry logic or alternative build path is defined. Similarly, git tag creation (lines 68–72) is unconditional — if `git tag` fails due to detached HEAD or tag collision, there is no fallback or graceful skip.
- **Impact**: In production, a transient build failure or git tag collision will block the entire pipeline with no recovery path.

### ❌ FAIL — Criterion 6: 漂移監控
- **Location**: File-wide
- **Defect**: No reference to `tests/fixtures/` directory in SKILL.md. No fixture files exist for evaluating skill correctness as models drift.
- **Impact**: Skill has no offline test harness. If model behavior changes over time, there is no way to detect build-artifact-phase regressions.

## Recommended Next Step

1. **Fix Criterion 5**: Add fallback behavior to lines 50–72. Example: "If `python -m build` fails, report BUILD_FAILED with error details and await user decision before proceeding." Consider adding a dry-run retry.
2. **Fix Criterion 6**: Create `skills/s7-build-artifact/tests/fixtures/` directory with ≥1 fixture (e.g., mock `test-results.json` with `release_gate: "PASS"` and a minimal `pyproject.toml`) and reference it in the SKILL.md body under a new "Validation" or "Test" section.
