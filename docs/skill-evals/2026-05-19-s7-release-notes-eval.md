# Skill Eval — s7-release-notes — 2026-05-19

**File**: `skills/s7-release-notes/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 4–5, 165–166: Names upstream `/s7-deploy` and downstream `/s7-telemetry`; clear boundary: release-notes phase reads deploy confirmation and writes CHANGELOG for telemetry to consume |
| 2 | 雙向阻斷 | ✅ | Lines 8–12, 148–150: 3+ negative triggers ("Do NOT write to CHANGELOG until deploy log exists", "Do NOT skip /s7-telemetry's own HARD-GATE", "猜測的 release notes 無法審計") with concrete examples |
| 3 | 輸入清洗 | ✅ | Lines 27–37: Explicit source material list (git log, requirements doc, audit doc, deploy log, prior CHANGELOG) with defined extraction rules; failure: "state what is missing" (line 157: NEEDS_CONTEXT) |
| 4 | 漸進披露 | ✅ | Largest code block: 17 lines (lines 65–83, CHANGELOG markdown example); largest table: 8 rows (lines 50–57, classification table); both under 50-line threshold |
| 5 | 優雅降級 | ⚠️ | Lines 27–44: git log and file reads (lines 39–44) have no fallback if `git log` fails or requirements doc is missing. Handling defined only as "state what is missing" but no graceful skip or alternative source path. |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` reference found in SKILL.md; no fixture directory exists for s7-release-notes |

**Total**: 4/6 PASS — NEAR READY

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級
- **Location**: Lines 27–44 (Step 1: Gather Source Material)
- **Gap**: File reads (docs/specs/.md, docs/audit/.md, docs/releases/.md, CHANGELOG.md) are unconditional. If any required file is missing, the skill reports NEEDS_CONTEXT (line 157) but does not attempt to proceed with partial information (e.g., "write CHANGELOG from git log alone if requirements doc is unavailable"). Git log fallback exists (line 41: `PREV_TAG` with `|| echo ""`) but is minimal.
- **Impact**: Missing a single audit document blocks the entire release-notes phase with no partial-success path.

### ❌ FAIL — Criterion 6: 漂移監控
- **Location**: File-wide
- **Defect**: No reference to `tests/fixtures/` directory in SKILL.md. No fixture files exist for evaluating release-notes-phase correctness.
- **Impact**: Skill has no offline eval harness. Model drift cannot be detected.

## Recommended Next Step

1. **Fix Criterion 5**: Add fallback logic to lines 27–44. Example: "If docs/specs/*.md is missing, extract feature names from commit messages prefixed with 'feat:' instead. If PR review is missing, continue without Breaking Changes section." Define minimum viable CHANGELOG (git log + version only).
2. **Fix Criterion 6**: Create `skills/s7-release-notes/tests/fixtures/` with ≥1 fixture (e.g., `sample_deploy_log.md` and `sample_requirements.md`) and reference in SKILL.md.
