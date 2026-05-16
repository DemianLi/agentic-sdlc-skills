# RULES.md — String Stats API

## Section 1: Linter / Formatter
- **Formatter**: Ruff (`ruff format src/ tests/`)
- **Linter**: Ruff (`ruff check src/ tests/`)
- **Line length**: 88 characters
- **Target Python**: 3.9+

## Section 2: Directory Structure
- `src/` — production code only
- `tests/unit/` — unit tests for pure functions
- `tests/integration/` — API-to-core boundary tests
- `tests/e2e/` — end-to-end user flow tests
- `tests/perf/` — performance benchmark tests
- `docs/specs/` — requirements documents
- `docs/tests/` — test result artifacts
- `docs/audit/` — audit reports

## Section 3: Forbidden Patterns
- No `print()` in production code (`# enforce: ruff`)
- No bare `except:` (`# enforce: ruff E722`)
- No functions > 20 lines (`# enforce: ruff PLR0912`)
- No global state mutation (`# manual review required`)
- No hardcoded strings in production logic (`# manual review required`)

## Section 4: Testing Rules
- All tests must follow `test_<behavior>` naming
- Every public function must have at least one test
- Test coverage threshold: **80%**
- Coverage command: `pytest --cov=src --cov-report=term-missing`

## Section 5: Toolchain Enforcement Map

| Rule Type | Tool | Command |
|-----------|------|---------|
| Formatting | Ruff | `ruff format src/ tests/` |
| Linting | Ruff | `ruff check src/ tests/` |
| Testing | Pytest | `pytest tests/ -v` |
| Coverage gate (≥80%) | pytest-cov | `pytest tests/ --cov=src --cov-report=term-missing` |
| Architecture boundaries | # manual review required | Code review checklist |

## Section 6: Performance SLO
- `word_count`: P99 < 1ms for text up to 10,000 characters
- `char_count`: P99 < 1ms for text up to 10,000 characters
- `sentence_count`: P99 < 2ms for text up to 10,000 characters
- `paragraph_count`: P99 < 1ms for text up to 10,000 characters
- API endpoint `GET /analyze`: P99 < 50ms for text up to 10,000 characters (ASGI transport)
