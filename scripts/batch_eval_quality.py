#!/usr/bin/env python3
"""
批次評估所有 SKILL.md 的 6 項生產級品質標準。
用法: python3 scripts/batch_eval_quality.py
"""

import json
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
OUT_DIR = ROOT / "docs" / "skill-evals"
EVAL_CASES_PATH = ROOT / "skills/s0-eval-alignment/tests/eval_cases.json"

PASS = "✅"
PARTIAL = "⚠️"
FAIL = "❌"


# ─── 評分函式 ──────────────────────────────────────────────────────────────

def score_c1_anti_collision(text: str) -> tuple[str, str]:
    """衝突防禦：正文是否點名 ≥1 相鄰 skill 並說明邊界？"""
    # 找 skill 引用（/sN-name 或 skill-creator 等）
    skill_refs = re.findall(r'`?(?:/s\d[\w-]+|skill-creator|s0-\w+|s\d-\w+)`?', text)
    # 找邊界說明用語
    boundary_words = re.search(
        r'(Distinct from|不同於|差異在於|而非|NOT for|vs\.?|相鄰|邊界|boundary|不同的是)',
        text, re.IGNORECASE
    )
    # 負面觸發表格也算（表格裡比較兩個 skill）
    neg_table = re.search(r'\|\s*情境.*\|\s*正確技能', text)

    if skill_refs and (boundary_words or neg_table):
        return PASS, f"引用 skill: {', '.join(set(skill_refs[:3]))}；有邊界說明"
    elif skill_refs:
        return PARTIAL, f"引用 skill: {', '.join(set(skill_refs[:3]))}，但未明確說明差異"
    else:
        return FAIL, "正文未提及任何相鄰 skill"


def score_c2_negative_triggers(text: str) -> tuple[str, str]:
    """雙向阻斷：是否有『絕對不要』區塊含 ≥2 個具體反例？"""
    # 找負面觸發標題
    neg_header = re.search(
        r'###.*?(絕對不要|Never trigger|Do NOT trigger|不要觸發|絕不|NEVER)',
        text, re.IGNORECASE
    )
    if not neg_header:
        return FAIL, "無任何負面觸發區塊（缺少『絕對不要』等 header）"

    # 從標題往後找表格行數
    after = text[neg_header.start():]
    # 找表格 row（| ... | ... | 模式，排除 header 和分隔線）
    table_rows = re.findall(r'^\|(?!\s*[-:]+\s*\|)(?!\s*情境).*\|', after, re.MULTILINE)
    row_count = len(table_rows)

    if row_count >= 2:
        return PASS, f"負面觸發區塊含 {row_count} 個反例"
    elif row_count == 1:
        return PARTIAL, f"負面觸發區塊只有 {row_count} 個反例（需 ≥2）"
    else:
        return PARTIAL, "有負面觸發標題但無具體反例表格"


def score_c3_input_linting(text: str) -> tuple[str, str]:
    """輸入清洗：輸入是否明列，且失敗情境都有定義行為？"""
    # 找 Step 0 / Input Validation
    step0 = re.search(
        r'###\s*Step\s*0|輸入驗證|Input Validation|Input Linting',
        text, re.IGNORECASE
    )
    # 找 BLOCKED / PARTIAL / 繼續 等行為定義
    behavior_defs = re.findall(r'BLOCKED|NEEDS_CONTEXT|PARTIAL.*—|→\s*(繼續|回報|提問)', text)
    # 找失敗情境表格
    failure_table = re.search(r'\|\s*失敗情境', text)

    if step0 and (failure_table or len(behavior_defs) >= 2):
        return PASS, f"有 Step 0 輸入驗證，含 {len(behavior_defs)} 個行為定義"
    elif step0 or failure_table:
        return PARTIAL, "有輸入驗證概念但失敗情境覆蓋不完整"
    elif behavior_defs:
        return PARTIAL, f"有 {len(behavior_defs)} 個 BLOCKED/行為定義，但無明確 Step 0"
    else:
        return FAIL, "無輸入定義，無失敗情境處理"


def score_c4_progressive_disclosure(text: str, skill_dir: Path) -> tuple[str, str]:
    """漸進披露：無單一 inline 區塊 >50 行；大模板外部化。"""
    lines = text.split('\n')
    total = len(lines)

    # 計算最大連續非空行數
    max_block = 0
    cur = 0
    for line in lines:
        if line.strip():
            cur += 1
            max_block = max(max_block, cur)
        else:
            cur = 0

    # 檢查是否有 references 外部化
    has_ref = bool(re.search(r'references/', text))
    ref_dir = skill_dir / "references"
    ref_exists = ref_dir.exists() and any(ref_dir.iterdir())

    if total <= 105 and max_block <= 50:
        note = "有外部化引用" if has_ref else "無外部化（但檔案夠小）"
        return PASS, f"總行數 {total}，最大連續區塊 {max_block} 行；{note}"
    elif max_block <= 100 and total <= 150:
        return PARTIAL, f"總行數 {total}，最大連續區塊 {max_block} 行（在可接受範圍）"
    else:
        return FAIL, f"總行數 {total}，最大連續區塊 {max_block} 行（超標）"


def score_c5_graceful_degradation(text: str) -> tuple[str, str]:
    """優雅降級：每個可能失敗的步驟是否有 BLOCKED / fallback？"""
    # 找 Completion Report 區塊
    completion = re.search(r'##\s*Completion Report', text, re.IGNORECASE)
    # 找 BLOCKED 和其他狀態
    blocked_count = len(re.findall(r'\bBLOCKED\b', text))
    needs_ctx = len(re.findall(r'\bNEEDS_CONTEXT\b', text))
    concerns = len(re.findall(r'\bDONE_WITH_CONCERNS\b', text))
    total_states = blocked_count + needs_ctx + concerns

    # 找步驟中的 fallback 標記
    step_fallbacks = re.findall(r'(→\s*BLOCKED|失敗.*→|fallback|備援)', text, re.IGNORECASE)

    if completion and total_states >= 3 and step_fallbacks:
        return PASS, f"Completion Report 存在，{total_states} 個失敗狀態，{len(step_fallbacks)} 個步驟 fallback"
    elif completion and total_states >= 2:
        return PARTIAL, f"Completion Report 存在，{total_states} 個狀態，但步驟內 fallback 不足"
    elif total_states >= 1:
        return PARTIAL, f"有 {total_states} 個失敗狀態定義，但無完整 Completion Report"
    else:
        return FAIL, "無 Completion Report，無 BLOCKED 狀態定義"


def score_c6_drift_monitoring(text: str, skill_dir: Path, eval_cases: dict) -> tuple[str, str]:
    """長效維護：對齊 scan.py 實際邏輯——集中式 eval_cases.json 為主，per-skill tests/ 為輔。

    PASS 條件（任一）:
      A. skill 名稱在 eval_cases.json 中，且同時有 golden_path 與 adversarial 條目
      B. skill 目錄下有 tests/ 且含 ≥2 個 fixture 檔案
    PARTIAL:
      - eval_cases.json 有該 skill 但缺其中一個條目
      - 或 tests/ 存在但只有 1 個 fixture
    FAIL:
      - 不在 eval_cases.json，且無 tests/ 目錄
    """
    skill_name = skill_dir.name
    entry = eval_cases.get(skill_name, {})
    has_golden = bool(entry.get("golden_path"))
    has_adversarial = bool(entry.get("adversarial"))

    # 優先：集中式 eval_cases.json
    if has_golden and has_adversarial:
        return PASS, f"eval_cases.json 有 golden_path + adversarial 條目"
    if has_golden or has_adversarial:
        missing = "adversarial" if has_golden else "golden_path"
        return PARTIAL, f"eval_cases.json 缺少 {missing} 條目"

    # 備選：per-skill tests/ 目錄
    tests_dir = skill_dir / "tests"
    if tests_dir.exists():
        count = len(list(tests_dir.iterdir()))
        if count >= 2:
            return PASS, f"tests/ 目錄存在，含 {count} 個 fixture 檔案"
        elif count == 1:
            return PARTIAL, f"tests/ 存在但只有 {count} 個 fixture（需 ≥2）"
        else:
            return PARTIAL, "tests/ 目錄存在但為空"

    return FAIL, f"不在 eval_cases.json，且無 tests/ 目錄"


# ─── 主程式 ────────────────────────────────────────────────────────────────

def eval_skill(skill_path: Path, eval_cases: dict) -> dict:
    text = skill_path.read_text(encoding='utf-8')
    skill_dir = skill_path.parent
    name = skill_dir.name

    c1, e1 = score_c1_anti_collision(text)
    c2, e2 = score_c2_negative_triggers(text)
    c3, e3 = score_c3_input_linting(text)
    c4, e4 = score_c4_progressive_disclosure(text, skill_dir)
    c5, e5 = score_c5_graceful_degradation(text)
    c6, e6 = score_c6_drift_monitoring(text, skill_dir, eval_cases)

    scores = [c1, c2, c3, c4, c5, c6]
    pass_count = scores.count(PASS)
    partial_count = scores.count(PARTIAL)

    return {
        "name": name,
        "path": str(skill_path.relative_to(ROOT)),
        "scores": scores,
        "evidence": [e1, e2, e3, e4, e5, e6],
        "pass": pass_count,
        "partial": partial_count,
        "fail": scores.count(FAIL),
    }


def grade(r: dict) -> str:
    if r["fail"] == 0 and r["partial"] == 0:
        return "EXCELLENT"
    elif r["fail"] == 0:
        return "GOOD"
    elif r["fail"] <= 2:
        return "NEEDS_WORK"
    else:
        return "CRITICAL"


GRADE_ICON = {
    "EXCELLENT": "🟢",
    "GOOD": "🟡",
    "NEEDS_WORK": "🟠",
    "CRITICAL": "🔴",
}

CRITERIA_NAMES = [
    "衝突防禦", "雙向阻斷", "輸入清洗", "漸進披露", "優雅降級", "長效維護"
]


def run():
    skill_paths = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    # 排除 tests/ 目錄下的
    skill_paths = [p for p in skill_paths if "tests" not in str(p)]

    # 載入集中式 eval_cases.json（scan.py 的軌三資料來源）
    eval_cases: dict = {}
    if EVAL_CASES_PATH.exists():
        eval_cases = json.loads(EVAL_CASES_PATH.read_text(encoding='utf-8'))
    else:
        print(f"[WARNING] eval_cases.json 不存在：{EVAL_CASES_PATH}", file=sys.stderr)

    results = [eval_skill(p, eval_cases) for p in skill_paths]

    # ── 終端摘要表 ──
    print(f"\n{'='*80}")
    print(f"  批次品質評估 — {date.today()}  ({len(results)} skills)")
    print(f"{'='*80}")
    print(f"{'Skill':<28} {'C1':>3} {'C2':>3} {'C3':>3} {'C4':>3} {'C5':>3} {'C6':>3}  {'P/P/F':>7}  Grade")
    print(f"{'-'*80}")

    grade_counts = {"EXCELLENT": 0, "GOOD": 0, "NEEDS_WORK": 0, "CRITICAL": 0}
    criterion_fails = [0] * 6
    criterion_partials = [0] * 6

    for r in results:
        g = grade(r)
        grade_counts[g] += 1
        icon = GRADE_ICON[g]
        scores_str = "  ".join(r["scores"])
        ppf = f"{r['pass']}/{r['partial']}/{r['fail']}"
        print(f"{r['name']:<28} {scores_str}  {ppf:>7}  {icon} {g}")
        for i, s in enumerate(r["scores"]):
            if s == FAIL:
                criterion_fails[i] += 1
            elif s == PARTIAL:
                criterion_partials[i] += 1

    # ── 統計摘要 ──
    print(f"\n{'='*80}")
    print(f"  整體統計")
    print(f"{'='*80}")
    total = len(results)
    for g, icon in GRADE_ICON.items():
        n = grade_counts[g]
        bar = "█" * n
        print(f"  {icon} {g:<12} {n:>3} / {total}  {bar}")

    avg_pass = sum(r["pass"] for r in results) / total
    print(f"\n  平均通過數：{avg_pass:.1f} / 6")

    print(f"\n{'─'*80}")
    print(f"  各標準失敗率")
    print(f"{'─'*80}")
    for i, name in enumerate(CRITERIA_NAMES):
        fails = criterion_fails[i]
        parts = criterion_partials[i]
        passes = total - fails - parts
        bar_p = "█" * passes
        bar_w = "░" * parts
        bar_f = "▓" * fails
        print(f"  C{i+1} {name:<8}  ✅{passes:>2}  ⚠️{parts:>2}  ❌{fails:>2}  {bar_p}{bar_w}{bar_f}")

    # ── 寫入報告 ──
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUT_DIR / f"{date.today()}-batch-quality-eval.md"

    lines = [
        f"# 批次品質評估報告",
        f"**日期**: {date.today()}",
        f"**涵蓋**: {total} skills",
        f"",
        f"## 總覽",
        f"",
        f"| Skill | C1衝突防禦 | C2雙向阻斷 | C3輸入清洗 | C4漸進披露 | C5優雅降級 | C6長效維護 | Pass | Grade |",
        f"|-------|-----------|-----------|-----------|-----------|-----------|-----------|------|-------|",
    ]
    for r in results:
        g = grade(r)
        icon = GRADE_ICON[g]
        s = r["scores"]
        lines.append(
            f"| `{r['name']}` | {s[0]} | {s[1]} | {s[2]} | {s[3]} | {s[4]} | {s[5]} | {r['pass']}/6 | {icon} {g} |"
        )

    lines += [
        f"",
        f"## 各標準失敗/待改清單",
        f"",
    ]
    for i, cname in enumerate(CRITERIA_NAMES):
        fails_list = [r["name"] for r in results if r["scores"][i] == FAIL]
        partials_list = [r["name"] for r in results if r["scores"][i] == PARTIAL]
        if fails_list or partials_list:
            lines.append(f"### C{i+1} — {cname}")
            if fails_list:
                lines.append(f"**❌ FAIL ({len(fails_list)})**: {', '.join(f'`{n}`' for n in fails_list)}")
            if partials_list:
                lines.append(f"**⚠️ PARTIAL ({len(partials_list)})**: {', '.join(f'`{n}`' for n in partials_list)}")
            lines.append("")

    lines += [
        f"## 詳細證據",
        f"",
    ]
    for r in results:
        g = grade(r)
        icon = GRADE_ICON[g]
        lines.append(f"### `{r['name']}` — {icon} {grade(r)}")
        lines.append(f"| # | 標準 | 分數 | 證據 |")
        lines.append(f"|---|------|------|------|")
        for i, (s, e) in enumerate(zip(r["scores"], r["evidence"])):
            lines.append(f"| C{i+1} | {CRITERIA_NAMES[i]} | {s} | {e} |")
        lines.append("")

    report_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"\n  報告已寫入：{report_path.relative_to(ROOT)}")
    print(f"{'='*80}\n")

    return results


if __name__ == "__main__":
    run()
