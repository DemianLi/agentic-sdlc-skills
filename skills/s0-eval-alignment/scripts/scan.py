#!/usr/bin/env python3
"""
s0-eval-alignment scanner — batch alignment check for all s1-s7 skills.

Usage:
  python3 skills/s0-eval-alignment/scripts/scan.py
  python3 skills/s0-eval-alignment/scripts/scan.py --stage s4
  python3 skills/s0-eval-alignment/scripts/scan.py --write

Exits 0 if all scanned skills are ALIGNED; exits 1 if any PARTIAL or DRIFTED.

Keyword map must be kept in sync with:
  skills/s0-eval-alignment/references/skill-design-intent.md
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Keyword map — update when skill-design-intent.md changes
# ---------------------------------------------------------------------------
KEYWORDS: dict[str, list[str]] = {
    "s1-define-rules":     ["coding standard", "lint", "architecture", "RULES.md", "security"],
    "s1-config-context":   ["context", "configure", "role", "identity", "agent", "global"],
    "s1-lock-tech-stack":  ["tech stack", "dependency", "language version", "framework", "package"],
    "s1-git-guardrails":   ["git", "security", "compliance", "branch", "commit", "hook"],
    "s2-capture-vision":   ["vision", "idea", "pain point", "requirement", "business"],
    "s2-align-req":        ["align", "conflict", "ambiguity", "boundary", "clarify"],
    "s2-struct-req":       ["structured", "PRD", "User Story", "Gherkin", "BDD"],
    "s2-snapshot-ctx":     ["snapshot", "context", "requirements", "iteration"],
    "s3-eval-system":      ["existing system", "impact", "code", "Schema", "API", "evaluate"],
    "s3-design-arch":      ["design", "architecture", "data structure", "interface", "sequence"],
    "s3-breakdown-wbs":    ["atomic", "breakdown", "WBS", "minimal", "execution"],
    "s3-build-dag":        ["DAG", "dependency", "topology", "concurrent", "sequence"],
    "s4-setup-env":        ["environment", "worktree", "branch", "sandbox", "init", "setup"],
    "s4-impl-task":        ["atomic task", "business logic", "implement", "core", "rules"],
    "s4-tdd":              ["test", "TDD", "pytest", "spec", "coverage"],
    "s4-local-debug":      ["compile", "debug", "log", "stack trace", "error"],
    "s5-sast-lint":        ["lint", "static analysis", "security", "SAST", "vulnerability"],
    "s5-audit-rules":      ["compliance", "rule", "architecture", "RULES.md", "violation"],
    "s5-pr-review":        ["PR", "pull request", "review", "refactor", "logic"],
    "s5-fix-optimize":     ["fix", "optimize", "resolve", "analysis", "audit"],
    "s6-test-integration": ["integration", "module", "merge", "interface"],
    "s6-test-e2e":         ["E2E", "end-to-end", "user behavior", "boundary", "edge"],
    "s6-test-perf":        ["performance", "stress", "concurrent", "memory", "database"],
    "s6-verify-release":   ["coverage", "test report", "release", "verify"],
    "s7-build-artifact":   ["build", "package", "artifact", "Docker", "image"],
    "s7-release-notes":    ["CHANGELOG", "release", "git log", "upgrade"],
    "s7-deploy":           ["deploy", "deployment", "GitOps", "production", "push"],
    "s7-telemetry":        ["telemetry", "monitoring", "anomaly", "feedback loop"],
}

STEPS: list[tuple[str, str]] = [
    ("s1-define-rules",     "1.1"), ("s1-config-context",   "1.2"),
    ("s1-lock-tech-stack",  "1.3"), ("s1-git-guardrails",   "1.1"),
    ("s2-capture-vision",   "2.1"), ("s2-align-req",        "2.2"),
    ("s2-struct-req",       "2.3"), ("s2-snapshot-ctx",     "2.4"),
    ("s3-eval-system",      "3.1"), ("s3-design-arch",      "3.2"),
    ("s3-breakdown-wbs",    "3.3"), ("s3-build-dag",        "3.4"),
    ("s4-setup-env",        "4.1"), ("s4-impl-task",        "4.2"),
    ("s4-tdd",              "4.3"), ("s4-local-debug",      "4.4"),
    ("s5-sast-lint",        "5.1"), ("s5-audit-rules",      "5.2"),
    ("s5-pr-review",        "5.3"), ("s5-fix-optimize",     "5.4"),
    ("s6-test-integration", "6.1"), ("s6-test-e2e",        "6.2"),
    ("s6-test-perf",        "6.3"), ("s6-verify-release",  "6.4"),
    ("s7-build-artifact",   "7.1"), ("s7-release-notes",   "7.2"),
    ("s7-deploy",           "7.3"), ("s7-telemetry",       "7.4"),
]

# C4: only these skills must have a Red Flag table
C4_SKILLS = {"s3-eval-system", "s5-pr-review", "s6-verify-release", "s5-audit-rules"}

# C1: stage-boundary skills end with "Awaiting your approval";
#     terminal skills (no downstream) use "report DONE";
#     all other intra-stage skills use "proceed immediately to"
BOUNDARY_SKILLS = {
    "s1-lock-tech-stack", "s2-snapshot-ctx", "s3-build-dag",
    "s4-local-debug", "s5-fix-optimize", "s6-verify-release", "s7-telemetry",
}
TERMINAL_SKILLS = {"s1-git-guardrails"}  # standalone; no downstream chain

WORKFLOW_RE = re.compile(r'Step\s+\d|Workflow|->|First:|Then:|Finally:', re.IGNORECASE)


# ---------------------------------------------------------------------------

def scan_skill(skill: str, step: str, base: Path) -> dict:
    path = base / skill / "SKILL.md"
    result = {"skill": skill, "step": step, "path": str(path)}

    if not path.exists():
        result["status"] = "MISSING"
        return result

    content = path.read_text(encoding="utf-8")
    lower = content.lower()

    # Q — keyword alignment
    kws = KEYWORDS.get(skill, [])
    hits = sum(1 for kw in kws if kw.lower() in lower)
    result["q_hits"] = hits
    result["q"] = "ALIGNED" if hits >= 3 else ("PARTIAL" if hits >= 1 else "DRIFTED")

    # C1 — HARD-GATE + gate phrase
    # boundary skills must have "Awaiting your approval"
    # intra-stage skills must have "proceed immediately to"
    result["c1_gate"]     = "HARD-GATE" in content
    if skill in BOUNDARY_SKILLS:
        result["c1_approval"] = "Awaiting your approval" in content
    elif skill in TERMINAL_SKILLS:
        result["c1_approval"] = "report DONE" in content
    else:
        result["c1_approval"] = "proceed immediately to" in content

    # C2 — artifact chain
    result["c2_reads"]  = "Reads"  in content
    result["c2_writes"] = "Writes" in content

    # C3 — Matt Pocock: description must NOT summarise workflow
    desc_match = re.search(
        r'^description:\s*[>|]?\s*(.*?)(?=^---|\Z)',
        content, re.MULTILINE | re.DOTALL
    )
    desc = (desc_match.group(1) if desc_match else "")[:400]
    result["c3_pass"] = not bool(WORKFLOW_RE.search(desc))

    # C4 — red flag table (only for designated skills)
    if skill in C4_SKILLS:
        result["c4_required"] = True
        result["c4_pass"] = bool(re.search(
            r'Red Flag|Common Rationalization|Stop', content, re.IGNORECASE
        ))
    else:
        result["c4_required"] = False
        result["c4_pass"] = True

    # Overall
    all_c1 = result["c1_gate"] and result["c1_approval"]
    all_c2 = result["c2_reads"] and result["c2_writes"]
    if result["q"] == "ALIGNED" and all_c1 and all_c2 and result["c3_pass"] and result["c4_pass"]:
        result["status"] = "ALIGNED"
    elif not all_c1 or not all_c2 or not result["c3_pass"] or not result["c4_pass"]:
        result["status"] = "DRIFTED"
    else:
        result["status"] = "PARTIAL"

    return result


def sym(ok: bool) -> str:
    return "✅" if ok else "❌"


def q_sym(r: dict) -> str:
    q, h = r["q"], r["q_hits"]
    if q == "ALIGNED": return f"✅({h})"
    if q == "PARTIAL": return f"⚠️({h})"
    return f"❌(0)"


def overall_sym(status: str) -> str:
    return {"ALIGNED": "✅ ALIGNED", "PARTIAL": "⚠️ PARTIAL",
            "DRIFTED": "❌ DRIFTED", "MISSING": "❌ MISSING"}.get(status, status)


def build_report(results: list, stage_filter: Optional[str]) -> str:
    today = date.today().isoformat()
    lines = [
        f"# Alignment Scan Report",
        f"**掃描範圍**: `skills/s1-*` 至 `skills/s7-*`（{len(results)} 個 skill）",
        f"**Date**: {today}",
        f"**Evaluator**: s0-eval-alignment",
        f"**基線**: `skills/s0-eval-alignment/references/skill-design-intent.md`",
        "",
        "---",
        "",
        "## 總覽表",
        "",
        "| Skill | Step | Q 對齊 | C1 GATE | C1 Phrase | C2 Chain | C3 Description | C4 RedFlag | 整體 |",
        "|-------|------|--------|---------|-----------|----------|----------------|------------|------|",
    ]

    aligned = partial = drifted = missing = 0
    partials = []
    drifteds = []

    for r in results:
        if r["status"] == "MISSING":
            lines.append(f"| {r['skill']} | {r['step']} | — | — | — | — | — | — | ❌ MISSING |")
            missing += 1
            continue

        c4_cell = sym(r["c4_pass"]) if r["c4_required"] else "—"
        row = (
            f"| {r['skill']} | {r['step']} | {q_sym(r)} "
            f"| {sym(r['c1_gate'])} | {sym(r['c1_approval'])} "
            f"| {sym(r['c2_reads'] and r['c2_writes'])} "
            f"| {'✅ PASS' if r['c3_pass'] else '❌ FAIL'} "
            f"| {c4_cell} | {overall_sym(r['status'])} |"
        )
        lines.append(row)

        if r["status"] == "ALIGNED":   aligned += 1
        elif r["status"] == "PARTIAL": partial += 1; partials.append(r)
        elif r["status"] == "DRIFTED": drifted += 1; drifteds.append(r)

    lines += [
        "",
        f"**總計：{aligned}/{len(results)} ✅ ALIGNED，"
        f"{partial}/{len(results)} ⚠️ PARTIAL，"
        f"{drifted}/{len(results)} ❌ DRIFTED**",
        "",
        "---",
        "",
        "## 強制執行機制掃描（C1–C4）",
        "",
        "| 檢查 | 結果 |",
        "|------|------|",
        f"| C1 HARD-GATE 存在 | {sum(r.get('c1_gate',False) for r in results if r['status']!='MISSING')}/{len(results)} |",
        f"| C1 gate phrase (boundary: 'Awaiting…' / intra: 'proceed immediately to') | {sum(r.get('c1_approval',False) for r in results if r['status']!='MISSING')}/{len(results)} |",
        f"| C2 Reads + Writes 聲明 | {sum(r.get('c2_reads',False) and r.get('c2_writes',False) for r in results if r['status']!='MISSING')}/{len(results)} |",
        f"| C3 Description 不含流程描述詞（Matt Pocock）| {sum(r.get('c3_pass',False) for r in results if r['status']!='MISSING')}/{len(results)} |",
        f"| C4 紅旗表（{len(C4_SKILLS)} 個高風險 skill）| {sum(r.get('c4_pass',False) for r in results if r.get('c4_required',False))}/{len(C4_SKILLS)} |",
    ]

    if partials or drifteds:
        lines += ["", "---", "", "## 需關注清單"]
        for r in drifteds + partials:
            tag = "❌ DRIFTED" if r["status"] == "DRIFTED" else "⚠️ PARTIAL"
            issues = []
            if r["q"] != "ALIGNED": issues.append(f"Q: {r['q_hits']} keywords (需 ≥3)")
            if not r["c1_gate"]: issues.append("C1: 缺 HARD-GATE")
            if not r["c1_approval"]:
                if r["skill"] in BOUNDARY_SKILLS:
                    phrase = '"Awaiting your approval"'
                elif r["skill"] in TERMINAL_SKILLS:
                    phrase = '"report DONE"'
                else:
                    phrase = '"proceed immediately to"'
                issues.append(f"C1: 缺 {phrase}")
            if not (r["c2_reads"] and r["c2_writes"]): issues.append("C2: 缺 Reads/Writes 聲明")
            if not r["c3_pass"]: issues.append("C3: description 含流程描述詞（Matt Pocock 違規）")
            if r.get("c4_required") and not r.get("c4_pass"): issues.append("C4: 缺紅旗表")
            lines.append(f"\n### {r['skill']} — {tag}\n")
            for i in issues:
                lines.append(f"- {i}")
    else:
        lines += ["", "---", "", "## 結論", "", "全部 skill 均 ALIGNED。無需修復。"]

    lines += [
        "",
        "---",
        "",
        f"*此報告由 `skills/s0-eval-alignment/scripts/scan.py` 自動產出。"
        f"下次掃描建議在任何 s1-s7 skill 有重大改動後執行。*",
    ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="s0-eval-alignment batch scanner")
    parser.add_argument("--stage", metavar="sN", help="只掃描指定 stage，例如 --stage s4")
    parser.add_argument("--write", action="store_true", help="將報告寫入 docs/skill-evals/")
    parser.add_argument(
        "--base", default="skills",
        help="skills 目錄路徑（預設: skills）"
    )
    args = parser.parse_args()

    base = Path(args.base)
    if not base.exists():
        print(f"ERROR: skills directory not found: {base}", file=sys.stderr)
        sys.exit(2)

    steps = STEPS
    if args.stage:
        prefix = args.stage.lower()
        steps = [(s, t) for s, t in STEPS if s.startswith(prefix)]
        if not steps:
            print(f"ERROR: no skills matched --stage {args.stage}", file=sys.stderr)
            sys.exit(2)

    results = [scan_skill(skill, step, base) for skill, step in steps]

    # Console summary
    print(f"\n{'Skill':<25} {'Step':<5} {'Q':<8} {'C1':<4} {'C2':<4} {'C3':<9} Overall")
    print("-" * 72)
    for r in results:
        if r["status"] == "MISSING":
            print(f"{'  ' + r['skill']:<25} {r['step']:<5} {'—':<8} {'—':<4} {'—':<4} {'—':<9} ❌ MISSING")
            continue
        c3 = "✅ PASS" if r["c3_pass"] else "❌ FAIL"
        c1 = "✅" if (r["c1_gate"] and r["c1_approval"]) else "❌"
        c2 = "✅" if (r["c2_reads"] and r["c2_writes"]) else "❌"
        print(f"  {r['skill']:<23} {r['step']:<5} {q_sym(r):<8} {c1:<4} {c2:<4} {c3:<9} {overall_sym(r['status'])}")

    aligned = sum(1 for r in results if r["status"] == "ALIGNED")
    partial = sum(1 for r in results if r["status"] == "PARTIAL")
    drifted = sum(1 for r in results if r["status"] in ("DRIFTED", "MISSING"))
    total = len(results)
    print(f"\n{'─'*72}")
    print(f"  {aligned}/{total} ALIGNED   {partial}/{total} PARTIAL   {drifted}/{total} DRIFTED")
    print(f"  C3 Matt Pocock: {sum(r.get('c3_pass', False) for r in results if r['status'] != 'MISSING')}/{total} PASS")

    if args.write:
        report = build_report(results, args.stage)
        out_dir = Path("docs/skill-evals")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{date.today().isoformat()}-alignment-scan.md"
        out_path.write_text(report, encoding="utf-8")
        print(f"\n  Report written → {out_path}")

    sys.exit(0 if partial == 0 and drifted == 0 else 1)


if __name__ == "__main__":
    main()
