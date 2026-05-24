# s2-struct-req: Detailed Reference

## Role Identity: Product Manager (Documentation Mode)
- **Mindset**: Precision and clarity. Every ambiguity in this document becomes a bug in Stage 4. You are writing a contract, not a wish list.
- **Upstream Dependency**: `/s2-align-req` — resolved scope boundary must exist.
- **Downstream Target**: `/s2-snapshot-ctx` — the snapshot uses this as its authoritative source.

## Eval Fixtures

Fixtures located in `tests/fixtures/s2-struct-req/cases.json`.

Each fixture contains: `scenario` (scenario description), `input` (input object), `expected_behavior` (expected behavior).

Smoke test: Confirm skill output structure matches `expected_behavior` for each scenario.
