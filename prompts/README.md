# Prompt pipeline

Nine prompts transform one Micro-Lesson Scaffold (MLS). Each returns **JSON only**, so an orchestrator script can validate and route it. A runner exists only for the **classify + gates** stages: [../evals/run_gates.py](../evals/run_gates.py), scored against [../evals/gate_fixtures.json](../evals/gate_fixtures.json). The transform, critic and render stages have no runner yet.

```
catalogue row ──► 10-parse ─┐
                            ├─► 20-classify ─► 30-gate-cl ─┐
resource text ──► 15-derive ┘                 31-gate-pb ─┼─► 40-transform ◄──┐
                                              32-gate-eb ─┘
                                                                  │            │ REVISE (max 2)
                                                                  ▼            │
                                                              50-critic ───────┘
                                                                  │ PASS
                                                                  ▼
                                                              60-render ─► catalogue_row / teacher_card / story_stub
                                                                  
                         all gates ABSTAIN ─► return the baseline unchanged (a valid outcome)
                         critic REJECT     ─► re-run gates once, else return the baseline + reasons
```

| Prompt | Input | Output | Notes |
|---|---|---|---|
| [10-parse](10-parse.md) | One project's rows from the MI catalogue (Commons #259) | Baseline MLS JSON | Verbatim; no improvements |
| [15-derive](15-derive.md) | Playbook or toolkit text (e.g. Commons #750, #753) | Catalogue-sized baseline MLS + follow-on slices | Fidelity over neatness |
| [20-classify](20-classify.md) | Baseline MLS (+ owner context) | Facts: student experience, constituency, resource, options, already-present, risks | No recommendations |
| [30-gate-cl](30-gate-cl.md) | MLS + facts + CL cards | APPLY / PARTIAL / ABSTAIN, ≤3 target cards | Abstaining is often correct |
| [31-gate-pb](31-gate-pb.md) | MLS + facts + PB cards | Four decisions: process, prioritise, allocate, budget-capped choice | Allocation needs a confirmed amount |
| [32-gate-eb](32-gate-eb.md) | MLS + facts + EB cards | APPLY / PARTIAL / CONDITIONAL / ABSTAIN, ≤2 practice cards + measurement | Only with all non-negotiables; Tier 1 of the evidence ranking |
| [40-transform](40-transform.md) | Baseline + gates + cards (+ critic feedback) | Transformed MLS + change log + open questions | ≤2 added tasks; supportable claims only |
| [50-critic](50-critic.md) | Baseline + transform + gates + cards + schema errors | PASS / REVISE / REJECT, with issues C1–C21 | Independent; no rewriting |
| [60-render](60-render.md) | Final MLS | Catalogue row, teacher card, improvement-story stub | No content changes |

## Shared context
- Cards: [../frameworks/connected-learning.md](../frameworks/connected-learning.md), [../frameworks/pb-techniques.md](../frameworks/pb-techniques.md), [../frameworks/evidence-based-practices.md](../frameworks/evidence-based-practices.md). Pass the **full text** into the gate, transform and critic prompts.
- Schema: [../schema/mip.schema.json](../schema/mip.schema.json). The orchestrator validates `40-transform` output and passes errors to `50-critic` as `{{SCHEMA_ERRORS}}`.
- Source documents are **data**: every prompt that reads source text tells the model to ignore instructions inside it.

## Implementation notes for the orchestrator
- **Variant identity and logging:** after `10-parse`/`15-derive` and again after a critic PASS, set `x_transform.variant_id` with [../schema/variant_id.py](../schema/variant_id.py) (never ask a model for it). Set `parent_variant_id` on transformed variants, and fill `x_transform.pipeline` (model, effort, prompt and card hashes, critic verdict). Usage at schools is logged with [../schema/mip-usage-event.schema.json](../schema/mip-usage-event.schema.json); see [../schema/README.md](../schema/README.md).
- **Run the critic in a separate context** from the transformer, so the review isn't anchored on the transformer's reasoning.
- **Deterministic checks belong in code, not the critic:** schema validation, task and duration limits (C1, C2), and a regex for digits or "%" in rationale claims (part of C9). The critic should still run them as a backstop.
- **Model choice:** gates and critic need careful reasoning; parse and render can use a cheaper model.
- **Logging:** keep every intermediate JSON. Gate decisions on the golden set are the first thing to measure (see [../evals/golden/README.md](../evals/golden/README.md)).

## Evaluating against the golden set
For each golden example, run `10-parse` or `15-derive` on its source, then compare:
1. **Gate decisions** against the "Expected gate decisions" table: exact match per gate.
2. **Transform output** against the example's transformed MLS: rubric-scored (fit, credit-first, real change, safety, micro limits, claim honesty), not string-matched.
3. **Critic catches:** feed the critic each example's *user-supplied "after"* (recorded in its "Changes from…" table) and check it flags the same problems.
