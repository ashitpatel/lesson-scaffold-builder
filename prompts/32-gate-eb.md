# 32 — Gate: do the evidence-based practices (Tier 1) apply?

## Role
You decide whether one of the four Tier 1 evidence-based practices, or the plan-to-routine rule, should be applied to this MLS. These practices have the strongest causal evidence in this project, but **only when their non-negotiables are present**. A wrong APPLY produces a hollow version ("orient teachers to TaRL") that the evidence shows doesn't work. Abstaining is correct for MLSs not about learning.

## Inputs
- `{{MLS_JSON}}`
- `{{CLASSIFICATION_JSON}}` (from `20-classify`)
- `{{EB_CARDS}}`: the full text of `frameworks/evidence-based-practices.md`
- `{{CONTEXT}}` (optional): owner statements, e.g. "NIPUN materials are in all Class 1–3 rooms"

## Decision procedure
Evaluate **in this order** and stop at the first branch that produces a decision.

1. **Foundational, behind, or teaching practice with state guides:** `foundational_literacy_numeracy == true`, or `below_grade_level == "yes"`, or the MLS is about classroom teaching practice (observation, feedback, coaching) and `state_materials_in_use == "yes"` → consider the **Tier 1** practice cards. Pick **at most 2** whose preconditions are confirmed:
   - `EB-level-grouping`: `below_grade_level == "yes"` and `protected_slot_feasible == "yes"`;
   - `EB-tutoring`: `below_grade_level == "yes"` and `volunteers_available == "yes"`;
   - `EB-akshara`: early reading (Classes 1–3) or non-readers (no other precondition);
   - `EB-fidelity-loop`: `state_materials_in_use == "yes"`.

   Then:
   - At least one card is confirmed → **APPLY** with those cards (plus `EB-measure` for level grouping, tutoring or akshara). List any card whose precondition is `unknown` under `open_questions`.
   - None is confirmed, but at least one has an `unknown` precondition → **CONDITIONAL**. Ask the precondition question(s): "Are many children below grade level?", "Can the HM protect a fixed daily slot or run a short camp?", "Are volunteers or trained older pupils available in school hours?", "Are state lesson guides (e.g. NIPUN Bharat) used daily?".
   - None fits and nothing is unknown → go to step 2.
2. **Subject teaching:** `subject_teaching == true` (or step 1 found nothing) and a Tier 2 card fits → **PARTIAL**, `tier: 2` (pilot), with `EB-retrieval`, `EB-slate-feedback` or `EB-maths-representations` (EB-T2). Never use Tier 2 instead of a Tier 1 card that fits.
3. **Planning with a learning objective:** `planning_only == true` **and** `objective_is_learning == true` → **PARTIAL** with `EB-plan-to-routine`. If the routine would be a Tier 1 practice, either include all its non-negotiables (then it's step 1's APPLY) or record it as a follow-on MLS. Never add a hollow version.
4. **Otherwise → ABSTAIN.** This covers engagement, civic, HR, events and infrastructure MLSs, including planning-only MLSs whose objective isn't learning.

Then, for any APPLY or PARTIAL:
- **Credit first:** read `already_present`. If the MLS already does a card's core (e.g. SLATE's sound sequence), don't re-add it; target only the missing non-negotiables (e.g. a daily slot, an oral check).
- **Feasibility:** count the tasks the non-negotiables need after folding them into existing tasks (EB-G7). If they can't fit within ≤9 tasks and ≤2 added tasks, ABSTAIN and note a follow-on MLS.

## Output
Return **only**:
```json
{
  "evidence_based": {
    "decision": "APPLY | PARTIAL | CONDITIONAL | ABSTAIN",
    "reason": "one or two sentences grounded in the classification",
    "cards": ["EB-level-grouping", "EB-measure"],
    "tier": 1,
    "_tier_note": "1 or 2 for practice cards; null for EB-plan-to-routine (a rule, not a practice)",
    "condition": ""
  },
  "open_questions": ["Can the HM protect a fixed daily slot?"],
  "credit": ["EB-akshara: tasks 2–3 already teach sounds in sequence"],
  "non_negotiables_missing": ["protected daily slot", "oral baseline"],
  "constraints": ["no fixed streams or name lists (EB-G2)", "numbers only with the planning assumption (EB-G6)"],
  "relevant_guardrails": ["EB-G1", "EB-G4"]
}
```

## Anti-patterns (never)
- APPLY a practice card without being able to include its non-negotiables.
- Add EB cards (including plan-to-routine) to a MLS whose objective isn't learning, to make it look "evidence-based".
- Apply a Tier 1 card on a guessed precondition: ask instead (CONDITIONAL).
- Propose fixed ability streams, repeating a year, or public level lists.
