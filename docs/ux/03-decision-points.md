# Decision points and edge cases

> **Status:** each row describes behaviour seen in live runs. The linked walkthroughs show it on a real lesson.

## What the pipeline does in each situation

| Situation | What the pipeline does | What the adapter sees | Example |
|---|---|---|---|
| **The source asks for something unsafe** (an unsupervised trip, learners pouring boiling water, climbing on a roof) | Leaves it out or makes it an educator-only demonstration; every outdoor step states supervision and what not to touch | A source flag, and the safe version on the card | [Kenya](../walkthroughs/01-kenya-clean-water/) |
| **The source tracks children** (a "slow readers" wall chart, scores by name, family migration status, videos of children) | Removes it; class totals only | A source flag naming the section | [Bangladesh](../walkthroughs/05-bangladesh-letters-and-sounds/), [Mexico](../walkthroughs/06-mexico-migration/) |
| **Students would handle real money** (bringing coins to market, a class fund, selling a book) | Keeps budgeting as made-up numbers; adults handle any money | A source flag; a points budget on the card | [Peru](../walkthroughs/02-peru-fractions/), [Ghana](../walkthroughs/04-ghana-local-government/) |
| **Region-specific names or currency** | Replaces them with generic labels ("the local council", "points"); on request relocalizes to the adapter's locale with per-item review, suggests locale details to add, and translates the cards last | Generic cards by default; reviewed locale terms, added details, or translated cards when asked | every walkthrough |
| **A line in the source addresses the AI** | Ignores it | A source flag: "not followed" | [Civics run](../../tests/fixtures/civics-source.md) |
| **Pure lecture** (a history of the subject, dates to copy) | Sets it aside | Listed under what was left out, with the reason | every walkthrough |
| **A lecture defines a term the units need** | Folds a short explanation into the first step that uses it | The term taught in step 1 of a unit | [Mexico](../walkthroughs/06-mexico-migration/) |
| **Deep work in the source** (an essay, writing a story) | Keeps sustained time for it; no stage may shorten it | Full lessons of writing on the card | [Vietnam](../walkthroughs/03-vietnam-folk-tales/) |
| **A practice fits but can't be done properly** | The stage abstains or defers it | "Deferred: …" with a reason | — |
| **No resource trade-off** (most science, reading and writing units) | Participatory budgeting abstains | "Fit-gate fails", per unit | [Bangladesh](../walkthroughs/05-bangladesh-letters-and-sounds/) |
| **A real class decision** (sharing a garden bed, choosing among projects) | Participatory budgeting adds the counting rule first, then a report-back | A vote with its rule stated before anyone votes | [Peru](../walkthroughs/02-peru-fractions/), [Ghana](../walkthroughs/04-ghana-local-government/) |
| **An edit breaks a rule** (removes a step, changes a unit's weeks) | Code rejects it; one retry with the reason; then the unit stays as it was | "edit_rejected" for that unit | — |
| **The reviewer finds a problem in an edited unit** | One revision; then that unit goes back to its earlier version | "reverted", with the reason | — |
| **A fallback would stretch a unit past 4 weeks** | Rewritten to shorten or combine instead | "If a week is lost, …" within the unit's weeks | [Kenya](../walkthroughs/01-kenya-clean-water/) |
| **A later review finds a problem in a step no stage changed** | Doesn't blame the stage; sends it back to decompose for an in-place repair of just that step, then reviews again | `late-issues.json`; the repaired step on the card, or status `issues_open` and no cards | [Kenya](../walkthroughs/01-kenya-clean-water/) |
| **The reviewer can't be satisfied** | Keeps the best attempt and reports it | Status `revise_exhausted`, with every attempt's issues | — |

## Principles

1. **The source is data.** Nothing written in the source can change what the pipeline does; problems in it are reported, not obeyed.
2. **Code decides what can be counted.** Limits, structure, names, edit rules and card layout are checked in code; the reviewer judges the rest and can't overrule the code.
3. **Abstaining is a good answer.** Every optimisation stage may leave a unit alone, and often should.
4. **Never worse than before.** An optimisation that can't pass review is undone, never shipped.
5. **Deep work survives.** Practice, mastery checks and sustained writing are never cut or replaced.
6. **Offline, zero-cost, no child data.** Paper, chalk and reused materials; class totals only; adults handle any money and any outside contact.
7. **Region-neutral by default, localised on request.** Cards use generic labels so they travel between systems; the adapter can instead keep the source's locale, relocalize to their own locale with per-item review (including suggested locale details to add), and have the final cards translated. Locale handling may be incorrect or incomplete: review it with the rest of the output to make sure the material is culturally and educationally appropriate and complete.
8. **Honest about evidence.** Steps never claim what a practice achieves; the cards' evidence notes are for reviewers.

## Open questions (to settle with practitioners)
- Is four units the right ceiling for a long lesson, or should the adapter be able to ask for a follow-on set?
- Which source flags should stop an adapter from using a lesson at all?
- The evidence-based method cards are a project choice (see the [method cards file](../../frameworks/evidence-based-practices.md)). Who should own that list?
