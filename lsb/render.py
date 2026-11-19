"""Render a passed MLS sequence as offline teacher cards, and check them (critic check G21).

    python3 -m lsb.render runs/<run>            # writes cards.txt and cards.html into the run
    python3 -m lsb.render runs/<run> --out DIR

The requirements' last stage is "Highly Scannable Offline Teacher Cards", and
G21 (Output Clarity) asks for a "high-contrast, text-only, dual-column format".
That is layout, so it is done here in code, not by a model: one overview card,
then one card per unit in dependency order. Each unit card has a two-column
WHO / WHAT TO DO step table, the conditions the unit relies on with what to do
if one doesn't hold, a fixed note on what to do when a group gets stuck (only
on units with group or pair work), and the changes the optimisation stages
made, by card.

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
# Free-text output language (summary.json "language") to BCP47 tag for
# cards.html. Unknown languages fall back to "en": no worse than before.
HTML_LANG = {
    "en": "en", "english": "en",
    "fr": "fr", "french": "fr", "francais": "fr", "français": "fr",
    "es": "es", "spanish": "es", "espanol": "es", "español": "es",
    "pt": "pt", "portuguese": "pt", "portugues": "pt", "português": "pt",
    "de": "de", "german": "de", "it": "it", "italian": "it",
    "nl": "nl", "dutch": "nl",
    "ar": "ar", "arabic": "ar",
    "hi": "hi", "hindi": "hi",
    "bn": "bn", "bengali": "bn", "bangla": "bn",
    "ur": "ur", "urdu": "ur",
    "ta": "ta", "tamil": "ta", "te": "te", "telugu": "te",
    "mr": "mr", "marathi": "mr", "gu": "gu", "gujarati": "gu",
    "kn": "kn", "kannada": "kn", "ml": "ml", "malayalam": "ml",
    "pa": "pa", "punjabi": "pa", "ne": "ne", "nepali": "ne",
    "th": "th", "thai": "th",
    "vi": "vi", "vietnamese": "vi",
    "id": "id", "indonesian": "id", "ms": "ms", "malay": "ms",
    "tl": "tl", "tagalog": "tl", "fil": "fil", "filipino": "fil",
    "my": "my", "burmese": "my", "myanmar": "my",
    "km": "km", "khmer": "km", "cambodian": "km", "lo": "lo", "lao": "lo",
    "zh": "zh", "chinese": "zh", "ja": "ja", "japanese": "ja", "ko": "ko", "korean": "ko",
    "sw": "sw", "swahili": "sw", "kiswahili": "sw",
    "yo": "yo", "yoruba": "yo", "ha": "ha", "hausa": "ha", "ig": "ig", "igbo": "ig",
    "am": "am", "amharic": "am",
    "ru": "ru", "russian": "ru", "tr": "tr", "turkish": "tr",
    "fa": "fa", "persian": "fa", "farsi": "fa",
    "fi": "fi", "finnish": "fi", "sv": "sv", "swedish": "sv", "is": "is", "icelandic": "is",
}


def html_lang(language: Any) -> str:
    """BCP47 tag for the run's output language; "en" when unknown."""
    if isinstance(language, str) and language.strip():
        return HTML_LANG.get(language.strip().lower(), "en")
    return "en"
# A fixed classroom-management note, the same on every card it appears on: it is
# rendered text, not a method card, so it adds no step and uses no card slot.
# It makes no outcome claim, and it ends in help (EB-03) rather than withholding it.
STUCK_HEADING = "If a group is stuck"
STUCK_LINES = (
    'Ask: "What exactly are you stuck on?"',
    'Then: "What is one small thing you can try in the next five minutes?"',
    "If they are still stuck, help: show them the next step or a worked example.",
)
# The English stuck note as the translate stage receives it ({{STUCK_NOTE}} in
# prompts/59-translate.md); a translated reply carries the same shape back.
STUCK_NOTE_EN = {"heading": STUCK_HEADING, "lines": list(STUCK_LINES)}
GROUP_WORK = re.compile(r"\b(groups?|pairs?|partners?|teams?|in threes|in fours)\b", re.I)
STAGE_NAMES = {"evidence_based": "Evidence-Based", "connected_learning": "Connected Learning", "participatory_budgeting": "Participatory Budgeting"}


@dataclass
class Deck:
    sequence: dict
    source_ref: str = ""
    assumptions: list[dict] = field(default_factory=list)  # final environment_assumptions (see run_assumptions)
    trace: list[dict] = field(default_factory=list)  # final source trace (card ids on changed steps)
    optimisation: dict = field(default_factory=dict)  # summary.json "optimisation"
    disclaimer: str = ""
    group_work_units: set[str] | None = None  # units with group work, decided on the reviewed English; None detects from this deck's actions
    stuck_note: tuple[str, tuple[str, ...]] | None = None  # translated (heading, lines); None prints the English note
    language: str | None = None  # summary.json output language when translated; None means English

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


FINAL_ASSUMPTIONS = "final_assumptions.json"  # environment_assumptions as printed on the cards


def _best_decompose(run_dir: Path, summary: dict) -> dict:
    best = summary.get("best_attempt")
    path = run_dir / f"{best:02d}-decompose.json" if isinstance(best, int) else None
    return json.loads(path.read_text(encoding="utf-8")) if path and path.exists() else {}


def run_assumptions(run_dir: Path, summary: dict | None = None) -> list[dict]:
    """The environment assumptions a saved run printed on its cards.

    Repair, relocalisation and translation change them after decompose, so a
    run saves the final ones in final_assumptions.json. Runs from before that
    have only the best attempt's NN-decompose.json, which is right only when
    none of those steps changed them.
    """
    path = run_dir / FINAL_ASSUMPTIONS
    if path.exists():
        found = json.loads(path.read_text(encoding="utf-8"))
    else:
        if summary is None:
            summary_p = run_dir / "summary.json"
            summary = json.loads(summary_p.read_text(encoding="utf-8")) if summary_p.exists() else {}
        found = _best_decompose(run_dir, summary).get("environment_assumptions")
    return [a for a in found or [] if isinstance(a, dict)]


TRANSLATION = "translation.json"
ENGLISH_FINAL = "english-final.json"


def group_work_for_run(run_dir: Path, summary: dict) -> set[str] | None:
    """Unit ids whose reviewed English had group work, or None to detect live.

    New translated runs record the set in summary.json; older ones are
    re-derived from english-final.json; English runs detect from their own
    actions, since those still match the pattern.
    """
    trans = summary.get("translation") or {}
    saved = trans.get("group_work_units")
    if isinstance(saved, list) and all(isinstance(u, str) for u in saved):
        return set(saved)
    if not trans.get("applied"):
        return None
    try:
        english = json.loads((run_dir / ENGLISH_FINAL).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    seq = english.get("sequence") if isinstance(english, dict) else None
    return find_group_work_units(seq) if isinstance(seq, dict) else None


def note_for_run(run_dir: Path) -> tuple[str, tuple[str, ...]] | None:
    """The run's translated stuck note, or None for the English note."""
    try:
        saved = json.loads((run_dir / TRANSLATION).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return parse_stuck_note(saved.get("stuck_note") if isinstance(saved, dict) else None)


def language_for_summary(summary: dict) -> str | None:
    """The output language for cards, or None for English.

    summary.json always records the requested "language", but the cards are
    translated only when translation applied; a failed translation stays English.
    """
    if (summary.get("translation") or {}).get("applied") and isinstance(summary.get("language"), str):
        return summary["language"]
    return None


def load_run(run_dir: Path) -> Deck:
    """A Deck from a saved `lsb.run` output directory."""
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    sequence = json.loads((run_dir / "sequence.json").read_text(encoding="utf-8"))
    decomposed = _best_decompose(run_dir, summary)
    trace_file = run_dir / "source_trace.json"
    trace = (json.loads(trace_file.read_text(encoding="utf-8")) if trace_file.exists()
             else decomposed.get("source_trace") or [])
    optimisation = summary.get("optimisation") or {}
    if "units" in optimisation:  # runs from before the PB stage logged one stage, unkeyed
        optimisation = {optimisation.get("stage", "connected_learning"): optimisation}
    return build_deck(sequence, {"environment_assumptions": run_assumptions(run_dir, summary)},
                      optimisation, trace, summary.get("source_ref", ""),
                      group_work_units=group_work_for_run(run_dir, summary),
                      stuck_note=note_for_run(run_dir),
                      language=language_for_summary(summary))


def build_deck(sequence: dict, decomposed: dict | None, optimisation: dict | None, trace: list | None,
               source_ref: str = "",
               group_work_units: set[str] | None = None,
               stuck_note: tuple[str, tuple[str, ...]] | None = None,
               language: str | None = None) -> Deck:
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
        group_work_units=group_work_units,
        stuck_note=stuck_note,
        language=language,
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


def _has_group_work(unit: dict, group_work: set[str] | None = None) -> bool:
    """True when the unit's steps put students in groups or pairs.

    `group_work` overrides detection: on translated runs the actions no longer
    match the English pattern, so the run records which units had group work
    in the reviewed English (see group_work_for_run).
    """
    if group_work is not None:
        return str(unit.get("mls_id")) in group_work
    return any(isinstance(t, dict) and GROUP_WORK.search(str(t.get("action", "")))
               for t in unit.get("tasks") or [])


def find_group_work_units(sequence: dict) -> set[str]:
    """Ids of the units whose actions put students in groups or pairs."""
    return {str(u.get("mls_id")) for u in (sequence or {}).get("mls_units") or []
            if isinstance(u, dict) and _has_group_work(u)}


def parse_stuck_note(obj: Any) -> tuple[str, tuple[str, ...]] | None:
    """A saved translated note as (heading, lines); None when absent or malformed."""
    if not isinstance(obj, dict):
        return None
    heading = obj.get("heading")
    lines = obj.get("lines")
    if not isinstance(heading, str) or not heading.strip():
        return None
    if not isinstance(lines, list) or not lines or \
            not all(isinstance(line, str) and line.strip() for line in lines):
        return None
    return heading, tuple(lines)


def _note(deck: Deck) -> tuple[str, tuple[str, ...]]:
    return deck.stuck_note or (STUCK_HEADING, STUCK_LINES)


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
        if _has_group_work(unit, deck.group_work_units):
            heading, lines = _note(deck)
            out.append(light)
            out.append(heading.upper())
            for line in lines:
                out += _wrap("- " + line, width, hang="  ")
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
        if _has_group_work(unit, deck.group_work_units):
            heading, lines = _note(deck)
            items = "".join(f"<li>{_e(line)}</li>" for line in lines)
            parts.append(f"<h3>{_e(heading)}</h3><ul>{items}</ul>")
        changes = _changes(deck, uid)
        if changes:
            items = "".join(f"<li>{_e(stage)}, {_e(card)} {_e(names.get(card, ''))}: {_e(summary)}</li>"
                            for stage, card, summary in changes)
            parts.append(f"<h3>Changes from the source</h3><ul>{items}</ul>")
        parts.append("</section>")

    return ("<!doctype html>\n" + f'<html lang="{html_lang(deck.language)}"><head><meta charset="utf-8">'
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>{_e(title)}</title><style>\n{CSS}\n</style></head><body>\n"
            + "\n".join(parts) + "\n</body></html>\n")


_WORD = re.compile(r"[A-Za-z']+")
_SENT_END = re.compile(r"[.!?]+")


def _syllables(word: str) -> int:
    word = word.lower().strip("'")
    if not word:
        return 0
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e"):
        count -= 1
    return max(count, 1)


def readability(sequence: dict | None, assumptions: list | None = None) -> dict:
    """Flesch reading ease over the teacher-facing texts, for summary.json.

    Titles, task actions and condition/fallback lines are the words a teacher
    reads; the score is recorded, never gated on, since locale terms and
    necessary detail legitimately lower it. Unclear wording is enforced by
    the critic (G02), which can judge what a count cannot.
    """
    texts = []
    for u in ((sequence or {}).get("mls_units") or []):
        if not isinstance(u, dict):
            continue
        if u.get("title"):
            texts.append(u["title"])
        for t in u.get("tasks") or []:
            if isinstance(t, dict) and t.get("action"):
                texts.append(t["action"])
    for a in assumptions or []:
        if not isinstance(a, dict):
            continue
        for key in ("assumes", "if_not"):
            if a.get(key):
                texts.append(a[key])
    blob = " ".join(texts)
    words = _WORD.findall(blob)
    sents = [s for s in _SENT_END.split(blob) if s.strip()]
    total = sum(_syllables(w) for w in words)
    longest = max((len(_WORD.findall(s)) for s in sents), default=0)
    words_n, sents_n = max(len(words), 1), max(len(sents), 1)
    return {"flesch": round(206.835 - 1.015 * (words_n / sents_n) - 84.6 * (total / words_n), 1),
            "words": len(words), "sentences": len(sents),
            "longest_sentence_words": longest}


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
    want = html_lang(deck.language)
    lang = re.search(r'<html lang="([^"]*)"', page)
    if lang is None:
        problems.append("cards.html has no lang attribute on <html>")
    elif lang.group(1) != want:
        problems.append(f"cards.html declares lang {lang.group(1)!r}; this run needs {want!r}")
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
