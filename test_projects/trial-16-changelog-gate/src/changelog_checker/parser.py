"""Parse a CHANGELOG.md string into structured objects."""
from __future__ import annotations
import re
from dataclasses import dataclass, field


@dataclass
class VersionBlock:
    line: int
    version: str
    date: str | None
    categories: list[str] = field(default_factory=list)


@dataclass
class ParsedChangelog:
    has_unreleased: bool
    version_blocks: list[VersionBlock]
    raw_lines: list[str]


_VERSION_RE = re.compile(
    r"^##\s+\[(?P<version>[^\]]+)\](?:\s+-\s+(?P<date>\S+))?",
    re.IGNORECASE,
)
_CATEGORY_RE = re.compile(r"^###\s+(.+)")


def parse(text: str) -> ParsedChangelog:
    lines = text.splitlines()
    blocks: list[VersionBlock] = []
    current: VersionBlock | None = None

    for i, line in enumerate(lines, start=1):
        m = _VERSION_RE.match(line)
        if m:
            current = VersionBlock(
                line=i,
                version=m.group("version"),
                date=m.group("date"),
            )
            blocks.append(current)
            continue
        cat = _CATEGORY_RE.match(line)
        if cat and current is not None:
            current.categories.append(cat.group(1).strip())

    has_unreleased = any(b.version.lower() == "unreleased" for b in blocks)
    return ParsedChangelog(
        has_unreleased=has_unreleased,
        version_blocks=blocks,
        raw_lines=lines,
    )
