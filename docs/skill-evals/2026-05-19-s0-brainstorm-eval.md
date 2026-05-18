# Skill Eval — s0-brainstorm — 2026-05-19

**File**: `skills/s0-brainstorm/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 12, 138: names `/s2-capture-vision` with clear downstream relationship |
| 2 | 雙向阻斷 | ❌ | Line 13: "Do NOT invoke" block mentions only 1 skill; needs ≥2 concrete counter-examples |
| 3 | 輸入清洗 | ✅ | No external user inputs required (operates on user conversation only). PASS with note: "ambient context only" |
| 4 | 漸進披露 | ✅ | Max inline block: dot diagram 26 lines (146-171); markdown template 44 lines (104-119). Both < 50 lines |
| 5 | 優雅降級 | ✅ | Artifact Dependencies (line 186-187): Reads=none, Writes=optional file. No high-risk external dependencies |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` reference found in SKILL.md; no drift monitoring fixtures on disk |

**Total**: 4/6 PASS — **DRAFT**

## Defect Details

### ❌ FAIL — Criterion 2: 雙向阻斷 (Negative Triggers)
- **Location**: Line 13
- **Defect**: `<HARD-GATE>` block contains "Do NOT invoke /s2-capture-vision or any other skill automatically" but provides only 1 concrete blocked skill. Rubric requires ≥2 concrete counter-examples.
- **Impact**: Over-generalization risk. When this skill is invoked alongside others, routing system lacks explicit examples of what should NOT trigger brainstorm.
- **Evidence**: Scoring rubric line 29: "≥2 concrete counter-examples" required for PASS

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: SKILL.md lines 1-189
- **Defect**: No reference to `tests/fixtures/` directory found in SKILL.md. Fixture system on disk exists (e.g., `/tests/fixtures/fast-track-cases.json`) but this skill does not reference it for offline eval.
- **Impact**: No baseline fixtures to detect skill drift as models evolve. If problem-generation logic degrades, no automated regression check exists.
- **Evidence**: Scoring rubric line 85-87: "referenced in SKILL.md AND exists on disk" required for PASS

## Recommended Next Step

Add ≥2 concrete negative-trigger examples to the `<HARD-GATE>` block (line 10-14), e.g., "Do NOT invoke when user provides a detailed spec (use /s1-refine-spec instead)" and "Do NOT invoke when the problem is already solved by an existing tool". Then create or link `tests/fixtures/brainstorm-fixture.md` with a test case and add reference at line 186 in supporting-info.
