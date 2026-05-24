---
name: s0-semantic-validate
description: >
  Use when verifying artifact content is correct — json_query, regex_match, file_hash checks.
  Outputs VALIDATED or BLOCKED. NOT for structural audit or token budget.
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

### Step 1 — Load Validators

Read target node's `validators` field from `skill_graph_schema.yaml`.

Three validator types:

| Type | Content | Protects Against |
|:---|:---|:---|
| `json_query` | JSON field assertion (jq syntax) | empty JSON, failed reports |
| `regex_match` | file content regex match | empty test files, stubs |
| `file_hash` | mtime vs sentinel timestamp | old report copies |

### Step 2 — Verify Each Validator

For each validator, run check:

| Result | Condition |
|------|------|
| ✅ PASS | condition met |
| ❌ FAIL | condition not met; output error_msg |
| ⚠️ N/A | no validators declared |

### Step 3 — Output Report

```
Semantic Validation: <node_id>  (<artifact_path>)
V1 [✅/❌/⚠️] json_query: <query>
V2 [✅/❌/⚠️] regex_match: <pattern>
V3 [✅/❌/⚠️] file_hash: not_older_than_sentinel
Overall: VALIDATED / BLOCKED / N/A
Issues: [list or none]
```

Overall: all ✅ → VALIDATED; has ❌ → BLOCKED; all ⚠️ → N/A.

---

## Completion Report

- **VALIDATED** — 所有 validators 通過；節點可繼續推進。
- **BLOCKED** — 至少一個 validator 失敗；說明具體 error_msg；下游節點不得推進。
- **N/A** — 節點無 validators 宣告；跳過驗證，不阻斷。
- **BLOCKED (NEEDS_CONTEXT)** — 工件不存在；說明缺少哪個工件。

</what-to-do>

<supporting-info>

**Reads**: `skill_graph_schema.yaml` (validators field), artifact (user-provided path)  
**Writes**: none (chat output only)

→ Full reference: `references/detail.md`

</supporting-info>
