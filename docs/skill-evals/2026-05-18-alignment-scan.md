# Alignment Scan — 2026-05-18

Baseline: `references/skill-design-intent.md`
Skills scanned: 28 / 28 (s1–s7 pipeline skills)
Meta-skills excluded: s-fast-track, s0-brainstorm, s0-eval-alignment, s0-eval-skill, s0-trace-feature

---

## Overview Table

| Skill | Q | C1a | C1b/C1c | C2 | C3 | C4 | Status |
|-------|---|-----|---------|-----|-----|-----|--------|
| s1-config-context | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s1-define-rules | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s1-git-guardrails | ✅ ALIGNED | ✅ | ❌ intra | ✅ | ✅ | N/A | **DRIFTED** |
| s1-lock-tech-stack | ⚠️ PARTIAL 2/5 | ✅ | ✅ boundary | ✅ | ✅ | N/A | **PARTIAL** |
| s2-capture-vision | ⚠️ PARTIAL 1/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s2-align-req | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s2-struct-req | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s2-snapshot-ctx | ⚠️ PARTIAL 1/5 | ✅ | ✅ boundary | ✅ | ✅ | N/A | **PARTIAL** |
| s3-eval-system | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | ✅ | **ALIGNED** |
| s3-design-arch | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s3-breakdown-wbs | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s3-build-dag | ✅ ALIGNED | ✅ | ✅ boundary | ✅ | ✅ | N/A | **ALIGNED** |
| s4-setup-env | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s4-impl-task | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s4-tdd | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s4-local-debug | ⚠️ PARTIAL 2/5 | ✅ | ✅ boundary | ✅ | ✅ | N/A | **PARTIAL** |
| s5-sast-lint | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s5-audit-rules | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | ✅ | **PARTIAL** |
| s5-pr-review | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | ✅ | **PARTIAL** |
| s5-fix-optimize | ⚠️ PARTIAL 1/5 | ✅ | ✅ boundary | ✅ | ✅ | N/A | **PARTIAL** |
| s6-test-integration | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s6-test-e2e | ⚠️ PARTIAL 2/5 | ✅ | ✅ intra | ✅ | ✅ | N/A | **PARTIAL** |
| s6-test-perf | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s6-verify-release | ✅ ALIGNED | ✅ | ✅ boundary | ✅ | ✅ | ✅ | **ALIGNED** |
| s7-build-artifact | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ❌ "produces" | N/A | **DRIFTED** |
| s7-deploy | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s7-release-notes | ✅ ALIGNED | ✅ | ✅ intra | ✅ | ✅ | N/A | **ALIGNED** |
| s7-telemetry | ✅ ALIGNED | ✅ | ✅ boundary | ✅ | ✅ | N/A | **ALIGNED** |

Legend: ✅ PASS · ⚠️ PARTIAL/WARN · ❌ FAIL · N/A not applicable

---

## Summary

| Result | Count | Skills |
|--------|-------|--------|
| ALIGNED | 13 | s1-config-context, s2-struct-req, s3-eval-system, s3-design-arch, s3-build-dag, s4-impl-task, s4-tdd, s6-test-perf, s6-verify-release, s7-deploy, s7-release-notes, s7-telemetry, s7-build-artifact* |
| PARTIAL | 13 | s1-define-rules, s1-lock-tech-stack, s2-capture-vision, s2-align-req, s2-snapshot-ctx, s3-breakdown-wbs, s4-setup-env, s4-local-debug, s5-sast-lint, s5-audit-rules, s5-pr-review, s5-fix-optimize, s6-test-integration, s6-test-e2e |
| DRIFTED | 2 | s1-git-guardrails, s7-build-artifact |

*s7-build-artifact listed under ALIGNED above for Q but DRIFTED overall due to C3 failure.

---

## Drift List

### ❌ DRIFTED — Structural failures

**s1-git-guardrails** — C1c FAIL
- OUTPUT DISCIPLINE block says `"report that git-guardrails are now active and proceed"` — missing the required `"proceed immediately to /sX-Y"` pattern
- Root cause: this skill has no single downstream skill (it's a setup tool that can be run standalone), so the auto-proceed routing was never added
- Fix: either (a) add `"proceed immediately to /s1-lock-tech-stack"` if it always feeds s1, or (b) reclassify as a standalone utility like s0-* skills and exclude from intra-stage C1c check

**s7-build-artifact** — C3 FAIL
- Description: `"Use after /s6-verify-release **produces** test-results.json"`
- `"produces"` triggers the forbidden-process-word filter — but here it describes the upstream skill's output, not s7-build-artifact's own workflow
- This is a **false positive** in the C3 scanner: the word appears in a qualifying clause describing a dependency, not as a process-description of this skill
- Fix: rephrase to `"Use after /s6-verify-release generates test-results.json with release_gate: PASS"` — wait, "generates" is also forbidden. Better: `"Use after /s6-verify-release writes test-results.json with release_gate: PASS"`

---

### ⚠️ PARTIAL — Q keyword mismatches (language gap)

The following 13 skills have Q=PARTIAL because the keyword list in `skill-design-intent.md` uses Chinese terms but the actual skill content uses English equivalents. **This is largely a baseline calibration issue, not content drift.**

Confirmed language-gap cases (skill content is aligned in English; Chinese keyword absent):

| Skill | Missing Chinese keywords | English equivalent present in SKILL.md |
|-------|--------------------------|------------------------------------------|
| s1-define-rules | 編碼規範, 架構範式, 安全性 | coding standards, architecture, security ✓ |
| s1-lock-tech-stack | 技術棧, 語言版本, 鎖定 | tech stack, language version, lock ✓ |
| s2-capture-vision | 構思, 業務, 痛點, 需求 | vision, business, pain point, requirement ✓ |
| s2-align-req | 對齊, 澄清, 共識 | align, clarify, consensus ✓ |
| s2-snapshot-ctx | 快照, 沉澱, 迭代 | snapshot, context, iteration ✓ |
| s3-breakdown-wbs | 原子, 拆解, 獨立 | atomic, decompose, independent ✓ |
| s4-setup-env | 工作區, 初始化, 沙盒 | workspace, initialize, sandbox ✓ |
| s4-local-debug | 調試, 堆疊追蹤, 復現 | debug, stack trace, reproduce ✓ |
| s5-sast-lint | 靜態, 安全性, 漏洞 | static analysis, security, vulnerability ✓ |
| s5-audit-rules | 合規, 架構範式, 違規 | compliance, architecture paradigm, violation ✓ |
| s5-pr-review | 評審, 重構, breaking change | review, refactor (need to verify) |
| s5-fix-optimize | 修復, regression, 重構, 迭代 | fix, regression, refactor, iteration ✓ |
| s6-test-integration | 接口, 模組, contract | interface, module, contract ✓ |
| s6-test-e2e | 端到端, 用戶行為, 邊界條件 | end-to-end, user flow, edge case ✓ |

**Recommended baseline fix**: Update keyword lists in `skill-design-intent.md` to use English (or bilingual) keywords. Example: `s2-capture-vision` keywords → `vision`, `pain point`, `business`, `requirement`, `problem statement`.

---

## Check Failures (C1–C4)

- **C1a FAIL**: none — all 28 skills have `<HARD-GATE>`
- **C1b FAIL**: none — all 7 boundary skills have "Awaiting your approval"
- **C1c FAIL**: `s1-git-guardrails` (missing "proceed immediately to")
- **C2 FAIL**: none — all skills declare Reads and Writes
- **C3 FAIL**: `s7-build-artifact` (description contains "produces" — likely false positive, see notes above)
- **C4 FAIL**: none — all 4 required skills have red-flag tables

---

## Known Deviations (matched from `references/skill-design-intent.md` Part 3)

- **s3-eval-system Step 5c contradiction**: HARD-GATE says "proceed immediately to /s3-design-arch" but Step 5c body says "Wait for explicit approval before proceeding." → Not counted as a failure in this scan (listed as known deviation), but should be resolved to avoid agent confusion.
- **s1-config-context Reads: none**: Intentional — this is the first skill in the pipeline with no upstream artifact.

---

## Priority Fixes (ordered by pipeline impact)

1. **s1-git-guardrails C1c** — Add `"proceed immediately to /s1-define-rules"` (or reclassify as standalone utility) to restore auto-proceed discipline. Risk: without it, AI may stop and await approval unnecessarily at an intra-stage step.

2. **s7-build-artifact C3** — Rephrase description to avoid "produces": `"Use after /s6-verify-release writes test-results.json with release_gate: PASS"`. Low effort, prevents future false positives from tooling that scans descriptions.

3. **Baseline keyword calibration** — Update 13 keyword entries in `references/skill-design-intent.md` from Chinese-only to bilingual. Q=PARTIAL is noise right now, masking real drift if it occurs. Recommended: add English variants alongside Chinese for each PARTIAL skill.

4. **s3-eval-system Step 5c body text** — Remove or reconcile "Wait for explicit approval before proceeding" in Step 5c to match the HARD-GATE "proceed immediately" intent. This is the only known intra-document contradiction in the codebase.

5. **s5-pr-review Q check** — Verify that English equivalents of '評審', '重構', 'breaking change' are present (likely yes — confirm and add to bilingual keyword list if so).

---

## Meta-Skills (excluded from scan)

| Skill | Reason |
|-------|--------|
| s-fast-track | Routing meta-skill; no QA substep counterpart |
| s0-brainstorm | Pre-pipeline ideation |
| s0-eval-alignment | Self-referential — cannot scan itself |
| s0-eval-skill | Single-skill structural auditor |
| s0-trace-feature | Cross-cutting tracer |
