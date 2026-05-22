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

import json
from engine import SkillGraphEngine, CycleDependencyError, DriftViolationError, parse_simple_yaml, SemanticValidator, ValidationResult, ExecutionStack


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

    vision_dir = workspace_dir / "docs" / "specs"
    vision_dir.mkdir(parents=True, exist_ok=True)
    (vision_dir / "0001-vision.md").write_text("vision", encoding="utf-8")

    completed = engine.get_completed_nodes()
    assert "s2-capture-vision" in completed

    bypassed_info = engine.get_bypassed_dependencies()
    assert "s2-capture-vision" in bypassed_info

    all_bypassed = set()
    for missing in bypassed_info.values():
        all_bypassed.update(missing)

    assert "s1-define-rules" in all_bypassed
    assert "s1-config-context" in all_bypassed
    assert "s1-lock-tech-stack" in all_bypassed


# ---------------------------------------------------------------------------
# 5. SemanticValidator unit tests
# ---------------------------------------------------------------------------

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_semantic_validator_json_query_pass(tmp_path):
    (tmp_path / "test-results.json").write_text('{"summary": {"failed": 0}}', encoding="utf-8")
    v = [{"type": "json_query", "file": "test-results.json",
          "query": ".summary.failed == 0", "error_msg": "failed != 0"}]
    result = SemanticValidator(v, tmp_path).run()
    assert result.passed
    assert result.errors == []


def test_semantic_validator_json_query_fail(tmp_path):
    (tmp_path / "test-results.json").write_text('{"summary": {"failed": 1}}', encoding="utf-8")
    v = [{"type": "json_query", "file": "test-results.json",
          "query": ".summary.failed == 0", "error_msg": "測試必須全部通過"}]
    result = SemanticValidator(v, tmp_path).run()
    assert not result.passed
    assert "測試必須全部通過" in result.errors[0]


def test_semantic_validator_json_query_missing_file(tmp_path):
    v = [{"type": "json_query", "file": "missing.json", "query": ".x == 1", "error_msg": "e"}]
    result = SemanticValidator(v, tmp_path).run()
    assert not result.passed
    assert "file not found" in result.errors[0]


def test_semantic_validator_json_query_invalid_json(tmp_path):
    (tmp_path / "bad.json").write_text("not json", encoding="utf-8")
    v = [{"type": "json_query", "file": "bad.json", "query": ".x == 1", "error_msg": "e"}]
    result = SemanticValidator(v, tmp_path).run()
    assert not result.passed
    assert "cannot read" in result.errors[0]


def test_semantic_validator_regex_match_pass(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "test_foo.py").write_text("def test_foo():\n    pass\n", encoding="utf-8")
    v = [{"type": "regex_match", "file": "src/*.py", "pattern": "def test_",
          "min_matches": 1, "error_msg": "no tests found"}]
    result = SemanticValidator(v, tmp_path).run()
    assert result.passed


def test_semantic_validator_regex_match_fail(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "app.py").write_text("def main():\n    pass\n", encoding="utf-8")
    v = [{"type": "regex_match", "file": "src/*.py", "pattern": "def test_",
          "min_matches": 1, "error_msg": "必須存在至少一個 test_ 函式"}]
    result = SemanticValidator(v, tmp_path).run()
    assert not result.passed
    assert "test_ 函式" in result.errors[0]


def test_semantic_validator_regex_match_no_files(tmp_path):
    v = [{"type": "regex_match", "file": "src/*.py", "pattern": "def test_",
          "min_matches": 1, "error_msg": "no files"}]
    result = SemanticValidator(v, tmp_path).run()
    assert not result.passed


def test_file_hash_mtime_pass(tmp_path):
    """Artifact newer than sentinel → PASS."""
    sentinel = tmp_path / ".s4-tdd.done"
    sentinel.write_text("", encoding="utf-8")
    import time; time.sleep(0.02)
    artifact = tmp_path / "report.json"
    artifact.write_text('{"ok": true}', encoding="utf-8")
    v = [{"type": "file_hash", "file": "report.json",
          "not_older_than_sentinel": True, "error_msg": "stale"}]
    result = SemanticValidator(v, tmp_path, node_id="s4-tdd").run()
    assert result.passed


def test_file_hash_mtime_fail(tmp_path):
    """Artifact older than sentinel → FAIL."""
    artifact = tmp_path / "report.json"
    artifact.write_text('{"ok": true}', encoding="utf-8")
    import time; time.sleep(0.02)
    sentinel = tmp_path / ".s4-tdd.done"
    sentinel.write_text("", encoding="utf-8")
    v = [{"type": "file_hash", "file": "report.json",
          "not_older_than_sentinel": True, "error_msg": "stale report"}]
    result = SemanticValidator(v, tmp_path, node_id="s4-tdd").run()
    assert not result.passed
    assert "stale report" in result.errors[0]


def test_file_hash_sha256_pass(tmp_path):
    """Sentinel stores sha256 of artifact → matching hash → PASS."""
    import hashlib
    artifact = tmp_path / "report.json"
    artifact.write_text('{"summary": {"failed": 0}}', encoding="utf-8")
    stored = hashlib.sha256(artifact.read_bytes()).hexdigest()
    sentinel = tmp_path / ".s4-tdd.done"
    sentinel.write_text(f"sha256:{stored}", encoding="utf-8")
    v = [{"type": "file_hash", "file": "report.json",
          "not_older_than_sentinel": True, "error_msg": "tampered"}]
    result = SemanticValidator(v, tmp_path, node_id="s4-tdd").run()
    assert result.passed


def test_file_hash_sha256_fail(tmp_path):
    """Sentinel stores sha256 but artifact was swapped → FAIL."""
    import hashlib
    original = b'{"summary": {"failed": 0}}'
    stored = hashlib.sha256(original).hexdigest()
    sentinel = tmp_path / ".s4-tdd.done"
    sentinel.write_text(f"sha256:{stored}", encoding="utf-8")
    # Write DIFFERENT content to artifact
    artifact = tmp_path / "report.json"
    artifact.write_text('{"summary": {"failed": 1}}', encoding="utf-8")
    v = [{"type": "file_hash", "file": "report.json",
          "not_older_than_sentinel": True, "error_msg": "tampered"}]
    result = SemanticValidator(v, tmp_path, node_id="s4-tdd").run()
    assert not result.passed
    assert "tampered" in result.errors[0]


def test_file_hash_missing_sentinel(tmp_path):
    """No sentinel file → FAIL with sentinel-not-found message."""
    (tmp_path / "report.json").write_text("{}", encoding="utf-8")
    v = [{"type": "file_hash", "file": "report.json",
          "not_older_than_sentinel": True, "error_msg": "stale"}]
    result = SemanticValidator(v, tmp_path, node_id="s4-tdd").run()
    assert not result.passed
    assert "sentinel" in result.errors[0]


def test_file_hash_missing_artifact(tmp_path):
    """Artifact doesn't exist → FAIL with not-found message."""
    (tmp_path / ".s4-tdd.done").write_text("", encoding="utf-8")
    v = [{"type": "file_hash", "file": "missing.json",
          "not_older_than_sentinel": True, "error_msg": "stale"}]
    result = SemanticValidator(v, tmp_path, node_id="s4-tdd").run()
    assert not result.passed
    assert "not found" in result.errors[0]


def test_file_hash_no_node_id_skips(tmp_path):
    """Without node_id, file_hash is a no-op (no sentinel to compare against)."""
    v = [{"type": "file_hash", "file": "report.json",
          "not_older_than_sentinel": True, "error_msg": "stale"}]
    result = SemanticValidator(v, tmp_path).run()  # no node_id
    assert result.passed


def test_semantic_validator_invalid_type(tmp_path):
    v = [{"type": "unknown_type", "file": "x", "error_msg": "e"}]
    result = SemanticValidator(v, tmp_path).run()
    assert not result.passed
    assert "Unknown validator type" in result.errors[0]


# ---------------------------------------------------------------------------
# 6. Engine integration: validators in get_completed_nodes
# ---------------------------------------------------------------------------

@pytest.fixture
def validator_project(tmp_path):
    schema_file = FIXTURE_DIR / "schema_with_validators.yaml"
    return schema_file, tmp_path


def test_strict_mode_semantic_block(validator_project):
    """In strict mode, failing validator prevents node from being COMPLETED."""
    schema_file, workspace = validator_project
    # Create upstream dependency
    (workspace / "upstream.txt").write_text("ok", encoding="utf-8")
    # Create test-results.json with failures (semantic fail)
    (workspace / "test-results.json").write_text('{"summary": {"failed": 1}}', encoding="utf-8")
    # Create the regex source file so regex_match can at least find files
    src = workspace / "src"
    src.mkdir()
    (src / "test_foo.py").write_text("def test_foo(): pass", encoding="utf-8")

    engine = SkillGraphEngine(schema_file, workspace, mode="strict")
    completed = engine.get_completed_nodes()

    assert "s4-tdd" not in completed
    failures = engine.get_validation_failures()
    assert "s4-tdd" in failures
    assert "failed == 0" in failures["s4-tdd"] or "通過" in failures["s4-tdd"]


def test_strict_mode_semantic_pass(validator_project):
    """In strict mode, passing validator → node is COMPLETED."""
    schema_file, workspace = validator_project
    (workspace / "upstream.txt").write_text("ok", encoding="utf-8")
    (workspace / "test-results.json").write_text('{"summary": {"failed": 0}}', encoding="utf-8")
    src = workspace / "src"
    src.mkdir()
    (src / "test_foo.py").write_text("def test_foo(): pass", encoding="utf-8")

    engine = SkillGraphEngine(schema_file, workspace, mode="strict")
    completed = engine.get_completed_nodes()

    assert "s4-tdd" in completed
    assert engine.get_validation_failures() == {}


def test_fluid_mode_semantic_warn(validator_project):
    """In fluid mode, failing validator → node still COMPLETED but failure recorded."""
    schema_file, workspace = validator_project
    (workspace / "upstream.txt").write_text("ok", encoding="utf-8")
    (workspace / "test-results.json").write_text('{"summary": {"failed": 2}}', encoding="utf-8")
    src = workspace / "src"
    src.mkdir()
    (src / "test_foo.py").write_text("def test_foo(): pass", encoding="utf-8")

    engine = SkillGraphEngine(schema_file, workspace, mode="fluid")
    completed = engine.get_completed_nodes()

    assert "s4-tdd" in completed  # fluid: still completed
    failures = engine.get_validation_failures()
    assert "s4-tdd" in failures
    assert "SemanticValidationWarning" in failures["s4-tdd"]


def test_downstream_blocked_when_validator_fails_strict(validator_project):
    """In strict mode, semantic block on s4-tdd cascades to s5-sast-lint."""
    schema_file, workspace = validator_project
    (workspace / "upstream.txt").write_text("ok", encoding="utf-8")
    (workspace / "test-results.json").write_text('{"summary": {"failed": 1}}', encoding="utf-8")
    # s5-sast-lint output present on disk — but s4-tdd is semantically blocked
    (workspace / "sast-report.json").write_text('{}', encoding="utf-8")
    src = workspace / "src"
    src.mkdir()
    (src / "test_foo.py").write_text("def test_foo(): pass", encoding="utf-8")

    engine = SkillGraphEngine(schema_file, workspace, mode="strict")
    completed = engine.get_completed_nodes()
    blocked = engine.get_blocked_nodes()

    assert "s4-tdd" not in completed
    assert "s5-sast-lint" in blocked


def test_validate_schema_rejects_invalid_validator_type(tmp_path):
    schema_file = tmp_path / "bad_validator.yaml"
    schema_file.write_text("""
skills:
  s-node:
    stage: 1
    requires: []
    outputs:
      - out.txt
    validators:
      - type: bad_type
        file: out.txt
        error_msg: "x"
""", encoding="utf-8")
    with pytest.raises(ValueError) as exc_info:
        SkillGraphEngine(schema_file, tmp_path)
    assert "invalid type" in str(exc_info.value)
    assert "bad_type" in str(exc_info.value)


def test_validate_schema_accepts_new_valid_keys(tmp_path):
    schema_file = tmp_path / "schema_new_keys.yaml"
    schema_file.write_text("""
skills:
  s-node:
    stage: 1
    requires: []
    outputs:
      - out.txt
    reads:
      - some-context.md
    writes:
      - out.txt
    sentinels:
      - .s-node.done
""", encoding="utf-8")
    # Should not raise
    engine = SkillGraphEngine(schema_file, tmp_path)
    assert "s-node" in engine.skills


# ---------------------------------------------------------------------------
# 7. P2: Bidirectional Spec Sync (sync_docs / lint_drift)
# ---------------------------------------------------------------------------

SIMPLE_SCHEMA = """
skills:
  a-task:
    stage: 1
    requires: []
    outputs: []
  b-task:
    stage: 2
    requires:
      - a-task
    outputs: []
  c-task:
    stage: 2
    requires:
      - a-task
    outputs: []
"""


@pytest.fixture
def sync_project(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(SIMPLE_SCHEMA, encoding="utf-8")
    readme = tmp_path / "README.md"
    readme.write_text("# My Project\n\nSome intro text.\n\n## The 35 Skills\n\nSkills table here.\n", encoding="utf-8")
    engine = SkillGraphEngine(schema_file, tmp_path)
    return engine, readme


def test_sync_docs_inserts_block(sync_project):
    engine, readme = sync_project
    changed = engine.sync_docs(readme)
    assert changed == 1
    content = readme.read_text()
    assert "<!-- SKILL-GRAPH-START -->" in content
    assert "<!-- SKILL-GRAPH-END -->" in content
    assert "graph LR" in content
    assert "a-task --> b-task" in content
    assert "a-task --> c-task" in content


def test_sync_docs_idempotent(sync_project):
    engine, readme = sync_project
    engine.sync_docs(readme)
    changed = engine.sync_docs(readme)
    assert changed == 0


def test_sync_docs_updates_existing_block(sync_project):
    engine, readme = sync_project
    engine.sync_docs(readme)
    # Manually corrupt the block
    readme.write_text(
        readme.read_text().replace("a-task --> b-task", "fake --> fake"),
        encoding="utf-8",
    )
    changed = engine.sync_docs(readme)
    assert changed == 1
    assert "a-task --> b-task" in readme.read_text()
    assert "fake --> fake" not in readme.read_text()


def test_lint_drift_no_violations(sync_project):
    engine, readme = sync_project
    engine.sync_docs(readme)
    violations = engine.lint_drift(readme)
    assert violations == []


def test_lint_drift_missing_edge(sync_project):
    engine, readme = sync_project
    engine.sync_docs(readme)
    # Remove one edge from README
    readme.write_text(
        readme.read_text().replace("    a-task --> b-task\n", ""),
        encoding="utf-8",
    )
    violations = engine.lint_drift(readme)
    assert any("MISSING" in v and "a-task" in v and "b-task" in v for v in violations)


def test_lint_drift_extra_edge(sync_project):
    engine, readme = sync_project
    engine.sync_docs(readme)
    # Inject a spurious edge
    content = readme.read_text()
    content = content.replace("    a-task --> b-task", "    a-task --> b-task\n    fake --> b-task")
    readme.write_text(content, encoding="utf-8")
    violations = engine.lint_drift(readme)
    assert any("EXTRA" in v and "fake" in v for v in violations)


def test_lint_drift_strict_raises(sync_project):
    engine, readme = sync_project
    engine.sync_docs(readme)
    readme.write_text(
        readme.read_text().replace("    a-task --> b-task\n", ""),
        encoding="utf-8",
    )
    with pytest.raises(DriftViolationError):
        engine.lint_drift(readme, strict=True)


def test_lint_drift_no_markers_warns(sync_project):
    engine, readme = sync_project
    # README without markers
    violations = engine.lint_drift(readme)
    assert len(violations) == 1
    assert "WARNING" in violations[0]
    assert "sync-docs" in violations[0]


def test_generate_mermaid_contains_subgraphs(sync_project):
    engine, _ = sync_project
    mermaid = engine._generate_mermaid()
    assert 'subgraph stage1["Stage 1' in mermaid
    assert 'subgraph stage2["Stage 2' in mermaid
    assert "a-task --> b-task" in mermaid


# ---------------------------------------------------------------------------
# 8. ExecutionStack unit tests (P3)
# ---------------------------------------------------------------------------

def test_execution_stack_push_pop(tmp_path):
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    assert stack.is_empty()
    ok = stack.push("s4-tdd", "s4-impl-task", "failed=2")
    assert ok
    assert stack.depth() == 1
    assert stack.peek()["node_id"] == "s4-tdd"
    entry = stack.pop()
    assert entry["rollback_target"] == "s4-impl-task"
    assert stack.is_empty()


def test_execution_stack_max_depth(tmp_path):
    stack = ExecutionStack(tmp_path / ".engine_stack.json", max_depth=2)
    assert stack.push("n1", "n0", "r1")
    assert stack.push("n2", "n1", "r2")
    assert not stack.push("n3", "n2", "r3")  # exceeds max_depth
    assert stack.depth() == 2


def test_execution_stack_persistence(tmp_path):
    path = tmp_path / ".engine_stack.json"
    s1 = ExecutionStack(path)
    s1.push("s4-tdd", "s3-design-arch", "test failure")
    # New instance reads from disk
    s2 = ExecutionStack(path)
    assert s2.depth() == 1
    assert s2.peek()["node_id"] == "s4-tdd"


def test_execution_stack_display_empty(tmp_path):
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    disp = stack.display()
    assert "empty" in disp
    assert "depth: 0" in disp


def test_execution_stack_display_with_frames(tmp_path):
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    stack.push("s4-tdd", "s3-design-arch", "test failure")
    disp = stack.display()
    assert "s4-tdd" in disp
    assert "s3-design-arch" in disp
    assert "test failure" in disp


def test_execution_stack_pop_empty(tmp_path):
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    assert stack.pop() is None


# ---------------------------------------------------------------------------
# 9. Rollback Trace & Stack Pop integration tests (P3)
# ---------------------------------------------------------------------------

VALIDATOR_SCHEMA = """
skills:
  s0-upstream:
    stage: 0
    requires: []
    outputs:
      - upstream.txt

  s4-tdd:
    stage: 4
    requires:
      - s0-upstream
    outputs:
      - test-results.json
    validators:
      - type: json_query
        file: test-results.json
        query: ".summary.failed == 0"
        error_msg: "測試必須全部通過（failed == 0）"

  s5-sast-lint:
    stage: 5
    requires:
      - s4-tdd
    outputs:
      - sast-report.json
"""


@pytest.fixture
def rollback_project(tmp_path):
    """Project where s4-tdd fails its validator."""
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(VALIDATOR_SCHEMA, encoding="utf-8")

    # Mark s0-upstream as complete
    (tmp_path / "upstream.txt").write_text("done", encoding="utf-8")

    # s4-tdd output exists but validator will fail (failed=1)
    (tmp_path / "test-results.json").write_text(
        '{"summary": {"failed": 1}}', encoding="utf-8"
    )
    engine = SkillGraphEngine(schema_file, tmp_path, mode="strict")
    return engine, tmp_path


def test_rollback_trace_no_failures(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(VALIDATOR_SCHEMA, encoding="utf-8")
    (tmp_path / "upstream.txt").write_text("done", encoding="utf-8")
    # s4-tdd passes validator
    (tmp_path / "test-results.json").write_text(
        '{"summary": {"failed": 0}}', encoding="utf-8"
    )
    engine = SkillGraphEngine(schema_file, tmp_path, mode="strict")
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    msg = engine.rollback_trace(stack)
    assert "not needed" in msg
    assert stack.is_empty()


def test_rollback_trace_pushes_frame(rollback_project):
    engine, tmp_path = rollback_project
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    msg = engine.rollback_trace(stack)
    assert stack.depth() == 1
    frame = stack.peek()
    assert frame["node_id"] == "s4-tdd"
    assert frame["rollback_target"] == "s0-upstream"
    assert "Pushed 1" in msg


def test_rollback_trace_creates_sentinel(rollback_project):
    engine, tmp_path = rollback_project
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    engine.rollback_trace(stack)
    sentinel = tmp_path / ".s0-upstream.rollback"
    assert sentinel.exists()
    assert "s4-tdd" in sentinel.read_text()


def test_rollback_trace_limit_exceeded(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(VALIDATOR_SCHEMA, encoding="utf-8")
    (tmp_path / "upstream.txt").write_text("done", encoding="utf-8")
    (tmp_path / "test-results.json").write_text(
        '{"summary": {"failed": 1}}', encoding="utf-8"
    )
    engine = SkillGraphEngine(schema_file, tmp_path, mode="strict")
    # Pre-fill stack to max_depth=1
    stack = ExecutionStack(tmp_path / ".engine_stack.json", max_depth=1)
    stack.push("existing-fail", "existing-target", "prior failure")
    msg = engine.rollback_trace(stack)
    assert "ROLLBACK_LIMIT_EXCEEDED" in msg
    assert stack.depth() == 1  # did not grow past max


def test_stack_pop_still_failing(rollback_project):
    engine, tmp_path = rollback_project
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    engine.rollback_trace(stack)
    # validator still fails (test-results.json not fixed)
    msg = engine.stack_pop(stack)
    assert "Cannot pop" in msg
    assert stack.depth() == 1  # not popped


def test_stack_pop_after_fix(rollback_project):
    engine, tmp_path = rollback_project
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    engine.rollback_trace(stack)
    # Fix the artifact
    (tmp_path / "test-results.json").write_text(
        '{"summary": {"failed": 0}}', encoding="utf-8"
    )
    msg = engine.stack_pop(stack)
    assert "Popped" in msg
    assert stack.is_empty()
    assert not (tmp_path / ".s0-upstream.rollback").exists()


def test_stack_pop_empty_stack(rollback_project):
    engine, tmp_path = rollback_project
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    msg = engine.stack_pop(stack)
    assert "empty" in msg.lower()


def test_rollback_trace_mtime_heuristic(tmp_path):
    """Primary mtime path: upstream output newer than failed artifact → chosen as target."""
    import time

    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(VALIDATOR_SCHEMA, encoding="utf-8")

    # Write upstream output first (older)
    upstream = tmp_path / "upstream.txt"
    upstream.write_text("done", encoding="utf-8")

    # Briefly pause so mtime differs, then write failed artifact
    time.sleep(0.05)
    artifact = tmp_path / "test-results.json"
    artifact.write_text('{"summary": {"failed": 1}}', encoding="utf-8")

    # Now set upstream to a newer mtime than the artifact (simulates upstream re-ran after artifact)
    import os
    new_mtime = artifact.stat().st_mtime + 10
    os.utime(upstream, (new_mtime, new_mtime))

    engine = SkillGraphEngine(schema_file, tmp_path, mode="strict")
    stack = ExecutionStack(tmp_path / ".engine_stack.json")
    engine.rollback_trace(stack)
    frame = stack.peek()
    assert frame["rollback_target"] == "s0-upstream"


# ---------------------------------------------------------------------------
# 10. JIT Context Injection (P4)
# ---------------------------------------------------------------------------

JIT_SCHEMA = """
skills:
  s0-root:
    stage: 0
    requires: []
    outputs:
      - root.txt

  s0-upstream:
    stage: 0
    requires:
      - s0-root
    outputs:
      - upstream.txt
    writes:
      - upstream.txt

  s4-impl:
    stage: 4
    requires:
      - s0-upstream
    outputs:
      - impl.py
    reads:
      - spec.md
    writes:
      - impl.py
    validators:
      - type: json_query
        file: impl.py
        query: ".status == 'done'"
        error_msg: "impl must be done"

  s5-quality:
    stage: 5
    requires:
      - s4-impl
    outputs:
      - report.json
"""


@pytest.fixture
def jit_project(tmp_path):
    schema_file = tmp_path / "schema.yaml"
    schema_file.write_text(JIT_SCHEMA, encoding="utf-8")
    engine = SkillGraphEngine(schema_file, tmp_path, mode="fluid")
    return engine, tmp_path


def test_detect_active_node_explicit_hint(jit_project):
    engine, tmp_path = jit_project
    state = tmp_path / "mock_ide.json"
    state.write_text(json.dumps({"active_node_hint": "s4-impl"}), encoding="utf-8")
    assert engine._detect_active_node(state) == "s4-impl"


def test_detect_active_node_invalid_hint_falls_through(jit_project):
    engine, tmp_path = jit_project
    state = tmp_path / "mock_ide.json"
    state.write_text(json.dumps({"active_node_hint": "nonexistent"}), encoding="utf-8")
    # No other signals → None
    assert engine._detect_active_node(state) is None


def test_detect_active_node_rollback_sentinel(jit_project):
    engine, tmp_path = jit_project
    (tmp_path / ".s4-impl.rollback").write_text("rollback: fixing s5-quality\n", encoding="utf-8")
    assert engine._detect_active_node(None) == "s4-impl"


def test_detect_active_node_done_sentinel(jit_project):
    engine, tmp_path = jit_project
    (tmp_path / ".s4-impl.done").write_text("", encoding="utf-8")
    assert engine._detect_active_node(None) == "s4-impl"


def test_detect_active_node_no_signal(jit_project):
    engine, tmp_path = jit_project
    assert engine._detect_active_node(None) is None


def test_detect_active_node_file_match(jit_project):
    engine, tmp_path = jit_project
    state = tmp_path / "mock_ide.json"
    # active_file matches s4-impl's writes field
    state.write_text(json.dumps({"active_file": "impl.py"}), encoding="utf-8")
    assert engine._detect_active_node(state) == "s4-impl"


def test_generate_jit_includes_current_and_upstream(jit_project):
    engine, tmp_path = jit_project
    state = tmp_path / "mock_ide.json"
    state.write_text(json.dumps({"active_node_hint": "s4-impl"}), encoding="utf-8")
    prompt = engine.generate_jit_prompt(state_path=state, depth=1)
    assert "s4-impl" in prompt
    assert "s0-upstream" in prompt  # direct upstream included


def test_generate_jit_excludes_downstream(jit_project):
    engine, tmp_path = jit_project
    state = tmp_path / "mock_ide.json"
    state.write_text(json.dumps({"active_node_hint": "s4-impl"}), encoding="utf-8")
    prompt = engine.generate_jit_prompt(state_path=state, depth=1)
    assert "s5-quality" not in prompt


def test_generate_jit_depth2_reaches_grandparent(jit_project):
    engine, tmp_path = jit_project
    state = tmp_path / "mock_ide.json"
    state.write_text(json.dumps({"active_node_hint": "s4-impl"}), encoding="utf-8")
    prompt = engine.generate_jit_prompt(state_path=state, depth=2)
    assert "s0-root" in prompt  # grandparent reached at depth=2


def test_generate_jit_depth1_excludes_grandparent(jit_project):
    engine, tmp_path = jit_project
    state = tmp_path / "mock_ide.json"
    state.write_text(json.dumps({"active_node_hint": "s4-impl"}), encoding="utf-8")
    prompt = engine.generate_jit_prompt(state_path=state, depth=1)
    assert "s0-root" not in prompt  # grandparent not in depth=1


def test_generate_jit_no_active_node(jit_project):
    engine, tmp_path = jit_project
    prompt = engine.generate_jit_prompt(state_path=None)
    assert "No active node" in prompt


def test_generate_jit_includes_hard_gate(jit_project):
    engine, tmp_path = jit_project
    # Create a mock SKILL.md with HARD-GATE block
    skill_dir = tmp_path / "skills" / "s4-impl"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: s4-impl\n---\n<HARD-GATE>\nDo NOT skip tests.\n</HARD-GATE>\n",
        encoding="utf-8",
    )
    state = tmp_path / "mock_ide.json"
    state.write_text(json.dumps({"active_node_hint": "s4-impl"}), encoding="utf-8")
    prompt = engine.generate_jit_prompt(
        state_path=state, skills_dir=tmp_path / "skills"
    )
    assert "HARD-GATE" in prompt
    assert "Do NOT skip tests" in prompt


def test_jit_token_check_passes_small_prompt(jit_project, tmp_path):
    engine, _ = jit_project
    skills_dir = tmp_path / "jit_skills"
    for i in range(5):
        d = skills_dir / f"s{i}-skill"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("word " * 300, encoding="utf-8")
    result = engine.jit_token_check("hello world tiny prompt", skills_dir)
    assert result["passed"]
    assert result["total_tokens"] > result["jit_tokens"]


def test_jit_token_check_fails_large_prompt(jit_project, tmp_path):
    engine, _ = jit_project
    skills_dir = tmp_path / "jit_skills"
    (skills_dir / "s0-skill").mkdir(parents=True)
    (skills_dir / "s0-skill" / "SKILL.md").write_text("word " * 10, encoding="utf-8")
    huge_prompt = "word " * 1000
    result = engine.jit_token_check(huge_prompt, skills_dir)
    assert not result["passed"]

