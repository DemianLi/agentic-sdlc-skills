# Skill Eval — s0-trace-feature — 2026-05-19

**File**: `skills/s0-trace-feature/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ PASS | Lines 21-27: Table explicitly names `/s3-eval-system`, `/s2-capture-vision`, `/s4-local-debug` with specific differences (evaluate vs. trace vs. debug) |
| 2 | 雙向阻斷 | ✅ PASS | Lines 21-27: "絕對不要觸發的情境" table with 3 concrete counter-examples; each row specifies the wrong skill's trigger condition |
| 3 | 輸入清洗 | ✅ PASS | Lines 44-52: Input validation table defines failure scenarios (vague name, not found, multiple matches) with defined behavior (re-prompt, BLOCKED, list candidates) |
| 4 | 漸進披露 | ✅ PASS | Low-confidence block (lines 111–121) ~10 lines; Mermaid template (lines 132–148) ~16 lines; no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ⚠️ PARTIAL | Multiple file reads (codebase scanning) have no fallback defined; line 169 requires "Commit the file to git before reporting completion" with no BLOCKED fallback if commit fails |
| 6 | 漂移監控 | ✅ PASS | Line 239: References `tests/fixtures/s0-trace-feature/cases.json`; fixture exists with 3 test scenarios covering complete traces, gap detection, and side effects |

**Total**: 5/6 PASS — **NEAR READY**

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Lines 77–85 (Step 3 — Full Chain Trace), Line 169 (git commit requirement)
- **Gap**: 
  - Step 3 reads workspace files with no fallback if a file is unreadable (permission denied, missing). Should state: "If file unreadable, mark as `[? — permission denied]`."
  - Line 169: "Commit the file to git before reporting completion" is a write operation with no fallback. If git commit fails (unstaged changes, merge conflict), skill has no recovery path.
- **Impact**: Read-only failures have low blast-radius, but the final git commit could silently fail, leaving the trace artifact uncommitted and incomplete.

## Recommended Next Step

1. Add fallback behavior for unreadable files in Step 3 (e.g., mark as `[? — unreadable]` and continue).
2. Wrap the git commit in try-catch logic: if commit fails, offer to save artifact with BLOCKED status and let user commit manually.

This will elevate Criterion 5 to PASS, making the skill PRODUCTION READY (6/6).
