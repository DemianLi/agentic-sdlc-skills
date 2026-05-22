---
name: s0-semantic-validate
description: >
  Use when an artifact exists but content correctness is unverified — semantic gate (json_query /
  regex_match / file_hash); outputs VALIDATED or BLOCKED. NOT structural audit (s0-eval-skill)
  or token check (s0-skill-budget).
---

<HARD-GATE>
Do NOT mark any node as COMPLETED without running validators.
Do NOT create or modify artifact files during this check.
Do NOT auto-trigger downstream skills.
Output: one status block per node in chat. No file written.

After presenting the report, your message MUST end with exactly:
  "Awaiting your approval to proceed."
</HARD-GATE>

<what-to-do>

You are the **Semantic Evidence Verifier**. Three checks. No edits. One output block.

> **設計狀態**: 本 Skill 為 P1 設計骨架。validators 執行機制（SemanticValidator 類別）待
> `engine.py` P1 PR 實作後生效。目前 `--mode strict` 下會輸出 `[SemanticValidationWarning]`
> 警告但不阻斷執行，直到 P1 PR 合入。

---

### 絕對不要觸發的情境

| 情境 | 正確技能 |
|------|----------|
| 用戶想評估 skill 的生產就緒度（結構、測資） | `s0-eval-skill` |
| 用戶想批次掃描設計意圖漂移 | `s0-eval-alignment` |
| 用戶想檢查 token 加載成本 | `s0-skill-budget` |
| 用戶想執行 V3.0 架構文件討論 | 直接閱讀 `docs/v3-architecture/` |
| 工件檔案完全不存在 | 這是 BLOCKED，不是語意失敗；回報 `NEEDS_CONTEXT` |

---

### Step 0 — Input Validation

接受輸入：`node_id`（skill graph 節點 ID，如 `s4-tdd`）或 `artifact_path`（待驗證工件路徑）。

| 失敗情境 | 行為 |
|---------|------|
| 兩者都未提供 | BLOCKED — 「請提供 node_id 或 artifact_path。」 |
| node_id 不在 schema 中 | BLOCKED — 「`<node_id>` 不存在於 skill_graph_schema.yaml。」 |
| artifact_path 不存在 | BLOCKED (NEEDS_CONTEXT) — 「工件不存在，無法語意驗證。」 |
| node_id 無 validators 欄位 | PASS (N/A) — 「此節點無 validators 宣告，跳過語意驗證。」 |

---

### Step 1 — Validator DSL 讀取

從 `skill_graph_schema.yaml` 讀取目標節點的 `validators` 欄位：

```yaml
# 範例節點配置（待 P1 PR 後生效）
s4-tdd:
  validators:
    - type: json_query
      file: test-results.json
      query: ".summary.failed == 0"
      error_msg: "測試必須全部通過（failed == 0）"
    - type: regex_match
      file: "src/**/*.py"
      pattern: "def test_"
      min_matches: 1
      error_msg: "必須存在至少一個 test_ 函式"
    - type: file_hash
      file: test-results.json
      not_older_than_sentinel: true
      error_msg: "測試報告必須比 sentinel 更新"
```

支援三種 validator type：

| Type | 驗證內容 | 防範目標 |
|:---|:---|:---|
| `json_query` | JSON 欄位值斷言（jq 語法） | 空 JSON、失敗報告 |
| `regex_match` | 檔案內容 regex 匹配 | 空測試檔、佔位文字 |
| `file_hash` | mtime vs sentinel 時間戳比對 | 複製舊報告欺騙 |

---

### Step 2 — 逐項驗證

對每個 validator，執行對應檢查並輸出：

| 結果 | 條件 |
|------|------|
| ✅ PASS | 驗證條件完全滿足 |
| ❌ FAIL | 驗證條件不滿足（輸出 `error_msg`） |
| ⚠️ SKIP | P1 PR 未合入，validators 執行機制不可用 |
| ⚠️ N/A | 節點無 validators 宣告 |

---

### Step 3 — 輸出報告

```
Semantic Validation: <node_id>  (<artifact_path>)
V1 [✅/❌/⚠️] json_query: <query>
V2 [✅/❌/⚠️] regex_match: <pattern>
V3 [✅/❌/⚠️] file_hash: not_older_than_sentinel
Overall: VALIDATED / BLOCKED / SKIP (P1 pending)
Issues:
- [Vn]: <error_msg>  （無問題寫「— none —」）
```

Overall：全 ✅ → VALIDATED；有 ❌ → BLOCKED（不允許下游繼續）；全 ⚠️ SKIP → 輸出警告並通知 P1 PR 待合入。

---

## Completion Report

- **VALIDATED** — 所有 validators 通過；節點可繼續推進。
- **BLOCKED** — 至少一個 validator 失敗；說明具體 error_msg；下游節點不得推進。
- **SKIP (P1 pending)** — validators 執行機制未就緒；輸出警告，不阻斷（暫行）。
- **BLOCKED (NEEDS_CONTEXT)** — 工件不存在；說明缺少哪個工件。

</what-to-do>

<supporting-info>

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

P1 PR 合入後，冒煙測試：
```bash
# 以語意失敗工件測試（期望：BLOCKED）
echo '{"summary": {"failed": 1}}' > /tmp/test-results.json
# 以語意成功工件測試（期望：VALIDATED）
echo '{"summary": {"failed": 0}}' > /tmp/test-results.json
```

</supporting-info>
