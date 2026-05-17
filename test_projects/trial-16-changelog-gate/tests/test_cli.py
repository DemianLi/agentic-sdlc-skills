"""Integration tests for the CLI — run via subprocess."""
import json
import subprocess
import sys
import textwrap
import tempfile
from pathlib import Path

TRIAL_DIR = Path(__file__).parent.parent
SRC = TRIAL_DIR / "src"

COMPLIANT_CONTENT = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [1.0.0] - 2026-05-17
    ### Added
    - Initial release
""")

FAILING_CONTENT = textwrap.dedent("""\
    # Changelog

    ## [1.0.0] - 2026-5-1
    ### Improvements
    - Something
""")


def run_cli(*args, content=COMPLIANT_CONTENT):
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
        f.write(content)
        tmp = Path(f.name)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "changelog_checker.cli", str(tmp), *args],
            capture_output=True, text=True,
            env={**__import__("os").environ, "PYTHONPATH": str(SRC)},
        )
        return result
    finally:
        tmp.unlink()


def test_compliant_exits_zero():
    r = run_cli()
    assert r.returncode == 0


def test_compliant_prints_pass():
    r = run_cli()
    assert "PASS" in r.stdout


def test_failing_exits_zero_without_strict():
    r = run_cli(content=FAILING_CONTENT)
    assert r.returncode == 0


def test_failing_strict_exits_one():
    r = run_cli("--strict", content=FAILING_CONTENT)
    assert r.returncode == 1


def test_json_output_valid():
    r = run_cli("--json")
    data = json.loads(r.stdout)
    assert "status" in data
    assert "violations" in data


def test_json_fail_has_violations():
    r = run_cli("--json", content=FAILING_CONTENT)
    data = json.loads(r.stdout)
    assert data["status"] == "FAIL"
    assert len(data["violations"]) > 0


def test_bad_extension_exits_two():
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
        f.write("anything")
        tmp = Path(f.name)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "changelog_checker.cli", str(tmp)],
            capture_output=True, text=True,
            env={**__import__("os").environ, "PYTHONPATH": str(SRC)},
        )
        assert result.returncode == 2
    finally:
        tmp.unlink()
