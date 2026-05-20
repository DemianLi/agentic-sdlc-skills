#!/usr/bin/env python3
"""
compare_actual_prompts.py — Calculates and compares the exact character, word,
and estimated token counts of actual LLM prompt payloads under the Legacy Paradigm 
versus the new Skill Graph Paradigm across different SDLC stages.
"""

import sys
from pathlib import Path

# Add script directory to path to import engine
sys.path.append(str(Path(__file__).parent))
try:
    from engine import SkillGraphEngine
except ImportError:
    print("Error: engine.py not found in the script directory.", file=sys.stderr)
    sys.exit(1)

# Standard OpenAI estimate for technical code/markdown text:
# Technical text with code blocks, yaml, and punctuation averages ~1.35 tokens per word.
TOKEN_WORD_RATIO = 1.35

SYSTEM_PROMPT = """You are Antigravity, an expert AI software engineer. 
You follow strict engineering disciplines, write immutable code, handle all errors, 
and ensure robust quality.
"""

USER_INPUT = "Please help me implement the next step in our project."

def get_skill_content(skill_dir: Path) -> str:
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        return skill_file.read_text(encoding="utf-8")
    return ""

def build_full_prompt(system: str, skills_content: str, workspace_info: str, user_query: str) -> str:
    return f"""=== SYSTEM INSTRUCTIONS ===
{system}

=== ACTIVE SKILL GUIDELINES ===
{skills_content}

=== CURRENT WORKSPACE STATE ===
{workspace_info}

=== USER REQUEST ===
{user_query}
"""

def main():
    script_dir = Path(__file__).parent.resolve()
    workspace = script_dir.parent.parent.parent.resolve()
    schema_path = workspace / "schemas" / "skill_graph_schema.yaml"

    if not schema_path.exists():
        print(f"Error: Schema not found at {schema_path}", file=sys.stderr)
        sys.exit(1)

    # Initialize Engine
    engine = SkillGraphEngine(schema_path, workspace)
    defined_skills = sorted(list(engine.skills.keys()))

    # Read all skills content
    all_skills_data = {}
    for skill in defined_skills:
        skill_dir = workspace / "skills" / skill
        all_skills_data[skill] = get_skill_content(skill_dir)

    print("\n" + "=" * 80)
    print("     🛡️  ACTUAL PROMPT PAYLOAD COMPARISON (BEFORE vs. AFTER UPGRADE) 🛡️     ")
    print("=" * 80)
    print(f"Workspace: {workspace}")
    print(f"Total skills defined: {len(defined_skills)}")
    print("-" * 80)

    # We will test three representative scenarios of the development lifecycle:
    # Scenario A: Stage 1 (Initial Setup) - Only s1-define-rules is active
    # Scenario B: Stage 4 (TDD & Implementation) - s4-tdd and s4-impl-task are active
    # Scenario C: Stage 6 (Verification) - s6-verify-release is active

    scenarios = [
        {
            "name": "Scenario A: Stage 1 (Project Kickoff)",
            "active_skills": ["s1-define-rules"],
            "workspace_state": "Files on disk: CONTEXT.md. No design files exist yet."
        },
        {
            "name": "Scenario B: Stage 4 (Coding & Testing)",
            "active_skills": ["s4-tdd", "s4-impl-task"],
            "workspace_state": "Files on disk: CONTEXT.md, RULES.md, docs/specs/vision.md, docs/arch/design.md, TASK_DAG.md."
        },
        {
            "name": "Scenario C: Stage 6 (Quality Assurance & Release)",
            "active_skills": ["s6-verify-release"],
            "workspace_state": "Files on disk: all source code files, tests/test_engine.py, docs/tests/integration-results.md."
        }
    ]

    for sc in scenarios:
        name = sc["name"]
        active = sc["active_skills"]
        ws_state = sc["workspace_state"]

        print(f"\n🎬 {name}")
        print(f"  • Topologically Active Skills in Graph: {', '.join(active)}")
        print(f"  • Workspace State: {ws_state}")
        print("-" * 80)

        # 1. Compile Legacy Prompt (Loads ALL 28 skills)
        legacy_skills_text = "\n\n".join([f"--- SKILL: {s} ---\n{content}" for s, content in all_skills_data.items() if content])
        legacy_prompt = build_full_prompt(SYSTEM_PROMPT, legacy_skills_text, ws_state, USER_INPUT)

        legacy_chars = len(legacy_prompt)
        legacy_words = len(legacy_prompt.split())
        legacy_tokens = int(legacy_words * TOKEN_WORD_RATIO)

        # 2. Compile Skill Graph Prompt (Loads ONLY active skills)
        graph_skills_text = "\n\n".join([f"--- SKILL: {s} ---\n{all_skills_data[s]}" for s in active if all_skills_data.get(s)])
        graph_prompt = build_full_prompt(SYSTEM_PROMPT, graph_skills_text, ws_state, USER_INPUT)

        graph_chars = len(graph_prompt)
        graph_words = len(graph_prompt.split())
        graph_tokens = int(graph_words * TOKEN_WORD_RATIO)

        # 3. Calculate Differences
        diff_chars = legacy_chars - graph_chars
        diff_words = legacy_words - graph_words
        diff_tokens = legacy_tokens - graph_tokens
        reduction_rate = (diff_tokens / legacy_tokens) * 100 if legacy_tokens > 0 else 0

        # Print Side-by-Side Comparison
        print(f"  {'-' * 33} | {'-' * 17} | {'-' * 20}")
        print(f"  {'Metric':<33} | {'Legacy Paradigm':<17} | {'Skill Graph':<20}")
        print(f"  {'-' * 33} | {'-' * 17} | {'-' * 20}")
        print(f"  {'Total Prompt Characters':<33} | {legacy_chars:<17,} | {graph_chars:<20,}")
        print(f"  {'Total Prompt Words':<33} | {legacy_words:<17,} | {graph_words:<20,}")
        print(f"  {'Estimated Prompt Tokens (GPT-4)':<33} | \033[91m{legacy_tokens:<17,}\033[0m | \033[92m{graph_tokens:<20,}\033[0m")
        print(f"  {'-' * 33} | {'-' * 17} | {'-' * 20}")
        print(f"  🎁 \033[1;94mNET PROMPT TOKENS SAVED\033[0m:        \033[1;92m{diff_tokens:,} tokens\033[0m")
        print(f"  🌟 \033[1;94mTOKEN REDUCTION RATE\033[0m:           \033[1;92m{reduction_rate:.2f}%\033[0m")
        print("=" * 80)

if __name__ == "__main__":
    main()
