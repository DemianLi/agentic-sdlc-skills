# WBS — changelog-checker

每個 task ≤5 分鐘。

| ID | Task | Outputs |
|----|------|---------|
| T1 | `parser.py` — `parse()` 函式，回傳 `ParsedChangelog` | `parser.py` |
| T2 | `rules.py` — R1 + R5（Unreleased 相關） | `rules.py` (R1, R5) |
| T3 | `rules.py` — R2（日期格式） | `rules.py` + R2 |
| T4 | `rules.py` — R3（unknown category） | `rules.py` + R3 |
| T5 | `rules.py` — R4（empty unreleased, warning） | `rules.py` + R4 |
| T6 | `reporter.py` — text + JSON 格式輸出 | `reporter.py` |
| T7 | `cli.py` — argparse + exit code | `cli.py` |
| T8 | `tests/test_parser.py` | 測試 T1 |
| T8b| `tests/test_rules.py` | 測試 T2–T5 |
| T9 | `tests/test_cli.py` — integration (subprocess) | end-to-end 測試 |
