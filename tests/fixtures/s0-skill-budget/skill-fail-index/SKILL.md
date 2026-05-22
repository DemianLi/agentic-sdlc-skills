---
name: fixture-skill-not-in-index
description: >
  Use when testing index coverage — outputs nothing real.
  NOT for production use.
---

<HARD-GATE>
Do NOT use in production.
After completing, your message MUST end with:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

### Step 0 — Input Validation

接受輸入：`topic`。

| 失敗情境 | 行為 |
|---------|------|
| 未提供 topic | BLOCKED — 「請提供 topic。」|

### Step 1 — Execute

執行並輸出結果。

</what-to-do>

<supporting-info>

## Artifact Dependencies
- **Reads**: `topic`（用戶提供）
- **Writes**: 無

</supporting-info>
