# Skill Eval — s1-config-context — 2026-05-19

**File**: `skills/s1-config-context/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 56: references `/s1-define-rules` (Recommended); line 13-14: explicit routing to next skill |
| 2 | 雙向阻斷 | ✅ | Lines 35-41: "Red Flags" section with 3 concrete counter-examples (vague inference, batch querying, missing boundaries) |
| 3 | 輸入清洗 | ✅ | Line 24-27: explicit input (user domain terms); failure scenarios documented (line 41: no AI boundary definition = blocked) |
| 4 | 漸進披露 | ✅ | No single inline block exceeds 50 lines; largest section (Red Flags table) = 7 rows; format definition at line 60-63 is structural |
| 5 | 優雅降級 | ✅ | Completion Report (line 43-48) has all four status values; no external dependencies; pure documentation task |
| 6 | 漂移監控 | ❌ | SKILL.md contains no reference to `tests/fixtures/` directory; no fixture path found on disk |

**Total**: 5/6 PASS — NEAR READY

## Defect Details

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Line 1-70 (entire file)
- **Defect**: No reference to `tests/fixtures/` or any eval fixture set in SKILL.md. Criterion 6 requires explicit reference to offline fixtures to prevent skill drift as LLM behavior evolves.
- **Impact**: Without an offline eval fixture set, it's impossible to detect if future LLM versions drift from the intended behavior (e.g., if model stops respecting the "ONE AT A TIME" domain language rule at line 24). CONTEXT.md creation requires precise, iterative human-model interaction — this is a high-drift-risk skill.

## Recommended Next Step

Add a `tests/fixtures/` section to SKILL.md that references 3–5 fixture files (e.g., `context-good-glossary.md`, `context-batch-question-fail.md`) demonstrating correct vs. incorrect behavior, then ensure those fixtures exist on disk at `skills/s1-config-context/tests/fixtures/`.
