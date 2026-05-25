# Skill Eval — s2-struct-req — 2026-05-19

**File**: `skills/s2-struct-req/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 106: Upstream `/s2-align-req` and downstream `/s2-snapshot-ctx` named; explicit semantic boundary (alignment scope → testable acceptance criteria) |
| 2 | 雙向阻斷 | ✅ | Lines 8-9: HARD-GATE "Do NOT commit...until...every requirement has explicit, testable acceptance criteria"; Red Flags (lines 84-90) contain 3 concrete counter-examples (missing test automation, vague language like "fast"/"correct", premature commit without approval) |
| 3 | 輸入清洗 | ✅ | Input explicitly: alignment document (line 106 reference); failure scenario defined at lines 96-98 (BLOCKED state for unclear acceptance criteria) |
| 4 | 漸進披露 | ✅ | REQ template (lines 39-50): 12 lines; Red Flags table (lines 84-90): 7 lines. All blocks well under 50-line limit. |
| 5 | 優雅降級 | ✅ | Document commitment gate (lines 8-9) is explicit. Change control process (lines 72-80) provides fallback: create new version if changes required after commitment, not silent edits. |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` found anywhere in SKILL.md |

**Total**: 5/6 PASS — **NEAR-READY**

## Defect Details

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)

- **Location**: Entire document (no fixture reference)
- **Defect**: SKILL.md does not reference `tests/fixtures/` directory or any fixture files.
- **Impact**: Without fixtures, drift is undetectable. Future model iterations have no offline eval baseline to verify that structured requirements output (REQ blocks with acceptance criteria) remains consistent.

## Recommended Next Step

Add a `## Eval Fixtures` section referencing `tests/fixtures/` with ≥1 example structured requirements fixture (e.g., `example-requirements-doc.md`). Include fixture path in supporting-info.
