# Design note: a staged field evaluation for LSB

*Turning lessons into teachable classroom plans.*

**Status: exploratory, 2026-11-12. Nothing here has been run.** LSB has no partner school system, no reviewer and no evaluator yet. This note turns the README's [How to find out](../README.md#what-this-project-can-and-cant-claim) line into a plan that a partner and a research team could start from. Every threshold below is a **project choice made for this note**, not a published standard from any research organisation. A partner or evaluator should replace them with their own.

## Why this note exists

The README separates what LSB can claim from what it can't. Code checks (D01–D11), a 21-check reviewer (G01–G21) and the nine-case regression sweep show that the pipeline produces well-formed sequences on original test lessons. They don't show that:
- the output is good on **real textbooks**, which are longer and messier than the test lessons;
- **teachers** find the cards usable;
- any card improves **learning**, attendance or engagement.

Each phase below answers one of those questions, in that order. Each phase must pass before the next one starts, because a trial of cards that teachers don't use measures nothing.

## What is being evaluated

The intervention is **not** the raw pipeline output. It is:

1. **LSB run on the partner's own curriculum units**, at one frozen version;
2. **reviewed by a named adapter at the partner**, who checks the source flags, the locale handling and the content before printing (the README requires this review before classroom use);
3. **printed as `cards.html`** and handed to teachers.

### Freeze the cards

LLM output differs from run to run, and LSB changes between releases. For Phases 2 and 3, generate each unit's cards **once**. Record:
- the LSB `VERSION` (currently 0.3.0) and the git commit;
- the backend and the model;
- the run folder (`runs/<timestamp>/`) with its `summary.json`.

Then print from that frozen set. Don't re-run or `lsb-refine` a unit mid-phase. A fix found during a phase goes into the next phase's frozen set, and the change is logged.

### Record the adapter's edits

For every unit, keep the adapter's changes to the cards as a diff against the frozen `cards.txt`. How much a person had to change is itself a result: it measures what the pipeline still gets wrong.

## Phase 1: curriculum review on real units (before any classroom)

**Question.** Does LSB produce faithful, safe, runnable cards from the partner's real material?

**Material.** Units from the **partner's own textbooks or syllabus**, not the [walkthroughs](walkthroughs/). The walkthroughs are original test lessons with planted traps; they show the pipeline works, not that it works on real curriculum. Choose units across the subjects and grade bands the partner would use, including at least one that is long and dense.

**Reviewers.** Curriculum specialists and experienced teachers from the partner system. A rough starting point is 2–3 specialists and 5–10 teachers per subject and grade band.

**Method.** An expert review, not a blind one: a reviewer comparing a textbook unit with its cards always knows which is which. If a blind comparison is wanted, compare LSB's cards with a version adapted by a person from the same unit, with the source hidden.

**What to record, per unit:**
- **Goal preservation** (1–5): do the unit's objective and core concepts survive decomposition?
- **Wrongly removed content.** For each source flag in `summary.json` (and each item in `locale-log.json` for relocalize runs), was the removal right? Count removals the reviewer would undo.
- **Missed problems.** Unsafe, costly or region-specific content that is still on the cards.
- **Evidence-based practice fit.** For each evidence-based method card applied, are its non-negotiables intact on the teacher card? Was it applied where it shouldn't have been, or missed where it clearly fits?
- **Adapter edits.** The size of the diff against the frozen cards.
- **Ready for class?** Yes, yes after minor edits, or no.

**Exit gate (project choice).** Most reviewed units rated ready after at most minor edits, with no missed safety problem left uncorrected. A missed safety problem is a pipeline bug to fix before Phase 2, whatever the overall rate.

**Also worth doing in this phase.** Check the evidence-based practice list itself against the partner's curriculum framework and against current reviews of structured pedagogy and Teaching at the Right Level. The README calls the list a project choice that needs review by the people who own the content.

## Phase 2: classroom fidelity pilot (one unit cycle, roughly 4–6 weeks)

**Question.** Do teachers run the cards as written, and where do they get stuck?

**Sample.** A small number of classrooms across several schools, chosen on purpose to include low-resource and offline settings. A rough starting point is 15–30 classrooms in 5–10 schools. There is no comparison group; this phase is about use, not effect.

**Method.** Brief weekly check-ins with each teacher by paper log, SMS or a short call, whichever the partner already uses. One or two classroom observations per teacher, if the partner can arrange them.

**What to record:**
- **Step completion:** the share of planned steps run within the unit's 2-to-4-week window, and which steps were skipped and why.
- **Fidelity to non-negotiables**, for units where these method cards were applied:
  - EB-01: notes away, answers shown straight after, **nothing marked or recorded**;
  - EB-04: **every** student answers at once, the teacher looks, and what happens next depends on it;
  - EB-06: a fresh level check, and groups re-checked rather than fixed.
  A hollow version counts as not done.
- **Conditions that didn't hold.** Each unit card lists the conditions it relies on and what to do if one doesn't hold. Record which conditions failed and whether the fallback worked.
- **Prep time:** teachers' own estimate of minutes spent preparing the unit, against their usual preparation for a similar unit. The cards are not designed to need no preparation, so measure it.
- **Teacher rating** of each card, with free-text comments.
- **Costs** per unit: model usage, adapter review time, printing and teacher preparation time (see [What this means for LSB](#what-this-means-for-lsb)).

**Exit gate (project choice).** Most planned steps run, fidelity to the non-negotiables high enough that a trial would test the practices and not a hollow version, and prep time **no worse** than usual. The gate does not require prep time to fall; whether it falls is a finding, not a condition.

## Phase 3: cluster-randomised trial (at least one term)

**Question.** Do LSB cards, reviewed by the partner's adapter, change learning or teacher workload compared with what schools do now?

This phase needs a research team with its own ethics approval, and a partner that can deliver cards to enough schools. The design is theirs to set. The points below are what LSB's design implies for it.

**Randomise by school.** Teachers in one school share printed cards and ideas, so randomising by teacher would leak treatment into the control group.

**Comparison.** "Business as usual" (the usual textbook and syllabus) is the simplest control, but it can't separate LSB's content from the effect of receiving new printed materials and attention. If that matters to the partner, add an arm that receives printed material without LSB's restructuring, or say plainly in the analysis plan that the comparison is with business as usual.

**One primary outcome.** Choose one, before baseline: most likely an end-of-term assessment aligned to the curriculum, set by the partner or the evaluator. Teacher time on task, prep burden, completion, attendance and engagement are secondary outcomes.

**Connected Learning and participatory budgeting are secondary only.** The README forbids claiming that CL or PB method cards improve test scores. Engagement in units where CL-01–CL-05 or PB-01–PB-05 were applied can be measured as a secondary outcome; it must not be the primary outcome or be reported as an effect on learning.

**Power and registration.** Size the trial with a power calculation based on the partner's own data on clustering of scores between schools. Pre-register the analysis plan, for example on the [AEA RCT Registry](https://www.socialscienceregistry.org/), before baseline testing.

**Duration.** A single term covers only a few 2-to-4-week units. Spaced and retrieval practice (EB-01, EB-02) may need longer to show. Consider a delayed follow-up assessment.

## Data: who holds what

This follows the decision in the [ELEVATE design note](integrations/elevate.md#1-evidence-capture-stays-optional-teacher-side-and-class-level): **LSB holds no student data.**

- **Cards stay free of child data** (critic check G06): no names, faces, individual scores or home details. The trial doesn't change that.
- **Assessment scores, attendance and teacher logs belong to the evaluator and the partner**, under their consent and data agreements. None of them go into LSB, its run folders or this repository.
- **The cards' quizzes are not trial instruments.** EB-01 retrieval questions must stay unmarked and unrecorded. Using them as assessments would break the practice being tested.
- **Teacher check-ins are about the class**, not about individual students.

## What this would and wouldn't let LSB claim

| After | LSB could say | LSB still couldn't say |
|---|---|---|
| Phase 1 | Cards from the partner's real units were judged faithful and runnable by its specialists, after a measured amount of editing | That teachers use them as designed |
| Phase 2 | Teachers in the pilot ran most steps, with measured fidelity and prep time | That the cards change learning |
| Phase 3 | An estimated effect on the primary outcome, for this partner, version and setting | That the effect carries over to other systems, subjects or LSB versions |

## Who builds this kind of evidence, and how LSB users can draw on it

LSB applies practices whose evidence comes from other people's studies. That leaves two separate questions:
1. **Do the practices work?** Mostly answered elsewhere, with the limits the [evidence guide](evidence-guide.md#what-the-evidence-does-and-doesnt-say) sets out.
2. **Does delivering them through LSB cards work,** in a given system, at a given cost? Nobody has answered this yet.

The organisations below work on both. None of them has reviewed or endorsed LSB. Details were checked against their own pages in November 2026 and can change; check them again before relying on them.

| Organisation | What it does | How an LSB user can draw on it |
|---|---|---|
| [J-PAL](https://www.povertyactionlab.org/) (Abdul Latif Jameel Poverty Action Lab, MIT, with regional offices) | A network of affiliated university researchers who run randomised evaluations, and a policy team that summarises what they find. Its [Learning for All Initiative](https://www.povertyactionlab.org/node/8033470) funds pilots, randomised evaluations and scale-ups of ways to improve children's learning in low- and middle-income countries. | The Teaching at the Right Level trials behind EB-06 [E10, E11] are J-PAL-affiliated work with Pratham. Its funding goes to affiliated researchers, not to implementers, and it covers research costs only: **the implementing partner pays for delivery**. A user needs a researcher to apply with. |
| [Innovations for Poverty Action](https://poverty-action.org/) (IPA) | A research and policy nonprofit with country offices that runs field trials, often with J-PAL affiliates. Its [Right-Fit Evidence](https://poverty-action.org/right-fit-evidence) unit helps implementers build monitoring, evaluation and learning systems. | Phases 1 and 2 are monitoring, not impact evaluation. This is where Right-Fit support fits: deciding what to measure, and collecting it well, before anyone pays for a trial. |
| [CEGA](https://cega.berkeley.edu/) (Center for Effective Global Action, UC Berkeley) | A network of researchers on global development. Its [BITSS](https://cega.berkeley.edu/theme/transparency) initiative promotes research transparency: registries and pre-analysis plans. Its [Cost Transparency Initiative](https://cega.berkeley.edu/initiative/cost-transparency-initiative) works on costing, noting that fewer than one in five impact evaluations report cost-effectiveness, and publishes a costing pre-analysis plan template. | Education is not CEGA's main focus. Its value here is methods: a pre-analysis plan for Phase 3, and a costing plan, so that a result can be compared with other ways of spending the same money. |
| [Global Education Evidence Advisory Panel](https://www.worldbank.org/en/topic/teachingandlearning/publication/cost-effective-approaches-to-improve-global-learning) (GEEAP, convened by the World Bank, the UK's FCDO and UNICEF, among others) | "Smart Buys" reports that rate approaches to improving learning in low- and middle-income countries by cost-effectiveness, drawing on hundreds of evaluations. In 2023, **structured pedagogy** and **targeting instruction by learning level** were among its "Great Buys"; investing in hardware or other inputs alone was a "Bad Buy". | The fairest summary of where LSB sits in the evidence. See [What this means for LSB](#what-this-means-for-lsb). |
| [What Works Hub for Global Education](https://www.bsg.ox.ac.uk/research/what-works-hub-global-education) (Blavatnik School of Government, Oxford, with governments and funders) | Turns evidence on foundational learning into action: evidence translation, evidence labs inside governments, and implementation science, the study of what makes a working approach survive delivery at scale. | Phase 2's question, whether teachers run the cards as written, is an implementation-science question. Relevant if the partner is a government it works with. |
| Registries and syntheses: [AEA RCT Registry](https://www.socialscienceregistry.org/), [3ie](https://www.3ieimpact.org/), the IES [What Works Clearinghouse](https://ies.ed.gov/ncee/wwc/), the EEF [Teaching and Learning Toolkit](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit) | Places to register a trial, and systematic reviews and evidence gap maps of what has already been tested. The IES practice guide is already one of LSB's sources [E2]; the EEF draws mainly on high-income evidence. | Check whether something close to an LSB trial already exists before designing one, and register the analysis plan before baseline. |

### What this means for LSB

1. **Structured pedagogy is the closest match, and LSB covers only part of it.** In the GEEAP sense, structured pedagogy is a package: structured lesson plans, learning materials, and ongoing support for teachers, such as coaching. LSB cards are structured lesson plans. LSB adds no materials beyond what classrooms already have, and no coaching. **The evidence for the package can't be borrowed for the cards alone.** A trial with one arm that gets the cards alone and one that gets the cards with the partner's coaching would show what the cards add on their own.
2. **Targeting by level depends on the conditions that made it work.** The TaRL trials used dedicated time and instructors, and EB-06 adapts the practice inside existing practice time. Phase 2's fidelity checks are what show whether the adaptation keeps the practice intact.
3. **Cost is part of the result.** Smart Buys ranks approaches by learning per unit of money spent. LSB's costs include the model usage per run (recorded in `summary.json`), the adapter's review time, printing and teachers' time. Record them per unit from Phase 1 on, using a costing template such as CEGA's, so a trial can report cost-effectiveness and not only effect.
4. **A trial tests the package as delivered.** A cluster trial of whole sets of teacher cards will not show which method card did the work. It also adds little to the evidence on the individual practices, which mostly comes from high-income settings. What it would add is evidence on whether an automated, reviewed adaptation of a system's own curriculum is a cost-effective way to get these practices into classrooms.

## Approaching a research team

This section is for an organisation that uses LSB: an NGO programme, a district training team, a textbook team or a ministry unit (the curriculum adapter in [Who uses it](ux/01-who-uses-it.md)). For a trial, **that organisation is the implementing partner**. LSB's maintainers are not a party to it.

### Are you ready?

Research groups that run field trials usually look for three things:
1. **An implementing partner** able to deliver the cards to enough schools for a school-level comparison. If you are writing, this is you.
2. **A way to randomise**: for example, phasing schools in by lottery or a waiting list, which you would have to be willing to do.
3. **Outcome data you already collect**, such as term assessments or attendance, which keeps the cost of evaluation down.

Write once you have all three and have finished **Phase 1** on your own units. Phase 2 results make a much stronger case. Without Phase 1 you can only offer a promise; with it you can show what your specialists found.

Possible contacts include the organisations in [Who builds this kind of evidence](#who-builds-this-kind-of-evidence-and-how-lsb-users-can-draw-on-it) (for school trials, usually J-PAL's regional offices or IPA's country offices), university education or economics departments near you, and your ministry's own research or assessment unit.

### Template

Fill in every `[bracket]` and delete any line you can't support. Keep LSB's status in its own terms: the README's [What this project can and can't claim](../README.md#what-this-project-can-and-cant-claim) table is the limit of what the email may say about the tool. Don't claim the cards improve learning; finding out is the point of the trial.

> **Subject:** Evaluation partnership: [your organisation] and printed teacher cards for [subject, grade band] in [region]
>
> Dear [name or team],
>
> I lead [programme] at [your organisation], which supports [number] teachers in [number] [primary/secondary] schools in [region]. We are looking for a research team interested in evaluating a change to how our teachers receive curriculum material.
>
> **What we are doing.** We use Lesson Scaffold Builder (LSB), an open-source pipeline, to turn our [textbook/syllabus] units into short printed teacher cards: 2-to-4-week sequences of classroom steps that need no devices or purchases. The pipeline removes unsafe, costly or region-specific requirements and adds a small set of practices with replicated evidence (such as retrieval practice, worked examples, checking every student's understanding and grouping by level, in the spirit of Teaching at the Right Level) only where they fit. Our [specialists/adapters] review every unit before it is printed. LSB is a working prototype, and its developers make no claim that the cards improve learning.
>
> **What we have found so far.**
> - Curriculum review ([n] units, [n] reviewers): [share rated ready after at most minor edits]; [main problems found and fixed].
> - [If done] Classroom pilot ([n] classrooms, [n] weeks): [share of steps completed]; [fidelity finding]; [prep-time finding].
>
> **What we can offer a study.**
> - Delivery to [number] schools, with willingness to phase schools in by [lottery/waiting list].
> - Existing outcome data: [assessment, attendance or other], collected [when], held by [whom].
> - A frozen, documented set of cards for the study period.
>
> **What we are asking.** Would your team, or researchers you work with, be interested in designing an evaluation with us? We would welcome a short call about fit, timing and any funding rounds you think suit this work.
>
> Our draft evaluation plan, based on LSB's evaluation protocol: [link]. Sample cards: [link].
>
> Best regards,
> [name, role, organisation, contact]

Keep the email free of student data: no names, individual scores or school-level results that could identify a child. Share data only after a data agreement is in place, as described under [Data: who holds what](#data-who-holds-what).
