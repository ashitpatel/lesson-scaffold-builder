"""Multi-turn refinement: structure check, revision loading, revision loop."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from lsb import refine, run


FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID = json.loads((FIXTURES / "hydrology-valid.json").read_text(encoding="utf-8"))
U0 = VALID["mls_units"][0]["mls_id"]
ASSUMPTIONS = [{"mls_id": U0, "assumes": "Bottles are ready.", "if_not": "Use jars."}]


class FakeModel:
    def __init__(self, replies):
        self.replies = list(replies)

    def complete(self, system, user):
        return self.replies.pop(0), {"input": 1, "output": 1}


def edited(action_suffix=" during the monsoon"):
    seq = copy.deepcopy(VALID)
    seq["mls_units"][0]["tasks"][0]["action"] += action_suffix
    return seq


def run_dir(tmp):
    root = Path(tmp) / "run"
    root.mkdir()
    (root / "sequence.json").write_text(json.dumps(VALID), encoding="utf-8")
    (root / "choices.json").write_text(json.dumps({"single_module": False}), encoding="utf-8")
    (root / "summary.json").write_text(
        json.dumps({"optimisation": {}, "source_ref": "Test"}), encoding="utf-8")
    (root / "decomposed-sequence.json").write_text(
        json.dumps({"environment_assumptions": ASSUMPTIONS}), encoding="utf-8")
    (root / "source_trace.json").write_text(json.dumps([]), encoding="utf-8")
    return root


CRITIC_PASS = json.dumps({"verdict": "PASS", "checks": []})


class StructureCheck(unittest.TestCase):
    def test_action_only_edit_accepted(self):
        problems, changed = refine.check_refinement(VALID, ASSUMPTIONS, {"sequence": edited()}, None)
        self.assertEqual(problems, [])
        self.assertEqual(changed, [[U0, 1]])

    def test_structural_edits_rejected(self):
        bad = edited()
        bad["mls_units"][0]["tasks"].append({"step": 9, "role": "educator", "action": "Extra."})
        problems, _ = refine.check_refinement(VALID, ASSUMPTIONS, {"sequence": bad}, None)
        self.assertTrue(any("renumbered" in p for p in problems), problems)
        bad = edited()
        bad["mls_units"][0]["title"] = "New title"
        problems, _ = refine.check_refinement(VALID, ASSUMPTIONS, {"sequence": bad}, None)
        self.assertTrue(any("title" in p for p in problems), problems)
        bad = {"sequence": {"mls_units": []}}
        problems, _ = refine.check_refinement(VALID, ASSUMPTIONS, bad, None)
        self.assertTrue(any("units" in p for p in problems), problems)

    def test_focus_confines_edits(self):
        other = VALID["mls_units"][1]["mls_id"]
        problems, _ = refine.check_refinement(VALID, ASSUMPTIONS, {"sequence": edited()}, other)
        self.assertTrue(any("outside unit focus" in p for p in problems), problems)

    def test_assumption_text_may_change_ids_may_not(self):
        changed_assump = [dict(ASSUMPTIONS[0], assumes="Jars are ready.")]
        problems, _ = refine.check_refinement(
            VALID, ASSUMPTIONS, {"sequence": copy.deepcopy(VALID), "assumptions": changed_assump}, None)
        self.assertEqual(problems, [])
        problems, _ = refine.check_refinement(
            VALID, ASSUMPTIONS, {"sequence": copy.deepcopy(VALID), "assumptions": []}, None)
        self.assertTrue(any("assumptions" in p for p in problems), problems)


class Loading(unittest.TestCase):
    def test_original_latest_and_explicit_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = run_dir(tmp)
            seq, _, _, _, label, _ = refine.load_base(root, None)
            self.assertEqual(label, "original")
            self.assertEqual(seq["mls_units"][0]["mls_id"], U0)
            rev1 = root / "revisions" / "rev1"
            rev1.mkdir(parents=True)
            (rev1 / "sequence.json").write_text(json.dumps(edited()), encoding="utf-8")
            self.assertEqual(refine.list_revisions(root), [1])
            seq, _, _, _, label, _ = refine.load_base(root, None)
            self.assertEqual(label, "rev1")
            self.assertIn("monsoon", seq["mls_units"][0]["tasks"][0]["action"])
            _, _, _, _, label, _ = refine.load_base(root, 0)
            self.assertEqual(label, "original")

    def test_missing_base_and_non_run_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = run_dir(tmp)
            with self.assertRaises(SystemExit):
                refine.load_base(root, 3)
            with self.assertRaises(SystemExit):
                refine.load_base(Path(tmp), None)


class Scoping(unittest.TestCase):
    def seq(self):
        return edited()

    def test_changed_step_issue_kept(self):
        kept, scoped = refine.scope_issues(
            [{"check": "G02", "where": "mls_units[0].tasks[0]",
              "problem": "x", "severity": "major"}],
            self.seq(), ASSUMPTIONS, ASSUMPTIONS, [[U0, 1]])
        self.assertEqual(len(kept), 1)
        self.assertEqual(scoped, [])

    def test_unchanged_step_style_issue_downgraded(self):
        kept, scoped = refine.scope_issues(
            [{"check": "G02", "where": "mls_units[0].tasks[1]",
              "problem": "x", "severity": "major"}],
            self.seq(), ASSUMPTIONS, ASSUMPTIONS, [[U0, 1]])
        self.assertEqual(kept, [])
        self.assertEqual(len(scoped), 1)
        self.assertEqual(scoped[0]["severity"], "minor")
        self.assertEqual(scoped[0]["original_severity"], "major")
        self.assertTrue(scoped[0]["scoped_out"])

    def test_harm_checks_stay_in_scope_everywhere(self):
        for check in ("G19", "G06", "G07"):
            with self.subTest(check=check):
                kept, scoped = refine.scope_issues(
                    [{"check": check, "where": "mls_units[0].tasks[1]",
                      "problem": "x", "severity": "blocker"}],
                    self.seq(), ASSUMPTIONS, ASSUMPTIONS, [[U0, 1]])
                self.assertEqual(len(kept), 1)
                self.assertEqual(scoped, [])

    def test_unparseable_location_stays_in_scope(self):
        kept, scoped = refine.scope_issues(
            [{"check": "G02", "where": "somewhere", "problem": "x", "severity": "minor"}],
            self.seq(), ASSUMPTIONS, ASSUMPTIONS, [[U0, 1]])
        self.assertEqual(len(kept), 1)
        self.assertEqual(scoped, [])

    def test_unit_level_issue_downgraded(self):
        kept, scoped = refine.scope_issues(
            [{"check": "G13", "where": "mls_units[0]",
              "problem": "x", "severity": "major"}],
            self.seq(), ASSUMPTIONS, ASSUMPTIONS, [[U0, 1]])
        self.assertEqual(kept, [])
        self.assertEqual(len(scoped), 1)

    def test_changed_assumption_kept_unchanged_downgraded(self):
        new_assump = [dict(a, assumes="Jars are ready.") for a in ASSUMPTIONS]
        kept, _ = refine.scope_issues(
            [{"check": "G02", "where": "environment_assumptions[0]",
              "problem": "x", "severity": "major"}],
            self.seq(), new_assump, ASSUMPTIONS, [[U0, 1]])
        self.assertEqual(len(kept), 1)
        kept, scoped = refine.scope_issues(
            [{"check": "G02", "where": "environment_assumptions[0]",
              "problem": "x", "severity": "major"}],
            self.seq(), ASSUMPTIONS, ASSUMPTIONS, [[U0, 1]])
        self.assertEqual(kept, [])
        self.assertEqual(len(scoped), 1)


class RevisionLoop(unittest.TestCase):
    def test_pass_saves_revision_with_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = run_dir(tmp)
            model = FakeModel([json.dumps({"sequence": edited(), "note": "Added season."}), CRITIC_PASS])
            seq, assumptions, choices, trace, label, ref = refine.load_base(root, None)
            record = refine.run_revision("source", root, label, seq, assumptions, choices,
                                         trace, ref, "name the season", None, model, 1)
            self.assertIsNotNone(record)
            self.assertEqual(record["changed_steps"], [[U0, 1]])
            self.assertEqual(record["kind"], "step-edits")
            self.assertEqual(record["scoped_out"], [])
            rev1 = root / "revisions" / "rev1"
            self.assertTrue((rev1 / "cards.txt").exists())
            self.assertTrue((rev1 / "cards.html").exists())
            # second turn builds on the first
            seq2 = edited(" during the monsoon, after assembly")
            model2 = FakeModel([json.dumps({"sequence": seq2, "note": "x"}), CRITIC_PASS])
            seq, assumptions, choices, trace, label, _ = refine.load_base(root, None)
            self.assertEqual(label, "rev1")
            record2 = refine.run_revision("source", root, label, seq, assumptions, choices,
                                          trace, ref, "add timing", None, model2, 2)
            self.assertIsNotNone(record2)
            self.assertEqual(record2["base"], "rev1")

    def test_reject_saves_no_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = run_dir(tmp)
            critic = json.dumps({"verdict": "REJECT", "checks": []})
            model = FakeModel([json.dumps({"sequence": edited()}), critic])
            seq, assumptions, choices, trace, label, ref = refine.load_base(root, None)
            self.assertIsNone(refine.run_revision("source", root, label, seq, assumptions,
                                                  choices, trace, ref, "x", None, model, 1))
            self.assertFalse((root / "revisions" / "rev1" / "sequence.json").exists())
            self.assertFalse((root / "revisions" / "rev1" / "revision.json").exists())

    def test_out_of_scope_issue_does_not_block_landing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = run_dir(tmp)
            critic = json.dumps({"verdict": "REVISE", "checks": [
                {"id": "G02", "status": "fail", "issues": [
                    {"severity": "major", "where": "mls_units[0].tasks[1]",
                     "problem": "pre-existing wording"}]}]})
            model = FakeModel([json.dumps({"sequence": edited(), "note": "x"}), critic])
            seq, assumptions, choices, trace, label, ref = refine.load_base(root, None)
            record = refine.run_revision("source", root, label, seq, assumptions,
                                         choices, trace, ref, "x", None, model, 1)
            self.assertIsNotNone(record)
            self.assertEqual(len(record["scoped_out"]), 1)
            self.assertEqual(record["scoped_out"][0]["original_severity"], "major")

    def test_harm_issue_outside_the_edit_still_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = run_dir(tmp)
            critic = json.dumps({"verdict": "REVISE", "checks": [
                {"id": "G19", "status": "fail", "issues": [
                    {"severity": "blocker", "where": "mls_units[0].tasks[1]",
                     "problem": "unsafe"}]}]})
            replies = [json.dumps({"sequence": edited(), "note": "x"}), critic,
                       json.dumps({"sequence": edited(), "note": "x"}), critic]
            model = FakeModel(replies)
            seq, assumptions, choices, trace, label, ref = refine.load_base(root, None)
            self.assertIsNone(refine.run_revision("source", root, label, seq, assumptions,
                                                  choices, trace, ref, "x", None, model, 1))

    def test_approved_terms_come_from_both_decision_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = run_dir(tmp)
            (root / "locale-decisions.json").write_text(
                json.dumps({"0": "suomi (Finnish)", "1": ""}), encoding="utf-8")
            (root / "locale-add-decisions.json").write_text(
                json.dumps({"0": "like a sauna", "1": ""}), encoding="utf-8")
            self.assertEqual(refine.approved_locale_terms(root),
                             ["suomi (Finnish)", "like a sauna"])

    def test_approved_terms_missing_files_mean_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(refine.approved_locale_terms(run_dir(tmp)), [])

    def test_prompt_has_its_placeholders(self):
        self.assertEqual(set(run.prompt_placeholders("58-refine.md")),
                         {"SEQUENCE_JSON", "SOURCE_TEXT", "TEACHER_INSTRUCTION",
                          "UNIT_FOCUS", "ASSUMPTIONS", "PREVIOUS_OUTPUT", "CRITIC_FEEDBACK",
                          "RUN_LANGUAGE"})


if __name__ == "__main__":
    unittest.main()
