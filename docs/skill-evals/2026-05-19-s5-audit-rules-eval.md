# Skill Eval — s5-audit-rules — 2026-05-19

**File**: `skills/s5-audit-rules/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 43–47: `<supporting-info>` names upstream `/s5-sast-lint` and downstream `/s5-pr-review`, explains role as "architectural guardian" |
| 2 | 雙向阻斷 | ✅ | Line 7–15: `<HARD-GATE>` with explicit "Do NOT hand off to `/s5-pr-review` if code violates RULES.md"; Red Flags table (line 27–33) provides 3 concrete counter-examples (architecture violations, rule strictness, outdated docs) |
| 3 | 輸入清洗 | ✅ | No external user inputs. Skill operates on ambient context only (`RULES.md`, design docs, source files). Mark: PASS with note "no external inputs required." |
| 4 | 漸進披露 | ✅ | All inline blocks well under 50 lines. Largest block: Red Flags table (7 lines). Code fences: none. `<what-to-do>` body subsections (lines 20–41): each < 10 lines. |
| 5 | 優雅降級 | ⚠️ | External dependencies: file reads (`RULES.md`, design docs, source files). No explicit fallback if design docs missing. Line 20 says "Load RULES.md" with no BLOCKED/fallback. Completion Report (line 40) includes "NEEDS_CONTEXT" state but step 1 has no BLOCKED label. |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` directory referenced anywhere in SKILL.md. No fixture path mentioned. Criterion 6 FAIL. |

**Total**: 4/6 PASS — DRAFT

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Line 20–25 (Step 1–5 in `<what-to-do>`)
- **Gap**: Steps explicitly read `RULES.md` (line 20) and `docs/arch/YYYY-MM-DD-<topic>-design.md` (line 20) without fallback or BLOCKED label if files are missing. Completion Report mentions "NEEDS_CONTEXT" but no early failure path in workflow.
- **Impact**: If design docs are missing, skill proceeds through steps 2–6 with incomplete context, producing invalid audit report. Should BLOCKED before Step 2 if design doc not found.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Entire SKILL.md
- **Defect**: No reference to `tests/fixtures/` directory. No fixture path mentioned anywhere.
- **Impact**: Cannot verify skill behavior drift as models evolve. Production routing without drift monitoring is high-risk; skill behavior changes silently.

## Recommended Next Step

Add `tests/fixtures/` reference with ≥1 fixture file (e.g., `tests/fixtures/2026-05-19-violation-samples/`) to enable drift monitoring. Add explicit "NEEDS_CONTEXT → BLOCKED" path in Step 1 if design doc not found (reference `NEEDS_CONTEXT` completion state from line 41).
