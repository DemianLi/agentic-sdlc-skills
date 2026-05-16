# Requirements: slugify

**Date**: 2026-05-16
**Skill**: s2-struct-req
**Stage**: s2
**Version**: 1.0.0

---

## Overview

`slugify` is a Python library and CLI tool that converts arbitrary text into URL-safe slugs. A slug consists only of lowercase ASCII letters, digits, and a configurable separator character (default: hyphen).

---

## Requirements

### REQ-1 — Core slugify function

**Statement**: The library must expose a `slugify(text, separator="-")` function that returns a `str`.

**Transformation rules** (applied in order):
1. Convert `text` to lowercase
2. Replace every whitespace character (space, tab, newline) with `separator`
3. Remove every character that is not `[a-z0-9<separator>]`

**Acceptance criteria**:

| ID | Input | Expected output |
|---|---|---|
| AC-1.1 | `slugify("Hello World")` | `"hello-world"` |
| AC-1.2 | `slugify("Héllo & Wörld!", separator="_")` | `"hllo__wrld"` |

Notes:
- The separator itself is preserved in the output (it is in the allowed set).
- Multiple consecutive separators are NOT collapsed (e.g., `"a  b"` → `"a--b"`); collapsing is out of scope for v1.0.
- Non-ASCII letters (e.g., accented characters) are stripped, not transliterated.

---

### REQ-2 — CLI: positional argument mode

**Statement**: The package must be executable as `python -m slugify TEXT` and print the slug to stdout followed by a newline.

**Acceptance criteria**:

| ID | Command | Expected stdout |
|---|---|---|
| AC-2.1 | `python -m slugify "Hello World"` | `hello-world\n` |
| AC-2.2 | `python -m slugify ""` | _(empty — triggers exit 1; see REQ-4)_ |

---

### REQ-3 — CLI: `--separator` flag

**Statement**: The CLI must accept an optional `--separator SEP` flag. When provided, `SEP` replaces the default separator `-` in the slugify transformation.

**Acceptance criteria**:

| ID | Command | Expected stdout |
|---|---|---|
| AC-3.1 | `python -m slugify "Hello World" --separator _` | `hello_world\n` |
| AC-3.2 | `python -m slugify "Hello World" --separator .` | `hello.world\n` |

---

### REQ-4 — CLI: exit codes and stdin fallback

**Statement**: The CLI exits with code 0 on success and code 1 when the slug produced is empty (i.e., input contained no characters surviving the strip step). When `TEXT` is not provided as a positional argument, the CLI reads from stdin until EOF.

**Acceptance criteria**:

| ID | Scenario | Expected behaviour |
|---|---|---|
| AC-4.1 | Input produces a non-empty slug | Exit 0 |
| AC-4.2 | Input produces an empty slug (e.g., `"!!!"`) | Exit 1, no stdout output |

Notes:
- stdin mode: `echo "Hello" \| python -m slugify` must behave identically to `python -m slugify "Hello"`.
- The CLI must not hang waiting for stdin if a positional `TEXT` argument is provided.

---

## Out of Scope (v1.0)

- Transliteration of non-ASCII characters (e.g., `ü → u`)
- Collapsing consecutive separators
- Unicode normalization (NFKD/NFC)
- Maximum slug length truncation
