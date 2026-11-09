# SPDX-License-Identifier: Apache-2.0
"""Locale handling: strip to generic, keep the source's locale, or relocalize.

The pipeline strips locale-specific content by default: places and polities,
subject and strand names, everyday objects that vary by locale, and stories
with cultural or religious weight. The user may instead keep the source's
locale, or strip and then relocalize: the run logs every removed item, proposes
an equivalent in the user's target locale, and applies only what the user
reviews.
"""

from __future__ import annotations

from typing import Any

from lsb import ask

MODES = ("strip", "keep", "relocalize")

GENERIC_RULE = ("Generic labels: use context-neutral names (e.g. `Community_Governance_Body`, "
                '"the local market", "a nearby clinic"), not names of specific countries, laws, '
                "agencies, programmes or currencies.")
KEEP_RULE = ("Keep the source's locale: keep place and polity names, subject names, everyday "
             "objects and culturally weighted stories as written; do not replace them with generic "
             "labels. All other constraints still apply.")

GENERIC_SCOPE = "Locale scope: `generic`. G09 applies: flag region-specific entities."
KEPT_SCOPE = ("Locale scope: `kept`: the run keeps the source's locale. "
              "Do not file G09 issues for region-specific names; G10 still applies.")


def locale_rule(mode: str) -> str:
    """The {{LOCALE_RULE}} value for prompts/05-decompose.md."""
    return KEEP_RULE if mode == "keep" else GENERIC_RULE


def locale_scope(mode: str, approved: tuple[str, ...] | list[str] = ()) -> str:
    """The {{LOCALE_SCOPE}} value for prompts/50-critic.md.

    `approved` lists relocalized terms the user already reviewed: the critic
    must not file G09 issues for exactly those strings.
    """
    if mode == "keep":
        return KEPT_SCOPE
    scope = GENERIC_SCOPE
    terms = [t for t in approved if isinstance(t, str) and t.strip()]
    if terms:
        scope += (" Approved relocalized terms (reviewed already; do not file G09 issues "
                  f"for exactly these): {'; '.join(terms)}.")
    return scope


def check_locale_log(obj: Any) -> list[str]:
    """Shape-check a 55-locale-log reply: a list of original/generic/category entries."""
    if not isinstance(obj, dict) or not isinstance(obj.get("locale_log"), list):
        return ["output has no 'locale_log' list"]
    problems = []
    for i, e in enumerate(obj["locale_log"]):
        if not isinstance(e, dict):
            problems.append(f"locale_log[{i}] is not an object")
            continue
        for key in ("original", "category"):
            if not isinstance(e.get(key), str) or not e[key].strip():
                problems.append(f"locale_log[{i}] has no {key!r}")
        if "generic" in e and e["generic"] is not None and not isinstance(e["generic"], str):
            problems.append(f"locale_log[{i}] 'generic' is not a string")
        if "drop_reason" in e and e["drop_reason"] not in (None, "locale", "withheld"):
            problems.append(f"locale_log[{i}] 'drop_reason' is not null, 'locale' or 'withheld'")
    return problems


def check_proposals(obj: Any, n_log: int) -> list[str]:
    """Shape-check a 56-relocalize reply against its locale log."""
    if not isinstance(obj, dict) or not isinstance(obj.get("proposals"), list):
        return ["output has no 'proposals' list"]
    problems = []
    seen = set()
    for p in obj["proposals"]:
        if not isinstance(p, dict):
            problems.append("a proposal is not an object")
            continue
        i = p.get("id")
        if not isinstance(i, int) or not 0 <= i < n_log or i in seen:
            problems.append(f"proposal id {i!r} is not a fresh locale-log index")
            continue
        seen.add(i)
        if not isinstance(p.get("proposed"), str) or not p["proposed"].strip():
            problems.append(f"proposal {i} has no 'proposed' text")
    return problems


def check_additions(obj: Any) -> list[str]:
    """Shape-check a 57-locale-add reply: unit/step/anchor/addition entries."""
    if not isinstance(obj, dict) or not isinstance(obj.get("additions"), list):
        return ["output has no 'additions' list"]
    problems = []
    for n, a in enumerate(obj["additions"]):
        if not isinstance(a, dict):
            problems.append(f"additions[{n}] is not an object")
            continue
        if not isinstance(a.get("unit"), str) or not a["unit"].strip():
            problems.append(f"additions[{n}] has no 'unit' id")
        if not isinstance(a.get("step"), int):
            problems.append(f"additions[{n}] has no 'step' number")
        for key in ("anchor", "addition"):
            if not isinstance(a.get(key), str) or not a[key].strip():
                problems.append(f"additions[{n}] has no {key!r}")
    return problems


def addition_choices(additions: list[dict]) -> list[ask.Choice]:
    """One approve/skip-or-own-text choice per locale addition, for the ask layer."""
    choices = []
    for n, a in enumerate(additions):
        where = f"{a['unit']} step {a['step']}"
        addition = a["addition"]
        context = (f"After: {a['anchor']}\n"
                   f"Why this fits {a.get('reason', 'your locale')}")
        choices.append(ask.Choice(
            f"locale_add_{n}", f"Add locale detail to {where}?",
            ((addition, f"Add '{addition}'", ""),
             ("", "Skip", "leave as is")),
            addition, free_text=True, context=context))
    return choices


def apply_additions(sequence: dict, additions: list[dict],
                    decisions: dict[int, str]) -> tuple[dict, list[str]]:
    """Insert approved additions after their anchors in task actions.

    Returns (sequence, notes). Only non-empty decisions whose unit, step and
    anchor are all found are applied, after the anchor's first occurrence.
    Anything missing is reported, never guessed at. Inputs are not mutated.
    """
    import copy

    out = copy.deepcopy(sequence)
    notes = []
    units = {u.get("mls_id"): u for u in out.get("mls_units", []) if isinstance(u, dict)}
    for n, a in enumerate(additions):
        want = decisions.get(n, "")
        if not want:
            continue
        unit = units.get(a.get("unit"))
        if unit is None:
            notes.append(f"locale addition {n}: unit {a.get('unit')!r} not found, skipped")
            continue
        task = next((t for t in (unit.get("tasks") or [])
                     if isinstance(t, dict) and t.get("step") == a.get("step")), None)
        if task is None:
            notes.append(f"locale addition {n}: {a.get('unit')} step {a.get('step')} not found, skipped")
            continue
        action = task.get("action") or ""
        anchor = a.get("anchor") or ""
        if not anchor or anchor not in action:
            notes.append(f"locale addition {n}: anchor not found in {a.get('unit')} step {a.get('step')}, skipped")
            continue
        if anchor[-1].isalnum() and want[0].isalnum():
            want = " " + want
        task["action"] = action.replace(anchor, anchor + want, 1)
        notes.append(f"locale addition {n}: added to {a.get('unit')} step {a.get('step')}")
    return out, notes


def review_choices(proposals: list[dict], log: list[dict]) -> list[ask.Choice]:
    """One approve/skip-or-own-text choice per proposal, for the ask layer."""
    choices = []
    for p in proposals:
        entry = log[p["id"]]
        original = entry.get("original", "")
        generic = entry.get("generic") or "(dropped)"
        proposed = p["proposed"]
        context = (f"Removed: {original}\nNow reads: {generic}\n"
                   f"Why this fits {p.get('reason', 'your locale')}")
        choices.append(ask.Choice(
            f"locale_{p['id']}", f"Relocalize '{original}'?",
            ((proposed, f"Use '{proposed}'", ""),
             ("", "Skip", "leave the generic wording")),
            proposed, free_text=True, context=context))
    return choices


def apply_locale(sequence: dict, log: list[dict], decisions: dict[int, str],
               assumptions: list[dict] | None = None) -> tuple[dict, list[dict] | None, list[str]]:
    """Replace approved generics with the reviewed terms.

    Returns (sequence, assumptions, notes). Only non-empty decisions whose
    generic text is found are applied, in task actions and condition/fallback
    texts. Anything missing is reported, never guessed at. Inputs are not
    mutated.
    """
    import copy

    out = copy.deepcopy(sequence)
    out_a = copy.deepcopy(assumptions) if assumptions is not None else None
    notes = []
    for i, entry in enumerate(log):
        want = decisions.get(i, "")
        if not want:
            continue
        generic = entry.get("generic") or ""
        if not generic:
            notes.append(f"locale {i} ({entry.get('original')}): dropped in the sequence, nothing to replace")
            continue
        hits = 0
        for u in out.get("mls_units", []):
            for t in (u.get("tasks") or []):
                if generic in (t.get("action") or ""):
                    t["action"] = t["action"].replace(generic, want)
                    hits += 1
        for a in out_a or []:
            for key in ("assumes", "if_not"):
                if generic in (a.get(key) or ""):
                    a[key] = a[key].replace(generic, want)
                    hits += 1
        if hits:
            notes.append(f"locale {i}: '{generic}' -> '{want}' ({hits} place(s))")
        else:
            notes.append(f"locale {i} ({entry.get('original')}): '{generic}' not found, left generic")
    return out, out_a, notes


def output_language(value: Any) -> str | None:
    """Normalize an output-language answer; blank or English means no translation."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or text.lower() in ("en", "english"):
        return None
    return text


def check_translation(before_seq: dict, before_assump: list,
                      after: Any) -> list[str]:
    """Shape-check a 59-translate reply against the English sequence.

    Only teacher-facing prose may differ (objective, titles, alignments,
    actions, condition/fallback texts). Structure, ids, roles, numbers, and
    anything emptied are problems.
    """
    if not isinstance(after, dict) or not isinstance(after.get("sequence"), dict):
        return ["output has no 'sequence' object"]
    if not isinstance(after.get("assumptions"), list):
        return ["output has no 'assumptions' list"]
    problems = []
    seq = after["sequence"]
    if not isinstance(seq.get("macro_objective"), str) or not seq["macro_objective"].strip():
        problems.append("macro_objective is missing or empty")
    if seq.get("global_context") != (before_seq.get("global_context") or {}):
        problems.append("global_context changed; only prose is translated")
    before_units = before_seq.get("mls_units") or []
    units = seq.get("mls_units")
    if not isinstance(units, list) or [u.get("mls_id") for u in units if isinstance(u, dict)] != \
            [u.get("mls_id") for u in before_units]:
        return problems + ["units changed; translate the same units in the same order"]
    for b, u in zip(before_units, units):
        uid = b.get("mls_id")
        if u.get("dependencies") != b.get("dependencies") or \
                u.get("duration_weeks") != b.get("duration_weeks"):
            problems.append(f"{uid}: dependencies or weeks changed")
        for key in ("title", "macro_alignment"):
            if b.get(key) and (not isinstance(u.get(key), str) or not u[key].strip()):
                problems.append(f"{uid}: {key} emptied")
        before_tasks = b.get("tasks") or []
        tasks = u.get("tasks")
        if not isinstance(tasks, list) or len(tasks) != len(before_tasks):
            problems.append(f"{uid}: tasks changed; translate the same steps in order")
            continue
        for bt, t in zip(before_tasks, tasks):
            if not isinstance(t, dict) or t.get("step") != bt.get("step") or \
                    t.get("role") != bt.get("role"):
                problems.append(f"{uid}: a step number or role changed")
                continue
            if bt.get("action") and (not isinstance(t.get("action"), str) or not t["action"].strip()):
                problems.append(f"{uid} step {bt.get('step')}: action emptied")
    before_assump = before_assump or []
    assumptions = after["assumptions"]
    if [a.get("mls_id") for a in assumptions if isinstance(a, dict)] != \
            [a.get("mls_id") for a in before_assump]:
        problems.append("assumptions changed; translate the same entries in the same order")
    else:
        for b, a in zip(before_assump, assumptions):
            for key in ("assumes", "if_not"):
                if b.get(key) and (not isinstance(a.get(key), str) or not a[key].strip()):
                    problems.append(f"{b.get('mls_id')}: {key} emptied")
    return problems
