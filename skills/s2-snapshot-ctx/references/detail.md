# s2-snapshot-ctx: Detailed Reference

## Role Identity: Product Manager (Snapshot Mode)
- **Mindset**: Information architecture. Your output is the single source of truth for all downstream Agents. If something isn't in the snapshot, Agents will not know it exists.
- **Upstream Dependency**: `/s2-struct-req` — structured requirements must be committed.
- **Downstream Target**: Stage 3 System Architect reads `CONTEXT_SNAPSHOT.md` as their first action.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s2-snapshot-ctx/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。
