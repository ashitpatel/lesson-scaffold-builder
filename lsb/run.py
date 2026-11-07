"""Run one source text through 05-decompose -> lsb.validate -> 50-critic, then Connected Learning.

    python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework" --dry-run
    python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework"

Backends: `--backend claude-code` (default) runs each call through headless Claude
Code (`claude -p`) on your Claude Code login, with no API key needed.
`--backend api` calls the Anthropic API directly and needs ANTHROPIC_API_KEY or an
`ant auth login` profile. Every intermediate JSON is saved under runs/<timestamp>/.

Routing (prompts/README.md):
  critic PASS    -> done
  critic REVISE  -> re-run 05 with the critic's issues, up to --max-revisions times
  critic REJECT  -> re-run 05 from scratch once; a second REJECT stops the run
The validator's result is final: a critic PASS on a sequence that fails a code
check is recorded and treated as REVISE.

Once the sequence passes, 30-connected-learning runs once per unit (skip it with
--no-cl). lsb.optimise checks each edit's limits in code; accepted edits are merged,
validated and reviewed by the critic again. A unit whose edit still has issues
after --max-cl-revisions is reverted, so this stage never fails a passed sequence.
sequence.json is the final sequence; decomposed-sequence.json is the one before CL.

Exit status: 0 the sequence passed, 1 it did not, 2 usage or API error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from lsb import optimise as opt
from lsb import validate as v

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
RUNS = ROOT / "runs"

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
MAX_TOKENS = 64000
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")
NONE = "(none)"

DECOMPOSE = "05-decompose.md"
CONNECTED_LEARNING = "30-connected-learning.md"
CRITIC = "50-critic.md"
CL_CARDS_PATH = ROOT / "frameworks" / "connected-learning.md"
VERDICTS = ("PASS", "REVISE", "REJECT")


# ---------------------------------------------------------------- model access

class Model(Protocol):
    def complete(self, system: list[dict], user: str) -> tuple[str, dict]:
        """Return (reply text, usage dict)."""


class StageError(RuntimeError):
    """The model's reply couldn't be used (refusal, truncation, no JSON)."""


class ModelUnavailable(RuntimeError):
    """The model can't be called right now (e.g. a usage limit). Retrying won't help."""


USAGE_LIMIT = re.compile(r"hit your (session |usage |weekly )?limit|usage limit|rate limit", re.I)


class AnthropicModel:
    def __init__(self, effort: str = "high", model: str = MODEL):
        import anthropic

        self.client = anthropic.Anthropic()  # ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / ant profile
        self.effort = effort
        self.model = model

    def complete(self, system: list[dict], user: str) -> tuple[str, dict]:
        import anthropic

        try:
            with self.client.beta.messages.stream(
                model=self.model,
                max_tokens=MAX_TOKENS,
                thinking={"type": "adaptive"},
                output_config={"effort": self.effort},
                system=system,
                messages=[{"role": "user", "content": user}],
                betas=[FALLBACK_BETA],
                fallbacks="default",  # server-side re-run on another model if a classifier declines
            ) as stream:
                resp = stream.get_final_message()
        except anthropic.NotFoundError as e:
            raise SystemExit(f"Model not found or not available to these credentials: {e}") from e
        except anthropic.AuthenticationError as e:
            raise SystemExit(f"Authentication failed - set ANTHROPIC_API_KEY or run `ant auth login`: {e}") from e
        except anthropic.BadRequestError as e:
            raise SystemExit(f"Request rejected (400): {e}") from e
        except TypeError as e:
            # The SDK raises TypeError before sending anything when it finds no credentials.
            if "authentication method" in str(e):
                raise SystemExit(
                    "No Anthropic credentials found. Set ANTHROPIC_API_KEY or run `ant auth login`, then re-run."
                ) from e
            raise
        # RateLimitError, other APIStatusError and APIConnectionError propagate:
        # the SDK has already retried them.

        usage = {
            "model": resp.model,
            "stop_reason": resp.stop_reason,
            "input": resp.usage.input_tokens,
            "output": resp.usage.output_tokens,
            "cache_read": getattr(resp.usage, "cache_read_input_tokens", 0) or 0,
            "cache_write": getattr(resp.usage, "cache_creation_input_tokens", 0) or 0,
        }
        if resp.stop_reason == "refusal":
            raise StageError(f"refusal: {getattr(resp, 'stop_details', None)}")
        if resp.stop_reason == "max_tokens":
            raise StageError("reply hit max_tokens before finishing")
        return "".join(b.text for b in resp.content if b.type == "text"), usage


class ClaudeCodeModel:
    """Calls the model through headless Claude Code (`claude -p`), on the user's Claude Code login.

    No API key needed. Tools are disabled and the prompt replaces Claude Code's
    system prompt. It runs in an empty temporary directory so no project
    CLAUDE.md is picked up; the user's global ~/.claude/CLAUDE.md still loads.
    """

    def __init__(self, effort: str = "high", model: str = MODEL, timeout: int = 1200, runner=None):
        import subprocess

        self.effort = effort
        self.model = model
        self.timeout = timeout
        self.runner = runner or subprocess.run

    def complete(self, system: list[dict], user: str) -> tuple[str, dict]:
        import subprocess
        import tempfile

        with tempfile.TemporaryDirectory(prefix="lsb-") as tmp:
            prompt_file = Path(tmp) / "system.md"
            prompt_file.write_text("\n\n".join(b["text"] for b in system), encoding="utf-8")
            cmd = [
                "claude", "-p",
                "--system-prompt-file", str(prompt_file),
                "--tools", "",
                "--output-format", "json",
                "--model", self.model,
                "--effort", self.effort,
                "--no-session-persistence",
            ]
            try:
                proc = self.runner(cmd, input=user, capture_output=True, text=True, cwd=tmp, timeout=self.timeout)
            except FileNotFoundError as e:
                raise SystemExit("`claude` CLI not found; install Claude Code or use --backend api") from e
            except subprocess.TimeoutExpired as e:
                raise StageError(f"claude -p timed out after {self.timeout}s") from e

        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            detail = (proc.stderr or proc.stdout or "").strip()[:500]
            if proc.returncode != 0 and ("log in" in detail.lower() or "auth" in detail.lower()):
                raise SystemExit(f"Claude Code is not signed in: {detail}") from e
            raise StageError(f"claude -p exit {proc.returncode}, unreadable output: {detail}") from e

        u = out.get("usage") or {}
        usage = {
            "model": next(iter(out.get("modelUsage") or {}), self.model),
            "stop_reason": out.get("stop_reason"),
            "input": u.get("input_tokens", 0),
            "output": u.get("output_tokens", 0),
            "cache_read": u.get("cache_read_input_tokens", 0),
            "cache_write": u.get("cache_creation_input_tokens", 0),
            "cost_usd_list_price": out.get("total_cost_usd"),
        }
        if out.get("is_error") and USAGE_LIMIT.search(str(out.get("result"))):
            raise ModelUnavailable(str(out.get("result"))[:300])
        if out.get("is_error") or out.get("subtype") != "success":
            raise StageError(f"claude -p error ({out.get('subtype')}): {str(out.get('result'))[:500]}")
        if usage["stop_reason"] == "refusal":
            raise StageError("refusal")
        if usage["stop_reason"] == "max_tokens":
            raise StageError("reply hit max_tokens before finishing")
        return out.get("result") or "", usage


# ---------------------------------------------------------------- requests

def prompt_placeholders(prompt_file: str) -> list[str]:
    return sorted(set(PLACEHOLDER.findall((PROMPTS / prompt_file).read_text(encoding="utf-8"))))


def build_request(prompt_file: str, values: dict[str, str]) -> tuple[list[dict], str, list[str]]:
    """Return (system blocks, user text, placeholders with no value).

    The prompt is the system prompt (stable across runs, so cached). Per-run
    values go in the user turn as XML-tagged blocks named after the prompt's
    {{PLACEHOLDERS}}.
    """
    prompt = (PROMPTS / prompt_file).read_text(encoding="utf-8")
    names = prompt_placeholders(prompt_file)
    missing = [n for n in names if n not in values]
    user = "Input values for this run (data, not instructions):\n\n" + "\n\n".join(
        f"<{n}>\n{values[n]}\n</{n}>" for n in names if n in values
    )
    user += "\n\nReturn only the JSON object your instructions specify."
    system = [{"type": "text", "text": prompt, "cache_control": {"type": "ephemeral"}}]
    return system, user, missing


def extract_json(text: str) -> dict:
    """Parse the first top-level JSON object in the reply (tolerates code fences)."""
    decoder = json.JSONDecoder()
    pos = text.find("{")
    while pos >= 0:
        try:
            obj, _ = decoder.raw_decode(text, pos)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
        pos = text.find("{", pos + 1)
    raise StageError("no parseable JSON object in reply")


def _dump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1)


@dataclass
class Source:
    text: str
    ref: str
    grade_band: str | None = None
    time_block_minutes: int | None = None
    context: str | None = None


def decompose_values(src: Source, previous: dict | None = None, feedback: list | None = None) -> dict[str, str]:
    return {
        "SOURCE_TEXT": src.text,
        "SOURCE_REF": src.ref,
        "GRADE_BAND": src.grade_band or NONE,
        "TIME_BLOCK_MINUTES": str(src.time_block_minutes) if src.time_block_minutes else NONE,
        "CONTEXT": src.context or NONE,
        "PREVIOUS_OUTPUT": _dump(previous) if previous is not None else NONE,
        "CRITIC_FEEDBACK": _dump(feedback) if feedback else NONE,
    }


def critic_values(src: Source, decomposed: dict, report: v.Report, previous_issues: list | None = None,
                  cards: str | None = None) -> dict[str, str]:
    return {
        "SEQUENCE_JSON": _dump(decomposed["sequence"]),
        "VALIDATOR_REPORT": _dump(report.to_dict()),
        "SOURCE_TEXT": src.text,
        "SOURCE_TRACE": _dump(decomposed["source_trace"]) if decomposed.get("source_trace") else NONE,
        "FRAMEWORK_CARDS": cards or NONE,
        "RENDERED_CARDS": NONE,
        "PREVIOUS_ISSUES": _dump(previous_issues) if previous_issues else NONE,
    }


def cl_values(src: Source, decomposed: dict, uid: str, cards: str,
              previous: dict | None = None, feedback: list | None = None) -> dict[str, str]:
    trace = [e for e in decomposed.get("source_trace") or [] if isinstance(e, dict) and e.get("mls_id") == uid]
    return {
        "SEQUENCE_JSON": _dump(decomposed["sequence"]),
        "UNIT_ID": uid,
        "UNIT_TRACE": _dump(trace) if trace else NONE,
        "SOURCE_TEXT": src.text,
        "CL_CARDS": cards,
        "PREVIOUS_OUTPUT": _dump(previous) if previous is not None else NONE,
        "CRITIC_FEEDBACK": _dump(feedback) if feedback else NONE,
    }


# ---------------------------------------------------------------- pipeline

@dataclass
class RunResult:
    status: str  # pass | revise_exhausted | rejected | error
    attempts: int
    sequence: dict | None  # the best attempt's sequence (fewest blockers, then majors)
    out_dir: Path
    best_attempt: int | None = None
    attempt_scores: dict[int, dict] = field(default_factory=dict)
    source_flags: list[dict] = field(default_factory=list)  # problems in the source itself, for a person
    optimisation: dict | None = None  # what the Connected Learning stage did, per unit
    usage: list[dict] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "pass"


def _issues(critic: dict) -> list[dict]:
    return [
        {"check": c.get("id"), **issue}
        for c in critic.get("checks", [])
        if isinstance(c, dict)
        for issue in c.get("issues", [])
        if isinstance(issue, dict)
    ]


def _code_issues(report: v.Report) -> list[dict]:
    return [
        {"check": c.id, "source": "code", "where": i.where, "problem": i.problem}
        for c in report.checks
        for i in c.issues
    ]


def _score(issues: list[dict]) -> dict:
    """Issue counts by severity; code failures count as blockers."""
    counts = {"blocker": 0, "major": 0, "minor": 0}
    for i in issues:
        sev = "blocker" if i.get("source") == "code" else i.get("severity")
        if sev in counts:
            counts[sev] += 1
    return counts


def _rank(score: dict) -> tuple:
    return (score.get("rejected", 0), score["blocker"], score["major"], score["minor"])


UNIT_WHERE = re.compile(r"mls_units\[(\d+)\]")


def run_connected_learning(src: Source, decomposed: dict, call, save, result: RunResult,
                           max_revisions: int = 1) -> list[dict] | None:
    """Apply the CL cards unit by unit to a sequence that passed the critic.

    Each unit's edit must pass `optimise.check_unit_edit` (one retry with the
    problems as feedback; then the unit stays as it was). Accepted edits are merged
    and the whole sequence goes back through the validator and the critic. A unit
    the critic finds issues in is revised up to `max_revisions` times, then
    reverted to its decomposed version. Anything the stage can't pin on one edited
    unit (a REJECT, an unusable review, an issue outside the edited units) reverts
    every edit. The stage can therefore only keep or improve the passed sequence;
    it never fails the run. Returns the final source trace if any edit was kept.
    """
    cards = CL_CARDS_PATH.read_text(encoding="utf-8")
    seq = decomposed["sequence"]
    trace = decomposed.get("source_trace") or []
    units = [u for u in seq.get("mls_units", []) if isinstance(u, dict) and isinstance(u.get("mls_id"), str)]
    originals = {u["mls_id"]: u for u in units}
    log: dict = {"stage": "connected_learning", "units": {}, "reviews": []}
    result.optimisation = log
    accepted: dict[str, dict] = {}

    def edit(uid: str, rnd: int, previous: dict | None = None, feedback: list | None = None) -> dict | None:
        for tries in (1, 2):
            label = f"cl{rnd}-{uid}" + ("-retry" if tries == 2 else "")
            try:
                out = call("connected-learning", CONNECTED_LEARNING,
                           cl_values(src, decomposed, uid, cards, previous, feedback), label)
                problems = opt.check_unit_edit(originals[uid], out)
            except StageError as e:
                out, problems = None, [str(e)]
            if out is not None:
                save(f"{label}.json", out)
            if not problems:
                return out
            result.notes.append(f"connected learning {uid}: edit failed the code check: {'; '.join(problems)}")
            previous = out
            feedback = [{"check": "edit-limits", "source": "code", "problem": p} for p in problems]
        return None

    def record(uid: str, out: dict | None, status: str) -> None:
        entry = log["units"].setdefault(uid, {})
        entry["status"] = status
        if out is not None:
            entry.update(decision=out.get("decision"), reason=out.get("reason"),
                         cards=sorted({c.get("card") for c in out.get("changes", [])}),
                         changes=out.get("changes", []), credit=out.get("credit", []),
                         deferred=out.get("deferred", []))

    for uid in originals:
        out = edit(uid, 1)
        if out is None:
            record(uid, None, "edit_rejected")
        elif out["decision"] == "ABSTAIN":
            record(uid, out, "abstained")
        else:
            accepted[uid] = out
            record(uid, out, "applied")

    def revert(uids, why: str) -> None:
        for uid in list(uids):
            accepted.pop(uid, None)
            log["units"][uid]["status"] = "reverted"
        result.notes.append(f"connected learning: reverted {', '.join(sorted(uids))}: {why}")

    def candidate() -> dict:
        merged = opt.merge(seq, {u: o["unit"] for u, o in accepted.items()})
        merged_trace = opt.merge_trace(trace, {u: opt.unit_trace(originals[u], o, trace) for u, o in accepted.items()})
        return {"sequence": merged, "source_trace": merged_trace}

    previous_issues: list | None = None
    for rnd in range(1, max_revisions + 2):
        if not accepted:
            return None
        cand = candidate()
        report = v.validate(cand["sequence"])
        save(f"cl{rnd}-validator.json", report.to_dict())
        try:
            critic = call("critic", CRITIC, critic_values(src, cand, report, previous_issues, cards), f"cl{rnd}-critic")
        except StageError as e:
            revert(accepted, f"critic unusable: {e}")
            return None
        save(f"cl{rnd}-critic.json", critic)
        verdict = critic.get("verdict")
        issues = _issues(critic)
        covered = {(i.get("where"), i.get("problem")) for i in issues}
        issues += [i for i in _code_issues(report) if (i["where"], i["problem"]) not in covered]
        blocking = [i for i in issues if i.get("source") == "code" or i.get("severity") in ("blocker", "major")]
        log["reviews"].append({"round": rnd, "verdict": verdict, "blocking_issues": len(blocking)})

        if verdict == "PASS" and report.passed:
            result.sequence = cand["sequence"]
            if critic.get("source_flags") is not None:
                result.source_flags = [f for f in critic["source_flags"] if isinstance(f, dict)]
            return cand["source_trace"]
        if verdict not in ("PASS", "REVISE"):
            revert(accepted, f"critic verdict {verdict!r}: {critic.get('notes', '')}")
            return None

        by_unit: dict[str, list[dict]] = {}
        unplaced = []
        for i in blocking:
            m = UNIT_WHERE.search(str(i.get("where", "")))
            uid = units[int(m.group(1))]["mls_id"] if m and int(m.group(1)) < len(units) else None
            if uid in accepted:
                by_unit.setdefault(uid, []).append(i)
            else:
                unplaced.append(i)
        if unplaced or not by_unit:
            revert(accepted, f"{len(unplaced) or len(blocking)} issue(s) not traceable to one edited unit")
            return None
        if rnd > max_revisions:
            revert(by_unit, "issues remained after revision")
            if not accepted:
                return None
            cand = candidate()  # the remaining edits had no issues in this review
            result.sequence = cand["sequence"]
            result.notes.append("connected learning: kept edits had no issues in the last review; "
                                "the sequence was not re-reviewed after the revert")
            return cand["source_trace"]

        for uid, unit_issues in by_unit.items():
            out = edit(uid, rnd + 1, accepted[uid], unit_issues)
            if out is None or out["decision"] == "ABSTAIN":
                revert([uid], "revision failed the code check" if out is None else "revision abstained")
                if out is not None:
                    record(uid, out, "abstained")
            else:
                accepted[uid] = out
                record(uid, out, "applied")
        previous_issues = blocking
    return None


def run_pipeline(src: Source, model: Model, out_dir: Path, max_revisions: int = 2,
                 connected_learning: bool = False, max_cl_revisions: int = 1) -> RunResult:
    out_dir.mkdir(parents=True, exist_ok=True)

    def save(name: str, obj: Any) -> None:
        (out_dir / name).write_text(_dump(obj) + "\n", encoding="utf-8")

    def call(stage: str, prompt_file: str, values: dict, attempt: int | str) -> dict:
        system, user, missing = build_request(prompt_file, values)
        if missing:
            raise SystemExit(f"{prompt_file}: no value for {missing}")
        text, usage = model.complete(system, user)
        result.usage.append({"attempt": attempt, "stage": stage, **usage})
        label = f"{attempt:02d}-{stage}" if isinstance(attempt, int) else attempt
        (out_dir / f"{label}.reply.txt").write_text(text, encoding="utf-8")
        return extract_json(text)

    result = RunResult("error", 0, None, out_dir)
    best_decomposed: dict | None = None
    previous: dict | None = None
    feedback: list | None = None
    rejects = 0

    for attempt in range(1, max_revisions + 2):
        result.attempts = attempt
        try:
            decomposed = call("decompose", DECOMPOSE, decompose_values(src, previous, feedback), attempt)
        except ModelUnavailable as e:
            result.notes.append(f"attempt {attempt}: model unavailable, run stopped: {e}")
            result.status = "error"
            break
        except StageError as e:
            result.notes.append(f"attempt {attempt}: decompose unusable: {e}")
            previous, feedback = None, [{"check": "format", "problem": str(e),
                                         "fix": "Return only the JSON object the instructions specify."}]
            continue
        save(f"{attempt:02d}-decompose.json", decomposed)
        sequence = decomposed.get("sequence")
        if not isinstance(sequence, dict):
            result.notes.append(f"attempt {attempt}: decompose output has no 'sequence' object")
            previous, feedback = decomposed, [{"check": "format", "problem": "no 'sequence' object",
                                               "fix": "Wrap the MLS_DAG_Sequence in a top-level 'sequence' key."}]
            continue

        report = v.validate(sequence)
        save(f"{attempt:02d}-validator.json", report.to_dict())

        reviewed_issues = feedback if previous is not None else None  # a revision of `previous`
        try:
            critic = call("critic", CRITIC, critic_values(src, decomposed, report, reviewed_issues), attempt)
        except ModelUnavailable as e:
            result.notes.append(f"attempt {attempt}: model unavailable, run stopped: {e}")
            result.status = "error"
            break
        except StageError as e:
            result.notes.append(f"attempt {attempt}: critic unusable: {e}")
            result.status = "error"
            break
        save(f"{attempt:02d}-critic.json", critic)
        # The latest review's list replaces earlier ones: each critic reviews the
        # whole source, so lists from different attempts repeat in different words.
        result.source_flags = [f for f in critic.get("source_flags") or [] if isinstance(f, dict)]

        verdict = critic.get("verdict")
        if verdict not in VERDICTS:
            result.notes.append(f"attempt {attempt}: critic verdict {verdict!r} is not one of {VERDICTS}")
            result.status = "error"
            break
        if verdict == "PASS" and not report.passed:
            result.notes.append(
                f"attempt {attempt}: critic said PASS but code checks failed ({', '.join(report.failed_ids())}); treated as REVISE"
            )
            verdict = "REVISE"

        # The critic's issues plus any code failures it didn't copy.
        issues = _issues(critic)
        covered = {(i.get("where"), i.get("problem")) for i in issues}
        issues += [i for i in _code_issues(report) if (i["where"], i["problem"]) not in covered]
        score = {**_score(issues), "rejected": int(verdict == "REJECT")}
        result.attempt_scores[attempt] = score
        if result.best_attempt is None or _rank(score) < _rank(result.attempt_scores[result.best_attempt]) \
                or verdict == "PASS":
            result.best_attempt, result.sequence, best_decomposed = attempt, sequence, decomposed

        if verdict == "PASS":
            result.status = "pass"
            break
        if verdict == "REJECT":
            rejects += 1
            result.notes.append(f"attempt {attempt}: critic REJECT: {critic.get('notes', '')}")
            if rejects > 1:
                result.status = "rejected"
                break
            previous, feedback = None, None  # start again from the source
            result.status = "rejected"
            continue
        # REVISE: send the issues back to decompose with its previous output.
        previous, feedback = decomposed, issues
        result.status = "revise_exhausted"

    if connected_learning and result.status == "pass" and best_decomposed is not None:
        save("decomposed-sequence.json", result.sequence)
        try:
            final_trace = run_connected_learning(src, best_decomposed, call, save, result, max_cl_revisions)
        except ModelUnavailable as e:
            result.notes.append(f"connected learning: model unavailable; kept the decomposed sequence: {e}")
        else:
            if final_trace is not None:
                save("source_trace.json", final_trace)

    if result.sequence is not None:
        save("sequence.json", result.sequence)
    save("summary.json", {
        "status": result.status,
        "attempts": result.attempts,
        "best_attempt": result.best_attempt,
        "attempt_scores": result.attempt_scores,
        "optimisation": result.optimisation,
        "source_flags": result.source_flags,
        "source_ref": src.ref,
        "notes": result.notes,
        "usage": result.usage,
    })
    return result


# ---------------------------------------------------------------- CLI

def dry_run(src: Source) -> int:
    problems = 0
    fake_decomposed = {"sequence": {}, "source_trace": []}
    fake_report = v.validate({})
    cards = CL_CARDS_PATH.read_text(encoding="utf-8")
    for name, values in (
        (DECOMPOSE, decompose_values(src)),
        (CRITIC, critic_values(src, fake_decomposed, fake_report)),
        (CONNECTED_LEARNING, cl_values(src, fake_decomposed, "MLS-X-01", cards)),
    ):
        system, user, missing = build_request(name, values)
        chars = len(system[0]["text"]) + len(user)
        status = "OK" if not missing else f"MISSING {missing}"
        problems += bool(missing)
        print(f"{name:26} ~{chars // 4:>6,} tokens  {status}")
    print("\nA live run makes 2 calls per decompose attempt (decompose + critic), then, once the\n"
          "sequence passes, 1 Connected Learning call per unit and 1 critic call per CL round.")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m lsb.run", description=__doc__.split("\n\n")[0])
    ap.add_argument("source", type=Path, help="text file with the source content")
    ap.add_argument("--ref", required=True, help="source identifier, e.g. 'Chapter 4 - Basic Hydrology Framework'")
    ap.add_argument("--grade-band", choices=["Primary", "Middle", "High"])
    ap.add_argument("--time-block", type=int, metavar="MINUTES", help="class period length, 5-120")
    ap.add_argument("--context-file", type=Path, help="educator's notes about their setting")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--backend", default="claude-code", choices=["claude-code", "api"],
                    help="claude-code: headless `claude -p` on your Claude Code login (default); api: Anthropic API key")
    ap.add_argument("--max-revisions", type=int, default=2)
    ap.add_argument("--no-cl", action="store_true", help="stop after decompose; skip the Connected Learning stage")
    ap.add_argument("--max-cl-revisions", type=int, default=1)
    ap.add_argument("--out", type=Path, help="output directory (default runs/<timestamp>)")
    ap.add_argument("--dry-run", action="store_true", help="assemble and check the requests; no API calls")
    args = ap.parse_args(argv)

    try:
        src = Source(
            text=args.source.read_text(encoding="utf-8"),
            ref=args.ref,
            grade_band=args.grade_band,
            time_block_minutes=args.time_block,
            context=args.context_file.read_text(encoding="utf-8") if args.context_file else None,
        )
    except OSError as e:
        print(f"cannot read input: {e}", file=sys.stderr)
        return 2

    if args.dry_run:
        return 2 if dry_run(src) else 0

    out_dir = args.out or RUNS / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    if args.backend == "claude-code":
        model: Model = ClaudeCodeModel(effort=args.effort)
        api_errors: tuple = ()
    else:
        import anthropic
        model = AnthropicModel(effort=args.effort)
        api_errors = (anthropic.RateLimitError, anthropic.APIStatusError, anthropic.APIConnectionError)
    try:
        result = run_pipeline(src, model, out_dir, args.max_revisions,
                              connected_learning=not args.no_cl, max_cl_revisions=args.max_cl_revisions)
    except api_errors as e:
        print(f"API error after retries: {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    tokens_in = sum(u["input"] + u["cache_read"] + u["cache_write"] for u in result.usage)
    tokens_out = sum(u["output"] for u in result.usage)
    print(f"status: {result.status} after {result.attempts} attempt(s), {len(result.usage)} API call(s), "
          f"{tokens_in:,} input / {tokens_out:,} output tokens")
    for n, score in result.attempt_scores.items():
        mark = "  <- kept in sequence.json" if n == result.best_attempt else ""
        print(f"  attempt {n}: {score['blocker']} blocker, {score['major']} major, {score['minor']} minor"
              f"{' (REJECT)' if score.get('rejected') else ''}{mark}")
    if result.optimisation:
        print("connected learning:")
        for uid, u in result.optimisation["units"].items():
            print(f"  {uid}: {u['status']}" + (f" ({', '.join(u['cards'])})" if u.get("cards") else ""))
        for r in result.optimisation["reviews"]:
            print(f"  review {r['round']}: {r['verdict']}, {r['blocking_issues']} blocking issue(s)")
    for note in result.notes:
        print(f"  {note}")
    for flag in result.source_flags:
        print(f"  source flag: {flag.get('where', '?')}: {flag.get('problem', '')}")
    print(f"saved to {out_dir}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
