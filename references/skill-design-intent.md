# Skill Design Intent — Evaluation Baseline

Source of truth: `QA.md` (7-stage, 4-substep SDLC outline)
Last updated: 2026-05-18

---

## Part 1 — Cross-Skill Pattern Checks (C1–C4)

These checks apply to **all s1–s7 skills** unless noted.

---

### C1a — HARD-GATE Block Exists

Every s1–s7 skill must contain a `<HARD-GATE>` block.

| Result | Condition |
|--------|-----------|
| PASS | `<HARD-GATE>` tag present in SKILL.md |
| FAIL | tag absent |

---

### C1b — Stage-Boundary Approval Gate

The following 7 skills sit at **stage transitions** and must contain `"Awaiting your approval"` inside their `<HARD-GATE>` OUTPUT DISCIPLINE block. They are the only checkpoints requiring explicit human sign-off.

| Skill | Transition |
|-------|-----------|
| s1-lock-tech-stack | S1 → S3 |
| s2-snapshot-ctx | S2 → S3 |
| s3-build-dag | S3 → S4 |
| s4-local-debug | S4 → S5 |
| s5-fix-optimize | S5 → S6 |
| s6-verify-release | S6 → S7 |
| s7-telemetry | End of cycle |

| Result | Condition |
|--------|-----------|
| PASS | `"Awaiting your approval"` present in HARD-GATE |
| FAIL | absent (intra-stage proceed pattern found instead) |

---

### C1c — Intra-Stage Auto-Proceed Pattern

All other s1–s7 skills (not in the C1b list, not in the C1-exempt list below) must contain `"proceed immediately to"` in their HARD-GATE OUTPUT DISCIPLINE block, and must NOT contain `"Awaiting your approval"`.

**C1-exempt standalone utilities** — these skills are invocable at any pipeline point and have no fixed downstream skill. They must have `<HARD-GATE>` (C1a) but are excluded from C1b and C1c routing checks:

| Skill | Reason |
|-------|--------|
| s1-git-guardrails | Safety-rail tool: "any time a project needs safety rails" (description); no fixed downstream |

| Result | Condition |
|--------|-----------|
| PASS | `"proceed immediately to /sX-Y"` present, `"Awaiting your approval"` absent |
| FAIL | `"Awaiting your approval"` found (approval-gate leak), or neither pattern present |
| EXEMPT | Skill is in the C1-exempt standalone utilities list |

---

### C2 — Artifact Chain Declared

`<supporting-info>` section must declare both:
- `**Reads**:` — what the skill consumes
- `**Writes**:` — what the skill produces

| Result | Condition |
|--------|-----------|
| PASS | Both `**Reads**` and `**Writes**` present under `## Artifact Dependencies` |
| FAIL | Either declaration missing |

---

### C3 — Description Field Is Trigger Language

`description:` frontmatter must use "Use when/after/at/before/during" trigger language.
It must NOT contain process-description vocabulary.

**Forbidden patterns (any match = C3 FAIL):**
`Step`, `Workflow`, `->`, ` produces `, ` generates `, ` runs `, ` executes `

| Result | Condition |
|--------|-----------|
| PASS | description opens with "Use when/after/at/before/during" AND no forbidden patterns |
| FAIL | description contains forbidden patterns (process summary, not trigger) |

---

### C4 — Red-Flag Table (High-Stakes Skills Only)

The following 4 skills handle irreversible or externally-visible decisions and MUST contain a Red Flag table:

`s3-eval-system`, `s5-audit-rules`, `s5-pr-review`, `s6-verify-release`

| Result | Condition |
|--------|-----------|
| PASS | Contains "Red Flag" OR "紅旗" OR "停下來" near a markdown table (`|`) |
| FAIL | None of those patterns found |
| N/A | Skill not in the required list (skip check) |

---

## Part 2 — Per-Skill QA Step Mapping & Keywords

The **Q check** counts how many keywords from the list below appear in the skill's full SKILL.md text.
- ✅ ALIGNED: ≥ 3 keywords found
- ⚠️ PARTIAL: 1–2 keywords found
- ❌ DRIFTED: 0 keywords found

Keywords are drawn directly from the QA.md description for each corresponding substep.

---

### Stage 1 — Initialization & Base Rules

**s1-define-rules** → QA 1.1 項目根本規則定義
Keywords: `RULES.md`, `編碼規範`, `Lint`, `架構範式`, `安全性`

**s1-config-context** → QA 1.2 基礎上下文配置
Keywords: `CONTEXT.md`, `上下文`, `AI 代理`, `邊界`, `詞彙`

**s1-git-guardrails** → QA 1.2 (supporting — repo safety baseline)
Keywords: `Git`, `.gitignore`, `branch`, `hook`, `保護`

**s1-lock-tech-stack** → QA 1.3 技術棧與依賴鎖定
Keywords: `技術棧`, `依賴`, `語言版本`, `框架`, `鎖定`

---

### Stage 2 — Requirement Alignment

**s2-capture-vision** → QA 2.1 原始構思捕獲
Keywords: `構思`, `業務`, `痛點`, `需求`, `vision`

**s2-align-req** → QA 2.2 需求對齊與衝突消除
Keywords: `對齊`, `衝突`, `邊界`, `澄清`, `共識`

**s2-struct-req** → QA 2.3 需求結構化描述
Keywords: `REQ`, `AC`, `acceptance criterion`, `結構化`, `標準化`

**s2-snapshot-ctx** → QA 2.4 文檔沉澱與快照
Keywords: `CONTEXT_SNAPSHOT`, `快照`, `沉澱`, `迭代`

---

### Stage 3 — Architecture & Breakdown

**s3-eval-system** → QA 3.1 現有系統評估
Keywords: `blast radius`, `impact`, `影響`, `Schema`, `API`

**s3-design-arch** → QA 3.2 技術方案設計
Keywords: `ADR`, `技術方案`, `API Contract`, `架構`, `設計`

**s3-breakdown-wbs** → QA 3.3 原子化任務拆解
Keywords: `WBS`, `原子`, `atomic`, `拆解`, `獨立`

**s3-build-dag** → QA 3.4 依賴拓撲建立
Keywords: `DAG`, `依賴`, `拓撲`, `有向無環圖`, `順序`

---

### Stage 4 — Implementation & Local Debug

**s4-setup-env** → QA 4.1 研發環境就緒
Keywords: `環境`, `工作區`, `branch`, `沙盒`, `初始化`

**s4-impl-task** → QA 4.2 原子任務並發實現
Keywords: `業務邏輯`, `原子任務`, `實現`, `acceptance criterion`, `minimal`

**s4-tdd** → QA 4.3 單元測試同步編寫
Keywords: `TDD`, `coverage`, `單元測試`, `可測性`, `brownfield`

**s4-local-debug** → QA 4.4 本地編譯與微調試
Keywords: `調試`, `堆疊追蹤`, `根因`, `復現`, `hypothesis`

---

### Stage 5 — Code Review & Verification

**s5-sast-lint** → QA 5.1 靜態代碼分析
Keywords: `SAST`, `Lint`, `靜態分析`, `安全性`, `漏洞`

**s5-audit-rules** → QA 5.2 根本規則合規審查
Keywords: `合規`, `RULES.md`, `架構範式`, `違規`, `compliance`

**s5-pr-review** → QA 5.3 代碼評審與意見反饋
Keywords: `PR`, `評審`, `重構`, `breaking change`, `代碼審查`

**s5-fix-optimize** → QA 5.4 排障與結構優化
Keywords: `修復`, `優化`, `regression`, `重構`, `迭代`

---

### Stage 6 — Dynamic Testing

**s6-test-integration** → QA 6.1 自動化整合測試
Keywords: `整合測試`, `integration`, `接口`, `模組`, `contract`

**s6-test-e2e** → QA 6.2 端到端與邊界驗證
Keywords: `E2E`, `端到端`, `用戶行為`, `邊界條件`, `Playwright`

**s6-test-perf** → QA 6.3 效能與壓力測試
Keywords: `P50`, `P95`, `P99`, `throughput`, `SLO`

**s6-verify-release** → QA 6.4 結果最終驗證
Keywords: `release gate`, `coverage`, `traceability`, `PASS`, `BLOCKED`

---

### Stage 7 — Delivery & Iteration

> Note: QA.md numbers 7.2 = Release Notes, 7.3 = Deploy. The skill pipeline order is
> build → deploy → release-notes → telemetry, which differs from QA numbering. Both mappings
> are recorded here for traceability.

**s7-build-artifact** → QA 7.1 構建與封裝
Keywords: `artifact`, `SHA-256`, `構建`, `封裝`, `版本`

**s7-deploy** → QA 7.3 生產環境部署
Keywords: `部署`, `smoke test`, `dry-run`, `rollout`, `生產`

**s7-release-notes** → QA 7.2 變更日誌沉澱
Keywords: `CHANGELOG`, `變更日誌`, `commit`, `release notes`, `版本`

**s7-telemetry** → QA 7.4 運維監控與反饋閉環
Keywords: `telemetry`, `next_cycle_inputs`, `anomaly`, `rollback`, `反饋`

---

### Meta-Skills (not mapped to QA steps — excluded from main scan)

| Skill | Reason |
|-------|--------|
| s-fast-track | Routing meta-skill; no QA substep counterpart |
| s0-brainstorm | Pre-pipeline ideation; no QA substep counterpart |
| s0-eval-alignment | Self-referential eval tool; cannot scan itself |
| s0-eval-skill | Single-skill structural auditor |
| s0-trace-feature | Cross-cutting tracer; not a pipeline stage |

---

## Part 3 — Known Deviations

Record confirmed intentional or accepted deviations so the scanner does not report them as regressions.

| Skill | Check | Deviation | Accepted? |
|-------|-------|-----------|-----------|
| s3-eval-system | C1c | Step 5c body says "Wait for explicit approval" but HARD-GATE says "proceed immediately" | ⚠️ Unresolved contradiction — body text not updated with overhaul |
| s1-config-context | C2 | **Reads**: none — this is correct (s1-config-context has no upstream artifact) | ✅ Intentional |
| s1-git-guardrails | C1c | Does not contain "proceed immediately to" — intentional; classified as standalone utility (see C1-exempt list above) | ✅ Resolved 2026-05-18 |

---

## Part 4 — Report Template

Scanner output must be written to `docs/skill-evals/YYYY-MM-DD-alignment-scan.md`.
Use this template exactly.

```markdown
# Alignment Scan — YYYY-MM-DD

Baseline: `references/skill-design-intent.md`
Skills scanned: N / 28

## Overview Table

| Skill | Q | C1a | C1b/C1c | C2 | C3 | C4 | Status |
|-------|---|-----|---------|-----|-----|-----|--------|
| s1-config-context | ✅ | ✅ | ✅ | ✅ | ✅ | N/A | ALIGNED |
| ... | | | | | | | |

Legend: ✅ PASS · ⚠️ PARTIAL/WARN · ❌ FAIL · N/A not applicable

## Drift List

### ❌ DRIFTED (Q = 0)
- **s_-_____**: missing keywords: [list them]

### ⚠️ PARTIAL (Q = 1–2 or C-check warnings)
- **s_-_____**: found [N] keyword(s) ([found]), missing: [list absent]

## Check Failures
- **C1a FAIL**: [skill list]
- **C1b FAIL**: [boundary skill list]
- **C1c FAIL**: [intra-stage skill list]
- **C2 FAIL**: [skill list]
- **C3 FAIL**: [skill list with offending word]
- **C4 FAIL**: [skill list]

## Known Deviations (from Part 3 — not counted as failures)
- [list any matched deviations]

## Priority Fixes (≤5, ordered by impact)
1. ...

## Meta-Skills (excluded from scan)
s-fast-track, s0-brainstorm, s0-eval-alignment, s0-eval-skill, s0-trace-feature
```
