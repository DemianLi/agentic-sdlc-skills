# Skill Eval — s1-lock-tech-stack — 2026-05-19

**File**: `skills/s1-lock-tech-stack/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 14: "Awaiting your approval to proceed to /s3-design-arch (Stage 3 System Architect)" — adjacent skill named; line 65: "Downstream Target: Stage 3 (System Architect)" with explicit dependency description |
| 2 | 雙向阻斷 | ✅ | Lines 44-50: "Red Flags" section with 3 concrete counter-examples ("latest" assumption, deferred compatibility, auto-dependency selection) |
| 3 | 輸入清洗 | ✅ | Lines 25-37: explicit inputs (runtime environment, framework, database, critical dependencies); line 40: "Wait for user resolution"; lines 39-42 all have defined success criteria (compatibility audit, pinned versions, ADR creation) |
| 4 | 漸進披露 | ✅ | Largest inline blocks: Red Flags table (3 rows × 2 cols); Runtime Environment example (6 lines); Execution Rules (5 lines). No single block exceeds 50 lines. Large artifact templates (lock files, ADR) are intentionally externalized (line 42) |
| 5 | 優雅降級 | ⚠️ | Step 0-4 involve multiple external dependencies: runtime version command execution (line 26-31), file I/O (lock files, ADR creation), compatibility checking. Step 0 is read-only (version check). Steps 1-2 have success criteria but no fallback documented (e.g., if runtime command fails, if user refuses to resolve compatibility issues, procedure does not describe abort/retry path). BLOCKED status exists (line 56) but recovery guidance is minimal |
| 6 | 漂移監控 | ❌ | SKILL.md contains no reference to `tests/fixtures/` directory; no fixture set found on disk for regression testing lock file generation and ADR creation |

**Total**: 5/6 PASS — NEAR-READY

## Defect Details

### ⚠️ WEAK — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Lines 25-42 (main execution steps)
- **Gap**: Step 0 (runtime version check) is read-only and has a fallback path (write to RULES.md with timestamp); however, Steps 1-3 have external dependencies with incomplete fallback guidance:
  - If runtime command fails (not found, permissions error), step does not describe alternative verification methods.
  - If compatibility check finds a mismatch, line 40 says "Wait for user resolution before proceeding" but does not describe what happens if user refuses to resolve (e.g., do we BLOCK or PARTIAL?).
  - Lock file generation (Step 3) assumes successful file write; no fallback if disk/permissions issue occurs.
  - ADR generation (Step 4) depends on `docs/adr/` directory existence; if it doesn't exist, no guidance on mkdir fallback.
- **Impact**: Multiple write operations (lock files, ADR) without documented failure paths could result in partial/invalid state. "Wait for user resolution" is reactive, not proactive error handling.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Line 1-77 (entire file)
- **Defect**: No reference to `tests/fixtures/` or offline eval fixture set. Lock file generation and ADR creation depend on accurate LLM reasoning about dependency compatibility and tech stack justification — high-drift-risk tasks.
- **Impact**: Without offline fixtures (e.g., `lock-python-fastapi.txt`, `adr-postgres-choice.md`, `compatibility-check-fail.md`), there is no way to detect if future LLM versions stop correctly performing compatibility audits, start over-pinning versions, or generate weak ADRs. This is a critical Stage 1 lock-in skill — drift detection prevents cascading failures in Stages 3-4.

## Recommended Next Step

1. Add fallback guidance for Step 0-3 (e.g., "if runtime command fails, try alternative versions or ask user to install latest; if compatibility check fails, show comparison table and ask for resolution; if lock file write fails, describe manual workaround").
2. Add a `tests/fixtures/` section referencing 3–4 baseline lock files and ADRs (e.g., `lock-node-express.json`, `adr-postgresql-choice.md`), then create fixtures at `skills/s1-lock-tech-stack/tests/fixtures/`.
