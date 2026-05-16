# Feature Trace: token-optimizer PreToolUse Bash Hook
Traced: 2026-05-16
Entry point(s): `hooks.json:14-20` — `PreToolUse` / `matcher: "Bash"` → `bash_hook.py`
Workspace boundary: Claude Code CLI (fires PreToolUse event), subprocess shell (executes final command)

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant CC as [external: Claude Code CLI]
    participant HJ as hooks.json
    participant PL as python-launcher.sh
    participant RD as run.py (dispatcher)
    participant BH as bash_hook.py
    participant PE as plugin_env.py
    participant LOG as bash-rewrites.jsonl
    participant BC as bash_compress.py

    CC->>HJ: PreToolUse event (tool_name="Bash", command="ls -la")
    Note over HJ: matcher:"Bash" fires command hook
    HJ->>PL: bash python-launcher.sh run.py bash_hook.py --quiet
    Note over PL: find_interpreter() — walks PATH for python3/python/py
    PL->>RD: exec python3 run.py bash_hook.py --quiet
    Note over RD: resolves CLAUDE_PLUGIN_ROOT + "bash_hook.py" → absolute path
    RD->>BH: subprocess.Popen([python3, bash_hook.py]) + wait(timeout=120)
    BH->>BH: json.loads(stdin) — reads hook payload
    BH->>PE: is_v5_flag_enabled("v5_bash_compress", "TOKEN_OPTIMIZER_BASH_COMPRESS", default=True)
    PE-->>BH: True (env var not set → config.json not set → default=True)
    BH->>BH: _has_dangerous_chars("ls -la") → False (no ;|&`$(){}><\n)
    BH->>BH: _is_whitelisted("ls -la") → shlex.split → cmd="ls" in _WHITELIST_SINGLE → True
    Note over BH: builds rewritten command:<br/>bash python-launcher.sh bash_compress.py ls -la
    BH->>LOG: append JSON event {timestamp, command[:100], session_id} via os.open O_APPEND
    BH-->>CC: stdout: {"hookSpecificOutput": {"updatedInput": {"command": "bash ... bash_compress.py ls -la"}}}
    Note over CC: applies updatedInput rewrite, executes rewritten command
    CC->>PL: bash python-launcher.sh bash_compress.py ls -la
    PL->>BC: exec python3 bash_compress.py ls -la
    BC->>BC: subprocess.Popen(["ls", "-la"], shell=False) — captures stdout+stderr
    BC->>BC: _strip_ansi(output) — remove ANSI escape codes
    BC->>BC: _find_preserved_lines() — scan _TOKEN_PATTERNS + _ERROR_STDERR_PATTERNS
    BC->>BC: apply compression handler [INFERRED: ls handler from command family routing]
    BC-->>CC: compressed output → tool_result returned to Claude
```

---

## Business Logic Summary

When Claude Code is about to run the Bash tool with a command like `ls -la` or `git status`, the token-optimizer intercepts it **before** execution via a `PreToolUse` hook. The hook:

1. Reads the command from the hook payload (JSON on stdin)
2. Safety-checks it: rejects anything with shell metacharacters (`;`, `|`, `&`, `` ` ``, etc.) or unsafe env var assignments
3. Whitelist-checks it: only known read-only commands (`ls`, `git status/log/diff`, `pytest`, `find`, etc.) are eligible
4. If eligible, rewrites the command to route through `bash_compress.py` — a wrapper that runs the original command, captures its output, scans for credentials (which are never compressed), and applies pattern-matched compression to strip noise
5. Returns `updatedInput` to Claude Code, which transparently executes the rewritten command instead

Net effect: Claude sees a shorter, token-compressed version of `ls`/`git status` output. The compression is invisible from Claude's perspective — `bash python-launcher.sh bash_compress.py ls -la` and `ls -la` look identical to Claude.

**Why bash_hook.py exits 0 on all errors**: Any hook failure that blocks a tool call would break Claude's workflow. Fail-open (exit 0, no output) means the original command runs unmodified if anything goes wrong.

---

## Confirmed Facts

- Entry point: `PreToolUse/Bash` matcher in `~/.claude/token-optimizer/hooks/hooks.json:14-20`
- Dispatcher: `hooks/run.py:53` — `subprocess.Popen([sys.executable, script_path, *script_args])` with 120s timeout
- Python resolver: `hooks/python-launcher.sh:13-39` — `find_interpreter()` walks `$PATH` for `python3`, then `python`, then `py -3`
- Whitelist: `bash_hook.py:38-52` — `_WHITELIST_SINGLE` includes `ls`, `git`, `pytest`, `find`; `_WHITELIST_COMPOUND` includes `("git", "status")`, `("git", "log")`, etc.
- Metachar guard: `bash_hook.py:27` — `_DANGEROUS_CHARS = frozenset(";|&\`$(){}><\n\r\x00")`
- Git write guard: `bash_hook.py:94-99` — `_GIT_WRITE_SUBCMDS` blocks `commit`, `push`, `pull`, `add`, `reset`, etc. from being rewritten
- Feature flag: `plugin_env.py:146-187` — priority order: env var → user config → plugin-data config → default (True)
- Rewrite format: `bash_hook.py:218-221` — `"bash " + shlex.quote(launcher_path) + " " + shlex.quote(compress_path) + " " + tokens`
- Recursion prevention: `bash_hook.py:161` — `bash`, `sh`, `zsh` etc. are never whitelisted, so the rewritten command starting with `bash` is not re-intercepted
- Log file: `~/.claude/token-optimizer/bash-rewrites.jsonl` — appended via `os.O_APPEND` (atomic on POSIX, mode 0o600)
- Credential preservation: `bash_compress.py:30-55` — 20+ regex patterns for AWS keys, GitHub PATs, JWTs, DB URIs, etc. — matching lines are never compressed
- Fail-open: `run.py:67-72` — `return 0` on any subprocess error; `bash_hook.py:172-173` — returns silently if feature disabled or payload malformed

---

## Gaps & Unknowns

- `bash_compress.py` compression handler dispatch: The file routes by command (git status → `_compress_git_status`, git log → `_compress_git_log`). The `ls` and `find` handlers were not fully read — routing logic is `[INFERRED: from parallel structure of confirmed handlers]`
- `PostToolUse` / `archive_result.py`: After the compressed output returns, a second hook fires (`PostToolUse` / `Bash`) calling `archive_result.py`. This sidecar was not traced.
- How Claude Code reads `updatedInput`: This is `[external: Claude Code CLI]` — the protocol is defined by Claude Code, not by the plugin.

---

## Boundary Map

| Crossed boundary | What lives there |
|---|---|
| `[external: Claude Code CLI]` | Fires PreToolUse event; applies `updatedInput` rewrite; executes the rewritten command; returns `tool_result` to Claude |
| `subprocess shell (bash_compress.py → ls)` | Actual command execution: `subprocess.Popen(["ls", "-la"], shell=False)` — OS process boundary |
| `~/.claude/token-optimizer/bash-rewrites.jsonl` | Sidecar audit log: every rewritten command is appended (timestamp, command prefix, session_id) |
| `~/.claude/token-optimizer/config.json` (user config) | Feature flag override: user can set `"v5_bash_compress": false` to disable |
| `$CLAUDE_PLUGIN_DATA/config/config.json` (plugin-data config) | Feature flag second source; dashboard toggle writes here |
