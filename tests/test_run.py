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

    def __init__(self, decompose, critic, cl=(), pb=()):
        self.script = {"decompose": list(decompose), "critic": list(critic), "cl": list(cl), "pb": list(pb)}
        self.calls = []

    def complete(self, system, user):
        text = system[0]["text"]
        stage = ("decompose" if "Input Decomposition Layer" in text
                 else "cl" if "Connected Learning stage" in text
                 else "pb" if "Participatory Budgeting stage" in text else "critic")
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

    def test_reject_reverts_every_edit(self):
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("REJECT")], [cl_reply(U0), cl_reply(U1)])
        r = self.go(m)
        self.assertEqual((r.status, r.sequence), ("pass", VALID))
        self.assertEqual(set(self.units(r).values()), {"reverted"})

    def test_issue_outside_the_edited_units_reverts_every_edit(self):
        other = {**CL_ISSUE, "where": "mls_units[1].tasks[0]"}
        m = FakeModel([decomposed(VALID)], [critic("PASS"), critic("REVISE", [other])],
                      [cl_reply(U0), cl_reply(U1, False)])
        r = self.go(m)
        self.assertEqual(r.sequence, VALID)
        self.assertEqual(self.units(r)["MLS-HYDRO-01"], "reverted")

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
             "stop_reason": "end_turn", "total_cost_usd": 0.01,
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


if __name__ == "__main__":
    unittest.main()
