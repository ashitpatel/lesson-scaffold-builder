# Localizations — Kenya: clean water and health

> **Live output, not a hand-written answer.** Each section below comes from one relocalize run of the pipeline on 8 November 2026 (`python3 -m lsb.run --backend muse` with `--locale`, `locale_mode: relocalize`, locale notes, and `locale_additions: true`; per-item review approved every proposal and addition as proposed). The run folders are gitignored; this file is the durable record.
> **Locale note:** The relocalized terms shown below may be incorrect or incomplete — review them with the rest of this output to make sure the material is culturally and educationally appropriate and complete.

The base walkthrough ([README.md](./README.md)) strips the Kenyan lesson to generic cards. These three runs instead strip and then relocalize to a Mumbai high-rise, a desert village in Rajasthan, and Flint, Michigan. All three passed (Flint on a rerun, after the first attempt stalled on unrepairable late issues — rerunning a failed locale is ordinary operations, not a pipeline change). The cholera lecture, lake-shore walk, kit purchase, and chief follow-up all drop during stripping; what survives is the SODIS sunny spot, which Mumbai and Flint each rename — and the additions do the rest.

## 1. High-rise housing society in Mumbai, India

Run `runs/kenya-mumbai-1`: pass, 3 units, 6 weeks, 16 calls, 530,348 in / 84,542 out tokens, Flesch 66.3. Locale notes asked for piped BMC water with overhead tanks and tanker supply — all experiments tabletop, no wells or lake access — Marathi and Hindi names, monsoon flooding instead of the lake-shore trip, and a housing-society notice board instead of the chief follow-up.

Final cards: [final-mumbai.md](./final-mumbai.md).

- Logged 12 items, the most in the sweep: county, lake, health department, outbreak history, razor blade, chief, baraza, kit price, and curriculum all dropped; the school roof and iron sheet merged into one generic sunny spot.
- Proposed 1, applied 1: `flat sunny spot by the classroom` → `sunny podium corner by the classroom`, the safe ground-level spot a housing-society school can use without climbing.
- 4 additions proposed, all 4 kept: stored water lives "in overhead tanks and buckets"; bottles are "cold-drink bottles kept in flats"; the covered vessel is "a steel matka or drum used in society flats"; the class chart is "worded like a housing-society notice-board note in Marathi and Hindi".

## 2. Desert village in western Rajasthan, India

Run `runs/kenya-rajasthan-1`: pass, 4 units, 8 weeks, 24 calls, 829,125 in / 159,538 out tokens, Flesch 69.3. Locale notes asked for extreme-scarcity framing — a distant baoli stepwell, no lake or river — Hindi names, and the caste-loaded guard: never assign water-carrying roles by pupil background; anonymous class tally instead of any family register.

Final cards: [final-rajasthan.md](./final-rajasthan.md).

- Logged 7 items, all dropped with their segments.
- Proposed 0: "no proposals for the target locale; cards stay generic."
- 6 additions proposed, all 6 kept: the shared vessel is "the shared rope-bucket at the baoli"; the ladle is named "(kalchhi)"; jars become "small matkas"; the filter layer is "a folded cotton gamchha"; boiling runs "over dry khejri twigs"; bottles sit "on the open aangan in full dhoop".

## 3. Flint, Michigan, USA

Run `runs/kenya-flint-1`: pass, 3 units, 7 weeks, 17 calls, 562,243 in / 83,496 out tokens, Flesch 68.6. Locale notes asked for piped-but-distrusted city water after the lead crisis: testing and filters are the lesson's core, not fetching; English and Spanish names, dollars; never imply tap water is safe without testing, and never ask pupils to report their home's water quality publicly.

Final cards: [final-flint.md](./final-flint.md).

- Logged 10 items; 2 proposals approved: `flat sunny spot on school grounds` → `school playground blacktop` applied; the `cafeteria tray` proposal (for the iron sheet) shared the same generic and lost the race — "not found, left generic."
- 3 additions proposed, all 3 kept, and all three enforce the trust guard: storage means "the covered jugs Flint families keep for tested tap water"; clear water "in Flint" needs "testing before trusting city tap water"; boiling kills germs "though Flint water still needs testing for lead".

## What this trio shows

The same SODIS step sunbathes on a podium corner, an aangan, and a playground blacktop. Flint's additions show sensitivity notes doing safety-critical work: every addition restates the testing rule without ever asking a child about their own home's water. And the shared-generic rule appears again (blacktop beats cafeteria tray) — consistent, explainable, and recorded in the run notes each time.
