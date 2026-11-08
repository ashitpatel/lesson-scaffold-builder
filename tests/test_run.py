"""Pipeline routing, tested with a scripted fake model (no network, no key)."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from lsb import run

FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID = json.loads((FIXTURES / "hydrology-valid.json").read_text(encoding="utf-8"))
SPEC = json.loads((FIXTURES / "hydrology-spec.json").read_text(encoding="utf-8"))
SOURCE = run.Source(text=(FIXTURES / "hydrology-source.md").read_text(encoding="utf-8"),
                    ref="Chapter 4 - Basic Hydrology Framework")


def decomposed(sequence):
    return json.dumps({"sequence": sequence, "source_trace": [], "environment_assumptions": [],
                       "deferred_segments": [], "decompose_warnings": []})


def critic(verdict, issues=()):
    checks = [{"id": f"G{i:02d}", "status": "pass", "issues": []} for i in range(1, 22)]
    if issues:
        checks[4] = {"id": "G05", "status": "fail", "issues": list(issues)}
    return json.dumps({"verdict": verdict, "checks": checks, "notes": "n"})


ISSUE = {"severity": "blocker", "source": "judgement", "where": "mls_units[0].tasks[2]",
         "problem": "role does not fit the action", "fix": "make it a Lead_Educator step"}


class FakeModel:
    """Replies with the next scripted text for the stage named by the system prompt."""

    def __init__(self, decompose, critic, cl=(), pb=(), eb=()):
        self.script = {"decompose": list(decompose), "critic": list(critic), "cl": list(cl), "pb": list(pb),
                       "eb": list(eb)}
        self.calls = []

    def complete(self, system, user):
        text = system[0]["text"]
        stage = ("decompose" if "Input Decomposition Layer" in text
                 else "cl" if "Connected Learning stage" in text
                 else "pb" if "Participatory Budgeting stage" in text
                 else "eb" if "Evidence-Based stage" in text else "critic")
        self.calls.append((stage, user))
        reply = self.script[stage].pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply, {"model": "fake", "stop_reason": "end_turn", "input": 10, "output": 5,
                       "cache_read": 0, "cache_write": 0}


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, model, **kw):
        return run.run_pipeline(SOURCE, model, self.out, **kw)

    def stages(self, model):
        return [s for s, _ in model.calls]

    def test_pass_first_time(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")])
        r = self.go(m)
        self.assertEqual((r.status, r.attempts), ("pass", 1))
        self.assertEqual(self.stages(m), ["decompose", "critic"])
        self.assertEqual(json.loads((self.out / "sequence.json").read_text()), VALID)
        for name in ("01-decompose.json", "01-validator.json", "01-critic.json", "summary.json"):
            self.assertTrue((self.out / name).exists(), name)

    def test_critic_gets_the_validator_report_for_this_sequence(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")])
        self.go(m)
        user = m.calls[1][1]
        self.assertIn("<VALIDATOR_REPORT>", user)
        self.assertIn('"passed": true', user)
        self.assertIn("MLS-HYDRO-02", user)

    def test_revise_sends_issues_and_previous_output_back(self):
        m = FakeModel([decomposed(VALID), decomposed(VALID)], [critic("REVISE", [ISSUE]), critic("PASS")])
        r = self.go(m)
        self.assertEqual((r.status, r.attempts), ("pass", 2))
        second = m.calls[2][1]
        self.assertIn("role does not fit the action", second.split("<CRITIC_FEEDBACK>")[1])
        self.assertIn("MLS-HYDRO-01", second.split("<PREVIOUS_OUTPUT>")[1])
        first = m.calls[0][1]
        self.assertIn("<CRITIC_FEEDBACK>\n(none)", first)

    def test_critic_pass_on_failing_code_checks_is_overridden(self):
        m = FakeModel([decomposed(SPEC), decomposed(VALID)], [critic("PASS"), critic("PASS")])
        r = self.go(m)
        self.assertEqual((r.status, r.attempts), ("pass", 2))
        self.assertTrue(any("treated as REVISE" in n for n in r.notes))
        # The code failures the critic didn't report still reach decompose.
        feedback = m.calls[2][1].split("<CRITIC_FEEDBACK>")[1]
        for cid in ("D03", "D04", "D09"):
            self.assertIn(cid, feedback)

    def test_critic_sees_previous_issues_only_on_a_revision(self):
        m = FakeModel([decomposed(VALID), decomposed(VALID)], [critic("REVISE", [ISSUE]), critic("PASS")])
        self.go(m)
        self.assertIn("<PREVIOUS_ISSUES>\n(none)", m.calls[1][1])
        self.assertIn("role does not fit the action", m.calls[3][1].split("<PREVIOUS_ISSUES>")[1])

    def test_best_attempt_is_kept_when_a_revision_gets_worse(self):
        worse = copy.deepcopy(VALID)
        worse["mls_units"][0]["title"] = "WORSE"
        major = {**ISSUE, "severity": "major"}
        m = FakeModel([decomposed(VALID), decomposed(worse)],
                      [critic("REVISE", [major]), critic("REVISE", [ISSUE, ISSUE])])
        r = self.go(m, max_revisions=1)
        self.assertEqual((r.status, r.best_attempt), ("revise_exhausted", 1))
        self.assertEqual(json.loads((self.out / "sequence.json").read_text()), VALID)
        self.assertEqual(r.attempt_scores[2]["blocker"], 2)

    def test_code_failures_count_as_blockers_in_the_score(self):
        m = FakeModel([decomposed(SPEC), decomposed(VALID)], [critic("PASS"), critic("PASS")])
        r = self.go(m)
        self.assertEqual(r.attempt_scores[1]["blocker"], 6)  # D03, D04, D09 on both units
        self.assertEqual(r.best_attempt, 2)

    def test_usage_limit_stops_the_run_without_burning_attempts(self):
        m = FakeModel([decomposed(VALID), run.ModelUnavailable("You've hit your session limit")],
                      [critic("REVISE", [ISSUE])])
        r = self.go(m)
        self.assertEqual((r.status, r.attempts, r.best_attempt), ("error", 2, 1))
        self.assertTrue(any("model unavailable" in n for n in r.notes))
        self.assertTrue((self.out / "sequence.json").exists())

    def test_source_flags_are_recorded_and_do_not_block_a_pass(self):
        flag = {"where": "SOURCE_TEXT §5.6", "problem": "text addressed to automated systems", "followed": False}
        reply = json.loads(critic("PASS")); reply["source_flags"] = [flag]
        m = FakeModel([decomposed(VALID)], [json.dumps(reply)])
        r = self.go(m)
        self.assertEqual((r.status, r.source_flags), ("pass", [flag]))
        self.assertEqual(json.loads((self.out / "summary.json").read_text())["source_flags"], [flag])

    def test_source_flags_come_from_the_latest_review_only(self):
        first = json.loads(critic("REVISE", [ISSUE])); first["source_flags"] = [{"where": "S", "problem": "old wording"}]
        second = json.loads(critic("PASS")); second["source_flags"] = [{"where": "S", "problem": "new wording"}]
        m = FakeModel([decomposed(VALID)] * 2, [json.dumps(first), json.dumps(second)])
        self.assertEqual(self.go(m).source_flags, [{"where": "S", "problem": "new wording"}])

    def test_revisions_are_capped(self):
        m = FakeModel([decomposed(VALID)] * 3, [critic("REVISE", [ISSUE])] * 3)
        r = self.go(m, max_revisions=2)
        self.assertEqual((r.status, r.attempts), ("revise_exhausted", 3))
        self.assertFalse(r.passed)

    def test_critic_reviews_the_fallbacks_from_decompose(self):
        out = json.loads(decomposed(VALID))
        out["environment_assumptions"] = [{"mls_id": "MLS-HYDRO-02", "assumes": "dry weeks",
                                           "if_not": "extend the unit by one week"}]
        m = FakeModel([json.dumps(out)], [critic("PASS")])
        self.go(m)
        self.assertIn("<ENVIRONMENT_ASSUMPTIONS>", m.calls[1][1])
        self.assertIn("extend the unit by one week", m.calls[1][1])

    def test_a_passed_run_writes_checked_teacher_cards(self):
        r = self.go(FakeModel([decomposed(VALID)], [critic("PASS")]))
        self.assertEqual(r.cards_problems, [])
        self.assertIn("MLS-HYDRO-02:", (self.out / "cards.txt").read_text(encoding="utf-8"))
        self.assertTrue((self.out / "cards.html").exists())
        self.assertEqual(json.loads((self.out / "summary.json").read_text())["cards_g21"], "pass")

    def test_a_run_that_did_not_pass_writes_no_cards(self):
        r = self.go(FakeModel([decomposed(VALID)] * 3, [critic("REVISE", [ISSUE])] * 3))
        self.assertIsNone(r.cards_problems)
        self.assertFalse((self.out / "cards.txt").exists())

    def test_reject_restarts_once_then_stops(self):
        m = FakeModel([decomposed(VALID)] * 2, [critic("REJECT"), critic("REJECT")])
        r = self.go(m)
        self.assertEqual((r.status, r.attempts), ("rejected", 2))
        self.assertIn("<PREVIOUS_OUTPUT>\n(none)", m.calls[2][1])  # fresh start, not a revision

    def test_reject_then_pass(self):
        m = FakeModel([decomposed(VALID)] * 2, [critic("REJECT"), critic("PASS")])
        self.assertEqual(self.go(m).status, "pass")

    def test_unparseable_decompose_is_retried_with_format_feedback(self):
        m = FakeModel(["Sorry, here is a summary instead.", decomposed(VALID)], [critic("PASS")])
        r = self.go(m)
        self.assertEqual((r.status, r.attempts), ("pass", 2))
        self.assertIn("Return only the JSON object", m.calls[1][1])

    def test_missing_sequence_key_is_retried(self):
        m = FakeModel([json.dumps(VALID), decomposed(VALID)], [critic("PASS")])
        r = self.go(m)
        self.assertEqual((r.status, r.attempts), ("pass", 2))
        self.assertIn("'sequence'", m.calls[1][1])

    def test_bad_critic_verdict_stops_with_error(self):
        m = FakeModel([decomposed(VALID)], [json.dumps({"verdict": "LGTM"})])
        self.assertEqual(self.go(m).status, "error")

    def test_refusal_from_critic_stops_with_error(self):
        m = FakeModel([decomposed(VALID)], [run.StageError("refusal: None")])
        r = self.go(m)
        self.assertEqual(r.status, "error")
        self.assertTrue((self.out / "summary.json").exists())


def cl_reply(unit, apply=True, card="CL-05"):
    """A stage reply for `unit`: one added step under `card`, or an abstain."""
    out = copy.deepcopy(unit)
    changes = []
    if apply:
        n = len(out["tasks"]) + 1
        out["tasks"].append({"step": n, "role": "Lead_Educator",
                             "action": f"Run the {card} activity for 10 minutes with the whole class."})
        changes = [{"step": n, "change": "added", "replaces_step": None, "card": card, "summary": "s"}]
    return json.dumps({"mls_id": unit["mls_id"], "decision": "APPLY" if apply else "ABSTAIN", "reason": "r",
                       "credit": [], "unit": out, "changes": changes, "deferred": []})


U0, U1 = VALID["mls_units"]
CL_ISSUE = {"severity": "major", "source": "judgement", "where": "mls_units[0].tasks[4]",
            "problem": "the showcase needs the educator present", "fix": "say the educator stays"}


class ConnectedLearning(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, model, **kw):
        return run.run_pipeline(SOURCE, model, self.out, stages=("cl",), **kw)

    def units(self, r, stage="connected_learning"):
        return {uid: u["status"] for uid, u in r.optimisation[stage]["units"].items()}

    def test_off_unless_asked(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")])
        r = run.run_pipeline(SOURCE, m, self.out)
        self.assertEqual([s for s, _ in m.calls], ["decompose", "critic"])
        self.assertIsNone(r.optimisation)

    def test_not_run_when_decompose_did_not_pass(self):
        m = FakeModel([decomposed(VALID)] * 3, [critic("REVISE", [ISSUE])] * 3)
        r = self.go(m)
        self.assertNotIn("cl", [s for s, _ in m.calls])
        self.assertIsNone(r.optimisation)

    def test_all_abstain_skips_the_second_review(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")], [cl_reply(U0, False), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual([s for s, _ in m.calls], ["decompose", "critic", "cl", "cl"])
        self.assertEqual(self.units(r), {"MLS-HYDRO-01": "abstained", "MLS-HYDRO-02": "abstained"})
        self.assertEqual(r.sequence, VALID)

    def test_applied_edit_is_reviewed_and_kept(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("PASS")], [cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual(r.status, "pass")
        self.assertEqual(self.units(r), {"MLS-HYDRO-01": "applied", "MLS-HYDRO-02": "abstained"})
        self.assertEqual(len(r.sequence["mls_units"][0]["tasks"]), 5)
        self.assertEqual(r.sequence["mls_units"][1], U1)
        review = m.calls[-1][1]
        self.assertIn("CL-G1 Mastery unchanged", review)  # the cards go to the critic
        self.assertIn('"card": "CL-05"', review)  # and the trace names the card
        saved = json.loads((self.out / "decomposed-sequence.json").read_text(encoding="utf-8"))
        self.assertEqual(saved, VALID)
        self.assertEqual(len(json.loads((self.out / "sequence.json").read_text())["mls_units"][0]["tasks"]), 5)

    def test_unit_with_issues_is_revised_with_feedback(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("REVISE", [CL_ISSUE]), critic("PASS")],
                      [cl_reply(U0), cl_reply(U1, False), cl_reply(U0)])
        r = self.go(m)
        self.assertEqual([s for s, _ in m.calls], ["decompose", "critic", "cl", "cl", "critic", "cl", "critic"])
        revision = m.calls[5][1]
        self.assertIn("the showcase needs the educator present", revision)
        self.assertIn("the showcase needs the educator present", m.calls[6][1])  # previous issues to the critic
        self.assertEqual(self.units(r)["MLS-HYDRO-01"], "applied")
        self.assertEqual(len(r.sequence["mls_units"][0]["tasks"]), 5)

    def test_unit_still_failing_is_reverted_and_the_run_still_passes(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("REVISE", [CL_ISSUE]), critic("REVISE", [CL_ISSUE])],
                      [cl_reply(U0), cl_reply(U1, False), cl_reply(U0)])
        r = self.go(m)
        self.assertEqual(r.status, "pass")
        self.assertEqual(self.units(r)["MLS-HYDRO-01"], "reverted")
        self.assertEqual(r.sequence, VALID)

    def test_failing_unit_is_reverted_but_other_edits_are_kept(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("REVISE", [CL_ISSUE]), critic("REVISE", [CL_ISSUE])],
                      [cl_reply(U0), cl_reply(U1), cl_reply(U0)])
        r = self.go(m)
        self.assertEqual(self.units(r), {"MLS-HYDRO-01": "reverted", "MLS-HYDRO-02": "applied"})
        self.assertEqual(r.sequence["mls_units"][0], U0)
        self.assertEqual(len(r.sequence["mls_units"][1]["tasks"]), 5)

    def test_edit_breaking_its_limits_is_retried_then_dropped(self):
        bad = json.loads(cl_reply(U0))
        bad["unit"]["dependencies"] = ["MLS-HYDRO-02"]
        m = FakeModel([decomposed(VALID)], [critic("PASS")], [json.dumps(bad), json.dumps(bad), cl_reply(U1, False)])
        r = self.go(m)
        self.assertIn("unit.dependencies changed", m.calls[3][1])  # the retry carries the problem
        self.assertEqual(self.units(r)["MLS-HYDRO-01"], "edit_rejected")
        self.assertEqual(r.sequence, VALID)

    def test_stage_review_does_not_get_the_fallbacks(self):
        out = json.loads(decomposed(VALID))
        out["environment_assumptions"] = [{"mls_id": U0["mls_id"], "assumes": "a", "if_not": "fallback text"}]
        m = FakeModel([json.dumps(out)], [critic("PASS"), critic("PASS")], [cl_reply(U0), cl_reply(U1, False)])
        self.go(m)
        self.assertIn("fallback text", m.calls[1][1])
        self.assertNotIn("fallback text", m.calls[-1][1])
        self.assertIn("<ENVIRONMENT_ASSUMPTIONS>\n(none)", m.calls[-1][1])

    def test_reject_reverts_every_edit(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("REJECT")], [cl_reply(U0), cl_reply(U1)])
        r = self.go(m)
        self.assertEqual((r.status, r.sequence), ("pass", VALID))
        self.assertEqual(set(self.units(r).values()), {"reverted"})

    def repaired(self, unit_index, step_index, text):
        seq = copy.deepcopy(VALID)
        seq["mls_units"][0] = json.loads(cl_reply(U0))["unit"]  # the kept CL edit
        seq["mls_units"][unit_index]["tasks"][step_index]["action"] = text
        return decomposed(seq)

    def test_issue_outside_the_edited_units_keeps_the_edit_and_is_repaired(self):
        other = {**CL_ISSUE, "where": "mls_units[1].tasks[0]"}
        m = FakeModel([decomposed(VALID), self.repaired(1, 0, "Fixed step.")],
                      [critic("PASS"), critic("REVISE", [other]), critic("PASS")],
                      [cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual([s for s, _ in m.calls], ["decompose", "critic", "cl", "cl", "critic", "decompose", "critic"])
        self.assertEqual(r.status, "pass")
        self.assertEqual(self.units(r)["MLS-HYDRO-01"], "applied")  # not blamed on CL
        self.assertEqual(len(r.sequence["mls_units"][0]["tasks"]), 5)
        self.assertEqual(r.sequence["mls_units"][1]["tasks"][0]["action"], "Fixed step.")
        self.assertEqual(r.late_issues[0]["where"], "mls_units[1].tasks[0]")
        self.assertIn("the showcase needs the educator present", m.calls[5][1])  # the repair gets the issue
        self.assertTrue((self.out / "cards.txt").exists())

    def test_issue_on_an_unchanged_step_of_an_edited_unit_is_not_the_stages(self):
        unchanged = {**CL_ISSUE, "where": "mls_units[0].tasks[1]"}
        m = FakeModel([decomposed(VALID), self.repaired(0, 1, "Fixed step.")],
                      [critic("PASS"), critic("REVISE", [unchanged]), critic("PASS")],
                      [cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual(self.units(r)["MLS-HYDRO-01"], "applied")
        self.assertEqual(r.sequence["mls_units"][0]["tasks"][1]["action"], "Fixed step.")
        self.assertEqual(r.status, "pass")

    def test_a_later_review_without_source_flags_keeps_the_earlier_ones(self):
        first = json.loads(critic("PASS"))
        first["source_flags"] = [{"where": "§1", "problem": "unsafe trip"}]
        later = json.loads(critic("PASS"))
        later["source_flags"] = []  # the live failure: an empty list, not a missing key
        m = FakeModel([decomposed(VALID)], [json.dumps(first), json.dumps(later)], [cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual(r.source_flags, [{"where": "§1", "problem": "unsafe trip"}])

    def test_unrepairable_late_issue_means_the_run_does_not_pass(self):
        other = {**CL_ISSUE, "where": "mls_units[1].tasks[0]"}
        m = FakeModel([decomposed(VALID), self.repaired(1, 0, "Try 1."), self.repaired(1, 0, "Try 2.")],
                      [critic("PASS"), critic("REVISE", [other]), critic("REVISE", [other]), critic("REVISE", [other])],
                      [cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual(r.status, "issues_open")
        self.assertFalse((self.out / "cards.txt").exists())
        self.assertTrue((self.out / "late-issues.json").exists())
        self.assertEqual([x["verdict"] for x in r.repair["rounds"]], ["REVISE", "REVISE"])

    def test_repair_that_changes_unflagged_steps_is_rejected(self):
        other = {**CL_ISSUE, "where": "mls_units[1].tasks[0]"}
        bad = json.loads(self.repaired(1, 0, "Fixed step."))
        bad["sequence"]["mls_units"][1]["tasks"][2]["action"] = "Sneaky change."
        m = FakeModel([decomposed(VALID), json.dumps(bad), json.dumps(bad)],
                      [critic("PASS"), critic("REVISE", [other])], [cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual(r.status, "issues_open")
        self.assertIn("mls_units[1].tasks[2] changed but no issue points at it", m.calls[6][1])

    def test_usage_limit_keeps_the_decomposed_sequence(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")], [run.ModelUnavailable("You've hit your session limit")])
        r = self.go(m)
        self.assertEqual((r.status, r.sequence), ("pass", VALID))


class StagesInOrder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, model):
        return run.run_pipeline(SOURCE, model, self.out, stages=("cl", "pb"))

    def test_pb_works_on_the_cl_output_and_the_critic_sees_both_card_sets(self):
        cl0 = json.loads(cl_reply(U0))["unit"]
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("PASS"), critic("PASS")],
                      [cl_reply(U0), cl_reply(U1, False)], [cl_reply(cl0, True, "PB-04"), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual([s for s, _ in m.calls], ["decompose", "critic", "cl", "cl", "critic", "pb", "pb", "critic"])
        self.assertIn("Run the CL-05 activity", m.calls[5][1])  # PB got the CL-edited unit
        last_review = m.calls[-1][1]
        self.assertIn("CL-G1 Mastery unchanged", last_review)
        self.assertIn("PB-G1 Numbers only", last_review)
        self.assertEqual([t["action"][:16] for t in r.sequence["mls_units"][0]["tasks"][-2:]],
                         ["Run the CL-05 ac", "Run the PB-04 ac"])
        self.assertEqual(r.optimisation["participatory_budgeting"]["units"]["MLS-HYDRO-01"]["status"], "applied")
        trace = json.loads((self.out / "source_trace.json").read_text(encoding="utf-8"))
        self.assertEqual({e.get("card") for e in trace if e.get("card")}, {"CL-05", "PB-04"})

    def test_pb_may_not_use_cl_cards(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")], [cl_reply(U0, False), cl_reply(U1, False)],
                      [cl_reply(U0), cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertIn("unknown card(s) CL-05", m.calls[5][1])
        self.assertEqual(r.optimisation["participatory_budgeting"]["units"]["MLS-HYDRO-01"]["status"], "edit_rejected")
        self.assertEqual(r.sequence, VALID)

    def test_pb_abstaining_everywhere_keeps_the_cl_result(self):
        cl0 = json.loads(cl_reply(U0))["unit"]
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("PASS")],
                      [cl_reply(U0), cl_reply(U1, False)], [cl_reply(cl0, False), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual(len(r.sequence["mls_units"][0]["tasks"]), 5)
        self.assertEqual(set(self.units_pb(r).values()), {"abstained"})

    def units_pb(self, r):
        return {u: x["status"] for u, x in r.optimisation["participatory_budgeting"]["units"].items()}


class AllStages(unittest.TestCase):
    def test_eb_runs_first_then_cl_then_pb(self):
        with tempfile.TemporaryDirectory() as tmp:
            eb0 = json.loads(cl_reply(U0, True, "EB-01"))["unit"]
            m = FakeModel([decomposed(VALID)], [critic("PASS")] * 3,
                          cl=[cl_reply(eb0, False), cl_reply(U1, False)],
                          pb=[cl_reply(eb0, False), cl_reply(U1, False)],
                          eb=[cl_reply(U0, True, "EB-01"), cl_reply(U1, False)])
            r = run.run_pipeline(SOURCE, m, Path(tmp) / "run", stages=run.STAGE_ORDER)
            self.assertEqual([s for s, _ in m.calls],
                             ["decompose", "critic", "eb", "eb", "critic", "cl", "cl", "pb", "pb"])
            self.assertEqual(list(r.optimisation), ["evidence_based", "connected_learning", "participatory_budgeting"])
            self.assertIn("Run the EB-01 activity", r.sequence["mls_units"][0]["tasks"][-1]["action"])
            self.assertIn("Evidence-Based, EB-01 Retrieval Practice", (Path(tmp) / "run/cards.txt").read_text())


class Choices(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"

    def tearDown(self):
        self.tmp.cleanup()

    def file_prompter(self, answers):
        f = Path(self.tmp.name) / "answers.json"
        f.write_text(json.dumps(answers), encoding="utf-8")
        return run.ask.FilePrompter(f)

    def test_max_units_forces_a_revise(self):
        three = copy.deepcopy(VALID)
        extra = copy.deepcopy(VALID["mls_units"][1])
        extra["mls_id"] = "MLS-HYDRO-03"
        three["mls_units"].append(extra)
        m = FakeModel([decomposed(three)] * 3, [critic("PASS")] * 3)
        r = run.run_pipeline(SOURCE, m, self.out, prompter=self.file_prompter({"max_units": 2}))
        self.assertEqual(r.status, "revise_exhausted")
        self.assertTrue(any("maximum of 2" in n for n in r.notes), r.notes)
        saved = json.loads((self.out / "choices.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["max_units"], 2)
        self.assertEqual(saved["focus"], "auto")

    def test_excluded_framework_is_never_called_or_asked(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")])
        r = run.run_pipeline(SOURCE, m, self.out, stages=("cl",),
                             prompter=self.file_prompter({"frameworks_excluded": ["connected_learning"]}))
        self.assertEqual([s for s, _ in m.calls], ["decompose", "critic"])
        self.assertEqual(r.status, "pass")
        saved = json.loads((self.out / "choices.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["frameworks_excluded"], ["connected_learning"])
        self.assertNotIn("connected_learning_cards", saved)

    def test_unknown_exclusion_falls_back_to_none(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")], [cl_reply(U0, False), cl_reply(U1, False)])
        run.run_pipeline(SOURCE, m, self.out, stages=("cl",),
                         prompter=self.file_prompter({"frameworks_excluded": ["nonsense"]}))
        self.assertIn("cl", [s for s, _ in m.calls])
        saved = json.loads((self.out / "choices.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["frameworks_excluded"], [])

    def test_single_module_passes_a_full_span_unit(self):
        one = copy.deepcopy(VALID)
        one["mls_units"] = one["mls_units"][:1]
        one["mls_units"][0]["duration_weeks"] = 6
        m = FakeModel([decomposed(one)], [critic("PASS")])
        r = run.run_pipeline(SOURCE, m, self.out, prompter=self.file_prompter({"single_module": True}))
        self.assertEqual(r.status, "pass")
        saved = json.loads((self.out / "choices.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["single_module"], True)
        self.assertEqual(saved["max_units"], 1)
        self.assertIsNone(saved["max_weeks"])

    def test_max_weeks_forces_a_revise(self):
        m = FakeModel([decomposed(VALID)] * 3, [critic("PASS")] * 3)
        r = run.run_pipeline(SOURCE, m, self.out, prompter=self.file_prompter({"max_weeks": 2}))
        self.assertEqual(r.status, "revise_exhausted")
        self.assertTrue(any("maximum of 2 weeks" in n for n in r.notes), r.notes)

    def test_focus_reaches_decompose_values(self):
        self.assertEqual(run.decompose_values(SOURCE)["USER_FOCUS"], "auto")
        self.assertEqual(run.decompose_values(SOURCE, focus="by skill")["USER_FOCUS"], "by skill")

    def test_stage_allowlist_drops_a_disallowed_card(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS")],
                      [cl_reply(U0), cl_reply(U0), cl_reply(U1, False)])
        r = run.run_pipeline(SOURCE, m, self.out, stages=("cl",),
                             prompter=self.file_prompter({"connected_learning_cards": ["CL-02"]}))
        self.assertIn("unknown card", m.calls[3][1])  # the retry carries the problem
        self.assertEqual(r.optimisation["connected_learning"]["units"]["MLS-HYDRO-01"]["status"], "edit_rejected")
        self.assertEqual(r.sequence, VALID)
        saved = json.loads((self.out / "choices.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["connected_learning_cards"], ["CL-02"])


class Requests(unittest.TestCase):
    def test_every_placeholder_is_supplied(self):
        values = {
            run.DECOMPOSE: run.decompose_values(SOURCE),
            run.CRITIC: run.critic_values(SOURCE, {"sequence": VALID}, run.v.validate(VALID)),
            **{st.prompt: run.stage_values(st, SOURCE, {"sequence": VALID}, "MLS-HYDRO-01")
               for st in run.STAGES.values()},
        }
        for prompt, vals in values.items():
            with self.subTest(prompt=prompt):
                self.assertEqual(run.build_request(prompt, vals)[2], [])
                self.assertEqual(sorted(vals), run.prompt_placeholders(prompt))

    def test_extract_json_tolerates_fences_and_prose(self):
        self.assertEqual(run.extract_json('Here:\n```json\n{"a": {"b": 1}}\n```'), {"a": {"b": 1}})
        with self.assertRaises(run.StageError):
            run.extract_json("no json here")

    def test_dry_run_passes(self):
        import io
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            code = run.main([str(FIXTURES / "hydrology-source.md"), "--ref", "x", "--dry-run"])
        self.assertEqual(code, 0)


class ClaudeCodeBackend(unittest.TestCase):
    """ClaudeCodeModel with a fake subprocess runner: no CLI call is made."""

    def model(self, stdout, returncode=0, stderr=""):
        import subprocess
        self.seen = {}

        def fake_run(cmd, **kw):
            self.seen = {"cmd": cmd, **kw}
            self.seen["system"] = Path(cmd[cmd.index("--system-prompt-file") + 1]).read_text()
            return subprocess.CompletedProcess(cmd, returncode, stdout, stderr)
        return run.ClaudeCodeModel(effort="high", runner=fake_run)

    def ok(self, result='{"a": 1}', **over):
        d = {"type": "result", "subtype": "success", "is_error": False, "result": result,
             "stop_reason": "end_turn",
             "usage": {"input_tokens": 3, "output_tokens": 4, "cache_read_input_tokens": 5,
                       "cache_creation_input_tokens": 6},
             "modelUsage": {"claude-opus-5-5": {}}}
        d.update(over)
        return json.dumps(d)

    def test_success_returns_text_and_usage(self):
        m = self.model(self.ok())
        text, usage = m.complete([{"type": "text", "text": "SYSTEM"}], "USER")
        self.assertEqual(text, '{"a": 1}')
        self.assertEqual((usage["input"], usage["output"], usage["cache_read"], usage["cache_write"]), (3, 4, 5, 6))
        self.assertEqual(usage["model"], "claude-opus-5-5")
        cmd = self.seen["cmd"]
        self.assertEqual(cmd[cmd.index("--tools") + 1], "")
        self.assertEqual(cmd[cmd.index("--model") + 1], "claude-opus-5-5")
        self.assertEqual(cmd[cmd.index("--effort") + 1], "high")
        self.assertEqual(self.seen["input"], "USER")
        self.assertEqual(self.seen["system"], "SYSTEM")

    def test_error_result_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model(self.ok(is_error=True, subtype="error_during_execution")).complete([{"text": "s"}], "u")

    def test_usage_limit_is_model_unavailable(self):
        out = self.ok(is_error=True, subtype="success", result="You've hit your session limit · resets 5:50pm")
        with self.assertRaises(run.ModelUnavailable):
            self.model(out).complete([{"text": "s"}], "u")

    def test_max_tokens_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model(self.ok(stop_reason="max_tokens")).complete([{"text": "s"}], "u")

    def test_unreadable_output_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model("boom", returncode=1).complete([{"text": "s"}], "u")

    def test_not_signed_in_exits(self):
        with self.assertRaises(SystemExit):
            self.model("", returncode=1, stderr="Please run /login to log in").complete([{"text": "s"}], "u")


class MuseBackend(unittest.TestCase):
    """MuseModel with a fake subprocess runner: no CLI call is made."""

    def model(self, stdout, returncode=0, stderr="", **kw):
        import subprocess
        self.seen = {}

        def fake_run(cmd, **call_kw):
            self.seen = {"cmd": cmd, **call_kw}
            self.seen["prompt"] = Path(cmd[cmd.index("--prompt-file") + 1]).read_text()
            return subprocess.CompletedProcess(cmd, returncode, stdout, stderr)
        return run.MuseModel(effort="high", runner=fake_run, **kw)

    def ev(self, payload_type, payload):
        return json.dumps({"payload_type": payload_type, "payload": payload})

    def ok(self, *texts):
        lines = [self.ev("run.model.configured", {"model_id": "muse-spark-1.3"})]
        lines += [self.ev("run.output.delta", {"text": t}) for t in texts or ['{"a": 1}']]
        lines.append(self.ev("run.usage", {"models": [{"model": "muse-spark-1.3", "input_tokens": 30,
                                                       "output_tokens": 4, "cached_tokens": 5}]}))
        return "\n".join(lines) + "\n"

    def test_success_joins_deltas_and_reports_usage(self):
        m = self.model(self.ok('{"a": ', "1}"))
        text, usage = m.complete([{"type": "text", "text": "SYSTEM"}], "USER")
        self.assertEqual(text, '{"a": 1}')
        self.assertEqual((usage["input"], usage["output"], usage["cache_read"]), (30, 4, 5))
        self.assertEqual(usage["model"], "muse-spark-1.3")
        self.assertNotIn("cost_usd_list_price", usage)
        cmd = self.seen["cmd"]
        self.assertNotIn("--model", cmd)
        self.assertEqual(cmd[cmd.index("--reasoning-effort") + 1], "high")
        self.assertEqual(cmd[cmd.index("--max-model-steps") + 1], "1")
        self.assertEqual(self.seen["prompt"], "SYSTEM\n\nUSER")

    def test_model_flag_is_passed_through(self):
        self.model(self.ok(), model="muse-spark-1.3").complete([{"text": "s"}], "u")
        cmd = self.seen["cmd"]
        self.assertEqual(cmd[cmd.index("--model") + 1], "muse-spark-1.3")

    def test_non_json_lines_are_ignored(self):
        m = self.model("muse: workspace root: /tmp/x\n" + self.ok())
        text, _ = m.complete([{"text": "s"}], "u")
        self.assertEqual(text, '{"a": 1}')

    def test_empty_reply_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model(self.ev("run.usage", {"models": []}) + "\n").complete([{"text": "s"}], "u")

    def test_error_exit_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model("", returncode=1, stderr="boom").complete([{"text": "s"}], "u")

    def test_usage_limit_is_model_unavailable(self):
        with self.assertRaises(run.ModelUnavailable):
            self.model("", returncode=1, stderr="rate limit exceeded").complete([{"text": "s"}], "u")

    def test_not_signed_in_exits(self):
        with self.assertRaises(SystemExit):
            self.model("", returncode=1, stderr="not logged in: run `muse login` first").complete(
                [{"text": "s"}], "u")

    def test_timeout_is_a_stage_error(self):
        import subprocess

        def slow(cmd, **kw):
            raise subprocess.TimeoutExpired(cmd, 1200)
        with self.assertRaises(run.StageError):
            run.MuseModel(runner=slow).complete([{"text": "s"}], "u")


class GeminiBackend(unittest.TestCase):
    """GeminiModel with a fake HTTPS opener: no network call is made."""

    def model(self, payload=None, error=None, **kw):
        import urllib.request
        self.seen = {}

        class FakeResponse:
            def __init__(self, body):
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def read(self):
                return json.dumps(self.body).encode("utf-8")

        def fake_opener(req, timeout=None):
            assert isinstance(req, urllib.request.Request)
            self.seen = {"url": req.full_url, "timeout": timeout,
                         "key": req.get_header("X-goog-api-key"),
                         "body": json.loads(req.data.decode("utf-8"))}
            if error is not None:
                raise error
            return FakeResponse(payload)

        kw.setdefault("api_key", "TESTKEY")
        kw.setdefault("effort", "high")
        return run.GeminiModel(opener=fake_opener, **kw)

    def ok(self, *texts, finish="STOP", usage=None):
        return {"candidates": [{"content": {"parts": [{"text": t} for t in texts or ['{"a": 1}']]},
                                "finishReason": finish}],
                "usageMetadata": usage or {"promptTokenCount": 30, "candidatesTokenCount": 4}}

    def test_success_joins_parts_and_reports_usage(self):
        m = self.model(self.ok('{"a": ', "1}"))
        text, usage = m.complete([{"type": "text", "text": "SYSTEM"}], "USER")
        self.assertEqual(text, '{"a": 1}')
        self.assertEqual((usage["input"], usage["output"], usage["cache_read"]), (30, 4, 0))
        self.assertEqual(usage["model"], "gemini-2.5-flash")
        self.assertNotIn("cost_usd_list_price", usage)
        body = self.seen["body"]
        self.assertEqual(body["system_instruction"]["parts"], [{"text": "SYSTEM"}])
        self.assertEqual(body["contents"][0]["parts"], [{"text": "USER"}])
        self.assertEqual(body["generationConfig"]["responseMimeType"], "application/json")
        self.assertEqual(body["generationConfig"]["thinkingConfig"], {"thinkingBudget": 8192})
        self.assertIn("models/gemini-2.5-flash:generateContent", self.seen["url"])
        self.assertEqual(self.seen["key"], "TESTKEY")

    def test_effort_maps_to_thinking_budget(self):
        self.model(self.ok(), effort="low").complete([{"text": "s"}], "u")
        self.assertEqual(self.seen["body"]["generationConfig"]["thinkingConfig"],
                         {"thinkingBudget": 0})

    def test_model_flag_changes_url(self):
        self.model(self.ok(), model="gemini-2.5-pro").complete([{"text": "s"}], "u")
        self.assertIn("models/gemini-2.5-pro:generateContent", self.seen["url"])

    def test_missing_key_exits(self):
        import os
        saved = {k: os.environ.pop(k) for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") if k in os.environ}
        try:
            with self.assertRaises(SystemExit):
                run.GeminiModel(opener=lambda req, timeout=None: None).complete([{"text": "s"}], "u")
        finally:
            os.environ.update(saved)

    def http_error(self, code, message):
        import io
        import urllib.error
        return urllib.error.HTTPError("http://x", code, message, {},
                                      io.BytesIO(json.dumps({"error": {"message": message}}).encode()))

    def test_auth_error_exits(self):
        with self.assertRaises(SystemExit):
            self.model(error=self.http_error(400, "API key not valid")).complete([{"text": "s"}], "u")

    def test_rate_limit_is_model_unavailable(self):
        with self.assertRaises(run.ModelUnavailable):
            self.model(error=self.http_error(429, "quota exceeded")).complete([{"text": "s"}], "u")

    def test_server_error_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model(error=self.http_error(500, "boom")).complete([{"text": "s"}], "u")

    def test_blocked_prompt_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model({"promptFeedback": {"blockReason": "SAFETY"}}).complete([{"text": "s"}], "u")

    def test_no_candidates_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model({"candidates": []}).complete([{"text": "s"}], "u")

    def test_safety_stop_is_a_stage_error(self):
        with self.assertRaises(run.StageError):
            self.model(self.ok("half", finish="SAFETY")).complete([{"text": "s"}], "u")

    def test_max_tokens_stop_is_a_stage_error(self):
        with self.assertRaisesRegex(run.StageError, "max_tokens"):
            self.model(self.ok("half", finish="MAX_TOKENS")).complete([{"text": "s"}], "u")

    def test_timeout_is_a_stage_error(self):
        import urllib.error
        with self.assertRaises(run.StageError):
            self.model(error=urllib.error.URLError(TimeoutError("timed out"))).complete(
                [{"text": "s"}], "u")


class Relocalize(unittest.TestCase):
    """run_relocalize never fails the run, even with degenerate model replies."""

    LOG = {"locale_log": [{"original": "pond", "generic": "small lake",
                            "category": "place"}]}

    def _run(self, proposals, prompter):
        script = iter([self.LOG, {"proposals": proposals}])
        saved = {}
        result = run.RunResult("pass", 1, copy.deepcopy(VALID), Path("."))
        info = run.run_relocalize(
            SOURCE, "Nowhere", result, {"environment_assumptions": []},
            lambda *a: next(script), lambda n, o: saved.update({n: o}),
            prompter, {})
        return result, info, saved

    def test_empty_proposals_keeps_generic(self):
        result, info, _ = self._run([], run.ask.DefaultPrompter())
        self.assertEqual(result.sequence, VALID)
        self.assertEqual(info["applied"], [])
        self.assertTrue(any("no proposals" in n for n in result.notes),
                        result.notes)

    def test_skipped_proposal_keeps_generic(self):
        class Skip:
            def ask(self, choice):
                return ""
        result, info, saved = self._run(
            [{"id": 0, "proposed": "tarn", "reason": "fits"}], Skip())
        self.assertEqual(result.sequence, VALID)
        self.assertEqual(info["applied"], [])
        self.assertEqual(info["skipped"], [0])
        self.assertIn("locale-decisions.json", saved)

    def test_approved_proposal_missing_generic_keeps_generic(self):
        result, info, _ = self._run(
            [{"id": 0, "proposed": "tarn", "reason": "fits"}],
            run.ask.DefaultPrompter())
        self.assertEqual(result.sequence, VALID)
        self.assertEqual(info["applied"], [0])


if __name__ == "__main__":
    unittest.main()
