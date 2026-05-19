# CHANGELOG Templates — s7-release-notes

## Standard CHANGELOG Entry (Keep a Changelog + Semantic Versioning)

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

---

## Full CHANGELOG.md File Structure

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

---

## Upgrade Guide Template (trigger: Breaking Changes section non-empty)

```markdown
## Upgrade Guide — v<prev> → v<current>

### Breaking Changes
- **<功能名稱>**：舊行為 → 新行為
  - 遷移：將 `<舊呼叫>` 改為 `<新呼叫>`
```

---

## API Changes Summary Template (trigger: any endpoint added/removed/changed)

```markdown
## API Changes — v<current>

| 變更類型 | Endpoint / Method | 說明 |
|---------|-------------------|------|
| Added   | POST /api/v2/... | 新增端點 |
| Removed | GET /api/v1/...  | 已移除，請改用 v2 |
| Changed | POST /api/...    | 回傳格式新增 `meta` 欄位 |
```

---

## New CHANGELOG.md Header (only when file doesn't exist yet)

```markdown
# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/) — [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [v1.0.0] - 2026-05-16
...
```
