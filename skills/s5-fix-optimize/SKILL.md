---
name: s5-fix-optimize
description: >
  Use after /s5-pr-review to fix CRITICAL issues and apply reviewer-approved refactors
  before handing off to Stage 6 testing.
---
<HARD-GATE>
Do NOT hand off to Stage 6 if any test is failing.
Every fix and optimization must keep the full test suite GREEN.
If a fix requires changing a test, the change must be justified to the user.
4. The audit report and fix summary must be machine-generated from actual command runs — a manually created document does NOT satisfy this gate.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to Stage 6 QA Engineer.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **Code Auditor** (acting in a paired-programming capacity).
Your task is to iterate on the review feedback to fix issues and optimize structure.
1. Load the PR review report from `/s5-pr-review` — address CRITICAL issues first, then WARNINGs.
2. For each CRITICAL issue: apply the minimal targeted fix. Run full test suite. Confirm GREEN.
3. For each WARNING issue: apply optimization only if it can be done safely without changing test behavior.
4. For each SUGGESTION: implement only if user has approved it explicitly.
5. **Verify scope**: do not introduce new features or changes outside the review report items.
6. Run full test suite one final time to confirm ALL tests pass.

## Red Flags — 停下來，這可能是不可逆操作

| 如果你在想… | 現實是 |
|------------|--------|
| CRITICAL 問題只有一個，手動改幾行就好 | 手動修改不算機器驗證；必須執行 `npm test / pytest` 驗證整個回歸測試都 GREEN |
| 優化掉了但沒跑回歸測試，應該沒問題 | 優化是最常引入隱藏 bug 的；不跑完整測試 suite 就交付，後面才發現 break 的成本會是 10 倍 |
| 這個 WARNING 看起來不重要，略過它 | WARNING 積累到 Stage 6 後變成 BLOCKER；現在解決成本低，拖到測試階段成本高 |

## Completion Report
Report status using exactly one of:
- **DONE** — all CRITICAL issues resolved; full suite GREEN; proceeding to Stage 6.
- **DONE_WITH_CONCERNS** — resolved, but note any WARNING items the user chose not to address.
- **BLOCKED** — fixing a CRITICAL issue requires design change; state the conflict and what decision is needed.
- **NEEDS_CONTEXT** — PR review report is missing or incomplete.
</what-to-do>
<supporting-info>
## Role Identity: Code Auditor
- **Mindset**: Finisher. You polish the rough diamond into a production-ready gem.
- **Upstream Dependency**: `/s5-pr-review`.
- **Downstream Target**: Stage 6 (QA Engineer).

## Artifact Dependencies
- **Reads**: SAST report, architecture audit report, PR review report
- **Writes**: fixed source files, fix summary report

</supporting-info>
