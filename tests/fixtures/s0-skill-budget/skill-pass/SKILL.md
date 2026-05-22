---
name: fixture-skill-pass
description: >
  Use when deploying a service — outputs deployment log.
  NOT for build steps (use s7-build-artifact).
---

<HARD-GATE>
Do NOT modify any infrastructure during this audit fixture.
After completing, your message MUST end with:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

You are the **Fixture Deploy Role**. This skill is a token-budget audit fixture only.

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶要真正部署 | `s7-deploy` |
| 用戶要建構產物 | `s7-build-artifact` |

### Step 0 — Input Validation

接受唯一輸入：`target_env`（字串，值為 staging 或 production）。

| 失敗情境 | 行為 |
|---------|------|
| 未提供 target_env | BLOCKED — 「請指定部署目標環境。」|
| 值不為 staging 或 production | BLOCKED — 「預期 staging 或 production，實際為 `<value>`。」|

### Step 1 — Execute

模擬部署流程並輸出結果。

### Step 2 — Present and Wait

呈現部署摘要，等待確認。

</what-to-do>

<supporting-info>

## Semantic Boundary

| Skill | 用途 | 此 skill 的差異 |
|-------|------|----------------|
| `s7-deploy` | 真實部署 | 此 fixture 僅供 s0-skill-budget 冒煙測試 |

## Artifact Dependencies
- **Reads**: `target_env`（用戶提供）
- **Writes**: 無

</supporting-info>
