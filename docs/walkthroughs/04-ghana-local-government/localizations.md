# Localizations — Ghana: local government and community development

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) generalizes the Ghanaian lesson to generic cards. These three runs instead generalize, then relocalize to Kakuma refugee camp, a Swiss Gemeinde, and Porto Alegre. All three passed (Porto Alegre on a rerun, after the first attempt exhausted its revisions on an invented detail — rerunning a failed locale is ordinary operations, not a pipeline change). Local government is the most institution-dense lesson in the sweep: 23 proposals approved across the trio, the heaviest replacement traffic anywhere — and two of the three sets reverted when long official terms newly broke check D11. The additions carried those runs instead.

## 1. Kakuma refugee camp, Kenya

Run `runs/ghana-kakuma-1`: pass, 4 units, 10 weeks, 22 calls, 752,510 in / 139,295 out tokens, Flesch 68.0. Locale notes removed every civic assumption: no elected assembly, tax base, or citizenship — block leaders plus camp management plus NGOs govern, and the budget is a fixed NGO grant; Somali, South Sudanese and Congolese names; never frame pupils as voters or citizens; the letter goes to the block leader; household visits are a protection risk, so survey by classroom role-play.

Final cards: [final-kakuma.md](./final-kakuma.md).

- Logged 14 items; 9 proposals approved — Block Leader, Camp Manager, Block Committee, block community meeting, communal tap stand, fixed NGO block grant, Kenyan shillings among them — one matched nothing (`Upper Primary`: the grade band is not in the cards), then the set newly broke D11 and everything reverted: "cards stay generic."
- 5 additions proposed, all 5 kept: needs group "by tap queue, latrine path, and dusty play area"; urgency weighs "shade in hot wind season or tap queues"; fairness means "different blocks or language groups sharing one grant"; the letter asks for "their own block, like a tap shelter or shaded study corner"; letters read aloud "in English, Kiswahili, or a home language they write best".

## 2. Swiss Gemeinde (municipality)

Run `runs/ghana-swiss-1`: pass, 3 units, 7 weeks, 24 calls, 817,741 in / 140,063 out tokens, Flesch 61.6. Locale notes asked for direct democracy: municipal council plus citizens' assembly, francs, real published budgets pupils can look up; German and French names; the town hall becomes the actual assembly pupils may attend with parents; referendum and initiative taught alongside the vote.

Final cards: [final-swiss.md](./final-swiss.md).

- Logged 12 items; 5 proposals approved, all 5 applied — the only set in this trio that survived: `district council` → `Gemeinderat / conseil communal (municipal council)`; `elected area representative` → `Gemeinderatsmitglied / conseiller communal (municipal councillor)`; `community committee` → `Gemeindeversammlung / assemblée communale (citizens' assembly)`; `water point` → `village fountain (Brunnen / fontaine)` (2 places); `market shelter` → `covered stall at the weekly market (Marktstand / stand de marché)` (2 places).
- 5 additions proposed, 3 kept, 2 dropped individually on D11 (the francs/budget and referendum wordings — the per-addition drop path, sparing the rest): the meeting becomes "the Gemeindeversammlung / assemblée communale pupils may attend with parents"; the needs list gains "a shelter for the Postauto / CarPostal stop"; the recommendation goes "for the next citizens' assembly".

## 3. Porto Alegre, Brazil

Run `runs/ghana-poa-1`: pass, 3 units, 7 weeks, 18 calls, 607,787 in / 121,490 out tokens, Flesch 65.3. Locale notes set the run in the birthplace of real participatory budgeting: neighborhood assemblies and delegates deciding part of the city budget; Brazilian Portuguese names, reais; the class vote maps to a real assembly cycle with delegates and a report-back; favelas and wealthy districts share the city, so fairness discussion must include unmet needs frankly.

Final cards: [final-poa.md](./final-poa.md).

- Logged 14 items; 9 proposals approved — Câmara Municipal, vereadores, bairro, prefeito, associação de moradores, assembleia do Orçamento Participativo, verba anual, reais, torneira comunitária — one matched nothing (`prefeito`: its generic was not found), then the set newly broke D11 and reverted like Kakuma's.
- 6 additions proposed, 4 kept, 2 dropped individually on D11: the needs list sits "near a praça in Restinga, an arroio margin, or a bus stop"; the school walk looks for "flooded arroio margins, shadeless praça corners, and broken bus stops"; the mock vote runs "as neighborhood delegates do in the city's assembly cycle"; fairness stretches "from vilas populares to wealthy bairros with paved streets".

## What this trio shows

Twenty-three proposals, two reverts, two per-addition drops — this trio exercises every safety path in the locale machinery, and every run still passed with its locale work intact in some form. The pattern is consistent: long official terms (`block leadership with camp management and partner NGOs`, `assembleia do Orçamento Participativo`) overflow steps that shorter ones fit, so the revert protects exactly the runs that need it. And the guard notes held everywhere: no voter framing in Kakuma, real-assembly attendance in Switzerland, frank fairness across the city divide in Porto Alegre.
