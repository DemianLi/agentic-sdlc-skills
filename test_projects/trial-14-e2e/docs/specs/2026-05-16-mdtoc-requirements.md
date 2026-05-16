# Structured Requirements: mdtoc CLI

**Date**: 2026-05-16
**Author**: Product Manager (s2-struct-req)
**Source**: `docs/specs/2026-05-16-mdtoc-vision.md`

---

## REQ-1: Parse ATX Headings

**User Story**: As a developer, I want the tool to correctly identify all ATX headings in my Markdown file, so that the TOC accurately reflects the document structure.

**Acceptance Criteria**:
- [ ] AC-1.1: Given a Markdown string with ATX headings at levels 1–6, when `parse_headers()` is called, then it returns a list of `Header` objects with correct `level` (int 1–6) and `text` (stripped heading text, no leading `#`)
- [ ] AC-1.2: Given a line that begins with `#` but has no space after (e.g., `#NotAHeading`), when `parse_headers()` is called, then that line is NOT included in the result
- [ ] AC-1.3: Given a heading with leading/trailing whitespace in text (e.g., `##  Hello  `), when `parse_headers()` is called, then `text` is stripped to `"Hello"`
- [ ] AC-1.4: Given a Markdown string with zero headings, when `parse_headers()` is called, then it returns an empty list

**Priority**: Must-Have
**Business Value**: Correct heading extraction is the foundation of TOC accuracy — every downstream function depends on it.

---

## REQ-2: Generate TOC Markdown

**User Story**: As a developer, I want the tool to format the extracted headings as a nested Markdown list with anchor links, so that users can click to navigate to sections.

**Acceptance Criteria**:
- [ ] AC-2.1: Given a list of `Header` objects, when `generate_toc()` is called, then it returns a string where each header appears as a Markdown list item `- [text](#slug)` at the correct nesting level (level 1 → no indent, level 2 → 2-space indent, etc.)
- [ ] AC-2.2: Given a heading text with mixed case and spaces (e.g., `"My Section Title"`), when the anchor slug is generated, then it is lowercase with spaces replaced by hyphens and all non-alphanumeric/non-hyphen characters removed (e.g., `#my-section-title`)
- [ ] AC-2.3: Given `max_level=2` and headers at levels 1, 2, 3, when `generate_toc(headers, max_level=2)` is called, then level-3 headers are excluded from the output
- [ ] AC-2.4: Given an empty list of headers, when `generate_toc([])` is called, then it returns an empty string `""`

**Priority**: Must-Have
**Business Value**: Correct formatting ensures rendered TOCs work as clickable navigation in GitHub, GitLab, and standard Markdown renderers.

---

## REQ-3: Insert/Replace TOC in Document

**User Story**: As a developer, I want the tool to insert the generated TOC into my file at the correct location, so that I can run one command to refresh the TOC without manual editing.

**Acceptance Criteria**:
- [ ] AC-3.1: Given a Markdown string containing `<!-- TOC -->` and `<!-- /TOC -->` markers (with any content between them), when `insert_toc()` is called, then the content between the markers is replaced with the new TOC; markers are preserved
- [ ] AC-3.2: Given a Markdown string with NO markers, when `insert_toc()` is called, then the TOC (wrapped in markers) is prepended to the document with a blank line separating it from existing content
- [ ] AC-3.3: Given a Markdown string where `insert_toc()` is called twice with the same content, then the result is identical to calling it once (idempotency)
- [ ] AC-3.4: Given a Markdown string where the TOC markers appear in a code block (` ``` `), when `insert_toc()` is called, then markers inside code blocks are NOT treated as TOC markers

**Priority**: Must-Have / AC-3.4 = Should-Have
**Business Value**: Idempotency is the core value proposition — CI pipelines need deterministic, repeatable behavior.

---

## REQ-4: CLI Entry Point

**User Story**: As a developer, I want to run `python -m mdtoc generate <file.md>` from the terminal, so that I can integrate TOC generation into scripts and CI pipelines without installing additional tools.

**Acceptance Criteria**:
- [ ] AC-4.1: Given an existing `.md` file, when `python -m mdtoc generate <file>` is run, then the processed content (with TOC inserted/updated) is written to stdout and exit code is 0
- [ ] AC-4.2: Given the `--in-place` flag, when `python -m mdtoc generate <file> --in-place` is run, then the file is overwritten in-place and stdout is empty
- [ ] AC-4.3: Given the `--max-level N` flag, when `python -m mdtoc generate <file> --max-level 2` is run, then only level-1 and level-2 headings appear in the TOC
- [ ] AC-4.4: Given a non-existent file path, when `python -m mdtoc generate <nonexistent>` is run, then a human-readable error message is printed to stderr and exit code is 1
- [ ] AC-4.5: Given no subcommand, when `python -m mdtoc` is run, then help text is printed to stdout and exit code is 0

**Priority**: Must-Have
**Business Value**: CLI usability is the primary delivery mechanism — without a working CLI, the tool cannot be adopted.

---

## REQ-5: Performance SLO

**User Story**: As a CI pipeline operator, I want the tool to process a large Markdown file quickly, so that it does not become a bottleneck in the CI pipeline.

**Acceptance Criteria**:
- [ ] AC-5.1: Given a 10,000-line Markdown file with 200 headings, when `python -m mdtoc generate <file>` is run 100 times (warm cache), P99 latency is < 500ms end-to-end
- [ ] AC-5.2: Given any input, the tool consumes < 50MB RAM during processing

**Priority**: Should-Have
**Business Value**: CI pipelines run on shared infrastructure; slow tools create adoption friction.

---

## Test Coverage Map

| AC | Unit | Integration | E2E | Perf |
|---|---|---|---|---|
| AC-1.1 – AC-1.4 | ✅ | — | — | — |
| AC-2.1 – AC-2.4 | ✅ | — | — | — |
| AC-3.1 – AC-3.3 | ✅ | — | — | — |
| AC-3.4 | ✅ | — | — | — |
| AC-4.1 – AC-4.5 | — | ✅ | ✅ | — |
| AC-5.1 – AC-5.2 | — | — | — | ✅ |

---

## Scope Contract

**IN scope**:
- `parse_headers()`, `generate_toc()`, `insert_toc()` functions
- `python -m mdtoc generate <file> [--max-level N] [--in-place]` CLI
- ATX headings only (# syntax)
- Performance SLO: P99 < 500ms for 10K-line file

**OUT of scope**:
- Setext-style headings
- HTML heading tags
- Recursive directory processing
- Watch mode
- `--check` mode for CI
- Custom anchor slug formatters
