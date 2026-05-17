"""CLI entry point for changelog-checker."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from .parser import parse
from .rules import check_all
from .reporter import format_text, format_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="changelog-check",
        description="Keep a Changelog compliance checker",
    )
    parser.add_argument("path", help="Path to CHANGELOG.md")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on violations")
    args = parser.parse_args(argv)

    p = Path(args.path)
    if not p.suffix == ".md":
        print(f"ERROR: {p} is not a .md file", file=sys.stderr)
        return 2
    if not p.exists():
        print(f"ERROR: {p} not found", file=sys.stderr)
        return 2

    text = p.read_text(encoding="utf-8")
    changelog = parse(text)
    violations = check_all(changelog)

    output = format_json(violations, str(p)) if args.json else format_text(violations, str(p))
    print(output)

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
