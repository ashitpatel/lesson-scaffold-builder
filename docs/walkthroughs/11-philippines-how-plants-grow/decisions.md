# Engine decisions — Philippines: how plants grow

> Run `runs/philippines-live-1` on 8 November 2026 via Muse (`muse exec`) (16 model calls). Run without `--ask`: nothing was asked; every choice below is the pipeline default. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-GROW-01 | applied (EB-04, EB-09) | abstained (credited CL-04) | abstained |
| MLS-GROW-02 | applied (EB-04, EB-09) | applied (CL-02) | abstained |
| MLS-GROW-03 | applied (EB-04, EB-09) | applied (CL-04) | abstained |
| MLS-GROW-04 | abstained (credited EB-05) | applied (CL-04) | abstained |

- Evidence-Based reviews: round 1: PASS.
- Connected Learning reviews: round 1: PASS.
- Decompose review: round 1: PASS. No late issues, no repair.

## What the user was asked

Nothing — the run did not use `--ask`. Had it been used, the run would have asked: framework exclusions at the outset; single-vs-multi MLS with max units, breakdown focus and max weeks; and before each stage, which cards may apply, the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: no exclusions, multi-MLS up to 4 units, `auto` focus, 2–4 weeks per unit, every card allowed (EB-01 to EB-09), at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose built 4 units from the nine sections, grouping by topic: needs+leaves, the light experiment, roots+stems, seeds+leaves outdoors.
- The EB stage used the new EB-09 card in three units and abstained unit 4 on all nine cards with one reason each; EB-06/EB-07 were deferred for lack of targets, EB-08 for the 2-card limit.
- The CL stage credited existing shared products twice and added rotating pairs plus two shared charts; PB found no trade-off anywhere and abstained throughout.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-GROW-01: What Plants Need and Why Leaves Are Green and Flat

- Step 1 +EB-04: the needs explanation gained slate answers from every pupil during teaching, with re-explanation before moving on.
- Step 2 +EB-09: the leaf paragraph became asking-then-telling — pupils attempt why leaves are green and flat first, then the educator states both answers.
- CL abstained: the class chart already gives the unit its shared product (credited CL-04).

### MLS-GROW-02: Light and Growth Classroom Experiment

- Step 1 +EB-04: every pupil answers on slates which seedling will grow taller before the comparison begins.
- Step 3 +EB-09: the covered-seedling why-question is attempted first, then the precise missed-light answer is stated.
- Step 2 +CL-02: the joint height tracking gained named rotating Measurer and Recorder pairs. (CL-03/CL-04 credited for the shared observation.)
- The solo night observation from the source never entered the sequence: two shared seedlings are observed jointly in class instead.

### MLS-GROW-03: Roots and Stems Carry Water and Minerals

- Step 1 +EB-04: slate answers from every pupil during the root explanation.
- Step 3 +EB-09: the why-roots/how-water answers are attempted, then both precise answers stated.
- Step 4 +CL-04 (added step): one shared labelled diagram of the water path, each pupil adding one arrow or label, no names or marks.

### MLS-GROW-04: Seeds and Leaves Around the School

- EB abstained on all nine cards: collecting, sorting and drawing need no memory, examples, checks, grouping or mixing (EB-05 credited for the linked drawing).
- Step 5 +CL-04 (added step): leaf drawings combine into a shared class shape chart. CL-05 (showing it to another class) was deferred — the one added step was used.
