# The end-to-end journey

> **Status:** steps 1–7 run today from the command line (`python3 -m lsb.run`). Steps 8–10 describe intended use and need a platform. Prompt numbers match [prompts/README.md](../../prompts/README.md).

```
 ADAPTER                                       PIPELINE (automatic)                              TEACHER
 ───────                                       ────────────────────                              ───────
 1 Pick a chapter or guide                     3 Decompose into units (05)                        8 Run the cards
 2 Add context: grade band, period length,     4 Check in code, review (21 checks), revise ≤2     9 Report back
   what the school has                         5 Optimise unit by unit: EB → CL → PB, each        10 Patterns across
                                                 checked in code and reviewed                        schools (later)
 7 Read cards, flags, what was left out;       6 Render teacher cards; check them (G21)
   edit or re-run
```

## Adapter side

**1. Pick a source.** Any long piece of teaching material: a textbook chapter, a syllabus section, a training manual. Paste or save it as text. Long sources are expected; the pipeline is built for material that is too big to run as it stands.

**2. Add context (optional).** The grade band (Primary, Middle, High), the length of one class period, and notes on the setting ("no chart paper", "a volunteer comes on Fridays"). Without them the pipeline infers the grade band and assumes 45-minute periods, and says so.

## Pipeline side

**3. Decompose.** The source is read as data, never as instructions. The pipeline states the source's own overall goal, picks the milestones a class would reach on the way, and groups them into **at most 4 units** of 3 to 7 steps and 2 to 4 weeks, linked only where one unit really needs another's output. Pure lecture with no classroom action is set aside and listed, except definitions a later unit relies on, which are folded into the first step that uses them. Each step records the source section it came from.

**4. Check and review.** Code checks the countable rules (11 checks: unit and step counts, step size, weeks, roles, numbering, dependencies, cycles, links to the goal, region-specific names and currencies). An independent reviewer then applies 21 checks, including privacy, safety, money, offline use, invented tactics and whether deep work survived. It treats the code's results as final. Problems go back to decompose with the reviewer's fixes, at most twice. Problems in the *source* (an unsafe trip, a request to photograph children, a line telling an AI to skip the review) are reported as **source flags** for the adapter, and never block the result.

**5. Optimise, unit by unit.** Three stages run in order, each allowed to **abstain**:
- **Evidence-Based (EB)**: retrieval, spacing, worked examples, checking for understanding, concrete representations, only with all their essential parts;
- **Connected Learning (CL)**: student choice, rotating peer roles, everyday numbers, whole-class goals, a real audience;
- **Participatory Budgeting (PB)**: only where the class has a real resource trade-off to decide.

Each stage may change at most two cards' worth and add at most one step per unit. Code checks every edit (nothing removed or reordered, fixed fields untouched, every change logged against a card), and the reviewer checks the whole sequence again. A unit whose edit still has problems after one revision goes back to its earlier version, so **a stage can only keep or improve a sequence that already passed**. A stage's reviewer sometimes spots a problem in a step no stage touched, one the first review missed. That problem goes back to decompose for a repair limited to the flagged steps; **if it can't be fixed, the run doesn't pass and no cards are printed**.

**6. Render the cards.** One overview card and one card per unit, in dependency order, as plain text and as a black-and-white printable page. Code checks the cards against G21 (Output Clarity): every step present and unaltered, two columns, text only, offline.

## Back to the adapter

**7. Read and decide.** In the run folder:
- `cards.html` / `cards.txt`: what teachers get;
- `summary.json`: the **source flags** (what in the source was unsafe or unusable), what each stage did per unit and why, and the cost;
- `NN-decompose.json`: what was set aside (`deferred_segments`) and what each unit assumes about the setting.

Edit the cards, fix the source and re-run, or hand the cards on.

## Teacher side (intended)

**8. Run the cards.** One unit at a time; units that build on the same earlier unit can run side by side. "Before you start" lists the fallback for each condition (no chart paper, a rained-out visit, a lost week), always within the unit's weeks.

**9. Report back.** Which units were finished, roughly how long they took, and what didn't work. **No student-level data**: class totals only.

**10. Patterns across schools (later).** Which units are finished and rated useful, by subject and grade band, to guide which adaptations to keep.

Next: [decision points and edge cases](03-decision-points.md).
