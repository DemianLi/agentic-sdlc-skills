# Changelog

All notable changes to changelog-checker are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]

## [1.0.0] - 2026-05-17

### Added
- `parser.py` — parse CHANGELOG.md into `ParsedChangelog` + `VersionBlock` dataclasses
- `rules.py` — 5 rules: R1 (missing [Unreleased]), R2 (bad date), R3 (unknown category), R4 (empty unreleased), R5 (unreleased not first)
- `reporter.py` — text and JSON output formatters
- `cli.py` — argparse entry point with `--strict` and `--json` flags
- 21 pytest tests (8 parser, 6 rules, 7 CLI integration)
- `dist/changelog_checker-1.0.0-py3-none-any.whl`
