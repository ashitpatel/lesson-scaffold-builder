# Engine decisions — Snail: water source mapping

> Run `runs/snail-mapping-live-1` on 8 November 2026 via Muse (`muse exec`) (13 model calls). Run without `--ask`: nothing was asked; every choice below is the pipeline default. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-WATER-01 | applied (EB-01, EB-04) | abstained (credited CL-03, CL-05) | abstained |
| MLS-WATER-02 | applied (EB-01, EB-04) | applied (CL-02) | abstained |
| MLS-WATER-03 | applied (EB-03, EB-04) | applied (CL-02) | abstained |

- Evidence-Based reviews: round 1: PASS.
- Connected Learning reviews: round 1: PASS.
- Decompose review: round 1: PASS. No late issues, no repair.

## What the user was asked

Nothing — the run did not use `--ask`. Had it been used, the run would have asked: framework exclusions at the outset; single-vs-multi MLS with max units, breakdown focus and max weeks; and before each stage, which cards may apply, the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: no exclusions, multi-MLS up to 5 units, `auto` focus, up to 4 weeks per unit, every card allowed in each stage, at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose built 3 units from the six sections, grouping by activity: maps+signs, the two source visits, reports+percentages+wall map — a linear chain over 7 weeks with nothing deferred.
- The EB stage used EB-04 checks in all three units, added EB-01 recall steps in units 1–2, and worked one percent step by step (EB-03) in unit 3; EB-09 never fit because the lesson holds no precise why/how answers.
- The CL stage abstained unit 1 with two credits and added peer roles in units 2–3; PB found no trade-off anywhere and abstained throughout.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-WATER-01: Household Water Maps with Shared Signs

- Step 3 +EB-04: the signs introduction gained a slate check — every child draws the sign for three named sources, the educator looks at all slates and re-explains missed signs before redrawing.
- Step 5 +EB-01 (added step): a week-2 recall of sources, signs and summer-only meaning from memory, self-checked against shown answers, nothing collected.
- CL abstained: the maps already use everyday walking-step data (credited CL-03) and already have a peer reader (credited CL-05).

### MLS-WATER-02: Visiting Sources and Recording Surroundings

- Step 1 +EB-04: the warning-sign agreement gained a slate check — every child names two warning signs at the same time before the visits.
- Step 5 +EB-01 (added step): a week-2 recall of warning signs and clean surroundings from memory, self-checked, nothing collected.
- Steps 2–3 +CL-02: both visits gained paired observer and recorder roles, swapping at the next source and across the two visits. (CL-03 credited for the observed surroundings; CL-04 deferred — pooling happens in MLS-WATER-03.)

### MLS-WATER-03: Class Reports, Percentages and Village Facilities Map

- Step 3 +EB-03 +CL-02: the tally-and-percent step gained rotating counter/recorder pairs and one source-type percent worked fully step by step on the board first.
- Step 4 +EB-04: the village chart step gained a scrap check — every child shows the sign for one named source, missed signs re-explained before continuing.
- (CL-03/CL-04 credited for the pooled totals and wall map; CL-05 credited for the class report sharing.)
