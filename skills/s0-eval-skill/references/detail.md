# s0-eval-skill: Detailed Reference

## Role Identity: Skill Quality Inspector
- **Mindset**: 審計員，不是編輯。你揭露缺口，不提供解法。Auditor, not editor. Diagnose, don't fix.
- **Upstream Dependency**: 任何用戶提供的 SKILL.md 路徑。Any user-provided SKILL.md path.
- **Downstream Target**: `/s5-fix-optimize` — 但只在用戶選擇行動後。Only after user chooses action.

## Semantic Boundary

與相鄰 skill 的明確區分 (Distinction from adjacent skills):

| Skill | 評估對象 | 此 skill 的差異 |
|-------|----------|----------------|
| `/s3-eval-system` | 軟體系統的架構與爆炸半徑 | 此 skill 評估 *skill 文件的生產就緒度* |
| `/s5-audit-rules` | 原始碼對 RULES.md 的合規性 | 此 skill 評估 *skill 元資料的 6 項 QA 標準* |
| `skill-creator` | 創建新 skill | 此 skill 審計現有 skill |
| `/s0-brainstorm` | 發散探索問題領域 | 此 skill 對具體檔案打分，有確定性輸出 |

## Eval Fixtures

Fixtures 位於 `tests/fixtures/`；預期輸出位於 `tests/expected/`。

**冒煙測試**：以此 skill 評估自身（`s0-eval-skill/SKILL.md`）是標準基線測試。若自評得分 < 6/6 PASS，回去修改 SKILL.md，不修改評分標準。
