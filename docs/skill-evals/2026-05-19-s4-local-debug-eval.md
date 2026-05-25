# Skill Eval — s4-local-debug — 2026-05-19

**File**: `skills/s4-local-debug/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 79 references `/s4-tdd`; lines 136–137 name `/s4-impl-task` as upstream and Stage 5 as downstream. Role is Debug Implementer, distinct from TDD writer and task implementer. |
| 2 | 雙向阻斷 | ✅ | Lines 8–18 HARD-GATE; lines 112–118 Red Flags section with 3 concrete counter-examples (直接改吧, 4號假設, 先提交修復). |
| 3 | 輸入清洗 | ✅ | No external inputs required; operates on ambient codebase context only. Lines 88–97 Error Type Triage define behaviors for all failure scenarios. Special case: no external inputs required → PASS. |
| 4 | 漸進披露 | ✅ | 6-phase loop (lines 24–84) broken into named subsections. Error Type Triage table (lines 88–97) ~10 rows. Red Flags table ~6 rows. All inline blocks well under 50 lines. |
| 5 | 優雅降級 | ✅ | Line 34: "STOP. Report `NEEDS_CONTEXT`" for intermittent failures. Lines 104–107: Escalation protocol at 3 failed attempts (explicit BLOCKED). All external dependencies (test runs, file reads) have fallback or explicit failure labels. |
| 6 | 漂移監控 | ✅ | Line 173 references `tests/fixtures/s4-local-debug/cases.json`. Verified: fixture exists on disk. |

**Total**: 6/6 PASS — **READY**

## Defect Details

None — all criteria met at PASS level.

## Recommended Next Step

No action required. Skill is production-ready.
