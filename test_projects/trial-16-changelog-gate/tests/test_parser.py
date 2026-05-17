"""Tests for changelog_checker.parser — RED before any production code."""
import textwrap
from changelog_checker.parser import parse, ParsedChangelog, VersionBlock


MINIMAL_COMPLIANT = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [1.0.0] - 2026-05-17
    ### Added
    - Initial release
""")

MISSING_UNRELEASED = textwrap.dedent("""\
    # Changelog

    ## [1.0.0] - 2026-05-17
    ### Added
    - Initial release
""")

BAD_DATE = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [1.0.0] - 2026-5-1
    ### Added
    - Initial release
""")

UNKNOWN_CATEGORY = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [1.0.0] - 2026-05-17
    ### Improvements
    - Something
""")


def test_parse_returns_parsed_changelog():
    result = parse(MINIMAL_COMPLIANT)
    assert isinstance(result, ParsedChangelog)


def test_parse_detects_unreleased():
    result = parse(MINIMAL_COMPLIANT)
    assert result.has_unreleased is True


def test_parse_no_unreleased():
    result = parse(MISSING_UNRELEASED)
    assert result.has_unreleased is False


def test_parse_version_blocks_count():
    result = parse(MINIMAL_COMPLIANT)
    # [Unreleased] + [1.0.0]
    assert len(result.version_blocks) == 2


def test_parse_version_block_date():
    result = parse(MINIMAL_COMPLIANT)
    versioned = [b for b in result.version_blocks if b.version != "Unreleased"]
    assert versioned[0].date == "2026-05-17"


def test_parse_version_block_bad_date_preserved():
    result = parse(BAD_DATE)
    versioned = [b for b in result.version_blocks if b.version != "Unreleased"]
    assert versioned[0].date == "2026-5-1"


def test_parse_categories():
    result = parse(UNKNOWN_CATEGORY)
    versioned = [b for b in result.version_blocks if b.version != "Unreleased"]
    assert "Improvements" in versioned[0].categories


def test_parse_raw_lines_nonempty():
    result = parse(MINIMAL_COMPLIANT)
    assert len(result.raw_lines) > 0
