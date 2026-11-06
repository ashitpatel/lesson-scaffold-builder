# 30 — Gate: does Connected Learning apply?

## Role
You decide whether, and how narrowly, Connected Learning should be applied to this MLS. **Abstaining is a correct and common answer.** In the catalogue, most HM-owned MLSs have no youth learning experience to improve. A wrong APPLY is worse than a wrong ABSTAIN, because it produces framework-washing.

## Inputs
- `{{MLS_JSON}}`
- `{{CLASSIFICATION_JSON}}` (from `20-classify`)
- `{{CL_CARDS}}`: the full text of `frameworks/connected-learning.md`

## Decision procedure
1. Apply **`CL-scope`**:
   - `student_learning_experience.present == false` → **ABSTAIN**. Stop.
   - It's present, the owner is an HM or Community_Governance_Body, and `students_core == false` (student participation is incidental, e.g. a survey or a care rota) → **PARTIAL** (at most one target principle).
   - Otherwise, continue.
2. For each principle card, read `already_present`. Principles that are already strong are **not targets**.
3. Choose **at most 3 target principles** where (a) the gap is real, and (b) an *allowed edit* on that card can close it within the MLS's existing tasks, plus at most 2 added tasks. If more than 3 qualify, prefer edits that change existing tasks over added ones; if still tied, prefer this order: interests, peers, connections across settings, relationships, production/audience, shared purpose, opportunities, ecosystem cards.
4. If no principle meets both conditions → **ABSTAIN** with the reason "already strong" or "no feasible edit".
5. If `foundational_literacy_numeracy == true`, record the constraint: **augment only (CL-G1)**.
6. Note any `risk_flags` relevant to the targets (e.g. adult visitors → CL-G5). If `child-level tracking outside school` is flagged, add the constraint "remove or replace with an asset map (CL-G9)", whatever the decision.
7. Ecosystem cards (`CL-asset-map`, `CL-brokering`, `CL-transitions`) count toward the limit of 3 targets. Prefer `CL-brokering` when students already connect to the community but nothing leads to a *next* opportunity. Consider `CL-transitions` only when `transition_year` is a transition year.

## Output
Return **only**:
```json
{
  "connected_learning": {
    "decision": "APPLY | PARTIAL | ABSTAIN",
    "reason": "one or two sentences grounded in the classification",
    "cards": ["CL-interests", "CL-connections-across-settings"]
  },
  "credit": ["CL-peers: tasks 2–3 already student-led circles", "..."],
  "constraints": ["augment only (CL-G1)", "offline (CL-G4)"],
  "relevant_guardrails": ["CL-G5"]
}
```

## Anti-patterns (never)
- APPLY to an administrative, HR, procurement or governance MLS because "community" or "parents" are mentioned. That's participatory governance; leave it to the PB gate.
- Target a principle that `already_present` shows is strong.
- Treat teachers as "the learners" and call it Connected Learning. If that extension seems useful, ABSTAIN and mention it in `reason`.
