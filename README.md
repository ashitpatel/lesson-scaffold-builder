# Lesson Scaffold Builder (LSB)

Turns long, lecture-heavy educational content into a small DAG of Micro-Lesson Scaffolds (MLS units): 2–4 week, 3–7 step, offline teacher cards.

**Status:** early. The LLM prompts are in [prompts/](prompts/). `05-decompose` and `50-critic` are written for LSB; the rest are still the Shikshagraha MIP transformer's. The deterministic validator and a runner for decompose → validate → critic work. The optimisation and render stages aren't wired in yet.

## Deterministic validator

```bash
pip install jsonschema anthropic
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
| D11 | Each step is at most 4 sentences and 80 words | Task Granularity (one action per step) |

D11 exists because revisions tend to append fixes to an existing step: in the live hydrology runs, one step grew from 5 to 9 sentences across attempts while the critic let it through. The other 13 critic checks need judgement: audience, privacy, financial isolation, offline default, socioeconomic adaptability, pedagogical sourcing, coherence, low overhead, materials, clerical reduction, safety, collaborative balance and output clarity. They belong to the LLM critic, which should receive this report as input. D09 and D10 also have a judgement half (is the link real, is a term regional) that stays with the critic.

The hydrology example printed in the requirements fails D03, D04 and D09. See [tests/fixtures/README.md](tests/fixtures/README.md).

## Pipeline runner (decompose → validate → critic)

```bash
python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework" --dry-run
python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework"
```

`--dry-run` builds both requests and checks every prompt placeholder has a value. It makes no API calls. A live run calls `claude-opus-5-5` (effort `high` by default, `--effort` to change), with server-side refusal fallback on. It needs Anthropic credentials: `ANTHROPIC_API_KEY`, or a profile from `ant auth login`. Each attempt is 2 API calls.

Routing: the critic's PASS ends the run. REVISE sends its issues and the previous output back to decompose, up to `--max-revisions` (default 2). REJECT starts again from the source once, and a second REJECT stops the run. Validator results are final, so a critic PASS on a sequence that fails a code check counts as REVISE. On a revision, the critic gets its previous issues: it confirms each one is fixed, judges the changed steps fully, and raises only new blockers elsewhere, so the loop converges.

Every reply and intermediate JSON is saved under `runs/<timestamp>/` (gitignored): `NN-decompose.json`, `NN-validator.json`, `NN-critic.json`, `sequence.json` (the best attempt: fewest blockers, then majors, with code failures counted as blockers), and `summary.json` with per-attempt issue counts and token usage. Exit status: `0` passed, `1` didn't pass, `2` usage or API error.
