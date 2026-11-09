# Localizations — Philippines: how plants grow

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) strips the Philippine lesson to generic cards. These three runs instead strip and then relocalize to the Westland greenhouse belt, a Singapore HDB school, and a Zaatari camp school. All three passed. The source's two locale markers are a ruler price (always dropped) and the Laguna de Bay shore trip (moved to supervised school grounds); the Netherlands and Singapore runs each land one replacement renaming those grounds, while Zaatari's generic water body draws no proposal — and the additions stock each garden with tomaat, kangkong, and zaatar.

## 1. Westland greenhouse belt, Netherlands

Run `runs/philippines-netherlands-1`: pass, 3 units, 8 weeks, 16 calls, 527,794 in / 93,391 out tokens, Flesch 70.7. Locale notes asked for greenhouse-horticulture framing: seedlings in school-garden plots or classroom propagators, Dutch names, euros; the riverbank trip becomes a supervised ditch-side walk with water-safety rules and hi-vis; cupboard experiments become light-versus-dark propagator trays.

Final cards: [final-netherlands.md](./final-netherlands.md).

- Logged 2 items: `45 pesos` dropped with the ruler purchase; `Laguna de Bay shore` → generic `school grounds`.
- Proposed 1, applied 1: → `schooltuin` (2 places), the school garden plot where pupils grow seedlings in the greenhouse belt.
- 3 additions proposed, all 3 kept: seedlings are "tomaat, as raised in nearby Westland kassen"; sorting uses "tomaat and komkommer seeds from the schooltuin"; the stem demo takes "a white chrysant grown in nearby kassen".

## 2. Singapore HDB school

Run `runs/philippines-singapore-1`: pass, 3 units, 7 weeks, 19 calls, 632,680 in / 111,208 out tokens, Flesch 71.7. Locale notes asked for land-scarce tropical growing: HDB corridor pots and hydroponics kits, dollars, English/Malay/Mandarin/Tamil names; strict park rules mean school grounds only, no seed collecting in nature areas; water and space limits are part of the lesson.

Final cards: [final-singapore.md](./final-singapore.md).

- Logged 2 items: `pesos` dropped; `Laguna de Bay shore` → generic `the school grounds`.
- Proposed 1, applied 1: → `the HDB school grounds` (2 places), keeping all collecting inside school grounds per the permit rules.
- 5 additions proposed, all 5 kept: minerals come "as in the small amount of potting mix in corridor pots"; leaves catch light "like kangkong and bayam grown in corridor pots"; the light comparison runs "in a small HDB corridor pot"; the stem demo takes "a white orchid"; roots grow "in shallow corridor pots where space is tight".

## 3. Zaatari camp school, Jordan

Run `runs/philippines-zaatari-1`: pass, 3 units, 7 weeks, 16 calls, 526,761 in / 100,985 out tokens, Flesch 75.8. Locale notes asked for container gardening with rationed water (measured cupfuls, counted drop by drop), Arabic names; all growing at school, no home experiments, teacher's phone only for photos with no faces; plants framed as food security; no ranked growers chart, ever.

Final cards: [final-zaatari.md](./final-zaatari.md).

- Logged 2 items: `Laguna de Bay` → generic `a nearby water body`; `pesos` dropped.
- Proposed 0: "no proposals for the target locale; cards stay generic."
- 5 additions proposed, all 5 kept: the four needs are "called daw', maa', hawaa', and ma'aadin in Arabic"; cups are "watered here by small measured cupfuls, drop by drop"; results matter "for the food our school garden can provide"; leaves are "like mint, sage, and zaatar in school containers"; sorting uses "lentils, chickpeas, and fava beans".

## What this trio shows

The same shore trip becomes a schooltuin, HDB grounds, and a generic water edge; the same seedling becomes tomaat, kangkong, and zaatar. Zaatari's additions show the phase at its most purposeful: rationed-water practice, food-security framing, and camp-kitchen seeds, all honoring constraints (no home experiments, no ranked charts) that a generic lesson could never know about. Readability runs high here (Flesch 71–76), fitting a primary science lesson.
