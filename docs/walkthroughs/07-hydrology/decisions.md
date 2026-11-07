# Engine decisions — Hydrology: tracking rainfall

> Run `runs/regress-3/hydrology` on 7 November 2026 via Claude Code (`claude -p`) (19 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-RAIN-01 | applied (EB-04) | abstained | abstained |
| MLS-RAIN-02 | applied (EB-03) | abstained | abstained |

- Evidence-Based reviews: round 1: REVISE; round 2: REVISE.
- Connected Learning reviews: no review call.
- Participatory Budgeting reviews: no review call.
- Repair rounds (2 late issues): round 1: REVISE; round 2: PASS.

## What the user was asked

Nothing — `--ask` did not exist when this run was made. Had it been used, the run would have asked: the unit maximum (2–5) and breakdown focus before decompose (with the source's section headings as suggestions); and before each stage, which cards may apply (with Targets lines), the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: unit maximum 5 (no enforcement beyond the critic gate's own limit), focus `auto`, every card allowed, at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose aimed at its built-in **at most 4 units**, grouping milestones by topic (`auto` focus).
- Each stage saw its full cards file and the default limits, and could abstain per unit — the table above is what it chose.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-RAIN-01: Approving, Building and Placing Rain Containers
- Step 4 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: In class, pour more clean water into one finished bottle so it stands a little above the 0 line, and show it to each row. Every student writes the depth in millimetres on scrap paper and holds it up at the same time. Look at all the answers; if many are wrong, re-explain counting millimetres up from the 0 line and repeat with a new depth. Nothing is collected or recorded.

### MLS-RAIN-02: Recording Rainfall and Calculating the Baseline
- Step 2 [repair]:
  - before: On the last school day before the first reading day, the educator empties each container and refills it to the 0 line, so the first reading counts only new rain.
  - after: On the last school day before the 4 weeks of readings begin, at reading time, the whole class goes together to the containers and the educator stays with all groups. The educator empties and refills each container to the 0 line, so the 4 weeks of readings cover 28 days. Students do not drink the water, lift the containers or touch the stones. Recording starts on the first school day of the 4 weeks.
- Step 6 [EB-03 (modified)]:
  - before: In the final week, give a full lesson for each student to calculate the baseline figures in their notebook. They work out each container's 4-week total from the weekly total rows, then the class's 4-week rainfall as the average of those container totals (leave out any container with a missing reading). The average per week is that figure ÷ 4. The average per day is that figure ÷ 28, the number of days the containers collected rain.
  - after: On the last school day, in a separate time block after that day's reading and weekly total, give a full lesson on baseline figures. On the board, work one example step by step using three containers' made-up weekly totals: total each container's weeks, average those totals (skip containers missing a reading), then divide by 4 weeks and by 28 days for the weekly and daily averages. Then each student calculates the class's figures in their notebook from the matrix.
- Step 7 [EB-03 (modified)]:
  - before: Lead the class in comparing their results and writing the agreed baseline figures on chart paper.
  - after: At the end of that lesson, lead the class in comparing their results and writing the agreed baseline figures on chart paper.
