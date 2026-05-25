"""
Smoke tests for s0-eval-alignment/scripts/scan.py

Run from repo root:
    pytest skills/s0-eval-alignment/tests/
"""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from scan import paranoid_judge, scan_skill, verify_test_coverage

FIXTURES = Path(__file__).parent / "fixtures"
REPO_ROOT = Path(__file__).parent.parent.parent.parent


@pytest.fixture()
def aligned():
    # eval_cases=None → has_tests skipped (defaults True)
    return scan_skill("skill-aligned", "test", FIXTURES)


@pytest.fixture()
def drifted():
    return scan_skill("skill-drifted", "test", FIXTURES)


# ---------------------------------------------------------------------------
# fixture-aligned: all checks must pass
# ---------------------------------------------------------------------------

def test_aligned_c1_gate(aligned):
    assert aligned["c1_gate"], "HARD-GATE block missing from fixture-aligned"

def test_aligned_c1_approval(aligned):
    assert aligned["c1_approval"], "'proceed immediately to' missing from fixture-aligned"

def test_aligned_c2_reads(aligned):
    assert aligned["c2_reads"], "Reads declaration missing from fixture-aligned"

def test_aligned_c2_writes(aligned):
    assert aligned["c2_writes"], "Writes declaration missing from fixture-aligned"

def test_aligned_c3_description(aligned):
    assert aligned["c3_pass"], "fixture-aligned description contains workflow verbs (C3 violation)"

def test_aligned_judge(aligned):
    assert aligned["judge"] == "ALIGNED", (
        f"fixture-aligned paranoid_judge verdict: {aligned['judge']} — issues: {aligned['judge_issues']}"
    )

def test_aligned_overall(aligned):
    assert aligned["status"] == "ALIGNED"


# ---------------------------------------------------------------------------
# fixture-drifted: C1 / C2 / C3 / judge must all fail; overall must be DRIFTED
# ---------------------------------------------------------------------------

def test_drifted_c1_gate_absent(drifted):
    assert not drifted["c1_gate"], "fixture-drifted should have no HARD-GATE"

def test_drifted_c1_approval_absent(drifted):
    assert not drifted["c1_approval"], "fixture-drifted should have no approval phrase"

def test_drifted_c2_reads_absent(drifted):
    assert not drifted["c2_reads"], "fixture-drifted should have no Reads declaration"

def test_drifted_c2_writes_absent(drifted):
    assert not drifted["c2_writes"], "fixture-drifted should have no Writes declaration"

def test_drifted_c3_violation(drifted):
    assert not drifted["c3_pass"], "fixture-drifted description should trigger C3 (has 'Step 1/2/3')"

def test_drifted_judge(drifted):
    assert drifted["judge"] == "DRIFTED", (
        f"fixture-drifted paranoid_judge should be DRIFTED; got {drifted['judge']}"
    )

def test_drifted_overall(drifted):
    assert drifted["status"] == "DRIFTED"


# ---------------------------------------------------------------------------
# paranoid_judge unit tests
# ---------------------------------------------------------------------------

def test_judge_j1_fails_on_no_steps():
    content = "<what-to-do>\nSome vague prose.\n</what-to-do>\n**DONE** ok\n**BLOCKED** fail\n"
    result = paranoid_judge(content)
    assert result["verdict"] == "DRIFTED"
    assert any("J1" in i for i in result["issues"])

def test_judge_j2_partial_on_missing_completion_report():
    content = (
        "<what-to-do>\n### Step 0\n### Step 1\n### Step 2\n</what-to-do>\n"
        "No completion report here.\n"
    )
    result = paranoid_judge(content)
    assert result["verdict"] == "PARTIAL"
    assert any("J2" in i for i in result["issues"])

def test_judge_aligned_on_full_content():
    content = (
        "<what-to-do>\n### Step 0\n### Step 1\n### Step 2\n### Step 3\n</what-to-do>\n"
        "## Completion Report\n- **DONE** ok\n- **BLOCKED** fail\n- **NEEDS_CONTEXT** info\n"
    )
    result = paranoid_judge(content)
    assert result["verdict"] == "ALIGNED"
    assert result["issues"] == []


# ---------------------------------------------------------------------------
# verify_test_coverage unit tests
# Uses monkeypatch to override _REPO_ROOT so tests are filesystem-isolated.
# ---------------------------------------------------------------------------

import scan as scan_module


def test_coverage_true_when_fixture_exists(tmp_path, monkeypatch):
    monkeypatch.setattr(scan_module, "_REPO_ROOT", tmp_path)
    fixture_dir = tmp_path / "tests" / "fixtures" / "my-skill"
    fixture_dir.mkdir(parents=True)
    (fixture_dir / "cases.json").write_text('[{"scenario": "ok"}]')
    assert verify_test_coverage("my-skill", tmp_path / "skills") is True


def test_coverage_false_when_fixture_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(scan_module, "_REPO_ROOT", tmp_path)
    assert verify_test_coverage("my-skill", tmp_path / "skills") is False


def test_coverage_false_when_empty_fixture(tmp_path, monkeypatch):
    monkeypatch.setattr(scan_module, "_REPO_ROOT", tmp_path)
    fixture_dir = tmp_path / "tests" / "fixtures" / "my-skill"
    fixture_dir.mkdir(parents=True)
    (fixture_dir / "cases.json").write_text("[]")
    assert verify_test_coverage("my-skill", tmp_path / "skills") is False


def test_coverage_false_when_invalid_json(tmp_path, monkeypatch):
    monkeypatch.setattr(scan_module, "_REPO_ROOT", tmp_path)
    fixture_dir = tmp_path / "tests" / "fixtures" / "my-skill"
    fixture_dir.mkdir(parents=True)
    (fixture_dir / "cases.json").write_text("not json")
    assert verify_test_coverage("my-skill", tmp_path / "skills") is False


# ---------------------------------------------------------------------------
# Integration: scan.py exit codes against real skills/
# ---------------------------------------------------------------------------

def test_real_skills_exit_zero():
    """28/28 ALIGNED → exit 0 (CI gate must pass on a clean repo)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "scan.py")],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"scan.py exited {result.returncode} — regression detected:\n{result.stdout}"
    )
