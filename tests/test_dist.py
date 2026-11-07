"""Generated browser-assistant files are in sync with prompt/ sources."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DistInSync(unittest.TestCase):
    def test_build_check_passes(self):
        proc = subprocess.run([sys.executable, "scripts/build.py", "--check"],
                              cwd=ROOT, capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
