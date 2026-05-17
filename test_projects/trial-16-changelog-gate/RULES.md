# RULES.md — changelog-checker

## Directory Layout
```
src/changelog_checker/   # 主套件
tests/                   # pytest 測試（mirror src 結構）
dist/                    # build artifact
docs/arch/               # design.md, wbs.md, TASK_DAG.md
docs/audit/              # SAST + PR review 報告
```

## Coding Standards
- Python 3.9+，不使用任何第三方套件（stdlib only）
- 型別標注所有公開函式
- 每個公開函式必須有對應的 pytest 測試

## Forbidden Patterns
- 不使用 `subprocess` 或 `os.system`
- 不修改傳入的檔案（read-only scanner）
- 不使用 `print()` 以外的 I/O 作為主要輸出（CLI 工具）

## Git Conventions
- commit prefix: `feat/fix/test/docs/chore`
- 每個 atomic task 一個 commit

## Security
- 不接受 glob `**`（防止意外掃描大型目錄）
- 路徑驗證：僅接受 `.md` 副檔名
