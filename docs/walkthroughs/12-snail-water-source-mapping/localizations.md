# Localizations — ATREE S.N.A.I.L.: water source mapping

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) strips the lesson to generic cards. These three runs instead strip and then relocalize to the approved "Three waters" trio: a desert village in Rajasthan, a Mumbai high-rise, and a Bangladesh char village. All three passed. This lesson carries almost no locale markers (no place names, currencies, or organizations reach the sequence), so replacements again find nothing — and this trio now shows the answer to that: sixteen landed additions that teach the same mapping spine through baolis, BMC taps, and arsenic-marked tubewells.

## 1. Desert village in western Rajasthan, India

Run `runs/snail-mapping-rajasthan-2`: pass, 2 units, 6 weeks, 12 calls, 392,259 in / 56,182 out tokens, Flesch 64.5. (Two units rather than the base run's three: the decompose grouped the sections differently this time — ordinary model variance across runs.) Locale notes asked for extreme-scarcity framing — women fetching water from a distant baoli stepwell, no lake or river nearby — Hindi names, and a caste-loaded sensitivity guard: never assign water-carrying roles by pupil background; replace any family water-use register with an anonymous class tally.

Final cards: [final-rajasthan.md](./final-rajasthan.md).

- Logged 0 items: "nothing locale-specific to relocalize." No proposals step ran.
- 6 additions proposed, all 6 kept: sources include "the baoli stepwell and household tanka"; distances run "along sandy paths, counting steps to the baoli or tanka"; storage is "called matka or tanka here"; surroundings name "dust, goat droppings and plastic near the baoli steps"; one access difficulty is "the long summer walk to the baoli"; the village map centers on "the baoli, tanka or hand pump".

## 2. High-rise housing society in Mumbai, India

Run `runs/snail-mapping-mumbai-2`: pass, 3 units, 7 weeks, 16 calls, 526,297 in / 82,512 out tokens, Flesch 67.6. Locale notes asked for piped BMC municipal water with overhead tanks and tanker supply — no wells, lakes, or river access, so all experiments tabletop (tap, bucket, bottle) — Marathi and Hindi names, monsoon flooding instead of any lake-shore trip, and a housing-society notice board instead of any village-chief follow-up.

Final cards: [final-mumbai.md](./final-mumbai.md).

- Logged 1 item: the dropped DRCSC credit line (agency, no generic).
- Proposed 0: "no proposals for the target locale; cards stay generic" — the empty-proposals path.
- 6 additions proposed, all 6 kept: homes are mapped "in the housing-society building and floor"; signs carry "Marathi and Hindi labels like nal and tanki"; stagnant water means "monsoon flooding around the building"; waterlogging reads "like overhead-tank overflow and tap leakage"; sources list "the BMC tap, overhead tanki, tanker, bucket, and bottle"; the class list goes up "for the housing-society notice board".

## 3. River-island char village in Bangladesh

Run `runs/snail-mapping-char-2`: pass, 3 units, 7 weeks, 20 calls, 663,536 in / 92,862 out tokens, Flesch 68.4. Locale notes asked for arsenic-safe/unsafe well marking, yearly re-mapping after floods, boats, Bangla names — and a shame guard: asking about real family earnings or harvests is shame-loaded in a bad year, so use the teacher's example figures, never real family data.

Final cards: [final-char.md](./final-char.md).

- Logged 1 item: the dropped DRCSC credit line, as in Mumbai.
- Proposed 0: "no proposals for the target locale; cards stay generic."
- 4 additions proposed, all 4 kept: home sources are named "tubewell, pukur, and nodi ghat"; the shared signs use "green and red marks for safe and arsenic-unsafe tubewells"; observation covers "flood silt around the tubewell platform"; the village map adds "the river ghat and boat landing used when floods cover paths".

## What this trio shows

The first version of this trio (replacement-only runs) relocalized nothing and said so honestly. With additions, the same three locales get sixteen concrete insertions — and the safety guards travel with them: the caste guard on water-carrying roles, the tabletop-only constraint, the arsenic marking, the teacher-figures-only rule. When the log is empty, additions are not a bonus; they are the localization.
