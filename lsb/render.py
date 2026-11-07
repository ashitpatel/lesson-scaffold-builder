"""Render a passed MLS sequence as offline teacher cards, and check them (critic check G21).

    python3 -m lsb.render runs/<run>            # writes cards.txt and cards.html into the run
    python3 -m lsb.render runs/<run> --out DIR

The requirements' last stage is "Highly Scannable Offline Teacher Cards", and
G21 (Output Clarity) asks for a "high-contrast, text-only, dual-column format".
That is layout, so it is done here in code, not by a model: one overview card,
then one card per unit in dependency order. Each unit card has a two-column
WHO / WHAT TO DO step table, the conditions the unit relies on with what to do
if one doesn't hold, and the changes the optimisation stages made, by card.

cards.txt is plain text at most 78 characters wide. cards.html is one
self-contained black-on-white page with no images, scripts, links or external
resources, one card per printed page.

Exit status: 0 cards written and every check passes, 1 a check failed, 2 the run
can't be read.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lsb import dag
from lsb._paths import resource_root

ROOT = resource_root()
FRAMEWORKS = ROOT / "frameworks"
CONFIG_PATH = ROOT / "config" / "taxonomy_mapping.json"

WIDTH = 78
WHO = 22  # left column width in cards.txt
ROLE_NAMES = {"Lead_Educator": "Lead Educator", "Peer_Facilitator": "Peer Facilitator",
              "Community_Volunteer": "Community Volunteer"}
STAGE_NAMES = {"evidence_based": "Evidence-Based", "connected_learning": "Connected Learning", "participatory_budgeting": "Participatory Budgeting"}


@dataclass
class Deck:
    sequence: dict
    source_ref: str = ""
    assumptions: list[dict] = field(default_factory=list)  # environment_assumptions from 05-decompose
    trace: list[dict] = field(default_factory=list)  # final source trace (card ids on changed steps)
    optimisation: dict = field(default_factory=dict)  # summary.json "optimisation"
    disclaimer: str = ""

    def units(self) -> list[dict]:
        units = [u for u in self.sequence.get("mls_units", []) if isinstance(u, dict)]
        try:
            order = dag.topological_order(units)
        except ValueError:
            return units
        by_id = {u.get("mls_id"): u for u in units}
        return [by_id[i] for i in order if i in by_id]


def card_names() -> dict[str, str]:
    """{'CL-02': 'Structural Peer Roles', ...} from the framework card files."""
    names: dict[str, str] = {}
    for path in sorted(FRAMEWORKS.glob("*.md")):
        for m in re.finditer(r"^## ([A-Z]{2}-\d\d) (.+)$", path.read_text(encoding="utf-8"), re.M):
            names[m.group(1)] = m.group(2).strip()
    return names


def load_run(run_dir: Path) -> Deck:
    """A Deck from a saved `lsb.run` output directory."""
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    sequence = json.loads((run_dir / "sequence.json").read_text(encoding="utf-8"))
    best = summary.get("best_attempt")
    decomposed: dict = {}
    if isinstance(best, int) and (run_dir / f"{best:02d}-decompose.json").exists():
        decomposed = json.loads((run_dir / f"{best:02d}-decompose.json").read_text(encoding="utf-8"))
    trace_file = run_dir / "source_trace.json"
    trace = (json.loads(trace_file.read_text(encoding="utf-8")) if trace_file.exists()
             else decomposed.get("source_trace") or [])
    optimisation = summary.get("optimisation") or {}
    if "units" in optimisation:  # runs from before the PB stage logged one stage, unkeyed
        optimisation = {optimisation.get("stage", "connected_learning"): optimisation}
    return build_deck(sequence, decomposed, optimisation, trace, summary.get("source_ref", ""))


def build_deck(sequence: dict, decomposed: dict | None, optimisation: dict | None, trace: list | None,
               source_ref: str = "") -> Deck:
    try:
        disclaimer = json.loads(CONFIG_PATH.read_text(encoding="utf-8")).get("onboarding_disclaimer", "")
    except (OSError, json.JSONDecodeError):
        disclaimer = ""
    return Deck(
        sequence=sequence,
        source_ref=source_ref or "",
        assumptions=[a for a in (decomposed or {}).get("environment_assumptions") or [] if isinstance(a, dict)],
        trace=[e for e in trace or [] if isinstance(e, dict)],
        optimisation=optimisation or {},
        disclaimer=disclaimer,
    )


# ---------------------------------------------------------------- content shared by both formats

def _deps_line(unit: dict) -> str:
    deps = [d for d in unit.get("dependencies") or [] if isinstance(d, str)]
    return "Builds on " + ", ".join(deps) if deps else "Starts fresh (no earlier unit needed)"


def _weeks(unit: dict) -> str:
    w = unit.get("duration_weeks")
    return f"{w} weeks" if isinstance(w, int) else "length not stated"


def _step_cards(deck: Deck, uid: str) -> dict[int, list[str]]:
    """{step: [card ids]} for steps an optimisation stage changed, from the final trace."""
    out: dict[int, list[str]] = {}
    for e in deck.trace:
        if e.get("mls_id") == uid and e.get("card") and isinstance(e.get("step"), int):
            out.setdefault(e["step"], []).append(e["card"])
    return out


def _changes(deck: Deck, uid: str) -> list[tuple[str, str, str]]:
    """[(stage name, card id, summary)] for each change an optimisation stage kept in this unit."""
    out = []
    for key, log in deck.optimisation.items():
        u = (log or {}).get("units", {}).get(uid) or {}
        if u.get("status") != "applied":
            continue
        for c in u.get("changes") or []:
            if isinstance(c, dict):
                out.append((STAGE_NAMES.get(key, key), str(c.get("card", "")), str(c.get("summary", ""))))
    return out


def _assumptions(deck: Deck, uid: str) -> list[tuple[str, str]]:
    return [(str(a.get("assumes", "")), str(a.get("if_not", ""))) for a in deck.assumptions if a.get("mls_id") == uid]


def _overview_rows(deck: Deck) -> list[tuple[str, str]]:
    return [(u.get("mls_id", "?"), f"{u.get('title', '')} ({_weeks(u)}). {_deps_line(u)}.") for u in deck.units()]


def _context(deck: Deck) -> str:
    gc = deck.sequence.get("global_context") or {}
    parts = []
    if gc.get("grade_band"):
        parts.append(f"Grade band: {gc['grade_band']}")
    if gc.get("time_block_minutes"):
        parts.append(f"Period: {gc['time_block_minutes']} minutes")
    return ". ".join(parts) + ("." if parts else "")


# ---------------------------------------------------------------- plain text

def _wrap(text: str, width: int, indent: str = "", hang: str | None = None) -> list[str]:
    return textwrap.wrap(text, width=width, initial_indent=indent,
                         subsequent_indent=indent if hang is None else hang,
                         break_long_words=True, break_on_hyphens=False) or [indent.rstrip()]


def _two_col(left: str, right: str, width: int = WIDTH) -> list[str]:
    lw = _wrap(left, WHO - 2)
    rw = _wrap(right, width - WHO)
    rows = max(len(lw), len(rw))
    lw += [""] * (rows - len(lw))
    rw += [""] * (rows - len(rw))
    return [(lft.ljust(WHO) + rgt).rstrip() for lft, rgt in zip(lw, rw)]


def render_text(deck: Deck, width: int = WIDTH) -> str:
    names = card_names()
    heavy, light = "=" * width, "-" * width
    out: list[str] = [heavy]
    out += _wrap("LESSON SCAFFOLD" + (f": {deck.source_ref}" if deck.source_ref else ""), width)
    out.append(heavy)
    out += _wrap("Goal: " + str(deck.sequence.get("macro_objective", "")), width)
    if _context(deck):
        out += _wrap(_context(deck), width)
    out.append("")
    out += _two_col("UNIT", "WHAT IT IS")
    out.append(light)
    for left, right in _overview_rows(deck):
        out += _two_col(left, right)
    out.append("")
    out += _wrap("Units that build on the same earlier unit, or start fresh, can run at the same time.", width)
    if deck.disclaimer:
        out.append("")
        out += _wrap(deck.disclaimer, width)

    for unit in deck.units():
        uid = str(unit.get("mls_id", "?"))
        out += ["", "", heavy]
        out += _wrap(f"{uid}: {unit.get('title', '')}", width)
        out += _wrap(f"{_weeks(unit)}. {_deps_line(unit)}.", width)
        out.append(heavy)
        out += _wrap("Goal: " + str(unit.get("macro_alignment", "")), width)
        out.append("")
        out += _two_col("WHO", "WHAT TO DO")
        out.append(light)
        changed = _step_cards(deck, uid)
        for t in unit.get("tasks") or []:
            if not isinstance(t, dict):
                continue
            step = t.get("step")
            left = f"{step}. {ROLE_NAMES.get(t.get('role'), str(t.get('role')))}"
            if step in changed:
                left += f" [changed: {', '.join(changed[step])}]"
            out += _two_col(left, str(t.get("action", "")))
            out.append("")
        assumptions = _assumptions(deck, uid)
        if assumptions:
            out.append(light)
            out.append("BEFORE YOU START")
            for assumes, if_not in assumptions:
                out += _wrap("- Needs: " + assumes, width, hang="  ")
                if if_not:
                    out += _wrap("If not: " + if_not, width, "  ")
        changes = _changes(deck, uid)
        if changes:
            out.append(light)
            out.append("CHANGES FROM THE SOURCE")
            for stage, card, summary in changes:
                out += _wrap(f"- {stage}, {card} {names.get(card, '')}: {summary}", width, hang="  ")
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------- HTML

CSS = """
@page { margin: 15mm; }
html, body { background: #fff; color: #000; }
body { font: 12pt/1.45 Georgia, "Times New Roman", serif; margin: 0 auto; max-width: 48rem; padding: 16px; }
.card { border: 2px solid #000; padding: 12px 16px; margin: 0 0 24px; break-after: page; page-break-after: always; }
.card:last-child { break-after: auto; page-break-after: auto; }
h1, h2, h3 { font-family: Arial, Helvetica, sans-serif; margin: 0 0 6px; }
h1 { font-size: 18pt; } h2 { font-size: 15pt; } h3 { font-size: 12pt; margin-top: 12px; }
p { margin: 4px 0; }
table { border-collapse: collapse; width: 100%; margin-top: 8px; }
th, td { border: 1px solid #000; padding: 6px 8px; vertical-align: top; text-align: left; }
th { font-family: Arial, Helvetica, sans-serif; }
td.who { width: 28%; font-weight: bold; }
td.id { width: 1%; white-space: nowrap; font-weight: bold; }
@media (max-width: 600px) {
  body { font-size: 11pt; padding: 8px; }
  .card { padding: 10px; }
  h1 { font-size: 15pt; } h2 { font-size: 13pt; }
  th, td { padding: 4px 6px; }
}
ul { margin: 4px 0; padding-left: 20px; }
""".strip()


def _e(s: Any) -> str:
    return html.escape(str(s), quote=True)


def _table(head: tuple[str, str], rows: list[tuple[str, str]], left: str = "who") -> str:
    body = "".join(f'<tr><td class="{left}">{_e(a)}</td><td>{_e(b)}</td></tr>' for a, b in rows)
    return f"<table><thead><tr><th>{_e(head[0])}</th><th>{_e(head[1])}</th></tr></thead><tbody>{body}</tbody></table>"


def render_html(deck: Deck) -> str:
    names = card_names()
    title = "Lesson scaffold" + (f": {deck.source_ref}" if deck.source_ref else "")
    parts = [f'<section class="card"><h1>{_e(title)}</h1>',
             f'<p><strong>Goal:</strong> {_e(deck.sequence.get("macro_objective", ""))}</p>']
    if _context(deck):
        parts.append(f"<p>{_e(_context(deck))}</p>")
    parts.append(_table(("Unit", "What it is"), _overview_rows(deck), left="id"))
    parts.append("<p>Units that build on the same earlier unit, or start fresh, can run at the same time.</p>")
    if deck.disclaimer:
        parts.append(f"<p>{_e(deck.disclaimer)}</p>")
    parts.append("</section>")

    for unit in deck.units():
        uid = str(unit.get("mls_id", "?"))
        changed = _step_cards(deck, uid)
        rows = []
        for t in unit.get("tasks") or []:
            if isinstance(t, dict):
                step = t.get("step")
                left = f"{step}. {ROLE_NAMES.get(t.get('role'), str(t.get('role')))}"
                if step in changed:
                    left += f" [changed: {', '.join(changed[step])}]"
                rows.append((left, str(t.get("action", ""))))
        parts.append(f'<section class="card" id="{_e(uid)}">'
                     f"<h2>{_e(uid)}: {_e(unit.get('title', ''))}</h2>"
                     f"<p>{_e(_weeks(unit))}. {_e(_deps_line(unit))}.</p>"
                     f"<p><strong>Goal:</strong> {_e(unit.get('macro_alignment', ''))}</p>"
                     + _table(("Who", "What to do"), rows))
        assumptions = _assumptions(deck, uid)
        if assumptions:
            items = "".join(f"<li>Needs: {_e(a)}" + (f"<br>If not: {_e(b)}" if b else "") + "</li>"
                            for a, b in assumptions)
            parts.append(f"<h3>Before you start</h3><ul>{items}</ul>")
        changes = _changes(deck, uid)
        if changes:
            items = "".join(f"<li>{_e(stage)}, {_e(card)} {_e(names.get(card, ''))}: {_e(summary)}</li>"
                            for stage, card, summary in changes)
            parts.append(f"<h3>Changes from the source</h3><ul>{items}</ul>")
        parts.append("</section>")

    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>{_e(title)}</title><style>\n{CSS}\n</style></head><body>\n"
            + "\n".join(parts) + "\n</body></html>\n")


# ---------------------------------------------------------------- the G21 check

FORBIDDEN_HTML = re.compile(r"<\s*(img|script|link|iframe|object|embed|video|audio|svg|canvas)\b|url\(|https?://|@import",
                            re.I)
COLOUR = re.compile(r"#[0-9a-f]{3,8}\b|\brgba?\(|\bhsla?\(", re.I)


def _norm(s: str) -> str:
    return " ".join(s.split())


def check_render(deck: Deck, text: str, page: str, width: int = WIDTH) -> list[str]:
    """Problems with rendered cards against G21 (Output Clarity); [] means the cards pass."""
    problems: list[str] = []
    # In cards.txt a step's action is the right-hand column, so read that column on
    # its own: a wrapped role or a [changed: ...] marker sits beside it on the left.
    flat_text = _norm(text)
    right_col = _norm(" ".join(line[WHO:] for line in text.splitlines()))
    flat_html = _norm(html.unescape(re.sub(r"<[^>]+>", " ", page)))
    for unit in deck.units():
        uid = str(unit.get("mls_id", "?"))
        for fmt, flat in (("cards.txt", flat_text), ("cards.html", flat_html)):
            if f"{uid}:" not in flat:
                problems.append(f"{fmt}: no card for {uid}")
        for t in unit.get("tasks") or []:
            if isinstance(t, dict) and isinstance(t.get("action"), str):
                action = _norm(t["action"])
                if action not in right_col:
                    problems.append(f"cards.txt: {uid} step {t.get('step')} is missing or altered")
                if action not in flat_html:
                    problems.append(f"cards.html: {uid} step {t.get('step')} is missing or altered")
    for n, line in enumerate(text.splitlines(), start=1):
        if len(line) > width:
            problems.append(f"cards.txt line {n} is {len(line)} characters; the limit is {width}")
    if FORBIDDEN_HTML.search(page):
        problems.append(f"cards.html is not text-only and offline: found {FORBIDDEN_HTML.search(page).group(0)!r}")
    colours = {c.lower() for c in COLOUR.findall(page)} - {"#000", "#fff", "#000000", "#ffffff"}
    if colours:
        problems.append(f"cards.html uses colours other than black and white: {', '.join(sorted(colours))}")
    for table in re.findall(r"<table>.*?</table>", page, re.S):
        for row in re.findall(r"<tr>(.*?)</tr>", table, re.S):
            cells = len(re.findall(r"<t[hd][ >]", row))
            if cells != 2:
                problems.append(f"cards.html has a table row with {cells} columns; cards are two-column")
                break
    return problems


def write_cards(deck: Deck, out_dir: Path) -> list[str]:
    """Write cards.txt and cards.html into out_dir; return the G21 check's problems."""
    text, page = render_text(deck), render_html(deck)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "cards.txt").write_text(text, encoding="utf-8")
    (out_dir / "cards.html").write_text(page, encoding="utf-8")
    return check_render(deck, text, page)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m lsb.render", description=__doc__.split("\n\n")[0])
    ap.add_argument("run", type=Path, help="an lsb.run output directory (with sequence.json and summary.json)")
    ap.add_argument("--out", type=Path, help="where to write the cards (default: the run directory)")
    args = ap.parse_args(argv)
    try:
        deck = load_run(args.run)
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read run {args.run}: {e}", file=sys.stderr)
        return 2
    out = args.out or args.run
    problems = write_cards(deck, out)
    print(f"wrote {out / 'cards.txt'} and {out / 'cards.html'} ({len(deck.units())} unit cards)")
    for p in problems:
        print(f"  FAIL G21: {p}")
    print("G21 Output Clarity: " + ("pass" if not problems else f"{len(problems)} problem(s)"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
