# Walkthrough 1 — Kenya: clean water and health

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 7 November 2026 (`python3 -m lsb.regress`, folder `runs/regress-3/kenya-water`). The source chapter is an original test input written for this project and set in a Kenyan upper-primary school: [tests/fixtures/kenya-water-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/kenya-water-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.
> Decision trace: [decisions.md](./decisions.md) · Full final cards: [final.md](./final.md)

| | |
|---|---|
| **Source** | A 6-week Grade 6 science strand, "Clean Water and Health", written for the Competency-Based Curriculum (CBC), Upper Primary |
| **Result** | Passed: 4 units (one foundation unit, a chain of two after it, one alongside), 23 model calls, about $5.14 at list price |
| **Kept** | How germs get into water and the class chart, building a filter, boiling and sunlight demonstrations, handwashing and the tippy-tap, covered storage, and each learner's safe-water guide |
| **Removed** | Learners cutting bottles with a razor, pouring boiling water and climbing on the roof; boiling water at home; a register of which families treat their water; an unsupervised walk to the lake shore; testing kits to buy; a two-lesson history lecture; the county, lake, currency, offices and curriculum names |
| **Added** | Whole-class finger checks and recall from memory (evidence-based); rotating roles for the jar comparison, and each guide read to a younger class (Connected Learning). Participatory budgeting abstained everywhere |

## 1. The starting point
A teacher's guide for six weeks of 35-minute lessons. It explains that clear-looking water can carry germs (§3.1), opens with a two-lesson lecture on the history of cholera in Kisumu County and around Lake Victoria (§3.2), then has learners build bottle filters, cutting their own bottles with a razor blade (§3.3). Each learner takes a turn pouring boiling water; two learners climb onto the school roof each afternoon to turn the sun-disinfection bottles; each learner boils water at home for homework while the teacher records in the class register which families treat their water, for follow-up with the chief at the next baraza (§3.4). It teaches six handwashing steps with a tippy-tap and covered storage (§3.5), sends groups to walk to the lake shore after school to collect samples and asks the school to buy a testing kit per group (§3.6), and ends with each learner writing a one-page safe-water guide for a younger child (§3.7).

## 2. What the pipeline kept, and why
- **The germ explanation leads the sequence.** Three ways germs get into water and three ways to stop them are taught in unit 1 and kept on a class chart, because units 2, 3 and 4 all build on them.
- **Unsafe steps became educator demos, not gaps.** The filter building, the boiling and the sunlight treatment all stay: the educator cuts every bottle beforehand, pours the boiling water alone while learners stand back, and handles the bottles on a sheet of iron on the ground with the whole class present.
- **The guide stays intact.** Four parts, a partner check against the chart, a correction lesson and a final copy: two full lessons of sustained writing.
- **The fallbacks absorb a lost week inside the unit's own weeks.** "End the unit on time" and "Do not extend the unit": a missed week compresses steps, never stretches the unit. Unit 2 declares 3 weeks partly to leave slack for a cloudy spell.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Learners cut their own bottles with a razor blade (§3.3) | Changed: the educator cuts every bottle before the lesson, out of learners' reach | A blade in children's hands |
| Each learner pours boiling water (§3.4) | Changed: the educator pours alone; learners watch from a distance | Burns |
| Two learners climb onto the school roof each afternoon (§3.4) | Left out; the bottles go on an iron sheet on the ground with the whole class | A fall from height, unsupervised |
| Each learner boils water at home (§3.4) | Left out | Boiling water with no educator present |
| The register records which families treat their water, for the chief at the baraza (§3.4) | Left out | Household data about children's families, and a record-keeping burden |
| Groups walk to the lake shore after school, unsupervised (§3.6) | Changed: the educator collects the samples before the lesson | An unsupervised off-site trip |
| A testing kit per group at KSh 2,000 each (§3.6) | Left out; the colour-and-smell comparison needs no kit | A purchase priced in the national currency |
| Two-lesson lecture on cholera outbreaks, dates copied (§3.2) | Set aside as lecture only | No unit needs it |
| Kisumu County, Lake Victoria, KSh, the chief, the baraza, the health department, the CBC | Replaced with generic wording or left out with the deferred segments | Cards stay region-neutral; code fails any currency left in |

The five problems were also reported as **source flags** for the adapter.

## 4. The units

```
MLS-WATER-01  How Germs Get into Water (2 weeks)
     │                              │
     ▼                              ▼
MLS-WATER-02  Filtering and       MLS-WATER-03  Clean Hands and
Disinfecting Water (3 weeks)      Covered Containers (2 weeks)
     │
     ▼
MLS-WATER-04  Writing a Safe-Water Guide for a Younger Child (2 weeks)   ← also builds on 01
```

The longest chain (units 1 → 2 → 4) runs 7 weeks against the source's 6; unit 3 runs alongside unit 2.

## 5. What each stage did

**Evidence-Based (ran first), applied in units 1, 2 and 3.**
- **EB-04 Checking for understanding**, in all three: after the storage explanation, every learner shows one finger for yes or two for no on whether scooping with a cup is safe (unit 1); one finger if filtered water is safe to drink, two if it needs more treatment (unit 2); 1 pour, 2 ladle, 3 scoop for which way is unsafe (unit 3). The educator looks at every hand and explains again if many are wrong.
- **EB-01 Retrieval practice**, units 1 and 2: the three lists written from memory with the chart covered, then self-checked (unit 1); an added step in week 3 recalling what a filter removes, why it is not enough, and how long to boil (unit 2).
- **Credited, not added:** the jars and class table, the bottle-filter demo and the real bucket as concrete models (EB-05); the filter built first by the educator, then by groups (EB-03); daily handwashing practice across both weeks (EB-02).
- **Abstained on the guide unit**, with reasons: the chart is meant to stay in view while pupils write, the partner check already shows each learner what is missing, and a worked model guide would hand them the answer (EB-03's "never").

**Connected Learning, applied in units 1 and 4.**
- **CL-02 Peer roles**, unit 1: the single fixed group reporter becomes three named roles, Holder, Smeller and Reporter, that swap with each jar.
- **CL-05 Real audience**, unit 4: the guides were written for a younger child but only the teacher and a partner ever read them, so pairs now read them aloud to a younger class, with the educator present. Reading is each learner's choice.
- Units 2 and 3 **abstained**: unit 2 has no gap an edit could fix and is already at the 7-step limit; unit 3 is demonstration and daily practice with a rotating rota already, where a tally would be busywork.

**Participatory Budgeting abstained on all four units.** The fit-gate fails: no fixed amount with more options than fit. The jars all get compared so nothing is rationed ("a vote for its own sake"); the writing is sustained individual work a vote must not replace. With every unit abstaining, the stage made no review call.

## 6. What the reviewers caught
- **Decompose review, attempt 1:** two blockers and one minor. Learners got water from a full covered bucket "by pouring", which means tipping a heavy container and contradicts the step's own "do not lift the full bucket"; the no-ladle fallback had the same flaw. And the no-soap fallback claimed "soap is what removes most germs", which the source never says. Attempt 2 fixed all three: the educator fills a small covered container with the ladle, learners ladle from the bucket and pour from the capped bottle, the bucket stays where it is, and the fallback only says the steps are done with soap and running water whenever soap is available.
- **Evidence-Based review:** REVISE, one blocking issue. Unit 1 step 4 told the educator to collect water from "a few different spots along the lake shore" — a school with no lake nearby can't do it. No stage had changed that step, so it was recorded as a **late issue**.
- **Connected Learning review 1:** REVISE, two blocking issues. The same lake-shore problem, plus a hygiene blocker in step 5: learners handle jars of untreated water that may carry cholera and typhoid germs, with no handwashing afterwards and no word on what happens to the samples.
- **Connected Learning round 2** fixed the hygiene problem in-stage (step 5 now ends with every learner washing their hands while the educator closes the jars and pours the water away), but the lake-shore step came back a third time ("not fixed from the previous review"). Review 2: REVISE, one blocking issue.
- **One repair round** rewrote step 4 to collect from two or three reachable water sources near the school, and the review passed. The repair's first output also rewrote the step's fallback to match, but the pipeline's edit check rejected that change because no issue pointed at the fallback, so the retry kept the old text. That left the stale fallback described in §9; the pipeline was fixed after this run so a repair may update the fallbacks of a unit it repairs.

## 7. Before → after (unit 1)

| Before (after decompose) | After |
|---|---|
| Step 2 explains unsafe storage, then straight to the chart | A finger check on whether scooping is safe, answered by all at once (EB-04) |
| Step 3 lists written with the chart in view | Written from memory with the chart covered, then self-checked (EB-01) |
| Step 4: collect water from "a few different spots along the lake shore" | Collect from two or three reachable sources near the school (repair) |
| Step 5: compare jars; one fixed reporter per group | Rotating Holder, Smeller and Reporter; handwashing and the educator disposing of the samples (CL-02; CL review) |
| Steps 1 and 6 | Unchanged |

## 8. Teacher card (unit 1, from `cards.txt`)

```
MLS-WATER-01: How Germs Get into Water
2 weeks. Starts fresh (no earlier unit needed).
==============================================================================
Goal: Gives learners the explanation of how water becomes unsafe, and shows
them that clear-looking water can still carry germs, as a class chart that
later units build on.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Explain to the class that water can look clear and still
                      carry germs that cause diarrhoea, typhoid and cholera.
                      Germs get into water from human and animal waste, from
                      dirty containers and from hands that touch the water.
                      Water from rivers, lakes, open wells and uncovered roof
                      tanks is most at risk. Write these three ways on chart
                      paper under the heading 'How germs get into water'.

2. Lead Educator      Explain that safely collected water can become unsafe
[changed: EB-04]      again in an open bucket or when scooped out with a cup
                      hands have touched. Ask if scooping with a cup is safe:
                      all learners at once show one finger for yes, two for
                      no. Look at every hand; if many show one, explain again.
                      Add a second chart column, 'How to stop germs': wash
                      hands, cover containers, and pour or use a long-handled
                      ladle instead of scooping with a cup.

3. Lead Educator      With the class chart covered, each learner writes from
[changed: EB-01]      memory three ways germs get into drinking water and
                      three ways to stop them in their exercise book. Then
                      uncover the chart so each learner checks their own list
                      against it. Nothing is collected or marked.

4. Lead Educator      Before the next lesson, collect water from two or three
                      different water sources you can reach near the school
                      (for example a tap, a stored container, a well, or a
                      stream, pond, river or lake) in clean jars with lids, so
                      each group gets two or three jars. Wipe the outside of
                      each jar dry and close the lids tightly. Mark each lid
                      with where the water came from.

5. Peer Facilitator   In groups, learners compare jars by colour and smell,
[changed: CL-02]      swapping roles for each jar: the Holder holds it to the
                      light, the Smeller opens the lid only to smell, and the
                      Reporter tells the results, which the educator writes in
                      a class table on chart paper. Learners do not taste the
                      water or put their fingers in it. Afterwards, every
                      learner washes their hands with soap and water, and the
                      educator closes the jars and pours the water away.

6. Lead Educator      Use the class table to explain that colour and smell
                      cannot show germs: water can look clear and smell clean
                      and still make us ill. Add this line to the 'How germs
                      get into water' chart. Keep the chart for the next
                      units.

------------------------------------------------------------------------------
BEFORE YOU START
- Needs: The educator can safely reach the lake shore to collect water before
  the lesson.
  If not: Collect the jars from any open water source you can reach safely,
  such as a river, an open well or an uncovered roof tank.
- Needs: There are enough clean jars with lids to give each group two or
  three.
  If not: Use clear plastic bottles with caps instead, or give each group one
  jar and have the groups swap jars during the same lesson.
- Needs: Chart paper is available, and the chart can be kept for the later
  units.
  If not: Write the chart on the back of a used calendar or a flattened cement
  or flour bag, and keep it on the wall.
- Needs: Two weeks of lessons run without a break.
  If not: If a week is lost, do steps 1 and 2 in one period and steps 5 and 6
  in one period.
------------------------------------------------------------------------------
CHANGES FROM THE SOURCE
- Evidence-Based, EB-04 Checking for Understanding: during the explanation of
  how stored water becomes unsafe, every learner answers one question with
  fingers at the same time, and the educator looks at every hand and explains
  again if many are wrong; the chart column and its three ways are unchanged
- Evidence-Based, EB-01 Retrieval Practice: learners write the three ways in
  and three ways to stop germs from memory with the chart covered, then
  uncover it and check their own list; nothing is collected or marked
- Connected Learning, CL-02 Structural Peer Roles: the single fixed group
  reporter becomes three named roles (Holder, Smeller, Reporter) that swap
  with each jar. The no-taste, no-fingers and lid-only-to-smell wording is
  kept, the educator still writes the class table, and the step now ends with
  every learner washing their hands with soap and water while the educator
  closes the jars and pours the untreated water away.
```

## 9. What to watch for
- **A stale fallback.** The card's first "Before you start" entry still assumes "the lake shore", from before the repair rewrote step 4 to use any reachable source. The repair's first output did update it, but the pipeline's edit check rejected the change and the retry kept the old text (see §6). An adapter should follow step 4 and delete the fallback. The pipeline was fixed after this run so this can't recur.
- **A stale note in the run log.** A Connected Learning note still says the jar comparison uses "real water samples from the local lake shore", and the budgeting notes call them "lake-water jars". Both were written before the repair; the steps are right, the notes predate it.
- **Seven weeks against the source's six.** The longest chain (units 1 → 2 → 4) needs an extra week, partly because unit 2 keeps three weeks as slack for a cloudy spell.
- **35-minute lessons, 45-minute cards.** Decompose used the 45-minute default and warned that the source's lessons are 35 minutes; it judged every step fits in 35, but the adapter should confirm.
- **The six handwashing steps aren't in the source.** §3.5 names them without listing them, so the card tells the educator to teach the six steps they already know. An adapter for new teachers should supply the actual steps.
