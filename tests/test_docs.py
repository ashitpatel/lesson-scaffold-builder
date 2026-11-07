"""Docs integrity: walkthrough folders, source-copy parity, and relative links."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WALKTHROUGHS = ROOT / "docs/walkthroughs"
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ORIGIN = re.compile(r"tests/fixtures/(\S+?\.md)")


class WalkthroughFolders(unittest.TestCase):
    def folders(self):
        return sorted(p for p in WALKTHROUGHS.iterdir() if p.is_dir())

    def test_every_folder_pairs_a_walkthrough_with_its_source(self):
        self.assertTrue(self.folders())
        for d in self.folders():
            with self.subTest(folder=d.name):
                self.assertTrue((d / "README.md").exists())
                self.assertTrue((d / "source.md").exists())

    def test_each_source_copy_matches_its_canonical_fixture(self):
        for d in self.folders():
            with self.subTest(folder=d.name):
                head, body = (d / "source.md").read_text(encoding="utf-8").split("---\n\n", 1)
                m = ORIGIN.search(head)
                self.assertTrue(m, "no origin URL in the source.md header")
                fixture = (ROOT / "tests/fixtures" / m.group(1)).read_text(encoding="utf-8")
                self.assertEqual(body.splitlines(), fixture.splitlines())
                self.assertIn("LICENSE", head)


class LinksResolve(unittest.TestCase):
    def test_every_relative_link_resolves_to_a_real_file(self):
        files = [ROOT / "README.md"] + sorted(ROOT.joinpath("docs").rglob("*.md"))
        broken = []
        for f in files:
            for target in LINK.findall(f.read_text(encoding="utf-8")):
                target = target.strip()
                if not target or target.startswith("#") or "://" in target:
                    continue
                if not (f.parent / target.split("#")[0]).exists():
                    broken.append(f"{f.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
