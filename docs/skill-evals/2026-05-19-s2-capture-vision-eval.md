# Skill Eval — s2-capture-vision — 2026-05-19

**File**: `skills/s2-capture-vision/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Lines 119-122: Downstream `/s2-align-req` named with explicit semantic boundary (vision capture vs. alignment resolution) |
| 2 | 雙向阻斷 | ✅ | Lines 8-9: HARD-GATE "Do NOT proceed...until...written...approved...committed"; Red Flags (lines 98-104) contain 3 concrete counter-examples (interpretation errors, uncommitted drafts, incomplete coverage) |
| 3 | 輸入清洗 | ⚠️ WEAK | Inputs implicit (brainstorm doc, project context) rather than explicitly listed with format. Failure scenarios defined (lines 108-112: BLOCKED, NEEDS_CONTEXT states), but input specification is inferred, not explicit. |
| 4 | 漸進披露 | ✅ | Largest block: dot diagram (lines 125-159): 35 lines, under 50-line limit. No oversized inline blocks. |
| 5 | 優雅降級 | ✅ | Step 1 context reads (line 24) have graceful fallback (NEEDS_CONTEXT at line 112). Spec write (line 29) is low-risk. Commitment required implicitly (line 31 self-review). |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` found anywhere in SKILL.md |

**Total**: 5/6 PASS — **NEAR-READY**

## Defect Details

### ⚠️ WEAK — Criterion 3: 輸入清洗 (Input Linting)

- **Location**: Lines 21-32 (Checklist section)
- **Gap**: Inputs are implicit (brainstorm doc from `/s0-brainstorm`, project context, CONTEXT.md, docs/, recent commits) rather than explicitly named in an "Inputs:" section. Failure behaviors (BLOCKED, NEEDS_CONTEXT) are defined, but the input specification could be clearer.
- **Recommendation**: Add an "Inputs" section naming brainstorm doc, CONTEXT.md path, and acceptable context file formats before Step 0.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)

- **Location**: Entire document (no fixture reference)
- **Defect**: SKILL.md does not reference `tests/fixtures/` directory. No fixture files are named or referenced.
- **Impact**: Without fixtures, drift cannot be monitored. Future model iterations will have no offline eval baseline to verify that vision spec output format remains consistent.

## Recommended Next Step

1. Clarify criterion 3 by adding explicit "Inputs:" section in `<what-to-do>` (before Step 0).
2. Add `tests/fixtures/` reference with ≥1 example vision spec fixture (e.g., `example-vision-spec.md`) in SKILL.md supporting-info.
