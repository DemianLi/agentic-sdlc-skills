---
name: example-fixture-skill
description: >
  Use when demonstrating all 6 production-quality criteria for s0-eval-skill
  smoke testing. Do NOT use in real SDLC workflows.
---

<HARD-GATE>
Do NOT use this skill in production routing.
After completing, your message MUST end with:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

You are the **Fixture Skill**. This skill exists only as a baseline test case for `s0-eval-skill`.

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶要執行任何真實 SDLC 工作 | 對應的 s1–s7 skill |
| 用戶要建立新的 skill | `skill-creator` |

## Workflow

### Step 0 — Input Validation

接受唯一輸入：`topic`（字串）。

| 失敗情境 | 行為 |
|---------|------|
| 未提供 topic | BLOCKED — 「請提供 topic。」 |
| topic 為空字串 | BLOCKED — 「topic 不可為空。」 |
| topic 非字串型別 | BLOCKED — 「預期字串，實際為 `<type>`。」 |

### Step 1 — Process

讀取 topic。若無法讀取 → BLOCKED，說明確切原因後停止。

### Step 2 — Present and Wait

呈現結果。等待明確批准，不自動進入下一階段。

</what-to-do>

<supporting-info>

## Semantic Boundary

| Skill | 用途 | 此 skill 的差異 |
|-------|------|----------------|
| s1–s7 skills | 真實 SDLC 流程 | 此 skill 僅為 s0-eval-skill 的測試 fixture，無生產功能 |

## Eval Fixtures

Fixtures 位於 `tests/fixtures/`；預期輸出位於 `tests/expected/`。

## Artifact Dependencies
- **Reads**: `topic`（用戶提供）
- **Writes**: nothing

</supporting-info>
