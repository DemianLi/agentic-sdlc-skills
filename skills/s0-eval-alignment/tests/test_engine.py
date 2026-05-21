"""
Unit tests for SkillGraphEngine.

Verify parsing, topological sorting, cycle detection, completed/next/blocked states under
various filesystem configurations.
"""

import sys
from pathlib import Path
import pytest

# Inject script directory to import engine
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from engine import SkillGraphEngine, CycleDependencyError, parse_simple_yaml


# ---------------------------------------------------------------------------
# 1. Parsing and helper unit tests
# ---------------------------------------------------------------------------

def test_parse_simple_yaml():
    yaml_content = """
skills:
  s1-define-rules:
    stage: 1
    requires: []
    outputs:
      - RULES.md

  s1-lock-tech-stack:
    stage: 1
    requires:
      - s1-define-rules
    outputs:
      - docs/adr/*-tech-stack.md
      - package.json
"""
    parsed = parse_simple_yaml(yaml_content)
    assert "skills" in parsed
    skills = parsed["skills"]
    assert "s1-define-rules" in skills
    assert skills["s1-define-rules"]["stage"] == 1
    assert skills["s1-define-rules"]["requires"] == []
    assert skills["s1-define-rules"]["outputs"] == ["RULES.md"]

    assert "s1-lock-tech-stack" in skills
    assert skills["s1-lock-tech-stack"]["requires"] == ["s1-define-rules"]
    assert skills["s1-lock-tech-stack"]["outputs"] == ["docs/adr/*-tech-stack.md", "package.json"]


# ---------------------------------------------------------------------------
# 2. Topological sort and Cycle detection tests
# ---------------------------------------------------------------------------

def test_topological_sort_order(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text("""
skills:
  c-task:
    stage: 3
    requires:
      - b-task
    outputs: []
  a-task:
    stage: 1
    requires: []
    outputs: []
  b-task:
    stage: 2
    requires:
      - a-task
    outputs: []
""", encoding="utf-8")
    
    engine = SkillGraphEngine(schema_file, tmp_path)
    order = engine.topological_sort()
    # Post-order traversal reversed / dependency order:
    # a-task must come before b-task, and b-task must come before c-task
    assert order.index("a-task") < order.index("b-task")
    assert order.index("b-task") < order.index("c-task")


def test_cycle_detection_direct(tmp_path):
    schema_file = tmp_path / "schema_cycle.yaml"
    schema_file.write_text("""
skills:
  a-task:
    stage: 1
    requires:
      - b-task
    outputs: []
  b-task:
    stage: 2
    requires:
      - a-task
    outputs: []
""", encoding="utf-8")
    
    with pytest.raises(CycleDependencyError) as exc_info:
        SkillGraphEngine(schema_file, tmp_path)
    assert "Cycle detected" in str(exc_info.value)
    assert "a-task" in str(exc_info.value)
    assert "b-task" in str(exc_info.value)


def test_cycle_detection_indirect(tmp_path):
    schema_file = tmp_path / "schema_cycle_ind.yaml"
    schema_file.write_text("""
skills:
  a-task:
    stage: 1
    requires:
      - c-task
    outputs: []
  b-task:
    stage: 2
    requires:
      - a-task
    outputs: []
  c-task:
    stage: 3
    requires:
      - b-task
    outputs: []
""", encoding="utf-8")
    
    with pytest.raises(CycleDependencyError) as exc_info:
        SkillGraphEngine(schema_file, tmp_path)
    assert "Cycle detected" in str(exc_info.value)


def test_undefined_dependency(tmp_path):
    schema_file = tmp_path / "schema_undef.yaml"
    schema_file.write_text("""
skills:
  a-task:
    stage: 1
    requires:
      - missing-task
    outputs: []
""", encoding="utf-8")
    
    with pytest.raises(ValueError) as exc_info:
        SkillGraphEngine(schema_file, tmp_path)
    assert "requires undefined skill" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 3. Dynamic filesystem resolution tests (completed, next, blocked)
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_project(tmp_path):
    """Sets up a complete 3-stage mock project with schema and workspace directory."""
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text("""
skills:
  s1-define-rules:
    stage: 1
    requires: []
    outputs:
      - RULES.md

  s1-config-context:
    stage: 1
    requires: []
    outputs:
      - CONTEXT.md

  s1-lock-tech-stack:
    stage: 1
    requires:
      - s1-define-rules
      - s1-config-context
    outputs:
      - docs/adr/*-tech-stack.md

  s2-capture-vision:
    stage: 2
    requires:
      - s1-lock-tech-stack
    outputs:
      - docs/specs/*-vision.md

  s4-impl-task:
    stage: 4
    requires:
      - s2-capture-vision
    outputs: []
""", encoding="utf-8")
    return schema_file, tmp_path


def test_empty_workspace_status(mock_project):
    schema_file, workspace_dir = mock_project
    engine = SkillGraphEngine(schema_file, workspace_dir)

    completed = engine.get_completed_nodes()
    next_nodes = engine.get_next_nodes()
    blocked = engine.get_blocked_nodes()

    # Nothing should be completed
    assert completed == set()
    # Only s1-define-rules and s1-config-context are topologically ready (they have no requirements)
    assert set(next_nodes) == {"s1-define-rules", "s1-config-context"}
    # Blocked nodes list missing dependencies
    assert "s1-lock-tech-stack" in blocked
    assert set(blocked["s1-lock-tech-stack"]) == {"s1-define-rules", "s1-config-context"}
    assert "s2-capture-vision" in blocked
    assert blocked["s2-capture-vision"] == ["s1-lock-tech-stack"]


def test_partial_completion_with_files(mock_project):
    schema_file, workspace_dir = mock_project
    engine = SkillGraphEngine(schema_file, workspace_dir)

    # Create RULES.md (completes s1-define-rules)
    (workspace_dir / "RULES.md").write_text("rules content", encoding="utf-8")

    completed = engine.get_completed_nodes()
    next_nodes = engine.get_next_nodes()
    blocked = engine.get_blocked_nodes()

    assert completed == {"s1-define-rules"}
    # s1-config-context is still the only next node ready to run (s1-lock-tech-stack is blocked by s1-config-context)
    assert next_nodes == ["s1-config-context"]
    assert "s1-lock-tech-stack" in blocked
    assert blocked["s1-lock-tech-stack"] == ["s1-config-context"]


def test_completed_overrides(mock_project):
    schema_file, workspace_dir = mock_project
    engine = SkillGraphEngine(schema_file, workspace_dir)

    # Force complete s1-define-rules and s1-config-context via overrides
    overrides = {"s1-define-rules", "s1-config-context"}
    completed = engine.get_completed_nodes(overrides)
    next_nodes = engine.get_next_nodes(overrides)

    assert completed == overrides
    # Now s1-lock-tech-stack is topologically ready!
    assert next_nodes == ["s1-lock-tech-stack"]


def test_glob_outputs_completion(mock_project):
    schema_file, workspace_dir = mock_project
    engine = SkillGraphEngine(schema_file, workspace_dir)

    # Write concrete outputs for s1 tasks
    (workspace_dir / "RULES.md").write_text("rules", encoding="utf-8")
    (workspace_dir / "CONTEXT.md").write_text("glossary", encoding="utf-8")
    
    # Create the adr folder and write an ADR (satisfies docs/adr/*-tech-stack.md glob)
    adr_dir = workspace_dir / "docs" / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)
    (adr_dir / "0001-tech-stack.md").write_text("adr stack lock", encoding="utf-8")

    completed = engine.get_completed_nodes()
    next_nodes = engine.get_next_nodes()

    # s1-define-rules, s1-config-context, and s1-lock-tech-stack should be completed
    assert "s1-define-rules" in completed
    assert "s1-config-context" in completed
    assert "s1-lock-tech-stack" in completed
    
    # s2-capture-vision is now ready!
    assert next_nodes == ["s2-capture-vision"]


def test_stage_4_sentinel_handling(mock_project):
    schema_file, workspace_dir = mock_project
    engine = SkillGraphEngine(schema_file, workspace_dir)

    # Force upstream completed
    overrides = {"s1-define-rules", "s1-config-context", "s1-lock-tech-stack", "s2-capture-vision"}

    # CASE 1: No sentinel file → s4-impl-task not completed
    assert "s4-impl-task" not in engine.get_completed_nodes(overrides)

    # CASE 2: Sentinel file exists → s4-impl-task completed
    sentinel = workspace_dir / ".s4-impl-task.done"
    sentinel.touch()
    completed = engine.get_completed_nodes(overrides)
    assert "s4-impl-task" in completed

    sentinel.unlink()
    assert "s4-impl-task" not in engine.get_completed_nodes(overrides)


def test_fluid_vs_strict_modes(mock_project):
    schema_file, workspace_dir = mock_project
    
    # Write a completed file for s1-lock-tech-stack (downstream)
    # docs/adr/*-tech-stack.md
    adr_dir = workspace_dir / "docs" / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)
    (adr_dir / "0001-tech-stack.md").write_text("tech stack details", encoding="utf-8")

    # Case 1: STRICT mode
    engine_strict = SkillGraphEngine(schema_file, workspace_dir, mode="strict")
    completed_strict = engine_strict.get_completed_nodes()
    # s1-lock-tech-stack has outputs, but its dependencies are missing.
    # In strict mode, s1-lock-tech-stack should NOT be completed!
    assert "s1-lock-tech-stack" not in completed_strict
    
    # Case 2: FLUID mode
    engine_fluid = SkillGraphEngine(schema_file, workspace_dir, mode="fluid")
    completed_fluid = engine_fluid.get_completed_nodes()
    # In fluid mode, s1-lock-tech-stack is completed because its files are on disk!
    assert "s1-lock-tech-stack" in completed_fluid

    # Verify catch-up suggestions (bypassed dependencies)
    bypassed = engine_fluid.get_bypassed_dependencies()
    assert "s1-lock-tech-stack" in bypassed
    # The bypassed dependencies should be s1-define-rules and s1-config-context
    assert set(bypassed["s1-lock-tech-stack"]) == {"s1-define-rules", "s1-config-context"}


# ---------------------------------------------------------------------------
# 4. V2.1 Refactoring & Enhancement Tests
# ---------------------------------------------------------------------------

def test_schema_typo_validation(tmp_path):
    schema_file = tmp_path / "schema_typo.yaml"
    # Contains typo "requiers" instead of "requires"
    schema_file.write_text("""
skills:
  a-task:
    stage: 1
    requiers: []
    outputs: []
""", encoding="utf-8")
    
    with pytest.raises(ValueError) as exc_info:
        SkillGraphEngine(schema_file, tmp_path)
    assert "Invalid configuration keys found in skill 'a-task'" in str(exc_info.value)
    assert "requiers" in str(exc_info.value)


def test_sentinel_file_completion(tmp_path):
    schema_file = tmp_path / "schema_sentinel.yaml"
    schema_file.write_text("""
skills:
  s1-define-rules:
    stage: 1
    requires: []
    outputs:
      - RULES.md
  s1-git-guardrails:
    stage: 1
    requires:
      - s1-define-rules
    outputs: []
""", encoding="utf-8")

    engine = SkillGraphEngine(schema_file, tmp_path)
    
    # 1. Initially, nothing is complete
    assert engine.get_completed_nodes() == set()
    
    # 2. Complete the upstream rules file
    (tmp_path / "RULES.md").write_text("rules", encoding="utf-8")
    assert engine.get_completed_nodes() == {"s1-define-rules"}
    
    # 3. Create sentinel file for git-guardrails (empty outputs skill)
    sentinel = tmp_path / ".s1-git-guardrails.done"
    sentinel.touch()
    
    # 4. Now both should be completed
    assert engine.get_completed_nodes() == {"s1-define-rules", "s1-git-guardrails"}


def test_iterative_dfs_sorting_and_cycle(tmp_path):
    schema_file = tmp_path / "schema_complex.yaml"
    schema_file.write_text("""
skills:
  d-task:
    stage: 4
    requires: [c-task]
    outputs: []
  c-task:
    stage: 3
    requires: [b-task]
    outputs: []
  b-task:
    stage: 2
    requires: [a-task]
    outputs: []
  a-task:
    stage: 1
    requires: []
    outputs: []
""", encoding="utf-8")

    engine = SkillGraphEngine(schema_file, tmp_path)
    order = engine.topological_sort()
    assert order == ["a-task", "b-task", "c-task", "d-task"]


def test_fluid_grouped_suggestions_logic(mock_project):
    schema_file, workspace_dir = mock_project
    engine = SkillGraphEngine(schema_file, workspace_dir, mode="fluid")

    # Complete the s2-capture-vision file, bypassing stage 1 upstream files
    vision_dir = workspace_dir / "docs" / "specs"
    vision_dir.mkdir(parents=True, exist_ok=True)
    (vision_dir / "0001-vision.md").write_text("vision", encoding="utf-8")

    completed = engine.get_completed_nodes()
    assert "s2-capture-vision" in completed

    # Verify that bypassed dependencies are correctly calculated
    bypassed_info = engine.get_bypassed_dependencies()
    assert "s2-capture-vision" in bypassed_info
    
    # Group unique bypassed skills to verify grouping logic correctness
    all_bypassed = set()
    for missing in bypassed_info.values():
        all_bypassed.update(missing)
        
    assert "s1-define-rules" in all_bypassed
    assert "s1-config-context" in all_bypassed
    assert "s1-lock-tech-stack" in all_bypassed

