"""User choices for a run: how to break the source down, what each stage may do.

A run asks nothing by default (`DefaultPrompter`): every choice falls back to
the value the pipeline has always used. `--ask` asks on the terminal;
`--answers FILE` reads the answers from a JSON object first (missing or
invalid answers fall back to defaults), which is how sweeps answer without
stopping. Whatever decided, the values land in choices.json in the run folder.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from lsb import optimise as opt

SECTION = re.compile(r"^##\s+(.+?)\s*$", re.M)
HEADING = re.compile(r"^## (.+?)\s*$", re.M)
CARD_HEADING = re.compile(r"^## ([A-Z]+-\d\d) (.+?)\s*$", re.M)
TARGETS = re.compile(r"^\*\*Targets:\*\* (.+?)\s*$", re.M)


@dataclass(frozen=True)
class Choice:
    """One question: `options` are (value, label, hint); one value is the default."""
    key: str
    question: str
    options: tuple[tuple[Any, str, str], ...]
    default: Any
    multi: bool = False
    free_text: bool = False
    context: str = ""
    details: tuple[tuple[Any, str], ...] = ()  # (value, expanded brief) for "?N" in InteractivePrompter


def detail_for(choice: Choice, value: Any) -> str | None:
    """The expanded brief for one option value, or None when it has none."""
    for v, text in choice.details:
        if v == value:
            return text
    return None


def interactive_available() -> bool:
    """True when a human can answer questions (stdin is a terminal)."""
    try:
        return sys.stdin.isatty()
    except (AttributeError, ValueError):
        return False


class Prompter(Protocol):
    def ask(self, choice: Choice) -> Any:
        """Return this choice's value."""

    def show(self, text: str) -> None:
        """Display a non-question message (a no-op where nobody reads)."""


class DefaultPrompter:
    """Ask nothing; every choice takes its default."""

    def ask(self, choice: Choice) -> Any:
        return choice.default

    def show(self, text: str) -> None:
        pass


class InteractivePrompter:
    """Ask on the terminal. Blank answers and EOF take the default."""

    def __init__(self, input=input, output=print):
        self.input = input
        self.output = output

    def show(self, text: str) -> None:
        self.output(text)

    @staticmethod
    def _show_detail(choice: Choice, which: str, output) -> None:
        if not choice.details:
            output("No further detail available.")
            return
        try:
            value = choice.options[int(which.strip()) - 1][0]
        except (ValueError, IndexError):
            output("Type ?1, ?2, ... for more about an option.")
            return
        found = detail_for(choice, value)
        output(found if found is not None else "No further detail for that option.")

    def ask(self, choice: Choice) -> Any:
        if choice.context:
            self.output(choice.context)
        self.output(f"{choice.question} (default: {self._label(choice, choice.default)})")
        for n, (_, label, hint) in enumerate(choice.options, start=1):
            self.output(f"  {n}. {label}" + (f" — {hint}" if hint else ""))
        if choice.multi:
            self.output("  (comma-separated numbers for more than one)")
        if choice.free_text:
            self.output("  (or type your own answer)")
        if choice.details:
            self.output("  (?N for more about an option)")
        while True:
            try:
                raw = self.input("> ").strip()
            except EOFError:
                return choice.default
            if not raw:
                return choice.default
            if raw.startswith("?"):
                self._show_detail(choice, raw[1:], self.output)
                continue
            if choice.multi:
                try:
                    picked = [choice.options[int(p.strip()) - 1][0] for p in raw.split(",")]
                except (ValueError, IndexError):
                    pass
                else:
                    if picked:
                        return picked
            else:
                try:
                    return choice.options[int(raw) - 1][0]
                except (ValueError, IndexError):
                    if choice.free_text:
                        return raw
            self.output("Please answer with one of the numbers shown.")

    @staticmethod
    def _label(choice: Choice, value: Any) -> str:
        if isinstance(value, list):
            return ", ".join(InteractivePrompter._label(choice, v) for v in value)
        for v, label, _ in choice.options:
            if v == value:
                return label
        return str(value)


class FilePrompter:
    """Take answers from a JSON object; anything missing or invalid takes its default."""

    def __init__(self, path: Path | str):
        self.answers = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(self.answers, dict):
            raise SystemExit(f"answers file {path} must hold a JSON object of choice answers")

    def show(self, text: str) -> None:
        pass

    def ask(self, choice: Choice) -> Any:
        if choice.key not in self.answers:
            return choice.default
        raw = self.answers[choice.key]
        valid = {v for v, _, _ in choice.options}
        if choice.multi:
            picked = [v for v in raw if v in valid] if isinstance(raw, list) else []
            return picked or choice.default
        if raw in valid or (choice.free_text and isinstance(raw, str) and raw.strip()):
            return raw
        return choice.default


def section_headers(source_text: str) -> list[str]:
    """The source's `##` section headings, for grounding breakdown choices."""
    return SECTION.findall(source_text)


def card_hints(cards_path: Path) -> list[tuple[str, str, str]]:
    """(card id, name, Targets line) for each card section in a frameworks file."""
    text = cards_path.read_text(encoding="utf-8")
    ids = [(m.group(1), m.group(2), m.start()) for m in CARD_HEADING.finditer(text)]
    out = []
    for i, (cid, name, start) in enumerate(ids):
        end = ids[i + 1][2] if i + 1 < len(ids) else len(text)
        m = TARGETS.search(text, start, end)
        out.append((cid, name, m.group(1) if m else ""))
    return out


def filter_cards(full_text: str, allowed: tuple[str, ...],
                 max_cards: int = opt.MAX_CARDS, added_step: bool = True) -> str:
    """Keep the file head, every non-card `##` section, and the allowed cards.

    Non-card sections (the PB fit-gate, the guardrails) always stay: they bind
    every card. When the limits differ from the code defaults, a user-limits
    line is prepended so the model sees them before the cards.
    """
    matches = list(HEADING.finditer(full_text))
    head = full_text[:matches[0].start()].rstrip() if matches else full_text.rstrip()
    parts = [head, ""]
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        cm = CARD_HEADING.match(m.group(0))
        if cm is None or cm.group(1) in allowed:
            parts += [full_text[m.start():end].rstrip(), ""]
    out = "\n".join(parts)
    if max_cards != opt.MAX_CARDS or not added_step:
        limits = [f"apply at most {max_cards} of these cards"]
        limits.append("you may add one step" if added_step else "do not add a step; edit existing steps only")
        out = "User limits: " + ", ".join(limits) + ".\n\n" + out
    return out
