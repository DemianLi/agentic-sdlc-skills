"""Format compliance results as text or JSON."""
from __future__ import annotations
import json
from .rules import Violation


def format_text(violations: list[Violation], path: str) -> str:
    if not violations:
        return f"PASS: {path} — compliant with Keep a Changelog"
    lines = [f"FAIL: {path} — {len(violations)} violation(s)"]
    for v in violations:
        lines.append(f"  Line {v.line:>3} [{v.rule}] {v.message}")
    return "\n".join(lines)


def format_json(violations: list[Violation], path: str) -> str:
    return json.dumps({
        "status": "PASS" if not violations else "FAIL",
        "path": path,
        "violations": [
            {"line": v.line, "rule": v.rule, "message": v.message}
            for v in violations
        ],
    }, indent=2)
