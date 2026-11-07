"""Run one source text through 05-decompose -> lsb.validate -> 50-critic, then the optimisation stages.

    python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework" --dry-run
    python3 -m lsb.run tests/fixtures/hydrology-source.md --ref "Chapter 4 - Basic Hydrology Framework"

Backends: `--backend claude-code` (default) runs each call through headless Claude
Code (`claude -p`) on your Claude Code login, with no API key needed.
`--backend muse` runs each call through headless Muse Code (`muse exec`) on
your Muse login instead. `--backend api` calls the Anthropic API directly and
needs ANTHROPIC_API_KEY or an `ant auth login` profile.
Every intermediate JSON is saved under runs/<timestamp>/.

Routing (prompts/README.md):
  critic PASS    -> done
  critic REVISE  -> re-run 05 with the critic's issues, up to --max-revisions times
  critic REJECT  -> re-run 05 from scratch once; a second REJECT stops the run
The validator's result is final: a critic PASS on a sequence that fails a code
check is recorded and treated as REVISE.

Once the sequence passes, the optimisation stages run in order, each once per unit:
25-evidence-based (skip with --no-eb), 30-connected-learning (--no-cl), then
31-participatory-budgeting (--no-pb).
lsb.optimise checks each edit's limits in code; accepted edits are merged, validated
and reviewed by the critic again. A unit whose edit still has issues after
--max-stage-revisions is reverted, so a stage never fails a passed sequence.
sequence.json is the final sequence; decomposed-sequence.json is the one before them.
A passed run also writes the teacher cards (cards.txt, cards.html; see lsb.render)
and records their G21 check in summary.json.

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
from lsb import render
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
CRITIC = "50-critic.md"


@dataclass(frozen=True)
class FrameworkStage:
    """One optimisation stage: a per-unit prompt plus the cards it may apply."""
    key: str  # name in summary.json
    short: str  # file-name prefix, CLI flag
    prompt: str
    cards_path: Path
    cards_placeholder: str
    card_ids: tuple[str, ...]

    def cards(self) -> str:
        return self.cards_path.read_text(encoding="utf-8")


STAGES = {
    "eb": FrameworkStage("evidence_based", "eb", "25-evidence-based.md",
                         ROOT / "frameworks" / "evidence-based-practices.md", "EB_CARDS", opt.EB_CARDS),
    "cl": FrameworkStage("connected_learning", "cl", "30-connected-learning.md",
                         ROOT / "frameworks" / "connected-learning.md", "CL_CARDS", opt.CL_CARDS),
    "pb": FrameworkStage("participatory_budgeting", "pb", "31-participatory-budgeting.md",
                         ROOT / "frameworks" / "participatory-budgeting.md", "PB_CARDS", opt.PB_CARDS),
}
STAGE_ORDER = ("eb", "cl", "pb")
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


class MuseModel:
    """Calls the model through headless Muse Code (`muse exec`), on the user's Muse login.

    No API key needed. `muse exec` has no system-prompt channel, so the system
    prompt and the user turn go in one prompt file, in that order. One model
    step and no reminders: the reply must be the JSON the prompt asks for. It
    runs in an empty temporary directory so no workspace skills or rules load.
    Stdout is JSONL; the reply is the joined run.output.delta texts and token
    counts come from the run.usage event, which reports no USD cost.
    """

    def __init__(self, effort: str = "high", model: str | None = None, timeout: int = 1200, runner=None):
        import subprocess

        self.effort = effort
        self.model = model
        self.timeout = timeout
        self.runner = runner or subprocess.run

    def complete(self, system: list[dict], user: str) -> tuple[str, dict]:
        import subprocess
        import tempfile

        with tempfile.TemporaryDirectory(prefix="lsb-") as tmp:
            prompt_file = Path(tmp) / "prompt.md"
            prompt_file.write_text("\n\n".join(b["text"] for b in system) + "\n\n" + user, encoding="utf-8")
            cmd = [
                "muse", "exec", "--json",
                "--prompt-file", str(prompt_file),
                "--reasoning-effort", self.effort,
                "--max-model-steps", "1",
                "--disable-reminders",
                "--no-session-log",
            ]
            if self.model:
                cmd += ["--model", self.model]
            try:
                proc = self.runner(cmd, capture_output=True, text=True, cwd=tmp, timeout=self.timeout)
            except FileNotFoundError as e:
                raise SystemExit("`muse` CLI not found; install Muse Code or use --backend claude-code") from e
            except subprocess.TimeoutExpired as e:
                raise StageError(f"muse exec timed out after {self.timeout}s") from e

        texts: list[str] = []
        model_id: str | None = None
        first: dict = {}
        for line in (proc.stdout or "").splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = ev.get("payload") or {}
            if ev.get("payload_type") == "run.output.delta":
                texts.append(payload.get("text") or "")
            elif ev.get("payload_type") == "run.model.configured":
                model_id = payload.get("model_id") or model_id
            elif ev.get("payload_type") == "run.usage" and not first:
                first = (payload.get("models") or [{}])[0]

        if proc.returncode != 0:
            detail = (proc.stderr or "").strip().splitlines()
            detail = (detail[-1] if detail else "no error message")[:500]
            low = (proc.stderr or "").lower()
            if any(s in low for s in ("log in", "logged in", "login", "auth")):
                raise SystemExit(f"Muse is not signed in: {detail}")
            if USAGE_LIMIT.search(proc.stderr or ""):
                raise ModelUnavailable(detail[:300])
            raise StageError(f"muse exec exit {proc.returncode}: {detail}")
        text = "".join(texts)
        if not text.strip():
            raise StageError("muse exec returned no text")
        usage = {
            "model": first.get("model") or model_id or self.model or "muse",
            "stop_reason": None,
            "input": first.get("input_tokens", 0),
            "output": first.get("output_tokens", 0),
            "cache_read": first.get("cached_tokens", 0),
            "cache_write": 0,
            "cost_usd_list_price": None,
        }
        return text, usage


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
        # The optimisation stages don't change the assumptions, so only the decompose
        # loop's reviews get them; a stage's review can't send an issue in one back.
        "ENVIRONMENT_ASSUMPTIONS": (_dump(decomposed["environment_assumptions"])
                                    if decomposed.get("environment_assumptions") else NONE),
        "FRAMEWORK_CARDS": cards or NONE,
        "RENDERED_CARDS": NONE,
        "PREVIOUS_ISSUES": _dump(previous_issues) if previous_issues else NONE,
    }


def stage_values(stage: FrameworkStage, src: Source, decomposed: dict, uid: str,
                 previous: dict | None = None, feedback: list | None = None) -> dict[str, str]:
    trace = [e for e in decomposed.get("source_trace") or [] if isinstance(e, dict) and e.get("mls_id") == uid]
    return {
        "SEQUENCE_JSON": _dump(decomposed["sequence"]),
        "UNIT_ID": uid,
        "UNIT_TRACE": _dump(trace) if trace else NONE,
        "SOURCE_TEXT": src.text,
        stage.cards_placeholder: stage.cards(),
        "PREVIOUS_OUTPUT": _dump(previous) if previous is not None else NONE,
        "CRITIC_FEEDBACK": _dump(feedback) if feedback else NONE,
    }


# ---------------------------------------------------------------- pipeline

@dataclass
class RunResult:
    status: str  # pass | revise_exhausted | rejected | issues_open | error
    attempts: int
    sequence: dict | None  # the best attempt's sequence (fewest blockers, then majors)
    out_dir: Path
    best_attempt: int | None = None
    attempt_scores: dict[int, dict] = field(default_factory=dict)
    source_flags: list[dict] = field(default_factory=list)  # problems in the source itself, for a person
    optimisation: dict | None = None  # per optimisation stage: what it did to each unit
    late_issues: list[dict] = field(default_factory=list)  # found by a stage's review in content no stage changed
    repair: dict | None = None  # the repair rounds that dealt with late_issues
    cards_problems: list[str] | None = None  # G21 check on the rendered cards; None if not rendered
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


def _update_flags(result: RunResult, critic: dict) -> None:
    """A later review's source flags replace earlier ones only if it lists any.

    Stage and repair reviews look at the sequence; some return no source flags at
    all, which would otherwise erase what the decompose review found in the source.
    """
    flags = [f for f in critic.get("source_flags") or [] if isinstance(f, dict)]
    if flags:
        result.source_flags = flags


def run_framework_stage(stage: FrameworkStage, src: Source, current: dict, call, save, result: RunResult,
                        earlier_cards: str = "", max_revisions: int = 1) -> dict | None:
    """Apply one stage's cards unit by unit to a sequence that passed the critic.

    `current` is {"sequence", "source_trace"}. Each unit's edit must pass
    `optimise.check_unit_edit` (one retry with the problems as feedback; then the
    unit stays as it was). Accepted edits are merged and the whole sequence goes
    back through the validator and the critic, with these cards and any from
    earlier stages. A unit the critic finds issues in is revised up to
    `max_revisions` times, then reverted to its input version. Anything the stage
    can't act on (a REJECT, an unusable review) reverts every edit.

    The review sees the whole sequence, so it can also find problems in content
    this stage didn't change: a step another stage wrote, or one the decompose
    review missed. Those aren't this stage's to fix and don't count against its
    edits; they go to `result.late_issues` for the repair round after the stages.

    Returns the new {"sequence", "source_trace"} if any edit was kept, else None.
    """
    cards = stage.cards()
    review_cards = "\n\n".join(c for c in (earlier_cards, cards) if c)
    seq = current["sequence"]
    trace = current.get("source_trace") or []
    units = [u for u in seq.get("mls_units", []) if isinstance(u, dict) and isinstance(u.get("mls_id"), str)]
    originals = {u["mls_id"]: u for u in units}
    log: dict = {"units": {}, "reviews": []}
    result.optimisation = {**(result.optimisation or {}), stage.key: log}
    accepted: dict[str, dict] = {}
    p = stage.short

    def edit(uid: str, rnd: int, previous: dict | None = None, feedback: list | None = None) -> dict | None:
        for tries in (1, 2):
            label = f"{p}{rnd}-{uid}" + ("-retry" if tries == 2 else "")
            try:
                out = call(stage.key, stage.prompt, stage_values(stage, src, current, uid, previous, feedback), label)
                problems = opt.check_unit_edit(originals[uid], out, stage.card_ids)
            except StageError as e:
                out, problems = None, [str(e)]
            if out is not None:
                save(f"{label}.json", out)
            if not problems:
                return out
            result.notes.append(f"{stage.key} {uid}: edit failed the code check: {'; '.join(problems)}")
            previous = out
            feedback = [{"check": "edit-limits", "source": "code", "problem": p_} for p_ in problems]
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
        names = sorted(uids)
        for uid in names:
            accepted.pop(uid, None)
            log["units"][uid]["status"] = "reverted"
        result.notes.append(f"{stage.key}: reverted {', '.join(names)}: {why}")

    def stage_unit(issue: dict) -> str | None:
        """The edited unit this issue is about, if it's about something this stage changed."""
        for loc in opt.locations(issue.get("where")):
            if loc[0] == "assumption" or loc[1] >= len(units):
                continue
            uid = units[loc[1]]["mls_id"]
            if uid not in accepted:
                continue
            if loc[0] == "unit":
                return uid
            if loc[0] == "task" and opt.match_steps(originals[uid], accepted[uid]["unit"])[loc[2]:loc[2] + 1] == [None]:
                return uid
        return None

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
        save(f"{p}{rnd}-validator.json", report.to_dict())
        try:
            critic = call("critic", CRITIC, critic_values(src, cand, report, previous_issues, review_cards),
                          f"{p}{rnd}-critic")
        except StageError as e:
            revert(accepted, f"critic unusable: {e}")
            return None
        save(f"{p}{rnd}-critic.json", critic)
        verdict = critic.get("verdict")
        issues = _issues(critic)
        covered = {(i.get("where"), i.get("problem")) for i in issues}
        issues += [i for i in _code_issues(report) if (i["where"], i["problem"]) not in covered]
        blocking = [i for i in issues if i.get("source") == "code" or i.get("severity") in ("blocker", "major")]
        log["reviews"].append({"round": rnd, "verdict": verdict, "blocking_issues": len(blocking)})

        if verdict == "PASS" and report.passed:
            _update_flags(result, critic)
            return cand
        if verdict not in ("PASS", "REVISE"):
            revert(accepted, f"critic verdict {verdict!r}: {critic.get('notes', '')}")
            return None

        by_unit: dict[str, list[dict]] = {}
        known = {(i.get("where"), i.get("problem")) for i in result.late_issues}
        for i in blocking:
            uid = stage_unit(i)
            if uid is not None:
                by_unit.setdefault(uid, []).append(i)
            elif (i.get("where"), i.get("problem")) not in known:
                result.late_issues.append({**i, "found_by": f"{stage.key} review {rnd}"})
                known.add((i.get("where"), i.get("problem")))
        if not by_unit:  # nothing wrong with this stage's own edits
            _update_flags(result, critic)
            return cand
        if rnd > max_revisions:
            revert(by_unit, "issues remained after revision")
            if not accepted:
                return None
            result.notes.append(f"{stage.key}: kept edits had no issues in the last review; "
                                "the sequence was not re-reviewed after the revert")
            return candidate()  # the remaining edits had no issues in this review

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


REPAIR_NOTE = {"check": "repair", "source": "orchestrator",
               "problem": "These issues were found after the optimisation stages, in PREVIOUS_OUTPUT as they left it. "
                          "Edit only the steps, fields and fallbacks the issues point at, in place, and update that unit's "
                          "fallbacks if the fix changes what they describe. Keep every other "
                          "step exactly as it is, and don't add, remove or reorder units, steps or fallbacks."}


def run_repair(src: Source, full: dict, issues: list[dict], call, save, result: RunResult,
               cards: str = "", max_rounds: int = 2) -> dict | None:
    """Fix problems a stage's review found in content no stage changed.

    `full` is a decompose-shaped output holding the current sequence and trace.
    Decompose gets it back with the issues ("fix every listed issue, change nothing
    else"); `optimise.check_repair` holds it to the steps, fields and fallbacks the
    issues point at (one retry). The repaired sequence is validated and reviewed
    with the fallbacks and the kept cards. Returns the repaired output if the review
    passes within `max_rounds`, else None.
    """
    log: dict = {"issues": len(issues), "rounds": []}
    result.repair = log
    current, previous_issues = full, issues
    for rnd in range(1, max_rounds + 1):
        feedback = [REPAIR_NOTE] + previous_issues
        out = None
        for tries in (1, 2):
            label = f"repair{rnd}" + ("-retry" if tries == 2 else "")
            try:
                out = call("repair", DECOMPOSE, decompose_values(src, current, feedback), label)
                problems = opt.check_repair(current, out, previous_issues)
            except StageError as e:
                out, problems = None, [str(e)]
            if out is not None:
                save(f"{label}.json", out)
            if not problems:
                break
            result.notes.append(f"repair {rnd}: output failed the code check: {'; '.join(problems)}")
            feedback = [REPAIR_NOTE] + previous_issues + [{"check": "edit-limits", "source": "code", "problem": p}
                                                          for p in problems]
        else:
            log["rounds"].append({"round": rnd, "verdict": "edit_rejected"})
            return None
        # Steps are edited in place, so the current trace (with card ids) still lines up.
        cand = {**out, "source_trace": current.get("source_trace") or []}
        report = v.validate(cand["sequence"])
        save(f"repair{rnd}-validator.json", report.to_dict())
        try:
            critic = call("critic", CRITIC, critic_values(src, cand, report, previous_issues, cards),
                          f"repair{rnd}-critic")
        except StageError as e:
            result.notes.append(f"repair {rnd}: critic unusable: {e}")
            return None
        save(f"repair{rnd}-critic.json", critic)
        verdict = critic.get("verdict")
        issues_now = _issues(critic)
        covered = {(i.get("where"), i.get("problem")) for i in issues_now}
        issues_now += [i for i in _code_issues(report) if (i["where"], i["problem"]) not in covered]
        blocking = [i for i in issues_now if i.get("source") == "code" or i.get("severity") in ("blocker", "major")]
        log["rounds"].append({"round": rnd, "verdict": verdict, "blocking_issues": len(blocking)})
        _update_flags(result, critic)
        if verdict == "PASS" and report.passed:
            return cand
        if verdict != "REVISE":
            return None
        current, previous_issues = cand, blocking
    return None


def run_pipeline(src: Source, model: Model, out_dir: Path, max_revisions: int = 2,
                 stages: tuple[str, ...] = (), max_stage_revisions: int = 1) -> RunResult:
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

    final_trace = (best_decomposed or {}).get("source_trace") or []
    if stages and result.status == "pass" and best_decomposed is not None:
        save("decomposed-sequence.json", result.sequence)
        current = {"sequence": best_decomposed["sequence"], "source_trace": best_decomposed.get("source_trace") or []}
        kept_cards: list[str] = []
        for key in stages:
            stage = STAGES[key]
            try:
                new = run_framework_stage(stage, src, current, call, save, result,
                                          "\n\n".join(kept_cards), max_stage_revisions)
            except ModelUnavailable as e:
                result.notes.append(f"{stage.key}: model unavailable; stopped before finishing this stage, "
                                    f"kept the sequence from the stages before it: {e}")
                break
            if new is not None:
                current = new
                kept_cards.append(stage.cards())
        if current["sequence"] is not best_decomposed["sequence"]:
            result.sequence = current["sequence"]
            final_trace = current["source_trace"]
            save("source_trace.json", final_trace)

        if result.late_issues:
            save("late-issues.json", result.late_issues)
            full = {**best_decomposed, "sequence": result.sequence, "source_trace": final_trace}
            try:
                repaired = run_repair(src, full, result.late_issues, call, save, result, "\n\n".join(kept_cards))
            except ModelUnavailable as e:
                result.notes.append(f"repair: model unavailable: {e}")
                repaired = None
            if repaired is not None:
                best_decomposed = repaired  # its fallbacks are the reviewed ones
                result.sequence = repaired["sequence"]
                final_trace = repaired["source_trace"]
                save("source_trace.json", final_trace)
            else:
                result.status = "issues_open"
                result.notes.append(f"{len(result.late_issues)} issue(s) found after decompose could not be "
                                    "repaired; see late-issues.json. No cards were rendered.")

    if result.status == "pass" and best_decomposed is not None:
        deck = render.build_deck(result.sequence, best_decomposed, result.optimisation, final_trace, src.ref)
        result.cards_problems = render.write_cards(deck, out_dir)
        for problem in result.cards_problems:
            result.notes.append(f"cards: G21 check failed: {problem}")

    if result.sequence is not None:
        save("sequence.json", result.sequence)
    save("summary.json", {
        "status": result.status,
        "attempts": result.attempts,
        "best_attempt": result.best_attempt,
        "attempt_scores": result.attempt_scores,
        "optimisation": result.optimisation,
        "late_issues": result.late_issues,
        "repair": result.repair,
        "cards_g21": None if result.cards_problems is None else (result.cards_problems or "pass"),
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
    for name, values in (
        (DECOMPOSE, decompose_values(src)),
        (CRITIC, critic_values(src, fake_decomposed, fake_report)),
        *((st.prompt, stage_values(st, src, fake_decomposed, "MLS-X-01")) for st in STAGES.values()),
    ):
        system, user, missing = build_request(name, values)
        chars = len(system[0]["text"]) + len(user)
        status = "OK" if not missing else f"MISSING {missing}"
        problems += bool(missing)
        print(f"{name:30} ~{chars // 4:>6,} tokens  {status}")
    print("\nA live run makes 2 calls per decompose attempt (decompose + critic), then, once the\n"
          "sequence passes, per optimisation stage (EB, CL, then PB): 1 call per unit and 1 critic\n"
          "call per review round (none if every unit abstains).")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m lsb.run", description=__doc__.split("\n\n")[0])
    ap.add_argument("source", type=Path, help="text file with the source content")
    ap.add_argument("--ref", required=True, help="source identifier, e.g. 'Chapter 4 - Basic Hydrology Framework'")
    ap.add_argument("--grade-band", choices=["Primary", "Middle", "High"])
    ap.add_argument("--time-block", type=int, metavar="MINUTES", help="class period length, 5-120")
    ap.add_argument("--context-file", type=Path, help="educator's notes about their setting")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--backend", default="claude-code", choices=["claude-code", "muse", "api"],
                    help="claude-code: headless `claude -p` on your Claude Code login (default); "
                         "muse: headless `muse exec` on your Muse login; api: Anthropic API key")
    ap.add_argument("--model", default=None,
                    help="model id (default: claude-opus-5-5 for claude-code/api, the CLI default for muse)")
    ap.add_argument("--max-revisions", type=int, default=2)
    ap.add_argument("--no-eb", action="store_true", help="skip the Evidence-Based stage")
    ap.add_argument("--no-cl", action="store_true", help="skip the Connected Learning stage")
    ap.add_argument("--no-pb", action="store_true", help="skip the Participatory Budgeting stage")
    ap.add_argument("--max-stage-revisions", type=int, default=1,
                    help="critic-driven revision rounds per optimisation stage (default 1)")
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
        model: Model = ClaudeCodeModel(effort=args.effort, model=args.model or MODEL)
        api_errors: tuple = ()
    elif args.backend == "muse":
        model = MuseModel(effort=args.effort, model=args.model)
        api_errors = ()
    else:
        import anthropic
        model = AnthropicModel(effort=args.effort, model=args.model or MODEL)
        api_errors = (anthropic.RateLimitError, anthropic.APIStatusError, anthropic.APIConnectionError)
    try:
        result = run_pipeline(src, model, out_dir, args.max_revisions,
                              stages=tuple(k for k in STAGE_ORDER if not getattr(args, f"no_{k}")),
                              max_stage_revisions=args.max_stage_revisions)
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
    for key, log in (result.optimisation or {}).items():
        print(f"{key.replace('_', ' ')}:")
        for uid, u in log["units"].items():
            print(f"  {uid}: {u['status']}" + (f" ({', '.join(u['cards'])})" if u.get("cards") else ""))
        for r in log["reviews"]:
            print(f"  review {r['round']}: {r['verdict']}, {r['blocking_issues']} blocking issue(s)")
    for note in result.notes:
        print(f"  {note}")
    for flag in result.source_flags:
        print(f"  source flag: {flag.get('where', '?')}: {flag.get('problem', '')}")
    if result.cards_problems is not None:
        print("teacher cards: cards.txt, cards.html; G21 " +
              ("pass" if not result.cards_problems else f"{len(result.cards_problems)} problem(s)"))
    print(f"saved to {out_dir}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
