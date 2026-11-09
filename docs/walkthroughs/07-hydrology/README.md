# Walkthrough 7 — Hydrology: tracking rainfall

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 7 November 2026 (`python3 -m lsb.regress`, folder `runs/regress-3/hydrology`). The source chapter is an original test input written for this project: [tests/fixtures/hydrology-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/hydrology-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.
> Decision trace: [decisions.md](./decisions.md) · Full final cards: [final.md](./final.md) · Localizations: [localizations.md](./localizations.md)

> **Locale note:** The stripped, kept, or relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

| | |
|---|---|
| **Source** | "Chapter 4 – Basic Hydrology Framework", a three-line brief from the requirements: track rainfall across seasons, lectures on cloud formations, backyard recording, a 4-week baseline via class matrices, governance approval for containers |
| **Result** | Passed: 2 units in a chain, 19 model calls, 276,218 input / 127,371 output tokens |
| **Kept** | The 4-week baseline window, the class matrix, placing containers with governance approval, and baseline figures computed from class data |
| **Removed** | Recording rainfall at home; lectures on global cloud formations; multi-season tracking; "secure sectors" wording |
| **Added** | A 0-line scale method and a reset protocol (decompose, under critic pressure); a whole-class reading check (evidence-based); a worked baseline example (evidence-based). Connected Learning and Participatory Budgeting abstained |

## 1. The starting point
Three lines. A summary for teachers says the segment covers tracking local rainfall data across seasons, with lectures on global cloud formations and assignments to record backyard accumulation numbers; the goal is to calculate baseline regional parameters over 4 weeks using class matrices; the local governance body must approve container placement in secure sectors. No grade band, no period length, no activities, no definitions — the pipeline inferred Middle from the calculation work and 45-minute periods, and nearly every step below is pipeline-built structure around that brief.

## 2. What the pipeline kept, and why
- **The 4-week baseline window leads everything.** Two units, six weeks: two to build and place the containers and the blank matrix, four to record and calculate.
- **Backyard recording became school recording.** Each learner recording at home would collect home details unsupervised, so the class reads shared containers at the school's approved secure spot, all together with the educator present. The run reported this as a warning asking for confirmation, not a source flag.
- **"Baseline regional parameters" got a definition.** The source never says what they are; the pipeline interpreted them as the 4-week total plus the weekly and daily averages from the class matrix, and said so in a warning.
- **The approval step stays.** Asking the governance body to approve the secure spot survives as unit 1 step 1, fenced as the educator's own administrative task.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Assignments to record backyard accumulation numbers | Changed: shared containers at the school, read by the whole class with the educator | Home details collected unsupervised |
| Lectures on global cloud formations | Set aside as lecture only | No classroom action; no step needs the concept |
| Tracking rainfall across seasons | Set aside as a follow-on: repeat unit 2 in a later season and compare | Beyond the 4-week baseline window |
| "Secure sectors" | Replaced with "secure spot" | Jargon with no meaning for a teacher |

No source flags were reported: three lines held no unsafe steps, child data, purchases or region-specific terms, and the one real adaptation (backyard → school) went out as a warning instead.

## 4. The units

```
MLS-RAIN-01  Approving, Building and Placing Rain Containers (2 weeks)
     │
     ▼
MLS-RAIN-02  Recording Rainfall and Calculating the Baseline (4 weeks)
```

One chain, six weeks. Unit 2 needs placed containers and the blank matrix, so nothing runs in parallel — a delay in approval delays recording.

## 5. What each stage did

**Evidence-Based (ran first), applied in both units.**
- **EB-04 Checking for understanding**, unit 1: nothing showed whether every learner could read a scale before 4 weeks of readings began, so an added step has all learners read a sample depth onto scrap paper at once while the educator looks at every answer.
- **EB-03 Worked examples**, unit 2: learners met the baseline procedure and went straight to calculating alone, so the educator now works one complete example with made-up totals on the board first, and the comparison step moves to the end of that lesson so both fit the declared weeks.
- **Credited, not added:** the water-filled bottle as a concrete model (EB-05); daily readings and weekly additions as spaced practice (EB-02).
- **Abstained nowhere, but deferred honestly:** a recall quiz would have little to recall in a setup unit and no room in a 7-step unit; a second check and a linked drawing would push step 6 past 80 words.

**Connected Learning abstained on both units.** The rota, the shared matrix and the class chart already cover peer roles, real data and a shared product; a showcase or theme choice would be busywork, and the one educator-checked step is a mastery check the rules protect. With every unit abstaining, the stage made no review call.

**Participatory Budgeting abstained on both units.** No fixed amount with more options than fit: every pair gets a container, the rota rations nothing, and asking the governance body for approval is the educator's own task, explicitly always skipped. With every unit abstaining, the stage made no review call.

## 6. What the reviewers caught
- **Decompose review, attempt 1:** six blockers and two minors — essentially a rebuild of the measurement protocol. One step combined three actions by different people; the scale started at the uneven bottle base and used an unprotected paper strip that rain would ruin; emptying the containers left no water up to 0, so the next reading ran low; nothing reset the containers before recording, so week 1 would include two weeks of rain; the baseline math never said how to combine containers and divided by school days even though Monday readings include weekend rain; and learners handled sharp cut-bottle edges. The two minors: the lost-week fallback never fixed the per-day divisor, and the approval fallback left the unit open-ended. Attempt 2 fixed all six blockers, leaving one minor (see §9).
- **Evidence-Based review 1:** REVISE, two blocking issues. The reset sat on the last school day before the first reading day — before the unit starts — and the baseline lesson said only "in the final week", where it would work from an incomplete matrix or fall outside the 4 weeks.
- **Evidence-Based round 2** fixed the lesson timing in-stage (last school day, separate time block), but the reset issue came back ("not fixed from the previous review"). Review 2: REVISE, one blocking issue. Both became **late issues**.
- **Two repair rounds.** Round 1's output was rejected by the code check three times over: it changed a step no issue pointed at, *removed* a step, and rewrote a fallback — exactly what the check exists to catch. Its retry passed the check but not the critic. Round 2's output was rejected once more for touching an unrelated step; its retry passed. The repair reframed the reset around the 28-day reading window (reset at reading time with the class present, readings covering 28 days) rather than taking the critic's suggestion to move it into unit 1's placement step.

## 7. Before → after (unit 2)

| Before (after decompose) | After |
|---|---|
| Step 2: reset on the last school day before the first reading day, educator alone, one sentence | Reset at reading time with the whole class present, readings covering 28 days, recording from the first school day (repair) |
| Step 6: baseline lesson "in the final week", straight to calculating alone | Full lesson on the last school day in a separate time block, worked example with made-up totals first (EB-03) |
| Step 7: compare results whenever | Comparison at the end of the step 6 lesson (EB-03) |
| Steps 1, 3, 4 and 5 | Unchanged |

## 8. Teacher card (unit 2, from `cards.txt`)

```
MLS-RAIN-02: Recording Rainfall and Calculating the Baseline
4 weeks. Builds on MLS-RAIN-01.
==============================================================================
Goal: Fills the class matrix with 4 weeks of rainfall readings and turns them
into the class's baseline rainfall figures.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Recall from MLS-RAIN-01: use the placed rain containers
                      and the blank class matrix on chart paper. Set a rota on
                      the chart so each student pair reads one container on
                      given days.

2. Lead Educator      On the last school day before the 4 weeks of readings
                      begin, at reading time, the whole class goes together to
                      the containers and the educator stays with all groups.
                      The educator empties and refills each container to the 0
                      line, so the 4 weeks of readings cover 28 days. Students
                      do not drink the water, lift the containers or touch the
                      stones. Recording starts on the first school day of the
                      4 weeks.

3. Peer Facilitator   Each school day at the same time, the whole class goes
                      together to the containers, and the educator stays with
                      all groups. The rota pair reads the water depth in
                      millimetres on the scale and calls it out for others to
                      check. The educator then empties each container and
                      refills it to the 0 line from a bottle of clean water
                      brought from class. Students do not drink the water,
                      lift or move the containers, or touch the stones.

4. Peer Facilitator   Back in class, the rota pair writes each container's
                      reading in that day's row of the class matrix. Write 0
                      on dry days.

5. Lead Educator      At the end of each week, lead the class in adding each
                      container's daily readings and writing the results in
                      the weekly total row of the class matrix.

6. Lead Educator      On the last school day, in a separate time block after
[changed: EB-03]      that day's reading and weekly total, give a full lesson
                      on baseline figures. On the board, work one example step
                      by step using three containers' made-up weekly totals:
                      total each container's weeks, average those totals (skip
                      containers missing a reading), then divide by 4 weeks
                      and by 28 days for the weekly and daily averages. Then
                      each student calculates the class's figures in their
                      notebook from the matrix.

7. Lead Educator      At the end of that lesson, lead the class in comparing
[changed: EB-03]      their results and writing the agreed baseline figures on
                      chart paper.

------------------------------------------------------------------------------
BEFORE YOU START
- Needs: Some rain falls during the 4 weeks.
  If not: Keep recording 0 on dry days. Zero readings are valid data, and the
  baseline figures are still calculated from them.
- Needs: All 4 weeks are school weeks with daily access to the containers.
  If not: If a week is lost to a holiday or closure, take readings for the
  remaining 3 weeks and draw a line through the lost week's rows. On the first
  day back, the educator empties and refills each container to the 0 line
  without recording, and readings start again the next school day. Do steps 6
  and 7 in the last periods of the final week and calculate over 3 weeks
  instead of 4. Divide by the number of weeks and the number of days actually
  covered by the recorded readings.
- Needs: The containers stay upright and in place between readings.
  If not: Mark that container's reading for the day as missing on the matrix
  and use the other containers for that day. The educator resets the container
  and refills it to the 0 line at the next visit.
------------------------------------------------------------------------------
CHANGES FROM THE SOURCE
- Evidence-Based, EB-03 Worked Examples, then Practice: one complete worked
  example with made-up totals is shown step by step on the board before each
  student calculates the class's own baseline figures in their notebook. The
  lesson is set on the last school day, in a separate time block after that
  day's reading and weekly total, so it works from the complete matrix within
  the 4 weeks. The full lesson, the missing-reading rule and the ÷ 4 and ÷ 28
  steps are kept.
- Evidence-Based, EB-03 Worked Examples, then Practice: the comparison of
  results is placed at the end of the step 6 lesson, so the worked-example
  lesson and its follow-up fit the declared weeks (EB-G6); the action itself
  is unchanged
```

## 9. What to watch for
- **The reset Friday belongs to no named unit.** The final step 2 still resets "before the 4 weeks of readings begin" — the repair reframed it around the 28-day window instead of moving it into unit 1 as the critic suggested, and the critic accepted that. A strict reader could still ask which unit that Friday counts toward.
- **The repair needed watching.** Two rounds, two code-check rejections, one of them for removing a step outright. The check caught everything, and the kept output passed — but this is the run that most shows the repair model reaching beyond its brief.
- **A knocked-over container can cascade.** The attempt-2 minor stands: over 28 days every container could collect a missing reading, leaving step 6 nothing to average. A class with only two containers should add a third.
- **A strict chain of two.** Unit 2 needs placed containers, so an approval delay stalls recording entirely. The fallback covers it (build and draw while waiting), but there is no parallel work to absorb a long wait.
- **Most of this unit is pipeline-built.** Three source lines became thirteen steps of scales, rotas and baseline math. An adapter should check the method against their syllabus rather than trusting that the source implied it.
