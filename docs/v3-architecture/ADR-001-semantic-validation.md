# ADR-001: 語意一致性與真偽驗證 (Semantic Evidence Verification)

**優先級**: P1 — 最高性價比，最小改動範圍
**設計來源**: Superpowers 倉庫哲學 + `skill_graph_3_0_design_dimensions.md` 維度 4
**狀態**: ✅ 已實作 — PR #8 (`feat/p1-semantic-validator` + `feat/p1.5-file-hash`，已合入 main)

---

## Context

V2.2 的工件驗證邏輯有兩個致命弱點：

1. **Sentinel 只檢查存在性**（`engine.py:214–215`）：`.{skill}.done` 檔案只要 `.exists()` 為 True，即視為完成。AI 可透過 `touch` 空檔案繞過門控。
2. **Outputs 只檢查 glob 匹配真值**（`engine.py:226–229`）：`glob.glob()` 返回非空列表即通過。空 JSON、佔位文字、舊報告複製都能騙過此檢查。

**根本問題**：形式上的 `exists()` 不等於語意上的完成。未經內容校驗的工件等同於不存在。

---

## Decision

在 `engine.py` 中引入 **validators DSL**，支援三種驗證器類型：

### Validators Schema（YAML 聲明式）

在 `skill_graph_schema.yaml` 中，節點可聲明 `validators` 欄位：

```yaml
s4-tdd:
  stage: 4
  requires:
    - s4-setup-env
  outputs:
    - test-results.json
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
      error_msg: "測試報告必須比 sentinel 更新（防止複製舊報告）"
```

### 三種驗證器類型

| Type | 行為 | 防範 |
|:---|:---|:---|
| `json_query` | 解析 JSON，以 jq 語法斷言 | 空 JSON、全失敗報告 |
| `regex_match` | 對檔案內容做 regex 匹配 | 空測試檔、佔位文字 |
| `file_hash` | 比對 mtime vs sentinel 時間戳 | 複製舊報告欺騙 |

### 整合點（engine.py 改動方向）

**步驟 1** — 放寬 `valid_keys`（`L110`）：
```python
# V2.2（必須改）
valid_keys = {"stage", "requires", "outputs"}

# V3.0
valid_keys = {"stage", "requires", "outputs", "reads", "writes", "sentinels", "validators"}
```

**步驟 2** — 新增 `SemanticValidator` 類別，在 `get_completed_nodes`（`L194–247`）中於 glob 匹配後調用：
```python
# 偽代碼（設計意圖，非最終實作）
if node_data.get("validators"):
    validator = SemanticValidator(node_data["validators"], workspace)
    result = validator.run()
    if not result.passed:
        # 不標記為 COMPLETED，記入 BLOCKED 原因
        blocked_reasons[node_id] = f"[SemanticValidationError] {result.error_msg}"
        continue
```

**步驟 3** — `strict` mode 下 validators 為**強制執行**；`fluid` mode 下為**建議警告**（不阻斷，但輸出 ⚠️）。

---

## Consequences

**正面**：
- 杜絕 AI 透過 touch 空檔案或複製舊報告繞過門控
- validator 聲明在 YAML 中，對人可讀，對工具可驗
- 不依賴外部 library（json 標準庫 + re 標準庫）

**負面/風險**：
- `valid_keys` 放寬後，若有拼寫錯誤（如 `validater`），舊版 engine 的 `UnknownFieldError` 不再攔截 → 需在 `_validate_schema` 加型別檢查
- `file_hash` 方案依賴 mtime，在 git clone 後 mtime 可能重置 → 退化為 SHA256 比對（P1.5 再處理）
- PyYAML fallback（`parse_simple_yaml` L20–66）不支援 nested 欄位解析 → validators 欄位需要真實 PyYAML；fallback 模式下跳過 validators（保持相容）

---

## Verification Plan

### 欺騙測試（對應原始設計文件驗證方法）

```bash
# 1. 建立語意失敗的報告（檔案存在且 size > 0，但內容表示失敗）
echo '{"summary": {"failed": 1}}' > test-results.json

# 2. 在 schema 為 s4-tdd 配置 json_query validator 後：
python3 skills/s0-eval-alignment/scripts/engine.py --status --mode strict

# 預期輸出包含：
# [SemanticValidationError] Node s4-tdd failed: 測試必須全部通過（failed == 0）
# s4-tdd 狀態為 BLOCKED
```

### 下游阻斷測試

```bash
# 確認 s4-tdd 被語意阻斷後，s5-sast-lint（依賴 s4-tdd）也應顯示 BLOCKED
python3 skills/s0-eval-alignment/scripts/engine.py --blocked
# 預期：s5-sast-lint 出現在 blocked list，依賴追蹤到 s4-tdd 語意失敗
```

### 6 指標框架核對

根據 [[reference_skill_checklist.md]] 第 3 項「輸入清洗（Input Linting）」：
- validators DSL 需對 `type` 欄位進行枚舉校驗（只允許 `json_query`、`regex_match`、`file_hash`）
- 非法 type 值 → `_validate_schema` 應拋出 `InvalidValidatorTypeError`，exit 1

根據第 5 項「優雅降級」：
- PyYAML 缺席時，validators 欄位跳過（不崩潰），輸出 `[WARNING] validators skipped: PyYAML not available`
