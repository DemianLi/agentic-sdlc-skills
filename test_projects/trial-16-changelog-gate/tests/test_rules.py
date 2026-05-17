"""Tests for changelog_checker.rules — RED before writing rules.py."""
import textwrap
from changelog_checker.parser import parse
from changelog_checker.rules import check_all, Violation

COMPLIANT = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [1.0.0] - 2026-05-17
    ### Added
    - Initial release
""")

NO_UNRELEASED = textwrap.dedent("""\
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

UNKNOWN_CAT = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [1.0.0] - 2026-05-17
    ### Improvements
    - Something
""")

UNRELEASED_NOT_FIRST = textwrap.dedent("""\
    # Changelog

    ## [1.0.0] - 2026-05-17
    ### Added
    - Initial release

    ## [Unreleased]
""")


def test_compliant_no_violations():
    result = check_all(parse(COMPLIANT))
    assert result == []


def test_r1_missing_unreleased():
    violations = check_all(parse(NO_UNRELEASED))
    rules = [v.rule for v in violations]
    assert "R1" in rules


def test_r2_bad_date():
    violations = check_all(parse(BAD_DATE))
    rules = [v.rule for v in violations]
    assert "R2" in rules


def test_r3_unknown_category():
    violations = check_all(parse(UNKNOWN_CAT))
    rules = [v.rule for v in violations]
    assert "R3" in rules


def test_r5_unreleased_not_first():
    violations = check_all(parse(UNRELEASED_NOT_FIRST))
    rules = [v.rule for v in violations]
    assert "R5" in rules


def test_violation_has_fields():
    violations = check_all(parse(NO_UNRELEASED))
    v = violations[0]
    assert isinstance(v, Violation)
    assert hasattr(v, "line")
    assert hasattr(v, "rule")
    assert hasattr(v, "message")
