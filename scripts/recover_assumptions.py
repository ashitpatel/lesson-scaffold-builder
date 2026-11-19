"""One-off: give runs from before final_assumptions.json the file, so they re-render.

    python3 scripts/recover_assumptions.py            # every run a walkthrough names
    python3 scripts/recover_assumptions.py --dry-run
    python3 scripts/recover_assumptions.py --runs DIR

lsb.run now saves the environment assumptions it printed on the cards
(final_assumptions.json). Older runs have only the best decompose attempt's,
which repair, relocalisation and translation may since have changed, so
`python3 -m lsb.render runs/<run>` can print the wrong BEFORE YOU START lines.

For each run a walkthrough's `Run` line names, this replays what the run did
from its own saved files: the accepted repair output (else the best decompose
attempt), then the approved locale replacements, then the translation. It
writes final_assumptions.json only when cards rendered with the result are
byte-identical to the walkthrough's committed copy, and reports every run it
could not match. Runs that already have the file, or whose cards already match,
are left alone. Run it with the renderer the walkthroughs were rendered with.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lsb import locale as loc  # noqa: E402
from lsb import render  # noqa: E402

RUN_LINE = re.compile(r"^> Run `runs/([^`]+)`", re.M)
BLOCK = re.compile(r"^```\n(.*?)^```$", re.M | re.S)


def committed_cards(walkthrough: Path) -> tuple[str, str] | None:
    """(run name, cards.txt text) from a walkthrough's final*.md, or None."""
    text = walkthrough.read_text(encoding="utf-8")
    run, block = RUN_LINE.search(text), BLOCK.search(text)
    return (run.group(1), block.group(1)) if run and block else None


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidates(run_dir: Path) -> list[list]:
    """Possible final assumptions, most likely first."""
    summary = _load(run_dir / "summary.json")
    bases = []
    rounds = ((summary.get("repair") or {}).get("rounds") or [])
    for rnd in sorted({r.get("round") for r in rounds if isinstance(r, dict) and r.get("round")}, reverse=True):
        for name in (f"repair{rnd}-retry.json", f"repair{rnd}.json"):
            if (run_dir / name).exists():
                bases.append(_load(run_dir / name).get("environment_assumptions") or [])
    best = summary.get("best_attempt")
    if isinstance(best, int) and (run_dir / f"{best:02d}-decompose.json").exists():
        bases.append(_load(run_dir / f"{best:02d}-decompose.json").get("environment_assumptions") or [])

    locale = summary.get("locale") or {}
    relocalised = (locale.get("mode") == "relocalize" and locale.get("applied") and not locale.get("reverted")
                   and (run_dir / "locale-log.json").exists() and (run_dir / "locale-decisions.json").exists())
    translation = (summary.get("translation") or {}).get("applied") and (run_dir / "translation.json").exists()

    out = []
    for assumptions in bases:
        if relocalised:
            log = _load(run_dir / "locale-log.json")
            log = log.get("locale_log", log) if isinstance(log, dict) else log
            decisions = {int(k): v for k, v in _load(run_dir / "locale-decisions.json").items()}
            _, new, _ = loc.apply_locale({"mls_units": []}, log, decisions, assumptions)
            assumptions = new if new is not None else assumptions
        if translation:
            assumptions = _load(run_dir / "translation.json").get("assumptions") or assumptions
        if assumptions not in out:
            out.append(assumptions)
    return out


def recover(run_dir: Path, want: str, write: bool) -> str:
    if (run_dir / render.FINAL_ASSUMPTIONS).exists():
        return "has final_assumptions.json"
    if render.render_text(render.load_run(run_dir)) == want:
        return "already matches"
    for assumptions in candidates(run_dir):
        (run_dir / render.FINAL_ASSUMPTIONS).write_text(
            json.dumps(assumptions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if render.render_text(render.load_run(run_dir)) == want:
            if not write:
                (run_dir / render.FINAL_ASSUMPTIONS).unlink()
            return "RECOVERED" + ("" if write else " (dry run, not written)")
        (run_dir / render.FINAL_ASSUMPTIONS).unlink()
    return "NO MATCH; left as it was"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--runs", type=Path, default=ROOT / "runs", help="the runs directory (default: ./runs)")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = ap.parse_args(argv)
    failed = 0
    for walkthrough in sorted((ROOT / "docs" / "walkthroughs").glob("*/final*.md")):
        found = committed_cards(walkthrough)
        if found is None:
            continue
        name, want = found
        run_dir = args.runs / name
        if not (run_dir / "summary.json").exists():
            print(f"{name}: no saved run at {run_dir}")
            continue
        status = recover(run_dir, want, not args.dry_run)
        failed += status.startswith("NO MATCH")
        print(f"{name}: {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
