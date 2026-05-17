# Architecture Design — changelog-checker

**Date**: 2026-05-17
**Version**: 1.0.0

## Module Structure

```
src/changelog_checker/
  __init__.py          # 空，標記套件
  parser.py            # 解析 CHANGELOG.md → 結構化物件
  rules.py             # 5 條規則函式，各回傳 list[Violation]
  reporter.py          # 格式化輸出（text / JSON）
  cli.py               # argparse entry point
```

## Data Model

```python
@dataclass
class Violation:
    line: int
    rule: str           # "R1" .. "R5"
    message: str

@dataclass
class ParsedChangelog:
    has_unreleased: bool
    version_blocks: list[VersionBlock]
    raw_lines: list[str]

@dataclass
class VersionBlock:
    line: int
    version: str        # "1.0.0" | "Unreleased"
    date: str | None    # "2026-05-17" | None
    categories: list[str]
```

## Rules

| ID | Rule | Violation 條件 |
|----|------|---------------|
| R1 | unreleased-missing | 無 `## [Unreleased]` 區塊 |
| R2 | bad-date-format | 版本區塊日期不符 YYYY-MM-DD |
| R3 | unknown-category | `### X` 中 X 不在允許清單 |
| R4 | empty-unreleased | `[Unreleased]` 區塊無任何項目（warning 等級） |
| R5 | unreleased-not-first | `[Unreleased]` 不在第一個版本區塊位置 |

## Sequence Diagram

```
User → CLI: changelog-check path [--strict] [--json]
CLI → Parser: parse(path)
Parser → CLI: ParsedChangelog
CLI → Rules: check_all(changelog)
Rules → CLI: list[Violation]
CLI → Reporter: format(violations, mode)
Reporter → CLI: output string
CLI → stdout: print(output)
CLI → exit: 0 if not strict or no violations; 1 if strict + violations
```

## Reads / Writes

- **Reads**: `CHANGELOG.md`（使用者指定路徑），`CONTEXT.md`，`RULES.md`
- **Writes**: stdout / stderr（不寫入磁碟）
