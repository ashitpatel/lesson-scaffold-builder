"""Packaging contracts: version single-sourcing, data files, release notes."""

import re
import unittest
from pathlib import Path

from lsb._paths import is_checkout, resource_root

ROOT = Path(__file__).resolve().parents[1]


class Packaging(unittest.TestCase):
    def test_version_matches_pyproject(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        m = re.search(r'^version = "([^"]+)"$', pyproject, flags=re.M)
        self.assertTrue(m, "no version in pyproject.toml")
        self.assertEqual(m.group(1), version)

    def test_changelog_has_this_version(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(f"## {version} ", changelog)

    def test_console_scripts_cover_the_four_runners(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        for name in ("lsb-run", "lsb-validate", "lsb-render", "lsb-regress"):
            self.assertIn(name, pyproject)

    def test_resource_root_is_the_checkout(self):
        self.assertTrue(is_checkout())
        self.assertEqual(resource_root(), ROOT)
        for d in ("prompts", "frameworks", "schemas", "config"):
            self.assertTrue((resource_root() / d).is_dir(), d)


if __name__ == "__main__":
    unittest.main()
