"""Keep the adapted prompts in step with the code that backs them."""

import json
import re
import unittest
from pathlib import Path

from lsb import validate as v

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
ADAPTED = ("05-decompose.md", "50-critic.md")


def read(name):
    return (PROMPTS / name).read_text(encoding="utf-8")


def critic_rows():
    """{'G01': (check name, code column), ...} from the critic's table."""
    rows = {}
    for line in read("50-critic.md").splitlines():
        m = re.match(r"\| (G\d\d) \| \*\*(.+?):\*\*.*?\| (.*?) \|", line)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(3))
    return rows


class CriticTable(unittest.TestCase):
    def test_has_exactly_g01_to_g21(self):
        self.assertEqual(list(critic_rows()), [f"G{i:02d}" for i in range(1, 22)])

    def test_every_code_check_maps_to_the_row_for_its_critic_check(self):
        rows = {name: code for name, code in critic_rows().values()}
        for check in v.validate({}).checks:
            if check.critic_check.startswith("("):
                continue  # D01, D06: integrity checks with no named critic check
            with self.subTest(check=check.id):
                self.assertIn(check.critic_check, rows, "critic table has no row for this check")
                self.assertIn(check.id, rows[check.critic_check])

    def test_no_row_cites_a_code_check_that_does_not_exist(self):
        ids = {c.id for c in v.validate({}).checks}
        for gid, (_, code) in critic_rows().items():
            for cited in re.findall(r"D\d\d", code):
                self.assertIn(cited, ids, f"{gid} cites unknown {cited}")


class DecomposeExample(unittest.TestCase):
    EXAMPLE = ROOT / "tests/fixtures/example-persuasive-valid.json"

    def test_example_unit_matches_its_fixture(self):
        blocks = re.findall(r"```json\n(.*?)```", read("05-decompose.md"), re.S)
        example = json.loads(blocks[-1])
        fixture = json.loads(self.EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(example, fixture["mls_units"][1])

    def test_example_fixture_passes_every_code_check(self):
        report = v.validate(json.loads(self.EXAMPLE.read_text(encoding="utf-8")))
        self.assertTrue(report.passed, v.format_text(report))

    def test_prompts_do_not_contain_any_test_source(self):
        # A worked example taken from a test source lets the model copy the
        # answer, so a pass on that source proves nothing (seen in a live run).
        fixtures = ROOT / "tests/fixtures"
        sources = sorted(fixtures.glob("*-source.md"))
        self.assertTrue(sources)
        for src in sources:
            markers = [src.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()]
            answer = fixtures / src.name.replace("-source.md", "-valid.json")
            if answer.exists():  # the mls_id prefix of the expected answer, e.g. "MLS-HYDRO-"
                markers += sorted(set(re.findall(r"MLS-[A-Z]+-", answer.read_text(encoding="utf-8"))))
            for prompt in sorted(PROMPTS.glob("*.md")):
                text = prompt.read_text(encoding="utf-8")
                for marker in markers:
                    with self.subTest(source=src.name, prompt=prompt.name, marker=marker):
                        self.assertNotIn(marker, text)


class AdaptedPromptsAreRegionNeutral(unittest.TestCase):
    def test_no_regional_terms(self):
        report = v.check_regional_terms({p: read(p) for p in ADAPTED}, v.load_config()["regional_terms"])
        self.assertTrue(report.passed, [f"{i.where}: {i.problem}" for i in report.issues])


if __name__ == "__main__":
    unittest.main()
