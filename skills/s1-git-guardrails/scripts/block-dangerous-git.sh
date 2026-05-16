#!/bin/bash
# git-guardrails: block destructive git commands from Claude Code autonomous execution
# Exit 2 = block the command (Claude Code shows stderr to user)
# Exit 0 = allow the command

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('command', ''))
except Exception:
    print('')
" 2>/dev/null)

BLOCKED_PATTERNS=(
    "git push"
    "git reset --hard"
    "git clean -f"
    "git clean -fd"
    "git branch -D"
    "git checkout \."
    "git restore \."
)

for PATTERN in "${BLOCKED_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$PATTERN"; then
        echo "⛔ git-guardrails: '${PATTERN}' is blocked. Requires explicit user confirmation." >&2
        exit 2
    fi
done

exit 0
