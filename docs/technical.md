# Technical reference

How to run, check and extend the pipeline. For what LSB is and why, start with the [README](../README.md); for how it's used, see [docs/README.md](README.md).

Requirements: Python 3.10+, `pip install jsonschema anthropic`, and a model backend: a Claude Code login (the default), a Muse login (`--backend muse`), a free Gemini key from Google AI Studio (`--backend gemini`, `GEMINI_API_KEY`), or an Anthropic API key (`--backend api`).

## Deterministic validator

```bash
pip install jsonschema anthropic
python3 -m lsb.validate tests/fixtures/hydrology-valid.json        # text report
python3 -m lsb.validate payload.json --json                         # machine-readable
python3 -m unittest discover -s tests                               # run the tests
```

Exit status: `0` all checks pass, `1` a check failed, `2` the file couldn't be read.

It validates against [schemas/mls-dag.schema.json](../schemas/mls-dag.schema.json). That is the requirements' `MLS_DAG_Sequence` schema plus two optional fields per unit, `macro_alignment` and `duration_weeks`, which the checks need. Limits and the list of region-specific terms are in [config/taxonomy_mapping.json](../config/taxonomy_mapping.json).

| ID | Check | Critic gate check (requirements §7) |
|---|---|---|
| D01 | Schema conformance | — (prerequisite) |
| D02 | ≤5 MLS units | Structural Boundaries |
| D03 | 3–7 steps per unit | Task Granularity |
| D04 | `duration_weeks` declared and 2–4 (a single-module run's one unit may span the chapter) | Execution Window |
| D05 | Roles are Lead_Educator / Community_Volunteer / Peer_Facilitator | Role Standardization |
| D06 | Steps numbered 1..n in order | — (integrity) |
| D07 | Every dependency exists; ids unique | Dependency Mapping |
| D08 | No dependency cycles | Cycle Prevention |
| D09 | Every unit has a `macro_alignment` link | Macro Alignment (presence only) |
| D10 | No region-specific terms in any string | Universal Taxonomy (term list only) |
| D11 | Each step is at most 4 sentences and 80 words | Task Granularity (one action per step) |

D11 exists because revisions tend to append fixes to an existing step: in the live hydrology runs, one step grew from 5 to 9 sentences across attempts while the critic let it through. The other 13 critic checks need judgement: audience, privacy, financial isolation, offline default, socioeconomic adaptability, pedagogical sourcing, coherence, low overhead, materials, clerical reduction, safety, collaborative balance and output clarity. They belong to the LLM critic, which should receive this report as input. D09 and D10 also have a judgement half (is the link real, is a term regional) that stays with the critic.

The hydrology example printed in the requirements fails D03, D04 and D09. See [tests/fixtures/README.md](../tests/fixtures/README.md).

## Pipeline runner

```bash
python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework" --dry-run
python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework"
```

`--dry-run` builds every request and checks each prompt placeholder has a value. It makes no model calls. A live run calls `claude-opus-5-5` (effort `high` by default, `--effort` to change). By default it goes through headless Claude Code (`claude -p`) on your Claude Code login, so no API key is needed; `--backend api` calls the Anthropic API instead and needs `ANTHROPIC_API_KEY` or an `ant auth login` profile. `--backend muse` goes through headless Muse Code (`muse exec`) on your Muse login: `muse exec` has no system-prompt channel, so the prompt and the input go in one file, and each call is a single model step in an empty directory. `--backend gemini` calls Google's Gemini API over plain HTTPS (standard library only, no SDK) with a free key from [Google AI Studio](https://aistudio.google.com/apikey) in `GEMINI_API_KEY` (or `GOOGLE_API_KEY`), no paid account needed: the prompt goes as the system instruction, the reply is requested as JSON, and `--effort` maps to a thinking budget (low 0, medium 2048, high 8192, xhigh 16384, max 24576), so the free path runs in a browser notebook — see README §2b. Every backend reports per-call token counts the same way. `--model` overrides the model id (default: `claude-opus-5-5`, the CLI default for `muse`, `gemini-2.5-flash` for `gemini`).

**Decompose loop.** Each attempt is 2 calls: decompose, then the critic. The critic's PASS ends the loop. REVISE sends its issues and the previous output back to decompose, up to `--max-revisions` (default 2). REJECT starts again from the source once, and a second REJECT stops the run. Validator results are final, so a critic PASS on a sequence that fails a code check counts as REVISE. On a revision, the critic gets its previous issues: it confirms each one is fixed, judges the changed steps fully, and raises only new blockers elsewhere, so the loop converges.

**User choices.** `--ask` pauses the run to ask, first of all, which frameworks to exclude for this run (each with a one-line summary; blank keeps all three, and combines with `--no-eb`/`--no-cl`/`--no-pb`). Then the MLS modularization decisions: one MLS or several; if several, the unit maximum (2–5, default 5), the breakdown focus (`auto`, one unit per source section with the sections listed, or free text, passed as `USER_FOCUS`), and the max timeframe per module (2–4 weeks, default 4). A single MLS spans the whole chapter, so the 2–4-week gate yields for it (the critic is told via `MODE`); the multi-module answers are skipped and recorded as single-module defaults. Before each remaining stage: which of its cards may apply (with each card's Targets line), the cards-per-unit limit (1–2), and whether it may add a step. Excluded frameworks are never called or asked about. Over-limit units and over-long modules are sent back with a code issue; card and step limits are enforced both by showing the model only the allowed cards and by the code check. `--answers FILE` reads the same answers from a JSON object (`{"frameworks_excluded": ["connected_learning"], "single_module": false, "max_units": 3, "max_weeks": 3, "focus": "by skill", "evidence_based_cards": ["EB-01", "EB-04"], ...}`); missing or invalid answers fall back to defaults, which is exactly what a run without either flag does. The values land in `choices.json` in the run folder.

**Optimisation stages.** Once the sequence passes, three stages run in order, each once per unit:
- [prompts/25-evidence-based.md](../prompts/25-evidence-based.md) with [frameworks/evidence-based-practices.md](../frameworks/evidence-based-practices.md): five practices (EB-01 to EB-05), each applied only with all its non-negotiables, with guardrails. `--no-eb` skips it.
- [prompts/30-connected-learning.md](../prompts/30-connected-learning.md) with [frameworks/connected-learning.md](../frameworks/connected-learning.md): the requirements' CL-01 to CL-05, with guardrails. It works on the Evidence-Based output. `--no-cl` skips it.
- [prompts/31-participatory-budgeting.md](../prompts/31-participatory-budgeting.md) with [frameworks/participatory-budgeting.md](../frameworks/participatory-budgeting.md): the requirements' PB fit-gate (a real resource trade-off, never for decoding drills or the educator's own admin) and cards PB-01 to PB-05, with guardrails. It works on the output of the stages before it. `--no-pb` skips it.

Each stage may abstain, or apply at most 2 of its own cards with at most 1 added step. [lsb/optimise.py](../lsb/optimise.py) checks each edit in code: the unit's id, title, dependencies, `macro_alignment` and weeks are unchanged, no step is removed or reordered, and every changed step is logged against one of that stage's cards. An edit that fails is retried once with the problems, then dropped. Accepted edits are merged, validated and reviewed by the critic, which gets the cards of this stage and of earlier stages that kept edits, and a source trace naming the card behind each changed step. A unit with issues is revised up to `--max-stage-revisions` times (default 1), then reverted to its input version; anything the critic can't pin on one edited unit (a REJECT, an issue elsewhere) reverts every edit of that stage. So a stage can only keep or improve a passed sequence. If every unit abstains, the stage makes no critic call.

**Late issues and the repair round.** A stage's review sees the whole sequence, so it can find problems in content no stage changed (a step the decompose review missed). Only issues on steps a stage changed count against that stage's edits; the rest are recorded as *late issues* (`late-issues.json`). After the stages, they go back to decompose for up to two repair rounds. The first feedback entry is marked `repair`, and [lsb/optimise.py](../lsb/optimise.py) `check_repair` holds the repair to the steps, unit fields and fallbacks the issues point at, edited in place (no units, steps or fallbacks added, removed or reordered), so the trace and every kept optimisation edit stay valid. The repaired sequence is validated and reviewed with its fallbacks and the kept cards. If the review passes, the repaired sequence is final; if not, the run's status is `issues_open` and no cards are rendered.

**Teacher cards.** A passed run ends with [lsb/render.py](../lsb/render.py), which is code, not a prompt. It writes `cards.txt` (plain text, at most 78 characters wide) and `cards.html` (one self-contained black-on-white page, one card per printed page, with no images, scripts or external resources). The cards are an overview, then one card per unit in dependency order. Each unit card has a two-column WHO / WHAT TO DO step table, with each step changed by an optimisation stage marked with its card; the conditions the unit relies on and what to do if one doesn't hold; and the changes the stages made, by card. The renderer then checks its own output against critic check G21 (Output Clarity): every unit has a card, every step's text appears unaltered, the text fits the width, and the HTML is two-column, text-only, offline and black and white. The result goes into `summary.json` as `cards_g21`. To render a run saved earlier:

```bash
python3 -m lsb.render runs/<run>
```

Every reply and intermediate JSON is saved under `runs/<timestamp>/` (gitignored): `choices.json` (the breakdown and per-stage answers, or defaults), `NN-decompose.json`, `NN-validator.json`, `NN-critic.json`, `cl1-<mls_id>.json`, `clN-critic.json` and the `pb…` equivalents for the optimisation stages, `decomposed-sequence.json` (before them), `source_trace.json` (after them), `sequence.json` (the final sequence; if decompose never passed, its best attempt), `cards.txt` and `cards.html`, and `summary.json` with per-attempt issue counts, what each optimisation stage did per unit, source flags and token usage. Statuses: `pass`, `revise_exhausted` (decompose never passed), `rejected`, `issues_open` (a later review found problems the repair couldn't fix) and `error`. Exit status: `0` passed, `1` didn't pass, `2` usage or API error.

## Regression sweep

```bash
python3 -m lsb.regress                                  # every case, 3 at a time, into runs/regress-<timestamp>/
python3 -m lsb.regress --only kenya-water,civics
python3 -m lsb.regress --check runs/regress-<timestamp>  # re-check saved runs; no model calls
python3 -m lsb.regress --check runs/regress-new --baseline runs/regress-old
python3 -m lsb.regress --backend muse                   # same sweep on Muse; extra flags pass to lsb.run
python3 -m lsb.regress --answers answers.json            # answer every run's --ask questions from a file
```

[lsb/regress.py](../lsb/regress.py) runs every case in [tests/regression/cases.json](../tests/regression/cases.json) through the whole pipeline and checks **properties** of each result rather than a golden answer, because two good decompositions of the same chapter can differ: the run passes; the unit count is within its limit; planted traps and region-specific names are absent from the final sequence; terms a faithful sequence must keep are present; enough source flags were raised; a stage that must abstain (participatory budgeting on a reading drill) did; and the teacher cards pass G21. It writes `report.md` and `report.json` under the sweep folder. A full sweep of the nine cases runs roughly 3.0M input / 1.0M output tokens; the report's Tokens column shows each case's metered input and output. The expectations are backend-agnostic, so the same sweep runs on any backend — but keep one backend per sweep folder so reports stay comparable. Validated: the Mexico case passes on `muse-spark-1.3` via `--backend muse` (13 calls, first-attempt pass, no repair).

## Tests

```bash
python3 -m unittest discover -s tests
```

All offline: a scripted fake model drives the runner, and every prompt's worked example is checked against its fixture with the same code the pipeline uses.
