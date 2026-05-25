# s0-eval-alignment — 三軌掃描判定條件

## 軌一 — 靜態句法冒煙測試（C1–C4）

| 檢查 | 判定條件 |
|------|---------|
| C1 HARD-GATE | 有 `<HARD-GATE>` 區塊，且含正確 gate phrase（boundary skill: "Awaiting your approval"；intra-stage: "proceed immediately to"；terminal: "report DONE"） |
| C2 工件鏈 | `<supporting-info>` 含 **Reads** 與 **Writes** 聲明 |
| C3 Description | frontmatter description 不含流程描述詞（"Step"、"Workflow"、"->"） |
| C4 紅旗表 | 僅適用 `s3-eval-system`、`s5-pr-review`、`s6-verify-release`、`s5-audit-rules`：含 "Red Flag"、"Stop" 字樣的表格 |

C1 或 C2 失敗 → ❌ DRIFTED。

## 軌二 — ParanoidJudge 結構語意審計（J1–J2）

| 代號 | 檢查 | 判定條件 |
|------|------|---------|
| J1 | `<what-to-do>` 完整性 | ≥3 個 step；缺失 → ❌ DRIFTED |
| J2 | Completion Report | ≥2 狀態類型；缺失 → ⚠️ PARTIAL |

## 軌三 — 行為測試覆蓋率

確認 skill 擁有 `golden_path` 與 `adversarial` 兩筆測資。兩者 → ✅ PASS；任一缺失 → ⚠️ PARTIAL。

## 綜合判定

| 條件 | 整體狀態 |
|------|---------|
| 靜態合規 + Judge ALIGNED + Tests PASS | ✅ ALIGNED |
| 靜態合規 + Judge ALIGNED + Tests 缺失 | ⚠️ PARTIAL |
| 靜態合規 + Judge PARTIAL | ⚠️ PARTIAL |
| 靜態不合規 或 Judge DRIFTED | ❌ DRIFTED |
