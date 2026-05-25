# Skill 合格標準 — 第一性原理推導

**版本**: 1.0  
**日期**: 2026-05-25  
**狀態**: DRAFT — 待三方確認後升為 CANONICAL

---

## 一、什麼是 Skill？

Skill 是一個**路由-執行單元**：LLM 路由器讀取它，決定「這個用戶請求要交給哪個 skill」；LLM 執行器再讀取它，決定「步驟是什麼、在哪裡停止」。

因此 Skill 有兩個讀者，各有不同需求：

| 讀者 | 任務 | 最在乎 |
|------|------|--------|
| **路由器** (s0-eval-skill) | 決定要不要啟動這個 skill | 邊界清晰、不重疊 |
| **執行器** (被選中後的模型) | 執行步驟、產出結果 | 步驟明確、終止條件清楚 |

---

## 二、第一性原理推導 P1–P5

從「Skill 要服務兩個讀者」出發，逐條推出必要屬性：

### P1 — Scopeable（可定界）

> 路由器必須能判斷「這個 skill 適用 / 不適用」。

**必要條件**：
- 至少說明一個相鄰 skill 及其邊界差異（正向定義「我做什麼」）
- 至少列出 2 個不該觸發的場景（負向定義「我不做什麼」）
- description 欄位描述觸發條件，而非執行流程

### P2 — Executable（可執行）

> 執行器必須能在不問用戶的情況下跑完每個步驟。

**必要條件**：
- 輸入明確列舉，且每種缺失情況有定義行為（BLOCKED / 繼續 / 詢問）
- 每個存取外部資源的步驟有 fallback 或 BLOCKED 標籤
- 步驟結構清晰（≥3 個步驟或清單項目）

### P3 — Bounded（有邊界）

> Skill 必須知道自己「何時結束」，執行器才能正確移交。

**必要條件**：
- Completion Report 列出 ≥2 種狀態類型（至少區分成功與失敗）
- 有明確的移交指令（交給下一個 skill / 等待用戶核准 / 輸出結果）

### P4 — Efficient（低消耗）

> 路由時不能把 Skill 的全部內容都塞進 context window。

**必要條件**：
- `<what-to-do>` 區塊 ≤ 50 行
- 任何單一 inline 區塊（code fence / table / subsection）≤ 50 行
- 大型樣板或表格必須外置到 `references/`

### P5 — Auditable（可審計）

> 模型版本更新後，skill 行為必須可驗證不漂移。

**必要條件**：
- `tests/fixtures/<skill-name>/cases.json` 存在於磁碟
- SKILL.md 內有明確引用（路徑可發現）
- 涵蓋 golden path 與 adversarial cases

---

## 三、P1–P5 與現有系統的對映

下表顯示每個 P 屬性在 Rubric（評估 skill）和 scan.py（CI 掃描）中的對應檢查。

| P 屬性 | Rubric 準則 | scan.py 檢查 | 覆蓋差距 |
|--------|------------|-------------|---------|
| **P1 Scopeable** | C1 衝突防禦（鄰近 skill + 邊界解釋）<br>C2 雙向阻斷（≥2 負向場景） | C3：description 不含 workflow 動詞<br>C1：`<HARD-GATE>` 存在 | scan.py **不驗證邊界說明品質**；Rubric **不驗證 description 格式** |
| **P2 Executable** | C3 輸入清洗（輸入列舉 + 失敗處理）<br>C5 優雅降級（外部依賴有 fallback） | J1：≥3 步驟/清單項目<br>C2：同時含 "Reads" 和 "Writes"<br>C1：含移交短語 | scan.py **不驗證輸入規格內容**；Rubric **不驗證步驟數量** |
| **P3 Bounded** | ⚠️ **Rubric 無直接準則** | J2：Completion Report ≥2 狀態類型<br>C1：含移交短語 | Rubric **完全缺少 P3** — 這是設計缺口 |
| **P4 Efficient** | C4 漸進披露（inline block ≤ 50 行） | ❌ **scan.py 無任何 P4 檢查** | scan.py **完全缺少 P4** — 線上 CI 不保護 token 預算 |
| **P5 Auditable** | C6 漂移監控（SKILL.md 引用 + 磁碟存在） | Tests：eval_cases.json 含 golden_path + adversarial | 兩者檢查**不同資料來源**（見下方說明） |

### P5 資料來源衝突（重要）

Rubric C6 和 scan.py Tests 都聲稱在驗證 P5，但讀的是**不同檔案**：

```
Rubric C6：   SKILL.md 是否有 "tests/fixtures/<name>/cases.json" 字串
              tests/fixtures/<name>/ 目錄是否存在磁碟
              
scan.py Tests: tests/eval_cases.json 是否有該 skill 的 golden_path + adversarial
```

這兩個資料庫可以**各自通過、各自失敗、互不感知**。

---

## 四、詞彙衝突解析

目前三個系統使用**相同術語指向不同概念**，是造成溝通失敗的根本原因。

### 4.1 「C1 / C2 / C3 / C4」衝突

| 標籤 | Rubric 意義 | scan.py 意義 |
|------|------------|-------------|
| **C1** | 衝突防禦：鄰近 skill 邊界說明 | HARD-GATE 存在 + 移交短語 |
| **C2** | 雙向阻斷：負向觸發場景 | 同時含 "Reads" 和 "Writes" |
| **C3** | 輸入清洗：輸入規格 + 失敗處理 | description 不含 workflow 動詞 |
| **C4** | 漸進披露：inline block 大小 | Red Flag 表（限定 skill 子集） |

**結論**：Rubric 的 C1–C6 和 scan.py 的 C1–C4 是**完全不同的索引空間**，數字重疊是歷史意外，非設計對齊。

### 4.2 「PARTIAL」衝突

| 上下文 | PARTIAL 意義 |
|--------|------------|
| Rubric 單準則評分 | 該準則部分滿足（有 evidence 但不完整） |
| scan.py 整體 verdict | J1 通過但 J2 失敗（或反之） |
| Developer Completion Report | 任務完成一半（是執行狀態，非品質評分） |

### 4.3 整體評級衝突

| 系統 | 整體評級詞彙 |
|------|------------|
| Rubric | PRODUCTION READY / NEAR READY / DRAFT |
| scan.py | ALIGNED / PARTIAL / DRIFTED / MISSING |
| Developer | 無整體評級（只有逐任務狀態） |

---

## 五、統一詞彙提案（Canonical Vocabulary）

以 **P-ID** 作為中立錨點，避免 C-number 重疊問題。

### 5.1 屬性評分（取代 Rubric 的 ✅/⚠️/❌）

| 新標籤 | 意義 | 取代 |
|--------|------|------|
| **PASS** | 該屬性完整滿足 | Rubric ✅ |
| **WEAK** | 該屬性部分滿足（有內容但不完整） | Rubric ⚠️ PARTIAL |
| **FAIL** | 該屬性完全缺失或錯誤 | Rubric ❌ |

> 棄用 PARTIAL 作為屬性評分術語，改用 WEAK，避免與 scan.py verdict 和 developer 狀態混淆。

### 5.2 整體就緒等級

| 新標籤 | 條件 | 對應舊術語 |
|--------|------|----------|
| **READY** | P1–P5 全部 PASS | Rubric: PRODUCTION READY；scan.py: ALIGNED |
| **NEAR-READY** | 最多 1 個 WEAK，無 FAIL | Rubric: NEAR READY |
| **DRAFT** | 有任何 FAIL，或 WEAK ≥ 2 | Rubric: DRAFT；scan.py: PARTIAL / DRIFTED |
| **MISSING** | SKILL.md 不存在 | scan.py: MISSING |

### 5.3 Developer Completion 狀態（保持不變，範圍限定）

以下狀態**只用於 Completion Report**，與 skill 品質評分無關：

`DONE` / `BLOCKED` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT`

> 棄用 Completion Report 中的 `PARTIAL`（與評分術語衝突），若需表達部分完成，使用 `DONE_WITH_CONCERNS`。

---

## 六、各系統對映到 P-ID 的標準表

### Rubric → P-ID

| Rubric 準則 | 對映 P-ID | 說明 |
|------------|---------|------|
| C1 衝突防禦 | P1 Scopeable（正向） | |
| C2 雙向阻斷 | P1 Scopeable（負向） | |
| C3 輸入清洗 | P2 Executable（輸入） | |
| C4 漸進披露 | P4 Efficient | |
| C5 優雅降級 | P2 Executable（外部依賴） | |
| C6 漂移監控 | P5 Auditable | |
| **缺失** | P3 Bounded | ⚠️ Rubric 需新增 C7 |

### scan.py → P-ID

| scan.py 檢查 | 對映 P-ID | 說明 |
|-------------|---------|------|
| J1 步驟數 ≥ 3 | P2 Executable（結構） | |
| J2 Completion 狀態 ≥ 2 | P3 Bounded | |
| C1 `<HARD-GATE>` | P2 Executable（執行保護） | |
| C1 移交短語 | P3 Bounded（移交） | |
| C2 Reads + Writes | P2 Executable（資源鏈） | |
| C3 description 格式 | P1 Scopeable（描述品質） | |
| C4 Red Flag 表 | P2 Executable（防誤執行） | |
| Tests coverage | P5 Auditable | |
| **缺失** | P4 Efficient | ⚠️ scan.py 需新增行預算檢查 |

---

## 七、需要修正的具體缺口

| 缺口 | 影響 | 建議行動 |
|------|------|---------|
| Rubric 無 P3（有界性） | skill 可在沒有明確結束條件下通過 Rubric | 新增 C7 準則：Completion Report ≥2 狀態類型 |
| scan.py 無 P4（效率） | 行數超標的 skill 可通過 CI | scan.py 加入 `<what-to-do>` 行數檢查（閾值 50） |
| P5 資料來源分裂 | Rubric C6 和 scan.py Tests 各自獨立，可各自通過但系統互不感知 | 統一到同一個 fixture 格式，或讓 scan.py 也讀 SKILL.md fixture 引用 |
| C-number 命名空間衝突 | 開發者說「C1」時對方不知道是哪個 C1 | 所有文件統一用 P-ID 作為跨系統錨點 |
| `PARTIAL` 多義 | 討論中需要說明「哪個系統的 PARTIAL」 | 棄用 PARTIAL：評分用 WEAK，CI 用 DRIFTED，Completion 用 DONE_WITH_CONCERNS |

---

## 八、收斂路徑

### 近期（本 worktree）

1. **Rubric** 新增 C7（P3 對映）
2. **scan.py** 新增 P4 行數檢查
3. **SKILL 範本** 移除 Completion Report 中的 `PARTIAL` 狀態

### 中期

4. 統一 P5 資料來源（確定 Rubric C6 和 scan.py Tests 讀相同 fixture）
5. 所有評估報告改用 P-ID 標示（可保留中文名稱作為副標）

### 長期

6. `s0-eval-skill` 升版，改用 P1–P5 + PASS/WEAK/FAIL 語言輸出
7. `scan.py` 輸出格式與 Rubric 評估格式統一，可 diff 比較

---

## 附錄：最小詞彙表

| 術語 | 正式定義 | 使用範圍 |
|------|---------|---------|
| **P1–P5** | Skill 合格的 5 個必要屬性（見第二節） | 跨系統錨點 |
| **PASS / WEAK / FAIL** | 單一 P 屬性的評分結果 | Rubric 評估 |
| **READY / NEAR-READY / DRAFT / MISSING** | Skill 整體就緒等級 | 所有系統 |
| **ALIGNED** | scan.py 通過所有結構檢查 | 僅 scan.py CI |
| **DRIFTED** | scan.py 發現結構性缺陷（J1 失敗） | 僅 scan.py CI |
| **DONE / BLOCKED / DONE_WITH_CONCERNS / NEEDS_CONTEXT** | 執行任務的完成狀態 | 僅 Completion Report |

---

*本文件由第一性原理推導，優先於任何現有系統的局部定義。當 Rubric 或 scan.py 與本文件衝突時，以本文件為準並更新對應系統。*
