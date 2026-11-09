# Localizations — Hydrology: tracking rainfall

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) generalizes the hydrology lesson to generic cards. These three runs instead generalize, then relocalize to the Atacama Desert, Mawsynram, and Venice. All three passed. A rainfall-tracking lesson carries no place names, currencies, or organizations into the sequence, so all three runs logged zero items — "nothing locale-specific to relocalize" — and the proposals step never ran. This trio exists to show what the additions phase does in exactly that case: without it, all three locales would get identical generic cards; with it, the same measurement spine teaches fog drip, monsoon overflow, and flood tides.

## 1. Atacama Desert, Chile

Run `runs/hydro-atacama-1`: pass, 2 units, 4 weeks, 12 calls, 384,970 in / 56,954 out tokens, Flesch 59.6. Locale notes pivoted the unit to near-zero rain: fog collection with mesh nets, dew measurement, water-truck arithmetic; the matrix records fog-water millilitres, not rain; Spanish names; container approval through the local water committee.

Final cards: [final-atacama.md](./final-atacama.md).

- Logged 0 items; no proposals step.
- 5 additions proposed, all 5 kept: catching rain gains "camanchaca fog drip from atrapanieblas nets nearby"; the approval body becomes "the local comité de agua"; the matrix records "fog-water in mililitros"; readings measure "dew and fog drip in mililitros"; averages are "counted in mililitros, like a camión aljibe tally".

## 2. Mawsynram, Meghalaya, India

Run `runs/hydro-mawsynram-1`: pass, 2 units, 4 weeks, 14 calls, 450,666 in / 69,489 out tokens, Flesch 62.4. Locale notes framed the wettest place on Earth: rain overflows normal gauges, so readings are large-capacity and twice-daily in monsoon, with roof-catchment maths; Khasi names; approval through the village council; runoff as the local hook.

Final cards: [final-mawsynram.md](./final-mawsynram.md).

- Logged 0 items; no proposals step.
- 4 additions proposed, all 4 kept: approval runs "through the Dorbar Shnong, as is customary in Khasi villages"; gauges become "large jars that will not overflow in heavy Mawsynram rain"; the table notes "both morning and evening readings in monsoon"; the baseline links "to roof-catchment runoff seen in the Khasi hills".

## 3. Venice, Italy

Run `runs/hydro-venice-1`: pass, 2 units, 4 weeks, 14 calls, 454,978 in / 65,219 out tokens, Flesch 61.6. Locale notes reframed the unit as flood tracking: tide charts, acqua alta sirens, raised walkways; pupils record tide-board readings and flood marks; the placed containers become classroom tide models; Italian names, euros; respect for the disruption flooding causes residents.

Final cards: [final-venice.md](./final-venice.md).

- Logged 0 items; no proposals step.
- 5 additions proposed, all 5 kept: depth marks read "like the tide boards seen along Venetian canals"; sectors stay "clear like raised walkways during acqua alta"; each bottle becomes "a small classroom tide model"; readings run "as with tide-board readings taken during acqua alta"; the matrix mirrors "the tide charts posted around Venice".

## What this trio shows

Three runs, zero logged items, fourteen landed additions: when the log is empty, replacements correctly stand down and additions do all the localization work. The same two units teach camanchaca nets, monsoon jars, and tide models depending on nothing but the target locale and its notes. These are also the cheapest runs in the sweep (12–14 calls) — the proposals call is skipped entirely on the empty-log path.
