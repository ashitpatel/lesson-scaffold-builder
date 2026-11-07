# Test fixtures

| File | What it is | Expected result of `python3 -m lsb.validate` |
|---|---|---|
| `hydrology-spec.json` | The hydrology output payload exactly as printed in the requirements (Part 3, section 8B). | **Fails** D03 (2 steps per unit; the critic needs 3–7), D04 (no `duration_weeks`) and D09 (no `macro_alignment`). The spec's own example does not meet its critic gate. |
| `hydrology-valid.json` | The same two units, written by hand to pass every deterministic check: 4 steps each, durations and macro-alignment links added. | **Passes** all checks. It is a test fixture, not a reviewed teaching design. |
| `hydrology-source.md` | The mock chapter from the requirements (Part 3, section 8A). | Input for `python3 -m lsb.run`. Kept out of every prompt (a test enforces this), so a pass on it means something. |
| `example-persuasive-valid.json` | The sequence behind the worked example in `prompts/05-decompose.md`; unit 2 appears there verbatim. | **Passes** all checks. Deliberately a different topic from every `*-source.md` test input. |
