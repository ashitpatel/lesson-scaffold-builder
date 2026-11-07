# Walkthrough 2 — Peru: fractions in the market and the garden

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 7 November 2026 (`python3 -m lsb.regress`, folder `runs/regress-3/peru-fractions`). The source chapter is an original test input written for this project and set in a Peruvian primary school: [tests/fixtures/peru-fractions-source.md](../../tests/fixtures/peru-fractions-source.md). No teacher has reviewed the result yet.

| | |
|---|---|
| **Source** | A 6-week Grade 5 mathematics unit, "Fractions in the Market and the Garden", from a regional edition of the national curriculum |
| **Result** | Passed: 3 units, 6 weeks in all, 17 model calls, about $3.60 at list price |
| **Kept** | Folding paper strips, equivalent fractions, comparing and adding, the class garden bed, the poster |
| **Removed** | Pupils bringing and spending money at a named market; homework on the family's harvest income; test scores posted by name on a wall chart; a two-session lecture on the history of measuring; the region's currency, curriculum body and education office |
| **Added** | Whole-class checks and recall from memory (evidence-based); a showcase for a younger class (Connected Learning); a class vote on the garden bed, with the rule announced first (participatory budgeting) |

## 1. The starting point
A teacher's guide for six weeks of 45-minute sessions. It defines a fraction, opens with a two-session lecture on how the Inca measured land and kept accounts on knotted cords, then folds paper strips into halves, quarters and eighths to find equivalent fractions, and compares and adds fractions. Then it sends pupils to a named market with 5 soles from home to buy potatoes, asks for the family's harvest earnings as homework, divides the class's own garden bed among three crops (the teacher decides), posts weekly test scores by name "so that pupils can see who is ahead", and ends with each pupil's poster.

## 2. What the pipeline kept, and why
- **The definition section (§4.1) was folded in, not deferred.** Every unit and the poster rely on numerator and denominator, so they're taught in unit 1 step 1, including the source's own example of a potato cut into unequal pieces.
- **The folded strips run through the whole sequence.** Pupils keep them in their notebooks for unit 2.
- **The garden bed stays, as the source's real trade-off.** 8 squares, with minimums for potatoes (2), broad beans (1) and maize (3), leave 2 squares the crops compete for.
- **Sustained work stays.** A full lesson of comparing and adding exercises; two full lessons for the draft poster; a full lesson to correct it.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Pupils bring S/ 5 from home and buy food at a named market (§4.5) | Left out; listed as a follow-on only if reworked as numbers on paper | Students never handle real money; an off-site trip; one locality's market and currency |
| Homework: ask parents what the family earned from the harvest (§4.5) | Left out | Household financial data about a child's family |
| Weekly scores written next to each pupil's name "so pupils can see who is ahead" (§4.7) | Left out | Individual performance records, displayed and ranked |
| Two-session lecture on the history of measuring, with a drawing to copy (§4.2) | Set aside as lecture only | No unit needs it |
| The national curriculum body, the regional education office, a named market, the currency | Replaced with generic wording | Cards stay region-neutral; code fails any currency left in |

All four problems were also reported as **source flags** for the adapter.

## 4. The units

```
MLS-FRAC-01  What a fraction is; folding equivalent fractions (2 weeks)
     │
     ▼
MLS-FRAC-02  Comparing and adding fractions (2 weeks)
     │
     ▼
MLS-FRAC-03  Sharing the garden bed; the fraction poster (2 weeks)   ← also builds on FRAC-01
```

## 5. What each stage did

**Evidence-Based (ran first), applied in all three units.**
- **EB-04 Checking for understanding**, in units 1 and 2: after the worked examples, every pupil writes an answer on scrap paper and holds it up at the same time (a fraction equivalent to 3/5; 1/6 + 4/6). The educator looks at all of them and re-explains with another example if many are wrong. Nothing is recorded and no one is named.
- **EB-01 Retrieval practice**, in units 2 and 3: in week 2, and again at the start of unit 3, three questions answered from memory with strips and notebooks put away, then the answers shown so each pupil checks their own.
- **Credited, not added:** the strips and the shaded shape already link pictures to symbols (EB-05); the four worked examples already come before practice (EB-03).
- **Deferred, with reasons:** spacing inside unit 1 (EB-02) would have fallen outside its 2 weeks, so it went to unit 3's recall instead.

**Connected Learning, applied in unit 3 only.**
- **CL-05 Real audience:** a 10-minute visit by a younger class to see and hear about the posters, with the educator present. Showing a poster is each pupil's choice.
- Units 1 and 2 **abstained**: a theme choice or a class chart would have rewritten the skill practice or added a product no later unit uses.

**Participatory Budgeting, applied in unit 3 only.**
- **PB-04 Shared resource round:** in the source, the teacher decides how the 2 free squares are shared. Now the class votes by show of hands, with the rule said before any hand goes up (most hands gets the first free square, second-most the second, ties re-voted), and the totals, the rule and the result written on chart paper (PB-05, folded into the same step).
- Units 1 and 2 **abstained**: "the fit-gate fails", because the unit has no fixed amount with more options than fit. A made-up budget ledger would practise totalling, not equivalent fractions, and would replace the unit's own practice.

## 6. What the reviewers caught
The decompose review passed the first attempt. The reviews after the Connected Learning and participatory-budgeting stages then found six problems in steps no stage had changed (**late issues**), and one repair round fixed them all:
- **Textbook pages:** practice steps pointed at "the twenty exercises on page 84 of the textbook", which another classroom won't have. Repaired: "exercises the educator writes on the board, or takes from the class textbook if it has them", with examples.
- **One step doing two things:** unit 3 step 1 combined the recall quiz with drawing the garden grid. Repaired: the grid has its own step.
- **No garden bed:** many schools have none, and the vote would then be about a bed that doesn't exist. Repaired: "If the class has no garden bed, say it is an imagined bed and a practice decision."

The participatory-budgeting edit itself was rejected once by the code check, which found two change-log entries for one step. The stage's retry passed.

## 7. Before → after (unit 3)

| Before (after decompose) | After |
|---|---|
| A spoken reminder of earlier rules, plus drawing the garden grid, in one step | Three recall questions from memory, self-checked (EB-01); the grid in its own step, with "imagined bed" if there's none (repair) |
| The educator decides how the 2 free squares are shared | A show-of-hands round with the rule announced first; totals and result on chart paper (PB-04, PB-05) |
| Poster drafted, checked by a partner, corrected | Unchanged |
| — | A younger class visits to see the posters, by each pupil's choice (CL-05) |

## 8. Teacher card (unit 3, from `cards.txt`)

```
MLS-FRAC-03: Sharing the Garden Bed and the Fraction Poster
2 weeks. Builds on MLS-FRAC-01, MLS-FRAC-02.
==============================================================================
Goal: Applies representing, equivalent fractions and adding to describe how
the class garden bed is shared, ending in each pupil's own corrected poster.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Recall from MLS-FRAC-01: with notebooks and strips put
[changed: EB-01]      away, pupils write from memory on scrap paper an
                      equivalent fraction for 3/4, then, from MLS-FRAC-02, the
                      bigger of 2/3 and 2/5, and 2/8 + 3/8. Show the answers
                      and the rules behind them, and each pupil checks their
                      own. Nothing is collected or marked.

2. Lead Educator      Draw the garden bed on the board as a grid of 8
                      one-metre squares, 4 long and 2 wide. Write on the board
                      that this term the class can plant potatoes (at least 2
                      squares), broad beans (at least 1) and maize (at least
                      3), and the other 2 can go to any crop. If the class has
                      no garden bed, say it is an imagined bed and a practice
                      decision; the shares and poster stay the same.

3. Lead Educator      Say the rule before voting: each pupil raises one hand
[changed: PB-04]      for one crop; most hands gets the first free square,
                      second-most gets the second, and ties are re-voted.
                      Count class totals, with no names. Write the totals, the
                      rule and each crop's squares for planting on chart
                      paper, and label the grid. Pupils write each crop's
                      share as a fraction of the bed in their notebook, for
                      example 3/8 for 3 squares of maize.

4. Lead Educator      Give two full lessons for each pupil to make a draft
                      poster on chart paper or reused paper, with their name
                      on it. ...

5. Peer Facilitator   In pairs, each pupil explains their draft poster to
                      their partner. ... Then partners swap roles.

6. Lead Educator      Give a full lesson for each pupil to correct the
                      mistakes their partner found and make the final copy of
                      their poster.

7. Lead Educator      Arrange a 10-minute visit by a younger class to the
[changed: CL-05]      classroom, with the educator present. ... Showing a
                      poster is each pupil's choice ...
------------------------------------------------------------------------------
BEFORE YOU START
- Needs: Enough chart paper or large reused sheets for one poster per pupil.
  If not: Pupils make the poster on a double page of their notebook or on the
  back of an old sheet of paper.
- Needs: Two full school weeks are available without a holiday or closure.
  If not: If a week is lost, do steps 1 to 3 in one period and give one lesson
  instead of two for the draft poster in step 4.
```
*(Steps 4–7 shortened here; the full card is in the run folder.)*

## 9. What to watch for
- **Seven steps in two weeks is full.** Two lessons of drafting plus a correction lesson plus a visit: check it fits a real timetable.
- **The vote decides only 2 squares.** That's the honest size of the trade-off, but a class may find it small; the "imagined bed" fallback keeps it a practice decision.
- **The EB change note for step 1 is stale.** It says the grid drawing was "kept unchanged" in step 1; the repair later moved it to its own step. The step itself is right; the logged summary predates the repair.
- **Unit 3 lists unit 1 as a prerequisite as well as unit 2**, which is redundant (unit 2 already depends on unit 1) but harmless.
