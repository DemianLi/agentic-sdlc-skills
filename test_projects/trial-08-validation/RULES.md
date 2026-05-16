# RULES.md — trial-08-validation Project

## 1. Linter & Formatter Configuration

### Ruff (Python Linter & Formatter)
- **Line length**: 100 characters
- **Target Python**: 3.8+
- **Formatting rules**:
  - `I` (isort) — enforce grouped imports
  - `F` (Pyflakes) — catch undefined names
  - `E/W` (pycodestyle) — PEP8 enforcement

**Tool enforcement**: `pyproject.toml [tool.ruff]` + `ruff format` + `ruff check`

### Pytest (Testing)
- **Test discovery**: `tests/test_*.py`
- **Coverage threshold**: 80% (enforced at gate)
- **Coverage report**: `pytest --cov=src --cov-report=term-missing`

**Tool enforcement**: `pyproject.toml [tool.pytest.ini_options]`

## 2. Directory Structure Governance

```
trial-08-validation/
├── src/
│   └── string_stats.py
├── tests/
│   └── test_string_stats.py
├── docs/specs/
└── RULES.md
```

**Rule**: Production code must be in `src/`. Tests must be in `tests/`. Never mix.

## 3. Forbidden Patterns

| Pattern | Reason | Enforcement |
|---------|--------|-------------|
| `print()` in production code | Breaks testing; use logging instead | Manual review required |
| Bare `except:` | Masks bugs; use specific exceptions | `ruff` automatic |
| Functions > 20 lines | Complex = hard to test | Manual review required |
| Global state mutations | Breaks isolation | Manual review required |
| Hardcoded strings in business logic | Reduces testability | Manual review required |

## 4. Testing Discipline

| Rule | Enforcement |
|------|------------|
| No production code without failing test first (Iron Law) | Manual review in PR |
| Test names follow `test_<behavior>` | Manual review required |
| Coverage ≥ 80% before merge | `pytest --cov` gate (automatic) |

## 5. Toolchain Enforcement Map

| Rule Type | Tool | Command |
|-----------|------|---------|
| Formatting | Ruff | `ruff format src/ tests/` |
| Linting | Ruff | `ruff check src/ tests/` |
| Testing | Pytest | `pytest tests/ -v` |
| Coverage gate (≥80%) | pytest-cov | `pytest tests/ --cov=src --cov-report=term-missing` |
| Architecture boundaries | # manual review required | Code review checklist |
