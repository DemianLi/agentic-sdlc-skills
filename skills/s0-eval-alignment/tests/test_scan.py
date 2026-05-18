"""
Smoke tests for s0-eval-alignment/scripts/scan.py

Run from repo root:
    pytest skills/s0-eval-alignment/tests/
"""

import subprocess
import sys
from pathlib import Path

import pytest

# Import scan module directly so we can monkeypatch internals
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import scan as scan_module
from scan import scan_skill

FIXTURES = Path(__file__).parent / "fixtures"
REPO_ROOT = Path(__file__).parent.parent.parent.parent

# Keywords that actually appear in the fixture-aligned SKILL.md body
_FIXTURE_KEYWORDS = {
    "skill-aligned": ["vision", "idea", "business", "spec", "Workflow"],
    "skill-drifted": ["vision", "idea", "business", "spec", "Workflow"],
}


@pytest.fixture()
def aligned(monkeypatch):
    monkeypatch.setattr(scan_module, "KEYWORDS", _FIXTURE_KEYWORDS)
    return scan_skill("skill-aligned", "test", FIXTURES)


@pytest.fixture()
def drifted(monkeypatch):
    monkeypatch.setattr(scan_module, "KEYWORDS", _FIXTURE_KEYWORDS)
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

def test_aligned_q_keywords(aligned):
    assert aligned["q"] == "ALIGNED", f"fixture-aligned keyword hits: {aligned['q_hits']} (need ≥3)"

def test_aligned_overall(aligned):
    assert aligned["status"] == "ALIGNED"


# ---------------------------------------------------------------------------
# fixture-drifted: C1 / C2 / C3 must all fail; overall must be DRIFTED
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

def test_drifted_overall(drifted):
    assert drifted["status"] == "DRIFTED"


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
