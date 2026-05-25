# s1-git-guardrails — Blocked Commands

| Pattern | Risk |
|---------|------|
| `git push` (all variants) | Overwrites remote history, triggers CI/CD, notifies other developers |
| `git reset --hard` | Destroys all uncommitted local changes — unrecoverable |
| `git clean -f` / `-fd` | Deletes untracked files/directories — unrecoverable |
| `git branch -D` | Force-deletes branch, potentially losing commits not merged elsewhere |
| `git checkout .` / `git restore .` | Discards all working-tree changes — unrecoverable |
