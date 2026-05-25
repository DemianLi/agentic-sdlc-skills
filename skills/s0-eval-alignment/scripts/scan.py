#!/usr/bin/env python3
"""
s0-eval-alignment scanner — batch alignment check for all s1-s7 skills.

Usage:
  python3 skills/s0-eval-alignment/scripts/scan.py
  python3 skills/s0-eval-alignment/scripts/scan.py --stage s4
  python3 skills/s0-eval-alignment/scripts/scan.py --write

Exits 0 if all scanned skills are ALIGNED; exits 1 if any PARTIAL or DRIFTED.

Eval cases must be kept in sync with:
  skills/s0-eval-alignment/tests/eval_cases.json
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Skill → QA.md step mapping
# ---------------------------------------------------------------------------
STEPS: List[Tuple[str, str]] = [
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
# ParanoidJudge — structural intent verification (replaces Q keyword counting)
# ---------------------------------------------------------------------------

def paranoid_judge(content: str) -> Dict:
    """
    Replaces Q keyword counting with structural intent verification.
    Checks substantive workflow content and completion discipline —
    properties that require deliberate authorship, not keyword stuffing.

    J1: <what-to-do> must contain ≥3 step headers, checklist items, or numbered items.
    J2: Completion Report must define ≥2 distinct status types.

    Returns {"verdict": "ALIGNED"|"PARTIAL"|"DRIFTED", "issues": [...]}
    """
    issues = []

    # J1: <what-to-do> block must have substantive workflow content
    wt_match = re.search(r'<what-to-do>(.*?)</what-to-do>', content, re.DOTALL)
    if not wt_match:
        issues.append("J1: <what-to-do> block missing")
    else:
        wt = wt_match.group(1)
        step_headers  = len(re.findall(r'###\s+Step\s+\d', wt, re.IGNORECASE))
        checklist_items = len(re.findall(r'- \[[ x]\]', wt))
        numbered_items  = len(re.findall(r'^\d+\.\s', wt, re.MULTILINE))
        total = step_headers + checklist_items + numbered_items
        if total < 3:
            issues.append(f"J1: <what-to-do> has {total} step/checklist item(s) (need ≥3)")

    # J2: Completion Report must enumerate ≥2 distinct status types
    statuses = set(re.findall(
        r'\*\*(DONE|BLOCKED|DONE_WITH_CONCERNS|NEEDS_CONTEXT|PARTIAL)\*\*', content
    ))
    if len(statuses) < 2:
        issues.append(f"J2: Completion Report has {len(statuses)} status type(s) (need ≥2)")

    j1_fail = any("J1" in i for i in issues)
    j2_fail = any("J2" in i for i in issues)

    if j1_fail:
        verdict = "DRIFTED"
    elif j2_fail:
        verdict = "PARTIAL"
    else:
        verdict = "ALIGNED"

    return {"verdict": verdict, "issues": issues}


def verify_test_coverage(skill: str, base: Path) -> bool:
    """
    Returns True if tests/fixtures/<skill>/cases.json exists and has ≥1 case.
    Aligns with Rubric C6 (P5 Auditable) which checks the same data source.
    """
    fixture = base.parent / "tests" / "fixtures" / skill / "cases.json"
    if not fixture.exists():
        return False
    try:
        cases = json.loads(fixture.read_text(encoding="utf-8"))
        return isinstance(cases, list) and len(cases) >= 1
    except Exception:
        return False


# ---------------------------------------------------------------------------

def scan_skill(skill: str, step: str, base: Path) -> Dict:
    path = base / skill / "SKILL.md"
    result: Dict = {"skill": skill, "step": step, "path": str(path)}

    if not path.exists():
        result["status"] = "MISSING"
        return result

    content = path.read_text(encoding="utf-8")

    # Judge — structural semantic check
    judge = paranoid_judge(content)
    result["judge"]        = judge["verdict"]
    result["judge_issues"] = judge["issues"]

    # Tests — P5 Auditable: tests/fixtures/<skill>/cases.json (same source as Rubric C6)
    result["has_tests"] = verify_test_coverage(skill, base)

    # C1 — HARD-GATE + gate phrase (match opening tag only, not closing or inline text)
    result["c1_gate"] = bool(re.search(r'<HARD-GATE>', content))
    if skill in BOUNDARY_SKILLS:
        result["c1_approval"] = "Awaiting your approval" in content
    elif skill in TERMINAL_SKILLS:
        result["c1_approval"] = "report DONE" in content
    else:
        result["c1_approval"] = "proceed immediately to" in content

    # C2 — artifact chain
    result["c2_reads"]  = "Reads"  in content
    result["c2_writes"] = "Writes" in content

    # C3 — description must NOT summarise workflow
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

    # P4 — <what-to-do> line budget (informational; does not affect verdict)
    wt_match = re.search(r'<what-to-do>(.*?)</what-to-do>', content, re.DOTALL)
    wt_lines = len(wt_match.group(1).splitlines()) if wt_match else 0
    result["p4_lines"] = wt_lines
    result["p4_pass"] = wt_lines <= 50

    # Overall verdict
    all_c1 = result["c1_gate"] and result["c1_approval"]
    all_c2 = result["c2_reads"] and result["c2_writes"]
    all_structural = all_c1 and all_c2 and result["c3_pass"] and result["c4_pass"]

    if all_structural and judge["verdict"] == "ALIGNED" and result["has_tests"]:
        result["status"] = "ALIGNED"
    elif not all_structural or judge["verdict"] == "DRIFTED":
        result["status"] = "DRIFTED"
    else:
        result["status"] = "PARTIAL"

    return result


def sym(ok: bool) -> str:
    return "✅" if ok else "❌"


def p_property_table(r: Dict) -> str:
    """
    Derives P1-P5 status from scan result dict.
    Produces a mini markdown table for diffing against Rubric reports.
    scan.py cannot verify all Rubric sub-criteria — coverage gaps are marked (partial).
    """
    judge_issues = r.get("judge_issues", [])
    j1_fail = any("J1" in i for i in judge_issues)
    j2_fail = any("J2" in i for i in judge_issues)

    # P1: description quality (c3). Anti-collision prose not checked by scan.py.
    p1 = "✅" if r.get("c3_pass") else "❌"
    p1_note = "description format only; prose boundary not checked"

    # P2: GATE + Reads/Writes chain + step structure (J1) + red flag (c4)
    p2_checks = [r.get("c1_gate", False), r.get("c2_reads", False) and r.get("c2_writes", False), not j1_fail, r.get("c4_pass", True)]
    p2 = "✅" if all(p2_checks) else "❌"
    p2_note = "GATE + chain + J1 steps + red flag"

    # P3: handoff phrase (c1_approval) + J2 completion statuses
    p3 = "✅" if r.get("c1_approval", False) and not j2_fail else "❌"
    p3_note = "handoff phrase + J2 completion statuses"

    # P4: line budget (informational)
    p4 = "✅" if r.get("p4_pass", False) else "⚠️"
    p4_note = f"{r.get('p4_lines', '?')}L (threshold 50; informational)"

    # P5: fixture file exists with ≥1 case
    p5 = "✅" if r.get("has_tests", False) else "❌"
    p5_note = "tests/fixtures/<skill>/cases.json ≥1 case"

    rows = [
        "| P 屬性 | scan.py 判定 | 依據 |",
        "|--------|-------------|------|",
        f"| P1 Scopeable | {p1} | {p1_note} |",
        f"| P2 Executable | {p2} | {p2_note} |",
        f"| P3 Bounded | {p3} | {p3_note} |",
        f"| P4 Efficient | {p4} | {p4_note} |",
        f"| P5 Auditable | {p5} | {p5_note} |",
    ]
    return "\n".join(rows)


def judge_sym(verdict: str) -> str:
    return {"ALIGNED": "✅", "PARTIAL": "⚠️ WEAK", "DRIFTED": "❌ DRIFTED"}.get(verdict, verdict)


def overall_sym(status: str) -> str:
    return {"ALIGNED": "✅ READY", "PARTIAL": "⚠️ NEAR-READY",
            "DRIFTED": "❌ DRAFT", "MISSING": "❌ MISSING"}.get(status, status)


def build_report(results: List[Dict]) -> str:
    today = date.today().isoformat()
    non_missing = [r for r in results if r["status"] != "MISSING"]

    j_aligned = sum(1 for r in non_missing if r.get("judge") == "ALIGNED")
    j_partial  = sum(1 for r in non_missing if r.get("judge") == "PARTIAL")
    j_drifted  = sum(1 for r in non_missing if r.get("judge") == "DRIFTED")

    lines = [
        "# Alignment Scan Report",
        f"**掃描範圍**: `skills/s1-*` 至 `skills/s7-*`（{len(results)} 個 skill）",
        f"**Date**: {today}",
        f"**Evaluator**: s0-eval-alignment",
        f"**基線**: `skills/s0-eval-alignment/references/skill-design-intent.md`",
        "",
        "---",
        "",
        "## 總覽表",
        "",
        "| Skill | Step | Judge | Tests | P2/P3 GATE | P3 Phrase | P2 Chain | P1 Description | P2 RedFlag | P4 行數 | 整體 |",
        "|-------|------|-------|-------|-----------|-----------|----------|----------------|------------|---------|------|",
    ]

    aligned = partial = drifted = missing = 0
    partials: List[Dict] = []
    drifteds: List[Dict] = []

    for r in results:
        if r["status"] == "MISSING":
            lines.append(f"| {r['skill']} | {r['step']} | — | — | — | — | — | — | — | — | ❌ MISSING |")
            missing += 1
            continue

        c4_cell = sym(r["c4_pass"]) if r["c4_required"] else "—"
        p4_cell = f"{'✅' if r['p4_pass'] else '⚠️'} {r['p4_lines']}L"
        row = (
            f"| {r['skill']} | {r['step']} | {judge_sym(r['judge'])} "
            f"| {sym(r['has_tests'])} "
            f"| {sym(r['c1_gate'])} | {sym(r['c1_approval'])} "
            f"| {sym(r['c2_reads'] and r['c2_writes'])} "
            f"| {'✅ PASS' if r['c3_pass'] else '❌ FAIL'} "
            f"| {c4_cell} | {p4_cell} | {overall_sym(r['status'])} |"
        )
        lines.append(row)

        if r["status"] == "ALIGNED":   aligned += 1
        elif r["status"] == "PARTIAL": partial += 1; partials.append(r)
        elif r["status"] == "DRIFTED": drifted += 1; drifteds.append(r)

    lines += [
        "",
        f"**總計：{aligned}/{len(results)} ✅ READY，"
        f"{partial}/{len(results)} ⚠️ NEAR-READY，"
        f"{drifted}/{len(results)} ❌ DRAFT**",
        "",
        "---",
        "",
        "## 強制執行機制掃描（Judge + P 屬性檢查）",
        "",
        "| 檢查 | P 屬性 | 結果 |",
        "|------|--------|------|",
        f"| Judge J1 <what-to-do> 步驟結構 | P2 Executable | ✅ {j_aligned} / ⚠️ {j_partial} / ❌ {j_drifted} |",
        f"| Judge J2 Completion Report 狀態 | P3 Bounded | ✅ {j_aligned} / ⚠️ {j_partial} / ❌ {j_drifted} |",
        f"| tests/fixtures/<skill>/cases.json ≥1 case | P5 Auditable | {sum(r.get('has_tests', False) for r in non_missing)}/{len(results)} |",
        f"| HARD-GATE 存在 | P2 Executable | {sum(r.get('c1_gate', False) for r in non_missing)}/{len(results)} |",
        f"| gate phrase (boundary: 'Awaiting…' / intra: 'proceed immediately to') | P3 Bounded | {sum(r.get('c1_approval', False) for r in non_missing)}/{len(results)} |",
        f"| Reads + Writes 聲明 | P2 Executable | {sum(r.get('c2_reads', False) and r.get('c2_writes', False) for r in non_missing)}/{len(results)} |",
        f"| Description 不含流程描述詞 | P1 Scopeable | {sum(r.get('c3_pass', False) for r in non_missing)}/{len(results)} |",
        f"| 紅旗表（{len(C4_SKILLS)} 個高風險 skill）| P2 Executable | {sum(r.get('c4_pass', False) for r in non_missing if r.get('c4_required', False))}/{len(C4_SKILLS)} |",
        f"| <what-to-do> ≤ 50 行（資訊欄）| P4 Efficient | {sum(r.get('p4_pass', False) for r in non_missing)}/{len(non_missing)} |",
    ]

    if partials or drifteds:
        lines += ["", "---", "", "## 需關注清單"]
        for r in drifteds + partials:
            tag = "❌ DRAFT" if r["status"] == "DRIFTED" else "⚠️ NEAR-READY"
            issues = []
            for ji in r.get("judge_issues", []):
                issues.append(f"Judge: {ji}")
            if not r["has_tests"]:
                issues.append("P5: tests/fixtures/<skill>/cases.json 不存在或無 case")
            if not r["c1_gate"]:
                issues.append("C1: 缺 HARD-GATE")
            if not r["c1_approval"]:
                if r["skill"] in BOUNDARY_SKILLS:
                    phrase = '"Awaiting your approval"'
                elif r["skill"] in TERMINAL_SKILLS:
                    phrase = '"report DONE"'
                else:
                    phrase = '"proceed immediately to"'
                issues.append(f"C1: 缺 {phrase}")
            if not (r["c2_reads"] and r["c2_writes"]):
                issues.append("C2: 缺 Reads/Writes 聲明")
            if not r["c3_pass"]:
                issues.append("C3: description 含流程描述詞（Matt Pocock 違規）")
            if r.get("c4_required") and not r.get("c4_pass"):
                issues.append("C4: 缺紅旗表")
            lines.append(f"\n### {r['skill']} — {tag}\n")
            lines.append(p_property_table(r))
            lines.append("")
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
    parser.add_argument(
        "--quiet", action="store_true",
        help="只在有 DRIFTED/PARTIAL 時輸出摘要（供 git hook 使用）"
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

    aligned = sum(1 for r in results if r["status"] == "ALIGNED")
    partial = sum(1 for r in results if r["status"] == "PARTIAL")
    drifted = sum(1 for r in results if r["status"] in ("DRIFTED", "MISSING"))

    # Console summary
    if not args.quiet:
        print(f"\n{'Skill':<25} {'Step':<5} {'Judge':<10} {'Tests':<6} {'C1':<4} {'C2':<4} {'C3':<9} Overall")
        print("-" * 80)
        for r in results:
            if r["status"] == "MISSING":
                print(f"{'  ' + r['skill']:<25} {r['step']:<5} {'—':<10} {'—':<6} {'—':<4} {'—':<4} {'—':<9} ❌ MISSING")
                continue
            c3 = "✅ PASS" if r["c3_pass"] else "❌ FAIL"
            c1 = "✅" if (r["c1_gate"] and r["c1_approval"]) else "❌"
            c2 = "✅" if (r["c2_reads"] and r["c2_writes"]) else "❌"
            j  = {"ALIGNED": "✅", "PARTIAL": "⚠️ PAR", "DRIFTED": "❌ DRF"}.get(r["judge"], r["judge"])
            t  = "✅" if r["has_tests"] else "❌"
            print(f"  {r['skill']:<23} {r['step']:<5} {j:<10} {t:<6} {c1:<4} {c2:<4} {c3:<9} {overall_sym(r['status'])}")
        print(f"\n{'─'*80}")

    total = len(results)
    if not args.quiet or partial > 0 or drifted > 0:
        print(f"  {aligned}/{total} ALIGNED   {partial}/{total} PARTIAL   {drifted}/{total} DRIFTED")

    if args.write:
        report = build_report(results)
        out_dir = Path("docs/skill-evals")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{date.today().isoformat()}-alignment-scan.md"
        out_path.write_text(report, encoding="utf-8")
        print(f"\n  Report written → {out_path}")

    sys.exit(0 if partial == 0 and drifted == 0 else 1)


if __name__ == "__main__":
    main()
