# s0-skill-budget — Detailed Reference

## Role Identity: Token Budget Auditor
- **Mindset**: 會計師。只數字，不主張。揭露缺口，不提供解法。
- **Upstream Dependency**: 任何 SKILL.md 路徑（新增或修改後）。
- **Downstream Target**: 用戶確認後，自行修正 SKILL.md 或 SKILL_INDEX.yaml。

## Semantic Boundary

| Skill | 評估什麼 | 此 skill 的差異 |
|-------|---------|----------------|
| `s0-eval-skill` | 6 項生產就緒標準（結構、語意邊界、測資） | 此 skill 只看 **token 加載成本**（D/I/S 三軸） |
| `s0-eval-alignment` | 設計意圖對齐度（批次掃描 28 個 skill） | 此 skill 單檔、聚焦加載成本；不看設計意圖 |
| `skill-creator` | 創建新 skill | 此 skill 審計已有草稿；不創建、不修改 |

## 建議使用時機

| 情境 | 使用方式 |
|------|---------|
| **新增 skill** | 完成 SKILL.md 草稿後，merge 前執行一次 |
| **修改 skill 功能** | 改動 `<what-to-do>` 後立即執行，確認 S 軸未超標 |
| **修改 description** | 改動後執行，確認 D1–D5 全部通過 |
| **擴充 SKILL_INDEX.yaml** | 新增 keyword 後執行，確認 I3 互斥性 |

## 與 s0-eval-skill 的搭配順序

新 skill 上線流程建議：
1. 草稿完成 → `/s0-skill-budget`（token 效率關卡）
2. 通過後 → `/s0-eval-skill`（結構品質關卡）
3. 兩者都 PASS → 合入

修改現有 skill 流程建議：
1. 改動完成 → `/s0-skill-budget`（快速；僅看改動影響面）
2. 若 Overall = FAIL → 修正後重跑
3. 確認 PASS/PARTIAL → 視需求決定是否跑完整 `/s0-eval-skill`

## Eval Fixtures

冒煙測試：以此 skill 對自身執行（`skills/s0-skill-budget/SKILL.md`）。
預期結果：Overall = PASS。若自評 FAIL，修正 SKILL.md，不修改評分標準。
