# s0-semantic-validate — Detailed Reference

## Role Identity: Semantic Evidence Verifier
- **Mindset**: 法證人員。只看物理證據，不接受口頭聲稱。工件必須自證其完成狀態。
- **Upstream Dependency**: `skill_graph_schema.yaml` 的 `validators` 欄位 + 對應工件檔案。
- **Downstream Target**: 通過後，下游節點可標記為可觸發；失敗則下游被物理阻斷。

## Semantic Boundary

| Skill | 評估什麼 | 此 skill 的差異 |
|-------|---------|----------------|
| `s0-eval-skill` | Skill 的 6 項生產就緒標準（結構、語意邊界） | 此 skill 驗證**工件內容**（JSON 值、regex、mtime），不看 Skill 文件結構 |
| `s0-eval-alignment` | 設計意圖漂移（批次掃描） | 此 skill 驗證單一**執行工件**是否語意正確；不看設計意圖 |
| `s0-skill-budget` | Token 加載成本（D/I/S 三軸） | 此 skill 完全關注**工件真偽**，不計算 token |

## 與 ADR-001 的關係

本 Skill 是 ADR-001（語意驗證設計）的**執行契約**。
設計文件：`docs/v3-architecture/ADR-001-semantic-validation.md`

## Artifact Dependencies
- **Reads**: `skill_graph_schema.yaml`（validators 欄位）、待驗證工件（用戶提供路徑）
- **Writes**: 無（僅 chat 輸出）

## Eval Fixtures

冒煙測試（在 workspace 目錄執行）：
```bash
# 以語意失敗工件測試（期望：BLOCKED）
echo '{"summary": {"failed": 1}}' > /tmp/test-results.json
# 以語意成功工件測試（期望：VALIDATED）
echo '{"summary": {"failed": 0}}' > /tmp/test-results.json
```
