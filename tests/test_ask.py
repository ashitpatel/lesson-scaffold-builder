"""User choices: prompters, content-derived suggestions, card filtering (no model calls)."""

import json
import tempfile
import unittest
from pathlib import Path

from lsb import ask
from lsb import optimise as opt

ROOT = Path(__file__).resolve().parents[1]
CARDS = {"eb": ROOT / "frameworks/evidence-based-practices.md",
         "cl": ROOT / "frameworks/connected-learning.md",
         "pb": ROOT / "frameworks/participatory-budgeting.md"}


def choice(**over):
    kw = {"key": "k", "question": "Pick?", "options": ((1, "one", ""), (2, "two", "")), "default": 2}
    kw.update(over)
    return ask.Choice(**kw)


def scripted(answers):
    it = iter(answers)

    def fake_input(_):
        try:
            return next(it)
        except StopIteration:
            raise EOFError from None
    return ask.InteractivePrompter(input=fake_input, output=lambda *a: None)


class Prompters(unittest.TestCase):
    def test_default_returns_defaults(self):
        self.assertEqual(ask.DefaultPrompter().ask(choice()), 2)

    def test_interactive_picks_retries_and_defaults(self):
        self.assertEqual(scripted(["1"]).ask(choice()), 1)
        self.assertEqual(scripted(["9", "x", "2"]).ask(choice()), 2)
        self.assertEqual(scripted([""]).ask(choice()), 2)
        self.assertEqual(scripted([]).ask(choice()), 2)  # EOF takes the default

    def test_interactive_multi_and_free_text(self):
        c = choice(multi=True, default=[1, 2])
        self.assertEqual(scripted(["2,1"]).ask(c), [2, 1])
        self.assertEqual(scripted([""]).ask(c), [1, 2])
        c = choice(free_text=True, default="auto", options=(("auto", "auto", ""),))
        self.assertEqual(scripted(["by skill"]).ask(c), "by skill")

    def test_file_answers_valid_missing_and_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "answers.json"
            f.write_text(json.dumps({"k": 1, "m": ["EB-01", "XX"], "n": "zzz"}), encoding="utf-8")
            p = ask.FilePrompter(f)
            self.assertEqual(p.ask(choice()), 1)
            self.assertEqual(p.ask(choice(key="missing")), 2)
            self.assertEqual(p.ask(choice(key="n")), 2)
            c = choice(key="m", multi=True, default=["EB-01"],
                       options=(("EB-01", "a", ""), ("EB-02", "b", "")))
            self.assertEqual(p.ask(c), ["EB-01"])

    def test_file_must_hold_an_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "answers.json"
            f.write_text("[1]", encoding="utf-8")
            with self.assertRaises(SystemExit):
                ask.FilePrompter(f)


class Suggestions(unittest.TestCase):
    def test_section_headers_come_from_the_source(self):
        src = (ROOT / "tests/fixtures/kenya-water-source.md").read_text(encoding="utf-8")
        heads = ask.section_headers(src)
        self.assertEqual(len(heads), 7)
        self.assertTrue(heads[0].startswith("3.1"))

    def test_card_hints_cover_every_card_the_code_accepts(self):
        for key, ids in (("eb", opt.EB_CARDS), ("cl", opt.CL_CARDS), ("pb", opt.PB_CARDS)):
            with self.subTest(stage=key):
                hints = ask.card_hints(CARDS[key])
                self.assertEqual(tuple(h[0] for h in hints), ids)
                self.assertTrue(all(h[1] and h[2] for h in hints), hints)

    def test_filter_keeps_head_guardrails_and_allowed_cards(self):
        for key, ids in (("eb", opt.EB_CARDS), ("cl", opt.CL_CARDS), ("pb", opt.PB_CARDS)):
            with self.subTest(stage=key):
                full = CARDS[key].read_text(encoding="utf-8")
                kept = ask.filter_cards(full, ids[:2])
                self.assertIn("## Guardrails", kept)
                for cid in ids[:2]:
                    self.assertIn(f"## {cid} ", kept)
                for cid in ids[2:]:
                    self.assertNotIn(f"## {cid} ", kept)
                self.assertNotIn("User limits", kept)
        pb = ask.filter_cards(CARDS["pb"].read_text(encoding="utf-8"), opt.PB_CARDS)
        self.assertIn("## The fit-gate", pb)

    def test_filter_adds_a_limits_line_only_when_non_default(self):
        full = CARDS["eb"].read_text(encoding="utf-8")
        self.assertIn("at most 1", ask.filter_cards(full, opt.EB_CARDS, max_cards=1))
        self.assertIn("do not add a step",
                      ask.filter_cards(full, opt.EB_CARDS, added_step=False))


if __name__ == "__main__":
    unittest.main()
