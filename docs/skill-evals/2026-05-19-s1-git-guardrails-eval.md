# Skill Eval — s1-git-guardrails — 2026-05-19

**File**: `skills/s1-git-guardrails/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ❌ FAIL | Lines 138–140: Upstream dependencies listed (`s1-config-context`, `s1-define-rules`), but no adjacent guard-rail skills named; no explanation of how this skill differs from other safety-rail installations |
| 2 | 雙向阻斷 | ⚠️ PARTIAL | Lines 116–122: "Red Flags" section lists 3 meta-concerns about implementation pitfalls, but no "Do NOT use this skill if" block; counter-examples are about what NOT to do in implementation, not when NOT to invoke the skill |
| 3 | 輸入清洗 | ✅ PASS | Lines 46–51: Input validation table defines failure scenarios (invalid choice, repeated invalid input) with defined behavior (re-prompt, default to project scope) |
| 4 | 漸進披露 | ✅ PASS | Script copy commands (lines 57–69) are ~6 lines each; no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ❌ FAIL | Multiple external dependencies (mkdir, file copy, chmod, settings.json parse/merge, git operations) with no fallback or BLOCKED handling defined for each; lines 57–69 assume all operations succeed silently |
| 6 | 漂移監控 | ✅ PASS | Line 181: References `tests/fixtures/s1-git-guardrails/cases.json`; fixture exists with 3 scenarios (project-level setup, customization, command blocking verification) |

**Total**: 3/6 PASS — **DRAFT**

## Defect Details

### ❌ FAIL — Criterion 1: 衝突防禦 (Semantic Anti-Collision)
- **Location**: Lines 138–140 (`<supporting-info>`)
- **Defect**: Lists upstream stage (Stage 1) but never names adjacent s1-* skills or explains when to use this vs. other setup skills. Is this for first-time projects only? Can it run on projects that already have guardrails?
- **Impact**: In production, s1-git-guardrails could be invoked redundantly or on the wrong projects, causing duplicate hook installations.

### ❌ FAIL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Lines 53–87 (Steps 2–3)
- **Defects**:
  - Line 57–69: `mkdir -p`, `cp`, `chmod +x` commands assumed to succeed; no error handling. What if disk is full? Permissions denied?
  - Line 72–85: settings.json merge assumed to succeed; what if JSON is malformed or locked by another process?
  - No explicit BLOCKED status if any setup step fails.
- **Impact**: Hook could be partially installed, creating false sense of security (user thinks guardrails active, but hook never fires). High blast-radius for security-critical feature.

### ⚠️ PARTIAL — Criterion 2: 雙向阻斷 (Negative Triggers)
- **Location**: Lines 116–122
- **Gap**: "Red Flags" are implementation gotchas, not skill invocation anti-patterns. Missing explicit block listing scenarios where this skill should NOT run (e.g., "if project already has pre-commit hooks installed," "if user has no git repo," etc.).

## Recommended Next Steps

1. Add explicit "Do NOT use if" section before Step 1, listing ≥2 concrete invocation scenarios that should route elsewhere.
2. Wrap each external dependency (mkdir, cp, chmod, settings.json merge, git commit) in try-catch with explicit BLOCKED status and error message if operation fails.
3. Add verification in Step 4 that not only tests command blocking, but also confirms hook installed correctly by running a safe command (should exit code 0).

This will require addressing both Criterion 1 and 5 to reach NEAR READY.
