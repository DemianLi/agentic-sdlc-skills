# Changelog

All notable changes to mdtoc are documented in this file.

---

## [v1.0.0] - 2026-05-16

> **Note**: This release was validated with `Status: DRY-RUN` (no live PyPI deployment configured for trial-14 validation).

### Added

- **`parse_headers(text)`** — Extracts ATX headings (levels 1–6) from Markdown text, skipping content inside fenced code blocks (REQ-1)
- **`generate_toc(headers, max_level=3)`** — Formats headers as a nested Markdown list with GitHub-flavored anchor links; supports `max_level` filtering (REQ-2)
- **`insert_toc(text, toc)`** — Inserts or replaces TOC between `<!-- TOC -->` / `<!-- /TOC -->` markers; prepends to document if markers absent; fully idempotent (REQ-3)
- **CLI entry point** `python -m mdtoc generate <file> [--max-level N] [--in-place]` — stdout output by default; `--in-place` overwrites source file; exit 1 on file-not-found (REQ-4)

### Performance

- P99 latency: **4.90ms** for 10,000-line file with 200 headings (SLO: < 500ms) (REQ-5)
- Warmup: 15 iterations discarded before measurement

### Requirements Covered

| ID | Title | Status |
|---|---|---|
| REQ-1 | Parse ATX Headings | ✅ |
| REQ-2 | Generate TOC Markdown | ✅ |
| REQ-3 | Insert/Replace TOC in Document | ✅ |
| REQ-4 | CLI Entry Point | ✅ |
| REQ-5 | Performance SLO (P99 < 500ms) | ✅ |
