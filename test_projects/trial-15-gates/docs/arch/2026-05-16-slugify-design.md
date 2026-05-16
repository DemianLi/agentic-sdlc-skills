# Design: slugify

**Date**: 2026-05-17
**Skill**: s3-design-arch
**Stage**: s3
**Version**: 1.0.0

---

## Context

The `slugify` library converts arbitrary text into URL-safe slugs suitable for web routes, slugs, and identifiers. The transformation is deterministic and follows a strict sequence: lowercase, replace whitespace with a separator, and strip non-alphanumeric characters.

**Input**: Any string (including empty, Unicode, special characters)
**Output**: URL-safe slug (lowercase ASCII letters, digits, separator) or error signal (empty result → exit code 1)

**Constraints**:
- No transliteration (accented characters are stripped, not converted)
- No consecutive separator collapsing
- No Unicode normalization
- Separator is a single character (default: `-`)

---

## Decision

The design follows a **layered architecture** with clear separation of concerns:

1. **Core transformation logic** (`slugify.py:slugify()`) — pure function, no I/O
2. **CLI wrapper** (`__main__.py`) — argument parsing, stdin handling, exit codes
3. **Entry point** (`__main__.py`) — Python module execution support

**Design rationale**:
- Pure function enables easy testing, reuse, and composition
- CLI logic isolated from core; easy to add other frontends (API, etc.)
- Transformation rules applied in strict order (lowercase → whitespace replacement → stripping)

---

## Data Structures

### Input
```python
text: str                    # Any string, possibly empty
separator: str              # Single character (default: "-")
```

### Output
```python
slug: str                   # Result: lowercase + digits + separators only
```

### Transformation State (Internal)
No intermediate data structures needed. Transformation is a single-pass stream operation.

---

## API Contracts

### `slugify(text: str, separator: str = "-") -> str`

**Signature**:
```python
def slugify(text: str, separator: str = "-") -> str:
    """
    Convert text to a URL-safe slug.
    
    Args:
        text: Input string (any content, including empty)
        separator: Character to replace whitespace (default: "-")
    
    Returns:
        URL-safe slug: lowercase ASCII [a-z0-9] + separator characters
    
    Algorithm (applied in order):
        1. Convert text to lowercase
        2. Replace whitespace (space, tab, newline) with separator
        3. Remove characters not in [a-z0-9<separator>]
    """
```

**Examples**:
- `slugify("Hello World")` → `"hello-world"`
- `slugify("Héllo & Wörld!", separator="_")` → `"hllo__wrld"`
- `slugify("  a  b  ")` → `"--a--b--"` (consecutive separators NOT collapsed)
- `slugify("!!!") → `""`
- `slugify("")` → `""`

### CLI: `python -m slugify`

**Usage**:
```bash
python -m slugify TEXT [--separator SEP]
python -m slugify [--separator SEP]  # reads from stdin
```

**Behavior**:
- `TEXT`: positional argument (optional); if absent, reads from stdin
- `--separator SEP`: override default `-` with `SEP`
- Output: slug + newline to stdout
- Exit 0: slug is non-empty
- Exit 1: slug is empty

**Examples**:
```bash
python -m slugify "Hello World"                    # → hello-world\n (exit 0)
python -m slugify "Hello World" --separator _      # → hello_world\n (exit 0)
python -m slugify "!!!"                            # → (no output, exit 1)
echo "Hello" | python -m slugify                   # → hello\n (exit 0)
```

---

## Sequence Diagram

```
User Command
    │
    ├─→ Argument Parsing
    │   ├─→ TEXT provided? → use TEXT
    │   └─→ TEXT absent? → read stdin
    │
    ├─→ Extract --separator (default: "-")
    │
    ├─→ Call slugify(text, separator)
    │
    │   [Inside slugify()]
    │   ├─→ 1. Lowercase text
    │   ├─→ 2. Replace whitespace with separator
    │   └─→ 3. Strip non-[a-z0-9<separator>]
    │
    ├─→ Receive slug (possibly empty)
    │
    ├─→ Check slug
    │   ├─→ Non-empty? → print slug + "\n", exit 0
    │   └─→ Empty? → print nothing, exit 1
    │
    └─→ Return to shell
```

---

## Consequences

### Implementation Simplicity
- Core logic is a few lines of Python (single-pass character filtering)
- CLI wrapper uses standard `sys`, `argparse` or simple argument parsing
- No external dependencies required

### Limitations
- **Accented characters stripped, not transliterated**: `ü` becomes ``, not `u`. If transliteration is needed, user must pre-process input or a separate library (e.g., `unidecode`) must be introduced.
- **Consecutive separators not collapsed**: `"a  b"` → `"a--b"`. If collapsing is needed, post-process the result or modify the algorithm in a future version.
- **No Unicode normalization**: Different forms of the same character (NFC/NFKD) may produce different slugs. Not an issue for ASCII, minor for accented text (already stripped).

### Testing Strategy
- **Unit tests**: Direct calls to `slugify()` with known inputs/outputs (AC-1.1, AC-1.2)
- **CLI integration tests**: Shell commands via subprocess (AC-2.1, AC-2.2, AC-3.1, AC-3.2, AC-4.1, AC-4.2)
- **Edge cases**: Empty input, only special characters, large input, stdin EOF handling

### Future Extensions
- CLI could add `--collapse-separators` flag
- Library could add `--transliterate` mode (requires dependency)
- HTTP API endpoint wrapper (FastAPI/Flask) using `slugify()` as core
- Bash/shell alias or standalone executable (PyInstaller)

---

## Design Decisions

### DC-1: Single-character separator only
**Ambiguity**: Specification says "separator character" (singular). Could mean:
- Option A (chosen): Separator must be a single character
- Option B: Separator could be multi-character (e.g., `"__"`)

**Decision**: Interpretation A (single character). Rationale: Simplifies the algorithm, matches common slug conventions, and "character" is singular in the spec.

### DC-2: Whitespace replacement happens before stripping
**Ambiguity**: The rules say "replace whitespace" then "remove non-[a-z0-9<separator>]", but the separator is only valid if it passes the character filter.

**Decision**: Separator is treated as in-scope for the filter (rule 3 preserves it). This means if the separator itself is a non-alphanumeric character, it still appears in the output.

**Confirmation**: AC-1.2 uses `separator="_"` and the output contains `"__"`, confirming the separator is preserved in the output.

### DC-3: Exit code 1 when slug is empty
**Ambiguity**: Spec says "exit 1 when slug is empty" but doesn't specify exit code for other errors (e.g., invalid `--separator` flag).

**Decision**: Exit 1 is specifically for empty slug. Invalid CLI arguments use standard argparse behavior (exit 2, or raise SystemExit). Other edge cases (stdin read failure) use exit 1 as a catch-all.

### DC-4: stdin reads until EOF, not newline
**Ambiguity**: Spec says "reads from stdin until EOF" in REQ-4.

**Decision**: Use `sys.stdin.read()` (or equivalent) to read all of stdin until EOF, then strip the trailing newline if present. This allows multi-line input to be slugified as one block (preserving internal newlines as replacements with separator).

**Example**: `echo -e "Hello\nWorld" | python -m slugify` → `"hello-world"` (newlines become separators).

---

## File Structure

```
slugify/
├── __init__.py           # Export slugify() for library usage
├── __main__.py           # CLI entry point
└── core.py (optional)    # Core slugify() logic (or inline in __init__.py)
```

**Recommendation**: Inline `slugify()` in `__init__.py` for simplicity; defer module split until multiple functions exist.
