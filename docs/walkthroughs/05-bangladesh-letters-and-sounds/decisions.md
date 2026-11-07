# Engine decisions — Bangladesh: letters, sounds and first words

> Run `runs/regress-3/bangladesh-letters` on 7 November 2026 via Claude Code (`claude -p`) (21 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-LETTERS-01 | applied (EB-01, EB-04) | abstained | abstained |
| MLS-LETTERS-02 | applied (EB-01, EB-02) | abstained | abstained |
| MLS-LETTERS-03 | applied (EB-04) | abstained | abstained |
| MLS-LETTERS-04 | abstained | abstained | abstained |

- Evidence-Based reviews: round 1: REVISE; round 2: REVISE.
- Connected Learning reviews: no review call.
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

### MLS-LETTERS-01: Sounds of the First Four Letters
- Step 4 [EB-04 (modified)]:
  - before: Show two pictures of things whose names start with the letter's sound. Draw them on the board or on reused card.
  - after: Show two pictures of things whose names start with the letter's sound. Draw them on the board or on reused card. Then say two more words, one that starts with the sound and one that does not, and every child shows thumbs up or thumbs down for each at the same time. Look at all the thumbs without naming anyone, and if many are wrong, say the sound with the pictures again before moving on.
- Step 6 [EB-01 (added)]:
  - before: (added — no earlier text)
  - after: In week 2, open two lessons with a few minutes of recall of the two week-1 letters, with the letter cards out of sight. Say their sounds four times in mixed order (first, second, second, first), and children write each letter on their slates from memory. After each one, show its card so every child checks their own slate. Nothing is collected, marked or recorded.

### MLS-LETTERS-02: Sounds of Letters Five to Eight
- Step 1 [EB-01 (modified)]:
  - before: Recall from MLS-LETTERS-01: put the four letter cards on the board in textbook order, so the new letter follows them. Show the fifth letter on a new card made from reused cardboard. Say its sound clearly, and have the whole class say the sound back three times.
  - after: Recall from MLS-LETTERS-01: with the four letter cards hidden, say each card's sound while children write its letter on their slates from memory, then show that card so each child checks their own slate. No results are collected or recorded. Put the four cards on the board in textbook order, then show the fifth letter on a new card made from reused cardboard. Say its sound clearly, and have the whole class say the sound back three times.
- Step 6 [EB-02 (added)]:
  - before: (added — no earlier text)
  - after: In the last two lessons of week 2, open each lesson by saying the sounds of letters five and six one at a time, with their cards turned face down. Children write each letter on their slates from memory, then show its card so each child checks their own slate. No results are collected or recorded.

### MLS-LETTERS-03: Blending Sounds into Short Words
- Step 3 [EB-04 (modified)]:
  - before: Blend five words this way each day. When the class learns a new letter, words from the next day on may use it.
  - after: Blend five words this way each day. Have children read the fifth word silently, then say two words aloud, one of them the word on the board, and all children at once hold up one finger for the first or two for the second. Look at all the hands; if many are wrong, blend it again before moving on, without naming anyone. When the class learns a new letter, words from the next day on may use it.

### MLS-LETTERS-04: Reading Words and a Sentence Aloud
- Step 5 [repair]:
  - before: Before the last lesson, write short sentences on chart paper, using only words the class has learned. Write one sentence for each child.
  - after: Before the last lesson, write short sentences on strips of reused paper or card, or on the board, using only words the class has learned. Write one sentence for each child.
