import copy
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from lsb import validate as v

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def failed(payload):
    return v.validate(payload).failed_ids()


class Fixtures(unittest.TestCase):
    def test_valid_hydrology_passes_everything(self):
        report = v.validate(fixture("hydrology-valid.json"))
        self.assertTrue(report.passed, v.format_text(report))

    def test_spec_hydrology_example_fails_its_own_gate(self):
        # The requirements' sample output has 2 steps per unit and no duration
        # or macro-alignment fields; it is schema-valid but fails these checks.
        self.assertEqual(failed(fixture("hydrology-spec.json")), ["D03", "D04", "D09"])

    def test_schema_file_is_a_valid_2020_12_schema(self):
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(v.load_json(v.SCHEMA_PATH))


class Mutations(unittest.TestCase):
    """Break one thing in the valid fixture and check exactly the right check fails."""

    def setUp(self):
        self.p = fixture("hydrology-valid.json")

    def unit(self, i=0):
        return self.p["mls_units"][i]

    def add_units(self, n):
        for k in range(n):
            u = copy.deepcopy(self.unit(1))
            u["mls_id"] = f"MLS-EXTRA-{k}"
            self.p["mls_units"].append(u)

    def test_six_units_exceed_cap(self):
        self.add_units(4)
        self.assertEqual(failed(self.p), ["D02"])

    def test_five_units_is_at_cap(self):
        self.add_units(3)
        self.assertEqual(failed(self.p), [])

    def test_two_steps_too_few(self):
        del self.unit()["tasks"][2:]
        self.assertEqual(failed(self.p), ["D03"])

    def test_eight_steps_too_many(self):
        tasks = self.unit()["tasks"]
        for s in range(5, 9):
            tasks.append({"step": s, "role": "Lead_Educator", "action": "Extra step."})
        self.assertEqual(failed(self.p), ["D03"])

    def test_duration_outside_window(self):
        self.unit()["duration_weeks"] = 6
        self.assertEqual(failed(self.p), ["D04"])

    def test_duration_missing(self):
        del self.unit()["duration_weeks"]
        self.assertEqual(failed(self.p), ["D04"])

    def test_single_span_yields_the_upper_weeks_bound(self):
        self.p["mls_units"] = self.p["mls_units"][:1]
        self.unit()["duration_weeks"] = 6
        self.assertEqual(failed(self.p), ["D04"])
        self.assertEqual(v.validate(self.p, single_span=True).failed_ids(), [])

    def test_single_span_keeps_the_minimum_and_multi_unit_cap(self):
        self.p["mls_units"] = self.p["mls_units"][:1]
        self.unit()["duration_weeks"] = 1
        self.assertEqual(v.validate(self.p, single_span=True).failed_ids(), ["D04"])
        self.p["mls_units"].append(copy.deepcopy(self.p["mls_units"][0]))
        self.p["mls_units"][1]["mls_id"] = "MLS-EXTRA-0"
        self.p["mls_units"][1]["duration_weeks"] = 6
        self.unit()["duration_weeks"] = 2
        self.assertEqual(v.validate(self.p, single_span=True).failed_ids(), ["D04"])

    def test_nonstandard_role_fails_schema_and_role_check(self):
        self.unit()["tasks"][0]["role"] = "Head_Teacher"
        self.assertEqual(failed(self.p), ["D01", "D05"])

    def test_steps_out_of_order(self):
        self.unit()["tasks"][1]["step"] = 3
        self.assertEqual(failed(self.p), ["D06"])

    def test_missing_dependency(self):
        self.unit(1)["dependencies"] = ["MLS-HYDRO-99"]
        report = v.validate(self.p)
        self.assertEqual(report.failed_ids(), ["D07"])
        self.assertIn("MLS-HYDRO-99", report.checks[6].issues[0].problem)

    def test_duplicate_id(self):
        self.unit(1)["mls_id"] = "MLS-HYDRO-01"
        self.unit(1)["dependencies"] = []
        self.assertEqual(failed(self.p), ["D07"])

    def test_cycle(self):
        self.unit(0)["dependencies"] = ["MLS-HYDRO-02"]
        self.assertEqual(failed(self.p), ["D08"])

    def test_macro_alignment_blank(self):
        self.unit()["macro_alignment"] = "   "
        self.assertEqual(failed(self.p), ["D09"])

    def test_regional_terms_found_anywhere(self):
        self.unit()["tasks"][2]["action"] = "Take the options to the SMC and the HM."
        self.p["macro_objective"] += " Budget: ₹500."
        report = v.validate(self.p)
        self.assertEqual(report.failed_ids(), ["D10"])
        self.assertEqual(len(report.checks[9].issues), 2)

    def test_regional_terms_match_whole_words_only(self):
        self.unit()["tasks"][0]["action"] = "Clap the rhythm; read the SMCs and MIPS logos."
        self.assertEqual(failed(self.p), [])

    def test_overloaded_step_fails_step_size(self):
        self.unit()["tasks"][0]["action"] = " ".join(f"Do thing {k}." for k in range(1, 6))
        report = v.validate(self.p)
        self.assertEqual(report.failed_ids(), ["D11"])
        self.assertIn("5 sentences", report.checks[10].issues[0].problem)

    def test_long_single_sentence_fails_step_size(self):
        self.unit()["tasks"][0]["action"] = "Measure " + "and record " * 55 + "the rain."
        self.assertEqual(failed(self.p), ["D11"])

    def test_hundred_word_step_is_at_cap(self):
        self.unit()["tasks"][0]["action"] = "Word " * 99 + "end."
        self.assertEqual(failed(self.p), [])

    def test_hundred_and_one_word_step_fails_step_size(self):
        self.unit()["tasks"][0]["action"] = "Word " * 100 + "end."
        self.assertEqual(failed(self.p), ["D11"])

    def test_four_sentences_with_abbreviations_pass(self):
        self.unit()["tasks"][0]["action"] = ("Use reused items, e.g. bottles. Mark a 0 line at 2.5 cm, i.e. the water level. "
                                              "Read it daily. Write the number down.")
        self.assertEqual(failed(self.p), [])

    def test_word_cap_multiplier_scales_the_limit(self):
        cfg = copy.deepcopy(v.load_config())
        cfg["limits"]["word_cap_multipliers"] = {"default": 1.0, "fr": 1.2}
        self.unit()["tasks"][0]["action"] = "Word " * 109 + "end."
        self.assertEqual(v.validate(self.p, config=cfg).failed_ids(), ["D11"])
        self.assertEqual(v.validate(self.p, config=cfg, language="fr").failed_ids(), [])


class WordCap(unittest.TestCase):
    def limits(self, multipliers):
        return {"max_words_per_step": 100, "word_cap_multipliers": multipliers}

    def test_no_language_uses_config_value(self):
        self.assertEqual(v.effective_word_cap(self.limits({"default": 1.0})), 100)
        self.assertEqual(v.effective_word_cap({"max_words_per_step": 100}), 100)

    def test_language_multiplier_scales_and_rounds_up(self):
        self.assertEqual(v.effective_word_cap(self.limits({"fr": 1.2}), "fr"), 120)
        self.assertEqual(v.effective_word_cap(self.limits({"fr": 1.15}), "fr"), 115)

    def test_unknown_language_falls_back_to_default(self):
        self.assertEqual(v.effective_word_cap(self.limits({"default": 1.0, "fr": 1.2}), "xx"), 100)

    def test_language_lookup_ignores_case(self):
        self.assertEqual(v.effective_word_cap(self.limits({"french": 1.2}), "French"), 120)

    def test_bad_multipliers_fall_back_to_one(self):
        for bad in (0, -1.5, "wide", None, [2]):
            with self.subTest(bad=bad):
                self.assertEqual(v.effective_word_cap(self.limits({"fr": bad}), "fr"), 100)


class Robustness(unittest.TestCase):
    def test_garbage_payload_reports_instead_of_crashing(self):
        for payload in (None, [], "x", {"mls_units": "nope"}, {"mls_units": [1, {"tasks": "x"}]}):
            report = v.validate(payload)
            self.assertFalse(report.passed)
            self.assertIn("D01", report.failed_ids())


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = v.main([str(a) for a in args])
        return code, out.getvalue()

    def test_exit_codes(self):
        self.assertEqual(self.run_cli(FIXTURES / "hydrology-valid.json")[0], 0)
        self.assertEqual(self.run_cli(FIXTURES / "hydrology-spec.json")[0], 1)

    def test_json_output(self):
        code, out = self.run_cli(FIXTURES / "hydrology-spec.json", "--json")
        data = json.loads(out)
        self.assertFalse(data["passed"])
        self.assertEqual(len(data["checks"]), 11)


if __name__ == "__main__":
    unittest.main()
