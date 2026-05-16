# Vision Spec: mdtoc CLI

**Date**: 2026-05-16
**Author**: Product Manager (s2-capture-vision)

---

## Problem Statement

Developers who maintain Markdown documentation (READMEs, wiki pages, technical specs) must manually write and update Tables of Contents when headings change. This is tedious, error-prone, and frequently falls out of sync. There is no zero-dependency CLI tool that can insert or refresh a TOC in a Markdown file using only a standard Python install.

---

## Target Users

**Primary user**: Developer or technical writer who maintains Markdown files and wants an automated, idempotent TOC. Success looks like: run one command, TOC is up to date, no manual editing.

**Secondary user**: CI pipeline that enforces TOC freshness on every PR (runs `mdtoc generate --check` and fails if TOC is stale).

---

## Proposed Approach

**Chosen: Marker-based idempotent insertion (Option B)**

Insert TOC between `<!-- TOC -->` and `<!-- /TOC -->` markers. If markers exist, replace the content between them. If absent, insert at the top of the file. This is idempotent: running `mdtoc generate` twice produces the same result.

*Rejected alternatives*:
- **Option A — First-heading insertion**: Insert TOC after the first `# Heading`. Fragile: ambiguous placement, breaks files with front matter.
- **Option C — Separate `.toc` sidecar file**: Keeps TOC separate. Rejected because it doesn't solve the "always-in-sync" problem for rendered Markdown views.

---

## Out of Scope

- Setext-style headings (`===` / `---` underlines) — ATX only in v1.0
- HTML heading tags (`<h1>`, `<h2>`)
- Processing directories of files recursively
- Watch mode (auto-update on file change)
- `--check` mode for CI (deferred to v1.1)
- Custom anchor slug formatters

---

## Open Questions

1. Should `--in-place` be the default for `generate`, with `--stdout` as an opt-in? (Resolved in requirements: default is stdout; `--in-place` is explicit opt-in)
2. What happens if the file has only one heading level — should the TOC still be generated? (Yes — min 1 heading produces a 1-entry TOC)
