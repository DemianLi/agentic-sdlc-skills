# Structured Requirements — changelog-checker

## User Stories

### US-1: 本地格式驗證
> As a 開發者，I want to run `changelog-check CHANGELOG.md` and see a list of violations，so that I can fix formatting before committing.

**Acceptance Criteria (Gherkin):**
```gherkin
Given a CHANGELOG.md with missing [Unreleased] section
When I run changelog-check CHANGELOG.md
Then I see "VIOLATION: missing [Unreleased] block"
And the exit code is 0 (report mode, not strict)
```

### US-2: CI 強制執行
> As a CI maintainer，I want `changelog-check --strict` to exit 1 on violations，so that non-compliant changelogs are blocked at PR gate.

**Acceptance Criteria:**
```gherkin
Given a CHANGELOG.md with date format "2026-5-1" (not YYYY-MM-DD)
When I run changelog-check CHANGELOG.md --strict
Then exit code is 1
And stderr contains the violation details
```

### US-3: JSON 機器輸出
> As a CI pipeline，I want `--json` output，so that I can parse violations programmatically.

**Acceptance Criteria:**
```gherkin
Given a CHANGELOG.md with 2 violations
When I run changelog-check CHANGELOG.md --json
Then stdout is valid JSON: {"status": "FAIL", "violations": [...]}
```

## Out of Scope
- 版本號語意驗證（SemVer）
- 重複版本號偵測
- 語言/拼字檢查
