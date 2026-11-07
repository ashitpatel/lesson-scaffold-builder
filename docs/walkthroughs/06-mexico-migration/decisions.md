# Engine decisions — Mexico: migration stories, past and present

> Run `runs/regress-3/mexico-migration` on 7 November 2026 via Claude Code (`claude -p`) (13 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-MIGRATE-01 | applied (EB-04) | abstained | abstained |
| MLS-MIGRATE-02 | applied (EB-01, EB-04) | abstained | abstained |
| MLS-MIGRATE-03 | abstained | applied (CL-04) | abstained |

- Evidence-Based reviews: round 1: PASS.
- Connected Learning reviews: round 1: PASS.
- Participatory Budgeting reviews: no review call.
- Repair: none needed (no late issues).

## What the user was asked

Nothing — `--ask` did not exist when this run was made. Had it been used, the run would have asked: the unit maximum (2–5) and breakdown focus before decompose (with the source's section headings as suggestions); and before each stage, which cards may apply (with Targets lines), the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: unit maximum 5 (no enforcement beyond the critic gate's own limit), focus `auto`, every card allowed, at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose aimed at its built-in **at most 4 units**, grouping milestones by topic (`auto` focus).
- Each stage saw its full cards file and the default limits, and could abstain per unit — the table above is what it chose.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-MIGRATE-01: Push and Pull Factors in Primary Sources
- Step 2 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Before students read the sources, read out three short reasons for moving, such as "the rains failed for three years" or "an uncle has work waiting in the city". Every student shows one finger for a push factor or two for a pull factor at the same time. Look at all the hands, and if many are wrong, re-explain using the class chart before moving on. Nothing is recorded and no one is named.

### MLS-MIGRATE-02: Building a Migration Timeline from 1900 to Today
- Step 1 [EB-04 (modified)]:
  - before: Recall from MLS-MIGRATE-01: use the class chart of push and pull factors and each student's notebook answers on the three sources. Give a short talk on the great migrations in the textbook chapter. Write the key dates on the board and draw a map of the routes. Students copy the dates and the map into their notebooks.
  - after: Recall from MLS-MIGRATE-01: use the class chart of push and pull factors and each student's notebook answers on the three sources. Give a short talk on the great migrations in the textbook chapter, with key dates on the board and a map of the routes. After each migration, every student holds up scrap paper naming one of its push factors; look at all answers and re-explain if many are wrong. Students copy the dates and map into their notebooks.
- Step 5 [EB-01 (added)]:
  - before: (added — no earlier text)
  - after: In week 2, open two lessons with three questions on push and pull factors and the migrations from the talk, answered from memory on scrap paper with the chart and notebooks put away. Then show the answers so each student checks their own. Nothing is collected or marked.

### MLS-MIGRATE-03: Writing and Revising an Explanation of a Migration
- Step 6 [CL-04 (added)]:
  - before: (added — no earlier text)
  - after: Collect every final copy and, with the class, tie the pages together with string inside a cover made from used paper to make one class book of migration explanations. Each student may write their name on their own pages or leave it off. Add no marks or comments, and keep the book in the classroom for students to read.
