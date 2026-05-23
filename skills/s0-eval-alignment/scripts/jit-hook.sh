#!/usr/bin/env bash
# JIT Context Injector (V3.0 P4)
#
# 安裝方式：見下方「Installation」區塊，或參閱
#   skills/s0-eval-alignment/SKILL.md  §「JIT Hook 安裝」
#   docs/v3-architecture/ADR-004-jit-context-injection.md
#
# 運作方式：
#   在每次 Edit / Write / Bash 工具呼叫前執行。
#   偵測 workspace 中的 .*.rollback / .*.done 哨兵 → 推斷當前活躍節點 →
#   輸出最小 JIT 上下文到 stdout（成為 Claude 的 hook feedback）。
#   無哨兵時在 <5ms 內靜默退出，零開銷。
#
# ── Installation ──────────────────────────────────────────────────────
#
#   步驟 1：複製 hook 腳本
#     cp skills/s0-eval-alignment/scripts/jit-hook.sh .claude/hooks/jit-inject.sh
#     chmod +x .claude/hooks/jit-inject.sh
#
#   步驟 2：在 .claude/settings.json 的 hooks 區塊加入以下配置
#     （若 settings.json 無 hooks 欄位則新增）：
#
#     "hooks": {
#       "PreToolUse": [
#         {
#           "matcher": "Edit|Write|Bash",
#           "hooks": [
#             {
#               "type": "command",
#               "command": "bash .claude/hooks/jit-inject.sh"
#             }
#           ]
#         }
#       ]
#     }
#
#   步驟 3：驗證（在專案根目錄）
#     touch .s4-tdd.done
#     bash .claude/hooks/jit-inject.sh   # 應輸出 JIT context block
#     rm .s4-tdd.done
# ─────────────────────────────────────────────────────────────────────

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ENGINE="$PROJECT_ROOT/skills/s0-eval-alignment/scripts/engine.py"
SCHEMA="$PROJECT_ROOT/schemas/skill_graph_schema.yaml"
SKILLS_DIR="$PROJECT_ROOT/skills"

# Fast exit: engine or schema missing
[ -f "$ENGINE" ] && [ -f "$SCHEMA" ] || exit 0

# Detect active node — .*.rollback takes priority over .*.done
ACTIVE_NODE=""

for f in "$PROJECT_ROOT"/.*.rollback; do
  [ -f "$f" ] || continue
  base="$(basename "$f")"
  ACTIVE_NODE="${base#.}"
  ACTIVE_NODE="${ACTIVE_NODE%.rollback}"
  break
done

if [ -z "$ACTIVE_NODE" ]; then
  latest="$(ls -t "$PROJECT_ROOT"/.*.done 2>/dev/null | head -1)"
  if [ -n "$latest" ]; then
    base="$(basename "$latest")"
    ACTIVE_NODE="${base#.}"
    ACTIVE_NODE="${ACTIVE_NODE%.done}"
  fi
fi

# No active node → silent exit
[ -n "$ACTIVE_NODE" ] || exit 0

# Output JIT prompt (stdout becomes hook feedback visible to Claude)
python3 "$ENGINE" \
  --schema "$SCHEMA" \
  --jit \
  --state <(printf '{"active_node_hint": "%s"}' "$ACTIVE_NODE") \
  --skills-dir "$SKILLS_DIR" \
  2>/dev/null

exit 0
