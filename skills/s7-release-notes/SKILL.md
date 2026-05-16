---
name: s7-release-notes
description: >
  版本發布說明 — 從 git log、需求文檔、audit 報告合成 CHANGELOG.md 條目，
  產出符合 Keep a Changelog 格式的版本塊，為 /s7-telemetry 提供人類可讀的變更記錄。
---

<HARD-GATE>
Do NOT write to `CHANGELOG.md` until the deploy log from `/s7-deploy` exists at
`docs/releases/YYYY-MM-DD-<version>-deploy.md` and confirms `Status: DEPLOYED` or
`Status: DRY-RUN`. Release notes describe what was shipped — writing them before
deployment creates a version history lie.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After updating `CHANGELOG.md`, your message MUST end with exactly:
  "Awaiting your approval to proceed to /s7-telemetry."
Do NOT generate the next stage's artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in the release notes phase.
Your task is to produce an accurate, auditable version entry in `CHANGELOG.md`.

## Workflow

### Step 1 — Gather Source Material

Read the following artifacts before writing a single word of release notes:

| Source | What to extract |
|---|---|
| `git log v<prev>..v<current> --oneline` | All commits since last tag |
| `docs/specs/YYYY-MM-DD-<topic>-requirements.md` | REQ-N titles (user-facing feature names) |
| `docs/audit/YYYY-MM-DD-<branch>-pr-review.md` | Any breaking changes flagged in PR review |
| `docs/releases/YYYY-MM-DD-<version>-deploy.md` | Confirm version, deploy mode, and timestamp |
| `CHANGELOG.md` (if exists) | Previous version block for formatting reference |

```bash
# Get previous tag
PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
# Get commits since last tag
git log ${PREV_TAG:+$PREV_TAG..}HEAD --oneline
```

### Step 2 — Classify Changes

Map each commit and REQ to a change category:

| Category | Contents |
|---|---|
| **Added** | New features from REQ-N / new endpoints / new functions |
| **Changed** | Modified behavior that is NOT a breaking change |
| **Deprecated** | Features that will be removed in a future version |
| **Removed** | Features removed in this version |
| **Fixed** | Bug fixes identified in audit or tests |
| **Security** | Security patches (if any SAST findings were fixed) |

Only include categories that have at least one entry. Do not invent entries.

### Step 3 — Write CHANGELOG.md Entry

Format (Keep a Changelog + Semantic Versioning):

```markdown
## [v1.0.0] - 2026-05-16

### Added
- `word_count(text)` — counts whitespace-separated words (REQ-1)
- `char_count(text)` — counts total characters excluding whitespace (REQ-2)
- `sentence_count(text)` — counts sentences by terminal punctuation (REQ-3)
- `paragraph_count(text)` — counts non-empty paragraphs separated by blank lines (REQ-4)
- REST API endpoint `POST /api/analyze` returning all four metrics (REQ-5)

### Fixed
- (list any bugs fixed in Stage 5)

### Breaking Changes
- (list any, or omit section if none)

### Migration Guide
- (required if Breaking Changes section is non-empty; omit if no breaking changes)
```

Rules:
- Each entry links to a REQ-N where applicable: `(REQ-1)`
- No implementation details (no function signatures, no file paths in user-facing notes)
- Present tense, imperative mood: "Add", not "Added" in the entry text
- If `deploy_mode: "dry-run"`, add a note: `> Note: This release was validated via dry-run. No live deployment was performed.`

### Step 4 — Prepend to CHANGELOG.md

If `CHANGELOG.md` does not exist, create it with a header:

```markdown
# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/) — [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [v1.0.0] - 2026-05-16
...
```

If `CHANGELOG.md` exists, prepend the new block after the `## [Unreleased]` line (or after the header if no Unreleased section).

Commit the file:
```bash
git add CHANGELOG.md
git commit -m "docs: add CHANGELOG entry for v<version>"
```

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| 部署還沒確認，但我先寫 CHANGELOG | CHANGELOG 是歷史記錄；記錄未發生的事是謊言；必須等 deploy.md 的 Status 確認 |
| 這個 commit 意義不明，我猜一下 | 猜測的 release notes 無法審計；如果 commit message 無法對應 REQ，就標記為 `Internal: <commit hash>` 並跳過 |
| 沒有 breaking change，但我順便提一下注意事項 | Breaking Changes 的定義是 API 合約變更；注意事項放在 Changed 或 Fixed，不要污染 Breaking 區塊 |

## Completion Report

Report status using exactly one of:
- **DONE** — `CHANGELOG.md` updated with `## [vN.N.N]` block; committed. Ready for `/s7-telemetry`.
- **BLOCKED** — deploy log missing or status is `FAILED`; cannot write release notes for an undeployed version.
- **NEEDS_CONTEXT** — no requirements doc or git history; state what is missing.

</what-to-do>

<supporting-info>

## Role Identity: Release Manager (Release Notes Phase)
- **Mindset**: Historian. Every entry is auditable, traceable to a requirement, and honest about what changed.
- **Upstream Dependency**: `/s7-deploy` — deploy log must confirm the version was deployed (or dry-run completed).
- **Downstream Target**: `/s7-telemetry` uses the CHANGELOG to populate `next_cycle_inputs`.

## Artifact Dependencies
- **Reads**: `git log`, `docs/specs/*.md`, `docs/audit/*.md`, `docs/releases/YYYY-MM-DD-<version>-deploy.md`
- **Writes**: `CHANGELOG.md` (appended, not overwritten)

## Pipeline Position

```
[s7-build-artifact] → dist/<artifact>, git tag v<version>
        ↓
[s7-deploy] → docs/releases/.../deploy.md
        ↓
[s7-release-notes] → CHANGELOG.md
        ↓
[s7-telemetry] → docs/releases/.../telemetry.json
```

## CHANGELOG Format Reference

```
# Changelog                                    ← one-time header

## [Unreleased]                                ← placeholder for next version

## [v1.0.0] - 2026-05-16                      ← current version block
### Added
- Feature X (REQ-1)
### Fixed
- Bug Y (REQ-2)
### Breaking Changes
- (if any)

## [v0.9.0] - 2026-04-01                      ← previous version (if exists)
...
```

## Process Flow

```
Deploy log (Status: DEPLOYED or DRY-RUN)
   ↓ Status confirmed?
   ├── NO → BLOCKED
   └── YES
        ↓
   git log v<prev>..v<current> --oneline
        ↓
   Read REQ-N titles from requirements doc
        ↓
   Classify commits → Added / Changed / Fixed / Breaking
        ↓
   Write CHANGELOG.md block
        ↓
   git add CHANGELOG.md && git commit
        ↓
   Await approval → /s7-telemetry
```

</supporting-info>
