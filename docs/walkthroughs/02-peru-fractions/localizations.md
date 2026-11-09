# Localizations — Peru: fractions in the market and the garden

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) generalizes the Peruvian lesson to generic cards. These three runs instead generalize, then relocalize to a rural Malawian village, the Marrakech medina, and urban Tokyo. All three passed. Malawi shows a replacement landing; Marrakech shows approved replacements being reverted as a set when they newly break a check, with additions still landing; Tokyo shows the empty-proposals path with additions carrying all the locale color.

## 1. Rural village in Malawi

Run `runs/peru-malawi-1`: pass, 3 units, 6 weeks, 18 calls, 608,013 in / 119,996 out tokens, Flesch 64.7. Locale notes asked for Kwacha, a weekly market day, real family maize ridges (not metre grids), Chichewa names, slates instead of printed worksheets, fractions through shared harvest portions, and the teacher's example figures — never real family harvest data.

Final cards: [final-malawi.md](./final-malawi.md).

- Logged 7 items: MINEDU, UGEL Cusco, Inca, quipus, San Pedro market, and S/ 5 were all dropped with the history lecture and market trip, so none was replaceable; only `quinoa` → generic `dry beans` survived into the sequence.
- Proposed 1, applied 1: `dry beans` → `dry maize kernels (chimanga)`, approved as proposed — the market quantities in MLS-FRAC-02 step 3 are now counted in maize kernels.
- 5 additions proposed, all 5 kept: folding strips work "as for sharing nsima portions equally"; comparing goes "like shared harvest portions on weekly market day"; the garden bed is "called munda in Chichewa"; and two additions pin the ridges and shares down as the teacher's example figures.

## 2. Medina in Marrakech, Morocco

Run `runs/peru-marrakech-1`: pass, 3 units, 6 weeks, 23 calls, 786,720 in / 140,042 out tokens, Flesch 69.6. Locale notes asked for Dirhams, souk haggling rather than fixed prices, fractions through bread portions and market weights, Arabic and French names, and a sensitivity guard: bargaining stays respectful play, never mockery of vendors, and no real money leaves the classroom.

Final cards: [final-marrakech.md](./final-marrakech.md).

- Logged 10 items; 2 proposals, both approved as proposed (`root vegetable` → `turnip (lift / navet)`; `beans` → `fava beans (foul / fèves)`) — then the whole set was reverted because the replacements newly broke check D11. The cards keep the generic terms, and the run notes say so: "replacements newly broke ['D11']; cards stay generic." The revert path working as designed, live.
- 4 additions proposed, all 4 kept: strips fold "as a baker cuts round khobz (pain rond) for sharing"; equivalent parts are "like quartered zellige squares seen around the medina"; comparing runs "as with a third of khobz against a fifth".

## 3. Urban Tokyo, Japan

Run `runs/peru-tokyo-1`: pass, 3 units, 6 weeks, 22 calls, 746,665 in / 140,798 out tokens, Flesch 70.5. Locale notes asked for Yen, rooftop planters in trays instead of a school garden, supermarket flyer prices instead of a market trip, fractions through school-lunch portions, Japanese names, and privacy guards: never ask about family earnings, keep any ranking effort-based.

Final cards: [final-tokyo.md](./final-tokyo.md).

- Logged 8 items, all dropped with the lecture and market trip (MINEDU, UGEL, Cusco, Inca, quipus, San Pedro market, S/ 5, quinoa).
- Proposed 0: "no proposals for the target locale; cards stay generic" — the empty-proposals path.
- 4 additions proposed, all 4 kept: folding uses "origami paper familiar from craft time"; thirds and sixths compare "like a roasted nori sheet for onigiri"; comparing runs "as with two kyushoku school-lunch portions"; the share grid is "drawn from the rooftop planters in trays".

## What this trio shows

Replacements land only where a generic term survives into the sequence — one word in Malawi, none in Tokyo — and Marrakech proves the safety net: approved replacements that break a check are rolled back rather than shipped. In all three runs the additions did the heavy lifting, grounding every unit in market-day shares, khobz, zellige, nsima, munda, nori, and rooftop trays. Readability stayed in the plain-language band (Flesch 65–71) throughout.
