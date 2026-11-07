"""Regression sweep: run every test source through the full pipeline and check the results.

    python3 -m lsb.regress                          # all cases, 3 at a time, into runs/regress-<timestamp>/
    python3 -m lsb.regress --only civics,kenya-water
    python3 -m lsb.regress --check runs/regress-<timestamp>      # re-check saved runs, no model calls
    python3 -m lsb.regress --check runs/regress-new --baseline runs/regress-old
    python3 -m lsb.regress --backend muse                     # extra flags pass through to lsb.run

The cases and their expectations are in tests/regression/cases.json. Each case
names a source file, and states what a good result must show: the run passes,
the number of units stays within a limit, the planted traps (forbidden terms) don't
appear anywhere in the final sequence, terms that must survive do appear, and the
teacher cards pass G21. These are properties, not a golden answer, because two
good decompositions of the same chapter can differ.

Results go to <root>/report.md and report.json. Exit status: 0 every expectation
met, 1 at least one failed or a run is missing, 2 bad arguments.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "regression" / "cases.json"
RUNS = ROOT / "runs"


def load_cases(path: Path = CASES_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def _strings(node: Any):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v)


def _term_hits(texts: list[str], term: str) -> int:
    left = r"(?<![A-Za-z0-9_])" if re.match(r"\w", term) else ""
    right = r"(?![A-Za-z0-9_])" if re.search(r"\w$", term) else ""
    pat = re.compile(left + re.escape(term) + right, re.I)
    return sum(len(pat.findall(t)) for t in texts)


def evaluate(case: dict, run_dir: Path) -> dict:
    """Check one saved run against its case's expectations."""
    out: dict = {"name": case["name"], "run": str(run_dir), "checks": [], "stats": {}}

    def check(what: str, ok: bool, detail: str = "") -> None:
        out["checks"].append({"check": what, "ok": bool(ok), "detail": detail})

    try:
        summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        check("run exists", False, str(e))
        out["ok"] = False
        return out
    seq_path = run_dir / "sequence.json"
    sequence = json.loads(seq_path.read_text(encoding="utf-8")) if seq_path.exists() else {}
    expect = case.get("expect", {})
    units = [u for u in sequence.get("mls_units", []) if isinstance(u, dict)]
    texts = list(_strings(sequence))

    usage = summary.get("usage") or []
    stages = summary.get("optimisation") or {}
    out["stats"] = {
        "status": summary.get("status"),
        "attempts": summary.get("attempts"),
        "calls": len(usage),
        "tokens_in": sum(u.get("input", 0) + u.get("cache_read", 0) + u.get("cache_write", 0) for u in usage),
        "tokens_out": sum(u.get("output", 0) for u in usage),
        "units": len(units),
        "stages": {k: {s: sum(1 for u in (log or {}).get("units", {}).values() if u.get("status") == s)
                       for s in ("applied", "abstained", "reverted", "edit_rejected")}
                   for k, log in stages.items()},
        "cards_applied": sorted({c for log in stages.values() for u in (log or {}).get("units", {}).values()
                                 if u.get("status") == "applied" for c in u.get("cards") or []}),
        "source_flags": len(summary.get("source_flags") or []),
    }

    check("status", summary.get("status") == expect.get("status", "pass"),
          f"got {summary.get('status')!r}, expected {expect.get('status', 'pass')!r}")
    if "max_units" in expect:
        check("unit count", 1 <= len(units) <= expect["max_units"], f"{len(units)} units, limit {expect['max_units']}")
    for term in expect.get("forbidden", []):
        hits = _term_hits(texts, term)
        check(f"absent: {term}", hits == 0, f"{hits} occurrence(s)" if hits else "")
    for term in expect.get("required", []):
        hits = _term_hits(texts, term)
        check(f"present: {term}", hits > 0, "" if hits else "not found")
    if expect.get("cards_g21", "pass") == "pass" and summary.get("status") == "pass":
        check("cards G21", summary.get("cards_g21") == "pass", str(summary.get("cards_g21")))
    if "min_source_flags" in expect:
        n = len(summary.get("source_flags") or [])
        check("source flags", n >= expect["min_source_flags"], f"{n} flagged, expected at least {expect['min_source_flags']}")
    if "stage_may_not_apply" in expect:
        for key in expect["stage_may_not_apply"]:
            applied = out["stats"]["stages"].get(key, {}).get("applied", 0)
            check(f"{key} abstains", applied == 0, f"{applied} unit(s) applied")
    out["ok"] = all(c["ok"] for c in out["checks"])
    return out


def run_case(case: dict, root: Path, extra: list[str], runner=None) -> Path:
    run_dir = root / case["name"]
    cmd = [sys.executable, "-m", "lsb.run", str(ROOT / case["source"]), "--ref", case["ref"], "--out", str(run_dir)]
    if case.get("grade_band"):
        cmd += ["--grade-band", case["grade_band"]]
    cmd += extra
    root.mkdir(parents=True, exist_ok=True)
    with open(root / f"{case['name']}.log", "w", encoding="utf-8") as log:
        (runner or subprocess.run)(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    return run_dir


def report_markdown(results: list[dict], baseline: dict[str, dict] | None = None) -> str:
    lines = ["# Regression report", "", "| Case | Result | Status | Units | Calls | Tokens in/out | Cards applied | Failed checks |",
             "|---|---|---|---|---|---|---|---|"]
    for r in results:
        st = r["stats"]
        failed = "; ".join(f"{c['check']} ({c['detail']})" if c["detail"] else c["check"]
                           for c in r["checks"] if not c["ok"]) or "—"
        tok = f"{st.get('tokens_in', 0):,} / {st.get('tokens_out', 0):,}"
        if baseline and r["name"] in baseline:
            b = baseline[r["name"]]["stats"]
            if "tokens_in" in b:
                tok += f" (was {b['tokens_in']:,} / {b['tokens_out']:,}, {b.get('status')})"
        lines.append(f"| {r['name']} | {'PASS' if r['ok'] else 'FAIL'} | {st.get('status')} | {st.get('units')} | "
                     f"{st.get('calls')} | {tok} | {', '.join(st.get('cards_applied') or []) or '—'} | {failed} |")
    total_in = sum(r["stats"].get("tokens_in", 0) for r in results)
    total_out = sum(r["stats"].get("tokens_out", 0) for r in results)
    lines += ["", f"{sum(r['ok'] for r in results)} of {len(results)} cases met every expectation. "
                  f"Total tokens: {total_in:,} in / {total_out:,} out."]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m lsb.regress", description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", help="comma-separated case names")
    ap.add_argument("--parallel", type=int, default=3, help="runs at a time (default 3)")
    ap.add_argument("--out", type=Path, help="root directory for the runs (default runs/regress-<timestamp>)")
    ap.add_argument("--check", type=Path, metavar="ROOT", help="only evaluate runs already saved under ROOT")
    ap.add_argument("--baseline", type=Path, metavar="ROOT", help="an earlier sweep to compare costs and statuses with")
    ap.add_argument("--cases", type=Path, default=CASES_PATH)
    args, extra = ap.parse_known_args(argv)

    cases = load_cases(args.cases)
    if args.only:
        wanted = set(args.only.split(","))
        unknown = wanted - {c["name"] for c in cases}
        if unknown:
            print(f"unknown case(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2
        cases = [c for c in cases if c["name"] in wanted]

    root = args.check or args.out or RUNS / dt.datetime.now().strftime("regress-%Y%m%d-%H%M%S")
    if not args.check:
        print(f"running {len(cases)} case(s), {args.parallel} at a time, into {root}")
        with cf.ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
            for done in cf.as_completed([pool.submit(run_case, c, root, extra) for c in cases]):
                print(f"  finished {done.result().name}")

    results = [evaluate(c, root / c["name"]) for c in cases]
    baseline = None
    if args.baseline and (args.baseline / "report.json").exists():
        baseline = {r["name"]: r for r in json.loads((args.baseline / "report.json").read_text(encoding="utf-8"))}
    report = report_markdown(results, baseline)
    root.mkdir(parents=True, exist_ok=True)
    (root / "report.md").write_text(report, encoding="utf-8")
    (root / "report.json").write_text(json.dumps(results, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(report)
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
