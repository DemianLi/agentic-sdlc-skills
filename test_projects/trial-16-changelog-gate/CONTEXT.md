# CONTEXT.md — changelog-checker 領域詞彙

## 核心概念

| 術語 | 定義 |
|------|------|
| **Keep a Changelog** | changelog.md 格式規範 (keepachangelog.com)：頂部 `[Unreleased]`，版本區塊格式 `## [x.y.z] - YYYY-MM-DD` |
| **Compliance** | 所有必要結構元素齊全且格式正確 |
| **Violation** | 任何不符合 Keep a Changelog 規範的項目（missing section, bad date, unknown category） |
| **Category** | Keep a Changelog 定義的 7 種標頭：Added / Changed / Deprecated / Removed / Fixed / Security / Breaking |
| **Version block** | `## [x.y.z] - YYYY-MM-DD` 格式的區塊 |
| **Unreleased block** | `## [Unreleased]` 區塊（必須存在於檔案頂部） |
| **Compliance report** | 工具輸出的結構化結果：`{status, violations: [{line, rule, message}]}` |

## 工具邊界

- **In scope**: 格式合規性（結構、標頭、日期格式）
- **Out of scope**: 語義品質（項目描述是否清晰）、版本號語意（SemVer）

## 角色

- **Linter**: 工具本身，read-only 掃描
- **Author**: changelog 撰寫者（工具的使用者）
- **CI Gate**: 在 PR pipeline 中使用此工具的自動化系統
