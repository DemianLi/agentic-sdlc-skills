#!/usr/bin/env python3
"""
Token Budget Checker — CI runner for s0-skill-budget D/I/S audit.

Exit codes:
  0 — all skills PASS or PARTIAL
  1 — at least one skill FAIL

Usage:
  python3 budget_check.py                     # audit all skills/*/SKILL.md
  python3 budget_check.py skills/s4-tdd/SKILL.md [...]  # audit specific files
"""
import re
import os
import sys
import glob


INDEX_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "schemas", "SKILL_INDEX.yaml"
)


def load_index(path):
    if not os.path.exists(path):
        return None, None
    index_map = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line == "index:":
                continue
            if ":" in line:
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip()
                if k and v:
                    index_map[k] = v
    return index_map, True


def audit(skill_path, index_map):
    with open(skill_path) as f:
        raw = f.read()

    # description
    desc_block = re.search(
        r"^description:\s*>\n((?:  .+\n?)+)", raw, re.MULTILINE
    )
    description = (
        " ".join(l.strip() for l in desc_block.group(1).splitlines()).strip()
        if desc_block
        else ""
    )

    # skill name
    name_match = re.search(r"^name:\s*(.+)", raw, re.MULTILINE)
    skill_name = name_match.group(1).strip() if name_match else ""

    file_size = os.path.getsize(skill_path)

    # sections
    sections, current, count = {}, None, 0
    for line in raw.splitlines():
        if re.match(r"^#{2,3} ", line):
            if current:
                sections[current] = count
            current, count = line.strip()[:70], 0
        else:
            count += 1
    if current:
        sections[current] = count

    # ── D axis ────────────────────────────────────────────
    est_tokens = len(description) // 4
    d1 = est_tokens <= 40
    d2 = description.startswith("Use when")
    d3 = any(w in description for w in ["outputs", "Outputs", "checklist", "report", "Outputs:"])
    d4 = "NOT" in description
    d5 = not any(w in description for w in ["Step", "->", "Workflow"])

    # ── I axis ────────────────────────────────────────────
    if index_map is None:
        i1 = i2 = i3 = None  # N/A
        matched_keys = []
    else:
        matched_keys = [k for k, v in index_map.items() if v == skill_name]
        i1 = skill_name in index_map.values()
        i2 = len(matched_keys) >= 2
        i3 = True  # 1:1 index design enforces mutual exclusion structurally

    # ── S axis ────────────────────────────────────────────
    s1 = file_size <= 10240
    oversized = [(n, c) for n, c in sections.items() if c > 50]
    s2 = not oversized
    reads_match = re.search(r"\*\*Reads\*\*:(.*?)(?:\n|$)", raw)
    s3 = True
    if reads_match:
        for ref in re.findall(r"`([^`]+\.(?:yaml|md|json|py))`", reads_match.group(1)):
            ref_path = os.path.join(os.path.dirname(skill_path), ref)
            repo_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "..", ref
            )
            if not os.path.exists(ref_path) and not os.path.exists(os.path.normpath(repo_path)):
                s3 = False

    # ── overall ───────────────────────────────────────────
    bool_marks = [d1, d2, d4, d5, s1, s2]
    if i1 is not None:
        bool_marks += [i1, i2]

    if not all(bool_marks):
        overall = "FAIL"
    elif not d3 or (i3 is not None and not i3) or not s3:
        overall = "PARTIAL"
    else:
        overall = "PASS"

    return {
        "skill": skill_name,
        "path": skill_path,
        "overall": overall,
        "est_tokens": est_tokens,
        "file_size": file_size,
        "D": {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5},
        "I": {"I1": i1, "I2": i2, "I3": i3, "keywords": matched_keys},
        "S": {"S1": s1, "S2": s2, "S3": s3, "oversized": oversized},
    }


def fmt(val):
    if val is None:
        return "N/A"
    return "✅" if val else "❌"


def print_report(result):
    d = result["D"]
    i = result["I"]
    s = result["S"]
    print(
        f"  {result['overall']:<8} {result['skill']}"
        f"  ({result['file_size'] / 1024:.1f} KB, ~{result['est_tokens']} tokens)"
    )
    if result["overall"] != "PASS":
        issues = []
        if not d["D1"]: issues.append(f"D1: ~{result['est_tokens']} tokens > 40")
        if not d["D2"]: issues.append("D2: missing 'Use when'")
        if not d["D3"]: issues.append("D3: no output artifact named")
        if not d["D4"]: issues.append("D4: no NOT exclusion clause")
        if not d["D5"]: issues.append("D5: process verb found")
        if i["I1"] is False: issues.append("I1: skill not in SKILL_INDEX.yaml")
        if i["I2"] is False: issues.append(f"I2: only {len(i['keywords'])} keyword(s) (need ≥2)")
        if not s["S1"]: issues.append(f"S1: {result['file_size']} bytes > 10240")
        if not s["S2"]: issues.append(f"S2: oversized sections: {s['oversized']}")
        if not s["S3"]: issues.append("S3: referenced file missing")
        for issue in issues:
            print(f"           → {issue}")


def main():
    repo_root = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    os.chdir(repo_root)

    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = sorted(glob.glob("skills/*/SKILL.md"))

    index_map, _ = load_index(INDEX_PATH)
    if index_map is None:
        print("⚠️  schemas/SKILL_INDEX.yaml not found — I-axis checks skipped")

    print(f"\nToken Budget Check — {len(paths)} skill(s)\n")
    results = [audit(p, index_map) for p in paths]

    fails = [r for r in results if r["overall"] == "FAIL"]
    partials = [r for r in results if r["overall"] == "PARTIAL"]
    passes = [r for r in results if r["overall"] == "PASS"]

    for r in results:
        print_report(r)

    print(
        f"\n{'─'*50}\n"
        f"PASS: {len(passes)}  PARTIAL: {len(partials)}  FAIL: {len(fails)}"
    )

    if fails:
        print("\nFAIL — fix the issues above before merging.")
        sys.exit(1)

    print("\nOK — all skills within token budget.")
    sys.exit(0)


if __name__ == "__main__":
    main()
