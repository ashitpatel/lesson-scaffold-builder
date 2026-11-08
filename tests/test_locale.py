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

    def test_locale_notes_default_is_empty(self):
        self.assertEqual(ask.DefaultPrompter().ask(run._locale_notes_choice()), "")
        self.assertEqual(run._locale_choice().default, "strip")


if __name__ == "__main__":
    unittest.main()
