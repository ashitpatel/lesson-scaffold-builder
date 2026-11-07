# Engine decisions — Civics: making decisions together

> Run `runs/regress-3/civics` on 7 November 2026 via Claude Code (`claude -p`) (20 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-DECIDE-01 | applied (EB-01, EB-04) | abstained | applied (PB-02) |
| MLS-DECIDE-02 | applied (EB-03, EB-04) | applied (CL-04) | abstained |
| MLS-DECIDE-03 | applied (EB-04) | abstained | abstained |
| MLS-DECIDE-04 | applied (EB-01) | applied (CL-05) | abstained |

- Evidence-Based reviews: round 1: PASS.
- Connected Learning reviews: round 1: REVISE.
- Participatory Budgeting reviews: round 1: REVISE.
- Repair rounds (3 late issues): round 1: PASS.

## What the user was asked

Nothing — `--ask` did not exist when this run was made. Had it been used, the run would have asked: the unit maximum (2–5) and breakdown focus before decompose (with the source's section headings as suggestions); and before each stage, which cards may apply (with Targets lines), the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: unit maximum 5 (no enforcement beyond the critic gate's own limit), focus `auto`, every card allowed, at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose aimed at its built-in **at most 4 units**, grouping milestones by topic (`auto` focus).
- Each stage saw its full cards file and the default limits, and could abstain per unit — the table above is what it chose.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-DECIDE-01: Why Communities Decide and Collecting School-Ground Ideas
- Step 2 [EB-04 (modified)]:
  - before: Draw a simple diagram of the local council on the board: residents elect council members for a fixed term, the council decides and reports back to residents, and officials carry out the decisions. Mention that some councils hold open meetings where residents raise needs directly. Students copy the diagram into their notebooks.
  - after: Draw a simple diagram of the local council on the board: residents elect council members for a fixed term, the council decides and reports back to residents, and officials carry out the decisions. Mention that some councils hold open meetings where residents raise needs directly. Ask who decides which projects get funded: all students together show one, two or three fingers for residents, council or officials. Scan every hand, re-explain if many are wrong, then students copy it.
- Step 4 [PB-02 (modified)]:
  - before: Collect the slips and read them out. Lead a class discussion of the ideas. Then pick the three best ideas and write them on a sheet of chart paper for the class to keep.
  - after: Collect the slips, read them out and lead a class discussion of the ideas. Before voting, state the rule: each student raises a hand once, for the idea they most want, the three with the most hands go forward, and ties go to a second show of hands. Count the hands and write on chart paper for the class to keep the three ideas, the class totals only, the rule used, and that costing comes next.
- Step 5 [EB-01 (added)]:
  - before: (added — no earlier text)
  - after: In week 2, open one lesson with four questions answered from memory on scrap paper, with notebooks closed and the board cleared: why a town cannot fund every need, who elects the council, who decides what is funded, and who carries decisions out. Then show the answers so each student checks their own. Nothing is collected or marked.

### MLS-DECIDE-02: Weighing Ideas Against a Points Budget
- Step 2 [EB-03 (modified)]:
  - before: Tell the class they have a made-up budget of 1,000 points for school-ground improvements. Write a price list on the board giving each idea a cost in points, for example benches 400, shade cloth 350, a garden bed 200, a notice board 150 and a covered waiting area 600.
  - after: Tell the class they have a made-up budget of 1,000 points for school-ground improvements. Write a price list on the board giving each idea a cost in points, for example benches 400, shade cloth 350, a garden bed 200, a notice board 150 and a covered waiting area 600. Work one combination aloud step by step: add benches, shade cloth and a notice board to get 900 points, then compare 900 with 1,000 to show it fits.
- Step 3 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Write one more combination on the board: the covered waiting area, shade cloth and a notice board. Every student writes the total and whether it fits within 1,000 points on scrap paper and holds it up. Look at all the answers, and if many are wrong, work the sum again on the board before students start. Nothing is collected or recorded.
- Step 5 [CL-04 (added)]:
  - before: (added — no earlier text)
  - after: Take about 10 minutes after the notebook work to build one class chart on chart paper listing every combination that fits within 1,000 points. Students call out combinations from their notebooks that are not yet listed, the class adds each one aloud to confirm it fits, and the educator writes it with its total. Calling out is a choice, and no names go next to any combination. Keep the chart for later units.

### MLS-DECIDE-03: Voting and Judging Whether the Vote Was Fair
- Field `macro_alignment` (repair):
  - before: "Gives students a real class decision by majority vote and the tools, such as approval voting and proportional sharing, to judge whether that process was fair."
  - after: "Has the class make its own decision among its three ideas by majority vote, then compare that result with approval voting to judge whether the process was fair."
- Step 3 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Write on the board: of five made-up voters, two accept only benches, and three accept both but prefer shade. Every student writes on scrap paper which option wins under a one-vote majority and which under approval voting, and holds it up at once. Look at all the answers; if many are wrong, re-explain with this example before moving on. Nothing is collected or recorded.

### MLS-DECIDE-04: Writing and Revising an Argument on Fair Decision-Making
- Step 1 [EB-01 (modified), repair]:
  - before: Recall from MLS-DECIDE-02: students reread the budget combinations in their notebooks. Recall from MLS-DECIDE-03: point to the vote totals chart and the fairness discussion. Write the question on the board: "Should the school grounds decision have been made by majority vote, by approval voting, or by the head of the school alone?"
  - after: Recall from MLS-DECIDE-02: cover the combinations and vote totals charts and clear the board. With notebooks closed, students write on scrap paper one combination within 1,000 points, what approval voting means, and which idea won, by how many hands. Uncover the charts and restate approval voting for self-checking; nothing is collected or marked. Write on the board: "Should the school grounds decision have been made by majority vote, by approval voting, or by the head of the school alone?"
- Step 5 [CL-05 (added)]:
  - before: (added — no earlier text)
  - after: Arrange a 10-minute session with another class in the classroom, with the educator present. Pairs take turns reading aloud the position and strongest reason from their final arguments to a small group of listeners. Reading is a choice: a student may lay the argument on the desk for listeners to read, or keep it and just listen.
