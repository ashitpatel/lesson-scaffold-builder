"""Deterministic half of the optimisation stages: check a per-unit edit, merge it back.

An optimisation stage (prompts/30-connected-learning.md, 31-participatory-budgeting.md) returns one edited unit
plus a change log. Code, not the model, decides whether the edit kept within its
limits: the unit's identity and placement in the DAG are unchanged, no step was
removed or reordered, at most one step was added, and every step that differs
from the original is logged against a card. `merge` puts accepted units back into
the sequence, and `unit_trace` rebuilds the source trace so every step still
points at the source section or card it comes from.
"""

from __future__ import annotations

import copy
from typing import Any

CL_CARDS = ("CL-01", "CL-02", "CL-03", "CL-04", "CL-05")
PB_CARDS = ("PB-01", "PB-02", "PB-03", "PB-04", "PB-05")
FIXED_FIELDS = ("mls_id", "title", "dependencies", "macro_alignment", "duration_weeks")
DECISIONS = ("APPLY", "ABSTAIN")
MAX_ADDED_STEPS = 1
MAX_CARDS = 2


def _key(task: Any) -> tuple | None:
    if isinstance(task, dict) and isinstance(task.get("action"), str):
        return task.get("role"), task["action"]
    return None


def match_steps(before: dict, after: dict) -> list[int | None]:
    """For each step of `after`, the 0-based index of the identical original step, or None.

    Originals are matched in order, each at most once.
    """
    originals = [_key(t) for t in before.get("tasks", [])]
    used: set[int] = set()
    out: list[int | None] = []
    for task in after.get("tasks", []):
        k = _key(task)
        hit = next((i for i, o in enumerate(originals) if i not in used and k is not None and o == k), None)
        if hit is not None:
            used.add(hit)
        out.append(hit)
    return out


def check_unit_edit(before: dict, result: Any, cards: tuple[str, ...] = CL_CARDS) -> list[str]:
    """Problems with an optimisation stage's output for one unit; [] means accepted."""
    if not isinstance(result, dict):
        return ["output is not a JSON object"]
    problems: list[str] = []
    uid = before.get("mls_id")
    if result.get("mls_id") != uid:
        problems.append(f"mls_id is {result.get('mls_id')!r}; expected {uid!r}")
    decision = result.get("decision")
    if decision not in DECISIONS:
        problems.append(f"decision {decision!r} is not one of {', '.join(DECISIONS)}")
    after = result.get("unit")
    changes = result.get("changes")
    if not isinstance(after, dict):
        return problems + ["'unit' is not an object"]
    if not isinstance(changes, list) or not all(isinstance(c, dict) for c in changes):
        return problems + ["'changes' is not a list of objects"]

    for f in FIXED_FIELDS:
        if after.get(f) != before.get(f):
            problems.append(f"unit.{f} changed; it must stay {before.get(f)!r}")

    tasks = after.get("tasks")
    if not isinstance(tasks, list) or not all(_key(t) for t in tasks):
        return problems + ["unit.tasks is not a list of steps with a role and an action"]

    if decision == "ABSTAIN":
        if after.get("tasks") != before.get("tasks"):
            problems.append("decision is ABSTAIN but the steps changed")
        if changes:
            problems.append("decision is ABSTAIN but 'changes' is not empty")
        return problems

    n_before = len(before.get("tasks", []))
    added = len(tasks) - n_before
    if added < 0:
        problems.append(f"{-added} step(s) removed; optimisation never removes a step")
    elif added > MAX_ADDED_STEPS:
        problems.append(f"{added} steps added; at most {MAX_ADDED_STEPS} may be added")

    used_cards = {c.get("card") for c in changes}
    unknown = sorted(str(c) for c in used_cards if c not in cards)
    if unknown:
        problems.append(f"unknown card(s) {', '.join(unknown)}; use one of {', '.join(cards)}")
    if len(used_cards) > MAX_CARDS:
        problems.append(f"{len(used_cards)} cards applied; at most {MAX_CARDS}")
    if decision == "APPLY" and not changes:
        problems.append("decision is APPLY but 'changes' is empty")

    matched = match_steps(before, after)
    logged: dict[int, dict] = {}
    for c in changes:
        step = c.get("step")
        if not isinstance(step, int) or not 1 <= step <= len(tasks):
            problems.append(f"change entry for step {step!r}, which is not a step of the unit")
        elif step in logged:
            problems.append(f"step {step} has more than one change entry")
        else:
            logged[step] = c

    origin: list[int] = []  # original index each step stands for, to check order
    replaced: set[int] = set()
    n_added = 0
    for pos, hit in enumerate(matched, start=1):
        entry = logged.get(pos)
        if hit is not None:
            if entry is not None:
                problems.append(f"step {pos} is an exact copy of original step {hit + 1} but has a change entry")
            origin.append(hit)
            continue
        if entry is None:
            problems.append(f"step {pos} differs from every original step but has no change entry")
            continue
        kind = entry.get("change")
        if kind == "added":
            n_added += 1
        elif kind == "modified":
            r = entry.get("replaces_step")
            if not isinstance(r, int) or not 1 <= r <= n_before:
                problems.append(f"step {pos} is modified but replaces_step {r!r} is not an original step")
            elif r - 1 in matched or r - 1 in replaced:
                problems.append(f"step {pos} says it replaces original step {r}, which is kept or already replaced")
            else:
                replaced.add(r - 1)
                origin.append(r - 1)
        else:
            problems.append(f"step {pos}: change {kind!r} is not 'added' or 'modified'")

    if n_added > MAX_ADDED_STEPS:
        problems.append(f"{n_added} steps logged as added; at most {MAX_ADDED_STEPS}")
    kept = {i for i in matched if i is not None} | replaced
    for i in range(n_before):
        if i not in kept and added >= 0:
            problems.append(f"original step {i + 1} is neither kept nor replaced")
    if origin != sorted(origin):
        problems.append("original steps were reordered; keep their order and insert any new step between them")
    for pos, task in enumerate(tasks, start=1):
        if task.get("step") != pos:
            problems.append(f"steps must be numbered 1..{len(tasks)} in order; position {pos} is {task.get('step')!r}")
            break
    return problems


def unit_trace(before: dict, result: dict, trace: list[dict]) -> list[dict]:
    """The source trace for an accepted unit, renumbered, with card ids on changed steps."""
    uid = before.get("mls_id")
    by_step: dict[Any, list[dict]] = {}
    for e in trace:
        if isinstance(e, dict) and e.get("mls_id") == uid:
            by_step.setdefault(e.get("step"), []).append(e)
    after = result["unit"]
    logged = {c.get("step"): c for c in result.get("changes", []) if isinstance(c, dict)}
    out: list[dict] = []
    for pos, hit in enumerate(match_steps(before, after), start=1):
        entry = logged.get(pos, {})
        orig = hit + 1 if hit is not None else entry.get("replaces_step")
        for e in by_step.get(orig, []) if orig is not None else []:
            out.append({**e, "step": pos})
        if hit is None:
            out.append({"mls_id": uid, "step": pos, "card": entry.get("card"), "change": entry.get("change")})
    return out


def merge(sequence: dict, units: dict[str, dict]) -> dict:
    """A copy of `sequence` with each unit whose mls_id is in `units` replaced."""
    out = copy.deepcopy(sequence)
    out["mls_units"] = [copy.deepcopy(units.get(u.get("mls_id"), u)) for u in out.get("mls_units", [])]
    return out


def merge_trace(trace: list[dict], unit_traces: dict[str, list[dict]]) -> list[dict]:
    """`trace` with the entries of each re-traced unit replaced."""
    kept = [e for e in trace if not (isinstance(e, dict) and e.get("mls_id") in unit_traces)]
    return kept + [e for entries in unit_traces.values() for e in entries]
