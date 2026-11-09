# Localizations — Tanzania: multiplication and division practice

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) generalizes the Tanzanian lesson to generic cards. These three runs instead generalize, then relocalize to a French primary school, a Mongolian steppe pastoralist school, and Seoul. All three passed. The trader story, workbook price, Kariakoo earnings homework, and ward officer return are all dropped when the lesson is generalized, so France — where every generic died with its segment — runs on additions alone; Mongolia and Seoul each keep enough generic fabric to land real replacements.

## 1. French primary school, France

Run `runs/tanzania-france-1`: pass, 3 units, 8 weeks, 16 calls, 527,595 in / 96,879 out tokens, Flesch 62.8. Locale notes asked for the daily calcul mental slate ritual, French names, euros; the timed race stays low-stakes and personal-best; strictly secular framing (laïcité), no religious references in word problems; ranking by progress bands, never named slowest lists.

Final cards: [final-france.md](./final-france.md).

- Logged 6 items, all dropped with their segments (Dar es Salaam story, workbook, shillings, Kariakoo homework, ward officer).
- Proposed 0: "no proposals for the target locale; cards stay generic."
- 6 additions proposed, all 6 kept: slate work runs "during the daily calcul mental ritual"; grouping uses "colour progress bands"; counters come "from the classroom bûchettes box"; problems carry "French first names like Léa and Hugo"; the mixed set includes "small euro amounts"; recall runs "as a low-stakes personal-best race".

## 2. Mongolian steppe pastoralist school

Run `runs/tanzania-mongolia-1`: pass, 4 units, 10 weeks, 31 calls, 1,069,710 in / 242,782 out tokens, Flesch 65.2 — the largest run in the sweep, after extra repair rounds. Locale notes asked for mobile-pastoralist word problems (sheep, goats, milk measures), togrog, Mongolian names; tiered problems for a multi-grade single classroom; Friday events moved earlier for the boarding week; winter cold keeps all practice indoors on slates.

Final cards: [final-mongolia.md](./final-mongolia.md).

- Logged 5 items; 2 proposals approved and applied: `points` → `togrog` in the mock ledger; `market quantities` → `soum market` where herder families trade.
- 5 additions proposed, all 5 kept: slate work happens "inside the warm classroom"; sharing counts run "like sheep, goats, and bowls of milk"; counters become "sheep, goats, and kindling counted indoors"; pairs mix "younger and older pupils across grades"; the weekly count is "counted by Thursday in the boarding week".

## 3. Seoul, South Korea

Run `runs/tanzania-seoul-1`: pass, 3 units, 8 weeks, 20 calls, 665,397 in / 142,791 out tokens, Flesch 56.2 — the lowest readability score in the sweep, still recorded, never gated. Locale notes asked for won, traditional-market versus convenience-mart settings, Korean names; no extra homework (evenings belong to academies); timed races track personal bests only, never announcing the slowest; teacher-given figures, never family earnings.

Final cards: [final-seoul.md](./final-seoul.md).

- Logged 7 items; 1 proposal approved and applied: `fruit` → `tangerines (gyul)` in 4 places across the division problems.
- 3 additions proposed, all 3 kept: grouping contexts name "taekwondo points or napa cabbage (baechu) growth in class"; worksheets run "using only teacher-given figures set at a traditional market or a convenience mart"; practice ends with "all practice stays in class with no extra homework."

## What this trio shows

Arithmetic generalizes cleanly — stories, prices, and homework all drop — so the localizations live in the counting objects and classroom rhythms: bûchettes and calcul mental, sheep counted indoors by Thursday, gyul shared from teacher-given figures. Mongolia's 31-call run also shows the pipeline absorbing genuine difficulty (extra repair rounds) without losing the locale work at the end. Seoul's Flesch 56.2 is the sweep's floor and illustrates the policy: readability is recorded, never a gate, since locale terms legitimately lower scores.
