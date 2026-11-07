# Engine decisions — Ghana: local government and community development

> Run `runs/regress-3/ghana-assembly` on 7 November 2026 via Claude Code (`claude -p`) (19 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-COMDEV-01 | applied (EB-01, EB-05) | abstained | abstained |
| MLS-COMDEV-02 | applied (EB-03, EB-04) | abstained | applied (PB-03, PB-05) |
| MLS-COMDEV-03 | abstained | applied (CL-05) | abstained |

- Evidence-Based reviews: round 1: REVISE.
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

### MLS-COMDEV-01: How the Local Council Works and What Our Community Needs
- Field `macro_alignment` (repair):
  - before: "Gives pupils the roles of the council member, community committee and development plan, and a ranked class list of real community needs to choose among."
  - after: "Gives pupils the roles of the council member, community committee and development plan, and a class list of real community needs, with the most urgent ones marked, to choose among."
- Step 1 [EB-05 (modified)]:
  - before: Explain on the chalkboard how a local council works. Each area elects one council member, and the government appoints other members. A chief administrator runs the council's work, and community committees bring each community's needs to the council. The council writes a development plan for several years, decides each year which projects to fund, and reports at town hall meetings where it says how money was spent and residents ask questions.
  - after: Explain how a local council works, drawing a council box above community circles on the chalkboard. Each area elects one council member, the government appoints others, and a chief administrator runs its work. Draw arrows up, saying they are community committees bringing local needs, and arrows down, saying they are projects funded yearly from the council's several-year development plan. Write town hall meeting beside the down arrows and say the council reports spending there and residents ask questions.
- Step 6 [EB-01 (added)]:
  - before: (added — no earlier text)
  - after: At the start of the last lesson in week 2, with notebooks closed and the chalkboard diagram rubbed off, ask three questions pupils answer from memory on scrap paper: what the elected council member does, what a community committee does, and what a development plan is. Then give the answers so each pupil checks their own. Nothing is collected, marked or recorded.

### MLS-COMDEV-02: Projects, Costs and Deciding Together
- Step 1 [EB-03 (modified)]:
  - before: Explain that a national development fund gives each local council money for development. Write this example on the chalkboard: the council has 500,000 units for new projects this year. A borehole costs 120,000, a footbridge 200,000, streetlights 90,000, a clinic extension 300,000, a library room 150,000 and a market shed 80,000.
  - after: Explain that a national development fund gives each local council money for development. Write this example on the chalkboard: the council has 500,000 units for new projects this year. A borehole costs 120,000, a footbridge 200,000, streetlights 90,000, a clinic extension 300,000, a library room 150,000 and a market shed 80,000. Then work one set aloud, step by step: borehole 120,000 plus footbridge 200,000 makes 320,000, plus streetlights 90,000 makes 410,000, which is within 500,000.
- Step 2 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Write one more set on the chalkboard: clinic extension, footbridge and market shed. Every pupil writes the total and "fits" or "too much" on scrap paper and holds it up at the same time. Look at all the papers; if many are wrong, work the sum again on the board before moving on. Nothing is collected or recorded.
- Step 4 [PB-03 (modified)]:
  - before: Hold a class vote on which project the council should fund first. Each pupil votes for one project by show of hands, and you record the class total for each project as tally marks on the chalkboard. The project with the most votes wins.
  - after: Hold a mock class vote on which project the council should fund first, announcing both counting rules before any hands go up. Single choice: each pupil raises a hand for one project only; approval: each pupil raises a hand for every project they accept. Record each count's class totals as tally marks on the chalkboard.
- Step 5 [PB-05 (added)]:
  - before: (added — no earlier text)
  - after: On chart paper, write both counting rules, the winning project under each rule, and that the class next discusses whether the result is fair. Write only class totals, never who voted for what.

### MLS-COMDEV-03: Writing and Revising a Letter to the Council Member
- Step 5 [CL-05 (added)]:
  - before: (added — no earlier text)
  - after: Arrange a 10-minute session with another class in the classroom, with the educator present. Pairs take turns reading their final letters aloud to a small group of listeners from the other class. Reading is a choice: a pupil may lay the letter on the desk for listeners to read, or keep it and just listen.
