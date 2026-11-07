# Engine decisions — Kenya: clean water and health

> Run `runs/regress-3/kenya-water` on 7 November 2026 via Claude Code (`claude -p`) (23 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-WATER-01 | applied (EB-01, EB-04) | applied (CL-02) | abstained |
| MLS-WATER-02 | applied (EB-01, EB-04) | abstained | abstained |
| MLS-WATER-03 | applied (EB-04) | abstained | abstained |
| MLS-WATER-04 | abstained | applied (CL-05) | abstained |

- Evidence-Based reviews: round 1: REVISE.
- Connected Learning reviews: round 1: REVISE; round 2: REVISE.
- Participatory Budgeting reviews: no review call.
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

### MLS-WATER-01: How Germs Get into Water
- Step 2 [EB-04 (modified)]:
  - before: Explain that water collected safely can become unsafe again if it is stored in an open bucket or scooped out with a cup that hands have touched. Add a second column to the chart, 'How to stop germs', with three ways: wash hands, cover containers, and pour water or use a long-handled ladle instead of scooping with a cup.
  - after: Explain that safely collected water can become unsafe again in an open bucket or when scooped out with a cup hands have touched. Ask if scooping with a cup is safe: all learners at once show one finger for yes, two for no. Look at every hand; if many show one, explain again. Add a second chart column, 'How to stop germs': wash hands, cover containers, and pour or use a long-handled ladle instead of scooping with a cup.
- Step 3 [EB-01 (modified)]:
  - before: Each learner writes three ways germs get into drinking water and three ways to stop them in their exercise book, then checks the list against the class chart.
  - after: With the class chart covered, each learner writes from memory three ways germs get into drinking water and three ways to stop them in their exercise book. Then uncover the chart so each learner checks their own list against it. Nothing is collected or marked.
- Step 4 [repair]:
  - before: Before the next lesson, collect water from a few different spots along the lake shore in clean jars with lids, so each group gets two or three jars. Mark each lid with the spot the water came from.
  - after: Before the next lesson, collect water from two or three different water sources you can reach near the school (for example a tap, a stored container, a well, or a stream, pond, river or lake) in clean jars with lids, so each group gets two or three jars. Wipe the outside of each jar dry and close the lids tightly. Mark each lid with where the water came from.
- Step 5 [CL-02 (modified)]:
  - before: In groups, learners compare their jars by colour and smell. They hold each jar up to the light to see the colour and open the lid only to smell. They do not taste the water or put their fingers in it. One learner from each group reports the results, and the educator writes them in a class table on chart paper.
  - after: In groups, learners compare jars by colour and smell, swapping roles for each jar: the Holder holds it to the light, the Smeller opens the lid only to smell, and the Reporter tells the results, which the educator writes in a class table on chart paper. Learners do not taste the water or put their fingers in it. Afterwards, every learner washes their hands with soap and water, and the educator closes the jars and pours the water away.

### MLS-WATER-02: Filtering and Disinfecting Water
- Step 1 [EB-04 (modified)]:
  - before: Recall from MLS-WATER-01: point to the class chart showing how germs get into water and that clear water can still carry germs. Explain that filtering removes mud and some dirt but not all germs.
  - after: Recall from MLS-WATER-01: point to the class chart showing how germs get into water and that clear water can still carry germs. Explain that filtering removes mud and some dirt but not all germs. Then every learner answers at once by holding up fingers: one if filtered water is safe to drink, two if it still needs more treatment. Look at all the hands, and explain again if many are wrong before moving on.
- Step 7 [EB-01 (added)]:
  - before: (added — no earlier text)
  - after: In week 3, open two lessons with three questions answered from memory on scrap paper, with the chart covered and exercise books closed: what a filter removes, why filtered water is not yet safe to drink, and how long to boil water. Then show the answers so each learner checks their own. Nothing is collected or marked.

### MLS-WATER-03: Clean Hands and Covered Containers
- Step 4 [EB-04 (modified)]:
  - before: Explain that drinking water should be kept in a covered container and poured out or taken with a long-handled ladle, never scooped out with a cup. Use a covered bucket of water to show both safe ways: pour some out, then take some with a long-handled ladle, putting the cover back each time.
  - after: Explain that drinking water should be kept covered and poured out or taken with a long-handled ladle, never scooped out with a cup. Use a covered bucket of water to show both safe ways, putting the cover back each time. Then every learner shows at once with fingers which way is unsafe: 1 pour, 2 ladle, 3 scoop with a cup. Look at all the hands and, if many are wrong, show both ways again.

### MLS-WATER-04: Writing a Safe-Water Guide for a Younger Child
- Step 5 [CL-05 (added)]:
  - before: (added — no earlier text)
  - after: Arrange a 10-minute session with a younger class in the classroom, with the educator present. Pairs take turns reading their final guides aloud to a small group of younger children and showing the labelled drawing. Reading is a choice: a learner may lay the guide on the desk for the children to look at, or keep it and just listen.
