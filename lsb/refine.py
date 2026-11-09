"""Multi-turn refinement: revise a finished run's cards over sessions and days.

A teacher points this at a past run folder plus their source lesson, gives a
follow-up instruction ("we have no garden", "periods are 30 minutes, not 45"),
and gets a new numbered revision: the revised sequence, re-rendered cards, and
a record of what changed. Each run stays valid input indefinitely, so tweaks
accumulate across days; --base replays from any earlier revision.

Scope in v1 is step-level tweaks: task wording and matching assumption lines.
Units, steps, titles, dependencies, weeks and roles never change, so every
revision reuses the run's trace and optimisation record. The revision format
carries a kind field so structural edits can follow later.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from lsb import render, run
from lsb import validate as v

REFINE = "58-refine.md"
FORMAT = 1


def _load_json(path: Path, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as e:
        raise SystemExit(f"cannot read {what} {path}: {e}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"cannot parse {what} {path}: {e}")


def list_revisions(run_dir: Path) -> list[int]:
    revs = run_dir / "revisions"
    if not revs.is_dir():
        return []
    out = []
    for child in revs.iterdir():
        if child.is_dir() and child.name.startswith("rev") and child.name[3:].isdigit():
            if (child / "sequence.json").exists():
                out.append(int(child.name[3:]))
    return sorted(out)


def load_base(run_dir: Path, base: int | None) -> tuple[dict, list, dict, list, str, str]:
    """Return (sequence, assumptions, choices, trace, label, ref) for a base.

    base 0 is the original run; None means the latest revision (or original
    when no revisions exist yet).
    """
    if not (run_dir / "sequence.json").exists():
        raise SystemExit(f"{run_dir} is not a finished run: no sequence.json")
    choices = _load_json(run_dir / "choices.json", "choices") if (run_dir / "choices.json").exists() else {}
    summary = _load_json(run_dir / "summary.json", "summary") if (run_dir / "summary.json").exists() else {}
    trace_p = run_dir / "source_trace.json"
    trace = _load_json(trace_p, "source trace") if trace_p.exists() else []
    ref = str(summary.get("source_ref") or choices.get("ref") or run_dir.name)
    revs = list_revisions(run_dir)
    if base is None:
        base = revs[-1] if revs else 0
    if base == 0:
        seq = _load_json(run_dir / "sequence.json", "sequence")
        dec_p = run_dir / "decomposed-sequence.json"
        assumptions = _load_json(dec_p, "decomposed").get("environment_assumptions", []) if dec_p.exists() else []
        return seq, assumptions, choices, trace, "original", ref
    if base not in revs:
        raise SystemExit(f"{run_dir} has no revision {base} (has: {revs or 'none'})")
    rev_dir = run_dir / "revisions" / f"rev{base}"
    seq = _load_json(rev_dir / "sequence.json", "sequence")
    assump_p = rev_dir / "assumptions.json"
    assumptions = _load_json(assump_p, "assumptions") if assump_p.exists() else []
    return seq, assumptions, choices, trace, f"rev{base}", ref


def check_refinement(before_seq: dict, before_assump: list, after: Any,
                     unit_focus: str | None) -> tuple[list[str], list[list]]:
    """Problems with a 58-refine reply; [] means accepted. Also changed steps.

    Only task action texts (and matching assumption lines) may change. Unit
    ids, order, titles, dependencies, weeks, roles, step counts and step
    numbers are fixed; with a unit focus, other units must be byte-identical.
    """
    if not isinstance(after, dict) or not isinstance(after.get("sequence"), dict):
        return ["output has no 'sequence' object"], []
    new_seq, problems, changed = after["sequence"], [], []
    old_units = before_seq.get("mls_units", [])
    new_units = new_seq.get("mls_units", [])
    if (not isinstance(new_units, list)
            or any(not isinstance(u, dict) for u in new_units)
            or [u.get("mls_id") for u in old_units] != [u.get("mls_id") for u in new_units]):
        return ["units added, removed, reordered or renamed"], []
    for old_u, new_u in zip(old_units, new_units):
        uid = old_u.get("mls_id")
        for key in ("title", "dependencies", "duration_weeks", "weeks", "macro_alignment"):
            if old_u.get(key) != new_u.get(key):
                problems.append(f"{uid}: {key} changed (step-level tweaks only)")
        old_tasks, new_tasks = old_u.get("tasks", []), new_u.get("tasks", [])
        if (not isinstance(new_tasks, list)
                or any(not isinstance(t, dict) for t in new_tasks)
                or [t.get("step") for t in old_tasks] != [t.get("step") for t in new_tasks]):
            problems.append(f"{uid}: steps added, removed or renumbered")
            continue
        for old_t, new_t in zip(old_tasks, new_tasks):
            if old_t.get("role") != new_t.get("role"):
                problems.append(f"{uid} step {old_t.get('step')}: role changed")
            if not isinstance(new_t.get("action"), str) or not new_t["action"].strip():
                problems.append(f"{uid} step {old_t.get('step')}: action missing")
            elif new_t["action"] != old_t.get("action"):
                if unit_focus and unit_focus != "any" and uid != unit_focus:
                    problems.append(f"{uid} step {old_t.get('step')}: outside unit focus {unit_focus}")
                else:
                    changed.append([uid, old_t.get("step")])
    if "assumptions" in after:
        new_assump = after["assumptions"]
        if (not isinstance(new_assump, list)
                or any(not isinstance(a, dict) for a in new_assump)):
            problems.append("'assumptions' is not a list of objects")
        elif [a.get("mls_id") for a in new_assump] != [a.get("mls_id") for a in before_assump]:
            problems.append("assumptions added, removed or reordered")
        else:
            for old_a, new_a in zip(before_assump, new_assump):
                for key in new_a:
                    if key not in ("mls_id", "assumes", "if_not"):
                        problems.append(f"assumption {old_a.get('mls_id')}: field {key!r} added")
    return problems, changed


def _critic_issues(model: run.Model, src_text: str, seq: dict, assumptions: list,
                  trace: list, report: v.Report, mode: str, keep_locale: bool,
                  reply_path: Path) -> tuple[dict, list[dict]]:
    values = run.critic_values(run.Source(text=src_text, ref=""), {"sequence": seq,
                               "source_trace": trace, "environment_assumptions": assumptions},
                               report, None, None, mode, keep_locale)
    system, user, missing = run.build_request(run.CRITIC, values)
    if missing:
        raise SystemExit(f"50-critic.md: no value for {missing}")
    text, usage = model.complete(system, user)
    reply_path.write_text(text, encoding="utf-8")
    critic = run.extract_json(text)
    return critic, run._issues(critic)


def run_revision(src_text: str, run_dir: Path, base_label: str, seq: dict,
                 assumptions: list, choices: dict, trace: list, ref: str,
                 instruction: str, unit: str | None, model: run.Model,
                 rev_num: int) -> dict | None:
    """Apply one teacher instruction; save revisions/revN on success, else None.

    The model reply passes the structure check, the code checks and one critic
    review with a single retry; anything failing leaves the run untouched.
    """
    rev_dir = run_dir / "revisions" / f"rev{rev_num}"
    rev_dir.mkdir(parents=True, exist_ok=True)
    usage: list[dict] = []
    mode = "single" if choices.get("single_module") else "multi"
    keep_locale = choices.get("locale_mode") == "keep"
    previous_output, feedback, critic = "(none)", "(none)", {}
    for attempt in (1, 2):
        values = {"SEQUENCE_JSON": run._dump(seq), "SOURCE_TEXT": src_text,
                  "TEACHER_INSTRUCTION": instruction,
                  "UNIT_FOCUS": unit or "any",
                  "ASSUMPTIONS": run._dump(assumptions) if assumptions else run.NONE,
                  "PREVIOUS_OUTPUT": previous_output, "CRITIC_FEEDBACK": feedback}
        system, user, missing = run.build_request(REFINE, values)
        if missing:
            raise SystemExit(f"{REFINE}: no value for {missing}")
        text, call_usage = model.complete(system, user)
        usage.append({"attempt": attempt, "stage": "refine", **call_usage})
        (rev_dir / f"refine{attempt}.reply.txt").write_text(text, encoding="utf-8")
        try:
            after = run.extract_json(text)
        except run.StageError as e:
            print(f"rev{rev_num}: reply unusable ({e}); run untouched")
            return None
        problems, changed = check_refinement(seq, assumptions, after, unit)
        if problems:
            print(f"rev{rev_num}: {problems[0]}; run untouched")
            return None
        report = v.validate(after["sequence"])
        code_issues = [{"where": i.where, "problem": i.problem, "severity": "blocker"}
                       for c in report.checks for i in c.issues]
        if code_issues:
            issues, verdict = code_issues, "REVISE"
        else:
            critic, issues = _critic_issues(model, src_text, after["sequence"],
                                            after.get("assumptions", assumptions),
                                            trace, report, mode, keep_locale,
                                            rev_dir / f"refine{attempt}-critic.reply.txt")
            (rev_dir / f"refine{attempt}-critic.json").write_text(
                json.dumps(critic, ensure_ascii=False, indent=2), encoding="utf-8")
            verdict = critic.get("verdict", "REJECT")
        if not issues and verdict == "PASS":
            new_seq = after["sequence"]
            new_assump = after.get("assumptions", assumptions)
            summary = _load_json(run_dir / "summary.json", "summary") if (run_dir / "summary.json").exists() else {}
            deck = render.build_deck(new_seq, {"environment_assumptions": new_assump},
                                     summary.get("optimisation"), trace, ref)
            card_problems = render.write_cards(deck, rev_dir)
            (rev_dir / "sequence.json").write_text(json.dumps(new_seq, ensure_ascii=False, indent=2), encoding="utf-8")
            (rev_dir / "assumptions.json").write_text(json.dumps(new_assump, ensure_ascii=False, indent=2), encoding="utf-8")
            record = {"format": FORMAT, "kind": "step-edits", "n": rev_num, "base": base_label,
                      "instruction": instruction, "unit": unit or "any", "changed_steps": changed,
                      "cards_g21": card_problems or "pass", "usage": usage,
                      "note": after.get("note", "") if isinstance(after.get("note"), str) else ""}
            (rev_dir / "revision.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"rev{rev_num}: PASS, {len(changed)} step(s) changed; cards in {rev_dir}")
            return record
        if verdict == "REJECT" or verdict not in run.VERDICTS:
            print(f"rev{rev_num}: critic verdict {verdict}; run untouched")
            return None
        if attempt == 2:
            worst = issues[0] if issues else {}
            print(f"rev{rev_num}: still {worst.get('severity', 'failing')} after retry "
                  f"({worst.get('problem', 'no detail')}); run untouched")
            return None
        previous_output, feedback = text, run._dump(issues)
        print(f"rev{rev_num}: {verdict}, retrying ({len(issues)} issue(s))")
    return None  # unreachable


def _build_model(args) -> run.Model:
    if args.backend == "claude-code":
        return run.ClaudeCodeModel(effort=args.effort, model=args.model or run.MODEL)
    if args.backend == "muse":
        return run.MuseModel(effort=args.effort, model=args.model)
    if args.backend == "gemini":
        return run.GeminiModel(effort=args.effort, model=args.model)
    import anthropic  # noqa: F401  (mirrors run.py; the class imports it too)
    return run.AnthropicModel(effort=args.effort, model=args.model or run.MODEL)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m lsb.refine", description=__doc__.split("\n\n")[0])
    ap.add_argument("source", type=Path, help="text file with the source lesson")
    ap.add_argument("run_dir", type=Path, help="finished run folder to revise")
    ap.add_argument("--instruction", action="append", default=[],
                    help="teacher follow-up (repeatable: one revision each, in order)")
    ap.add_argument("--unit", default=None, metavar="MLS_ID",
                    help="confine edits to one unit (applies to every --instruction turn)")
    ap.add_argument("--base", type=int, default=None, metavar="N",
                    help="revise from revN (0 = original run); default is the latest")
    ap.add_argument("--ask", action="store_true", help="prompt for follow-up turns interactively")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--backend", default="claude-code", choices=["claude-code", "muse", "gemini", "api"])
    ap.add_argument("--model", default=None, help="model id (backend defaults apply)")
    args = ap.parse_args(argv)
    if not args.instruction and not args.ask:
        ap.error("give at least one --instruction or --ask")
    try:
        src_text = args.source.read_text(encoding="utf-8")
    except OSError as e:
        print(f"cannot read source: {e}", file=sys.stderr)
        return 2
    if not args.run_dir.is_dir():
        print(f"not a run folder: {args.run_dir}", file=sys.stderr)
        return 2
    model = _build_model(args)
    failed = False

    def one_turn(instruction: str, unit: str | None, base: int | None) -> None:
        nonlocal failed
        try:
            revs = list_revisions(args.run_dir)
            seq, assumptions, choices, trace, label, ref = load_base(args.run_dir, base)
            record = run_revision(src_text, args.run_dir, label, seq, assumptions,
                                  choices, trace, ref, instruction, unit, model,
                                  (revs[-1] if revs else 0) + 1)
            failed = failed or record is None
        except (run.StageError, run.ModelUnavailable, SystemExit) as e:
            print(f"turn failed ({e}); run untouched")
            failed = True

    first = True
    for instruction in args.instruction:
        one_turn(instruction, args.unit, args.base if first else None)
        first = False
    if args.ask:
        try:
            while True:
                instruction = input("Follow-up tweak (blank to finish): ").strip()
                if not instruction:
                    break
                unit = input("Confine to a unit id (blank for any): ").strip() or None
                one_turn(instruction, unit, args.base if first else None)
                first = False
        except (EOFError, KeyboardInterrupt):
            print()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
