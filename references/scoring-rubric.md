# Skill Scoring Rubric

Source of truth for `s0-eval-skill`. Defines PASS/PARTIAL/FAIL conditions for all 6 production-quality criteria.

Last updated: 2026-05-19

---

## Criterion 1 — 衝突防禦 (Semantic Anti-Collision)

**Purpose**: Define semantic boundary against adjacent skills to prevent routing confusion when dozens of skills coexist.

| Score | Condition |
|-------|-----------|
| ✅ PASS | `<supporting-info>` or `<what-to-do>` names ≥1 adjacent skill AND explains the specific difference |
| ⚠️ PARTIAL | Adjacent skills mentioned but explanation is vague ("similar" without specifics) |
| ❌ FAIL | No adjacent skill named; boundary undefined |

**Evidence to capture**: Section name + line number where comparison appears.

---

## Criterion 2 — 雙向阻斷 (Negative Triggers)

**Purpose**: Prevent over-generalization by explicitly listing scenarios where this skill must NOT be triggered.

| Score | Condition |
|-------|-----------|
| ✅ PASS | Contains a "絕對不要" / "Do NOT use" / "BLOCKED" trigger block with ≥2 concrete counter-examples |
| ⚠️ PARTIAL | Has ≥1 counter-example but fewer than 2; OR uses vague language without specifics |
| ❌ FAIL | No negative trigger block found |

**Evidence to capture**: Line number of block + count of concrete examples listed.

---

## Criterion 3 — 輸入清洗 (Input Linting)

**Purpose**: Prevent silent failures or misdirected execution from invalid inputs.

| Score | Condition |
|-------|-----------|
| ✅ PASS | Inputs explicitly listed AND every failure scenario (missing, wrong type, non-existent path) has a defined behavior (BLOCKED / PARTIAL / error message) |
| ⚠️ PARTIAL | Inputs listed but ≥1 failure scenario has no defined behavior; OR inputs are inferred but not explicit |
| ❌ FAIL | No input specification found; or failure handling entirely undefined |

**Special case**: If the skill accepts no user-provided inputs (operates on ambient context only), mark ✅ PASS with note "no external inputs required."

---

## Criterion 4 — 漸進披露 (Progressive Disclosure)

**Purpose**: Keep routing-phase token cost low. Large boilerplate and verbose templates must be externalized rather than embedded inline.

**Definition of "inline block"**: A single contiguous block delimited by ` ``` ` fences, contiguous `|` table rows, or a single `###` subsection body — **not** the entire `<what-to-do>` section wrapper.

| Score | Condition |
|-------|-----------|
| ✅ PASS | No single inline block (as defined above) exceeds 50 lines; large templates reference external files |
| ⚠️ PARTIAL | One inline block is 51–80 lines but contains non-repetitive prose (not boilerplate) |
| ❌ FAIL | Any single inline block exceeds 80 lines; OR a clearly repetitive template/boilerplate is embedded inline when it could reference an external file |

---

## Criterion 5 — 優雅降級 (Graceful Degradation)

**Purpose**: Ensure every step with an external dependency has a fallback or an explicit BLOCKED/FAIL label.

**External dependency**: file read, file write, git operation, API call, tool invocation, directory existence check.

| Score | Condition |
|-------|-----------|
| ✅ PASS | Every step with an external dependency has either a fallback path OR an explicit BLOCKED/FAIL label |
| ⚠️ PARTIAL | ≥1 step with external dependency has no fallback and no BLOCKED label, but the step is low blast-radius (read-only) |
| ❌ FAIL | ≥1 step with high blast-radius (write, commit, delete) has no failure handling; OR multiple read steps have no fallback |

---

## Criterion 6 — 漂移監控 (Drift Monitoring)

**Purpose**: Prevent skill drift as underlying models evolve. Skills must reference an offline eval fixture set that actually exists on disk.

| Score | Condition |
|-------|-----------|
| ✅ PASS | `tests/fixtures/` directory referenced in SKILL.md AND exists on disk with ≥1 fixture file |
| ⚠️ PARTIAL | Fixture directory referenced in SKILL.md but directory is empty; OR reference exists but path is partially incorrect |
| ❌ FAIL | No fixture directory referenced in SKILL.md; OR reference points to a non-existent path |

---

## Score Summary Rule

| Total ✅ | Result |
|---------|--------|
| 6/6 | PRODUCTION READY |
| 5/6, ❌ ≤ 1 | NEAR READY — address ❌ before shipping |
| 4/6 or below | DRAFT — not safe for production routing |

---

## Report Template

Write evaluation output to: `docs/skill-evals/YYYY-MM-DD-<skill-name>-eval.md`

Use this template exactly:

```
# Skill Eval — <skill-name> — YYYY-MM-DD

**File**: `skills/<skill-name>/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅/⚠️/❌ | Line N: ... |
| 2 | 雙向阻斷 | ✅/⚠️/❌ | Line N: ... |
| 3 | 輸入清洗 | ✅/⚠️/❌ | Line N: ... |
| 4 | 漸進披露 | ✅/⚠️/❌ | Line N: ... |
| 5 | 優雅降級 | ✅/⚠️/❌ | Line N: ... |
| 6 | 漂移監控 | ✅/⚠️/❌ | Line N: ... |

**Total**: X/6 PASS — [PRODUCTION READY / NEAR READY / DRAFT]

## Defect Details

### ❌ FAIL — Criterion N: <name>
- **Location**: Line N
- **Defect**: [specific description]
- **Impact**: [why this matters in production]

### ⚠️ PARTIAL — Criterion N: <name>
- **Location**: Line N
- **Gap**: [what's present vs. what's missing]

## Recommended Next Step

[One sentence: specific action + which skill, e.g.,
"Add ≥2 negative trigger examples to `<what-to-do>` (line 30) via /s5-fix-optimize."]
```
