# Coverage Gate — s4-tdd

## Step 0 — Detect Project Mode

Before running any coverage command, check `RULES.md` for a `mode:` field:

```
mode: brownfield   → activate Characterization Test Mode (see below)
mode: greenfield   → use standard threshold gate
(field absent)     → use standard threshold gate
```

---

## Standard Mode (greenfield or unset)

After all behaviors are GREEN, run the coverage report and check against the threshold in `RULES.md` (default: 80% if not specified):

```bash
pytest --cov=. --cov-report=term-missing
```

| Coverage | Status |
|----------|--------|
| ≥ threshold | **DONE** — attach coverage summary |
| 60% – threshold | **DONE_WITH_CONCERNS** — list uncovered lines and why |
| < 60% | **BLOCKED** — coverage too low; add tests before proceeding |

Do NOT self-report coverage. Paste the actual `pytest --cov` terminal output.

---

## Characterization Test Mode (brownfield)

Legacy codebases often have zero existing tests. Blocking on 80% total coverage would freeze all progress. In brownfield mode:

**Goal**: cover the code YOU added or modified in this task — not the pre-existing legacy lines.

```bash
# Run coverage scoped to files touched in this task only
pytest --cov=<module_you_changed> --cov-report=term-missing
```

| Coverage of new/modified lines | Status |
|-------------------------------|--------|
| ≥ 80% of YOUR new lines | **DONE** — attach scoped coverage summary |
| 60–79% of YOUR new lines | **DONE_WITH_CONCERNS** — list which new lines are uncovered and why |
| < 60% of YOUR new lines | **BLOCKED** — even in brownfield, your own new code must be tested |

Report header must read:
```
BROWNFIELD MODE: coverage scoped to new/modified lines only.
Pre-existing untested code excluded from gate.
```

**What this is NOT**: a license to skip tests. You still TDD every new behavior. The gate just doesn't penalize pre-existing legacy debt you didn't create.
