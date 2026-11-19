# Stanford methodologies: triage, thresholds, and inventory

> **Status:** implemented (adaptable cores, threshold gates, tech
> inventory, tech-conditional stage). "Phase" here means implementation
> phase, not the field-evaluation phases in evaluation-protocol.md.

How LSB offers methodologies translated from Stanford Accelerator for Learning
research: what adapts to offline teacher cards, what waits on technology, and
the effectiveness thresholds that decide between applying and abstaining.
Every threshold value below traces to an inspected primary source (Step 1,
2026-11-19); rows without one stay out.

## Triage

| Methodology | Verdict | Reason |
|---|---|---|
| NSSA tutoring protocol | ADAPT → CL-02 fold-in (`nssa-tutoring`) | Human routine, no tech. Dose 3+/week for 10+ weeks, consistent trained tutors, ≤4:1, curriculum-aligned, in-school-day. [NSSA playbook](https://nssa.stanford.edu/district-playbook-high-impact-tutoring/about) |
| Talk uptake moves | ADAPT method only → EB-04 fold-in (`uptake-moves`) | Revoice ideas, press for reasoning, wait time need no tech. Recording the classroom to measure them is vetoed (G06). [TeachFX FAQ](https://teachfx.com/faq), [Learning Forward](https://learningforward.org/journal/learning-with-ai/ai-enhanced-coaching-what-early-studies-show/) |
| Civic mapping | ADAPT paper core → CL-03 fold-in (`civic-mapping`) | Our Voice runs Discover/Discuss/Activate/Change; the app (photos, GPS, audio narratives) is dropped for G06/G08. In-school paper mapping + class tallies + in-school report-back survive. [PARCS](https://pmc.ncbi.nlm.nih.gov/articles/PMC10522010/) |
| UDL choice | ADAPT → EB-05 fold-in (`udl-choice`) | CAST's three principles (Engagement, Representation, Action & Expression) prescribe no technology; choice/autonomy and multiple perception channels encode directly. [CAST](https://udlguidelines.cast.org/) |
| ROAR screening | OFFERED as ST-01 (opt-in + inventory + Primary) | Self-administered browser assessment; needs one browser device per student plus connectivity; runs in class or at home. [Stanford](https://news.stanford.edu/stories/2022/06/new-online-tool-helps-schools-spot-struggling-readers) |
| AI literacy (CRAFT-style) | OFFERED as ST-02 (opt-in + inventory + High) | Needs basic AI tools, bandwidth, teacher training; High band. [Stanford GSE](https://ed.stanford.edu/news/bringing-ai-literacy-high-schools) |
| RQ Lab | OUT OF SCOPE | Grade-9 pastoral workshops in 16-per-cohort groups; no lesson-scaffold mapping. Revisit for advisory content. [Transcript](https://ampedto11.com/podcast/can-we-teach-the-capacity-to-relate/) |
| Classroom recording (TeachFX-full, MPT-full) | VETO (never offered) | Audio/transcripts of children breach G06 unconditionally; licenses breach G17. |
| IEP admin tooling (Journify-style) | OUT (not a lesson artifact) | Teacher workflow tooling has no card mapping. No primary source inspected; verdict stands regardless. |

Evidence gaps: Harvard CEPR page (403; MPT covered by Learning Forward
instead); ROAR per-screener minutes and exact grades (snippet-only);
the "8-workshop" RQ count (unverified, unused). No effect-size claim
from any source ships to cards.

## What changes on your cards

One paragraph per family, in teacher language:

- **Peer tutoring.** One practice step per fitting unit becomes paired
  tutoring: the same pairs each session, tutor and tutee swapping roles,
  working the unit's own exercises. Nothing new needed.
- **Talk uptake moves.** Whole-class checks gain three teacher moves:
  revoice one student idea, press one student for reasoning, wait
  silently after asking. Nothing is recorded.
- **Civic mapping.** One step per fitting unit sends groups to map
  school grounds on paper and combine marks into one class tally, then
  report back in school. No photos, devices, or trips.
- **UDL choice.** Explanation steps present each key point heard and
  seen; answers may be spoken, written or shown. Nothing beyond paper,
  chalk and voice.
- **ROAR screening.** One step runs a short browser reading check per
  child, then the teacher regroups for decoding practice. Marked with
  its tech needs; nothing about any child is recorded.
- **AI literacy.** One step has pairs use classroom AI for a bounded
  task, then critique bias and errors with a teacher debrief. Marked
  with its tech needs.

## Using the guided flow

With `--ask`, the run interviews you before spending anything on models:

1. **Goals.** Pick what matters in plain language (find strugglers,
   more talk, real surroundings, access, AI). Leave blank for none.
2. **Proposal.** The next question suggests method families with
   numbered picks and grade-band caveats. Type the suggestion, adjust
   it, or leave blank. Type `?N` on any option for what it is, what it
   demands, what changes on your cards, and where to read more.
3. **Inventory.** Five short questions (sessions, tutor, devices,
   internet, home access), each explaining what it gates.
4. **Preview.** Before the first model call, a methodology check lists
   what will be considered and what stays out with reasons. Overruling
   the proposal is allowed; thresholds still apply.

`--answers` files skip the guidance and answer directly; `method_goals`
is accepted but gates nothing.

Worked example (middle-school class via `--grade-band Middle`, wants
strugglers found and AI judged; practice 3 times a week with a steady
tutor; shared devices with internet; the teacher overrules the proposal
to include the two gated families):

```
Which goals matter for this run?
  1. Find where strugglers are stuck — screening + extra practice
  [... options 2–5 ...]
> 1,5
Based on your goals (Find where strugglers are stuck, Students using and judging AI tools), suggested: 1 — peer tutoring (extra practice in steady pairs).
ROAR screening (browser check per student) needs the Primary band (this run: Middle) — left out
AI literacy (use + critique AI) needs the High band (this run: Middle) — left out
Each applies only above its threshold (checked next). Type suggested numbers, adjust, or blank for none.
Which Stanford-translated method families may apply?
  [... options 1–6 ...]
  (?N for more about an option)
> ?5
What: each child completes a short browser reading check; the teacher regroups from it.
Demands: one browser device per student + internet, Primary band. Nothing recorded.
Changes: one screening step, marked with its tech needs.
More: docs/methodologies.md.
> 1,5,6
[... five inventory questions ...]
Methodology check (based on your answers):
• Peer tutoring protocol: will be considered for fitting units.
• ROAR screening: not offered — one browser device per student; Primary grade band.
• AI literacy: not offered — High grade band.
Details: docs/methodologies.md.
```

## Threshold model

Each offered family has a fit-gate. Below the gate the run abstains or
defers with a reason naming the failed factor — never a weakened variant.

| Family | Code gates (countable) | Model-judged fit |
|---|---|---|
| `tutoring` | Opted in; sessions/week ≥ 3; consistent tutor available | Skill practice suited to pairs; same pairs across the unit's weeks |
| `uptake` | Opted in | Explanation/discussion steps (not silent drills); move complexity fits the grade band; no recording ever |
| `mapping` | Opted in | Place/data/community content; on school grounds; in-school or mock audience only; fits declared weeks/periods |
| `udl` | Opted in | Single-mode explanation or response worth a second channel |
| `roar` (ST-01) | Opted in; one browser device per student; internet; Primary band | Foundational-reading content where bottlenecks are invisible |
| `ai` (ST-02) | Opted in; shared or 1:1 devices; internet; High band | Any subject where students could use and critique AI |

Notes:

- The NSSA 10-week program span cannot fit a 2–4-week unit, so the
  fold-in is an in-unit adaptation (same pairs, rotating roles, ≥3x/week
  within the unit's weeks), labeled as such on the card's Basis line.
- Grade band and period length reuse the existing `GRADE_BAND` /
  `TIME_BLOCK_MINUTES` inputs; PB-03 already conditions on grade band.
- `home_access` currently customizes only the ROAR pointer; it is asked
  now so tech-conditional steps inherit a complete inventory.

## Inventory questions (`choices.json`)

| Key | Options | Default | Consumers |
|---|---|---|---|
| `method_goals` | multi of `gaps`, `talk`, `world`, `access`, `ai` | `[]` | proposes opt-in suggestions (guides humans; gates nothing) |
| `method_opt_in` | multi of `tutoring`, `uptake`, `mapping`, `udl`, `roar`, `ai` | `[]` | every gate |
| `sessions_per_week` | `1`, `2`, `3`, `4`, `5+` | `1` | tutoring gate |
| `tutor_staff` | `yes`, `no` | `no` | tutoring gate |
| `classroom_devices` | `none`, `teacher-only`, `shared`, `one-per-student` | `none` | ROAR/AI abstention reasons |
| `classroom_internet` | `yes`, `no` | `no` | ROAR/AI abstention reasons |
| `home_access` | `most`, `some`, `few` | `few` | ROAR pointer |

All defaults preserve current behavior: a run that answers nothing gets
no new methods. Audio recording is deliberately not asked: no answer
could authorize it.

Guided flow (`--ask`): plain-language goals propose families, every
option explains itself via `?N` with pointers here, and an eligibility
preview shows what will and won't apply (and why) before the run
proceeds. `--answers` files skip the guidance and answer directly.

## Routine tokens

Fold-ins name a `routine` in their change entry so code can gate them:

| Token | Host card | Family |
|---|---|---|
| `nssa-tutoring` | CL-02 | `tutoring` |
| `uptake-moves` | EB-04 | `uptake` |
| `civic-mapping` | CL-03 | `mapping` |
| `udl-choice` | EB-05 | `udl` |

Summaries stay teacher-readable; the token is structural only and is not
printed on cards.

## Tech-conditional steps (G08 exception)

ST cards are the one exception to the offline default, mirroring how the
stuck-group note excepts the no-routines rule. Each applied step carries a
`(needs: ...)` tech marker plus a same-day plan B in the step text. Three
independent checks enforce the gate: the stage is skipped entirely without
opt-in; code rejects unmarked steps and failing inventories; the critic's
G08 row re-verifies marked steps against the run's methodology context.
Recording the classroom stays vetoed: no ST step collects audio,
transcripts, photos, scores, names or accounts tied to a student.
