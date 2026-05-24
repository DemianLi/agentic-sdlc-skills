"""
Regression test: every skill with real (non-sentinel) prerequisites must have a
--check-prereqs call in its SKILL.md HARD-GATE.

"Real" means the prerequisite skill's outputs list is non-empty (file globs).
Sentinel-based skills (outputs: []) cannot be verified by the engine because no
SKILL.md creates the .{skill}.done sentinel file — those consumers are intentionally
excluded from this gate.

Add a skill name to INTENTIONAL_EXCEPTIONS only when there is a documented reason
why the prerequisite check cannot work (see inline comments).
"""

import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "skill_graph_schema.yaml"
SKILLS_DIR = REPO_ROOT / "skills"

# Skills whose check-prereqs cannot work correctly and are excluded by design.
# Each entry must have an inline comment explaining why.
INTENTIONAL_EXCEPTIONS = {
    "s2-capture-vision",  # docs/adr/*-tech-stack.md legitimately absent in brownfield projects
}

sys.path.insert(0, str(REPO_ROOT / "skills" / "s0-eval-alignment" / "scripts"))
from engine import SkillGraphEngine


def _sentinel_skills(skills: dict) -> set:
    return {name for name, info in skills.items() if not info.get("outputs")}


def _requires_real_prereqs(skill_name: str, info: dict, sentinel_skills: set) -> list:
    """Return requires entries that are NOT sentinel-producing."""
    return [r for r in info.get("requires", []) if r not in sentinel_skills]


def _has_check_prereqs(skill_name: str) -> bool:
    skill_md = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_md.exists():
        return False
    return "--check-prereqs" in skill_md.read_text()


def _load_skills() -> dict:
    engine = SkillGraphEngine(schema_path=str(SCHEMA_PATH), workspace_dir=str(REPO_ROOT))
    return engine.skills


@pytest.fixture(scope="module")
def skills():
    return _load_skills()


@pytest.fixture(scope="module")
def sentinel_set(skills):
    return _sentinel_skills(skills)


def _coverable_skills(skills, sentinel_set):
    """Skills that have ≥1 real (non-sentinel) prerequisite and are not exceptions."""
    result = []
    for name, info in skills.items():
        if name in INTENTIONAL_EXCEPTIONS:
            continue
        real_prereqs = _requires_real_prereqs(name, info, sentinel_set)
        if real_prereqs:
            result.append(name)
    return sorted(result)


def test_all_coverable_skills_have_check_prereqs(skills, sentinel_set):
    """
    Every skill with at least one real-file prerequisite must have
    --check-prereqs in its SKILL.md.
    """
    missing = []
    for name in _coverable_skills(skills, sentinel_set):
        if not _has_check_prereqs(name):
            real_prereqs = _requires_real_prereqs(name, skills[name], sentinel_set)
            missing.append((name, real_prereqs))

    if missing:
        lines = ["Skills with real prerequisites but missing --check-prereqs:\n"]
        for skill, prereqs in missing:
            lines.append(f"  {skill}  (requires: {prereqs})")
        lines.append(
            "\nFix: add Step 0 to the HARD-GATE section of each skill's SKILL.md:\n"
            "  Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for <skill>`\n"
            "  If it reports any missing prerequisite, follow its suggestion and **STOP**."
        )
        pytest.fail("\n".join(lines))


def test_intentional_exceptions_still_exist_in_graph(skills):
    """
    Guard against INTENTIONAL_EXCEPTIONS becoming stale: every name in the set
    must still be a real skill in the graph.
    """
    missing = [name for name in INTENTIONAL_EXCEPTIONS if name not in skills]
    if missing:
        pytest.fail(
            f"INTENTIONAL_EXCEPTIONS contains skills not in the graph: {missing}\n"
            "Remove them from the exception set."
        )


def test_no_sentinel_skills_accidentally_gain_file_outputs(skills, sentinel_set):
    """
    If a previously sentinel-producing skill gains real outputs in the schema,
    its downstream consumers may now be coverable — surface that opportunity.

    This test documents the current known-sentinel set so changes are visible.
    """
    known_sentinels = {
        "s1-git-guardrails",
        "s4-setup-env",
        "s4-impl-task",
        "s4-tdd",
        "s4-local-debug",
        "s5-fix-optimize",
        "s7-build-artifact",
    }
    new_sentinels = sentinel_set - known_sentinels
    removed_sentinels = known_sentinels - sentinel_set

    if new_sentinels:
        pytest.fail(
            f"New sentinel skills detected (outputs: []): {sorted(new_sentinels)}\n"
            "Their downstream consumers cannot use --check-prereqs until sentinels are created.\n"
            "Update known_sentinels in this test to acknowledge them."
        )
    if removed_sentinels:
        pytest.fail(
            f"Skills no longer sentinel (now have real outputs): {sorted(removed_sentinels)}\n"
            "Their downstream consumers can now use --check-prereqs. Add Step 0 to them,\n"
            "then remove from known_sentinels in this test."
        )
