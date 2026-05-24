---
name: s5-pr-review
description: >
  Use when reviewing PRs for correctness. Outputs severity-graded findings with scope
  drift detection. NOT for linting. Blocks on CRITICAL issues.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s5-pr-review`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT proceed to `/s5-fix-optimize` if ANY CRITICAL issue remains unresolved.
CRITICAL issues are blocking. The PR cannot merge until they are fixed.

Hotfix Mode exception: if the current session was declared Hotfix Mode by `/s-fast-track`
(the `🔧 Hotfix Mode` announcement appears in conversation history), WARNING items are
informational only — not blocking. Run a simplified review (see Step 0).

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s5-fix-optimize.
Do NOT skip /s5-fix-optimize’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

**Code Auditor (peer review)**: Review like senior engineer—concrete, specific, actionable. Name files, functions, line numbers. No vague "consider improving"; state exact fix.

## Workflow

### Step 0 — Input Validation
**Required**: git diff, TASK_DAG.md, SAST report. If any missing → `NEEDS_CONTEXT`. Design doc optional (warning only).

---

### Step 0b — Mode Check
**Standard**: all steps (Scope Drift → Logic → Security), full report. **Hotfix Mode** (from /s-fast-track): Steps 1+3 only, CRITICAL checks in step 2, no SUGGESTION, WARNINGs non-blocking.

---

### Step 1 — Scope Drift Detection
Read TASK_DAG.md, commit messages, git diff. Compare changed files against task scope. Flag if files have no corresponding task or features not in scope. CRITICAL before other checks.

### Step 2 — Logic Review
Check: API contract match, error handling, edge cases without tests, naming (CONTEXT.md), N+1 queries, race conditions (read-then-write), stale cache, trust boundaries, enum handlers.

### Step 3 — Security Spot-Check
Check: input validation, parameterized queries, env-only secrets, authorization on protected endpoints.

### Step 4 — Format Report
Sections: Scope Drift (CLEAN/DETECTED), Overall Status (APPROVED/CHANGES REQUIRED), CRITICAL/WARNING/SUGGESTION with file:line, issue, fix. Hotfix Mode: simplified, WARNINGs non-blocking. No CRITICALs → "✅ APPROVED". Present and wait for acknowledgment.

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| test 都過了，代碼應該沒有問題 | 測試通過不代表代碼審查通過。測試只驗證了你的假設；審查驗證你的假設是否完整。競態條件、N+1 查詢、邊界情況經常在測試通過後才被發現。 |
| 這只是小改動，不需要完整的 review | 「小改動」產生的 bug 並不比「大改動」的小。五行代碼可能比五千行代碼更危險。每一個改動都要 scope drift check。 |
| 代碼看起來合理，我會跳過檢查清單 | 檢查清單存在就是為了防止「看起來合理」的假象。跳過任何一項（特別是 scope drift、race condition、trust boundary），就等於放棄了這個 stage 的責任。 |

---

## Completion Report

Report status using exactly one of:
- **DONE** — APPROVED: no CRITICAL issues; WARNING items noted; user acknowledged. Proceeding to `/s5-fix-optimize`.
- **DONE_WITH_CONCERNS** — CHANGES REQUIRED: list all CRITICAL issues; blocked until fixed.
- **BLOCKED** — scope drift detected that requires re-scoping at Stage 3 level; state the issue.
- **NEEDS_CONTEXT** — design doc not found; cannot validate scope; state what is missing.

</what-to-do>

<supporting-info>

Output: `docs/audit/YYYY-MM-DD-<branch>-pr-review.md` with Scope Drift status, Overall Status, CRITICAL/WARNING/SUGGESTION, Confirmed Good. Severity: CRITICAL (correctness/security/scope/contract), WARNING (perf/error/naming), SUGGESTION (optional).

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: git diff, TASK_DAG.md, `docs/arch/YYYY-MM-DD-<topic>-design.md`
- **Writes**: PR review report

</supporting-info>
