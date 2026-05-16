# Project Context: mdtoc CLI

## Language

**Heading**: An ATX-style Markdown heading beginning with one or more `#` characters, followed by a space and heading text. Levels 1–6 correspond to `#` through `######`.

**TOC (Table of Contents)**: A structured list of Headings in a document, rendered as nested Markdown bullet points with anchor links, enabling quick navigation.

**TOC Marker**: A pair of HTML comments — `<!-- TOC -->` and `<!-- /TOC -->` — that delimit the region where the TOC is inserted or replaced. If absent, the TOC is inserted at the top of the file.

**Anchor Link**: A GitHub-flavored Markdown link of the form `[text](#slug)` where `slug` is the heading text lowercased, with spaces replaced by hyphens and non-alphanumeric characters removed.

**In-place Mode**: When the CLI flag `--in-place` is set, the output overwrites the input file directly. When absent, output is written to stdout.

**Max Level**: An integer (1–6, default 3) controlling which heading levels appear in the TOC. Headings deeper than `max_level` are omitted.

## AI Boundaries

### Autonomous (no human confirmation needed)
- Read and parse `.md` files
- Generate TOC text and insert between markers
- Write output to stdout or overwrite file in-place
- Run unit and integration tests
- Run linters and format checkers

### Requires human confirmation
- Any operation that modifies files outside the project directory
- Changing the TOC marker convention (<!-- TOC --> / <!-- /TOC -->)
- Publishing to PyPI or any package registry

## Architecture

Rules defined in `RULES.md` (to be created in `/s1-define-rules`).

**Key constraints**:
- Pure Python 3.9+; zero external runtime dependencies
- CLI entry point: `python -m mdtoc generate <file.md> [--max-level N] [--in-place]`
- Functions are pure where possible — side effects isolated to CLI layer only
