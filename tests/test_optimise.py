"""The code check on optimisation-stage edits, and merging accepted edits back."""

import copy
import json
import re
import unittest
from pathlib import Path

from lsb import optimise as opt
from lsb import validate as v

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = json.loads((ROOT / "tests/fixtures/example-persuasive-valid.json").read_text(encoding="utf-8"))
BEFORE = EXAMPLE["mls_units"][1]


def prompt_example():
    """The worked output in prompts/30-connected-learning.md."""
    text = (ROOT / "prompts/30-connected-learning.md").read_text(encoding="utf-8")
    return json.loads(re.findall(r"```json\n(.*?)```", text, re.S)[-1])


def abstain():
    return {"mls_id": BEFORE["mls_id"], "decision": "ABSTAIN", "reason": "r", "credit": [],
            "unit": copy.deepcopy(BEFORE), "changes": [], "deferred": []}


def modified(step=2, card="CL-04"):
    out = abstain()
    out["decision"] = "APPLY"
    out["unit"]["tasks"][step - 1]["action"] += " Add each draft to a class folder."
    out["changes"] = [{"step": step, "change": "modified", "replaces_step": step, "card": card, "summary": "s"}]
    return out


def problems(result):
    return opt.check_unit_edit(BEFORE, result)


class Accepted(unittest.TestCase):
    def test_prompt_example_passes_the_check(self):
        self.assertEqual(problems(prompt_example()), [])

    def test_prompt_example_merged_passes_every_code_check(self):
        ex = prompt_example()
        merged = opt.merge(EXAMPLE, {ex["mls_id"]: ex["unit"]})
        report = v.validate(merged)
        self.assertTrue(report.passed, v.format_text(report))
        self.assertEqual(len(merged["mls_units"][1]["tasks"]), 5)
        self.assertEqual(merged["mls_units"][0], EXAMPLE["mls_units"][0])
        self.assertEqual(len(EXAMPLE["mls_units"][1]["tasks"]), 4, "merge must not change its input")

    def test_abstain_unchanged(self):
        self.assertEqual(problems(abstain()), [])

    def test_modified_step_with_replaces_step(self):
        self.assertEqual(problems(modified()), [])

    def test_modified_plus_added(self):
        out = modified()
        out["unit"]["tasks"].append({"step": 5, "role": "Lead_Educator", "action": "Show the letters to another class."})
        out["changes"].append({"step": 5, "change": "added", "replaces_step": None, "card": "CL-05", "summary": "s"})
        self.assertEqual(problems(out), [])


class Rejected(unittest.TestCase):
    def assertProblem(self, result, fragment):
        found = problems(result)
        self.assertTrue(any(fragment in p for p in found), found)

    def test_abstain_with_edits(self):
        out = modified()
        out["decision"] = "ABSTAIN"
        self.assertProblem(out, "ABSTAIN but the steps changed")

    def test_apply_without_changes(self):
        out = abstain()
        out["decision"] = "APPLY"
        self.assertProblem(out, "APPLY but 'changes' is empty")

    def test_wrong_unit(self):
        out = abstain()
        out["mls_id"] = "MLS-PERSUADE-01"
        self.assertProblem(out, "mls_id is")

    def test_fixed_fields_cannot_change(self):
        for f, value in (("dependencies", []), ("duration_weeks", 4), ("macro_alignment", "x"), ("title", "x")):
            with self.subTest(field=f):
                out = modified()
                out["unit"][f] = value
                self.assertProblem(out, f"unit.{f} changed")

    def test_removed_step(self):
        out = modified()
        del out["unit"]["tasks"][3]
        self.assertProblem(out, "removed")

    def test_two_added_steps(self):
        out = abstain()
        out["decision"] = "APPLY"
        for s in (5, 6):
            out["unit"]["tasks"].append({"step": s, "role": "Lead_Educator", "action": f"Extra {s}."})
            out["changes"].append({"step": s, "change": "added", "replaces_step": None, "card": "CL-05", "summary": "s"})
        self.assertProblem(out, "2 steps added")

    def test_unlogged_change(self):
        out = modified()
        out["changes"] = []
        out["unit"]["tasks"][0]["action"] += " Also this."
        self.assertProblem(out, "step 1 differs from every original step but has no change entry")

    def test_role_change_counts_as_a_change(self):
        out = modified()
        out["unit"]["tasks"][2]["role"] = "Lead_Educator"
        self.assertProblem(out, "step 3 differs")

    def test_change_logged_on_an_exact_copy(self):
        out = modified()
        out["changes"].append({"step": 1, "change": "modified", "replaces_step": 1, "card": "CL-04", "summary": "s"})
        self.assertProblem(out, "exact copy")

    def test_replaces_a_kept_step(self):
        out = modified()
        out["changes"][0]["replaces_step"] = 1
        self.assertProblem(out, "kept or already replaced")

    def test_reordered_steps(self):
        out = abstain()
        out["decision"] = "APPLY"
        tasks = out["unit"]["tasks"]
        tasks[1], tasks[2] = tasks[2], tasks[1]
        tasks[1]["step"], tasks[2]["step"] = 2, 3
        tasks[2]["action"] += " Then swap."
        out["changes"] = [{"step": 3, "change": "modified", "replaces_step": 2, "card": "CL-02", "summary": "s"}]
        self.assertProblem(out, "reordered")

    def test_unknown_card(self):
        self.assertProblem(modified(card="EB-01"), "unknown card")

    def test_three_cards(self):
        out = modified(step=1, card="CL-01")
        for step, card in ((2, "CL-02"), (3, "CL-03")):
            out["unit"]["tasks"][step - 1]["action"] += " More."
            out["changes"].append({"step": step, "change": "modified", "replaces_step": step, "card": card, "summary": "s"})
        self.assertProblem(out, "3 cards applied")

    def test_garbage(self):
        for result in (None, [], {"mls_id": BEFORE["mls_id"]}, {**abstain(), "changes": "none"},
                       {**abstain(), "unit": {**BEFORE, "tasks": [1, 2]}}):
            with self.subTest(result=result):
                self.assertTrue(problems(result))


class Trace(unittest.TestCase):
    TRACE = [{"mls_id": "MLS-PERSUADE-02", "step": s, "source_locator": f"para {s}"} for s in range(1, 5)]

    def test_added_step_traces_to_its_card(self):
        trace = opt.unit_trace(BEFORE, prompt_example(), self.TRACE)
        self.assertEqual(trace[:4], self.TRACE)
        self.assertEqual(trace[4], {"mls_id": "MLS-PERSUADE-02", "step": 5, "card": "CL-05", "change": "added"})

    def test_modified_step_keeps_its_source_and_adds_the_card(self):
        trace = opt.unit_trace(BEFORE, modified(), self.TRACE)
        step2 = [e for e in trace if e["step"] == 2]
        self.assertEqual(step2, [self.TRACE[1], {"mls_id": "MLS-PERSUADE-02", "step": 2, "card": "CL-04",
                                                 "change": "modified"}])

    def test_merge_trace_replaces_only_the_retraced_unit(self):
        other = {"mls_id": "MLS-PERSUADE-01", "step": 1, "source_locator": "intro"}
        merged = opt.merge_trace([other] + self.TRACE, {"MLS-PERSUADE-02": [{"mls_id": "MLS-PERSUADE-02", "step": 1}]})
        self.assertEqual(merged, [other, {"mls_id": "MLS-PERSUADE-02", "step": 1}])


if __name__ == "__main__":
    unittest.main()
