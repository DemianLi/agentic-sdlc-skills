"""
SkillGraphEngine — Declarative YAML Schema + Runtime Topology Engine for Skill Graphs.

Tracks SDLC skill execution state, validates dependencies, computes completed/next/blocked
nodes, and performs topological sorting and cycle detection.
"""

import glob
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Union, Optional


class CycleDependencyError(ValueError):
    """Raised when a cycle is detected in the dependency graph."""
    pass


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


class SkillGraphEngine:
    """
    The runtime topology engine for the Skill Graph concept.
    """

    def __init__(self, schema_path: Union[str, Path], workspace_dir: Union[str, Path], mode: str = "fluid"):
        self.schema_path = Path(schema_path)
        self.workspace_dir = Path(workspace_dir)
        self.mode = mode  # "fluid" or "strict"
        self.skills = self._load_schema()
        # Validate schema upon initialization
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
            # If yaml parsing yields empty or invalid format, raise
            if not isinstance(data, dict) or "skills" not in data:
                raise ValueError("Invalid schema file format.")
            return data["skills"]
        except (ImportError, Exception):
            # Fall back to custom robust parser
            data = parse_simple_yaml(content)
            if "skills" not in data or not data["skills"]:
                raise ValueError("Failed to parse schema with fallback parser.")
            return data["skills"]

    def _validate_schema(self) -> None:
        """
        Ensures all requires are defined skills in the graph, detects cycles early,
        and validates that each skill contains only valid fields to prevent typos.
        """
        valid_keys = {"stage", "requires", "outputs"}
        # Ensure all referenced dependencies exist in the graph and have valid structures
        for skill_name, skill_info in self.skills.items():
            if not isinstance(skill_info, dict):
                raise ValueError(f"Skill '{skill_name}' configuration must be a dictionary.")
            
            # Check for invalid keys (typo detection)
            invalid_keys = set(skill_info.keys()) - valid_keys
            if invalid_keys:
                raise ValueError(
                    f"Invalid configuration keys found in skill '{skill_name}': {', '.join(sorted(invalid_keys))}. "
                    f"Supported keys are: {', '.join(sorted(valid_keys))} (check for typos like 'requiers' or 'outpus')"
                )

            # Validate value types
            if not isinstance(skill_info.get("stage", 1), int):
                raise ValueError(f"Skill '{skill_name}': 'stage' must be an integer")
            for key in ("requires", "outputs"):
                val = skill_info.get(key, [])
                if not isinstance(val, list):
                    raise ValueError(f"Skill '{skill_name}': '{key}' must be a list, got {type(val).__name__}")

            for req in skill_info.get("requires", []):
                if req not in self.skills:
                    raise ValueError(
                        f"Skill '{skill_name}' requires undefined skill '{req}'"
                    )
        # Perform cycle detection
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
        self_completed = set()

        for skill_name, skill_info in self.skills.items():
            if skill_name in overrides:
                self_completed.add(skill_name)
                continue

            outputs = skill_info.get("outputs", [])

            # Sentinel file check for empty outputs
            if not outputs:
                sentinel_file = self.workspace_dir / f".{skill_name}.done"
                if sentinel_file.exists():
                    self_completed.add(skill_name)
                    continue
                # If no outputs, no override, and no sentinel file, it is incomplete
                continue

            # Check files on disk
            all_outputs_exist = True
            for pattern in outputs:
                # Resolve relative path using glob matching inside workspace
                full_pattern = str(self.workspace_dir / pattern)
                matched_files = glob.glob(full_pattern, recursive=True)
                if not matched_files:
                    all_outputs_exist = False
                    break

            if all_outputs_exist:
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

    # Calculate status
    completed = engine.get_completed_nodes()
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
            if bypassed_deps:
                print(f"  [x] Stage {stage}: {node} (Bypassed upstream: {', '.join(bypassed_deps)})")
            else:
                print(f"  [x] Stage {stage}: {node}")
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
