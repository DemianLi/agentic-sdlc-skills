# Skill Eval — s1-git-guardrails — 2026-05-19

**File**: `skills/s1-git-guardrails/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 131: "Upstream Dependency: Stage 1 setup (`s1-config-context`, `s1-define-rules`)" — adjacent skills named; boundary is safety-rail installation during Stage 1 |
| 2 | 雙向阻斷 | ✅ | Lines 109-115: "Red Flags" section with 3 concrete counter-examples (skip verification, assume defaults, defer settings.json fixes) |
| 3 | 輸入清洗 | ⚠️ | Lines 39-44: user choice (scope: project vs. global) is collected; lines 100-105: optional customization offered. However, no explicit failure handling documented for invalid input (e.g., if mkdir fails, if hook entry parse fails). Completion Report (lines 117-123) has status values but no "input validation failed" path |
| 4 | 漸進披露 | ✅ | Largest inline blocks: Blocked Commands table (lines 23-33) = 6 rows; code blocks (lines 50-55, 68-77) are 6 and 10 lines respectively; Red Flags table = 4 rows. Process Flow diagram (lines 146-166) is 21 lines but is a flowchart (non-prose). No block exceeds 50 lines |
| 5 | 優雅降級 | ⚠️ | External dependencies: mkdir, cp, chmod, JSON parsing, bash execution. Step 2-4 steps have no fallback for failure (e.g., if mkdir fails, if settings.json is malformed, if hook execution fails). Line 122-123 lists BLOCKED and error states, but procedure itself does not describe recovery paths (e.g., "if settings.json fails to parse, run validation tool X") |
| 6 | 漂移監控 | ❌ | SKILL.md contains no reference to `tests/fixtures/` directory; no fixture set found on disk for regression testing hook behavior |

**Total**: 4/6 PASS — DRAFT

## Defect Details

### ⚠️ PARTIAL — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Lines 39-44, 100-105
- **Gap**: Scope choice (project vs. global) is collected, but no failure scenario is defined if the user provides invalid input (e.g., neither "project" nor "global", or ambiguous response). Step 2 (mkdir) and Step 3 (settings.json merge) assume success with no error handling specified. Completion Report does not include an explicit "input validation failed" status.

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Lines 47-105 (main procedure steps)
- **Gap**: External dependencies (file I/O, JSON parsing, bash execution) have no fallback paths documented:
  - If `mkdir -p` fails (permissions, disk full), there is no "try alternative location" fallback.
  - If `settings.json` fails to parse (malformed JSON), step does not describe validation/recovery.
  - If `chmod +x` fails, no fallback is documented.
  - Verification step (lines 83-98) can fail, but only reports "BLOCKED" status — no troubleshooting guidance.
- **Impact**: In production, if any single step fails silently or with permission errors, the guardrails will not activate, and the user won't know until attempting a destructive git command.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Line 1-177 (entire file)
- **Defect**: No reference to `tests/fixtures/` or offline eval fixture set. This skill involves critical hook installation and verification — drift detection is essential to ensure hook execution remains robust across LLM versions.
- **Impact**: Hook behavior can silently regress if the LLM stops correctly parsing JSON input to `block-dangerous-git.sh` or stops following the verification test procedure. Without offline fixtures (e.g., `hook-installation-success.json`, `hook-verification-fail.md`), there is no way to catch regressions.

## Recommended Next Step

1. Add explicit error handling to steps 2-4 (file I/O, JSON parsing) with fallback guidance or clear BLOCKED labels.
2. Add a `tests/fixtures/` section documenting expected hook behavior (e.g., test JSON inputs, expected stderr outputs), then create fixtures at `skills/s1-git-guardrails/tests/fixtures/`.
