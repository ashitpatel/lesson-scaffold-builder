# Walkthrough 12 — Snail: water source mapping

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse`, folder `runs/snail-mapping-live-1`). The source is a real SNAIL/DRCSC lesson, DRCSC's 'Creative Lesson Plan on Water' (2003), adapted into lesson prose as a test input: [tests/fixtures/snail-water-mapping-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/snail-water-mapping-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.
> Decision trace: [decisions.md](./decisions.md) · Full final cards: [final.md](./final.md) · Localizations: [localizations.md](./localizations.md)

> **Locale note:** The stripped, kept, or relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

| | |
|---|---|
| **Source** | A Grade 6 environmental studies lesson, "Water Source Mapping": household maps, shared signs, source visits, reports, percentages, a village wall map |
| **Result** | Passed: 3 units, 7 weeks in all, 13 model calls, 438,089 input / 75,287 output tokens |
| **Kept** | The household maps with walking-step distances and uses; the shared signs with summer-only marking and the peer readability check; the source visits with warning signs; the reports, the percentages, the wall village map |
| **Removed** | Nothing removed: no deferred segments and no source flags. Visits run whole-class with the educator present and no-touch rules; reports carry no home addresses |
| **Added** | Whole-class slate checks on signs before redrawing, visiting and wall-mapping (EB-04, all units); week-2 recall from memory, self-checked (EB-01, units 1–2); one percent worked step by step (EB-03, unit 3); observer/recorder and counter/recorder pairs (CL-02, units 2–3). Participatory budgeting abstained everywhere |

## 1. The starting point
A Grade 6 environmental studies lesson in six sections, for Class 5 to 7 in rural and urban schools. It opens with a discussion of where domestic water comes from: each child draws a map of house and surroundings, marking every family source — hand pump, well, tubewell, community tap, river, pond — with its distance in walking steps and its uses. A shared set of signs (tap, well, tubewell, a pot for stored rainwater) marks the sources, summer drinking sources marked separately from year-round ones, and every map must be readable by another child using only the signs. Children visit the sources, observe pollution, waterlogging, garbage and animal waste, and add these warning signs to the map. Each child writes a water source report and shares it; the class pools the reports into percentages of source types and domestic-water mix, compares household mixes with the class average, and builds a simplified water facilities map of the village — main roads only — that stays on the classroom wall.

## 2. What the pipeline kept, and why
- **The household maps became the sequence's spine.** Source types, walking-step distances and uses are mapped in unit 1, carried on the visits in unit 2, and pooled into totals in unit 3.
- **The shared signs stay, with their checks.** Summer-only versus year-round marking and the read-by-another-child test survive as unit 1 steps 3–4, with a slate check added before redrawing.
- **The visits stay, made supervised.** Both source visits run whole-class with the educator staying with all groups, and observer/recorder pairs now split the recording.
- **Reports, percentages and the wall map stay almost as written.** Reports name types and surroundings only; the percent step gained one worked example; the village chart stays on the wall with peer help placing the signs.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Nothing — §§1–6 all entered the sequence | No deferred segments, no source flags | A clean source with no traps to drop |
| "Children visit the sources" (§3), unsupervised as written | Both visits run whole-class with the educator staying with all groups; no touching, drinking, picking up or lifting | Safety near water and waste |
| Household detail in maps and reports (§§1, 4) | Reports state types, uses, distances and surroundings without home addresses; names stay on own work, class totals only | Children's home privacy |
| Town-vs-village framing (§1) | Kept as discussion context; cards stay region-neutral | Cards carry no regional terms |

## 4. The units

```
MLS-WATER-01  Household water maps with shared signs (2 weeks)
     │
     ▼
MLS-WATER-02  Visiting sources and recording surroundings (2 weeks)
     │
     ▼
MLS-WATER-03  Class reports, percentages and village facilities map (3 weeks)
```

A linear chain: each unit builds on the one before it.

## 5. What each stage did

**Evidence-Based, applied in all three units.**
- **EB-04 Checking for understanding**, in all three units: every child draws each sign on a slate during teaching (unit 1), names two warning signs on slates before the visits (unit 2), and shows the sign for a named source on scrap before the wall map continues (unit 3) — the educator looks at all answers and re-explains what many miss.
- **EB-01 Retrieval practice**, in units 1–2 (added steps): a short week-2 recall of sources, signs, warning signs and clean surroundings from memory, self-checked against shown answers, nothing collected or marked.
- **EB-03 Worked examples**, in unit 3: one source-type percent is worked fully step by step on the board before children work the rest themselves.
- **Credited, not added:** the household maps already pair drawing with the idea (EB-05, unit 1).
- **Deferred, with reasons:** spacing (EB-02) — already covered by the EB-01 recall or blocked by the added-step and 2-card limits; worked examples (EB-03, units 1–2) — no stepwise procedure is taught; dual coding (EB-05, units 2–3) — surroundings are observed directly and the wall chart is itself visual; level groups (EB-06) — no leveled reading or mathematics practice; interleaving (EB-07) — no blocked sets of taught types to mix; self-explanation (EB-08) — no worked example with reasoning to explain; elaborative interrogation (EB-09) — signs and warning signs have no precise why/how answers in the lesson.

**Connected Learning, abstained in unit 1, applied in units 2–3.**
- **CL-02 Peer roles**, in unit 2: paired observer and recorder roles that swap at the next source across the two visits.
- **CL-02 Peer roles**, in unit 3: the class tally done in mixed pairs with rotating counter and recorder roles.
- **Unit 1 abstained with two credits**: the maps already use everyday walking-step data (CL-03) and already have a peer reader (CL-05); a showcase would expose home surroundings and a class tally would duplicate unit 3.
- **Further credits:** observed surroundings as real data (CL-03, units 2–3), the existing class totals and wall map (CL-04, unit 3), reports shared with the class (CL-05, unit 3). A warning-sign tally (CL-04, unit 2) was deferred — pooling happens in unit 3.

**Participatory Budgeting abstained in all three units**: maps, visits and pooled totals contain no fixed amount with more options than fit — no budget, time slots, space or proposal set to allocate.

## 6. What the reviewers caught
Nothing on the scored attempt. Attempt 1 never got going — a transient `muse exec` failure ("model did not reach a terminal state") left decompose unusable. Attempt 2 passed clean: the decompose review and both stage reviews passed on the first round with zero issues, no late issues, no repair round, and no source flags. The only notes are two decompose warnings: the grade band was inferred as Middle from "Grade 6 / Class 5 to 7" and the period defaulted to 45 minutes, both absent from the source.

## 7. Before → after (unit 3)

| Before (after decompose) | After |
|---|---|
| Short water source report from map and visit | Unchanged |
| Share reports; list water problems and difficult access | Unchanged (credited CL-05) |
| Pool reports into tallies; calculate source-type and domestic-mix percents | Tallies done in counter/recorder pairs (CL-02); one percent worked fully step by step first (EB-03) |
| Draw the village facilities chart with shared signs | Every child shows a sign on scrap first; re-explain missed signs before continuing (EB-04) |
| Pairs place roads and signs; fix unclear marks | Unchanged |

## 8. Teacher card (unit 3, from `cards.txt`)

```
==============================================================================
MLS-WATER-03: Class Reports, Percentages and Village Facilities Map
3 weeks. Builds on MLS-WATER-02.
==============================================================================
Goal: Turns individual maps and visit notes into pooled class totals,
percentages, problem lists, and one wall village facilities map.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Recall from MLS-WATER-02: bring maps with visit
                      observations and warning signs. Each child makes a short
                      water source report from the map and visit in the
                      notebook. State source types, uses, distances in steps,
                      and surroundings without home addresses.

2. Peer Facilitator   In turn, share water source reports with the class,
                      stating source types and surroundings only. List on
                      chart paper the kinds of water problems heard and which
                      sources have difficult access. Keep names on own work
                      only and record class totals only.

3. Lead Educator      Pool the reports into class totals on chart paper with
[changed: EB-03,      chalk tallies in mixed pairs, with one child counting
CL-02]                aloud and the partner marking the tally, then swapping
                      roles for each source type. Work one source-type percent
                      fully on the board step by step, saying each step aloud.
                      Each child then works the rest of the percents in the
                      notebook and compares the household mix with the class
                      average.

4. Lead Educator      Draw a simplified village facilities chart on chart
[changed: EB-04]      paper showing only main roads. Mark the water tank,
                      well, pump, tap, canal, and pond with the shared signs.
                      Have every child hold up a scrap showing the sign for
                      one named source, look at all scraps, and re-explain any
                      sign many miss before continuing. Keep the finished map
                      on the classroom wall for the next activities.

5. Peer Facilitator   In pairs, children who know the village outline help
                      those who do not to place roads and signs. Check each
                      mark uses the shared signs and can be read by another
                      child. Fix unclear marks on the wall chart with chalk.

------------------------------------------------------------------------------
BEFORE YOU START
- Needs: Classroom wall space is available to keep the village facilities
  chart for later activities.
  If not: Keep the chart folded and bring it out per lesson; shorten
  percentage work to one source-type calculation and one use calculation.
------------------------------------------------------------------------------
```

## 9. What to watch for
- **A real source, fully kept.** This is the first walkthrough adapted from a published lesson rather than an original test input, and every section survived — the pipeline added checks, recall and roles without dropping any activity.
- **One transient backend failure.** Attempt 1 died in `muse exec` before producing anything; attempt 2 passed with zero flags. Nothing in the output reflects the failed attempt.
- **No teacher review yet**, as with every walkthrough here.
