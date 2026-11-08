# Localizations — ATREE S.N.A.I.L.: water source mapping

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, and locale notes; per-item review approved every proposal). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) strips the lesson to generic cards. These three runs instead strip and then relocalize to the approved "Three waters" trio: a desert village in Rajasthan, a Mumbai high-rise, and a Bangladesh char village. All three passed. All three relocalized nothing — and the logs show why: this lesson carries almost no locale markers (no place names, currencies, or organizations reach the sequence), so there was genuinely nothing to replace. Generic cards with a clear note is the right outcome here, not a failure.

## 1. Desert village in western Rajasthan, India

Run `runs/snail-mapping-rajasthan-1`: pass, 3 units, 17 calls, 568,095 in / 80,112 out tokens. Locale notes asked for stepwell scarcity framing, Hindi names, no water-carrying roles by pupil background, and an anonymous class tally instead of any family register.

Final cards: [final-rajasthan.md](./final-rajasthan.md).

- Logged 1 item: the dropped DRCSC credit line (agency, no generic).
- Proposed 0: nothing replaceable remained, so the run noted "no proposals for the target locale; cards stay generic" and stopped — the empty-proposals path, exercised live.

## 2. High-rise housing society in Mumbai, India

Run `runs/snail-mapping-mumbai-1`: pass, 4 units, 18 calls, 602,701 in / 87,115 out tokens. (Four units rather than the base run's three: the decompose grouped the six sections differently this time — ordinary model variance across runs.) Locale notes asked for piped-water tabletop framing, Marathi/Hindi names, and a society notice board.

Final cards: [final-mumbai.md](./final-mumbai.md).

- Logged 0 items: "nothing locale-specific to relocalize." No proposals step ran.
- Cards stay generic, matching the base walkthrough.

## 3. River-island char village in Bangladesh

Run `runs/snail-mapping-char-1`: pass, 3 units, 14 calls, 460,910 in / 60,941 out tokens. Locale notes asked for arsenic-safe/unsafe well marking, yearly re-mapping after floods, boats, Bangla names, and teacher example figures instead of real family data.

Final cards: [final-char.md](./final-char.md).

- Logged 1 item: the dropped DRCSC credit line, as in Rajasthan.
- Proposed 0: "no proposals for the target locale; cards stay generic."

## What this trio shows

Relocalization is only as rich as the log: with zero replaceable items, all three runs correctly did nothing while recording why. The Rajasthan and Char runs both demonstrate the fixed empty-proposals path (no crash, clear note, generic cards). A lesson with real locale content relocalizes for real — see the [pond walkthrough's localizations](../13-snail-pond-management/localizations.md).
