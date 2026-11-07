# Walkthrough 5 — Bangladesh: letters, sounds and first words

> **Live output, not a hand-written answer.** Everything below comes from one run of the pipeline on 7 November 2026 (`python3 -m lsb.regress`, folder `runs/regress-3/bangladesh-letters`). The source chapter is an original test input written for this project and set in a Bangladeshi Class 1 classroom: [tests/fixtures/bangladesh-letters-source.md](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/tests/fixtures/bangladesh-letters-source.md) (copied into this folder as [source.md](./source.md)). No teacher has reviewed the result yet.

| | |
|---|---|
| **Source** | A 6-week Class 1 language chapter, "Letters, Sounds and First Words": the first eight letters, two a week, then blending sounds into words |
| **Result** | Passed: 4 units fitting the source's 6 weeks (two run side by side), 21 model calls, about $3.56 at list price |
| **Kept** | The explicit letter-sound routine (card, sound said back three times, tracing, chalk on slates, two pictures), daily blending of five words, partner reading, daily reading practice, weekly listening, and each child reading a sentence aloud |
| **Removed** | Children who can't yet read moved to the back benches with colouring sheets; a "slow readers" chart naming children on the wall; a workbook parents must buy; nightly smartphone videos of each child reading; a history lecture with a date to copy; the language's, script's, curriculum body's and currency's names |
| **Added** | Thumbs and finger checks every child answers at once, and letters written from memory (evidence-based). **Connected Learning and participatory budgeting both abstained on every unit**, which is the right answer for a decoding drill |

## 1. The starting point
A teacher's guide for six weeks of daily 40-minute lessons. It says children learn faster when taught directly which sound each letter stands for and how to blend sounds into words. It teaches the first eight letters in textbook order, two a week, with a clear routine, then blends short words from known letters. It also opens with a two-lesson history lecture, moves children who can't yet read to the back benches with colouring sheets "so that they don't slow down the others", writes their names on a "slow readers" chart "to encourage them to work harder", asks parents to buy a workbook and send a nightly video of their child reading, and ends with each child reading a sentence standing in front of the class.

## 2. What the pipeline kept, and why
- **The decoding routine, intact.** Every new letter gets the same explicit sequence, and every unit keeps daily practice. This is the chapter's core and the part a scaffold must not dilute.
- **Every child keeps reading.** Rather than separating struggling readers, the daily ten-minute practice is explicitly for "all children".
- **The weekly listening stays, with nothing written down.** The teacher still hears every child read the week's words; the step says "Do not write down names or results."
- **The timing fits the source.** Letters 1–4 (weeks 1–2), then letters 5–8 and blending side by side (weeks 3–4), then reading words and a sentence (weeks 5–6). Decompose noted that blending could start a little earlier, once three letters are known.

## 3. What was removed, and why

| In the source | What happened | Why |
|---|---|---|
| Children who can't yet read go to the back benches with colouring sheets (§3.5) | Left out; all children do the reading practice | Excludes and singles out the children who most need the practice |
| A "slow readers" chart naming children on the wall (§3.6) | Left out; the listening stays, with nothing recorded | Public individual performance records |
| Parents buy the companion workbook (§3.6) | Left out | A cost to families |
| Parents send a smartphone video of their child reading every evening (§3.6) | Left out | Devices, and children's images sent to the teacher |
| Two-lesson history of the script, with a date to copy (§3.2) | Set aside as lecture only | No unit needs it |
| "Children learn to read faster when…" (§3.1) | Not repeated on the cards | Flagged as an unsupported outcome claim; cards describe what to do, not what it achieves |

All of these were also reported as **source flags**.

## 4. The units

```
MLS-LETTERS-01  Sounds of the first four letters (2 weeks)
        │                                  │
        ▼                                  ▼
MLS-LETTERS-02  Letters five to eight   MLS-LETTERS-03  Blending sounds into
(2 weeks)                               short words (2 weeks)
        │                                  │
        └──────────────┬───────────────────┘
                       ▼
MLS-LETTERS-04  Reading words and a sentence aloud (2 weeks)
```

## 5. What each stage did

**Evidence-Based (ran first), applied in units 1, 2 and 3.**
- **EB-04 Checking for understanding.** After each letter's pictures, the teacher says two more words and every child shows thumbs up or down at once for whether it starts with the sound (unit 1). In the blending unit, the fifth daily word becomes a check: children read it silently, then hold up one or two fingers for which of two spoken words it is (unit 3). The teacher looks at every hand and re-teaches if many are wrong, naming no one.
- **EB-01 Retrieval practice**, units 1 and 2: with the cards hidden, the teacher says each earlier sound and children write its letter on their slates **from memory**, then check against the card shown straight after.
- **EB-02 Spaced practice**, unit 2: letters five and six are reviewed from memory in the last lessons of week 2, at least a week after they were first taught.
- **Abstained on unit 4**, because every lesson already has children say each sound from memory and blend words, so an added quiz "would repeat this routine".
- **The review held the edit to the card.** Unit 1's first recall asked only two questions, and the reviewer pointed out that EB-01 allows 3 to 5. The revision says the two week-1 sounds four times in mixed order.

**Connected Learning abstained on all four units.** It credited what's already there (partners swap reading, the sentence reading has the class as its audience) and judged that a theme choice or a class tally "would add busywork for Class 1 children without closing a real gap".

**Participatory Budgeting abstained on all four units.** Every unit falls under the fit-gate's **"Always skip PB: foundational decoding and fluency drills"**: "a vote or ledger here would add friction and break the drill."

## 6. What the reviewers caught
- **Decompose review, attempt 1, a safety and inclusion blocker:** "every child must stand alone in front of the class and read a sentence aloud, with no support… That exposes the struggling readers the source wanted to single out." Attempt 2 rewrote the final reading (see §7).
- **Evidence-Based review:** the sentences for the final reading were to be written "on chart paper", a purchased material many low-resource classrooms lack. No stage had touched that step, so it was recorded as a **late issue**. One repair round changed it to "strips of reused paper or card, or on the board".

## 7. Before → after (the final reading)

| In the source | After |
|---|---|
| Each child reads a sentence standing in front of the class | Each child reads their own sentence **standing at the front or from their seat, as the child chooses**. The teacher stands beside them and, if the child stops at a word, points to each letter and blends it with them "so every child finishes the sentence". No correcting or commenting in front of the class. With a large class, readings spread over two lessons |
| The names of children who can't read go on a wall chart | The teacher listens to every child each week; "Do not write down names or results" |

## 8. Teacher card (unit 4, from `cards.txt`)

```
MLS-LETTERS-04: Reading Words and a Sentence Aloud
2 weeks. Builds on MLS-LETTERS-02, MLS-LETTERS-03.
==============================================================================
Goal: Brings all eight letter sounds and blending together. Each child ends by
reading aloud a sentence of short words they have learned.

WHO                   WHAT TO DO
------------------------------------------------------------------------------
1. Lead Educator      Recall from MLS-LETTERS-03: use the blending routine,
                      with the eight letter cards from MLS-LETTERS-02 on the
                      board. Each day, write five short words made from the
                      eight letters. Point to each letter while the class says
                      its sound, then sweep your finger under the word while
                      the class blends it and says the word.

2. Peer Facilitator   In pairs, children read the same five words to a
                      partner. Then partners swap, so each child reads.

3. Lead Educator      End every lesson with ten minutes of reading practice
                      from the textbook word list. All children read from the
                      list.

4. Lead Educator      At the end of each week, during the reading practice,
                      listen to each child read that week's words. Do not
                      write down names or results.

5. Lead Educator      Before the last lesson, write short sentences on strips
                      of reused paper or card, or on the board, using only
                      words the class has learned. Write one sentence for each
                      child.

6. Lead Educator      In the last lesson, each child reads their sentence
                      aloud, standing at the front or from their seat, as the
                      child chooses; with a large class, spread the readings
                      over the last two lessons. Stand beside the child. If
                      the child stops at a word, point to each letter and
                      blend the sounds together with them, so every child
                      finishes the sentence. Don't correct or comment on any
                      child's reading in front of the class.
------------------------------------------------------------------------------
BEFORE YOU START
- Needs: Chart paper is available for the sentences.
  If not: Write the sentences on the board before the last lesson.
- Needs: Every child is present for the last lesson.
  If not: A child who is absent reads their sentence aloud on the next day
  they attend.
```

## 9. What to watch for
- **A stale fallback.** "Needs: Chart paper is available for the sentences" is left over from before the repair, which moved step 5 to reused paper or the board. The repair only changes what the reviewer flags. Harmless, but an adapter should delete it.
- **Weekly listening for a large class.** Hearing every child read the week's words inside ten minutes of practice may take several lessons; the card doesn't say how to spread it.
- **"The textbook word list."** Steps rely on the class textbook's list; the fallback copies the known-letter words onto the board if there are no textbooks.
- **No language-specific content.** The cards say "the first letter" and "a short word" because the pipeline is region-neutral. The adapter supplies the actual letters and words.
