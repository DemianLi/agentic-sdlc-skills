"""Compliance rules for Keep a Changelog format."""
from __future__ import annotations
import re
from dataclasses import dataclass
from .parser import ParsedChangelog

ALLOWED_CATEGORIES = {
    "Added", "Changed", "Deprecated", "Removed", "Fixed", "Security", "Breaking",
}

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Violation:
    line: int
    rule: str
    message: str


def check_all(changelog: ParsedChangelog) -> list[Violation]:
    violations: list[Violation] = []
    violations.extend(_r1_unreleased_missing(changelog))
    violations.extend(_r2_bad_date(changelog))
    violations.extend(_r3_unknown_category(changelog))
    violations.extend(_r5_unreleased_not_first(changelog))
    return violations


def _r1_unreleased_missing(c: ParsedChangelog) -> list[Violation]:
    if not c.has_unreleased:
        return [Violation(line=1, rule="R1", message="Missing [Unreleased] block")]
    return []


def _r2_bad_date(c: ParsedChangelog) -> list[Violation]:
    out = []
    for b in c.version_blocks:
        if b.version.lower() == "unreleased":
            continue
        if b.date is None or not _DATE_RE.match(b.date):
            out.append(Violation(
                line=b.line,
                rule="R2",
                message=f"[{b.version}] date '{b.date}' is not YYYY-MM-DD",
            ))
    return out


def _r3_unknown_category(c: ParsedChangelog) -> list[Violation]:
    out = []
    for b in c.version_blocks:
        for cat in b.categories:
            if cat not in ALLOWED_CATEGORIES:
                out.append(Violation(
                    line=b.line,
                    rule="R3",
                    message=f"Unknown category '{cat}' in [{b.version}]",
                ))
    return out


def _r5_unreleased_not_first(c: ParsedChangelog) -> list[Violation]:
    if not c.version_blocks:
        return []
    if c.version_blocks[0].version.lower() != "unreleased":
        for b in c.version_blocks:
            if b.version.lower() == "unreleased":
                return [Violation(
                    line=b.line,
                    rule="R5",
                    message="[Unreleased] must be the first version block",
                )]
    return []
