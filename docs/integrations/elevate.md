# Design note: exporting LSB runs to ShikshaLokam ELEVATE

*Turning lessons into teachable classroom plans.*

**Status: exploratory, 2026-11-11. Nothing here is built.** No ELEVATE deployment or partner is being targeted. The mapping below has **not** been checked against ELEVATE's real project-template format, whose field names could not be confirmed from public sources. Treat every ELEVATE field name in this note as a placeholder.

## Why this note exists

A proposal suggested turning LSB into an ELEVATE-aligned service. It had four parts:
- a Program → Project → Task → Subtask schema;
- NetworkX graph validation;
- mandatory evidence capture (`samiksha_evidence_rules`);
- a framework "conflict matrix".

It also suggested Kafka and PostgreSQL persistence behind a standalone/ELEVATE adapter. This note records what holds up against the code, what doesn't, and the smallest integration worth building if a real ELEVATE target appears.

## What LSB already does (and the proposal assumed it didn't)

| Proposal assumed | What LSB has |
|---|---|
| A flat list of steps | A DAG of up to 5 MLS units ([schema](../../schemas/mls-dag.schema.json)). Each unit has 3–7 steps with standard roles, dependencies, `macro_alignment` and `duration_weeks` (2–4). This is already close to a project/task/subtask hierarchy. |
| Only item-count checks; add NetworkX | [lsb/dag.py](../../lsb/dag.py) already does cycle detection, missing-dependency checks and topological ordering. These are enforced as code checks D07/D08 and critic checks G11/G12 ([technical.md](../technical.md)). NetworkX would add a dependency and catch nothing new. |
| Frameworks applied all at once, causing prompt drift | The stages run one after another: evidence-based, then Connected Learning, then participatory budgeting. Each stage applies at most 2 cards and adds at most 1 step per unit. [lsb/optimise.py](../../lsb/optimise.py) checks every edit in code, the critic reviews it with earlier stages' cards in view, and a failing edit is reverted. Participatory budgeting also has its own fit-gate. The proposed conflict matrix already exists as this pipeline. |
| An adapter reading `lesson_title`, `steps`, `heading`, `body_text`, `tags` | These fields don't exist. The real inputs are listed under [Source of each field](#source-of-each-field). |

## Decisions

### 1. Evidence capture stays optional, teacher-side and class-level

Requiring a camera capture before a step can be completed would break two blocker-level critic checks:
- **G06 Privacy Guardrails:** no photos, individual child data or performance logs.
- **G08 Offline Default:** no devices.

These checks are central to LSB, as the [walkthroughs](../README.md) show: removing "weekly photos for grading" and "children's videos sent to parents" is part of what the pipeline is for. ELEVATE's evidence upload is meant for an educator documenting their own improvement work, and that is the only use LSB should support.

If evidence hints are ever added, they must:
- be **optional**, never a condition for completing a step;
- be attached only to steps that already produce a **class artifact** (a poster, a class book, a mock ledger, a tally chart);
- describe an **artifact with no students in it**: no faces, names, individual scores or home details;
- be checked in code (a deny-list in the spirit of D10) and by the critic under G06, like any other text LSB produces.

### 2. LSB doesn't own a broker or a database

ELEVATE's project service already runs its own messaging, storage, template APIs and evidence upload. If LSB wrote its own `projects` / `tasks` / `subtasks` tables, it would duplicate ELEVATE's system of record and drift away from it. The integration point is a **project template file that ELEVATE imports**. Kafka, PostgreSQL and WeasyPrint are out of scope; the cards are already self-contained offline HTML.

### 3. The core stays as it is

The core schema and its two dependencies (`jsonschema`, `anthropic`) don't change. No `custom_attributes` block is added. Anything ELEVATE-specific, such as program and tenant ids, is an export parameter and appears only in the exported file. An exporter, if built, lives in `lsb/adapters/` behind an optional extra.

### 4. The NetworkX validator and the conflict matrix are dropped

The existing modules already cover both, as shown above.

## Proposed mapping (provisional)

Default: **one LSB run becomes one ELEVATE Project.**

| LSB | ELEVATE (placeholder names) | Notes |
|---|---|---|
| run (`sequence.json`) | Project | `macro_objective` becomes the project objective, `global_context.grade_band` a category |
| — | `program_id`, `tenant_id` | export parameters, never stored in the core |
| `mls_units[]` | Task | `title`, `duration_weeks`, and `macro_alignment` as the description; tasks are ordered by `lsb.dag.topological_order`, with `dependencies` kept as prerequisites if ELEVATE supports them and otherwise as ordering only |
| `mls_units[].tasks[]` (steps) | Subtask | `action` as the text, `step` as the order, `role` as metadata or a tag |
| `source_trace.json` card entries | Subtask tags | e.g. `EB-04`, `CL-02`, `PB-01` on the steps a stage changed |
| `environment_assumptions[]` (`assumes` / `if_not`) | Task notes | the teacher's plan B; it must travel with the unit |
| `choices.json` | Project metadata | the language, locale mode and excluded frameworks used to generate it |

**Alternative:** each 2–4-week unit becomes its own Project, grouped under a program. A unit is about the length of a typical micro-improvement project, but splitting loses the single objective that ties the units together. Decide this once a real ELEVATE template is in hand.

### Source of each field

- `sequence.json`: `macro_objective`, `global_context`, `mls_units[]` (`mls_id`, `title`, `dependencies`, `macro_alignment`, `duration_weeks`, `tasks[]` with `step`, `role`, `action`).
- `source_trace.json`: one entry per step; `source_locator` for source-traced steps, and `card` plus `change` for steps an optimisation stage changed.
- The best `NN-decompose.json`: `environment_assumptions[]`, with `mls_id`, `assumes` and `if_not`. This is the same file [lsb/render.py](../../lsb/render.py) reads.
- `choices.json` and `summary.json`: the run's choices and status. Only runs with status `pass` would be exported.
- Refined runs: export the latest `revisions/revN/`, not the original.

## Gaps an exporter would need to close

1. **Stable step ids.** Steps have no ids that survive a refinement; `optimise.match_steps` matches steps by role and text. Without deterministic ids (for example a hash of run, `mls_id` and step number), re-exporting a refined run would create a duplicate project instead of updating the existing one.
2. **ELEVATE's real template format.** This is needed before any field name above is final.
3. **Translated runs.** Decide whether to export the translated sequence, the English original (`english-final.json`), or both.

## If a real ELEVATE target appears

1. Get a real project-template export or the import API spec, and freeze it as `schemas/elevate-template.schema.json`.
2. Settle the mapping choice: one project per run, or one per unit.
3. Build `lsb-export --target elevate runs/<run>`. It should be pure and offline, and tested against the fixtures with the rest of the suite.
4. Add stable step ids.
5. Only after that, and only if ELEVATE asks for it: optional class-level evidence hints (decision 1), and a thin HTTP client behind `pip install lesson-scaffold-builder[elevate]`.

## References

- [ShikshaLokam ELEVATE](https://shikshalokam.org/elevate/) and [ELEVATE building blocks](https://elevate.shikshalokam.org/?p=24786)
- [ELEVATE Projects concept note](https://elevate.shikshalokam.org/wp-content/uploads/2025/05/Projects-Concept-Note.pdf): tasks, subtasks and evidence upload, as product features
- ELEVATE project-service repository, read only through a [mirror](https://github.imc.re/ELEVATE-Project/project-service): it lists Kafka, MongoDB and PostgreSQL among its tools. The template data model was not confirmed.
