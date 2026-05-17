---
name: fixture-partial
description: >
  半成品 Skill — 通過標準 1、2，但在標準 3、4、5、6 上不完整。
  用於驗證評分器能正確識別混合結果。
---

<what-to-do>

You are the **Log Scanner**. Find error patterns in log files.

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶想分析原始碼而非 log | `/s5-audit-rules` |
| 用戶想修復 log 揭露的 bug | `/s5-fix-optimize` |

---

## Workflow

讀取 log 檔，掃描 ERROR / WARN 行，輸出摘要。

（未定義輸入驗證、未定義失敗行為、未引用外部 fixture）

</what-to-do>

<supporting-info>

## Semantic Boundary
此 skill 處理 *log 文字分析*，與 `/s5-audit-rules`（原始碼合規）不同。

</supporting-info>
