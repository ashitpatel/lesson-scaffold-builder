# Engine decisions — Peru: fractions in the market and the garden

> Run `runs/regress-3/peru-fractions` on 7 November 2026 via Claude Code (`claude -p`) (17 model calls). This run predates `--ask`: nothing was asked; every choice below is the default the pipeline has always used. The run folder is gitignored; this file and `final.md` are the durable record.

## Frameworks the engine found relevant

| Unit | Evidence-Based | Connected Learning | Participatory Budgeting |
|---|---|---|---|
| MLS-FRAC-01 | applied (EB-04) | abstained | abstained |
| MLS-FRAC-02 | applied (EB-01, EB-04) | abstained | abstained |
| MLS-FRAC-03 | applied (EB-01) | applied (CL-05) | applied (PB-04) |

- Evidence-Based reviews: round 1: PASS.
- Connected Learning reviews: round 1: REVISE.
- Participatory Budgeting reviews: round 1: REVISE.
- Repair rounds (6 late issues): round 1: PASS.

## What the user was asked

Nothing — `--ask` did not exist when this run was made. Had it been used, the run would have asked: the unit maximum (2–5) and breakdown focus before decompose (with the source's section headings as suggestions); and before each stage, which cards may apply (with Targets lines), the cards-per-unit limit, and whether it may add a step.

## What the user answered

Defaults: unit maximum 5 (no enforcement beyond the critic gate's own limit), focus `auto`, every card allowed, at most 2 cards per unit, one added step allowed.

## Decisions the engine made from those answers

- Decompose aimed at its built-in **at most 4 units**, grouping milestones by topic (`auto` focus).
- Each stage saw its full cards file and the default limits, and could abstain per unit — the table above is what it chose.

## How the frameworks were applied (original → new)

`decomposed-sequence.json` → `sequence.json`, step by step. Only changed steps are shown; anything else is exactly as decomposed.

### MLS-FRAC-01: What a Fraction Is and Folding Equivalent Fractions
- Step 5 [EB-04 (modified)]:
  - before: Work four examples on the board of finding an equivalent fraction by multiplying the numerator and the denominator by the same number, for example 2/3 = (2×2)/(3×2) = 4/6.
  - after: Work four examples on the board of finding an equivalent fraction by multiplying the numerator and the denominator by the same number, for example 2/3 = (2×2)/(3×2) = 4/6. Then every pupil writes a fraction equivalent to 3/5 on scrap paper and holds it up at the same time. Look at all the answers, and re-explain the rule with one more example if many are wrong before moving on. Answers are not recorded and no pupil is named.
- Step 6 [repair]:
  - before: Pupils work through the twelve practice exercises on equivalent fractions from the textbook in their notebooks. Each pupil keeps their labelled strips inside their notebook for the next unit.
  - after: Pupils work in their notebooks through twelve equivalent-fraction exercises that the educator writes on the board, or takes from the class textbook if it has them, such as "write two fractions equivalent to 1/2, 2/3, 3/4 and 1/5". Each pupil keeps their labelled strips inside their notebook for the next unit.

### MLS-FRAC-02: Comparing and Adding Fractions
- Step 3 [EB-04 (modified)]:
  - before: Explain how to add fractions with the same denominator: add the numerators and keep the denominator. Show 3/8 + 2/8 = 5/8 on the board.
  - after: Explain how to add fractions with the same denominator: add the numerators and keep the denominator. Show 3/8 + 2/8 = 5/8 on the board. Then every pupil writes the answer to 1/6 + 4/6 on scrap paper and holds it up at the same time. Look at all the answers without naming anyone, and explain the rule again with a new example if many are wrong before moving on.
- Step 4 [repair]:
  - before: Give a full lesson for pupils to complete the twenty comparing and adding exercises on page 84 of the textbook in their notebooks.
  - after: Give a full lesson for pupils to complete in their notebooks twenty exercises the educator writes on the board, or takes from the class textbook if it has them: ten comparing fractions with the same denominator or the same numerator (e.g. 2/7 and 5/7, 3/4 and 3/8), and ten adding fractions with the same denominator (e.g. 2/9 + 5/9).
- Step 5 [EB-01 (added)]:
  - before: (added — no earlier text)
  - after: In week 2, open two lessons with three questions answered from memory on scrap paper, with strips, notebooks and textbooks put away: one comparing fractions with the same denominator, one comparing fractions with the same numerator, and one adding fractions with the same denominator. Then show the answers so each pupil checks their own. Nothing is collected or marked.

### MLS-FRAC-03: Sharing the Garden Bed and the Fraction Poster
- Step 1 [EB-01 (modified), repair]:
  - before: Recall from MLS-FRAC-01: a fraction names equal parts of a whole, and multiplying the numerator and denominator by the same number gives an equivalent fraction. From MLS-FRAC-02, recall adding fractions with the same denominator. Draw the class garden bed, 4 metres long and 2 metres wide, on the board as a grid of 8 squares, each 1 square metre.
  - after: Recall from MLS-FRAC-01: with notebooks and strips put away, pupils write from memory on scrap paper an equivalent fraction for 3/4, then, from MLS-FRAC-02, the bigger of 2/3 and 2/5, and 2/8 + 3/8. Show the answers and the rules behind them, and each pupil checks their own. Nothing is collected or marked.
- Step 2 [repair]:
  - before: Explain that the class can plant three crops this term: potatoes, broad beans and maize. Write on the board that potatoes need at least 2 squares, broad beans at least 1 and maize at least 3. Explain that the remaining 2 squares can go to any crop.
  - after: Draw the garden bed on the board as a grid of 8 one-metre squares, 4 long and 2 wide. Write on the board that this term the class can plant potatoes (at least 2 squares), broad beans (at least 1) and maize (at least 3), and the other 2 can go to any crop. If the class has no garden bed, say it is an imagined bed and a practice decision; the shares and poster stay the same.
- Step 3 [PB-04 (modified)]:
  - before: Decide how many squares each crop gets, keeping every minimum, and write the crop names on the grid squares. Pupils write each crop's share as a fraction of the bed in their notebook, for example 3/8 for 3 squares of maize.
  - after: Say the rule before voting: each pupil raises one hand for one crop; most hands gets the first free square, second-most gets the second, and ties are re-voted. Count class totals, with no names. Write the totals, the rule and each crop's squares for planting on chart paper, and label the grid. Pupils write each crop's share as a fraction of the bed in their notebook, for example 3/8 for 3 squares of maize.
- Step 7 [CL-05 (added)]:
  - before: (added — no earlier text)
  - after: Arrange a 10-minute visit by a younger class to the classroom, with the educator present. Pupils lay their final posters on their desks, and pairs take turns explaining to small groups of visitors how the class garden bed was shared. Showing a poster is each pupil's choice: a pupil may keep it put away and walk round with the visitors instead, and any pupil may fold their name out of sight.
