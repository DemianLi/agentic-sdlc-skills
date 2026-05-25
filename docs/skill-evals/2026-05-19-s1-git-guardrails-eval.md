# Skill Eval — s1-git-guardrails — 2026-05-19 (re-eval)

**File**: `skills/s1-git-guardrails/SKILL.md`
**Evaluator**: s0-eval-skill
**Previous score**: 3/6 DRAFT
**Re-eval trigger**: C1/C2/C5×3 fixes applied

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ PASS | `<supporting-info>` §Semantic Boundary table names s1-git-guardrails vs s1-config-context vs update-config with specific boundary diffs |
| 2 | 雙向阻斷 | ✅ PASS | `### 絕對不要觸發的情境` block in `<what-to-do>` lists 2 concrete counter-examples: settings-only change → /update-config; full Stage 1 init → /s1-config-context |
| 3 | 輸入清洗 | ✅ PASS | Step 1 Input Validation table: non-"project"/"global" → re-prompt; >2 invalid → default to project scope with explanation |
| 4 | 漸進披露 | ✅ PASS | Each step is a focused block; JSON snippet ~10 lines, bash snippet ~4 lines — no block exceeds 50 lines |
| 5 | 優雅降級 | ✅ PASS | 3 BLOCKED fallbacks: (a) mkdir/cp failure, (b) settings.json JSON parse failure, (c) verification exit code ≠ 2 |
| 6 | 漂移監控 | ✅ PASS | `tests/fixtures/s1-git-guardrails/cases.json` referenced and exists on disk |

**Total**: 6/6 — **READY**

## Fix Summary

| Criterion | Before | After |
|-----------|--------|-------|
| C1 衝突防禦 | ❌ FAIL — no adjacent skill boundary | ✅ Semantic Boundary table, 3 skills |
| C2 雙向阻斷 | ⚠️ WEAK — Red Flags ≠ invocation triggers | ✅ 絕對不要觸發 table, 2 invocation counter-examples |
| C5 優雅降級 | ❌ FAIL — 3 external ops with no fallback | ✅ BLOCKED fallback at each failure point (mkdir, JSON parse, exit code) |
