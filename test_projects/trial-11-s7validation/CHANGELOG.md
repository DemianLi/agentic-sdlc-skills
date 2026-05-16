# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/) — [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [v1.0.0] - 2026-05-16

> Note: This release was validated via dry-run. No live deployment to PyPI was performed.

### Added

- `word_count(text)` — counts whitespace-separated words; empty string returns 0 (REQ-1)
- `char_count(text)` — counts non-whitespace characters; whitespace-only returns 0 (REQ-2)
- `sentence_count(text)` — counts sentence boundaries (`.`, `!`, `?`); consecutive punctuation counts as one (REQ-3)
- `paragraph_count(text)` — counts non-empty paragraphs separated by blank lines (REQ-4)
- REST API endpoint `POST /api/analyze` returning all four metrics as JSON (REQ-5)
- Perf baseline: P99 latency ≤ 0.19ms per operation at 1 concurrent user (REQ-5)

### Fixed

- No bugs were identified and fixed in this release.

### Breaking Changes

None.
