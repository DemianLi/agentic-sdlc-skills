"""Pure core functions for Markdown TOC generation."""
from __future__ import annotations
import re
from dataclasses import dataclass


@dataclass
class Header:
    level: int
    text: str


_ATX_RE = re.compile(r'^(#{1,6}) (.+)')
_FENCE_RE = re.compile(r'^(`{3,}|~{3,})')
_TOC_START = "<!-- TOC -->"
_TOC_END = "<!-- /TOC -->"


def parse_headers(text: str) -> list[Header]:
    """Extract ATX headings from Markdown text, skipping fenced code blocks."""
    headers: list[Header] = []
    in_fence = False
    fence_char = ""
    for line in text.splitlines():
        m = _FENCE_RE.match(line)
        if m:
            char = m.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_char = char
            elif char == fence_char:
                in_fence = False
            continue
        if in_fence:
            continue
        m = _ATX_RE.match(line)
        if m:
            headers.append(Header(level=len(m.group(1)), text=m.group(2).strip()))
    return headers


def _slugify(text: str) -> str:
    slug = text.lower()
    slug = slug.replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug


def generate_toc(headers: list[Header], max_level: int = 3) -> str:
    """Format headers as a nested Markdown TOC string."""
    lines: list[str] = []
    for h in headers:
        if h.level > max_level:
            continue
        indent = "  " * (h.level - 1)
        slug = _slugify(h.text)
        lines.append(f"{indent}- [{h.text}](#{slug})")
    return "\n".join(lines)


def _find_markers_outside_fences(lines: list[str]) -> tuple[int, int] | tuple[None, None]:
    """Return (start_idx, end_idx) of TOC markers outside code fences, or (None, None)."""
    in_fence = False
    fence_char = ""
    start = None
    for i, line in enumerate(lines):
        m = _FENCE_RE.match(line)
        if m:
            char = m.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_char = char
            elif char == fence_char:
                in_fence = False
            continue
        if in_fence:
            continue
        stripped = line.rstrip()
        if stripped == _TOC_START:
            start = i
        elif stripped == _TOC_END and start is not None:
            return start, i
    return None, None


def insert_toc(text: str, toc: str) -> str:
    """Insert or replace TOC markers in Markdown text. Returns updated text."""
    lines = text.splitlines(keepends=True)
    # Normalize: work with stripped-end lines for marker detection
    stripped_lines = [l.rstrip("\n") for l in lines]

    start, end = _find_markers_outside_fences(stripped_lines)

    toc_block = [_TOC_START + "\n"] + [line + "\n" for line in toc.splitlines()] + [_TOC_END + "\n"]

    if start is not None and end is not None:
        new_lines = lines[:start] + toc_block + lines[end + 1:]
    else:
        # Prepend TOC block with a blank line separator
        new_lines = toc_block + ["\n"] + lines

    result = "".join(new_lines)
    # Don't add a trailing newline that wasn't there originally
    if not text.endswith("\n") and result.endswith("\n"):
        result = result[:-1]
    return result
