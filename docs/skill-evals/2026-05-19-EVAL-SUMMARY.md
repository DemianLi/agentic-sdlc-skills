# Skill Evaluation Summary — 2026-05-19

**Evaluator**: s0-eval-skill  
**Date**: 2026-05-19  
**Scope**: 4 Stage 1 Foundation Skills

---

## Results

| Skill | File | C1 | C2 | C3 | C4 | C5 | C6 | Total | Status |
|-------|------|----|----|----|----|----|----|-------|--------|
| s1-config-context | `skills/s1-config-context/SKILL.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 5/6 | NEAR READY |
| s1-define-rules | `skills/s1-define-rules/SKILL.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 5/6 | NEAR READY |
| s1-git-guardrails | `skills/s1-git-guardrails/SKILL.md` | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ❌ | 4/6 | DRAFT |
| s1-lock-tech-stack | `skills/s1-lock-tech-stack/SKILL.md` | ✅ | ✅ | ✅ | ✅ | ⚠️ | ❌ | 5/6 | NEAR READY |

**Legend**: C1=衝突防禦, C2=雙向阻斷, C3=輸入清洗, C4=漸進披露, C5=優雅降級, C6=漂移監控

---

## Cross-Skill Pattern: Criterion 6 Failure

**All 4 skills FAIL Criterion 6** (漂移監控 — Drift Monitoring).

- **Finding**: None of the skills reference `tests/fixtures/` directories. No offline eval fixture sets exist on disk.
- **Root Cause**: Criterion 6 requires explicit fixture references in SKILL.md AND fixture files on disk. This appears to be a project-wide pattern.
- **Risk**: Without offline fixtures, the entire Stage 1 suite cannot regression-test against LLM drift. Skills that bridge human-AI interaction (especially CONTEXT.md, RULES.md generation) are high-drift-risk.
- **Priority**: HIGH — should be addressed before any skill is shipped to production.

---

## Skill-Specific Summary

### s1-config-context (5/6) — NEAR READY
- **Strengths**: Clear anti-collision boundary (references s1-define-rules); comprehensive "Red Flags" with 3 concrete examples; well-structured input (domain terms) and completion states.
- **Single Gap**: Criterion 6 — no fixture set.
- **Fix Effort**: Medium — create 3–5 fixtures demonstrating correct glossary iteration vs. batch inference failure.

### s1-define-rules (5/6) — NEAR READY
- **Strengths**: Strong "Red Flags" (old rules, oversimplification, silent assumptions); explicit inputs (coding standards, architecture paradigm, security baseline); references downstream Stage 5 Code Auditor.
- **Single Gap**: Criterion 6 — no fixture set.
- **Fix Effort**: Medium — create 3–4 reference RULES.md files (e.g., TypeScript strict, Python Pydantic, hexagonal architecture) as regression baselines.

### s1-git-guardrails (4/6) — DRAFT
- **Strengths**: Clear "Red Flags" with 3 examples; explicit scope choice (project vs. global); comprehensive verification test procedure.
- **Gaps**:
  - **Criterion 3 (⚠️ PARTIAL)**: Scope input is collected but failure scenarios for invalid input (invalid choice, mkdir failure, settings.json parse error) are not explicitly handled.
  - **Criterion 5 (⚠️ PARTIAL)**: Multiple external dependencies (mkdir, cp, chmod, JSON parsing) without fallback paths. If settings.json is malformed or chmod fails, procedure offers no recovery guidance.
  - **Criterion 6 (❌)**: No fixture set — hook execution can drift silently.
- **Fix Effort**: High — add error handling for Steps 2-4; create fixtures for hook installation scenarios.

### s1-lock-tech-stack (5/6) — NEAR READY
- **Strengths**: Clear anti-collision routing to s3-design-arch; strong "Red Flags" (assumption of "latest", deferred compatibility, auto-dependency selection); well-separated Steps 0-4 with clear success criteria.
- **Gap (⚠️ PARTIAL in Criterion 5)**: Multiple write operations (lock files, ADR) assume success. If runtime version command fails, compatibility check stalls, or file write fails, procedure offers no fallback (e.g., alternative verification, manual input, try-again logic).
- **Single FAIL**: Criterion 6 — no fixture set.
- **Fix Effort**: Medium — add fallback guidance for write-phase failures; create 3–4 lock file and ADR fixtures as regression baselines.

---

## Recommended Priority Actions

1. **URGENT (Criterion 6 — all 4 skills)**:
   - Create `tests/fixtures/` directories for each skill.
   - Add fixture references to each SKILL.md file.
   - Populate with 3–5 representative fixtures per skill demonstrating correct vs. incorrect behavior.

2. **HIGH (s1-git-guardrails — Criterion 3 & 5)**:
   - Define failure scenarios for invalid user input (scope choice, parse errors).
   - Add fallback paths for file I/O operations (mkdir, settings.json parse, chmod).
   - Provide troubleshooting guidance in Completion Report.

3. **MEDIUM (s1-lock-tech-stack — Criterion 5)**:
   - Add fallback guidance for runtime version check (alternative verification if command fails).
   - Clarify what happens if user refuses to resolve compatibility issues (BLOCK status? manual override?).
   - Add recovery path for lock file write failures.

---

## Details

Full evaluation reports:
- `docs/skill-evals/2026-05-19-s1-config-context-eval.md`
- `docs/skill-evals/2026-05-19-s1-define-rules-eval.md`
- `docs/skill-evals/2026-05-19-s1-git-guardrails-eval.md`
- `docs/skill-evals/2026-05-19-s1-lock-tech-stack-eval.md`
