# Engine decisions — Ecosystems: energy flow and food webs

> Run `runs/regress-3/ecosystems` on 7 November 2026 via Claude Code (`claude -p`) (24 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-ECO-01 | applied (EB-04) | abstained | abstained |
| MLS-ECO-02 | applied (EB-03) | applied (CL-02) | abstained |
| MLS-ECO-03 | applied (EB-04, EB-05) | abstained | abstained |
| MLS-ECO-04 | applied (EB-04) | abstained | abstained |

- Evidence-Based reviews: round 1: REVISE; round 2: REVISE.
- Connected Learning reviews: round 1: REVISE; round 2: PASS.
- Participatory Budgeting reviews: no review call.
- Repair rounds (2 late issues): round 1: PASS.

## What the user was asked

Nothing — `--ask` did not exist when this run was made. Had it been used, the run would have asked: the unit maximum (2–5) and breakdown focus before decompose (with the source's section headings as suggestions); and before each stage, which cards may apply (with Targets lines), the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: unit maximum 5 (no enforcement beyond the critic gate's own limit), focus `auto`, every card allowed, at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose aimed at its built-in **at most 4 units**, grouping milestones by topic (`auto` focus).
- Each stage saw its full cards file and the default limits, and could abstain per unit — the table above is what it chose.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-ECO-01: Sorting the Living Things on the School Grounds
- Step 3 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Before going outside, name three familiar organisms, such as grass, a goat and a mushroom, one at a time. For each, every student holds up one, two or three fingers at the same moment for producer, consumer or decomposer. Look at all the hands, and re-explain any group that many students get wrong before moving on. No names or answers are recorded.

### MLS-ECO-02: Food Webs and Energy Pyramids
- Step 2 [CL-02 (modified)]:
  - before: Give each student a card, made from reused card or paper, naming one organism from the class list. Students stand in a circle and pass a ball of string from each organism to the things that eat it, until the string forms a web.
  - after: Give each student a card, made from reused card or paper, naming one organism from the class list. Students stand in a circle and pass a ball of string from each organism to the things that eat it, until the string forms a web. As they pass the string, each student writes on the back of their card the names of the organisms they passed it to.
- Step 4 [CL-02 (modified)]:
  - before: Students read out the links from their cards while you draw the class food web on chart paper, with an arrow from each organism to each thing that eats it. Keep this chart for the final unit.
  - after: Students read out the links from their cards in turn while two students at the chart paper build the class food web: one draws an arrow from each organism to each thing that eats it, and the other checks it against the card. After three links they swap roles, and after three more they hand over to the next two students in the circle. Check each arrow as it is drawn. Keep this chart for the final unit.
- Step 6 [EB-03 (added)]:
  - before: (added — no earlier text)
  - after: Work one food chain from the class food web on the board step by step, saying each step aloud: start with 10,000 energy units at the producer, divide by ten for each level, choose a scale so the producer bar fills the board's width, and draw each level as a bar. Then write a second chain with its last level left for students to calculate and draw in their notebooks, and show the answer.

### MLS-ECO-03: Quadrat Sampling of the School Grounds
- Step 1 [EB-05 (modified)]:
  - before: Recall from MLS-ECO-01: groups will use the class list of school-grounds organisms to name what they find. Explain that scientists cannot count every organism, so they sample. A quadrat is a square frame, usually one metre on each side, and counts from several quadrats estimate what is in the whole area.
  - after: Recall from MLS-ECO-01: groups will use the class list of school-grounds organisms to name what they find. Explain that scientists cannot count every organism, so they sample. A quadrat is a square frame, usually one metre on each side. Draw the school grounds on the board as a rectangle with four small squares in it, and explain that counts from these quadrats estimate what is in the whole rectangle.
- Step 2 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Before going outside, ask one question every student answers at once with a thumb up or down: if one quadrat has five snails, are there exactly five snails on the whole school grounds? Look at all the thumbs, and if many are up, re-explain with the board drawing before moving on. No answers are recorded or named.

### MLS-ECO-04: What If a Species Disappeared?
- Step 2 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Name one plant from the class food web. Every student writes on scrap paper one organism that would lose food without it and holds it up at the same moment; look at all the papers and re-explain if many are wrong before moving on. No names or answers are recorded.
- Step 4 [repair]:
  - before: In small groups, students discuss how each change in the case studies moved through the food web.
  - after: In small mixed groups, students discuss how each change in the case studies moved through the food web. A different student leads the discussion of each case study, so no one leads both, and everyone in the group speaks before the group moves to the next case study.
