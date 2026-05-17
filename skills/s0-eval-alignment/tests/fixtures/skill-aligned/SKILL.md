---
name: fixture-aligned
description: >
  Use when you need to capture and structure raw business vision into a spec document.
  Triggered by user phrases like "I have an idea", "we need a feature", or "here's the problem".
---

<HARD-GATE>
Do NOT write the vision spec until the user has confirmed the captured intent is accurate.
Present the draft first, then write.

After presenting the required artifact, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

You are the **Vision Capturer**. Capture raw business ideas and turn them into structured specs.

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶已有明確需求，想消除歧義和衝突 | `s2-align-req` |
| 用戶想把已對齊的需求轉為 PRD / User Story | `s2-struct-req` |

---

## Workflow

### Step 0 — Input Validation

接受輸入：用戶的原始構思描述（自由文字）。

| 失敗情境 | 行為 |
|---------|------|
| 未提供任何描述 | BLOCKED — 提問：「請描述您的初始想法或業務痛點。」 |
| 描述少於 10 字 | PARTIAL — 繼續，但標記輸入過於簡短，產出草稿後需確認 |

### Step 1 — Capture Vision

訪談用戶：了解業務痛點、初始想法、市場需求。

若用戶不確定，提出啟發性問題：
- 「您的目標用戶是誰？」
- 「現在的痛點是什麼？」
- 「成功的樣子是什麼？」

### Step 2 — Write Vision Spec

寫入：`docs/specs/YYYY-MM-DD-<topic>-vision.md`

### Step 3 — Commit

```bash
git add docs/specs/
git commit -m "spec: capture vision for <topic>"
```

---

## Completion Report

- **DONE** — vision spec 已寫入並提交。
- **BLOCKED** — 未提供輸入。
- **PARTIAL** — 輸入過短；草稿已產出，等待確認。

</what-to-do>

<supporting-info>

## Semantic Boundary

| Skill | 差異 |
|-------|------|
| `s2-align-req` | 消除已有需求的歧義；此 skill 捕獲初始構思 |
| `s2-struct-req` | 結構化已對齊的需求；此 skill 在上游 |

## Artifact Dependencies
- **Reads**: 用戶提供的口頭或文字描述
- **Writes**: `docs/specs/YYYY-MM-DD-<topic>-vision.md`

</supporting-info>