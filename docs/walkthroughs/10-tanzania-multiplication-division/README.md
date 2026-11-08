# Walkthrough 10 — Tanzania: multiplication and division practice

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse`, folder `runs/tanzania-live-2`). The source lesson is an original test input written for this project and set in a Tanzanian primary school: [tests/fixtures/tanzania-tables-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/tanzania-tables-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.
> Decision trace: [decisions.md](./decisions.md) · Full final cards: [final.md](./final.md)

> **Locale note:** The stripped, kept, or relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

| | |
|---|---|
| **Source** | A Grade 4 mathematics lesson, "Multiplication and Division Practice": tables, remainders, mixed sets, timed races |
| **Result** | Passed: 3 units, 8 weeks in all, 23 model calls, 799,999 input / 178,051 output tokens |
| **Kept** | The 23 × 4 example; twenty-problem practice sets; pair practice (rotating, not fixed); market-amount word problems; mango-sharing division; the Friday mixed set; peer checking without scores |
| **Removed** | Ranked scoreboard of the fastest five; a purchased workbook (with answer-copying); homework on family market earnings; fixed pairs with one worksheet for all levels; the timed race with slowest pupils named; scores with names in an outside return; a two-lesson history story; shillings, Dar es Salaam, Kariakoo, the ward office |
| **Added** | Whole-class checks, level groups and a worked remainder example (evidence-based, incl. new card EB-06); theme choice and a shared class set (Connected Learning); a mock 400-point ledger practised with multiplication (participatory budgeting) |

## 1. The starting point
A teacher's guide in ten sections. It opens with a two-lesson story of market traders memorising tables, then one board example (23 × 4) followed by twenty solo problems — with the fastest five scores ranked on the board. Division with remainders gets the same treatment, then mango-sharing word problems. Early finishers buy a workbook; the unfinished copy answers from the back. Homework asks parents for the family's weekly market earnings. Pairs are fixed all term with the stronger pupil always leading — while the register shows half the class still counts on fingers and the rest multiply fluently, all on the same worksheet. A Friday mixed set keeps multiplication and division in two labelled blocks. Fridays end with a timed table race, recorded times, the three slowest pupils named, and scores with names sent to the ward office.

## 2. What the pipeline kept, and why
- **The example-to-practice spine stayed.** 23 × 4 on the board, twenty similar problems, pair practice, word problems, peer checking — the unit's own progression, kept in order.
- **The mixed set stayed, but unblocked.** The first attempt kept the Friday worksheet as two labelled blocks; the critic failed it (G18: box-ticking without choosing a method) and the second attempt interleaved all twenty problems with choose-the-method prompts.
- **Mango sharing stayed concrete.** Ten division word problems about sharing mangoes equally among baskets, kept as the division unit's application.
- **Checking stayed peer-based and unrecorded.** Notebook exchange against a board answer chart, with "no scores recorded or announced" now explicit.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Fastest five scores ranked on the board (§2b) | Left out | Individual performance records, displayed and ranked |
| Workbook to buy; copying answers when unfinished (§4) | Left out; board problems plus completion time | A purchase; copying answers teaches nothing |
| Homework: family market earnings brought to class (§5b) | Left out; teacher-provided amounts instead | Household financial data about a child's family |
| Fixed pairs, one worksheet for all levels (§7b) | Replaced with fluid level groups (EB-06) | A fixed stronger-leader pair entrenches the gap it hides |
| Timed race, recorded times, slowest named (§9) | Left out | Timed ranking by name; break-time punishment |
| Every score with names in an outside return (§10b) | Left out | Child-level performance records leaving the classroom |
| Two-lesson trader story (§1) | Set aside as lecture only | No unit needs it |
| Shillings, Dar es Salaam, Kariakoo, the ward office | Replaced with generic wording | Cards stay region-neutral |

No source flags were filed on this run — Muse's critic reported nothing while still removing all seven traps (no trap term survives in the final sequence).

## 4. The units

```
MLS-MULTDIV-01  Multiplying two-digit numbers (3 weeks)
     │                    ╲
     │                     ╲
     ▼                      ▼
MLS-MULTDIV-02  Division with remainders; sharing problems (3 weeks)
     │
     ▼
MLS-MULTDIV-03  Mixed multiplication and division set (2 weeks)
```

Unit 3 builds on units 1 and 2, which can run in either order.

## 5. What each stage did

**Evidence-Based, applied in all three units.**
- **EB-06 Level groups (new card)**, in unit 1: a fresh slate check in week 1 forms two or three fluid groups, re-checked as they progress, and the twenty-problem practice runs in level sets — same skill, same minutes, nothing marked. Applied, not forced: the register's level spread is stated in the source.
- **EB-04 Checking for understanding**, in unit 1: two short problems solved on slates at once after the board example.
- **EB-03 Worked examples**, in unit 2: one complete remainder example, then a second left for pupils to finish before solo practice.
- **EB-01 Retrieval practice**, in unit 2: low-stakes recall of division from memory in week 3, self-checked.
- **EB-07 credited, not added**, in unit 3: the mixed set already alternates with choose-the-method prompts after the decompose fix, so there was nothing left to interleave.
- **Unit 3's EB-06 edit was reverted**: the EB review rejected it and the unit fell back to its pre-stage steps; the G14 late issue it left behind (a choose-the-method sentence without card attribution) was repaired by removing the sentence.
- **EB-08/EB-09 deferred** with reasons: the 2-card limit was reached, or (unit 3) there are no facts with precise lesson answers to interrogate.

**Connected Learning, applied in all three units.**
- **CL-01 Interest**, in units 1–2: the same practice sets offered as sports scores or crop counts, same numbers, same answer chart.
- **CL-04 Shared purpose**, in unit 1: one solved problem per group combined into a nameless class set.
- **CL-03 Real-world context**, in unit 3: everyday quantities and a made-up price list ground the mixed set.

**Participatory Budgeting, applied in unit 1 only.**
- **PB-01 Knapsack ledger:** the practice step became a paper mock ledger — a made-up 400-point budget, six costed options needing two-digit multiplication, groups choosing a fitting set and saying what they gave up. Mock points, real arithmetic; units 2–3 abstained (no trade-off).

## 6. What the reviewers caught
- **Decompose took two attempts.** The first kept the Friday mixed set as two labelled blocks; the critic failed it (G18) for removing method choice, and the second attempt interleaved all twenty problems — which is why EB-07 later had only a credit.
- **One late issue, two repair rounds.** The EB review's rejection left a G14 blocker (an unattributed choose-the-method sentence in unit 3 step 1); repair round 1 still had 2 blocking issues, round 2 passed with zero. The sentence was removed to match the trace.

## 7. Before → after (unit 1)

| Before (after decompose) | After |
|---|---|
| Board example, pupils copy it | Slate answers from every pupil added after the example (EB-04) |
| Twenty problems, solved alone | Level check + fluid groups added as a step; practice in level sets (EB-06) |
| Same practice, sports-or-crops theme choice (CL-01) | Rewritten as a mock 400-point ledger with six costed options (PB-01) |
| Fixed pairs practise tables | Already rotating pairs at decompose; unchanged |
| Peer checking, no scores | Unchanged |
| — | One problem per group combined into a class set (CL-04) |

## 8. Teacher card (unit 1, from `cards.txt`)

```
MLS-MULTDIV-01: Multiplying Two-Digit Numbers
3 weeks. Starts fresh (no earlier unit needed).
==============================================================================
Goal: Builds accurate two-digit multiplication and teacher-provided market
word problems for the mixed work in the final unit.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Show 23 x 4 on the board and explain each multiplying
[changed: EB-04]      step. Pupils copy the example into their notebooks. Then
                      give two short problems for every pupil to solve on
                      slates at once and hold up, look at all slates, and
                      re-explain the steps if many are wrong before moving on.

2. Lead Educator      In week 1, give three short multiplication problems for
[changed: EB-06]      every pupil to solve on slates at once and hold up.
                      Using what they show today, form two or three fluid
                      groups for practice and re-check with slates as they
                      progress. Nothing is marked or recorded.

3. Lead Educator      Give groups a paper mock ledger on the board: a made-up
[changed: EB-06,      budget of 400 points and six options, each with a
CL-01, PB-01]         made-up two-digit quantity and single-digit per-item
                      points. Groups multiply to work out each option cost,
                      then choose options whose total fits under 400 points,
                      writing the sum, and say what they gave up. Each pupil
                      solves their group's chosen set alone in their notebooks
                      using the same answer chart.

4. Peer Facilitator   In pairs with rotating questioner roles, pupils practise
                      multiplication tables aloud. The questioner checks
                      answers against the notebook table.

5. Lead Educator      Write two market amounts on chart paper. Each pupil
                      writes three multiplication word problems using those
                      amounts and solves them.

6. Peer Facilitator   In pairs, pupils exchange notebooks and check work
                      against the answer chart on the board, then return
                      books. No scores are recorded or announced.

7. Lead Educator      Collect one solved word problem from each group onto one
[changed: CL-04]      class chart on chart paper to make a combined class set,
                      without names or scores. Read the combined set aloud
                      together.

------------------------------------------------------------------------------
BEFORE YOU START
- Needs: Chalk, board, notebooks and reused chart paper are available.
  If not: Copy the example and amounts on the board only and have pupils work
  in notebooks; combine steps 2 and 4 in one period.
- Needs: A full 3-week run with no lost week.
  If not: Drop one practice round from step 2 and shorten pair practice to one
  session; do not extend the unit.
------------------------------------------------------------------------------
```

## 9. What to watch for
- **New-card behaviour held up.** EB-06 applied once with all non-negotiables (fresh check, same time and skill, fluid re-checked groups, nothing marked); EB-07 correctly credited instead of re-applied; EB-08/EB-09 deferred for stated reasons. Nothing was forced onto a unit that didn't want it.
- **Later stages can overwrite earlier ones.** PB-01's ledger rewrite of step 3 dropped CL-01's sports-or-crops theme choice from the same step. Each edit was valid on its own; the combination lost the theme. A teacher wanting both would need to re-add it.
- **A reverted unit still leaves a trace.** Unit 3's rejected EB-06 edit surfaced as a G14 late issue and cost two repair rounds. The mechanism worked, but a rejection deep in the pipeline is expensive.
- **No source flags, again.** Seven traps removed, zero flags filed — the Muse pattern. Safe output, sparse record.
- **No teacher review yet**, as with every walkthrough here.
