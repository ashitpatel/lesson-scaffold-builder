# Changelog

Each release on GitHub attaches the ready-to-use files from `dist/`. The version lives in [`VERSION`](VERSION). The pipeline is also installable: `pip install git+https://github.com/ashitpatel/lesson-scaffold-builder.git`.

## Unreleased

- **Source-flag severity taxonomy.** Critic flags now carry severity (`blocker`/`major`/`minor`), category and handling notes; `summary.json` counts them and blockers stand out in CLI output. Flags still never fail a run: the adapter decides use.
- **`--max-model-steps` for the muse backend.** Raises the per-call model-step budget when calls fail for needing more steps (default 1, unchanged); the failure message now names the flag.

## 0.4.0 — 2026-11-19

- [x] A. Stuck-group note: **keep** the one-exception policy. Teachers new to group work need a first move when a group stalls; the note ends in help (EB-03-consistent); the exception is disclosed in the disclaimer.
- [x] B. Stuck-note wording: **keep** the three lines unchanged. Short, plain, printable; dropping "before giving any hints" was the right cut.
- [x] C. Untranslated note on non-English cards: **keep English-fixed for now**, translate in a follow-up. Renderer string-table plumbing is real work; the limitation is already disclosed in the blog.
- [x] D. EF routines: **strengthen** into required-when-fitting edits, then re-sweep to verify. The fractions sweep showed optional bullets get skipped; the routines are sound, the failure is prompt strength.
- [x] E. Already-present widening: **keep widened**. Routine-less units with base practice stay eligible targets; with D, this is how the routines reach most units.
- [x] R. Standing rule: **adopted** for this session. Bug fixes and factual corrections proceed silently; teacher-facing content, project claims, or pipeline-behavior changes get a one-question checkpoint first.

Follow-up to C (implemented):
- **Translated stuck note.** The translate stage now carries the fixed "If a group is stuck" note's heading and lines into the run's language; which units get the note is decided on the reviewed English, since translated steps no longer match the group-work pattern. Runs translated before this change re-render with the English note via `english-final.json`.
- **Translated-page language tag.** `cards.html` now declares the run's output language (`<html lang>`, BCP47 with an `en` fallback for unknown languages); the G21 self-check verifies the tag.
- **Stanford methods.** Opt-in method families (peer tutoring, talk uptake, civic mapping, UDL choice) as named routines gated on a tech/time inventory, plus a fourth optimisation stage with two tech-conditional cards (ST-01 ROAR screening, ST-02 AI literacy) applied only with opt-in plus a passing inventory; applied tech steps carry a `(needs: …)` marker and plan B. Recording children stays vetoed. Deck grows to twenty-one cards. See docs/methodologies.md.
- **EF+Math routines on EB cards.** One-sentence plan gates on EB-03/EB-08 multi-step problems and thumbs-signal confidence checks on EB-01/EB-04, applied as required-unless-capped edits and labeled project adaptations with inspected sources.
- **Stuck-group note.** Unit cards with group work print a fixed "If a group is stuck" note (two questions, then show the next step); the onboarding disclaimer names it as the one exception to no prescribed routines. Final environment assumptions are saved so re-rendered cards match.
- **Non-English intake.** Source lessons in another language are translated to English first, with the original kept alongside for checking.
- **Docs.** Tagline on front doors, ELEVATE export note, exploratory field-evaluation protocol with adopter outreach template, eighth blog post, annotated teacher/method card examples, per-unit method-limit correction.

## 0.3.0 — 2026-11-09

- **Locale support.** An outset choice — generalize, keep, or relocalize locale-specific content — with a removal log, target proposals, overall locale notes, and per-item approve/skip/own-text review (revertible as a set when replacements newly break a code check). Locale additions propose anchored insertions with per-item review and per-addition trial application; final-content translation renders the cards in the run's language (English original kept), with per-language word-cap multipliers (`--language`, `--locale`).
- **Multi-turn refine.** A new `lsb-refine` entry point revises steps over days or weeks, storing each turn in `revisions/revN/` with structure, code-check, and critic review scoped to the edit (harm checks stay global); replies come back in the run's language.
- **More evidence-based practices.** EB-06 to EB-09 — TaRL-inspired level grouping plus interleaving, self-explanation, and elaboration from Dunlosky — bring the deck to nineteen cards, with verified citations; a plain-language evidence guide covers EB-01 to EB-05.
- **Check updates.** D11 step cap 80 → 100 words; G02 flags two separable teacher actions even under the cap; readability (Flesch) is recorded in `summary.json`, never gated; a dependencies repair may add the G15 Recall opener to the unit's first step.
- **Thirteen walkthroughs.** New Tanzania, Philippines, and two ATREE S.N.A.I.L. water lessons, each with decision trace and final cards; every walkthrough carries per-locale final cards, and the regression suite extends to 13 cases.
- **Docs.** A seventh blog post on tweak-it-later revision, locale-choice coverage across the series, decision-points documentation, and the Zenodo concept DOI wired into `CITATION.cff` and the README badge.

## 0.2.0 — 2026-11-08

- **"Lesson" everywhere.** The input is now consistently called a lesson, not a chapter, across the README, docs, prompts, browser-assistant kickoff and blog posts (including two renamed post URLs). Test fixtures, walkthrough records and validated model prompts keep the original term.
- **Better evidence coverage.** Each evidence-based practice now cites its own reviews: Rowland (2014) and Karpicke & Roediger (2008) for retrieval, Cepeda et al. (2006) for spacing, Atkinson et al. (2000) for worked examples, and Kingston & Nash (2011) — with its modest 0.20 mean effect as an honest caution — for checking understanding. All references carry DOI/ERIC/IES links.
- **Shikshagraha acknowledgment.** The README, first blog post and about page credit Shikshagraha's Micro-Improvement Plan as the inspiration for the Micro-Lesson Scaffold.
- **Discoverability.** Repository topics, homepage and description; a generated `CITATION.cff` (GitHub's "Cite this repository" button); a social preview image.

## 0.1.0 — 2026-11-07

First release. A pipeline that turns a long, lecture-heavy teaching chapter into at most four 2-to-4-week Micro-Lesson Scaffolds (or one spanning the chapter), printed as offline teacher cards.

- **Stages:** decompose → 11 deterministic checks (D01–D11) → a 21-check reviewer (G01–G21) with revise/reject → three optimisation stages (evidence-based practices, Connected Learning, participatory budgeting), each per unit and each allowed to abstain → repair of flagged steps → rendered cards with a G21 clarity check.
- **Backends:** Claude Code login (default, no key), Muse login (`--backend muse`), Gemini on a free AI Studio key (`--backend gemini`), or the Anthropic API (`--backend api`). Per-call input/output tokens are reported; every reply and intermediate JSON is saved.
- **Choices:** `--ask` asks which method families to exclude, whether to build one scaffold or several (with breakdown focus and max weeks), and each stage's limits; `--answers FILE` supplies them for sweeps.
- **Checks and guardrails:** no child data or ranked scores, no unsupervised trips or hazardous work, no real money through learners' hands, offline paper-or-chalk steps with conditions and fallbacks, region-neutral output, no invented tactics or outcome claims.
- **Nine walkthroughs** on original test chapters set in different countries, each with the source, a decision trace and the final cards.
- **Browser assistants:** a condensed first-message prompt (`dist/kickoff.md`, under 4,000 characters) with one-click links for ChatGPT, Claude and Google AI Mode, generated by `scripts/build.py`.
