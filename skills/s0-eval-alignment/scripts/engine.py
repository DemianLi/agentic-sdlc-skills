"""
SkillGraphEngine — Declarative YAML Schema + Runtime Topology Engine for Skill Graphs v2.2.

Tracks SDLC skill execution state, validates dependencies, computes completed/next/blocked
nodes, and performs topological sorting and cycle detection.
"""

import glob
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Union, Optional


class CycleDependencyError(ValueError):
    """Raised when a cycle is detected in the dependency graph."""
    pass


class DriftViolationError(ValueError):
    """Raised when YAML schema and README Mermaid DAG are out of sync."""
    pass


class ValidationResult:
    """Holds results from a SemanticValidator run."""

    def __init__(self, errors: List[str], warnings: List[str]):
        self.errors = errors
        self.warnings = warnings
        self.passed = len(errors) == 0


class SemanticValidator:
    """
    Runs validator DSL checks (json_query / regex_match / file_hash) defined in skill schema nodes.
    file_hash uses SHA256-in-sentinel when available, falls back to mtime comparison.
    """

    VALID_TYPES = {"json_query", "regex_match", "file_hash"}

    def __init__(self, validators: list, workspace: Path, node_id: str = ""):
        self.validators = validators
        self.workspace = workspace
        self.node_id = node_id  # needed for file_hash sentinel lookup

    def run(self) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []
        for v in self.validators:
            vtype = v.get("type")
            if vtype == "json_query":
                err = self._check_json_query(v)
                if err:
                    errors.append(err)
            elif vtype == "regex_match":
                err = self._check_regex_match(v)
                if err:
                    errors.append(err)
            elif vtype == "file_hash":
                err = self._check_file_hash(v)
                if err:
                    errors.append(err)
            else:
                errors.append(f"Unknown validator type: {vtype!r}")
        return ValidationResult(errors=errors, warnings=warnings)

    def _check_json_query(self, v: dict) -> Optional[str]:
        """Returns error_msg if check fails, None if passes."""
        import json
        import re as _re

        file_path = self.workspace / v["file"]
        if not file_path.exists():
            return f"json_query: file not found: {v['file']}"
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            return f"json_query: cannot read {v['file']}: {exc}"

        query = v.get("query", "")
        error_msg = v.get("error_msg", f"json_query failed: {query}")

        # Minimal jq subset: <dotpath> <op> <literal>
        m = _re.match(r'^([\w.]+)\s*(==|!=|>=|<=|>|<)\s*(.+)$', query.strip())
        if not m:
            return f"json_query: unsupported query syntax: {query!r}"
        path_str, op, literal_str = m.group(1), m.group(2), m.group(3).strip()

        value = data
        for part in [p for p in path_str.lstrip(".").split(".") if p]:
            if not isinstance(value, dict) or part not in value:
                return f"json_query: path {path_str!r} not found in {v['file']}"
            value = value[part]

        # Parse literal value
        ls = literal_str
        if ls.lower() == "true":
            literal: object = True
        elif ls.lower() == "false":
            literal = False
        elif (ls.startswith('"') and ls.endswith('"')) or (ls.startswith("'") and ls.endswith("'")):
            literal = ls[1:-1]
        else:
            try:
                literal = float(ls) if "." in ls else int(ls)
            except ValueError:
                literal = ls

        ops = {
            "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,  "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b,
        }
        try:
            passed = ops[op](value, literal)
        except TypeError:
            return f"json_query: cannot compare {type(value).__name__} {op} {type(literal).__name__}"
        return None if passed else error_msg

    def _check_regex_match(self, v: dict) -> Optional[str]:
        """Returns error_msg if check fails, None if passes."""
        import re as _re

        file_pattern = v.get("file", "")
        regex = v.get("pattern", "")
        min_matches = v.get("min_matches", 1)
        error_msg = v.get("error_msg", f"regex_match failed: {regex!r}")

        matched_files = glob.glob(str(self.workspace / file_pattern), recursive=True)
        if not matched_files:
            return error_msg

        compiled = _re.compile(regex)
        count = 0
        for fpath in matched_files:
            try:
                count += len(compiled.findall(Path(fpath).read_text(encoding="utf-8", errors="replace")))
            except OSError:
                pass
        return None if count >= min_matches else error_msg

    def _check_file_hash(self, v: dict) -> Optional[str]:
        """
        Returns error_msg if artifact is stale, None if fresh.

        Strategy (in priority order):
          1. If sentinel contains "sha256:<hex>" → compare artifact SHA256 against stored hash.
             Equality means artifact matches what was recorded at completion time (fresh).
             Mismatch means artifact was swapped after sentinel was written (tampered).
          2. Otherwise → compare artifact mtime > sentinel mtime (fresh if newer).

        SHA256 mode is preferred because git-clone resets mtime to current time,
        making mtime comparison unreliable in CI environments.
        """
        import hashlib

        if not v.get("not_older_than_sentinel") or not self.node_id:
            return None

        file_path = self.workspace / v["file"]
        error_msg = v.get("error_msg", "file_hash: artifact may be stale or copied")

        if not file_path.exists():
            return f"file_hash: artifact not found: {v['file']}"

        sentinel = self.workspace / f".{self.node_id}.done"
        if not sentinel.exists():
            return f"file_hash: sentinel .{self.node_id}.done not found — run the skill first"

        sentinel_content = sentinel.read_text(encoding="utf-8", errors="replace").strip()
        if sentinel_content.startswith("sha256:"):
            stored_hash = sentinel_content[7:].strip()
            artifact_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
            return None if artifact_hash == stored_hash else error_msg

        # mtime fallback: artifact must be strictly newer than sentinel
        if file_path.stat().st_mtime <= sentinel.stat().st_mtime:
            return error_msg
        return None


def parse_simple_yaml(content: str) -> dict:
    """
    Extremely robust regex/line-based YAML parser for our specific skill schema.
    Used as a fallback if the PyYAML 'yaml' module is not installed.
    """
    data = {"skills": {}}
    current_skill = None
    current_key = None
    
    for line in content.splitlines():
        # Strip comments and whitespace
        line = line.split("#")[0].strip()
        if not line:
            continue
        
        # Check for top-level keys like "skills:"
        if line == "skills:":
            continue
            
        # Match a skill name block, e.g. "s1-define-rules:"
        if line.endswith(":") and not line.startswith("-") and line[:-1].strip() not in ("requires", "outputs", "skills", "stage"):
            key = line[:-1].strip()
            # Since skills block is indented, we detect top-level skill keys
            current_skill = key
            data["skills"][current_skill] = {
                "stage": 1,
                "requires": [],
                "outputs": []
            }
            current_key = None
        elif ":" in line and not line.startswith("-"):
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if current_skill:
                if k == "stage":
                    try:
                        data["skills"][current_skill]["stage"] = int(v)
                    except ValueError:
                        pass
                elif k in ("requires", "outputs"):
                    current_key = k
        elif line.startswith("- ") and current_skill and current_key:
            val = line[2:].strip().strip('"').strip("'")
            data["skills"][current_skill][current_key].append(val)
            
    return data


class ExecutionStack:
    """
    Persistent execution stack for rollback trace. Stored in .engine_stack.json.
    Tracks FAILED nodes and their designated rollback targets across Agent restarts.
    """

    DEFAULT_MAX_DEPTH = 3

    def __init__(self, stack_path: Path, max_depth: int = DEFAULT_MAX_DEPTH):
        self.stack_path = Path(stack_path)
        self.max_depth = max_depth
        self._data = self._load()

    def _load(self) -> dict:
        if self.stack_path.exists():
            try:
                return json.loads(self.stack_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"active_stack": [], "stack_depth": 0, "max_depth": self.max_depth, "last_updated": ""}

    def _save(self) -> None:
        self._data["stack_depth"] = len(self._data["active_stack"])
        self._data["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.stack_path.write_text(json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8")

    def push(self, node_id: str, rollback_target: str, failure_reason: str) -> bool:
        """Push a rollback frame. Returns False (without saving) if max_depth exceeded."""
        if self.depth() >= self._data["max_depth"]:
            return False
        self._data["active_stack"].append({
            "node_id": node_id,
            "status": "FAILED",
            "failed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "failure_reason": failure_reason,
            "rollback_target": rollback_target,
        })
        self._save()
        return True

    def pop(self) -> Optional[dict]:
        """Remove and return the top frame. Returns None if empty."""
        if not self._data["active_stack"]:
            return None
        entry = self._data["active_stack"].pop()
        self._save()
        return entry

    def peek(self) -> Optional[dict]:
        """Return top frame without removing it."""
        if not self._data["active_stack"]:
            return None
        return self._data["active_stack"][-1]

    def depth(self) -> int:
        return len(self._data["active_stack"])

    def is_empty(self) -> bool:
        return len(self._data["active_stack"]) == 0

    def display(self) -> str:
        lines = [
            f"Execution Stack ({self.stack_path}):",
            f"  depth: {self.depth()}/{self._data['max_depth']}",
        ]
        if self.is_empty():
            lines.append("  (empty)")
        else:
            for i, frame in enumerate(reversed(self._data["active_stack"])):
                lines.append(f"  [{i}] {frame['node_id']} → rollback: {frame['rollback_target']}")
                lines.append(f"       reason: {frame['failure_reason']}")
        return "\n".join(lines)


class SkillGraphEngine:
    """
    The runtime topology engine for the Skill Graph concept.
    """

    def __init__(self, schema_path: Union[str, Path], workspace_dir: Union[str, Path], mode: str = "fluid"):
        self.schema_path = Path(schema_path)
        self.workspace_dir = Path(workspace_dir)
        self.mode = mode  # "fluid" or "strict"
        self._last_validation_failures: Dict[str, str] = {}
        self.skills = self._load_schema()
        self._validate_schema()

    def _load_schema(self) -> dict:
        """
        Parses the YAML schema from file. Uses PyYAML if available, or falls back
        to a highly robust custom regex line parser.
        """
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema file not found at: {self.schema_path}")

        content = self.schema_path.read_text(encoding="utf-8")
        try:
            import yaml
            data = yaml.safe_load(content)
            if not isinstance(data, dict) or "skills" not in data:
                raise ValueError("Invalid schema file format.")
            return data["skills"]
        except ImportError:
            if "validators:" in content:
                print("[WARNING] validators detected but PyYAML missing — skipped", file=sys.stderr)
            data = parse_simple_yaml(content)
            if "skills" not in data or not data["skills"]:
                raise ValueError("Failed to parse schema with fallback parser.")
            return data["skills"]
        except Exception:
            data = parse_simple_yaml(content)
            if "skills" not in data or not data["skills"]:
                raise ValueError("Failed to parse schema with fallback parser.")
            return data["skills"]

    def _validate_schema(self) -> None:
        """
        Ensures all requires are defined skills in the graph, detects cycles early,
        and validates that each skill contains only valid fields to prevent typos.
        """
        valid_keys = {"stage", "requires", "outputs", "reads", "writes", "sentinels", "validators"}
        valid_validator_types = {"json_query", "regex_match", "file_hash"}

        for skill_name, skill_info in self.skills.items():
            if not isinstance(skill_info, dict):
                raise ValueError(f"Skill '{skill_name}' configuration must be a dictionary.")

            invalid_keys = set(skill_info.keys()) - valid_keys
            if invalid_keys:
                raise ValueError(
                    f"Invalid configuration keys found in skill '{skill_name}': {', '.join(sorted(invalid_keys))}. "
                    f"Supported keys are: {', '.join(sorted(valid_keys))} (check for typos like 'requiers' or 'outpus')"
                )

            if not isinstance(skill_info.get("stage", 1), int):
                raise ValueError(f"Skill '{skill_name}': 'stage' must be an integer")
            for key in ("requires", "outputs"):
                val = skill_info.get(key, [])
                if not isinstance(val, list):
                    raise ValueError(f"Skill '{skill_name}': '{key}' must be a list, got {type(val).__name__}")

            for req in skill_info.get("requires", []):
                if req not in self.skills:
                    raise ValueError(f"Skill '{skill_name}' requires undefined skill '{req}'")

            if "validators" in skill_info:
                validators = skill_info["validators"]
                if not isinstance(validators, list):
                    raise ValueError(f"Skill '{skill_name}': 'validators' must be a list")
                for i, v in enumerate(validators):
                    if not isinstance(v, dict):
                        raise ValueError(f"Skill '{skill_name}': validators[{i}] must be a dict")
                    vtype = v.get("type")
                    if vtype not in valid_validator_types:
                        raise ValueError(
                            f"Skill '{skill_name}': validators[{i}] has invalid type {vtype!r}. "
                            f"Valid types: {', '.join(sorted(valid_validator_types))}"
                        )

        self.topological_sort()

    def topological_sort(self) -> List[str]:
        """
        Returns a topologically sorted list of skill names.
        Raises CycleDependencyError if a cycle is detected.
        Uses an iterative DFS with a stack to avoid recursion limit issues.
        """
        # 0 = unvisited (white), 1 = visiting (gray), 2 = visited (black)
        visited = {node: 0 for node in self.skills}
        order: List[str] = []
        path: List[str] = []

        for start_node in self.skills:
            if visited[start_node] != 0:
                continue

            # Stack element: (node, state)
            # state: 0 = first visit (push neighbors), 1 = post-order processing (backtracking)
            stack = [(start_node, 0)]

            while stack:
                curr, state = stack.pop()

                if state == 0:
                    if visited[curr] == 2:
                        continue
                    
                    visited[curr] = 1  # visiting (gray)
                    path.append(curr)
                    
                    # Push backtracking marker to stack first
                    stack.append((curr, 1))

                    # Iterate through neighbors in reverse order to preserve original sorting direction
                    for req in reversed(self.skills[curr].get("requires", [])):
                        req_state = visited[req]
                        if req_state == 1:
                            # Found a cycle! Build the cycle path cleanly.
                            cycle_start = path.index(req)
                            cycle_path = path[cycle_start:] + [req]
                            path_str = " -> ".join(cycle_path)
                            raise CycleDependencyError(
                                f"Cycle detected: {path_str}"
                            )
                        elif req_state == 0:
                            stack.append((req, 0))
                else:
                    # Post-order backtrack
                    if visited[curr] == 1:
                        visited[curr] = 2  # visited (black)
                        path.pop()
                        order.append(curr)

        return order

    def get_completed_nodes(self, completed_overrides: Optional[Set[str]] = None, mode: Optional[str] = None) -> Set[str]:
        """
        Dynamically inspects the filesystem to determine completion status.
        Supports both 'fluid' and 'strict' modes.
        Also supports checking for sentinel files (e.g., '.{skill_name}.done')
        for skills with no defined output files.
        """
        current_mode = mode or self.mode
        overrides = completed_overrides or set()
        self._last_validation_failures = {}
        self_completed = set()

        for skill_name, skill_info in self.skills.items():
            if skill_name in overrides:
                self_completed.add(skill_name)
                continue

            outputs = skill_info.get("outputs", [])

            if not outputs:
                sentinel_file = self.workspace_dir / f".{skill_name}.done"
                if sentinel_file.exists():
                    self_completed.add(skill_name)
                continue

            all_outputs_exist = True
            for pattern in outputs:
                full_pattern = str(self.workspace_dir / pattern)
                matched_files = glob.glob(full_pattern, recursive=True)
                if not matched_files:
                    all_outputs_exist = False
                    break

            if not all_outputs_exist:
                continue

            validators = skill_info.get("validators")
            if validators:
                sv = SemanticValidator(validators, self.workspace_dir, node_id=skill_name)
                result = sv.run()
                for w in result.warnings:
                    print(f"[WARNING] [{skill_name}] {w}", file=sys.stderr)
                if not result.passed:
                    first_error = result.errors[0]
                    if current_mode == "strict":
                        self._last_validation_failures[skill_name] = first_error
                        continue
                    else:
                        self._last_validation_failures[skill_name] = f"[SemanticValidationWarning] {first_error}"
                        print(f"[SemanticValidationWarning] [{skill_name}] {first_error}", file=sys.stderr)

            self_completed.add(skill_name)

        # Apply mode constraints in topological dependency order
        completed = set()
        sorted_skills = self.topological_sort()

        for skill_name in sorted_skills:
            if skill_name in self_completed:
                if current_mode == "strict":
                    requires = self.skills[skill_name].get("requires", [])
                    if all(req in completed for req in requires):
                        completed.add(skill_name)
                else:
                    completed.add(skill_name)

        return completed

    def get_validation_failures(self) -> Dict[str, str]:
        """Returns semantic validator failures from the last get_completed_nodes() call."""
        return dict(self._last_validation_failures)

    # ── P3: Execution Stack & Rollback Trace ─────────────────────────────────

    def _find_rollback_target(self, failed_node: str) -> Optional[str]:
        """
        Find the best rollback target for a failed node.
        Primary: mtime heuristic — requires whose outputs are newer than failed node's outputs
                 (picks the most recently modified upstream, i.e. max mtime).
        Fallback: BFS — topologically latest direct requires node.
        """
        requires = self.skills.get(failed_node, {}).get("requires", [])
        if not requires:
            return None

        # Get oldest output mtime for the failed node (most stale output)
        failed_outputs = self.skills.get(failed_node, {}).get("outputs", [])
        failed_mtime: Optional[float] = None
        for out in failed_outputs:
            p = self.workspace_dir / out
            if p.exists():
                t = p.stat().st_mtime
                if failed_mtime is None or t < failed_mtime:
                    failed_mtime = t

        # Primary: pick requires with the highest mtime among those newer than failed artifact
        if failed_mtime is not None:
            best_target: Optional[str] = None
            best_mtime: float = failed_mtime
            for req in requires:
                req_outputs = self.skills.get(req, {}).get("outputs", [])
                for out in req_outputs:
                    p = self.workspace_dir / out
                    if p.exists() and p.stat().st_mtime > best_mtime:
                        best_mtime = p.stat().st_mtime
                        best_target = req
            if best_target is not None:
                return best_target

        # Fallback: topologically latest direct requires
        sorted_skills = self.topological_sort()
        latest_req: Optional[str] = None
        latest_idx = -1
        for req in requires:
            try:
                idx = sorted_skills.index(req)
                if idx > latest_idx:
                    latest_idx = idx
                    latest_req = req
            except ValueError:
                pass
        return latest_req

    def rollback_trace(self, stack: "ExecutionStack") -> str:
        """
        Refresh state, analyze validation failures, find rollback targets, push to stack.
        Policy: push one frame per failing node until max_depth; then ROLLBACK_LIMIT_EXCEEDED.
        Returns a human-readable summary.
        """
        self.get_completed_nodes()  # force-refresh _last_validation_failures
        failures = self.get_validation_failures()

        if not failures:
            return "No validation failures detected. Rollback trace not needed."

        pushed: List[tuple] = []
        for node_id, reason in failures.items():
            if stack.depth() >= stack.max_depth:
                return (
                    f"ROLLBACK_LIMIT_EXCEEDED: stack depth {stack.depth()} reached max "
                    f"{stack.max_depth}. Manual intervention required.\n"
                    f"  Already pushed: {[p[0] for p in pushed]}"
                )
            target = self._find_rollback_target(node_id)
            if target is None:
                continue
            ok = stack.push(node_id, target, reason)
            if ok:
                sentinel = self.workspace_dir / f".{target}.rollback"
                sentinel.write_text(f"rollback: fixing {node_id}\n", encoding="utf-8")
                pushed.append((node_id, target))

        if not pushed:
            return "No rollback targets found (failed nodes may have no upstream requires)."

        lines = [f"Pushed {len(pushed)} rollback frame(s):"]
        for node_id, target in pushed:
            lines.append(f"  {node_id} → rollback target: {target}")
        return "\n".join(lines)

    def stack_pop(self, stack: "ExecutionStack") -> str:
        """
        Re-validate the top frame's failed node; if validators now pass, pop the frame and
        clear the .rollback sentinel. If still failing, return the current error without popping.
        """
        entry = stack.peek()
        if entry is None:
            return "Stack is empty. Nothing to pop."

        node_id = entry["node_id"]
        target = entry["rollback_target"]

        # Re-run validators for the failed node
        validators = self.skills.get(node_id, {}).get("validators")
        if validators:
            sv = SemanticValidator(validators, self.workspace_dir, node_id=node_id)
            result = sv.run()
            if not result.passed:
                return (
                    f"Cannot pop: {node_id} validators still failing.\n"
                    f"  {result.errors[0]}\n"
                    f"  Fix the artifact, then run --stack-pop again."
                )

        # Validators pass (or no validators) → clear sentinel and pop
        sentinel = self.workspace_dir / f".{target}.rollback"
        if sentinel.exists():
            sentinel.unlink()
        stack.pop()
        return f"Popped frame: {node_id} (rollback target was {target}). Sentinel cleared."

    def _get_all_dependencies(self, node: str) -> Set[str]:
        """Helper to find all transitive dependencies of a node (iterative)."""
        deps = set()
        stack = list(self.skills[node].get("requires", []))
        while stack:
            dep = stack.pop()
            if dep not in deps:
                deps.add(dep)
                stack.extend(self.skills[dep].get("requires", []))
        return deps

    def get_bypassed_dependencies(self, completed_overrides: Optional[Set[str]] = None) -> Dict[str, List[str]]:
        """
        Returns a dictionary mapping completed skill names to a list of their missing/bypassed
        upstream dependencies. Only computed in 'fluid' mode.
        """
        completed = self.get_completed_nodes(completed_overrides, mode="fluid")
        bypassed = {}
        
        for node in completed:
            all_deps = self._get_all_dependencies(node)
            missing = [dep for dep in sorted(all_deps) if dep not in completed]
            if missing:
                bypassed[node] = missing
                
        return bypassed

    def get_next_nodes(self, completed_overrides: Optional[Set[str]] = None) -> List[str]:
        """
        Returns a list of skills that are NOT completed but all their dependencies ARE completed.
        Returned list is sorted in topological order.
        """
        completed = self.get_completed_nodes(completed_overrides)
        sorted_skills = self.topological_sort()
        
        next_nodes = []
        for skill_name in sorted_skills:
            if skill_name in completed:
                continue

            # Check if all requirements are completed
            requires = self.skills[skill_name].get("requires", [])
            if all(req in completed for req in requires):
                next_nodes.append(skill_name)

        return next_nodes

    def get_blocked_nodes(self, completed_overrides: Optional[Set[str]] = None) -> Dict[str, List[str]]:
        """
        Returns a dictionary mapping each blocked skill name to a list of missing dependencies.
        A skill is blocked if it is not completed and at least one dependency is not completed.
        """
        completed = self.get_completed_nodes(completed_overrides)
        blocked = {}

        # Preserve graph topological order for clean outputs
        sorted_skills = self.topological_sort()

        for skill_name in sorted_skills:
            if skill_name in completed:
                continue

            requires = self.skills[skill_name].get("requires", [])
            missing_deps = [req for req in requires if req not in completed]
            
            if missing_deps:
                blocked[skill_name] = missing_deps

        return blocked

    # ------------------------------------------------------------------
    # P2: Bidirectional Spec Sync (ADR-002)
    # ------------------------------------------------------------------

    _STAGE_LABELS = {
        0: "Stage 0 — Standalone",
        1: "Stage 1 — Foundation",
        2: "Stage 2 — Requirements",
        3: "Stage 3 — Design",
        4: "Stage 4 — Implementation",
        5: "Stage 5 — Quality",
        6: "Stage 6 — Testing",
        7: "Stage 7 — Release",
    }
    _GRAPH_START = "<!-- SKILL-GRAPH-START -->"
    _GRAPH_END = "<!-- SKILL-GRAPH-END -->"

    def _generate_mermaid(self) -> str:
        """Build Mermaid graph LR block from current schema."""
        stage_nodes: Dict[int, List[str]] = {}
        for node_id, node_data in self.skills.items():
            stage = node_data.get("stage", 1)
            stage_nodes.setdefault(stage, []).append(node_id)

        lines = ["```mermaid", "graph LR"]
        for stage in sorted(stage_nodes.keys()):
            label = self._STAGE_LABELS.get(stage, f"Stage {stage}")
            lines.append(f'    subgraph stage{stage}["{label}"]')
            for node_id in sorted(stage_nodes[stage]):
                lines.append(f"        {node_id}")
            lines.append("    end")

        lines.append("")
        for node_id in sorted(self.skills.keys()):
            for req in sorted(self.skills[node_id].get("requires", [])):
                lines.append(f"    {req} --> {node_id}")
        lines.append("```")
        return "\n".join(lines)

    def sync_docs(self, readme_path: Path) -> int:
        """
        Update README.md Mermaid DAG between SKILL-GRAPH markers.
        If markers are absent, inserts block before "## The 35 Skills".
        Returns 1 if file was modified, 0 if already up-to-date.
        """
        if not readme_path.exists():
            raise FileNotFoundError(f"README not found: {readme_path}")

        content = readme_path.read_text(encoding="utf-8")
        mermaid = self._generate_mermaid()
        block = f"{self._GRAPH_START}\n{mermaid}\n{self._GRAPH_END}"

        if self._GRAPH_START in content and self._GRAPH_END in content:
            s = content.index(self._GRAPH_START)
            e = content.index(self._GRAPH_END) + len(self._GRAPH_END)
            new_content = content[:s] + block + content[e:]
        else:
            # Insert before the skills table or append
            INSERT_BEFORE = "## The 35 Skills"
            if INSERT_BEFORE in content:
                idx = content.index(INSERT_BEFORE)
                new_content = content[:idx] + block + "\n\n---\n\n" + content[idx:]
            else:
                new_content = content.rstrip() + "\n\n" + block + "\n"

        if new_content == content:
            return 0
        readme_path.write_text(new_content, encoding="utf-8")
        return 1

    def lint_drift(self, readme_path: Path, strict: bool = False) -> List[str]:
        """
        Compare README.md Mermaid DAG edges against schema requires.
        Returns list of drift strings. Empty = no drift.
        Raises DriftViolationError when strict=True and violations exist.
        """
        import re as _re

        if not readme_path.exists():
            raise FileNotFoundError(f"README not found: {readme_path}")

        content = readme_path.read_text(encoding="utf-8")
        if self._GRAPH_START not in content or self._GRAPH_END not in content:
            msg = "Mermaid block markers not found — run --sync-docs first"
            if strict:
                raise DriftViolationError(msg)
            return [f"[WARNING] {msg}"]

        s = content.index(self._GRAPH_START) + len(self._GRAPH_START)
        e = content.index(self._GRAPH_END)
        block = content[s:e]

        doc_edges: Set[tuple] = set()
        for line in block.splitlines():
            line = line.strip()
            if not line or line.startswith(("%%", "style", "subgraph", "end", "graph", "```", "classDef")):
                continue
            # Matches: A --> B  and  A --label--> B
            m = _re.match(r'^(\S+)\s+--[^>]*>\s+(\S+)', line)
            if m:
                doc_edges.add((m.group(1), m.group(2)))

        schema_edges: Set[tuple] = set()
        for node_id, node_data in self.skills.items():
            for req in node_data.get("requires", []):
                schema_edges.add((req, node_id))

        violations: List[str] = []
        for a, b in sorted(schema_edges - doc_edges):
            violations.append(f"MISSING in docs: {a} --> {b}")
        for a, b in sorted(doc_edges - schema_edges):
            violations.append(f"EXTRA in docs: {a} --> {b}")

        if violations and strict:
            raise DriftViolationError("\n".join(violations))
        return violations


def main() -> None:
    """CLI Entrypoint for the Skill Graph Engine."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Skill Graph CLI — Declarative Topology Engine for Agentic SDLC Skills"
    )
    parser.add_argument(
        "--schema",
        default="schemas/skill_graph_schema.yaml",
        help="Path to YAML schema file (default: schemas/skill_graph_schema.yaml)"
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Path to the workspace root directory (default: .)"
    )
    parser.add_argument(
        "--mode",
        choices=["fluid", "strict"],
        default="fluid",
        help="Navigation mode: 'fluid' (advisory) or 'strict' (blocking) (default: fluid)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show full status of the graph (completed, next, blocked nodes)"
    )
    parser.add_argument(
        "--next",
        action="store_true",
        help="Print next topologically ready skills"
    )
    parser.add_argument(
        "--blocked",
        action="store_true",
        help="Print blocked skills and their missing dependencies"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the YAML schema (checks syntax, undefined dependencies, and cycles)"
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Collapse BLOCKED list into stage-grouped counts (reduces noise when many skills are blocked)"
    )
    parser.add_argument(
        "--sync-docs",
        action="store_true",
        help="(P2) Regenerate Mermaid DAG in README.md between SKILL-GRAPH markers"
    )
    parser.add_argument(
        "--lint-drift",
        action="store_true",
        help="(P2) Compare README.md Mermaid DAG against schema; exit 1 if out of sync"
    )
    parser.add_argument(
        "--strict-lint",
        action="store_true",
        help="(P2) Used with --lint-drift: treat any drift as a hard error (exit 1)"
    )
    parser.add_argument(
        "--readme",
        default="README.md",
        help="Path to README.md (default: README.md, used by --sync-docs and --lint-drift)"
    )
    parser.add_argument(
        "--stack",
        action="store_true",
        help="(P3) Display the current execution stack from .engine_stack.json"
    )
    parser.add_argument(
        "--rollback-trace",
        action="store_true",
        help="(P3) Analyze validation failures, find rollback targets, push to execution stack"
    )
    parser.add_argument(
        "--stack-pop",
        action="store_true",
        help="(P3) Re-validate top frame; if passing, pop and clear .rollback sentinel"
    )
    parser.add_argument(
        "--stack-file",
        default=".engine_stack.json",
        help="Path to execution stack JSON file (default: .engine_stack.json)"
    )
    parser.add_argument(
        "--max-rollback-depth",
        type=int,
        default=ExecutionStack.DEFAULT_MAX_DEPTH,
        help=f"Maximum rollback stack depth (default: {ExecutionStack.DEFAULT_MAX_DEPTH})"
    )

    args = parser.parse_args()

    schema_path = Path(args.schema)
    workspace_path = Path(args.workspace)

    # 1. Validation and initialization
    try:
        engine = SkillGraphEngine(schema_path, workspace_path, mode=args.mode)
    except CycleDependencyError as e:
        print(f"❌ Cycle Dependency Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ File Not Found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Initialization Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.validate:
        print("✅ Schema is valid. No cycles or undefined dependencies detected!")
        sys.exit(0)

    # P2: --sync-docs
    if args.sync_docs:
        readme_path = Path(args.readme)
        try:
            changed = engine.sync_docs(readme_path)
            if changed:
                print(f"✅ {readme_path} updated with latest Mermaid DAG.")
            else:
                print(f"✅ {readme_path} already up-to-date.")
        except Exception as e:
            print(f"❌ sync-docs failed: {e}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    # P2: --lint-drift
    if args.lint_drift:
        readme_path = Path(args.readme)
        try:
            violations = engine.lint_drift(readme_path, strict=args.strict_lint)
        except DriftViolationError as e:
            print(f"❌ DriftViolationError:\n{e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ lint-drift failed: {e}", file=sys.stderr)
            sys.exit(1)
        if violations:
            for v in violations:
                print(v)
            if args.strict_lint:
                sys.exit(1)
        else:
            print("✅ No drift detected — README Mermaid DAG matches schema.")
        sys.exit(0)

    # P3: --stack / --rollback-trace / --stack-pop
    stack_path = workspace_path / args.stack_file
    if args.stack or args.rollback_trace or args.stack_pop:
        exec_stack = ExecutionStack(stack_path, max_depth=args.max_rollback_depth)

        if args.stack:
            print(exec_stack.display())
            sys.exit(0)

        if args.rollback_trace:
            msg = engine.rollback_trace(exec_stack)
            print(msg)
            sys.exit(0)

        if args.stack_pop:
            msg = engine.stack_pop(exec_stack)
            print(msg)
            sys.exit(0)

    # Calculate status
    completed = engine.get_completed_nodes()
    validation_failures = engine.get_validation_failures()
    next_nodes = engine.get_next_nodes()
    blocked = engine.get_blocked_nodes()
    bypassed_info = engine.get_bypassed_dependencies() if args.mode == "fluid" else {}

    # 2. Output handling
    if args.next:
        for node in next_nodes:
            print(node)
        sys.exit(0)

    if args.blocked:
        for node, deps in blocked.items():
            print(f"{node} is blocked by: {', '.join(deps)}")
        sys.exit(0)

    # Default to status if no specific option is requested
    # Let's print a beautiful report
    print("\n" + "=" * 60)
    print("           SKILL GRAPH RUNTIME TOPOLOGY ENGINE          ")
    print("=" * 60)
    print(f"Schema:    {schema_path}")
    print(f"Workspace: {workspace_path.absolute()}")
    print(f"Mode:      {args.mode.upper()}")
    print("-" * 60)

    print(f"\n✅ COMPLETED SKILLS ({len(completed)}):")
    if completed:
        # Sort in topological order for readability
        sorted_completed = [s for s in engine.topological_sort() if s in completed]
        for node in sorted_completed:
            stage = engine.skills[node].get("stage", 1)
            bypassed_deps = bypassed_info.get(node, [])
            validator_warn = validation_failures.get(node, "")
            suffix = ""
            if bypassed_deps:
                suffix += f" (Bypassed upstream: {', '.join(bypassed_deps)})"
            if validator_warn:
                suffix += f" ⚠️  {validator_warn}"
            print(f"  [x] Stage {stage}: {node}{suffix}")
    else:
        print("  (None)")

    print(f"\n🚀 NEXT TO RUN ({len(next_nodes)}):")
    if next_nodes:
        for node in next_nodes:
            stage = engine.skills[node].get("stage", 1)
            print(f"  [ ] Stage {stage}: {node}")
    else:
        print("  (None)")

    print(f"\n🔒 BLOCKED SKILLS ({len(blocked)}):")
    if blocked:
        if args.compact:
            stage_counts: dict = {}
            for node in blocked:
                stage = engine.skills[node].get("stage", 1)
                stage_counts[stage] = stage_counts.get(stage, 0) + 1
            for stage in sorted(stage_counts):
                print(f"  [Stage {stage}] {stage_counts[stage]} blocked  (omit --compact to expand)")
        else:
            for node, deps in blocked.items():
                stage = engine.skills[node].get("stage", 1)
                print(f"  [ ] Stage {stage}: {node}")
                print(f"      Missing: {', '.join(deps)}")
    else:
        print("  (None)")

    # Print Adaptive Catch-up Suggestions in fluid mode (grouped by stage)
    if args.mode == "fluid" and bypassed_info:
        print("\n💡 ADAPTIVE CATCH-UP SUGGESTIONS (智慧補足建議):")
        print("-" * 60)
        
        # Collect all unique bypassed skills
        all_bypassed_skills = set()
        for missing in bypassed_info.values():
            all_bypassed_skills.update(missing)
            
        # Group unique bypassed skills by stage
        stage_groups = {}
        for skill in all_bypassed_skills:
            stage = engine.skills[skill].get("stage", 1)
            stage_groups.setdefault(stage, []).append(skill)
            
        # Print grouped suggestions in stage order
        for stage in sorted(stage_groups.keys()):
            skills_in_stage = sorted(stage_groups[stage])
            print(f"  [Stage {stage}] 補全建議 ({len(skills_in_stage)} 個):")
            for m in skills_in_stage:
                missing_outputs = engine.skills[m].get("outputs", [])
                outputs_str = f" ➔ 產生 {', '.join(missing_outputs)}" if missing_outputs else " (環境配置/工具類哨兵標記)"
                print(f"    👉 補完 '{m}'{outputs_str}")
                
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
