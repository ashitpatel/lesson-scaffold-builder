# Lesson Scaffold Builder (LSB)

Turns long, lecture-heavy educational content into a small DAG of Micro-Lesson Scaffolds (MLS units): 2–4 week, 3–7 step, offline teacher cards.

**Status:** early. The LLM prompts are in [prompts/](prompts/) (inherited from the Shikshagraha MIP transformer, only partly adapted). The deterministic validation layer below works. There is no orchestrator yet.

## Deterministic validator

```bash
pip install jsonschema
python3 -m lsb.validate tests/fixtures/hydrology-valid.json        # text report
python3 -m lsb.validate payload.json --json                         # machine-readable
python3 -m unittest discover -s tests                               # run the tests
```

Exit status: `0` all checks pass, `1` a check failed, `2` the file couldn't be read.

It validates against [schemas/mls-dag.schema.json](schemas/mls-dag.schema.json). That is the requirements' `MLS_DAG_Sequence` schema plus two optional fields per unit, `macro_alignment` and `duration_weeks`, which the checks need. Limits and the list of region-specific terms are in [config/taxonomy_mapping.json](config/taxonomy_mapping.json).

| ID | Check | Critic gate check (requirements §7) |
|---|---|---|
| D01 | Schema conformance | — (prerequisite) |
| D02 | ≤5 MLS units | Structural Boundaries |
| D03 | 3–7 steps per unit | Task Granularity |
| D04 | `duration_weeks` declared and 2–4 | Execution Window |
| D05 | Roles are Lead_Educator / Community_Volunteer / Peer_Facilitator | Role Standardization |
| D06 | Steps numbered 1..n in order | — (integrity) |
| D07 | Every dependency exists; ids unique | Dependency Mapping |
| D08 | No dependency cycles | Cycle Prevention |
| D09 | Every unit has a `macro_alignment` link | Macro Alignment (presence only) |
| D10 | No region-specific terms in any string | Universal Taxonomy (term list only) |

The other 13 critic checks need judgement: audience, privacy, financial isolation, offline default, socioeconomic adaptability, pedagogical sourcing, coherence, low overhead, materials, clerical reduction, safety, collaborative balance and output clarity. They belong to the LLM critic, which should receive this report as input. D09 and D10 also have a judgement half (is the link real, is a term regional) that stays with the critic.

The hydrology example printed in the requirements fails D03, D04 and D09. See [tests/fixtures/README.md](tests/fixtures/README.md).
