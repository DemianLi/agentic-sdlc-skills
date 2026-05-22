---
name: fixture-skill-fail-description
description: >
  This skill is used when you want to perform a Step-by-step Workflow for
  deploying services to production environments. It will guide you through
  the entire deployment pipeline including build, test, and release phases
  using a structured multi-stage approach -> final output is a deployed service.
---

<HARD-GATE>
Do NOT modify any infrastructure during this audit fixture.
After completing, your message MUST end with:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

### Step 0 — Input Validation

接受輸入：`target_env`。

| 失敗情境 | 行為 |
|---------|------|
| 未提供 target_env | BLOCKED |

### Step 1 — Execute

執行部署。

</what-to-do>

<supporting-info>

## Artifact Dependencies
- **Reads**: `target_env`（用戶提供）
- **Writes**: 無

</supporting-info>
