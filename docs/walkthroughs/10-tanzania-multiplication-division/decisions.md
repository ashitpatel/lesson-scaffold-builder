# Engine decisions — Tanzania: multiplication and division practice

> Run `runs/tanzania-live-2` on 8 November 2026 via Muse (`muse exec`) (23 model calls). Run without `--ask`: nothing was asked; every choice below is the pipeline default. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-MULTDIV-01 | applied (EB-04, EB-06) | applied (CL-01, CL-04) | applied (PB-01) |
| MLS-MULTDIV-02 | applied (EB-01, EB-03) | applied (CL-01) | abstained |
| MLS-MULTDIV-03 | reverted (EB-06 rejected) | applied (CL-03) | abstained |

- Decompose reviews: round 1: REVISE (G18: blocked mixed set removed method choice); round 2: PASS.
- Evidence-Based reviews: round 1: REVISE; round 2: REVISE → unit 3 reverted.
- Connected Learning reviews: round 1: PASS. Participatory Budgeting reviews: round 1: PASS.
- Repair rounds (1 late issue): round 1: REVISE (2 blocking); round 2: PASS.

## What the user was asked

Nothing — the run did not use `--ask`. Had it been used, the run would have asked: framework exclusions at the outset; single-vs-multi MLS with max units, breakdown focus and max weeks; and before each stage, which cards may apply, the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: no exclusions, multi-MLS up to 4 units, `auto` focus, 2–4 weeks per unit, every card allowed (EB-01 to EB-09), at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose built 3 units from the ten sections by operation: multiplication, division+sharing, then the mixed set on both.
- The EB stage applied new card EB-06 in unit 1 (level check + regrouped practice), credited EB-07 in unit 3 (already alternating), and deferred EB-08/EB-09 for the 2-card limit or lack of targets; its EB-06 edit to unit 3 was rejected on review and reverted.
- The CL stage added theme choice, a shared class set and real-world grounding; PB applied its mock ledger once and abstained twice.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-MULTDIV-01: Multiplying Two-Digit Numbers

- Step 1 +EB-04: two short problems solved on slates at once after the board example, with re-explanation if many are wrong.
- Step 2 +EB-06 (added step): a fresh slate level check forming two or three fluid groups, re-checked as they progress, nothing marked.
- Practice +EB-06: the twenty problems run in level sets — same skill, same minutes per group.
- Step 3 +PB-01: the practice step rewritten as a paper mock ledger (made-up 400-point budget, six costed options needing multiplication); groups choose a fitting set and say what they gave up. This replaced CL-01's sports-or-crops theme on the same step.
- Step 7 +CL-04 (added step): one solved problem per group combined into a nameless class set.

### MLS-MULTDIV-02: Division With Remainders and Sharing Problems

- Step 1 +EB-03: one complete remainder example, then a second left for pupils to finish before solo practice.
- Step 6 +EB-01 (added step): low-stakes recall of division from memory in week 3, self-checked.
- CL-01: practice sets offered as sports scores or crop counts with the same numbers.
- PB abstained: sharing mangoes equally is joint work, not a trade-off to decide.

### MLS-MULTDIV-03: Mixed Multiplication and Division Set

- EB-07 credited on step 2: the set already alternates with choose-the-method prompts after the decompose fix.
- The EB-06 edit (level grouping the mixed set) was rejected on review and the unit reverted; the leftover choose-the-method sentence without card attribution became a G14 late issue, repaired by removing the sentence.
- Step 2 +CL-03: everyday quantities and a made-up price list ground the problems.
- PB abstained: no amount with competing options.
