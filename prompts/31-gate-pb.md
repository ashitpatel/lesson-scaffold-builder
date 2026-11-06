# 31 — Gate: which participatory budgeting techniques apply?

## Role
You decide, separately, four things:
1. whether the work may be **labelled** participatory budgeting (`pb_process`);
2. whether a **prioritisation ballot** helps (`pb_prioritise`);
3. whether a **knapsack allocation** is justified (`pb_allocate`);
4. whether **knapsack reasoning without the PB label** fits (`budget_capped_choice`).

In the catalogue, almost no MLS mentions money, so `pb_allocate` is usually ABSTAIN or CONDITIONAL. Most PB value is in **prioritisation** and **report-back**.

## Inputs
- `{{MLS_JSON}}`
- `{{CLASSIFICATION_JSON}}`
- `{{PB_CARDS}}`: the full text of `frameworks/pb-techniques.md`
- `{{CONTEXT}}` (optional): owner statements, e.g. a confirmed amount

## Decision procedure
1. **`pb_process`** (card `PB-scope`): APPLY only if `constituency.present` and `shared_resource.kind ∈ {money, space, materials}`. The third condition, a public outcome, is met either by the MLS as written or by adding one report-back task (the transformer always adds it). A team dividing its own time → ABSTAIN.
2. **`pb_prioritise`** (card `PB-prioritise`): APPLY if `competing_options.count ≥ 2` (or a task generates several needs or options) **and** `constituency.collective_decision == true`. A decision is **legitimately collective** when it belongs, by role or law, to a group: competing school needs or uses of shared money, space or materials (the Community_Governance_Body, under the RTE Act), or a school-wide or class-wide student choice. This holds **even if the MLS as written has one person deciding**. It is **not** collective when a team or staff group decides about its own work or event, or when an HM chooses specific items within a purpose already agreed (e.g. which library books to buy with a library budget). Otherwise ABSTAIN (a team's own work goes to `budget_capped_choice`, step 4). If `pb_prioritise` is APPLY but `pb_process` is ABSTAIN, the transformer calls it "a class vote" or "a group vote", never "participatory budgeting".
3. **`pb_allocate`** (card `PB-allocate-knapsack`). **Precondition:** someone must vote. If neither `pb_process` nor `pb_prioritise` is APPLY → **ABSTAIN** (a budget ballot needs a group). Otherwise:
   - `amount_confirmed == "yes"` and costed options exceed the amount → **APPLY**;
   - `shared_resource.choice_among_costed_items == true` but `amount_confirmed != "yes"` → **CONDITIONAL**, with `condition`: "Is a discretionary (non-earmarked) amount confirmed, how much, and from what source?". Event logistics and routine running costs don't count;
   - otherwise → **ABSTAIN**.
4. **`budget_capped_choice`** (card `PB-not-pb`): APPLY when there is a hard cap (e.g. the team's own hours) and more options than fit, **but** `pb_process` is ABSTAIN. The transformer must then label it "adapted from knapsack voting", never "participatory budgeting".
5. **Indian Community_Governance_Body context** (card `PB-india-smc`): if the constituency is or includes the Community_Governance_Body, add the constraint "ballots are advisory to Community_Governance_Body agreement (PB-G5)". If students are added as voters, add "student voice is an addition to Community_Governance_Body practice; label it as such".
6. **Mobilisation** (applications to the Gram Panchayat or block, donors): note it if present, and record "not PB; leave as is".

## Output
Return **only**:
```json
{
  "pb_process":           { "decision": "APPLY | ABSTAIN", "reason": "", "cards": ["PB-scope"] },
  "pb_prioritise":        { "decision": "APPLY | ABSTAIN", "reason": "", "cards": ["PB-prioritise"] },
  "pb_allocate":          { "decision": "APPLY | CONDITIONAL | ABSTAIN", "reason": "", "cards": ["PB-allocate-knapsack", "PB-count-greedy"], "condition": "" },
  "budget_capped_choice": { "decision": "APPLY | ABSTAIN", "reason": "", "cards": ["PB-not-pb"] },
  "credit": ["PB-ideas: task 2 already lists needs with evidence"],
  "constraints": ["ballots advisory to Community_Governance_Body agreement (PB-G5)"],
  "relevant_guardrails": ["PB-G1", "PB-G2", "PB-G4"]
}
```

## Anti-patterns (never)
- `pb_allocate = APPLY` without a confirmed, discretionary amount.
- `pb_process = APPLY` for a single team's internal planning.
- `pb_allocate` APPLY or CONDITIONAL when no group decides (neither `pb_process` nor `pb_prioritise` is APPLY).
- A CONDITIONAL budget question for event logistics or routine costs.
- Attributing Equal Shares to Stanford.
