# Localizations — Vietnam: folk tales and retelling

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) generalizes the Vietnamese lesson to generic cards. These three runs instead generalize, then relocalize to Iceland, Saudi Arabia, and a Yoruba community in Nigeria. All three passed. This trio is the strongest demonstration of the additions phase: almost every locale marker in the source (Tết, Zalo, VND, MOET) was dropped with its segment, so replacements had nothing to bite on — while the additions wove saga evenings, Ramadan storytelling, and Ijapa tales through every unit. Iceland also exercises two safety paths live: a replacement whose generic text is not found, and a per-addition drop.

## 1. Iceland

Run `runs/vietnam-iceland-1`: pass, 3 units, 7 weeks, 16 calls, 528,785 in / 76,106 out tokens, Flesch 64.4. Locale notes asked for the saga and hidden-people storytelling tradition, Icelandic names, krona, a midwinter storytelling evening for parents as the performance — and a sensitivity guard: some families genuinely hold elf beliefs, so treat them as living tradition, never superstition to debunk.

Final cards: [final-iceland.md](./final-iceland.md).

- Logged 7 items: the programme, MOET, Vietnam, Tết, Zalo group, and 20,000 VND all dropped with their segments; only the subject name `Ngữ văn 6` → generic `Middle grade band` survived.
- Proposed 1, approved 1 (`Íslenska, miðstig`) — but the generic text was not found in the cards, so the run noted "'Middle grade band' not found, left generic" and changed nothing. An approved replacement that lands nowhere, handled gracefully.
- 4 additions proposed, 3 kept: characters take "Icelandic names"; home collection reaches for "a saga episode or a hidden-people account told with respect"; the rota becomes "practice toward a midwinter storytelling evening for parents". Addition 0 (a hidden-person example) was dropped on its own because it would newly break D11 — the per-addition drop path, keeping one tight step from wiping the other three.

## 2. Saudi Arabia

Run `runs/vietnam-saudi-1`: pass, 3 units, 6 weeks, 17 calls, 559,053 in / 83,719 out tokens, Flesch 62.5. Locale notes asked for Kalila wa Dimna and 1001 Nights as the tale stock, a Ramadan family storytelling evening, gender-segregated groupings — and strict sensitivity guards: magic must avoid any hint of shirk (no charms or fortune-telling as real); no video uploads of girls anywhere.

Final cards: [final-saudi.md](./final-saudi.md).

- Logged 7 items, all dropped with their segments (Tết survived only as the generic `seasonal school celebration`, which drew no proposal).
- Proposed 0: "no proposals for the target locale; cards stay generic."
- 4 additions proposed, all 4 kept — and they carry the sensitivity notes into the steps: the magic pot is framed "as mere invention" against any hint of shirk; pairs work "within their class group"; character evidence comes "as in Kalila wa Dimna tales"; home collection names tales "such as one shared on a Ramadan evening".

## 3. Yoruba community in Nigeria

Run `runs/vietnam-yoruba-1`: pass, 3 units, 7 weeks, 16 calls, 527,844 in / 77,883 out tokens, Flesch 65.7. Locale notes asked for Yoruba and English names, naira, tortoise (Ijapa) tales and talking-drum rhythms as the tale stock — and an ownership guard: elders own the stories, so pupils collect from willing family elders only, never strangers, and perform with respect, not parody.

Final cards: [final-yoruba.md](./final-yoruba.md).

- Logged 6 items, all dropped with their segments.
- Proposed 0: "no proposals for the target locale; cards stay generic."
- 5 additions proposed, all 5 kept: story structure is marked "with talking-drum rhythms marking beginning, middle, and ending"; the fisherman tale uses "Yoruba and English names as families use them"; retelling goes "with respect for its lesson, without parody"; collection happens "only if the elder is willing, such as a familiar Ijapa tale"; and the trickster slot names "a trickster like Ijapa".

## What this trio shows

When the source's locale markers die with dropped segments, replacements correctly do nothing — and the additions phase is what makes the lesson teachable in Reykjavik, Riyadh, or Ibadan anyway. The sensitivity notes did real work here: shirk framing, gender-segregated pairing, respect-not-parody, and elder ownership all landed as concrete step text, not preamble. And Iceland shows both safety nets at once: a replacement that matches nothing changes nothing, and one over-long addition is dropped without taking the rest down. Readability held at Flesch 62–66.
