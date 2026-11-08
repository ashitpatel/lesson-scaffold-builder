# Walkthrough 13 — Pond management

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse`, folder `runs/snail-pond-live-1`). The source is a real SNAIL/DRCSC lesson, DRCSC's 'Creative Lesson Plan on Water' (2003), adapted into lesson prose: [tests/fixtures/snail-pond-management-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/snail-pond-management-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.
> Decision trace: [decisions.md](./decisions.md) · Full final cards: [final.md](./final.md) · Localizations: [localizations.md](./localizations.md)

> **Locale note:** The stripped, kept, or relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

| | |
|---|---|
| **Source** | A Grade 9 environmental studies lesson, "Pond Management": pond uses, songs and sayings, sketching, user surveys, analysis, a design and action plan, plus a town-schools variant |
| **Result** | Passed: 4 units, 10 weeks in all, 18 model calls, 616,068 input / 99,924 output tokens |
| **Kept** | The pond-use discussion and water source maps; the songs-and-sayings collection with pond/river/sea sorting; the sketch categories; the users, hygiene, creatures and history survey; the pooled analysis debates; the design, clearing, planting, posters and report |
| **Removed** | Solo study of the pond nearest each home; the town-schools variant track; South 24 Parganas, the ENRE network, pujas, rice fields; direct contact with waste, water and pond equipment |
| **Added** | Whole-class slate checks on every explanation (EB-04, all four units) and week-2 self-checked recall (EB-01, units 1 and 3); rotating Reader/Writer/Checker and Measurer/Recorder/Checker roles (CL-02, units 1–2). Participatory budgeting abstained everywhere |

## 1. The starting point
A Grade 9 environmental studies lesson in seven sections, adapted from Step 3, Activity A of the DRCSC lesson plans. The class revisits water source maps and discusses why some areas have many ponds, lists everyday pond uses, and collects pond poems, songs and sayings to compare against river and sea references. Each child studies the pond nearest their home — position, size and shape, plants, bank condition — then surveys its users, materials, seasonal changes, hygiene, creatures, history and religious functions. The class pools everything into charts, graphs and diagrams and debates community rules, good pond design, pollutants, protections and mosquitoes. Finally each group draws up a pond design and management plan modelled on a well-managed village pond in South 24 Parganas, does what clearing and planting it can, makes posters, and sends a report to the ENRE network. A seventh section offers town schools a separate track: a guide map, a historical map of reclaimed ponds, and a trash survey.

## 2. What the pipeline kept, and why
- **The pond-use list became the sequence's spine.** Everyday uses are taught with the water source maps in unit 1, and units 3 and 4 recall from the class charts.
- **The songs-and-sayings collection stays almost as written.** Collecting, sorting into pond/river/sea piles, counting into one class table and discussing what it says about community values needed no changes beyond shared recording roles.
- **The sketch categories survived the move to supervised visits.** Position, size and shape, plants, bank condition — still the four items, now checked on slates before the first visit.
- **The full survey stayed, with guardrails.** Users, materials, seasons, hygiene, creatures, history and social/religious uses are all still recorded, as class totals with no names or home details.
- **The analysis debates and the action plan are intact.** Community rules, good design, pollutants, protections, mosquitoes, then each group's own design plus clearing, planting, posters and a shared report.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Each child studies the pond nearest their home, individually or in groups (§3) | Replaced with educator-assigned ponds, a visit rota, and the whole class going together | Solo home-linked visits; no child-level data — class totals with no names or home details |
| Hygiene checks on garbage, plastics, waste and sewage inflow (§4); clearing and planting (§6) | Kept as observation and work targets, with explicit must-not rules | No touching waste, water, plastics, sharp items or tools; sticks and reused sacks for clearing |
| Town-schools variant: guide map, historical map, trash survey (§7) | Deferred as a follow-on candidate | Over the unit cap; a setting variant, not part of the main track |
| South 24 Parganas, the ENRE network (§6); pujas (§4); rice fields (§3) | Replaced with generic wording | Cards stay region-neutral |

No source flags: the run was fully quiet — a clean adapted source with nothing to flag.

## 4. The units

```
MLS-POND-01  Pond uses and community values (2 weeks) ───────┐
                                                             ├─► MLS-POND-03  Pooling findings and analysing pond health (2 weeks)
MLS-POND-02  Sketching ponds and surveying use (3 weeks) ────┘          │
                                                                       ▼
                                                             MLS-POND-04  Pond design and action plan (3 weeks)
```

Units 1 and 2 both start fresh and can run in any order or at the same time; unit 3 builds on both, and unit 4 builds on unit 3.

## 5. What each stage did

**Evidence-Based, applied in all four units.**
- **EB-04 Checking for understanding**, in all four units: every student answers on slates during each new explanation — the pond uses, the four sketch items, the pollutants, the well-managed pond features — and the educator looks at all slates and re-explains before moving on.
- **EB-01 Retrieval practice (added step)**, in units 1 and 3: a short week-2 recall from memory (four questions on uses and sayings; three on pollutants and protections), self-checked, nothing collected or recorded.
- **Credited, not added:** the maps and use list already shown with the explanation (EB-05, unit 1); the features paired with charts and a named pond model (EB-05, unit 4); pooling earlier sheets weeks after teaching (EB-02, unit 3).
- **Deferred, with reasons:** a week-2 review (EB-02, unit 1) and self-explanation (EB-08, unit 1) — the added-step and 2-card limits were reached; recall in unit 2 (records stay on sheets) and unit 4 (a final unit using charts openly); worked examples (EB-03) — no stepwise procedure; level groups (EB-06) and interleaving (EB-07) — no level gaps or blocked sets to mix; asking-then-telling (EB-09) — no precise why/how fact with one lesson answer.

**Connected Learning, applied in units 1–2, abstained in units 3–4.**
- **CL-02 Peer roles**, in unit 1: teacher copying became mixed groups with rotating Reader, Writer and Checker roles for each collected item.
- **CL-02 Peer roles**, in unit 2: the sketch task gained rotating Measurer, Recorder and Checker roles swapping each visit.
- **Abstained with credit:** units 3 and 4 already pool into shared charts and tallies (CL-03, CL-04) and already send posters and a report beyond the teacher (CL-05) — no edit without busywork.

**Participatory Budgeting abstained in all four units**: no fixed amount with more options than fit anywhere — listing, sketching, debating and joint clearing/planting involve no class-owned trade-off, and unit 4's sustained design time is explicitly Always-skip.

## 6. What the reviewers caught
One thing. The decompose review failed attempt 1 with a single blocker (G05): unit 2's off-site sketching step was peer-led, taking the whole class to the ponds without an educator role. Attempt 2 made it a Lead_Educator step — group sketching kept, educator staying with all groups — and passed. The Evidence-Based and Connected Learning reviews then passed on the first round each, with zero issues. No late issues, no repair round, no source flags.

## 7. Before → after (unit 1)

| Before (after decompose) | After |
|---|---|
| Explain uses; list them on chart paper | Every student holds up a slate listing two uses, re-explain missing uses if many are wrong (EB-04) |
| Teacher copies all collected items onto chart paper | Mixed groups pool the items with rotating Reader, Writer and Checker roles (CL-02) |
| Pairs sort lines into piles, count, build one class table | Unchanged |
| — | New step 4: week-2 recall of uses and sayings from memory, self-checked (EB-01) |

## 8. Teacher card (unit 1, from `cards.txt`)

```
MLS-POND-01: Pond Uses and Community Values
2 weeks. Starts fresh (no earlier unit needed).
==============================================================================
Goal: Builds the shared pond-use list and songs-and-sayings collection that
later observation and analysis use toward the management plan.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Explain that a pond is a small still water body common
[changed: EB-04]      in the area. Revisit the class water source maps and
                      discuss why some areas have many ponds and others have
                      few. List everyday uses on chart paper: bathing,
                      washing, swimming, fishing, watering gardens, and duck
                      keeping. Then each student holds up a slate listing two
                      uses from memory, look at all slates and re-explain
                      missing uses if many are wrong before moving on.

2. Peer Facilitator   In mixed groups, pool the pond poems, songs, or sayings
[changed: CL-02]      each student brings from family or neighbours. Groups
                      take turns as Reader, Writer, and Checker on chart paper
                      without names or home details, swapping roles for each
                      item. Read the combined collection aloud in class.

3. Peer Facilitator   In pairs, sort the collected lines into pond, river, and
                      sea piles and count each pile. Add the pairs' counts
                      into one class table on chart paper. Discuss what the
                      collection says about how the community values ponds.

4. Lead Educator      In week 2, open a lesson with four short questions on
[changed: EB-01]      pond uses and the sayings collection, answered from
                      memory on slates with charts and notes out of sight.
                      Show the answers straight after so each student checks
                      their own. Nothing is collected, marked or recorded.

------------------------------------------------------------------------------
BEFORE YOU START
- Needs: Students can recall pond songs or sayings and chart paper is
  available.
  If not: Use two educator-provided examples and hold one class discussion;
  combine steps 2 and 3 in one period.
------------------------------------------------------------------------------
```

## 9. What to watch for
- **The town track is gone.** The sequence serves the rural main track only; town teachers get no variant — the guide map, historical map and trash survey were deferred as a follow-on, over the unit cap.
- **Home ponds became assigned ponds.** "The pond nearest their home" is now educator-assigned ponds with whole-class visits and a rota — check the rota works for real class sizes and walking distances.
- **Slates are assumed, never listed.** All four EB-04 checks hinge on every student holding up a slate, but no BEFORE YOU START lists slates among its needs.
- **No teacher review yet**, as with every walkthrough here.
