---
name: s7-release-notes
description: 變更日誌沉澱 (Delivery & Iteration)
---
<HARD-GATE>
Do NOT proceed to `/s7-deploy` until release notes are written and committed.
Breaking changes require an explicit upgrade guide — missing upgrade guides block deployment.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s7-deploy.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **Release Manager**.
Your task is to generate documentation for the release.
1. **Read commit history**: `git log <previous-tag>..HEAD --oneline` to list all changes.
2. **Categorize changes** using the Keep a Changelog format:
   - `## Added` — new features
   - `## Changed` — changes to existing features
   - `## Fixed` — bug fixes
   - `## Deprecated` — features that will be removed
   - `## Removed` — features removed in this release
   - `## Security` — security fixes
3. **Breaking changes**: If any change is breaking (API contract changed, field removed, behavior altered), write an explicit `## Migration Guide` section with step-by-step upgrade instructions.
4. **Write to CHANGELOG.md**: Prepend the new release block at the top under `## [v<version>] - YYYY-MM-DD`.
5. Commit: `git add CHANGELOG.md && git commit -m "docs: release notes for v<version>"`

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| CHANGELOG 上次寫過了，這次只是小更新，跳過 | 每一個 release 都需要文檔。「小更新」對某個用戶可能是 breaking change。commit 歷史不能替代 release notes。 |
| 用戶會讀 git log，不用寫 CHANGELOG | git log 是開發者看的；CHANGELOG 是用戶看的。兩者受眾不同，格式和語言都應該不同。你無法跳過這一步。 |
| breaking change 「應該明顯」，不用寫遷移指南 | 什麼叫「明顯」？一個 API 簽名改變，對某些使用者是顯而易見的破壞，對其他人可能需要一小時調試。遷移指南是義務，不是選項。 |

---

## Completion Report
Report status using exactly one of:
- **DONE** — `CHANGELOG.md` updated and committed; migration guide written if breaking changes exist. Proceeding to `/s7-deploy`.
- **BLOCKED** — breaking change detected but migration guide cannot be written without user input; state what decision is needed.
- **NEEDS_CONTEXT** — no previous release tag found; state what baseline to use.
</what-to-do>
<supporting-info>
## Role Identity: Release Manager
- **Mindset**: Communicator. The users must know exactly what changed.
- **Upstream Dependency**: `/s7-build-artifact`.
- **Downstream Target**: `/s7-deploy`.
</supporting-info>
