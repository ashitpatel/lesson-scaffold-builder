# Engine decisions — Pond management

> Run `runs/snail-pond-live-1` on 8 November 2026 via Muse (18 model calls). Run without `--ask`: nothing was asked; every choice below is the pipeline default. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-POND-01 | applied (EB-01, EB-04) | applied (CL-02) | abstained |
| MLS-POND-02 | applied (EB-04) | applied (CL-02) | abstained |
| MLS-POND-03 | applied (EB-01, EB-04) | abstained (credited CL-03, CL-04) | abstained |
| MLS-POND-04 | applied (EB-04) | abstained (credited CL-05) | abstained |

- Evidence-Based reviews: round 1: PASS.
- Connected Learning reviews: round 1: PASS.
- Decompose review: round 1: REVISE (1 blocker, G05 off-site role); round 2: PASS. No late issues, no repair.

## What the user was asked

Nothing — the run did not use `--ask`. Had it been used, the run would have asked: framework exclusions at the outset; single-vs-multi MLS with max units, breakdown focus and max weeks; and before each stage, which cards may apply, the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: no exclusions, multi-MLS up to 5 units, `auto` focus, up to 4 weeks per unit, every card allowed (EB-01 to EB-09), at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose built 4 units from the seven sections, grouping by phase: uses+values, field sketching+survey, pooling+analysis, design+action. It deferred the town-schools variant (§7) as a follow-on candidate, converted home-pond study to supervised whole-class visits with class totals, and stripped locale names to generic labels.
- The EB stage put a slate check (EB-04) on every explanation in all four units and added self-checked week-2 recall (EB-01) in units 1 and 3; it credited EB-05 twice and EB-02 once, and deferred the rest for card/step limits or lack of targets.
- The CL stage added rotating peer roles in units 1–2 and abstained units 3–4 with credits for work already shared; PB found no trade-off anywhere and abstained throughout.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-POND-01: Pond Uses and Community Values

- Step 1 +EB-04: the uses explanation (list slightly shortened) gained slates from every student listing two uses, with missing uses re-explained if many are wrong.
- Step 2 +CL-02 (now Peer_Facilitator): teacher copying became mixed groups pooling the items with rotating Reader, Writer and Checker roles, swapping for each item.
- Step 4 +EB-01 (added step): week-2 recall of uses and sayings from memory on slates, self-checked, nothing collected or recorded.
- Step 3 (pairs sort, count, build one class table) unchanged.

### MLS-POND-02: Sketching Ponds and Surveying Use

- Step 1 +EB-04: every student holds up a slate naming the four sketch items before the first visit, with missed items re-explained.
- Step 2 +CL-02: the sketch task gained rotating Measurer, Recorder and Checker roles swapping each visit.
- The home-pond study from the source never entered the sequence: educator-assigned ponds are visited by the whole class together instead, with class totals and no names or home details.

### MLS-POND-03: Pooling Findings and Analysing Pond Health

- Step 1 +EB-04: every student holds up a slate naming one pollutant during the pooling explanation, with re-explaining before moving on.
- Step 5 +EB-01 (added step): week-2 recall of pollutants and protections from memory on scrap paper, self-checked, nothing collected or recorded.
- CL abstained: pooling already builds shared charts, graphs, diagrams and a class tally (credited CL-03, CL-04).

### MLS-POND-04: Pond Design and Action Plan

- Step 1 +EB-04: every student shows the well-managed pond features on slates together, with missed features re-explained before group design.
- CL abstained: the posters and shared report already go to readers beyond the teacher (credited CL-05); EB-05 credited for the features paired with charts and a named pond model.
