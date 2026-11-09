# Walkthrough 6 — Mexico: migration stories, past and present

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 7 November 2026 (`python3 -m lsb.regress`, folder `runs/regress-3/mexico-migration`). The source chapter is an original test input written for this project and set in a Mexican lower-secondary history class: [tests/fixtures/mexico-migration-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/mexico-migration-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.
> Decision trace: [decisions.md](./decisions.md) · Full final cards: [final.md](./final.md) · Localizations: [localizations.md](./localizations.md)

> **Locale note:** The generalized, kept, or relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

| | |
|---|---|
| **Source** | An 8-week Grade 8 history block, "Migration Stories, Past and Present" |
| **Result** | Passed on the first attempt: 3 units, 7 weeks of content (one week of slack), 13 model calls, 191,189 input / 58,178 output tokens, the smallest run in the sweep |
| **Kept** | Push and pull factors, three primary sources analysed with the same four questions, a 1900-to-today timeline, and a two-page source-based explanation drafted, peer-read and revised |
| **Removed** | Students asking family members whether relatives had legal documents or live abroad without papers; family photos pinned on a map with the family name; an unsupervised Saturday trip to the bus terminal to question travellers; students paying to print timelines in colour; the programme's, state's, country's and currency's names |
| **Added** | Finger and scrap-paper checks every student answers at once, and recall from memory (evidence-based); an unranked class book of everyone's explanations (Connected Learning). Participatory budgeting abstained everywhere |

## 1. The starting point
A teacher's guide for eight weeks of 50-minute sessions. It defines migration and push and pull factors, then gives a three-session lecture on the great migrations of history with dates and a route map to copy. Students read three short primary sources (a farm worker's letter from 1945, a newspaper report from 1960, a song verse) and build a timeline. Then it asks students to interview family members about migration "including whether they had legal documents to cross the border and whether any relatives are living abroad without papers", to pin family photographs labelled with the family name on a classroom map, to visit the bus terminal on their own on a Saturday to question travellers, and to bring 50 pesos each for colour printing. It ends with a two-page explanation of one migration, using the sources as evidence.

## 2. What the pipeline kept, and why
- **The definitions lead the sequence.** Push and pull factors, internal and international migration are taught in unit 1 step 1 and written on a class chart, because every unit and the final explanation use them.
- **Only the lecture content the units need was kept.** The three-session lecture was set aside, *except* the dates and route map the timeline relies on, which became a short talk at the start of unit 2. This is the fold-in rule at work: defer background, keep what a unit relies on.
- **Source analysis, one source per step.** Each source gets its own step and the same four questions (who, when, why, which factors), so the analysis isn't bundled into one overloaded step.
- **Sustained writing.** Two full sessions of drafting, a partner's written suggestion, and a full revision session.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Interview family about whether relatives had legal documents or live abroad without papers (§3.5) | Left out entirely; the adapter is told to decide on a safe version | Household data and a real risk of exposing families' immigration status |
| Family photographs pinned on a classroom map with the family name (§3.5) | Left out | Images and family names displayed |
| Groups visit the bus terminal on their own on a Saturday to question travellers (§3.6) | Left out | Unsupervised off-site movement and contact with strangers |
| Each student brings 50 pesos for colour printing (§3.7) | Left out; the hand-made timelines are used directly | Students handling money; a purchase and a printing service |
| Three-session lecture on the great migrations (§3.2) | Set aside, except the dates and route map, which became a short talk in unit 2 | Background beyond what the timeline needs |

All four were also reported as **source flags**. For the family interviews, the pipeline didn't invent a "safe version" of its own. It set the section aside and told the adapter to decide, because a safe design for a topic this sensitive is a judgement for people who know the community.

## 4. The units

```
MLS-MIGRATE-01  Push and pull factors in primary sources (2 weeks)
        │
        ▼
MLS-MIGRATE-02  Building a migration timeline, 1900 to today (2 weeks)
        │
        ▼
MLS-MIGRATE-03  Writing and revising an explanation of a migration (3 weeks)   ← also builds on 01
```

## 5. What each stage did

**Evidence-Based (ran first), applied in units 1 and 2.**
- **EB-04 Checking for understanding.** Before students read the sources, the teacher reads three reasons for moving ("the rains failed for three years", "an uncle has work waiting in the city") and every student shows one finger for push or two for pull, all at once. In unit 2's talk, after each migration every student holds up a push factor on scrap paper. The teacher re-explains if many are wrong.
- **EB-01 Retrieval practice**, unit 2: in week 2, two lessons open with three questions on push and pull factors and the talk's migrations, answered with the chart and notebooks put away, then self-checked.
- **Credited, not added:** the talk is already paired with a route map and the timeline strip (EB-05).
- **Abstained on the explanation unit:** students write with their sources and timeline open as evidence, so a closed-book quiz wouldn't help, and a worked example would hand them the answer.

**Connected Learning, applied in unit 3 only.**
- **CL-04 Collective shared purpose:** every final copy is tied with string into one class book with a used-paper cover. Names are optional and nothing is marked.
- Units 1 and 2 **abstained**, crediting student choice (each student picks their own examples and five timeline events) and the class chart.

**Participatory Budgeting abstained on all three units.** No fixed amount with more options than fit, and the work is individual source analysis and writing. With every unit abstaining, the stage made no review call.

## 6. What the reviewers caught
Nothing blocking. The decompose review passed the first attempt, and the Evidence-Based and Connected Learning reviews passed their edits first time. No late issues were found, so no repair round was needed. This was the only run in the sweep where no later review found anything.

## 7. Before → after (unit 1)

| Before (after decompose) | After |
|---|---|
| Explain push and pull factors; students go straight to reading the sources | Explain the factors, then every student classifies three reasons for moving with fingers before reading (EB-04) |
| Three sources, each with the same four questions | Unchanged |
| Students write their own definitions with two examples each | Unchanged |

## 8. Teacher card (unit 1, from `cards.txt`)

```
MLS-MIGRATE-01: Push and Pull Factors in Primary Sources
2 weeks. Starts fresh (no earlier unit needed).
==============================================================================
Goal: Gives students the push and pull vocabulary and their own written
analysis of three primary sources, the evidence base the later timeline and
explanation draw on.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Explain that migration is the movement of people from
                      one place to live in another. It can happen within a
                      country (internal) or between countries (international).
                      Explain push factors (war, drought, poverty, lack of
                      land or work) and pull factors (work, land, safety,
                      family already there), and that most migrations have
                      several of each. Write both lists on chart paper as the
                      class chart, and have students copy them into their
                      notebooks.

2. Lead Educator      Before students read the sources, read out three short
[changed: EB-04]      reasons for moving, such as "the rains failed for three
                      years" or "an uncle has work waiting in the city". Every
                      student shows one finger for a push factor or two for a
                      pull factor at the same time. Look at all the hands, and
                      if many are wrong, re-explain using the class chart
                      before moving on. Nothing is recorded and no one is
                      named.

3. Lead Educator      Students read the textbook letter from a farm worker
                      writing home in 1945. Each student answers in their
                      notebook: who wrote it, when, why, and which push or
                      pull factors it shows, using the class chart.

4. Lead Educator      Students read the textbook newspaper report from 1960 on
                      families arriving in the capital. Each student answers
                      in their notebook: who wrote it, when, why, and which
                      push or pull factors it shows.

5. Lead Educator      Students read the textbook song verse about leaving
                      home. Each student answers in their notebook: who wrote
                      it, when, why, and which push or pull factors it shows.

6. Lead Educator      Each student writes in their notebook a definition of
                      push factors and a definition of pull factors in their
                      own words. Under each definition, they give two examples
                      from the migrations in the three sources.
```

## 9. What to watch for
- **Migration is personal for many students.** The cards ask only about historical sources and the textbook's migrations, which is safe; but the topic can still touch students' own families in discussion. That's for the teacher's judgement, and the pipeline flagged the family-interview section for the adapter to decide on.
- **"Present" migrations rely on the textbook.** The final task allows "a migration, past or present", but the sources are all historical; a teacher may need to supply a present-day source.
- **The timeline goes from 1900, but the talk covers earlier migrations too.** Students choose five events within the strip's range; the talk's earlier migrations are context only.
- **Chart paper.** The class chart assumes chart paper, with a fallback to the board. Unlike in Bangladesh, no reviewer flagged it here; reviewers aren't fully consistent across runs.
