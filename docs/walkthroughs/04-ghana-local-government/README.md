# Walkthrough 4 — Ghana: local government and community development

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 7 November 2026 (`python3 -m lsb.regress`, folder `runs/regress-3/ghana-assembly`). The source chapter is an original test input written for this project and set in a Ghanaian junior high school: [tests/fixtures/ghana-assembly-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/ghana-assembly-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.
> Decision trace: [decisions.md](./decisions.md) · Full final cards: [final.md](./final.md)

| | |
|---|---|
| **Source** | A 7-week JHS 2 social studies section, "Our District Assembly and Community Development" |
| **Result** | Passed: 3 units (two that can run side by side, then a letter), 19 model calls, 308,561 input / 96,882 output tokens |
| **Kept** | How a local council works, the community's needs, a fixed development budget with costed projects, a class vote, whether the result is fair, and a revised letter to the council member |
| **Removed** | An unsupervised household survey recording names and phone numbers; a real class-prefect election with campaign speeches; pupils attending a town hall meeting on their own; pupils bringing money to a class fund held by a pupil treasurer; a history lecture; the country's own names for its council, committees, national fund and currency |
| **Added** | A chalkboard diagram, a worked budget example, a whole-class check and recall from memory (evidence-based); a reading of the letters to another class (Connected Learning); a mock vote counted two ways, with the rules announced first and the result reported (participatory budgeting) |

## 1. The starting point
Teacher's notes for seven weeks of 60-minute lessons. They explain how the District Assembly, Assembly Members and Unit Committees work, open with a two-lesson history lecture, and have groups list community needs. Then they send groups through the community after school, without the teacher, to interview ten households and record each household head's name and phone number. A worked budget follows: 500,000 cedis against six costed projects. Then a single-choice class vote, a real prefect election "so pupils see an election in action", attending the next town hall meeting alone, each pupil bringing 5 cedis to a class fund with a pupil treasurer, and finally a letter to the Assembly Member arguing for one project.

## 2. What the pipeline kept, and why
- **The real decision content.** A fixed fund (500,000) against six projects worth 940,000 in total is a genuine trade-off, so the budget sums, the vote and the fairness discussion all stay.
- **Region-neutral, not content-free.** The District Assembly becomes "the local council", the Assembly Member "the elected council member", the Unit Committee "a community committee", the Common Fund "a national development fund", and cedis "units", with the same amounts. The ideas survive; the names travel.
- **Sustained writing stays:** a full lesson of drafting, a partner reading, and a second full lesson to revise.
- **Parallel units.** The council-and-needs unit and the budget-and-vote unit don't depend on each other; the letter needs both.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Groups walk the community after school without the teacher and record household heads' names and phone numbers (§4.3) | Left out | Unsupervised off-site movement and contact with adults; personal data |
| A real class-prefect election with candidate speeches (§4.5) | Left out | Pupils voting on other pupils and campaigning against each other; the class vote already shows an election in action |
| Pupils attend the town hall meeting on their own (§4.6) | Left out; what a town hall meeting is stays in unit 1's explanation | Unsupervised off-site attendance |
| Each pupil brings money to a class fund kept by a pupil treasurer (§4.7) | Left out | Minors handling and tracking real money; a cost to families |
| Two-lesson history of local government (§4.2) | Set aside as lecture only | No unit needs the timeline |

All four problems were also reported as **source flags**.

## 4. The units

```
MLS-COMDEV-01  How the council works; our community's needs (2 weeks) ─┐
                                                                         ├─► MLS-COMDEV-03  Writing and revising a letter
MLS-COMDEV-02  Projects, costs and deciding together (2 weeks) ─────────┘    to the council member (3 weeks)
```

## 5. What each stage did

**Evidence-Based (ran first), applied in units 1 and 2.**
- **EB-05 Concrete and visual representations**, unit 1: the explanation of the council is now given while drawing it on the chalkboard (a council box above community circles, arrows up for needs, arrows down for funded projects, "town hall meeting" beside them), saying what each part stands for.
- **EB-01 Retrieval practice**, unit 1: in the last lesson of week 2, with the diagram rubbed off, three questions from memory on what the council member and a community committee do and what a development plan is, then self-checked.
- **EB-03 Worked example**, unit 2: one set of projects is added up aloud, step by step, before pupils spend a full lesson finding sets alone.
- **EB-04 Checking for understanding**, unit 2: every pupil totals one more set and writes "fits" or "too much", held up at once; the educator re-works the sum if many are wrong.
- **Abstained on the letter unit:** the needs list and cost work are meant to be used as written evidence, and a worked letter would hand pupils the argument.

**Connected Learning, applied in unit 3 only.**
- **CL-05 Real audience:** final letters read to another class, in the classroom with the educator present. Reading is each pupil's choice.
- Units 1 and 2 **abstained**, crediting what was already there: pupils choosing needs and project sets (CL-01), rotating writer and reader (CL-02), and the class needs list and vote tally (CL-04).

**Participatory Budgeting, applied in unit 2 only.**
- **PB-03 Counting methods:** the vote is now labelled a **mock** vote and counted two ways, single choice and approval, with both rules announced before any hands go up.
- **PB-05 Report-back:** an added step writes both rules and the winner under each on chart paper, class totals only, giving the fairness discussion something concrete to compare.
- **Credited, not added:** PB-01. Pupils already choose costed projects under a fixed total.
- Units 1 and 3 **abstained**: unit 1 has no fixed amount of its own, and the letter is individual argument writing that a vote would interrupt.
- The participatory-budgeting edit was **rejected once by the code check**: it logged two cards against the same step. The retry made the report-back its own step.

## 6. What the reviewers caught
- **Decompose review, attempt 1:** two fallbacks would squeeze a 2-week unit into one week ("so the unit fits in one week"), below the 2-to-4-week window. Separately, one pupil had the writer's job for a whole group task. Both were fixed in attempt 2: the fallbacks carry steps into the next week, and pupils take turns writing.
- **All three stage reviews** then found the same problem in a field no stage could change: unit 1's `macro_alignment` promised "a ranked class list of needs", but no step ranks them; the class only marks the most urgent. Recorded as a **late issue**. One repair round rewrote the alignment to match what the steps deliver ("…with the most urgent ones marked"), and the review passed.

## 7. Before → after (unit 2)

| Before (after decompose) | After |
|---|---|
| The costs are listed; pupils find sets alone for a full lesson | One set worked aloud first (EB-03), then every pupil checks one more set on scrap paper (EB-04), then the full lesson |
| A single-choice show-of-hands vote, the rule unstated | A clearly labelled mock vote counted two ways, with both rules announced first (PB-03) |
| — | Both rules and both winners written on chart paper, totals only (PB-05) |
| A discussion of whether the choice is fair | Unchanged, now with two results to compare |

## 8. Teacher card (unit 2, from `cards.txt`)

```
MLS-COMDEV-02: Projects, Costs and Deciding Together
2 weeks. Starts fresh (no earlier unit needed).
==============================================================================
Goal: Shows pupils, through their own budget sums and a class vote, how a
fixed fund forces a choice among projects and why that choice raises questions
of fairness.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Explain that a national development fund gives each
[changed: EB-03]      local council money for development. Write this example
                      on the chalkboard: the council has 500,000 units for new
                      projects this year. A borehole costs 120,000, a
                      footbridge 200,000, streetlights 90,000, a clinic
                      extension 300,000, a library room 150,000 and a market
                      shed 80,000. Then work one set aloud, step by step:
                      borehole 120,000 plus footbridge 200,000 makes 320,000,
                      plus streetlights 90,000 makes 410,000, which is within
                      500,000.

2. Lead Educator      Write one more set on the chalkboard: clinic extension,
[changed: EB-04]      footbridge and market shed. Every pupil writes the total
                      and "fits" or "too much" on scrap paper and holds it up
                      at the same time. Look at all the papers; if many are
                      wrong, work the sum again on the board before moving on.
                      Nothing is collected or recorded.

3. Lead Educator      Give a full lesson for each pupil to work out, in their
                      notebook, several sets of projects whose total cost is
                      500,000 units or less. Pupils show every sum.

4. Lead Educator      Hold a mock class vote on which project the council
[changed: PB-03]      should fund first, announcing both counting rules before
                      any hands go up. Single choice: each pupil raises a hand
                      for one project only; approval: each pupil raises a hand
                      for every project they accept. Record each count's class
                      totals as tally marks on the chalkboard.

5. Lead Educator      On chart paper, write both counting rules, the winning
[changed: PB-05]      project under each rule, and that the class next
                      discusses whether the result is fair. Write only class
                      totals, never who voted for what.

6. Lead Educator      Lead a class discussion on whether the winning choice is
                      fair to communities that did not get their project.
```

## 9. What to watch for
- **The CL-05 step copies the prompt's worked example almost word for word** ("Arrange a 10-minute session with another class… Reading is a choice: a pupil may lay the letter on the desk…"). It's correct here, but models lean on worked examples; that's why test sources are kept out of them.
- **The letter is addressed to a real official but read only in class.** The pipeline kept the source's own letter task and didn't add sending it; whether to send letters is the school's decision.
- **Two counts in one vote step.** Running single-choice and approval counts back to back is quick in a small class but may need a second period in a large one.
- **Lessons are 60 minutes in the source, 45 here.** Decompose used the 45-minute default and warned the adapter to confirm the period length.
