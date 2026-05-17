# Vision — changelog-checker

## Problem Statement
CHANGELOG.md 格式不一致，導致：
1. CI pipeline 無法可靠解析版本歷史
2. 人工 review 耗時（reviewer 需手動對比 keepachangelog.com 規範）
3. 每次 release 時才發現格式問題（修復成本高）

## Target Users
- **개발者**: 撰寫 CHANGELOG 後想在本地驗證格式
- **CI maintainer**: 在 PR gate 中加入格式檢查

## Proposed Approach
一個 Python stdlib-only CLI 工具：
```bash
changelog-check CHANGELOG.md          # 輸出人類可讀結果
changelog-check CHANGELOG.md --json   # 輸出機器可讀 JSON
changelog-check CHANGELOG.md --strict # exit 1 on any violation (CI 用)
```

## Acceptance Criteria
- AC-1: 能偵測缺少 `[Unreleased]` 區塊
- AC-2: 能偵測版本區塊日期格式錯誤
- AC-3: 能偵測未知的類別標頭（非 Keep a Changelog 規範）
- AC-4: `--strict` 模式下有 violation 時 exit 1
- AC-5: stdlib only，無需 pip install 第三方套件
