# Walkthrough 3 — Vietnam: folk tales and retelling

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 7 November 2026 (`python3 -m lsb.regress`, folder `runs/regress-3/vietnam-folktales`). The source chapter is an original test input written for this project and set in a Vietnamese lower-secondary literature class: [tests/fixtures/vietnam-folktales-source.md](../../tests/fixtures/vietnam-folktales-source.md). No teacher has reviewed the result yet.

| | |
|---|---|
| **Source** | A 6-week Grade 6 literature unit, "Folk Tales and Retelling", written to the national education programme |
| **Result** | Passed: 4 units (one foundation unit, then three that can run side by side), 22 model calls, about $4.25 at list price |
| **Kept** | Folk-tale structure and character types, two set tales with story maps, character and lesson with a quotation, retelling aloud, collecting a tale by word of mouth, writing an original tale of 400–600 words |
| **Removed** | Videos of each child uploaded to a parents' messaging group; winners' names on the school loudspeaker; visits to elderly neighbours pupils don't know; a class book sold at the fair with pupils collecting the money; a two-lesson history lecture; the country, ministry, festival, app and currency |
| **Added** | Whole-class checks and recall from memory (evidence-based); an unranked class book of everyone's tales (Connected Learning). Participatory budgeting rightly abstained everywhere |

## 1. The starting point
A teacher's book for six weeks of 45-minute lessons. It defines a folk tale (three parts; character types; a magical helper), opens with a two-lesson lecture on the history of collecting folk tales, reads two tales from the textbook with story maps, discusses character with evidence, then has pupils retell a tale in under three minutes. The best retellers are chosen to perform at the school's festival and named on the loudspeaker; the teacher films every retelling and uploads it for parents. Pupils collect a tale from a grandparent, or from "elderly neighbours they don't know well" if their family has no storyteller. Finally each pupil writes their own tale, and "the best tales" are printed in a book sold at the fair, with pupils collecting the money.

## 2. What the pipeline kept, and why
- **The definition of a folk tale was folded in, not deferred.** Every unit and the final tale rely on the three parts and the character types, so unit 1 step 1 teaches them and keeps the chart for later units.
- **Deep work survives in full:** a story map for each tale, two quiet writing tasks on each tale's lesson with a supporting quotation, timed retelling practice in pairs, two full lessons of drafting the pupil's own tale, a partner's suggestion and a full revision lesson.
- **The structure allows parallel work.** Units 2, 3 and 4 all build only on unit 1. Decompose warned that run one after another they take 10 weeks against the source's 6, and suggested alternating units 2 and 3 in the same weeks.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Teacher films each retelling and uploads it to a parents' messaging group (§2.5) | Left out | Devices, internet, and children's images shared online |
| Best retellers chosen and named on the loudspeaker (§2.5) | Left out | Ranks pupils and singles them out by name |
| Pupils visit elderly neighbours they don't know well (§2.6) | Left out; replaced by a tale the educator tells the whole class | Unsupervised contact with unfamiliar adults off school grounds |
| The best tales printed and sold at the fair, pupils collecting the money (§2.7) | Left out; every tale goes into an unranked class book instead (see §5) | Minors handling money, a printing cost, and ranking pupils' work |
| Two-lesson lecture on the history of collecting folk tales (§2.2) | Set aside as lecture only | No unit needs it |

## 4. The units

```
                 MLS-FOLK-01  Structure and story maps (2 weeks)
                 /                   |                     \
MLS-FOLK-02 Character and lesson   MLS-FOLK-03 Retelling and      MLS-FOLK-04 Writing our own
(2 weeks)                          collecting a tale (3 weeks)    folk tale (3 weeks)
```

## 5. What each stage did

**Evidence-Based (ran first), applied in units 1, 2 and 3.**
- **EB-04 Checking for understanding.** Right after the structure is explained, every pupil answers two questions at once: which part a line belongs to (one, two or three fingers) and a character type (on scrap paper, held up). In unit 2, every pupil writes a character trait and a supporting line and holds it up. The educator rereads a key line if many lack evidence.
- **EB-01 Retrieval practice.** Unit 1's last step: pupils label their story maps with the parts and types **from memory**, with the chart covered, then uncover it and check their own.
- **EB-02 Spaced practice.** Unit 3 opens with the parts and types written from memory, at least a week after unit 1, then self-checked.
- **Abstained on unit 4** (the culminating tale), with reasons: the chart is meant to stay in view while pupils write, and modelling a complete tale would hand them the answer (EB-03's "never").

**Connected Learning, applied in unit 4 only.**
- **CL-04 Collective shared purpose:** every final copy is tied into one class book with a chart-paper cover, with **no choosing of best tales, no order of quality, and no marks**. A pupil may leave their name off or keep their tale out of the book. This keeps the source's "class book" idea and removes what made it unsafe (selling, ranking, money).
- Units 1–3 **abstained**. Unit 3 already credits choice (CL-01), timed pairs (CL-02) and the class as an audience for retellings (CL-05). A class book of collected home tales was rejected because it "would show which pupils have no storyteller at home".

**Participatory Budgeting abstained on every unit.** The fit-gate fails: no fixed amount with more options than fit, and every unit is sustained individual reading, retelling or writing that a vote would interrupt. On unit 4 it also noted that a ballot on the class book "could rank pupils' work". With every unit abstaining, the stage made no review call.

## 6. What the reviewers caught (the inclusion problem)
This run shows why every stage's review, and the repair round, matter.

1. **Decompose review, attempt 1:** a fallback had the educator tell a tale in class for pupils with no older person at home, and "only those pupils" wrote it down, so "the whole class can see which children have no older relative at home". Revised in attempt 2.
2. **Evidence-based and Connected Learning reviews:** both found the same problem in unit 3 step 2, a step neither stage had changed. As written, every pupil had to collect a tale from an older person in their own household, with no other way to do the task. Recorded as a **late issue**.
3. **Repair round 1** added the educator's tale as an option, but the reviewer found it still singled pupils out: only those without a storyteller would be writing during that lesson.
4. **Repair round 2:** the educator tells one tale to **the whole class, and every pupil writes it down**. Then each pupil privately chooses which tale to keep: that one, one they've heard before, or one from home. The step ends: "Don't ask who lives at home, why, or which option was used." The review passed.

## 7. Before → after (unit 3, step 2)

| Before (after decompose) | After repair round 2 |
|---|---|
| Each pupil collects a tale from a grandparent or older person in their own household; no other option | The educator tells a tale to the whole class and every pupil writes it; each pupil then chooses which tale to keep (that one, one heard before, or one from home). No visits outside the household; only the tale is written; nobody is asked who lives at home or which option they used |

## 8. Teacher card (unit 3, from `cards.txt`)

```
MLS-FOLK-03: Retelling Aloud and Collecting a Tale by Word of Mouth
3 weeks. Builds on MLS-FOLK-01.
==============================================================================
Goal: Turns each pupil's story map into an oral retelling of one tale in their
own words, and has them write down a tale told to them by word of mouth.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Recall from MLS-FOLK-01: with the class chart covered
[changed: EB-02]      and notebooks closed, each pupil writes the three parts
                      of a folk tale and two character types from memory on
                      scrap paper, then the chart is uncovered so each pupil
                      checks their own; nothing is collected. Each pupil then
                      chooses one of the two tales and takes out its story
                      map. Pupils put the textbook away. From now on they
                      retell from the story map only.

2. Lead Educator      In a lesson early in the week, the Lead_Educator tells
                      one folk tale aloud from memory to the whole class, and
                      every pupil writes it in their notebook. Each pupil then
                      chooses which tale to keep: this one, one they have
                      heard told before, or one from an older person at home.
                      Pupils never visit neighbours or others outside their
                      household and write only the tale. Don't ask who lives
                      at home, why, or which option was used.

3. Peer Facilitator   In pairs, pupils take turns retelling their chosen tale
                      in their own words, using only the story map. The
                      listening partner watches the classroom clock and says
                      when three minutes are up. Pairs practise this way over
                      several lessons until each pupil finishes in under three
                      minutes.

4. Lead Educator      Each pupil in turn retells their tale aloud in their own
                      words in under three minutes, without the book, holding
                      only the story map. Spread the retellings over as many
                      lessons as the class size needs.
------------------------------------------------------------------------------
BEFORE YOU START
- Needs: A classroom clock or the educator's watch to time three minutes.
  If not: The educator calls out when three minutes are up for the whole class
  during pair practice.
- Needs: Enough lessons for every pupil to give a final retelling (a large
  class needs several periods).
  If not: If a week is lost, cut pair practice to one lesson and start the
  final retellings sooner, so the unit still ends within 3 weeks.
```
*(One "Before you start" entry is omitted here: see §9.)*

## 9. What to watch for
- **A stale fallback.** The card's first "Before you start" entry still reads "Each pupil has a grandparent or another older person at home", from before the repair; its fallback is now the main step. The repair is limited to what reviewers flag, and this fallback wasn't flagged. It's harmless but redundant, and an adapter should delete it.
- **Ten weeks if run in sequence.** Units 2–4 can run side by side after unit 1; a teacher who runs them one after another needs 10 weeks, not the source's 6.
- **"The Lead_Educator" appears inside a step's text** (unit 3 step 2). Steps should say "the educator"; the role name belongs in the left column.
- **Two late issues were the same problem in different words** (found by two stages). The repair handled both, but the log counts two.
