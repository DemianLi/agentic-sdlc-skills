# Skill Eval — s0-trace-feature — 2026-05-19

**File**: `skills/s0-trace-feature/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 7: frontmatter mentions "獨立於 s1-s7 流程，完成後可銜接 /s3-eval-system"; line 180: supporting-info explains downstream difference (input to system evaluation) |
| 2 | 雙向阻斷 | ❌ | Line 14: "Do NOT invoke /s3-eval-system" names 1 skill only. Lines 156-160 "Red Flags" section is internal checklist, not negative triggers. Needs ≥2 concrete blocked scenarios with reasons |
| 3 | 輸入清洗 | ⚠️ | Line 37-38: asks user "Which feature do you want to trace?"; accepts varied input types. But no explicit failure scenario table (missing path, non-existent feature, etc.). Partially defined: user input present, failure handling incomplete |
| 4 | 漸進披露 | ✅ | Largest inline block: markdown output template (106-149) = 44 lines. < 50 lines. Process flow dot diagram small. Both acceptable |
| 5 | 優雅降級 | ✅ | Artifact Dependencies (line 220-221): Reads=source files (read-only), Writes=output file. Step 4 (lines 86-87) includes LOW CONFIDENCE block with fallback ask-user path ("proceed or investigate?"). Graceful degradation via checkpoint |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` found in SKILL.md. Root-level `/tests/fixtures/` exists but skill does not reference it; no specific trace-feature test fixtures on disk |

**Total**: 3/6 PASS — **DRAFT**

## Defect Details

### ❌ FAIL — Criterion 2: 雙向阻斷 (Negative Triggers)
- **Location**: Line 14
- **Defect**: `<HARD-GATE>` block names only "/s3-eval-system" as blocked. Line 156-160 "Red Flags" is an internal checklist, not a negative-trigger block. Rubric requires ≥2 concrete counter-examples in a dedicated block.
- **Impact**: Routing confusion. System cannot distinguish between "trace a feature" vs. "evaluate impact of feature changes" (overlap with s3-eval-system) without explicit negative examples.
- **Evidence**: Scoring rubric line 29: "≥2 concrete counter-examples" for PASS

### ⚠️ PARTIAL — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Line 37-38, 48-55
- **Defect**: Inputs are implicitly present (user picks entry point at line 48-55, specifies feature name at line 37). But no explicit failure scenario table. Missing: "What if entry point not found?", "What if workspace is empty?", "What if user provides ambiguous spec?"
- **Impact**: Step 4 (line 77-88) shows LOW CONFIDENCE warning mechanism but doesn't pre-define failure handling strategy.
- **Recommendation**: Add explicit failure scenario table after Step 1, e.g.:
  ```
  | Failure Scenario | Behavior |
  | Feature name too vague | Ask user for clarification (file path or function name) |
  | No entry points found | BLOCKED — state "searched X patterns, found nothing" |
  | User cancels confirmation | DONE_WITH_CONCERNS — report what was found before cancel |
  ```

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: SKILL.md lines 1-222
- **Defect**: No reference to `tests/fixtures/` in SKILL.md. Root-level fixtures exist but are shared across skills; no trace-feature-specific fixtures defined.
- **Impact**: No offline eval set to catch drift if trace output format or depth changes.
- **Evidence**: Scoring rubric line 85: "referenced in SKILL.md AND exists on disk" required for PASS

## Recommended Next Step

1. Add ≥2 concrete negative-trigger examples to `<HARD-GATE>` (line 10-14), e.g., "Do NOT invoke when user wants to evaluate impact (use /s3-eval-system)" and "Do NOT invoke when no codebase access exists"
2. Add explicit input failure scenario table in Step 1 (after line 38)
3. Create `tests/fixtures/trace-feature-fixture.md` with a traced feature example and reference it in supporting-info (line 220)
