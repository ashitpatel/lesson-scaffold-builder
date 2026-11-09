# Localizations — Civics: making decisions together

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) strips the civics lesson to generic cards. These three runs instead strip and then relocalize to a Chinese city residents' committee, a Kerala panchayat, and a US council-manager city. All three passed. The lesson's single running example — the Gram Panchayat — survives stripping as a generic council in every run, so each trio member lands exactly one replacement naming its own local body; the additions then tune the harder question of what pupil decision-making means under three different civic systems.

## 1. Chinese city residents' committee

Run `runs/civics-china-1`: pass, 4 units, 8 weeks, 25 calls, 874,280 in / 161,030 out tokens, Flesch 65.1. Locale notes framed the class vote as consultation, never decision: explicitly a simulation that never implies pupils bind real budgets; Yuan, Mandarin names; fundraising needs prior written school approval; pupil work displayed inside school only; fairness as who was heard.

Final cards: [final-china.md](./final-china.md).

- Logged 1 item: `Gram Panchayat` → generic `elected local council`.
- Proposed 1, applied 1: → `the Residents' Committee`, the neighborhood body that consults residents rather than binding budgets.
- 5 additions proposed, all 5 kept: the courtyard wishlist names "wutong shade, stone stools, and a hallway bulletin board"; charts stay "for display inside the classroom only"; rotating roles mirror "classroom duty teams"; the vote runs "in a classroom simulation that decides nothing real"; the close count is "framed as who was heard, not only who won".

## 2. Kerala panchayat, India

Run `runs/civics-kerala-1`: pass, 3 units, 7 weeks, 17 calls, 574,471 in / 117,106 out tokens, Flesch 62.5. Locale notes asked for decentralized panchayat democracy: gram sabha open meetings, Kudumbashree women's self-help groups, Malayalam names, rupees; the class decision maps to a gram sabha cycle (needs raised openly, projects chosen with reasons, results reported back), with the quietest voices included by design.

Final cards: [final-kerala.md](./final-kerala.md).

- Logged 1 item: `Gram Panchayat` → generic `the elected council`.
- Proposed 1, applied 1: → `Grama Panchayat`, Kerala's own spelling and institution.
- 3 additions proposed, all 3 kept: the class totals mirror how "a gram sabha likewise reports back its choice with reasons"; approval voting runs "as in a gram sabha open meeting where all may accept any option"; role-swapping "lets quieter members be heard, as Kudumbashree groups aim to do".

## 3. US city with council-manager government

Run `runs/civics-usa-1`: pass, 3 units, 7 weeks, 19 calls, 650,976 in / 125,706 out tokens, Flesch 64.3. Locale notes asked for a council-manager system with open meetings pupils may attend, dollars; no cash box in the classroom (fundraising through the school activity fund with receipts); no names plus photos on social media (first names only, no faces, opt-in); the uniform-rule vote stays a live issue.

Final cards: [final-usa.md](./final-usa.md).

- Logged 1 item: `Gram Panchayat` → generic `Community_Governance_Body`.
- Proposed 1, applied 1: → `City Council`, the elected body whose open meetings pupils may attend.
- 4 additions proposed, all 4 kept: meetings hold "open meetings where residents raise needs, which pupils may observe"; role cards include "the city manager who carries out council policy"; the wishlist means "a bottle-filling station, bike racks, or shaded pick-up benches"; the fairness debate ties to "the live uniform-rule question".

## What this trio shows

One logged item, one applied replacement, three different democracies: the Residents' Committee that consults, the Grama Panchayat that cycles through gram sabha, the City Council with its manager. The replacements rename the institution; the additions renegotiate what voting means — simulation versus live issue, who is heard versus who won, duty teams versus open meetings. Same decision-making spine, three civic theories of the classroom.
