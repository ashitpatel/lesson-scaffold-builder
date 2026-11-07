# Engine decisions — Vietnam: folk tales and retelling

> Run `runs/regress-3/vietnam-folktales` on 7 November 2026 via Claude Code (`claude -p`) (22 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-FOLK-01 | applied (EB-01, EB-04) | abstained | abstained |
| MLS-FOLK-02 | applied (EB-04) | abstained | abstained |
| MLS-FOLK-03 | applied (EB-02) | abstained | abstained |
| MLS-FOLK-04 | abstained | applied (CL-04) | abstained |

- Evidence-Based reviews: round 1: REVISE.
- Connected Learning reviews: round 1: REVISE.
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

### MLS-FOLK-01: Folk Tale Structure and Story Maps
- Step 2 [EB-04 (added)]:
  - before: (added — no earlier text)
  - after: Ask two questions every pupil answers at once: which part 'and the kind brother lived happily ever after' belongs to, shown with one, two or three fingers for beginning, middle or ending; and the character type of a younger sister who shares her bread with a stranger, written on scrap paper and held up. Look at all the answers. If many are wrong, re-explain from the chart before the reading; otherwise move on. Nothing is recorded.
- Step 7 [EB-01 (modified)]:
  - before: Using the class chart, ask pupils to name the beginning, middle and ending in each of their two story maps. Each pupil writes the character type next to each main character on their story maps.
  - after: With the class chart covered and textbooks closed, each pupil marks the beginning, middle and ending on each of their two story maps and writes the character type next to each main character, from memory. Then uncover the chart so each pupil checks and corrects their own maps. Nothing is collected or marked.

### MLS-FOLK-02: Character and Lesson
- Step 1 [EB-04 (modified)]:
  - before: Recall from MLS-FOLK-01: pupils open their story maps for both tales. Lead a class discussion on what kind of person the fisherman is, using evidence from the story: what he says and what he does. Pupils find the lines in the textbook that show it.
  - after: Recall from MLS-FOLK-01: pupils open their story maps for both tales. Lead a class discussion on what kind of person the fisherman is, using evidence from the story: what he says and what he does. Then each pupil writes on scrap paper one word for his character and key words from a line showing it, and all hold them up together. Look at every paper without collecting it; if many lack evidence, reread a key line together.

### MLS-FOLK-03: Retelling Aloud and Collecting a Tale by Word of Mouth
- Step 1 [EB-02 (modified)]:
  - before: Recall from MLS-FOLK-01: each pupil chooses one of the two tales and takes out its story map. Pupils put the textbook away. From now on they retell from the story map only.
  - after: Recall from MLS-FOLK-01: with the class chart covered and notebooks closed, each pupil writes the three parts of a folk tale and two character types from memory on scrap paper, then the chart is uncovered so each pupil checks their own; nothing is collected. Each pupil then chooses one of the two tales and takes out its story map. Pupils put the textbook away. From now on they retell from the story map only.
- Step 2 [repair]:
  - before: Ask each pupil to ask a grandparent or another older person in their own household to tell them a folk tale, and to write the tale down in their notebook within one week. Pupils write down only the tale, not details about their family or home.
  - after: In a lesson early in the week, the Lead_Educator tells one folk tale aloud from memory to the whole class, and every pupil writes it in their notebook. Each pupil then chooses which tale to keep: this one, one they have heard told before, or one from an older person at home. Pupils never visit neighbours or others outside their household and write only the tale. Don't ask who lives at home, why, or which option was used.

### MLS-FOLK-04: Writing and Revising Our Own Folk Tale
- Step 6 [CL-04 (added)]:
  - before: (added — no earlier text)
  - after: Gather the pupils' final copies into one class book of folk tales, with no choosing of best tales, no order of quality, and no marks or comments on any page. Fold a sheet of chart paper as the cover and tie the pages in with reused string. A pupil may leave their name off their tale or keep it out of the book. Keep the book in the classroom for pupils to read.
