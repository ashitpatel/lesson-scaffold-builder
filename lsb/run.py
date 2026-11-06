"""Run one source text through 05-decompose -> lsb.validate -> 50-critic.

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
VERDICTS = ("PASS", "REVISE", "REJECT")


# ---------------------------------------------------------------- model access

class Model(Protocol):
    def complete(self, system: list[dict], user: str) -> tuple[str, dict]:
        """Return (reply text, usage dict)."""


class StageError(RuntimeError):
    """The model's reply couldn't be used (refusal, truncation, no JSON)."""


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


def critic_values(src: Source, decomposed: dict, report: v.Report, previous_issues: list | None = None) -> dict[str, str]:
    return {
        "SEQUENCE_JSON": _dump(decomposed["sequence"]),
        "VALIDATOR_REPORT": _dump(report.to_dict()),
        "SOURCE_TEXT": src.text,
        "SOURCE_TRACE": _dump(decomposed["source_trace"]) if decomposed.get("source_trace") else NONE,
        "FRAMEWORK_CARDS": NONE,
        "RENDERED_CARDS": NONE,
        "PREVIOUS_ISSUES": _dump(previous_issues) if previous_issues else NONE,
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


def run_pipeline(src: Source, model: Model, out_dir: Path, max_revisions: int = 2) -> RunResult:
    out_dir.mkdir(parents=True, exist_ok=True)

    def save(name: str, obj: Any) -> None:
        (out_dir / name).write_text(_dump(obj) + "\n", encoding="utf-8")

    def call(stage: str, prompt_file: str, values: dict, attempt: int) -> dict:
        system, user, missing = build_request(prompt_file, values)
        if missing:
            raise SystemExit(f"{prompt_file}: no value for {missing}")
        text, usage = model.complete(system, user)
        result.usage.append({"attempt": attempt, "stage": stage, **usage})
        (out_dir / f"{attempt:02d}-{stage}.reply.txt").write_text(text, encoding="utf-8")
        return extract_json(text)

    result = RunResult("error", 0, None, out_dir)
    previous: dict | None = None
    feedback: list | None = None
    rejects = 0

    for attempt in range(1, max_revisions + 2):
        result.attempts = attempt
        try:
            decomposed = call("decompose", DECOMPOSE, decompose_values(src, previous, feedback), attempt)
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
        except StageError as e:
            result.notes.append(f"attempt {attempt}: critic unusable: {e}")
            result.status = "error"
            break
        save(f"{attempt:02d}-critic.json", critic)

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
            result.best_attempt, result.sequence = attempt, sequence

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

    if result.sequence is not None:
        save("sequence.json", result.sequence)
    save("summary.json", {
        "status": result.status,
        "attempts": result.attempts,
        "best_attempt": result.best_attempt,
        "attempt_scores": result.attempt_scores,
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
    ):
        system, user, missing = build_request(name, values)
        chars = len(system[0]["text"]) + len(user)
        status = "OK" if not missing else f"MISSING {missing}"
        problems += bool(missing)
        print(f"{name:16} ~{chars // 4:>6,} tokens  {status}")
    print("\nA live run makes 2 API calls per attempt (decompose + critic).")
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
        result = run_pipeline(src, model, out_dir, args.max_revisions)
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
    for note in result.notes:
        print(f"  {note}")
    print(f"saved to {out_dir}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
