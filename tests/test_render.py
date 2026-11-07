"""Teacher cards: content, layout, and the G21 check that guards them."""

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from lsb import render

FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID = json.loads((FIXTURES / "hydrology-valid.json").read_text(encoding="utf-8"))
U0, U1 = (u["mls_id"] for u in VALID["mls_units"])

DECOMPOSED = {"environment_assumptions": [
    {"mls_id": U0, "assumes": "Reused bottles are available.", "if_not": "Use any straight-sided jar."}]}
OPTIMISATION = {"connected_learning": {"units": {
    U0: {"status": "applied", "changes": [{"step": 2, "change": "modified", "card": "CL-02", "summary": "rotating roles"}]},
    U1: {"status": "reverted", "changes": [{"step": 1, "change": "added", "card": "CL-05", "summary": "dropped edit"}]},
}}}
TRACE = [{"mls_id": U0, "step": 2, "source_locator": "§8A"}, {"mls_id": U0, "step": 2, "card": "CL-02", "change": "modified"}]


def deck(sequence=VALID, **kw):
    args = {"decomposed": DECOMPOSED, "optimisation": OPTIMISATION, "trace": TRACE, "source_ref": "Test source"}
    args.update(kw)
    return render.build_deck(sequence, args["decomposed"], args["optimisation"], args["trace"], args["source_ref"])


class Content(unittest.TestCase):
    def setUp(self):
        self.deck = deck()
        self.text = render.render_text(self.deck)
        self.page = render.render_html(self.deck)

    def test_cards_pass_their_own_check(self):
        self.assertEqual(render.check_render(self.deck, self.text, self.page), [])

    def test_one_card_per_unit_in_dependency_order(self):
        reordered = copy.deepcopy(VALID)
        reordered["mls_units"].reverse()
        text = render.render_text(deck(reordered))
        self.assertLess(text.index(f"{U0}:"), text.index(f"{U1}:"))

    def test_changed_step_is_marked_with_its_card(self):
        self.assertIn("[changed: CL-02]", self.text)
        self.assertIn("[changed: CL-02]", self.page)

    def test_kept_changes_are_listed_by_card_name_and_reverted_ones_are_not(self):
        self.assertIn("Connected Learning, CL-02 Structural Peer Roles: rotating roles", self.text)
        self.assertNotIn("dropped edit", self.text)
        self.assertNotIn("dropped edit", self.page)

    def test_assumptions_and_fallbacks_are_shown(self):
        self.assertIn("Needs: Reused bottles are available.", self.text)
        self.assertIn("If not: Use any straight-sided jar.", self.page)

    def test_overview_and_disclaimer(self):
        self.assertIn("LESSON SCAFFOLD: Test source", self.text)
        self.assertIn("does not prescribe operational", self.text)
        self.assertIn(f"Builds on {U0}", self.text)

    def test_html_is_escaped(self):
        seq = copy.deepcopy(VALID)
        seq["mls_units"][0]["tasks"][0]["action"] = "Compare <b>2 < 3</b> & label it."
        d = deck(seq)
        page = render.render_html(d)
        self.assertIn("&lt;b&gt;2 &lt; 3&lt;/b&gt; &amp; label it.", page)
        self.assertEqual(render.check_render(d, render.render_text(d), page), [])

    def test_long_role_and_marker_wrap_beside_the_action(self):
        seq = copy.deepcopy(VALID)
        seq["mls_units"][0]["tasks"][1]["role"] = "Community_Volunteer"
        d = deck(seq)
        self.assertEqual(render.check_render(d, render.render_text(d), render.render_html(d)), [])

    def test_works_without_optional_inputs(self):
        d = render.build_deck(VALID, None, None, None)
        self.assertEqual(render.check_render(d, render.render_text(d), render.render_html(d)), [])


class Check(unittest.TestCase):
    def setUp(self):
        self.deck = deck()
        self.text = render.render_text(self.deck)
        self.page = render.render_html(self.deck)
        self.action = VALID["mls_units"][0]["tasks"][0]["action"]

    def problems(self, text=None, page=None):
        return render.check_render(self.deck, text or self.text, page or self.page)

    def test_altered_step(self):
        first_words = " ".join(self.action.split()[:3])
        found = self.problems(text=self.text.replace(first_words, "Do something else", 1))
        self.assertTrue(any("step 1 is missing or altered" in p for p in found), found)

    def test_missing_card(self):
        found = self.problems(page=self.page.replace(f"{U1}:", f"{U1} -"))
        self.assertIn(f"cards.html: no card for {U1}", found)

    def test_line_too_long(self):
        found = self.problems(text=self.text + "x" * 90 + "\n")
        self.assertTrue(any("characters; the limit is 78" in p for p in found), found)

    def test_images_scripts_and_links_are_rejected(self):
        for bad in ('<img src="a.png">', "<script>x()</script>", '<link rel="stylesheet" href="a.css">',
                    "body{background:url(a.png)}", "see https://example.org"):
            with self.subTest(bad=bad):
                found = self.problems(page=self.page.replace("</body>", bad + "</body>"))
                self.assertTrue(any("not text-only and offline" in p for p in found), found)

    def test_colours_other_than_black_and_white(self):
        found = self.problems(page=self.page.replace("color: #000", "color: #333", 1))
        self.assertTrue(any("#333" in p for p in found), found)

    def test_three_column_row(self):
        found = self.problems(page=self.page.replace("</td></tr>", "</td><td>extra</td></tr>", 1))
        self.assertTrue(any("3 columns" in p for p in found), found)


class Files(unittest.TestCase):
    def test_load_run_reads_a_saved_run_including_the_old_log_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "sequence.json").write_text(json.dumps(VALID))
            (run_dir / "01-decompose.json").write_text(json.dumps({"sequence": VALID, **DECOMPOSED, "source_trace": []}))
            old_log = {"stage": "connected_learning", **OPTIMISATION["connected_learning"], "reviews": []}
            (run_dir / "summary.json").write_text(json.dumps({"best_attempt": 1, "optimisation": old_log,
                                                              "source_ref": "Saved"}))
            (run_dir / "source_trace.json").write_text(json.dumps(TRACE))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(render.main([str(run_dir)]), 0)
            text = (run_dir / "cards.txt").read_text(encoding="utf-8")
            self.assertIn("LESSON SCAFFOLD: Saved", text)
            self.assertIn("CL-02 Structural Peer Roles", text)
            self.assertIn("Reused bottles", text)
            self.assertTrue((run_dir / "cards.html").exists())

    def test_unreadable_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stderr(io.StringIO()):
                self.assertEqual(render.main([tmp]), 2)


if __name__ == "__main__":
    unittest.main()
