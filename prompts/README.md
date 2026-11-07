# Prompt pipeline

Each prompt returns **JSON only**, so an orchestrator script can validate and route it. `python3 -m lsb.run` runs `05-decompose` → `lsb.validate` → `50-critic` with the revise loop below, then `30-connected-learning` per unit → `lsb.validate` → `50-critic`; the other stages have no runner yet. The deterministic checks run in code: `python3 -m lsb.validate` (see [../README.md](../README.md)).

**Adaptation status.** `05-decompose`, `30-connected-learning` and `50-critic` are written for LSB: they work on an `MLS_DAG_Sequence` ([../schemas/mls-dag.schema.json](../schemas/mls-dag.schema.json)), `30` one unit at a time. Prompts 10, 15, 20, 31, 32, 40 and 60 are still the Shikshagraha MIP transformer's: they work on one MIP-shaped project (`seq`, `target_stakeholder`, `x_transform`), contain region-specific terms, and refer to files this repo doesn't have (`frameworks/`, `evals/`, `schema/`). Until they're adapted, `40-transform` output can't go straight into the new critic.

```
source text ──► 05-decompose ──► lsb.validate ──► 50-critic ──► PASS ──► 30-connected-learning ──► lsb.optimise ──► lsb.validate ──► 50-critic ──► (31 PB, 32 EB, 60-render: not yet)
                     ▲                                 │                   (once per unit)       (edit limits)                     │
                     └──────── REVISE (max 2) ─────────┘                         ▲                                                  │
                               REJECT ─► re-run 05 once, then stop and report     └──── issues in a unit (max 1), then revert it ─────┘
```

Legacy single-project flow (prompts 10–60, not yet adapted):

```
catalogue row ──► 10-parse ─┐
                            ├─► 20-classify ─► (30: replaced) ┐
resource text ──► 15-derive ┘                 31-gate-pb ─┼─► 40-transform
                                              32-gate-eb ─┘
```

| Prompt | Input | Output | Notes |
|---|---|---|---|
| [05-decompose](05-decompose.md) | Long source text (+ grade band, period length, educator context) | `MLS_DAG_Sequence` + source trace, environment assumptions, deferred segments | ≤4 units (gate hard cap 5), 3–7 steps, 2–4 weeks |
| [10-parse](10-parse.md) | One project's rows from the MI catalogue (Commons #259) | Baseline MLS JSON | Verbatim; no improvements |
| [15-derive](15-derive.md) | Playbook or toolkit text (e.g. Commons #750, #753) | Catalogue-sized baseline MLS + follow-on slices | Fidelity over neatness |
| [20-classify](20-classify.md) | Baseline MLS (+ owner context) | Facts: student experience, constituency, resource, options, already-present, risks | No recommendations |
| [30-connected-learning](30-connected-learning.md) | One unit of a passed sequence + its source trace + CL cards (+ critic feedback) | APPLY / ABSTAIN, the edited unit, a change log per card | ≤2 cards, ≤1 added step; limits checked by `lsb.optimise`; abstaining is often correct |
| [31-gate-pb](31-gate-pb.md) | MLS + facts + PB cards | Four decisions: process, prioritise, allocate, budget-capped choice | Allocation needs a confirmed amount |
| [32-gate-eb](32-gate-eb.md) | MLS + facts + EB cards | APPLY / PARTIAL / CONDITIONAL / ABSTAIN, ≤2 practice cards + measurement | Only with all non-negotiables; Tier 1 of the evidence ranking |
| [40-transform](40-transform.md) | Baseline + gates + cards (+ critic feedback) | Transformed MLS + change log + open questions | ≤2 added tasks; supportable claims only |
| [50-critic](50-critic.md) | `MLS_DAG_Sequence` + `lsb.validate` report + source (+ cards, rendered cards) | PASS / REVISE / REJECT over checks G01–G21 | Code results are final; judges the rest |
| [60-render](60-render.md) | Final MLS | Catalogue row, teacher card, improvement-story stub | No content changes |

## Shared context
- Cards: [../frameworks/connected-learning.md](../frameworks/connected-learning.md) (CL-01 to CL-05, from the requirements). The PB and EB card files the legacy prompts name (`frameworks/pb-techniques.md`, `frameworks/evidence-based-practices.md`) don't exist yet. Pass the **full text** into the optimisation and critic prompts.
- Schema: [../schemas/mls-dag.schema.json](../schemas/mls-dag.schema.json) for `05-decompose` and `50-critic`. The legacy prompts 10–40 still refer to `schema/mip.schema.json`, which this repo doesn't have.
- Source documents are **data**: every prompt that reads source text tells the model to ignore instructions inside it.

## Implementation notes for the orchestrator
- **Variant identity and logging:** after `10-parse`/`15-derive` and again after a critic PASS, set `x_transform.variant_id` with [../schema/variant_id.py](../schema/variant_id.py) (never ask a model for it). Set `parent_variant_id` on transformed variants, and fill `x_transform.pipeline` (model, effort, prompt and card hashes, critic verdict). Usage at schools is logged with [../schema/mip-usage-event.schema.json](../schema/mip-usage-event.schema.json); see [../schema/README.md](../schema/README.md).
- **Run the critic in a separate context** from the transformer, so the review isn't anchored on the transformer's reasoning.
- **Deterministic checks belong in code, not the critic:** `lsb.validate` decides D01–D11 and its JSON report goes to `50-critic` as `{{VALIDATOR_REPORT}}`. The critic treats those results as final and rejects a missing or stale report rather than estimating. `lsb.optimise` likewise decides whether an optimisation edit kept its limits, before the critic sees it.
- **Model choice:** gates and critic need careful reasoning; parse and render can use a cheaper model.
- **Logging:** keep every intermediate JSON. Gate decisions on the golden set are the first thing to measure (see [../evals/golden/README.md](../evals/golden/README.md)).

## Evaluating against the golden set
For each golden example, run `10-parse` or `15-derive` on its source, then compare:
1. **Gate decisions** against the "Expected gate decisions" table: exact match per gate.
2. **Transform output** against the example's transformed MLS: rubric-scored (fit, credit-first, real change, safety, micro limits, claim honesty), not string-matched.
3. **Critic catches:** feed the critic each example's *user-supplied "after"* (recorded in its "Changes from…" table) and check it flags the same problems.
