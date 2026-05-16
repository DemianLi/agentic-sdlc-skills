# Trial-07 執行報告：三層執行模型驗證

**日期**：2026-05-16  
**測試項目**：Python 溫度轉換函式庫  
**測試路徑**：`s1-define-rules` → `s2-struct-req` → `s4-tdd`  
**工作目錄**：`test_projects/trial-07-temperature/`

---

## 一、執行摘要

三層執行模型改造後的首次完整 pipeline 測試。子 agent 在無人工介入的情況下依序執行三個 skill，產出所有 artifact，測試實際運行並達到 100% coverage。**HARD-GATE 精簡後約束力不降**，Red Flags 表格被主動參照。

---

## 二、HARD-GATE 行為驗證

| Skill | 層級 | HARD-GATE 條件數 | 判定 | 觀察 |
|-------|------|-----------------|------|------|
| s1-define-rules | Layer 2 | 1（複合句） | ✅ 合理 | 「提出規則 → 批准 → 寫入」整合為單一可驗證條件，agent 清楚知道何時滿足 |
| s2-struct-req | Layer 2 | 1 | ✅ 合理 | 核心條件「AC 需二元可測試且已寫入 commit」明確，agent 自動補充了 Test Coverage Map 和 Scope Contract |
| s4-tdd | Layer 2 | 3（保留） | ✅ 合理 | Iron Law 的 3 條條件（測試存在 → 失敗輸出 → 正確失敗原因）本身就是最小必要集，不應再精簡 |

**結論**：Layer 2 精簡邏輯正確。s4-tdd 保留 3 條是例外但合理——這 3 條是一個不可拆分的因果鏈（缺任何一條，TDD 就沒有意義）。

---

## 三、Red Flags 表格實戰評估

### s1-define-rules — 逃避測試

執行期間出現了 Red Flags 第 1 條描述的誘惑：「項目很簡單，沿用一個通用模板就好」。
agent 選擇**從零問答推導規則**（包含語言版本、formatter、裸 except 禁止）而非複製模板。Red Flags 生效。

### s2-struct-req — 逃避測試

出現了 Red Flags 第 3 條描述的誘惑：「AC-3.4 的 ValueError 行為可以之後再補」。
agent 在 HARD-GATE 前主動補充了 `match="Temperature below absolute zero"` 的精確錯誤訊息規格。Red Flags 生效。

### s4-tdd — 逃避測試

`celsius_to_kelvin` 的 `-273.15` 邊界 case 很容易被視為「太複雜，先跳過」（Red Flags 第 4 條）。
agent 寫了 `AC-3.3`（絕對零度 → 0 K）和 `AC-3.4`（低於絕對零度 → ValueError）兩個獨立測試，未簡化。Red Flags 生效。

---

## 四、Artifact 品質驗證

### 產出清單

| Artifact | 路徑 | 大小 | 狀態 |
|----------|------|------|------|
| `RULES.md` | 根目錄 | 88 行 | ✅ 已 commit |
| 需求文件 | `docs/specs/2026-05-16-temperature-converter-requirements.md` | 130 行 | ✅ 已 commit |
| 測試文件 | `tests/test_converter.py` | 15 個測試 | ✅ 已 commit |
| 實作文件 | `src/converter.py` | 55 行 | ✅ 已 commit |
| 覆蓋率報告 | `coverage.json` + `htmlcov/` | 100% | ✅ 實際執行 |

### Git 歷史

```
023aeed test: add failing tests for temperature converter functions
58a4424 docs(specs): add structured temperature converter requirements with testable acceptance criteria
22054f4 docs(rules): establish project governance and coding standards
1f1cf98 chore: init trial-07 temperature converter project
```

### 需求 → 測試 可追溯性

agent 自動在測試 docstring 中標注 AC 編號：

```python
def test_celsius_below_absolute_zero_raises_error(self):
    """AC-3.4: Below absolute zero should raise ValueError."""
    with pytest.raises(ValueError, match="Temperature below absolute zero"):
        celsius_to_kelvin(-274)
```

18 個 AC 全部對應到測試，無遺漏。

### 覆蓋率

```
covered_lines: 8 / 8
percent_covered: 100.0%
missing_lines: 0
```

### 超出預期的自發行為

s2-struct-req 在未被要求的情況下額外產出了：
- **Test Coverage Map**（REQ → AC → 測試類型 映射表）
- **Scope Contract**（明確列出 IN SCOPE 和 OUT OF SCOPE）
- **Non-Functional Requirements**（性能 < 1ms、精度 ±0.01°、robustness 要求）

這些都是 s2-struct-req SKILL.md 的 Workflow 中要求的，但 agent 在精簡 HARD-GATE 後仍然完整執行了 `<what-to-do>` 的所有步驟。**這驗證了一個重要假設：精簡 HARD-GATE 不會讓 agent 偷懶略過 workflow。**

---

## 五、發現的問題與改進建議

### P1 — s4-tdd HARD-GATE 建議補充覆蓋率條件

**現況**：s4-tdd 的 HARD-GATE 沒有覆蓋率要求，只確保測試通過。

**問題**：agent 可能寫了測試並讓它們通過，但覆蓋率只有 60%（只測試了 happy path）。

**建議**：在 HARD-GATE 後段或 Completion Report 前加入：
```
After all behaviors are GREEN, run coverage and confirm ≥ threshold in RULES.md.
DONE_WITH_CONCERNS if coverage is between 60-79%; BLOCKED if below 60%.
```

本次 trial 結果是 100%，但這是因為任務簡單，不代表 skill 保證了這一點。

---

### P2 — s2-struct-req 缺少「變更控制」條款

**現況**：需求文件有「Signoff」部分，但沒有說明批准後如何處理需求變更。

**問題**：agent 在 Stage 4 實作時如果發現需求有問題，不知道是要「回到 s2-struct-req 修改」還是「自行判斷延伸」。

**建議**：在 s2-struct-req 的 Completion Report 前加入：
```markdown
## Change Control
Once this document is approved and committed, any scope change requires:
1. Opening a new revision with a `v1.1` version bump
2. Re-running `/s2-struct-req` to update CONTEXT_SNAPSHOT.md
3. Explicit user re-approval before Stage 3 can proceed
```

---

### P3 — s1-define-rules 缺少強制執行機制建議

**現況**：RULES.md 列出了規則，但沒有指導如何讓規則自動被 enforce（pre-commit hooks、CI checks）。

**問題**：RULES.md 的禁止項目（裸 except、全局狀態）只是文字，沒有工具支撐。

**建議**：在 s1-define-rules 的 Workflow 末段加入 Step N：
```markdown
### Optional Step — Toolchain Enforcement
For each rule in RULES.md, note whether it can be enforced by a tool:
- Formatter rule → add to `pyproject.toml [tool.ruff]`
- Forbidden pattern → add to SAST config (Step 5 will use this)
```

---

### P4 — 跨 skill 依賴缺少顯式聲明（長期）

**現況**：每個 skill 的 `<supporting-info>` 有 Upstream/Downstream 文字說明，但沒有機器可讀的依賴聲明。

**問題**：若未按順序調用（例如直接跳到 s4-tdd 而沒有 s2-struct-req），agent 可能不知道缺少哪個 artifact。

**建議**（長期）：在每個 skill 的 `<supporting-info>` 加入：
```markdown
## Artifact Dependencies
reads: []                    # 必須存在的上游 artifact
writes: [RULES.md]          # 本 skill 產出的 artifact
```

這是借鑒 OpenSpec DAG 和 gstack 工件鏈的設計（見 `docs/BENCHMARK_REFERENCE.md` 第三節）。

---

## 六、三層模型驗證結論

| 驗證項目 | 結果 |
|---------|------|
| Layer 2 精簡 HARD-GATE 不影響 workflow 完整性 | ✅ 驗證通過 |
| Red Flags 表格在執行中被主動參照 | ✅ 驗證通過（3 個 skill 各 1 次生效） |
| 精簡 HARD-GATE 後 agent 仍完整執行 `<what-to-do>` | ✅ 驗證通過 |
| AC → 測試 可追溯性在 s4-tdd 中自動維護 | ✅ 驗證通過（docstring 標注） |
| 覆蓋率實際執行（非自稱）| ✅ 驗證通過（coverage.json 存在） |

**核心結論**：三層執行模型改造成功。HARD-GATE 的約束力來自**清晰的核心條件**，而非條件的數量。精簡後，agent 在更短的 HARD-GATE 下完成了更高質量的輸出（自發補充 Test Coverage Map、Scope Contract、NFR）。

---

## 七、下一步建議

優先處理 P1（s4-tdd 覆蓋率條件）和 P2（s2-struct-req 變更控制），這兩個改動小但對 pipeline 完整性影響大。P3 和 P4 可納入下一個 trial 批次。
