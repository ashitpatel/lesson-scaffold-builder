# Test fixtures

| File | What it is | Expected result of `python3 -m lsb.validate` |
|---|---|---|
| `hydrology-spec.json` | The hydrology output payload exactly as printed in the requirements (Part 3, section 8B). | **Fails** D03 (2 steps per unit; the critic needs 3–7), D04 (no `duration_weeks`) and D09 (no `macro_alignment`). The spec's own example does not meet its critic gate. |
| `hydrology-valid.json` | The same two units, written by hand to pass every deterministic check: 4 steps each, durations and macro-alignment links added. | **Passes** all checks. It is a test fixture, not a reviewed teaching design. |
