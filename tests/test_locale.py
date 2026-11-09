"""Locale handling: log/proposal checks, review, apply, keep-mode plumbing."""

import unittest

from lsb import ask
from lsb import locale as loc
from lsb import run
from lsb import validate as v


def sequence():
    return {"macro_objective": "m", "global_context": "g", "mls_units": [
        {"mls_id": "U1", "tasks": [
            {"action": "Buy paper at the local market."},
            {"action": "Count coins from the market trip."}]},
        {"mls_id": "U2", "tasks": [{"action": "Read the story."}]}]}


def log():
    return [
        {"original": "Kariakoo market", "generic": "the local market", "category": "market"},
        {"original": "shillings", "generic": "coins", "category": "currency"},
        {"original": "trader story", "generic": None, "category": "story"},
    ]


class Texts(unittest.TestCase):
    def test_strip_rule_is_the_old_generic_labels_line(self):
        self.assertIn("context-neutral names", loc.locale_rule("strip"))
        self.assertIn("context-neutral names", loc.locale_rule("relocalize"))

    def test_scope_with_approved_terms_lists_exceptions(self):
        scope = loc.locale_scope("strip", ["suomi (Finnish)", "chimanga"])
        self.assertIn("suomi (Finnish)", scope)
        self.assertIn("chimanga", scope)
        self.assertIn("G09", scope)
        plain = loc.locale_scope("strip")
        self.assertNotIn("suomi", plain)

    def test_keep_rule_and_scope_cover_names_objects_stories(self):
        self.assertIn("stories", loc.locale_rule("keep"))
        self.assertIn("Do not file G09", loc.locale_scope("keep"))
        self.assertIn("G09 applies", loc.locale_scope("strip"))


class ShapeChecks(unittest.TestCase):
    def test_locale_log_accepts_empty_and_full(self):
        self.assertEqual(loc.check_locale_log({"locale_log": []}), [])
        self.assertEqual(loc.check_locale_log({"locale_log": log()}), [])
        self.assertEqual(len(loc.check_locale_log({})), 1)
        found = loc.check_locale_log({"locale_log": [{"original": "x"}]})
        self.assertTrue(any("category" in p for p in found), found)

    def test_locale_log_checks_drop_reason(self):
        good = {"locale_log": [{"original": "x", "category": "market",
                                "generic": None, "drop_reason": "locale"}]}
        self.assertEqual(loc.check_locale_log(good), [])
        good["locale_log"][0]["drop_reason"] = "withheld"
        self.assertEqual(loc.check_locale_log(good), [])
        good["locale_log"][0]["drop_reason"] = None
        self.assertEqual(loc.check_locale_log(good), [])
        del good["locale_log"][0]["drop_reason"]
        self.assertEqual(loc.check_locale_log(good), [])
        bad = {"locale_log": [{"original": "x", "category": "market",
                               "drop_reason": "sometimes"}]}
        self.assertTrue(any("drop_reason" in p for p in loc.check_locale_log(bad)))

    def test_proposals_check_ids_and_text(self):
        good = {"proposals": [{"id": 0, "proposed": "Kisumu market"},
                              {"id": 1, "proposed": "shillings"}]}
        self.assertEqual(loc.check_proposals(good, 3), [])
        self.assertEqual(len(loc.check_proposals({}, 3)), 1)
        bad = {"proposals": [{"id": 0, "proposed": "x"}, {"id": 0, "proposed": "y"}]}
        self.assertTrue(loc.check_proposals(bad, 3))
        bad = {"proposals": [{"id": 5, "proposed": "x"}]}
        self.assertTrue(loc.check_proposals(bad, 3))
        bad = {"proposals": [{"id": 0, "proposed": "  "}]}
        self.assertTrue(loc.check_proposals(bad, 3))


class Additions(unittest.TestCase):
    ADD = {"unit": "U1", "step": 1, "anchor": "the local market",
           "addition": "in Kisumu", "reason": "names the district market"}

    def sequence(self):
        return {"mls_units": [
            {"mls_id": "U1", "tasks": [
                {"step": 1, "action": "Buy paper at the local market, then return to the local market."},
                {"step": 2, "action": "Count coins."}]},
            {"mls_id": "U2", "tasks": [{"step": 1, "action": "Read."}]}]}

    def test_check_accepts_good_rejects_bad(self):
        self.assertEqual(loc.check_additions({"additions": [dict(self.ADD)]}), [])
        self.assertEqual(loc.check_additions({"additions": []}), [])
        self.assertTrue(loc.check_additions({}))
        self.assertTrue(loc.check_additions({"additions": [{"unit": "U1"}]}))

    def test_choices_keyed_by_position_default_to_addition(self):
        (c,) = loc.addition_choices([dict(self.ADD)])
        self.assertEqual(c.key, "locale_add_0")
        self.assertEqual(c.default, "in Kisumu")
        self.assertTrue(c.free_text)
        self.assertIn("U1 step 1", c.question)

    def test_inserts_after_anchor_first_occurrence_only(self):
        out, notes = loc.apply_additions(self.sequence(), [dict(self.ADD)], {0: "in Kisumu"})
        action = out["mls_units"][0]["tasks"][0]["action"]
        self.assertIn("the local market in Kisumu, then return to the local market.", action)
        self.assertEqual(action.count("in Kisumu"), 1)
        self.assertTrue(any("added to U1 step 1" in n for n in notes), notes)
        # original untouched
        self.assertNotIn("Kisumu", str(self.sequence()))

    def test_adds_missing_space_and_reports_missing_targets(self):
        add = dict(self.ADD, addition="fresh")
        out, _ = loc.apply_additions(self.sequence(), [add], {0: "fresh"})
        self.assertIn("market fresh, then", out["mls_units"][0]["tasks"][0]["action"])
        for bad in (dict(self.ADD, unit="UX"),
                    dict(self.ADD, step=9),
                    dict(self.ADD, anchor="nowhere")):
            _, notes = loc.apply_additions(self.sequence(), [bad], {0: "x"})
            self.assertTrue(any("skipped" in n for n in notes), notes)


class Review(unittest.TestCase):
    def test_choices_default_to_proposed_with_free_text(self):
        props = [{"id": 0, "proposed": "Kisumu market", "reason": "r"},
                 {"id": 1, "proposed": "shillings", "reason": "r"}]
        choices = loc.review_choices(props, log())
        self.assertEqual([c.key for c in choices], ["locale_0", "locale_1"])
        self.assertEqual(choices[0].default, "Kisumu market")
        self.assertTrue(choices[0].free_text)
        self.assertIn("Kariakoo", choices[0].question)

    def test_file_answers_accept_custom_skip_and_default(self):
        import json
        import tempfile
        props = [{"id": 0, "proposed": "Kisumu market", "reason": "r"},
                 {"id": 1, "proposed": "shillings", "reason": "r"}]
        choices = loc.review_choices(props, log())
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"locale_0": "My town market", "locale_1": ""}, f)
            path = f.name
        prompter = ask.FilePrompter(path)
        self.assertEqual(prompter.ask(choices[0]), "My town market")
        self.assertEqual(prompter.ask(choices[1]), "")
        self.assertEqual(ask.DefaultPrompter().ask(choices[0]), "Kisumu market")


class Translation(unittest.TestCase):
    def seq(self):
        return {"macro_objective": "Learn maps.", "global_context": {"grade_band": "Middle"},
                "mls_units": [
                    {"mls_id": "U1", "title": "Home maps", "duration_weeks": 2,
                     "dependencies": [], "macro_alignment": "Maps homes.",
                     "tasks": [{"step": 1, "role": "Lead_Educator", "action": "Draw home."},
                               {"step": 2, "role": "Peer_Facilitator", "action": "Share maps."}]},
                    {"mls_id": "U2", "title": "Totals", "duration_weeks": 2,
                     "dependencies": ["U1"], "macro_alignment": "Adds up.",
                     "tasks": [{"step": 1, "role": "Lead_Educator", "action": "Count all."}]}]}

    def assump(self):
        return [{"mls_id": "U1", "assumes": "Paper around.", "if_not": "Use slates."}]

    def translated(self):
        seq = self.seq()
        seq["macro_objective"] = "Apprendre les cartes."
        for u in seq["mls_units"]:
            u["title"] += " (fr)"
            u["macro_alignment"] += " (fr)"
            for t in u["tasks"]:
                t["action"] += " (fr)"
        assump = [{"mls_id": "U1", "assumes": "Papier autour. (fr)", "if_not": "Ardoises. (fr)"}]
        return {"sequence": seq, "assumptions": assump}

    def test_good_translation_passes(self):
        self.assertEqual(loc.check_translation(self.seq(), self.assump(), self.translated()), [])

    def test_bad_shapes_fail(self):
        before, assump = self.seq(), self.assump()
        self.assertTrue(loc.check_translation(before, assump, {}))
        self.assertTrue(loc.check_translation(before, assump, {"sequence": {}, "assumptions": []}))

    def test_structure_changes_fail(self):
        before, assump = self.seq(), self.assump()
        good = self.translated()
        dropped = {"sequence": {"mls_units": good["sequence"]["mls_units"][:1],
                                "macro_objective": "x", "global_context": {"grade_band": "Middle"}},
                   "assumptions": good["assumptions"]}
        self.assertTrue(loc.check_translation(before, assump, dropped))
        bad = self.translated()
        bad["sequence"]["mls_units"][0]["tasks"][0]["role"] = "Peer_Facilitator"
        self.assertTrue(any("role" in p for p in loc.check_translation(before, assump, bad)))
        bad = self.translated()
        bad["sequence"]["mls_units"][1]["dependencies"] = []
        self.assertTrue(loc.check_translation(before, assump, bad))
        bad = self.translated()
        bad["sequence"]["mls_units"][0]["tasks"][0]["action"] = "  "
        self.assertTrue(any("emptied" in p for p in loc.check_translation(before, assump, bad)))
        bad = self.translated()
        bad["assumptions"][0]["mls_id"] = "U9"
        self.assertTrue(loc.check_translation(before, assump, bad))

    def test_output_language_normalizes_english_away(self):
        self.assertIsNone(loc.output_language(""))
        self.assertIsNone(loc.output_language("  "))
        self.assertIsNone(loc.output_language("en"))
        self.assertIsNone(loc.output_language("English"))
        self.assertEqual(loc.output_language("French"), "French")
        self.assertEqual(loc.output_language("  fr "), "fr")


class Apply(unittest.TestCase):
    def test_replaces_in_actions_and_assumptions(self):
        assumptions = [{"assumes": "paper from the local market", "if_not": "use coins"}]
        out, out_a, notes = loc.apply_locale(sequence(), log(), {0: "Kisumu market", 1: "tokens"}, assumptions)
        text = out["mls_units"][0]["tasks"][0]["action"]
        self.assertIn("Kisumu market", text)
        self.assertNotIn("the local market", text)
        self.assertIn("tokens", out["mls_units"][0]["tasks"][1]["action"])
        self.assertIn("Kisumu market", out_a[0]["assumes"])
        self.assertIn("tokens", out_a[0]["if_not"])
        self.assertEqual(len(notes), 2)
        # inputs untouched
        self.assertIn("the local market", sequence()["mls_units"][0]["tasks"][0]["action"])

    def test_skips_empty_dropped_and_missing(self):
        out, _, notes = loc.apply_locale(sequence(), log(), {0: "", 2: "X"})
        self.assertNotIn("X", str(out))
        self.assertTrue(any("dropped" in n for n in notes), notes)
        out, _, notes = loc.apply_locale(
            sequence(), [{"original": "x", "generic": "nope", "category": "place"}], {0: "Y"})
        self.assertTrue(any("not found" in n for n in notes), notes)


class Plumbing(unittest.TestCase):
    def test_validate_skip_d10(self):
        term = v.load_config()["regional_terms"][0]
        payload = {"mls_units": [{"tasks": [{"action": f"Visit {term}."}]}]}
        self.assertIn("D10", v.validate(payload).failed_ids())
        self.assertNotIn("D10", v.validate(payload, skip_d10=True).failed_ids())

    def test_values_carry_locale_placeholders(self):
        src = run.Source(text="t", ref="r")
        self.assertIn("LOCALE_RULE", run.decompose_values(src))
        self.assertIn("Keep the source's locale",
                      run.decompose_values(src, locale_mode="keep")["LOCALE_RULE"])
        vals = run.critic_values(src, {"sequence": {}}, v.validate({}))
        self.assertIn("LOCALE_SCOPE", vals)
        kept = run.critic_values(src, {"sequence": {}}, v.validate({}), keep_locale=True)
        self.assertIn("Do not file G09", kept["LOCALE_SCOPE"])

    def test_new_prompts_have_their_placeholders(self):
        self.assertEqual(set(run.prompt_placeholders("55-locale-log.md")),
                         {"SOURCE_TEXT", "SEQUENCE_JSON"})
        self.assertEqual(set(run.prompt_placeholders("56-relocalize.md")),
                         {"LOCALE_LOG", "TARGET_LOCALE", "LOCALE_NOTES", "SEQUENCE_JSON"})
        self.assertEqual(set(run.prompt_placeholders("57-locale-add.md")),
                         {"SEQUENCE_JSON", "TARGET_LOCALE", "LOCALE_NOTES", "LOCALE_LOG"})
        self.assertEqual(set(run.prompt_placeholders("59-translate.md")),
                         {"SEQUENCE_JSON", "ASSUMPTIONS", "TARGET_LANGUAGE", "FEEDBACK"})

    def test_critic_values_carry_approved_terms(self):
        src = run.Source(text="t", ref="r")
        vals = run.critic_values(src, {"sequence": {}}, v.validate({}),
                                 approved_terms=["suomi (Finnish)"])
        self.assertIn("suomi (Finnish)", vals["LOCALE_SCOPE"])

    def test_locale_notes_default_is_empty(self):
        self.assertEqual(ask.DefaultPrompter().ask(run._locale_notes_choice()), "")
        self.assertEqual(run._locale_choice().default, "strip")

    def test_locale_additions_default_is_off(self):
        self.assertFalse(ask.DefaultPrompter().ask(run._locale_additions_choice()))

    def test_output_language_default_is_empty(self):
        self.assertEqual(ask.DefaultPrompter().ask(run._output_language_choice()), "")


if __name__ == "__main__":
    unittest.main()
