# Lesson Scaffold Builder (LSB)

Turns long, lecture-heavy educational content into a small DAG of Micro-Lesson Scaffolds (MLS units): 2–4 week, 3–7 step, offline teacher cards.

**Status:** early. The LLM prompts are in [prompts/](prompts/). `05-decompose`, `30-connected-learning`, `31-participatory-budgeting` and `50-critic` are written for LSB; the rest are still the Shikshagraha MIP transformer's. The deterministic validator and a runner for decompose → validate → critic, then Connected Learning and Participatory Budgeting (each followed by validate → critic), work. A passed run ends with printable teacher cards. The evidence-based stage isn't written yet.

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

## Pipeline runner

```bash
python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework" --dry-run
python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework"
```

`--dry-run` builds every request and checks each prompt placeholder has a value. It makes no model calls. A live run calls `claude-opus-5-5` (effort `high` by default, `--effort` to change). By default it goes through headless Claude Code (`claude -p`) on your Claude Code login, so no API key is needed; `--backend api` calls the Anthropic API instead and needs `ANTHROPIC_API_KEY` or an `ant auth login` profile.

**Decompose loop.** Each attempt is 2 calls: decompose, then the critic. The critic's PASS ends the loop. REVISE sends its issues and the previous output back to decompose, up to `--max-revisions` (default 2). REJECT starts again from the source once, and a second REJECT stops the run. Validator results are final, so a critic PASS on a sequence that fails a code check counts as REVISE. On a revision, the critic gets its previous issues: it confirms each one is fixed, judges the changed steps fully, and raises only new blockers elsewhere, so the loop converges.

**Optimisation stages.** Once the sequence passes, two stages run in order, each once per unit:
- [prompts/30-connected-learning.md](prompts/30-connected-learning.md) with [frameworks/connected-learning.md](frameworks/connected-learning.md): the requirements' CL-01 to CL-05, with guardrails. `--no-cl` skips it.
- [prompts/31-participatory-budgeting.md](prompts/31-participatory-budgeting.md) with [frameworks/participatory-budgeting.md](frameworks/participatory-budgeting.md): the requirements' PB fit-gate (a real resource trade-off, never for decoding drills or the educator's own admin) and cards PB-01 to PB-05, with guardrails. It works on the Connected Learning output. `--no-pb` skips it.

Each stage may abstain, or apply at most 2 of its own cards with at most 1 added step. [lsb/optimise.py](lsb/optimise.py) checks each edit in code: the unit's id, title, dependencies, `macro_alignment` and weeks are unchanged, no step is removed or reordered, and every changed step is logged against one of that stage's cards. An edit that fails is retried once with the problems, then dropped. Accepted edits are merged, validated and reviewed by the critic, which gets the cards of this stage and of earlier stages that kept edits, and a source trace naming the card behind each changed step. A unit with issues is revised up to `--max-stage-revisions` times (default 1), then reverted to its input version; anything the critic can't pin on one edited unit (a REJECT, an issue elsewhere) reverts every edit of that stage. So a stage can only keep or improve a passed sequence. If every unit abstains, the stage makes no critic call.

**Teacher cards.** A passed run ends with [lsb/render.py](lsb/render.py), which is code, not a prompt. It writes `cards.txt` (plain text, at most 78 characters wide) and `cards.html` (one self-contained black-on-white page, one card per printed page, with no images, scripts or external resources). The cards are an overview, then one card per unit in dependency order. Each unit card has a two-column WHO / WHAT TO DO step table, with each step changed by an optimisation stage marked with its card; the conditions the unit relies on and what to do if one doesn't hold; and the changes the stages made, by card. The renderer then checks its own output against critic check G21 (Output Clarity): every unit has a card, every step's text appears unaltered, the text fits the width, and the HTML is two-column, text-only, offline and black and white. The result goes into `summary.json` as `cards_g21`. To render a run saved earlier:

```bash
python3 -m lsb.render runs/<run>
```

Every reply and intermediate JSON is saved under `runs/<timestamp>/` (gitignored): `NN-decompose.json`, `NN-validator.json`, `NN-critic.json`, `cl1-<mls_id>.json`, `clN-critic.json` and the `pb…` equivalents for the optimisation stages, `decomposed-sequence.json` (before them), `source_trace.json` (after them), `sequence.json` (the final sequence; if decompose never passed, its best attempt), `cards.txt` and `cards.html`, and `summary.json` with per-attempt issue counts, what each optimisation stage did per unit, source flags and token usage. Exit status: `0` passed, `1` didn't pass, `2` usage or API error.
