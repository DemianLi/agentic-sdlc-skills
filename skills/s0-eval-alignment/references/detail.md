# s0-eval-alignment — Extended Reference

## Role Identity: Alignment Inspector
- **Mindset**: 對照設計意圖，找出現實與設計的落差。不修改，只診斷。
- **Upstream Dependency**: `references/skill-design-intent.md`（評估基線）
- **Downstream Target**: 用戶確認後，由對應 stage 的維護者修復漂移 skill。

## Semantic Boundary

| Skill | 評估什麼 | 此 skill 的差異 |
|-------|---------|----------------|
| `s0-eval-skill` | 單一 skill 的 6 項結構品質 | 此 skill 評估**設計意圖對齊度**，批次跑完所有 28 個 skill |
| `s3-eval-system` | 軟體系統架構與爆炸半徑 | 此 skill 評估 skill 文件與原始需求的語意吻合度 |
| `s5-audit-rules` | 代碼對 RULES.md 的合規性 | 此 skill 不看代碼，只看 skill 文件 |

## Eval Fixtures

Fixtures 位於 `tests/fixtures/`；預期輸出位於 `tests/expected/`。

- `skill-aligned/SKILL.md` — 對齊案例（Q: ALIGNED, C1-C3: PASS）
- `skill-drifted/SKILL.md` — 漂移案例（Q: DRIFTED，關鍵詞全缺失）

冒煙測試：以此 skill 對 `tests/fixtures/` 中兩個 fixture 進行掃描，對照 `tests/expected/alignment-scan.md` 驗證輸出格式與判斷邏輯。

## JIT Hook 安裝（P4 自動注入）

hook 腳本位於 `skills/s0-eval-alignment/scripts/jit-hook.sh`。
安裝後，每次 Edit / Write / Bash 工具呼叫前會自動偵測活躍節點並注入最小上下文；無哨兵時靜默退出（<5ms）。

```bash
# 步驟 1：複製腳本
cp skills/s0-eval-alignment/scripts/jit-hook.sh .claude/hooks/jit-inject.sh
chmod +x .claude/hooks/jit-inject.sh

# 步驟 2：在 .claude/settings.json 加入 hooks 區塊
# （完整 JSON 範例見腳本頂部注釋）
#
# "hooks": {
#   "PreToolUse": [
#     { "matcher": "Edit|Write|Bash",
#       "hooks": [{ "type": "command",
#                   "command": "bash .claude/hooks/jit-inject.sh" }] }
#   ]
# }

# 步驟 3：驗證
touch .s4-tdd.done
bash .claude/hooks/jit-inject.sh   # 應輸出 JIT context block
rm .s4-tdd.done
```

觸發條件：`.*.rollback`（P3 回滾哨兵，最高優先）> `.*.done`（節點完成哨兵）。

---

## V3.0 Engine CLI（直接操作引擎時使用）

```bash
# 基礎
python3 skills/s0-eval-alignment/scripts/engine.py --validate           # P1: schema 語法 + 循環檢查
python3 skills/s0-eval-alignment/scripts/engine.py --status             # 完整拓撲狀態

# P2 — 雙向編譯
python3 skills/s0-eval-alignment/scripts/engine.py --sync-docs          # 更新 README Mermaid DAG
python3 skills/s0-eval-alignment/scripts/engine.py --lint-drift         # 比對 README vs schema（--strict-lint 變 hard gate）

# P3 — 執行棧回滾
python3 skills/s0-eval-alignment/scripts/engine.py --stack              # 顯示當前執行棧
python3 skills/s0-eval-alignment/scripts/engine.py --rollback-trace     # 分析失敗節點，壓棧修復目標
python3 skills/s0-eval-alignment/scripts/engine.py --stack-pop          # 重驗後彈棧（失敗仍會阻擋）

# P4 — JIT 上下文注入
python3 skills/s0-eval-alignment/scripts/engine.py \
  --jit --state mock_ide.json --depth 2 \
  --token-check --skills-dir skills       # 生成最小上下文 + 10% token 預算斷言
```

模式：`--mode fluid`（預設，validator 失敗為 warning）｜`--mode strict`（validator 失敗阻斷節點）
