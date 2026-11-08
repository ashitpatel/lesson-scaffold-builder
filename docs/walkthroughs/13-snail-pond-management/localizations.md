# Localizations — ATREE S.N.A.I.L.: pond management

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, and locale notes; per-item review approved every proposal). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) strips the lesson to generic cards. These three runs instead strip and then relocalize to the approved "Three commons" trio: a Kerala backwaters panchayat, an English village parish, and an Arizona ranch town. All three passed, and unlike the [mapping lesson's trio](../12-snail-water-source-mapping/localizations.md), all three replaced real terms — this lesson logs about six locale items per run (attribution, pujas, the district example, bank crops, the sharing network).

## 1. Backwaters panchayat in Kerala, India

Run `runs/snail-pond-kerala-1`: pass, 4 units, 20 calls, 682,618 in / 111,746 out tokens. Locale notes asked for panchayat governance, Malayalam names, monsoon seasons, and a fisher-family perspective alongside conservation.

- Logged 6: DRCSC credit (dropped), pujas → "social or religious uses", South 24 Parganas (dropped), taro and ipomoea → "useful trees and plants" (shared generic), ENRE network → "school sharing network".
- Proposed 3, approved 3, landed 2: "useful trees and plants" → **coconut palms (thengu)** (1 place); "school sharing network" → **panchayat school cluster** (1 place). The ipomoea proposal (bananas/vazha) missed: both crops shared one generic phrase and the taro substitution consumed it first, so the run noted it "not found, left generic" instead of guessing.
- DRCSC, pujas, South 24 Parganas were never proposed: dropped or generalized content is never resurrected.

## 2. English village parish, UK

Run `runs/snail-pond-parish-1`: pass, 4 units, 22 calls, 754,434 in / 137,885 out tokens. Locale notes asked for parish-council oversight, planning-permission rules, wildlife-trust guidance, pounds, and permission slips for trips.

- Logged 6: DRCSC (dropped), South 24 Parganas → "the example well-managed village pond", pujas → "community or religious gatherings", taro and ipomoea → "vegetables" (shared generic), ENRE network → "a school sharing network".
- Proposed 4, approved 4, landed 3: the pond example → **the parish Mill Pond**; "vegetables" → **broad beans**; the network → **the local primary schools cluster**. The ipomoea proposal (cabbages) missed for the same shared-generic reason as Kerala, and was reported the same way.
- DRCSC and pujas were never proposed.

## 3. Ranch town in Arizona, USA

Run `runs/snail-pond-arizona-1`: pass, 3 units, 19 calls, 649,329 in / 106,531 out tokens. (Three units rather than the base run's four — ordinary model variance across runs.) Locale notes asked for stock tanks under prior-appropriation water rights, drought framing, dollars, ranching livelihoods first, and English/Spanish names.

- Logged 6: DRCSC (dropped), rice fields → "surrounding trees and plants", pujas → "social and religious activities", South 24 Parganas → "well-managed village pond example", taro and ipomoea folded into one item → "food and useful plants", ENRE network → "school-sharing network".
- Proposed 4, approved 4, landed 4 — the cleanest of the three, because the log folded both crops into one item, so no shared-generic collision: rice fields → **surrounding mesquite, cottonwoods and range grasses**; the pond example → **well-managed neighboring ranch stock tank example**; the crops → **prickly pear and mesquite**; the network → **county school-sharing network**.
- DRCSC and pujas were never proposed.

## What this trio shows

Two behaviors worth keeping in mind. First, when two log items share one generic phrase, the first approved substitution wins and the second is reported missing (Kerala, Parish) — honest, but a reviewer should check whether the surviving generic still reads sensibly. Second, the model sometimes declines to propose for a live generic (pujas in all three runs): review the skipped items, not just the applied ones, since a missing proposal can mean the locale notes ruled it out or the model simply had no fit.
