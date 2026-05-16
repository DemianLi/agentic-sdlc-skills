# Work Breakdown Structure (WBS): slugify

**Date**: 2026-05-17
**Skill**: s3-breakdown-wbs
**Stage**: s3
**Version**: 1.0.0

---

## Overview

This WBS decomposes the `slugify` project into implementable tasks. Tasks are sequenced to support early testing and parallel work where possible.

---

## 1. Core Library Implementation

### 1.1 Implement `slugify()` function
**Description**: Write the core transformation function in `slugify/__init__.py` (or `slugify/core.py`).

**Acceptance Criteria**:
- Function signature: `slugify(text: str, separator: str = "-") -> str`
- Implements three-step transformation: lowercase → whitespace replacement → character stripping
- Handles empty input (returns empty string)
- Returns string of lowercase, digits, and separator characters only

**Testing**: Unit tests (see §2.1)

**Dependencies**: None

**Effort**: ~30 minutes

---

### 1.2 Handle edge cases in `slugify()`
**Description**: Verify and document behavior on edge cases.

**Edge Cases**:
- Empty string: `""` → `""`
- Whitespace only: `"   "` → `"---"` (or `separator` repeated)
- Non-ASCII (accented): `"Café"` → `"caf"` (no transliteration)
- Special characters: `"Hello & World!"` → `"hello--world"`
- Unicode: `"你好世界"` → `""` (all non-ASCII)
- Large input: no truncation, process as-is

**Acceptance Criteria**:
- All edge cases produce correct output per requirements
- No exceptions raised (except if separator is invalid, if any validation added later)

**Testing**: Unit tests (see §2.1)

**Dependencies**: §1.1

**Effort**: ~15 minutes

---

## 2. Testing

### 2.1 Write unit tests for `slugify()`
**Description**: Create test file `tests/test_slugify.py` with comprehensive unit test coverage.

**Test Cases** (from requirements):
- AC-1.1: `slugify("Hello World")` → `"hello-world"`
- AC-1.2: `slugify("Héllo & Wörld!", separator="_")` → `"hllo__wrld"`
- Empty input: `slugify("")` → `""`
- Only separator: `slugify("   ")` → `separator * 3`
- Custom separators: `separator="."`, `separator="_"`, `separator="~"`
- Non-ASCII: accented chars, CJK, emoji (all stripped)
- Multiple whitespace: `"a  b"` → `"a--b"` (consecutive separators preserved)

**Acceptance Criteria**:
- All AC criteria pass
- All edge cases have tests
- Test coverage ≥ 90% of `slugify()` code

**Testing Framework**: `pytest`

**Dependencies**: §1.1, §1.2

**Effort**: ~45 minutes

---

## 3. CLI Implementation

### 3.1 Implement CLI argument parsing
**Description**: Create `slugify/__main__.py` to handle CLI invocation.

**Features**:
- Accept positional argument `TEXT` (optional)
- Accept `--separator SEP` flag (optional)
- Parse arguments using `argparse` or manual parsing

**Acceptance Criteria**:
- `python -m slugify "Hello World"` parses correctly
- `python -m slugify "Hello" --separator _` parses correctly
- Invalid arguments produce clear error messages
- Help text available: `python -m slugify --help`

**Testing**: Integration tests (see §3.3)

**Dependencies**: §1.1

**Effort**: ~20 minutes

---

### 3.2 Implement stdin fallback
**Description**: Extend `slugify/__main__.py` to read from stdin when `TEXT` is not provided.

**Features**:
- Detect if `TEXT` positional is absent
- If absent, read from stdin until EOF
- Strip trailing newline from stdin input before slugifying
- Do not hang if `TEXT` is provided (no stdin read)

**Acceptance Criteria**:
- `echo "Hello" | python -m slugify` behaves same as `python -m slugify "Hello"`
- Multi-line stdin: `"Hello\nWorld"` → both lines processed (newlines become separators)
- No hanging when `TEXT` is provided

**Testing**: Integration tests (see §3.3)

**Dependencies**: §3.1

**Effort**: ~20 minutes

---

### 3.3 Implement exit code handling
**Description**: Extend `slugify/__main__.py` to produce correct exit codes and output.

**Features**:
- Exit 0 and print slug if non-empty
- Exit 1 and print nothing if slug is empty
- Print slug followed by `\n` (newline) on success

**Acceptance Criteria** (from requirements):
- AC-4.1: Non-empty slug → exit 0, stdout has slug
- AC-4.2: Empty slug → exit 1, no stdout output
- AC-2.1: `python -m slugify "Hello World"` → `hello-world\n` (exit 0)
- AC-2.2: `python -m slugify ""` → empty stdout (exit 1)

**Testing**: Integration tests (see §3.4)

**Dependencies**: §3.1, §3.2

**Effort**: ~15 minutes

---

### 3.4 Write CLI integration tests
**Description**: Create `tests/test_cli.py` with end-to-end CLI tests.

**Test Cases** (from requirements):
- AC-2.1: `python -m slugify "Hello World"` → `hello-world\n` (exit 0)
- AC-2.2: `python -m slugify ""` → exit 1, no output
- AC-3.1: `python -m slugify "Hello World" --separator _` → `hello_world\n`
- AC-3.2: `python -m slugify "Hello World" --separator .` → `hello.world\n`
- AC-4.1: Non-empty slug → exit 0
- AC-4.2: Empty slug → exit 1
- stdin mode: `echo "Hello" | python -m slugify` matches `python -m slugify "Hello"`
- Help text: `python -m slugify --help` exits 0

**Acceptance Criteria**:
- All AC criteria pass
- Exit codes verified
- stdout/stderr correct

**Testing Framework**: `pytest`, subprocess for CLI invocation

**Dependencies**: §3.1, §3.2, §3.3

**Effort**: ~45 minutes

---

## 4. Package Structure & Metadata

### 4.1 Create `setup.py` or `pyproject.toml`
**Description**: Package metadata and installation configuration.

**Contents**:
- Package name: `slugify`
- Version: `1.0.0`
- Description: "Convert text to URL-safe slugs"
- Entry point (if using `setup.py`): `console_scripts` for optional CLI executable
- Python version: `>=3.6` (or specify as needed)
- Dependencies: None (except `pytest` for dev)

**Acceptance Criteria**:
- `pip install -e .` installs package in dev mode
- `python -m slugify` works after installation
- `import slugify; slugify.slugify("test")` works

**Testing**: Manual installation test

**Dependencies**: §1.1, §3.1

**Effort**: ~15 minutes

---

### 4.2 Create `__init__.py` with proper exports
**Description**: Ensure `slugify/__init__.py` exports the `slugify()` function for library use.

**Contents**:
```python
from .core import slugify  # or inline definition

__all__ = ["slugify"]
__version__ = "1.0.0"
```

**Acceptance Criteria**:
- `from slugify import slugify` works
- `slugify("test")` is directly callable

**Testing**: Import test in §2.1

**Dependencies**: §1.1

**Effort**: ~5 minutes

---

## 5. Documentation

### 5.1 Write README.md
**Description**: User-facing documentation.

**Contents**:
- What is `slugify`?
- Installation instructions
- Basic usage examples (library + CLI)
- Examples of behavior (multiple separators, non-ASCII, edge cases)
- Limitations (no transliteration, no collapsing, no truncation)
- Out-of-scope features (for future versions)

**Acceptance Criteria**:
- README is clear and complete
- Examples are correct and representative

**Testing**: Manual review

**Dependencies**: §1.1, §3.1

**Effort**: ~30 minutes

---

### 5.2 Add docstrings to `slugify()` and CLI
**Description**: Inline documentation for developers.

**Contents**:
- Function docstring: parameters, returns, algorithm, examples
- Module docstring: package overview
- CLI help text: `--help` argument

**Acceptance Criteria**:
- `help(slugify)` provides clear information
- `python -m slugify --help` is helpful

**Testing**: Manual review

**Dependencies**: §1.1, §3.1

**Effort**: ~15 minutes

---

## 6. Validation & Release

### 6.1 Run full test suite
**Description**: Execute all unit and integration tests; verify coverage.

**Acceptance Criteria**:
- All tests pass (`pytest tests/`)
- Test coverage ≥ 90%
- No warnings or deprecations

**Testing**: `pytest tests/ --cov=slugify`

**Dependencies**: §2.1, §3.4, §4.1

**Effort**: ~10 minutes

---

### 6.2 Final acceptance testing
**Description**: Verify all acceptance criteria from requirements.

**Checklist**:
- [ ] AC-1.1: `slugify("Hello World")` → `"hello-world"`
- [ ] AC-1.2: `slugify("Héllo & Wörld!", separator="_")` → `"hllo__wrld"`
- [ ] AC-2.1: `python -m slugify "Hello World"` → `hello-world\n`
- [ ] AC-2.2: `python -m slugify ""` → exit 1
- [ ] AC-3.1: `python -m slugify "Hello World" --separator _` → `hello_world\n`
- [ ] AC-3.2: `python -m slugify "Hello World" --separator .` → `hello.world\n`
- [ ] AC-4.1: Non-empty slug → exit 0
- [ ] AC-4.2: Empty slug → exit 1
- [ ] stdin fallback works

**Testing**: Manual verification + automated test suite

**Dependencies**: §1.1, §3.1, §4.1, §6.1

**Effort**: ~20 minutes

---

## Implementation Sequence

**Phase 1: Core** (parallel-safe)
1. §1.1 Implement `slugify()` function
2. §1.2 Handle edge cases

**Phase 2: Testing** (depends on Phase 1)
3. §2.1 Write unit tests

**Phase 3: CLI** (depends on Phase 1)
4. §3.1 Argument parsing
5. §3.2 stdin fallback
6. §3.3 Exit code handling
7. §3.4 CLI integration tests

**Phase 4: Packaging** (depends on Phase 1 & 3)
8. §4.1 setup.py / pyproject.toml
9. §4.2 __init__.py exports

**Phase 5: Documentation** (depends on Phase 1 & 3)
10. §5.1 README
11. §5.2 Docstrings

**Phase 6: Release** (depends on all)
12. §6.1 Full test suite
13. §6.2 Final acceptance testing

---

## Summary

| Task | Duration | Dependencies |
|---|---|---|
| §1.1 Core implementation | 30 min | None |
| §1.2 Edge cases | 15 min | §1.1 |
| §2.1 Unit tests | 45 min | §1.1, §1.2 |
| §3.1 Argument parsing | 20 min | §1.1 |
| §3.2 stdin fallback | 20 min | §3.1 |
| §3.3 Exit codes | 15 min | §3.1, §3.2 |
| §3.4 CLI tests | 45 min | §3.1, §3.2, §3.3 |
| §4.1 setup.py | 15 min | §1.1, §3.1 |
| §4.2 __init__.py | 5 min | §1.1 |
| §5.1 README | 30 min | §1.1, §3.1 |
| §5.2 Docstrings | 15 min | §1.1, §3.1 |
| §6.1 Test suite | 10 min | §2.1, §3.4, §4.1 |
| §6.2 Acceptance | 20 min | All |
| **Total** | **285 min** (~4.75 hours) | |

**Critical path**: §1.1 → §1.2 → §2.1 → §3.1 → §3.2 → §3.3 → §3.4 → §6.1 → §6.2
