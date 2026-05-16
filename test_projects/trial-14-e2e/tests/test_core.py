"""Unit tests for mdtoc core functions — written before implementation (TDD)."""
import pytest
from mdtoc.core import Header, parse_headers, generate_toc, insert_toc


# ── REQ-1: parse_headers ────────────────────────────────────────────────────

class TestParseHeaders:
    def test_returns_headers_at_all_levels(self):
        # AC-1.1
        text = "# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6"
        result = parse_headers(text)
        assert result == [
            Header(1, "H1"),
            Header(2, "H2"),
            Header(3, "H3"),
            Header(4, "H4"),
            Header(5, "H5"),
            Header(6, "H6"),
        ]

    def test_ignores_heading_without_space(self):
        # AC-1.2
        text = "#NotAHeading\n# Valid Heading"
        result = parse_headers(text)
        assert len(result) == 1
        assert result[0] == Header(1, "Valid Heading")

    def test_strips_heading_text(self):
        # AC-1.3
        text = "##  Hello  "
        result = parse_headers(text)
        assert result == [Header(2, "Hello")]

    def test_returns_empty_for_no_headings(self):
        # AC-1.4
        text = "Just some paragraph text.\nNo headings here."
        result = parse_headers(text)
        assert result == []

    def test_skips_headings_inside_code_block(self):
        text = "```\n# Not a heading\n```\n# Real heading"
        result = parse_headers(text)
        assert result == [Header(1, "Real heading")]

    def test_skips_headings_inside_tilde_code_block(self):
        text = "~~~\n## Not a heading\n~~~\n## Real heading"
        result = parse_headers(text)
        assert result == [Header(2, "Real heading")]


# ── REQ-2: generate_toc ─────────────────────────────────────────────────────

class TestGenerateToc:
    def test_basic_nested_structure(self):
        # AC-2.1
        headers = [Header(1, "Intro"), Header(2, "Usage"), Header(3, "Examples")]
        result = generate_toc(headers)
        assert result == (
            "- [Intro](#intro)\n"
            "  - [Usage](#usage)\n"
            "    - [Examples](#examples)"
        )

    def test_anchor_slug_lowercases_and_hyphens(self):
        # AC-2.2
        headers = [Header(1, "My Section Title")]
        result = generate_toc(headers)
        assert "- [My Section Title](#my-section-title)" in result

    def test_anchor_slug_removes_special_chars(self):
        headers = [Header(1, "Hello, World! (2024)")]
        result = generate_toc(headers)
        assert "#hello-world-2024" in result

    def test_max_level_excludes_deeper_headings(self):
        # AC-2.3
        headers = [Header(1, "A"), Header(2, "B"), Header(3, "C")]
        result = generate_toc(headers, max_level=2)
        assert "A" in result
        assert "B" in result
        assert "C" not in result

    def test_empty_headers_returns_empty_string(self):
        # AC-2.4
        assert generate_toc([]) == ""

    def test_single_header_produces_one_entry(self):
        headers = [Header(2, "Only One")]
        result = generate_toc(headers)
        assert result == "  - [Only One](#only-one)"


# ── REQ-3: insert_toc ───────────────────────────────────────────────────────

class TestInsertToc:
    def test_replaces_content_between_markers(self):
        # AC-3.1
        text = "# Doc\n\n<!-- TOC -->\nold content\n<!-- /TOC -->\n\nBody."
        toc = "- [Doc](#doc)"
        result = insert_toc(text, toc)
        assert "<!-- TOC -->\n- [Doc](#doc)\n<!-- /TOC -->" in result
        assert "old content" not in result

    def test_prepends_toc_when_no_markers(self):
        # AC-3.2
        text = "# Doc\n\nBody text."
        toc = "- [Doc](#doc)"
        result = insert_toc(text, toc)
        assert result.startswith("<!-- TOC -->")
        assert "- [Doc](#doc)" in result
        assert "Body text." in result

    def test_idempotent(self):
        # AC-3.3
        text = "# Doc\n\nBody text."
        toc = "- [Doc](#doc)"
        first = insert_toc(text, toc)
        second = insert_toc(first, toc)
        assert first == second

    def test_ignores_markers_inside_code_block(self):
        # AC-3.4
        text = "```\n<!-- TOC -->\n<!-- /TOC -->\n```\n\n# Doc"
        toc = "- [Doc](#doc)"
        result = insert_toc(text, toc)
        assert result.startswith("<!-- TOC -->")

    def test_preserves_content_outside_markers(self):
        text = "Preamble.\n\n<!-- TOC -->\nold\n<!-- /TOC -->\n\nPostamble."
        toc = "- [New](#new)"
        result = insert_toc(text, toc)
        assert "Preamble." in result
        assert "Postamble." in result
