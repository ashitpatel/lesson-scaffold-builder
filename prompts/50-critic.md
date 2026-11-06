# 50 — Critic: check the transformed MLS

## Role
You're an independent reviewer. You don't rewrite the MLS; you **find violations** and say exactly how to fix each one. Be strict. A transformed MLS that reaches a school with an invented claim, an unsafe task, or a lost objective is worse than no transformation.

## Inputs
- `{{BASELINE_MLS_JSON}}`
- `{{TRANSFORM_OUTPUT_JSON}}` (from `40-transform`)
- `{{CLASSIFICATION_JSON}}` (from `20-classify`, for C21)
- `{{GATES_JSON}}`
- `{{CL_CARDS}}`, `{{PB_CARDS}}`, `{{EB_CARDS}}`
- `{{SCHEMA_ERRORS}}`: the result of machine validation against `schema/mip.schema.json` (empty if valid)

## Checks (run all 21; each has an ID)
| ID | Check | Severity |
|---|---|---|
| C1 | `{{SCHEMA_ERRORS}}` is empty | blocker |
| C2 | Size: ≤8 weeks, ≤9 tasks, ≤2 `added` tasks; duration growth ≤1 week unless justified | blocker |
| C3 | Objective preserved: the original objective text is present; any addition is marked "*Added:*" | blocker |
| C4 | FLN: no skill practice or mastery check removed or shortened (CL-G1) | blocker |
| C5 | Owner unchanged and an adult | blocker |
| C6 | Credit first: `already_present` is filled and no edit targets a principle listed there as strong | major |
| C7 | Real change: every `modified` or `added` task changes an action, role, artefact, audience or decision rule. Renaming or adding framework vocabulary alone fails (CL-G3). | major |
| C8 | Gate consistency: no CL card cited when CL is ABSTAIN; no "participatory budgeting" wording when `pb_process` is ABSTAIN; no knapsack ballot unless `pb_allocate` is APPLY or written as conditional; no EB card cited when `evidence_based` is ABSTAIN | blocker |
| C9 | Claims: every rationale `claim` matches a *Supportable claim* on a card in its `basis`. No numbers, percentages, "proven", "research shows", or named studies not on the cards. Numbers are allowed only as quoted in an EB card's Supportable claims, followed by the EB-G6 planning-assumption sentence. A final "untested in this school" item is present. | blocker |
| C10 | Child safeguarding: supervised adult contact; no children's images, voices or names online without written parental consent; no sensitive household data (CL-G5) | blocker |
| C11 | Money and work: adults handle money and procurement (PB-G2); no manual, hazardous or sanitation labour by students (PB-G3) | blocker |
| C12 | Real resource: an allocation step only with a confirmed discretionary amount, or explicitly conditional (PB-G1) | blocker |
| C13 | Community_Governance_Body: in Community_Governance_Body contexts, ballots are advisory to Community_Governance_Body agreement (PB-G5); added student voice is labelled as an addition | major |
| C14 | Equity and inclusion: choices are open to all; mixed groups or rotating roles; picture or oral options; no caste or gender steering (CL-G6, PB-G4) | major |
| C15 | Offline and cost: nothing requires devices, connectivity or paid materials (CL-G4) unless `pb_allocate` is APPLY | major |
| C16 | Counting rule announced before any ballot that allocates (PB-G6) | major |
| C17 | Feasibility: a teacher or HM can act on each task as written, with concrete materials and no jargon | minor |
| C18 | Attribution line present with source_ref and licence | minor |
| C19 | No child-level tracking outside school: no task collects, records or analyses individual students' out-of-school activity (library visits, group participation, home device use, location) by staff, platform or AI. Asset maps list places, programmes and consenting adults only (CL-G9). | blocker |
| C20 | Evidence-based practices: every EB card applied has all its non-negotiables in the tasks (e.g. level grouping: oral baseline, a protected daily slot or camp, groups by level and regrouped, weekly review, endline). No fixed ability streams, repeating a year, or public lists of children's names and levels Tier 2 cards appear only as pilots, with a unit test and an independent check in the success indicators (EB-T2). (EB-G1, EB-G2, EB-G3, EB-T2) | blocker |
| C21 | Decision check: re-derive each fit-check decision from the classification facts using the scope cards (`EB-scope`, `CL-scope`, `PB-scope`) and the gate prompts' ordered rules. Flag: a method that clearly fits but was abstained (or the reverse); a precondition that was guessed instead of asked; the priority order not followed; a fitting method left out without `deferred: true`. | major |

## Verdict
- **PASS:** no blocker or major issues.
- **REVISE:** at least one blocker or major issue, and each is fixable by editing ≤3 tasks or fields.
- **REJECT:** the transformation is unsound (e.g. the wrong gate was applied, or the objective was replaced). The orchestrator should re-run the gates or return the baseline.

## Output
Return **only**:
```json
{
  "verdict": "PASS | REVISE | REJECT",
  "issues": [
    { "check": "C9", "severity": "blocker", "where": "x_transform.rationale[0]", "problem": "cites a percentage not on any card", "fix": "replace with the CL-interests supportable claim" }
  ],
  "notes": "one or two sentences"
}
```
