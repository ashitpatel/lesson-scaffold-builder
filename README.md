# Lesson Scaffold Builder (LSB)

**A pipeline that turns long, lecture-heavy teaching material (a textbook chapter, a syllabus section, a teacher's guide) into a small set of 2-to-4-week Micro-Lesson Scaffolds, printed as offline teacher cards. Along the way it removes what is unsafe, costly or region-specific, and adds evidence-based practices, Connected Learning and participatory budgeting only where they genuinely fit.**

> **Status (November 2026): working prototype, run live.** The whole pipeline runs from the command line: decompose → code checks → a 21-check reviewer → three optimisation stages → teacher cards. It has been run on nine original test chapters set in different countries (see [live results](#live-results)). **No teacher or curriculum specialist has reviewed its output yet**, and nothing here shows that the cards improve learning. The evidence-based practice list is a project choice that needs review by the people who own the content.

---

## Goal

Teachers and the people who support them are handed curriculum documents that are long, lecture-heavy and written for an ideal classroom. Curricula that move faster than students can learn are one reason learning stalls in many systems [R1], and the World Bank and partners estimate that around 70% of 10-year-olds in low- and middle-income countries can't read and understand a simple text [R2]. Turning a chapter into something a teacher can run next week, with the materials they have, is slow work usually done by hand.

LSB asks one question: **can an AI pipeline turn a long chapter into a short, safe, runnable sequence of classroom steps, without losing what the chapter was for?**

It does that by:
1. **decomposing** the source into at most four units of 3 to 7 steps each, linked as a dependency graph, every step traced to the section it came from;
2. **checking** everything countable in code (unit and step limits, step size, weeks, roles, links, cycles, region-specific names and currencies) and everything else with an independent reviewer applying 21 checks, including privacy, safety, money, offline use, invented tactics and whether deep work survived;
3. **optimising** unit by unit with three sets of methods, each allowed to abstain: **evidence-based practices**, **Connected Learning** and **participatory budgeting**;
4. **never making things worse:** an optimisation that can't pass review is undone, and a problem any later review finds must be repaired before cards are printed;
5. **delivering** teacher cards (plain text and a printable black-and-white page) plus a list of what in the source was unsafe or unusable.

It generalises the [Shikshagraha MIP Transformer](https://github.com/ashitpatel/shikshagraha-mip-transformer), which revises single Micro-Improvement Projects for Indian public schools, to any K-12 material in any system, with region-neutral output.

### What the source usually asks for that a card must not
Every one of the nine test chapters contains things a real chapter might: trips without an adult, learners pouring boiling water, a "slow readers" wall chart, scores posted by name, family migration status, children's videos in a parents' group, students collecting money, purchases, devices, and region-specific bodies and currencies. Two include a line addressed to automated systems. The pipeline must remove all of them, say what it removed, and still deliver the chapter's goal.

---

## How it works

```
source chapter ──► decompose ──► code checks ──► reviewer (21 checks) ──► PASS ──► Evidence-Based ──► Connected Learning ──► Participatory Budgeting ──► teacher cards
                      ▲                               │                             (each: per unit, may abstain, edit checked in code,                (code-checked:
                      └──── REVISE (≤2), REJECT (1) ──┘                              reviewed again, reverted if it can't pass)                         G21 clarity)
```

| Stage | What it does | Decided by |
|---|---|---|
| [Decompose](prompts/05-decompose.md) | Macro objective, ≤4 units, 3–7 one-action steps, 2–4 weeks, dependencies, source trace, what each unit assumes and its fallback, what was set aside | Model |
| [Validate](lsb/validate.py) | 11 deterministic checks (D01–D11) | Code |
| [Critic](prompts/50-critic.md) | 21 checks (G01–G21); code results are final; source problems become *source flags* | Model |
| [Evidence-Based](prompts/25-evidence-based.md) · [Connected Learning](prompts/30-connected-learning.md) · [Participatory Budgeting](prompts/31-participatory-budgeting.md) | One unit at a time: credit what's already there, apply ≤2 cards and ≤1 added step, or abstain | Model; edit limits checked in [code](lsb/optimise.py) |
| Repair | Problems a stage's review finds in steps no stage changed go back to decompose, fixed in place; if they can't be fixed, the run doesn't pass | Model; limits checked in [code](lsb/optimise.py) |
| [Render](lsb/render.py) | Overview card + one card per unit; G21 checked on the output | Code |
| [Regression](lsb/regress.py) | Runs every test chapter and checks properties of the result | Code |

---

## Getting started

### 1. See what it produces (2 minutes, no setup)
Open a walkthrough from [docs/README.md](docs/README.md). Each one starts from a test chapter set in a different country, shows what the pipeline removed and why, what each stage did, and the teacher card it printed.

### 2. Run it on a chapter (Python 3.10+)
```bash
python3 -m pip install jsonschema anthropic
```
```bash
python3 -m lsb.run my-chapter.md --ref "Unit 3 - Fractions" --grade-band Middle --dry-run
```
```bash
python3 -m lsb.run my-chapter.md --ref "Unit 3 - Fractions" --grade-band Middle
```
A live run uses `claude-opus-5-5` through your **Claude Code login** (no API key needed), `muse-spark` through your **Muse login** with `--backend muse`, or the Anthropic API with `--backend api`. Everything is saved under `runs/<timestamp>/`: open `cards.html` for the teacher cards and `summary.json` for the source flags and what each stage did. Add `--ask` to be asked about the breakdown (unit maximum, focus) and each stage's limits (cards, cards per unit, added step), with suggestions drawn from your source; `--answers FILE` supplies those answers from JSON so sweeps don't stop.

### 3. Develop or test it
```bash
python3 -m unittest discover -s tests
```
```bash
python3 -m lsb.regress
```
The tests are offline (a scripted fake model drives the whole pipeline). The regression sweep runs all nine test chapters live and checks each against its expectations. See [docs/technical.md](docs/technical.md) for every check, flag, output file and exit code.

---

## The frameworks

> **How they rank.** Of the three, only the **evidence-based practices** have broad, replicated evidence about learning. **Connected Learning** and **participatory budgeting** have no causal evidence of improving test scores; they're used as engagement and civic-reasoning designs, and the pipeline is forbidden from claiming otherwise. All three must abstain when they don't fit.

### 1. Evidence-based practices (run first)

**What they are.** Five practices with broad, replicated support across well-known research syntheses, chosen because each works offline with paper or chalk and fits inside an existing classroom step. Each is applied **only with all its non-negotiables**; a hollow version ("a quiz" that is graded) is worse than none. Full cards: [frameworks/evidence-based-practices.md](frameworks/evidence-based-practices.md).

| Practice | What it adds to a unit | Non-negotiables | Basis |
|---|---|---|---|
| **EB-01 Retrieval practice** | A few questions answered from memory at the start of a later lesson | Notes away; answers shown straight after; nothing marked or recorded | Rated high utility [E1]; an IES practice-guide recommendation [E2] |
| **EB-02 Spaced practice** | A short review of earlier content in a later week | At least a week after first teaching; students do something with it | Rated high utility [E1]; IES recommendation [E2] |
| **EB-03 Worked examples, then practice** | A complete example, then one students finish, before solving alone | A full example first; students then solve similar problems | IES recommendation [E2]; Rosenshine's principles [E3] |
| **EB-04 Checking for understanding** | A question every student answers at once, on slates or with fingers, before moving on | Every student answers; the educator looks; what happens next depends on it | Rosenshine's principles [E3]; formative-assessment review [E4] |
| **EB-05 Concrete and visual representations** | A drawing or model linked explicitly to the abstract idea | Shown with the words or symbols; the link is stated | IES recommendations [E2] |

**What the evidence does and doesn't say.** These syntheses mostly draw on laboratory and classroom studies in high-income countries. They support the practices as generally effective ways to learn and remember; **they don't predict an effect size for a given chapter, school or system**, and no step on a card may claim one.

### 2. Connected Learning (Mizuko Ito and the Connected Learning Research Network)

**What it is.** Learning that is interest-driven, supported by relationships, and connected to opportunity [C1, C2]. The requirements turn it into five rules, which LSB writes as cards with limits and guardrails: [frameworks/connected-learning.md](frameworks/connected-learning.md).

| Card | What it adds to a unit |
|---|---|
| CL-01 Interest integration | A choice of theme or format for the same practice; the learning target is unchanged |
| CL-02 Structural peer roles | Rotating roles (Counter, Recorder, Checker) instead of one student or the teacher recording alone |
| CL-03 Real-world context | Everyday numbers students can observe, never household or family details |
| CL-04 Collective shared purpose | A whole-class product (a class table, a class book) alongside individual work, with no ranking |
| CL-05 Real audience | Finished work shown to someone other than the teacher, at school, and only by the student's choice |

**What the evidence shows.** Mainly ethnographic and design-based research, mostly from the US and UK and often outside school [C1, C2]. It describes how engagement happens; **it doesn't establish effects on test scores.** No card claims one.

### 3. Participatory budgeting

**What it is.** A group deciding directly how to use a shared resource: ideas → vetting → ballot → report-back. Stanford's Crowdsourced Democracy Team contributed knapsack voting, where each voter picks options whose costs fit the budget [B1]; the Method of Equal Shares gives proportional outcomes [B2]. The requirements allow PB cards **only where there is a real resource trade-off** for the class to decide, never in decoding drills or the educator's own administration. Cards: [frameworks/participatory-budgeting.md](frameworks/participatory-budgeting.md).

| Card | When it fits |
|---|---|
| PB-01 Knapsack ledger | Percentages, arithmetic or data practice that can use a made-up budget with more options than fit |
| PB-02 Civic decision cycle | A governance lesson with no decision activity of its own |
| PB-03 Counting methods | A vote, or a lesson on fairness: approval voting compared with a single-choice count; Equal Shares in a High grade band |
| PB-04 Shared resource round | The class shares a real non-money resource (a garden bed, materials, time slots) |
| PB-05 Report-back | After any vote: the result and the counting rule, on chart paper |

**What the evidence shows.** School PB research concerns participation and civic learning; **evidence of academic effects is thin** [B3]. Students never handle real money: every budget is in made-up points.

---

## Live results

On 7 November 2026 the full sweep (`python3 -m lsb.regress`) ran all nine test chapters. Every case met every expectation: the right status, unit limit, planted traps gone, required terms kept, and teacher cards passing the clarity check.

| Case (country, subject) | Result | Units | Calls | Cost | Cards applied |
|---|---|---|---|---|---|
| Hydrology (generic, science) | PASS | 2 | 19 | $4.00 | EB-03, EB-04 |
| Ecosystems (generic, science) | PASS | 4 | 24 | $5.08 | CL-02, EB-03, EB-04, EB-05 |
| Civics (generic, civics) | PASS | 4 | 20 | $4.57 | CL-04, CL-05, EB-01, EB-03, EB-04, PB-02 |
| [Kenya, Grade 6 science](docs/walkthroughs/01-kenya-clean-water/) | PASS | 4 | 23 | $5.14 | CL-02, CL-05, EB-01, EB-04 |
| [Peru, Grade 5 mathematics](docs/walkthroughs/02-peru-fractions/) | PASS | 3 | 17 | $3.60 | CL-05, EB-01, EB-04, PB-04 |
| [Vietnam, Grade 6 literature](docs/walkthroughs/03-vietnam-folk-tales/) | PASS | 4 | 22 | $4.25 | CL-04, EB-01, EB-02, EB-04 |
| [Ghana, JHS 2 social studies](docs/walkthroughs/04-ghana-local-government/) | PASS | 3 | 19 | $3.84 | CL-05, EB-01, EB-03, EB-04, EB-05, PB-03, PB-05 |
| [Bangladesh, Class 1 reading](docs/walkthroughs/05-bangladesh-letters-and-sounds/) | PASS | 4 | 21 | $3.56 | EB-01, EB-02, EB-04 |
| [Mexico, Grade 8 history](docs/walkthroughs/06-mexico-migration/) | PASS | 3 | 13 | $2.16 | CL-04, EB-01, EB-04 |
| **Total (9 of 9)** | | **31** | **178** | **$36.20** | |

What the sweep shows:
- **Eight of nine runs needed the repair round.** The review after each optimisation stage catches what the decompose review missed: problems in steps no stage changed (a lake-shore assumption in Kenya, chart paper in Bangladesh, a ranked list that was never ranked in Ghana). One repair round fixed them; hydrology and Vietnam needed a second. Mexico is the exception: it passed its stage reviews clean and needed no repair.
- **Participatory budgeting abstains where it should.** It stayed out of every reading, science and literature unit (Bangladesh, Kenya, Vietnam, ecosystems, hydrology) and applied only where the unit held a real trade-off or decision: the garden vote in Peru, the mock vote in Ghana, the decision cycle in civics.
- **Every run removed its planted traps and reported them.** Unsafe activities, child data, money handling, purchases and region-specific names and currencies are gone from the cards and listed as source flags for the adapter.
- **The usage limit cut the first pass off part-way.** Five of nine cases finished before the session limit hit; those were kept, only the rest were re-run, and the full report was rebuilt once all nine had finished.

---

## What this project can and can't claim

| Can say | Can't say (yet) |
|---|---|
| On nine original test chapters, the pipeline produced sequences that pass every code check, with the planted traps removed and reported | That any card improves learning, attendance or engagement |
| Every step traces to the source or to a named card, and code verifies every optimisation edit kept its limits | That the evidence-based practice list is the right one for a given system |
| A failed optimisation never reaches the cards | That the output is good on real textbooks, which are longer and messier than the test chapters |
| The reviewer catches real problems (missing supervision, a vote with no rule, a broken prerequisite) and revisions fix them | That teachers find the cards usable: no practitioner has reviewed them |

**How to find out:** have curriculum specialists review the walkthrough cards → run real chapters from partner systems → pilot a few units with teachers and collect class-level feedback → compare completion and teacher ratings across versions.

---

## Folder structure

```
lesson-scaffold-builder/
├── README.md                    ← you are here
├── LICENSE                      Apache 2.0
│
├── docs/                        READ FIRST if you're new
│   ├── README.md                index
│   ├── ux/                      who uses it, the end-to-end journey, decision points
│   ├── walkthroughs/            six folders: walkthrough + source + decision trace + final cards each
│   ├── technical.md             every check, flag, output file and exit code
│   └── regeneration-prompts.md  prompts to rebuild this project with an AI coding agent
│
├── frameworks/                  THE METHOD: the cards the stages may apply
│   ├── evidence-based-practices.md   EB-01 to EB-05, non-negotiables, guardrails
│   ├── connected-learning.md         CL-01 to CL-05, guardrails
│   └── participatory-budgeting.md    fit-gate, PB-01 to PB-05, guardrails
│
├── prompts/                     MODEL STAGES (JSON in, JSON out)
│   ├── README.md                flow diagram and orchestration notes
│   ├── 05-decompose.md  25-evidence-based.md  30-connected-learning.md
│   ├── 31-participatory-budgeting.md  50-critic.md
│   └── 10, 15, 20, 40, 60       legacy single-project prompts from the MIP transformer, not used
│
├── lsb/                         CODE
│   ├── run.py                   the pipeline runner (Claude Code, Muse, or API backend)
│   ├── validate.py  dag.py      deterministic checks D01–D11
│   ├── optimise.py              edit limits for the optimisation stages; merge and trace
│   ├── render.py                teacher cards and the G21 check
│   └── regress.py               regression sweep with per-case expectations
│
├── schemas/mls-dag.schema.json  the MLS_DAG_Sequence schema
├── config/taxonomy_mapping.json limits, region-specific terms and currencies
└── tests/                       offline tests; fixtures (9 test chapters); regression cases
```

---

## References

**Context**
- [R1] Pritchett, L., & Beatty, A. (2015). Slow down, you're going too fast: Matching curricula to student skill levels. *International Journal of Educational Development*, 40, 276–288.
- [R2] World Bank, UNESCO, UNICEF, FCDO, USAID & Bill & Melinda Gates Foundation (2022). *The State of Global Learning Poverty: 2022 Update.*

**Evidence-based practices**
- [E1] Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest*, 14(1), 4–58.
- [E2] Pashler, H., Bain, P. M., Bottge, B. A., Graesser, A., Koedinger, K., McDaniel, M., & Metcalfe, J. (2007). *Organizing Instruction and Study to Improve Student Learning* (NCER 2007-2004). Institute of Education Sciences, U.S. Department of Education.
- [E3] Rosenshine, B. (2012). Principles of Instruction: Research-based strategies that all teachers should know. *American Educator*, 36(1), 12–19, 39.
- [E4] Black, P., & Wiliam, D. (1998). Inside the Black Box: Raising standards through classroom assessment. *Phi Delta Kappan*, 80(2), 139–148.

**Connected Learning**
- [C1] Ito, M., Gutiérrez, K., Livingstone, S., Penuel, B., Rhodes, J., Salen, K., Schor, J., Sefton-Green, J., & Watkins, S. C. (2013). *Connected Learning: An Agenda for Research and Design.* Digital Media and Learning Research Hub.
- [C2] Ito, M., Arum, R., Conley, D., Gutiérrez, K., Kirshner, B., Livingstone, S., Michalchik, V., Penuel, W., Peppler, K., Pinkard, N., Rhodes, J., Salen Tekinbaş, K., Schor, J., Sefton-Green, J., & Watkins, S. C. (2020). *The Connected Learning Research Network: Reflections on a Decade of Engaged Scholarship.* Connected Learning Alliance.

**Participatory budgeting**
- [B1] Goel, A., Krishnaswamy, A. K., Sakshuwong, S., & Aitamurto, T. (2019). Knapsack Voting for Participatory Budgeting. *ACM Transactions on Economics and Computation*, 7(2), Art. 8.
- [B2] Peters, D., Pierczyński, G., & Skowron, P. (2021). Proportional Participatory Budgeting with Additive Utilities. *NeurIPS 34*, 12726–12737.
- [B3] Gibbs, N. P., Bartlett, T., & Schugurensky, D. (2021). Does School Participatory Budgeting Increase Students' Political Efficacy? *Curriculum and Teaching*, 36(1).

*Statistics are reproduced from the sources above; check the primary source before quoting.*

---

## Licence

Copyright 2026 Ashit Patel. Licensed under the [Apache License, Version 2.0](LICENSE). The prompts, framework cards, docs and test chapters are covered by the same licence. Research cited in the cards and docs belongs to its authors and is summarised, not reproduced.
