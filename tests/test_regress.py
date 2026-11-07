"""The regression harness's expectations, checked on synthetic saved runs (no model calls)."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from lsb import regress

ROOT = Path(__file__).resolve().parents[1]
VALID = json.loads((ROOT / "tests/fixtures/hydrology-valid.json").read_text(encoding="utf-8"))

CASE = {"name": "demo", "source": "tests/fixtures/hydrology-source.md", "ref": "x",
        "expect": {"status": "pass", "max_units": 4, "forbidden": ["Kisumu", "S/"], "required": ["rain"],
                   "min_source_flags": 1, "stage_may_not_apply": ["participatory_budgeting"]}}


def save_run(root, sequence=VALID, **summary):
    run = Path(root) / "demo"
    run.mkdir(parents=True)
    (run / "sequence.json").write_text(json.dumps(sequence), encoding="utf-8")
    base = {"status": "pass", "attempts": 1, "cards_g21": "pass", "source_flags": [{"where": "x"}],
            "usage": [{"input": 10, "output": 3, "cache_read": 4, "cache_write": 1},
                      {"input": 20, "output": 7}],
            "optimisation": {"participatory_budgeting": {"units": {"A": {"status": "abstained"}}}}}
    base.update(summary)
    (run / "summary.json").write_text(json.dumps(base), encoding="utf-8")
    return run


def failed(result):
    return [c["check"] for c in result["checks"] if not c["ok"]]


class Evaluate(unittest.TestCase):
    def test_a_good_run_meets_every_expectation(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = regress.evaluate(CASE, save_run(tmp))
        self.assertTrue(r["ok"], failed(r))
        self.assertEqual((r["stats"]["tokens_in"], r["stats"]["tokens_out"]), (35, 10))
        self.assertEqual(r["stats"]["calls"], 2)

    def test_forbidden_term_anywhere_in_the_sequence(self):
        seq = json.loads(json.dumps(VALID))
        seq["mls_units"][1]["tasks"][0]["action"] += " Prices are in S/ at the Kisumu market."
        with tempfile.TemporaryDirectory() as tmp:
            r = regress.evaluate(CASE, save_run(tmp, seq))
        self.assertEqual(failed(r), ["absent: Kisumu", "absent: S/"])

    def test_forbidden_terms_match_whole_words_only(self):
        case = {**CASE, "expect": {**CASE["expect"], "forbidden": ["tablet"]}}
        seq = json.loads(json.dumps(VALID))
        seq["mls_units"][0]["tasks"][0]["action"] += " Use the stone tablets of history."
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(regress.evaluate(case, save_run(tmp, seq))["ok"])

    def test_missing_required_term(self):
        case = {**CASE, "expect": {**CASE["expect"], "required": ["quadrat"]}}
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(failed(regress.evaluate(case, save_run(tmp))), ["present: quadrat"])

    def test_status_cards_flags_and_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = regress.evaluate(CASE, save_run(tmp, status="revise_exhausted", source_flags=[],
                                                optimisation={"participatory_budgeting": {"units": {
                                                    "A": {"status": "applied", "cards": ["PB-01"]}}}}))
        self.assertEqual(failed(r), ["status", "source flags", "participatory_budgeting abstains"])

    def test_g21_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(failed(regress.evaluate(CASE, save_run(tmp, cards_g21=["bad"]))), ["cards G21"])

    def test_missing_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = regress.evaluate(CASE, Path(tmp) / "nothing")
        self.assertFalse(r["ok"])


class Cli(unittest.TestCase):
    def test_run_case_forwards_extra_args_to_lsb_run(self):
        seen = {}

        def fake_run(cmd, **kw):
            seen["cmd"] = cmd
        with tempfile.TemporaryDirectory() as tmp:
            regress.run_case(CASE, Path(tmp), ["--backend", "muse", "--model", "m"], runner=fake_run)
        self.assertEqual(seen["cmd"][-4:], ["--backend", "muse", "--model", "m"])

    def test_check_mode_writes_a_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_run(tmp)
            cases = Path(tmp) / "cases.json"
            cases.write_text(json.dumps({"cases": [CASE]}), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                code = regress.main(["--check", tmp, "--cases", str(cases)])
            self.assertEqual(code, 0)
            self.assertIn("| demo | PASS |", (Path(tmp) / "report.md").read_text(encoding="utf-8"))


class Cases(unittest.TestCase):
    def test_every_case_names_an_existing_source_and_unique_name(self):
        cases = regress.load_cases()
        self.assertEqual(len({c["name"] for c in cases}), len(cases))
        for c in cases:
            with self.subTest(case=c["name"]):
                self.assertTrue((ROOT / c["source"]).exists())
                self.assertTrue(c["ref"])

    def test_every_source_fixture_has_a_case(self):
        sources = {f"tests/fixtures/{p.name}" for p in (ROOT / "tests/fixtures").glob("*-source.md")}
        self.assertEqual(sources, {c["source"] for c in regress.load_cases()})


if __name__ == "__main__":
    unittest.main()
