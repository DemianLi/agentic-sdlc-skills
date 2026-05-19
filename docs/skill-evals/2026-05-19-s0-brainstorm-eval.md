# Skill Eval — s0-brainstorm — 2026-05-19

**File**: `skills/s0-brainstorm/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ⚠️ PARTIAL | Lines 138-142: Mentions `/s2-capture-vision` as downstream, but no adjacent skills named with specific differences explaining the boundary |
| 2 | 雙向阻斷 | ❌ FAIL | No "絕對不要觸發" or "Do NOT use" block found; no negative trigger examples listed |
| 3 | 輸入清洗 | ⚠️ PARTIAL | Accepts vague problem descriptions, but no explicit input specification; no failure scenarios with defined behavior documented |
| 4 | 漸進披露 | ✅ PASS | Workflow steps are clear and concise; visual questions (lines 35-42), problem space table (lines 52-59), framings (lines 68-72)—no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ⚠️ PARTIAL | File write to `docs/brainstorm/YYYY-MM-DD-<topic>-problem-draft.md` has no fallback defined, but write is low blast-radius |
| 6 | 漂移監控 | ✅ PASS | Line 187 references `tests/fixtures/s0-brainstorm/cases.json`; fixture file exists with 3 test cases |

**Total**: 2/6 PASS — **DRAFT**

## Defect Details

### ❌ FAIL — Criterion 2: 雙向阻斷 (Negative Triggers)
- **Location**: Entire document
- **Defect**: No negative trigger block exists. Skill lists what TO DO (Steps 1–7) but never explicitly states when NOT to invoke this skill or scenarios where it would produce wrong output.
- **Impact**: In production with many s0-* skills, routing confusion could invoke s0-brainstorm for problems already ready for s2-capture-vision, wasting tokens and user time on re-brainstorming.

### ⚠️ PARTIAL — Criterion 1: 衝突防禦 (Semantic Anti-Collision)
- **Location**: Lines 138-142 (`<supporting-info>` section)
- **Gap**: `/s2-capture-vision` is mentioned as "downstream target," but the boundary is not explained. What problem statement features justify routing to s2 vs. staying in s0 for more brainstorm iterations? Never stated.

### ⚠️ PARTIAL — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Lines 16-131
- **Gap**: Step 1 says "Ask the user to describe," but what if they refuse? What if their description is single-word gibberish? What minimum input quality is required to proceed? No fallback behavior defined (re-prompt n times? BLOCKED?).

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Line 102 (Step 7 — file write)
- **Gap**: If file write fails (permissions, path doesn't exist, disk full), skill has no fallback. Should either: (a) catch write errors and offer to dump to stdout, or (b) mark as BLOCKED with explicit error message.

## Recommended Next Step

Add a "Do NOT use this skill if" block in `<what-to-do>` listing ≥2 concrete counter-examples (e.g., "if problem statement already exists," "if user has already chosen a framing"), then re-evaluate Criterion 2.
