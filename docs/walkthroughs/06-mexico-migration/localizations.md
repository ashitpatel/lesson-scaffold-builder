# Localizations — Mexico: migration stories, past and present

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) generalizes the Mexican lesson to generic cards. These three runs instead generalize, then relocalize to Amritsar (Partition histories), a Berlin classroom with refugee-background students, and Ireland. All three passed. Migration is the most place-dense lesson in the sweep, so replacements bite harder here than anywhere else: Amritsar lands three, Ireland five, while Berlin approves seven and then reverts them all. The sensitivity notes — trauma-informed teaching, Partition told with care, diaspora pride — shape every run's additions.

## 1. Amritsar, India (Partition histories)

Run `runs/mexico-amritsar-1`: pass, 3 units, 8 weeks, 16 calls, 528,245 in / 86,729 out tokens, Flesch 65.4. Locale notes asked for Partition 1947 as the core case, Hindi and Punjabi names, rupees — and a care guard: Hindu, Muslim and Sikh experiences each heard with respect; never press pupils for family trauma in class; use archives and testimony collections rather than personal disclosure.

Final cards: [final-amritsar.md](./final-amritsar.md).

- Logged 14 items: the border crossing, papers, bus terminal, pesos, and stationery shop all dropped with their segments; three generics survived into the overview.
- Proposed 3, applied 3: `early settlement movements` → `Harappan settlements in Punjab`; `movements to cities` → `Amritsar and Delhi`; `northern areas` → `towns of northern Indian Punjab`.
- 4 additions proposed, all 4 kept: the song verse becomes "a Punjabi folk boli already in the textbook"; the timeline includes "1947 Partition movements"; the final choice offers "the 1947 Partition as one respectful option among others"; changed home places read "such as a village home or mohalla".

## 2. Berlin classroom with refugee-background students, Germany

Run `runs/mexico-berlin-1`: pass, 3 units, 8 weeks, 16 calls, 529,544 in / 90,744 out tokens, Flesch 68.8. Locale notes demanded trauma-informed teaching throughout, non-negotiable: never ask about legal status, journeys, or papers; teach push and pull through historical cases only (Huguenots, guest workers); no family photos on maps, no solo trips to transit hubs; Arabic, Turkish and German names; timelines from provided sources, never family data.

Final cards: [final-berlin.md](./final-berlin.md).

- Logged 14 items; 7 proposals approved — the most in the sweep — mapping the generics onto Brandenburg, France, Salzburg, the Ruhr cities, Anatolia, the Ruhr region, and Berlin. Two proposals (`France`, `Salzburg`) found their shared generic already consumed and were left generic; then the set newly broke D11 and everything reverted: "replacements newly broke ['D11']; cards stay generic."
- 4 additions proposed, all 4 kept, and they enforce the trauma guard directly: cases are named "such as Huguenots in Berlin and guest workers in West Germany"; the song runs "with Arabic, Turkish, and German verses provided"; the timeline and the final choice both stay on "Huguenot settlement and guest-worker recruitment" — historical cases, never personal journeys.

## 3. Ireland

Run `runs/mexico-ireland-1`: pass, 3 units, 8 weeks, 16 calls, 529,078 in / 91,573 out tokens, Flesch 66.0. Locale notes asked for emigration as national story — Famine, coffin ships, the American wake, remittances — Euros, Irish names; family interviews safe and encouraged (diaspora pride, no papers issue); present-day immigration handled carefully with neutral sources.

Final cards: [final-ireland.md](./final-ireland.md).

- Logged 9 items; 6 proposals approved, 5 applied: `the continent` → `Europe`; `other continents` → `North America`; `the capital city` → `Dublin` (2 places); `a southern rural region` → `County Kerry`; `the northern region` → `Belfast`. The sixth (`Australia`) found its generic already consumed by `North America` and stayed generic.
- 4 additions proposed, all 4 kept: vocabulary includes "the Famine and coffin ships among them"; the migrant letter mentions "remittances sent home to family"; the song is "like an emigration ballad sung at an American wake"; changed home places read "such as empty cottages or quiet villages".

## What this trio shows

Place-dense sources produce replacement-rich runs — 16 proposals approved across the trio — and the pipeline's ordering rules show their value: shared generics go to the first proposal that claims them (North America beats Australia; Brandenburg beats France and Salzburg), over-long sets revert instead of shipping broken steps, and the additions hold the line on meaning either way. The contrast between Berlin's guardrails (nothing personal, historical cases only) and Ireland's (family interviews encouraged) is exactly the kind of radically different localization requirement the per-run locale notes exist to express. Readability held at Flesch 65–69.
