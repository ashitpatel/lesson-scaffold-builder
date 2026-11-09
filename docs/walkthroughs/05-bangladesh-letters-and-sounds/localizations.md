# Localizations — Bangladesh: letters, sounds and first words

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) generalizes the Bangladeshi lesson to generic cards. These three runs instead generalize, then relocalize to Finland, Morocco, and Thailand. All three passed. Early-reading steps run close to their word caps, so this trio leans hard on the safety nets: Finland lands one replacement while a second matches nothing; Morocco and Thailand approve two and three replacements respectively, then revert all of them when the longer terms newly break check D11 — while every addition lands.

## 1. Finland (Finnish)

Run `runs/bangladesh-finland-1`: pass, 2 units, 6 weeks, 12 calls, 385,387 in / 70,295 out tokens, Flesch 74.4. Locale notes asked for a transparent-orthography framing (blending is trivial; long multisyllabic words are the challenge), Finnish names, no purchased workbook (materials are free by law) — and a dignity guard: no public ranking of strugglers; private teacher records and in-lesson support instead.

Final cards: [final-finland.md](./final-finland.md).

- Logged 8 items: the history lecture (Brahmi, Language Movement, 21 February) and the workbook purchase (bazaar, taka) all dropped; `NCTB` → generic `the textbook` and `Bengali script` → generic `the first eight letters` survived.
- Proposed 2, approved 2: `the textbook` → `the free school Aapinen` applied in 2 places; `the first eight letters` → `the first eight Finnish letters` matched nothing and was left generic ("not found, left generic").
- 3 additions proposed, all 3 kept: the sound routine uses "Finnish words like sauna and metsä"; pairs become "the usual parityö"; the class blends "sitting in the lukupiiri on the mat".

## 2. Morocco (Arabic)

Run `runs/bangladesh-morocco-1`: pass, 2 units, 6 weeks, 12 calls, 383,615 in / 60,391 out tokens, Flesch 80.3. Locale notes asked for right-to-left Arabic script with position-changing letterforms, school Arabic (not Darija) for drills, Dirhams — and a sacredness guard: the script carries Quranic sacredness, so never use religious words as throwaway items and never let pupils discard or step on letter cards.

Final cards: [final-morocco.md](./final-morocco.md).

- Logged 8 items; 2 proposals approved as proposed (`textbook` → `Moroccan Ministry of National Education textbook` in 3 places; `letters` → `school Arabic letters` in 5 places) — then reverted as a set: "replacements newly broke ['D11']; cards stay generic." The long official terms overflowed steps already near the cap.
- 4 additions proposed, all 4 kept: tracing moves "right to left as school Arabic is written"; picture names use "school Arabic names, not Darija home words"; review covers letters "in their start, middle, and end word forms"; cards go "in their box, kept clean and off the floor".

## 3. Thailand (Thai)

Run `runs/bangladesh-thai-1`: pass, 2 units, 6 weeks, 12 calls, 383,993 in / 61,907 out tokens, Flesch 78.3. Locale notes asked for Thai script (44 consonants, tone marks, no spaces between words — word boundaries are the core challenge), Thai names, baht — and a Buddhist-school-culture guard: respect routines, gentle group-based competition, never single out a struggling reader publicly.

Final cards: [final-thai.md](./final-thai.md).

- Logged 8 items; 3 proposals approved as proposed (`reading` → `Thai reading`; `textbook` → `Thai Ministry of Education textbook`; `letter` → `Thai letter` in 8 places) — then reverted as a set on D11, same as Morocco.
- 4 additions proposed, all 4 kept: pictures come "from familiar Thai animals, fruits, or foods"; slate copying includes "copying any tone mark with the letter"; board words leave "wide spaces between words at first since Thai normally runs together"; review starts "after the wai respect routine".

## What this trio shows

Replacements are word-hungry and early-reading steps are word-poor: two of three runs approved replacements and then correctly rolled them back when D11 broke, which is the revert path earning its keep twice in one trio. The additions, being short insertions trialed one by one, all landed — and they carry the deepest locale knowledge here: positional letterforms, tone marks, missing word spaces, parityö, lukupiiri, the wai, and card-handling rules that honor the script's sacredness. The highest readability scores in the sweep (Flesch 74–80) fit a lesson for beginning readers.
