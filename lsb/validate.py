"""Deterministic critic checks for an MLS_DAG_Sequence payload.

These are the parts of the 21-point critic gate (requirements, Part 3, section 7)
that code can decide exactly. The judgement checks (offline default, safety,
pedagogical sourcing, coherence, cognitive depth, ...) stay with the LLM critic,
which receives this report as input.

    python3 -m lsb.validate payload.json [--json]

Exit status: 0 all checks pass, 1 at least one check fails, 2 the file is unreadable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterator

from jsonschema import Draft202012Validator

from lsb import dag
from lsb._paths import resource_root

ROOT = resource_root()
SCHEMA_PATH = ROOT / "schemas" / "mls-dag.schema.json"
CONFIG_PATH = ROOT / "config" / "taxonomy_mapping.json"

ROLES = ("Lead_Educator", "Community_Volunteer", "Peer_Facilitator")


@dataclass
class Issue:
    where: str
    problem: str


@dataclass
class CheckResult:
    id: str
    name: str
    critic_check: str  # the check's name in the requirements' 21-point list
    issues: list[Issue] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.issues

    def fail(self, where: str, problem: str) -> None:
        self.issues.append(Issue(where, problem))


@dataclass
class Report:
    checks: list[CheckResult]

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    def failed_ids(self) -> list[str]:
        return [c.id for c in self.checks if not c.passed]

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "checks": [
                {**asdict(c), "passed": c.passed} for c in self.checks
            ],
        }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(path: Path = CONFIG_PATH) -> dict:
    return load_json(path)


# ---------------------------------------------------------------- helpers

def _units(payload: Any) -> list[tuple[int, dict]]:
    """(index, unit) for each well-formed unit; schema errors cover the rest."""
    units = payload.get("mls_units") if isinstance(payload, dict) else None
    if not isinstance(units, list):
        return []
    return [(i, u) for i, u in enumerate(units) if isinstance(u, dict)]


def _graph_units(payload: Any) -> list[dict]:
    """Units with a string id and a list of string dependencies, for the DAG checks."""
    out = []
    for _, u in _units(payload):
        deps = u.get("dependencies", [])
        if isinstance(u.get("mls_id"), str) and isinstance(deps, list):
            out.append({"mls_id": u["mls_id"], "dependencies": [d for d in deps if isinstance(d, str)]})
    return out


def _label(i: int, unit: dict) -> str:
    uid = unit.get("mls_id")
    return f"mls_units[{i}]" + (f" ({uid})" if isinstance(uid, str) else "")


def _tasks(unit: dict) -> list[tuple[int, dict]]:
    tasks = unit.get("tasks")
    if not isinstance(tasks, list):
        return []
    return [(j, t) for j, t in enumerate(tasks) if isinstance(t, dict)]


def _strings(node: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _strings(v, f"{path}[{i}]")


# A sentence ends at . ! or ? followed by whitespace and a capital letter or
# opening quote/bracket. "e.g." and "i.e." don't end a sentence.
_SENTENCE_END = re.compile(r"(?<!\be\.g)(?<!\bi\.e)(?<=[.!?])\s+(?=[A-Z'\"(])")


def sentence_count(text: str) -> int:
    return len([s for s in _SENTENCE_END.split(text.strip()) if s.strip()])


def _term_pattern(term: str) -> re.Pattern:
    # Word-boundary match for terms that start/end with a word character, so
    # "HM" does not match inside "rhythm" or "MIP" inside "MIPS"; plain
    # substring for symbols such as the rupee sign.
    left = r"(?<![A-Za-z0-9_])" if re.match(r"\w", term) else ""
    right = r"(?![A-Za-z0-9_])" if re.search(r"\w$", term) else ""
    return re.compile(left + re.escape(term) + right)


# ---------------------------------------------------------------- checks

def check_schema(payload: Any, schema: dict) -> CheckResult:
    r = CheckResult("D01", "Schema conformance", "(prerequisite for all checks)")
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.absolute_path)):
        where = "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in err.absolute_path)
        r.fail(where, err.message)
    return r


def check_unit_cap(payload: Any, limits: dict) -> CheckResult:
    r = CheckResult("D02", "Unit cap", "Structural Boundaries")
    n = len(_units(payload))
    cap = limits["max_mls_units"]
    if n > cap:
        r.fail("$.mls_units", f"{n} MLS units; the cap is {cap}")
    return r


def check_task_granularity(payload: Any, limits: dict) -> CheckResult:
    r = CheckResult("D03", "Steps per unit", "Task Granularity")
    lo, hi = limits["min_steps_per_unit"], limits["max_steps_per_unit"]
    for i, u in _units(payload):
        n = len(u["tasks"]) if isinstance(u.get("tasks"), list) else 0
        if not lo <= n <= hi:
            r.fail(_label(i, u), f"{n} steps; each unit needs {lo} to {hi}")
    return r


def check_execution_window(payload: Any, limits: dict, single_span: bool = False) -> CheckResult:
    r = CheckResult("D04", "Run length", "Execution Window")
    lo, hi = limits["min_duration_weeks"], limits["max_duration_weeks"]
    units = _units(payload)
    span_all = single_span and len(units) == 1
    for i, u in units:
        weeks = u.get("duration_weeks")
        if weeks is None:
            r.fail(_label(i, u), "duration_weeks is not declared, so the 2-to-4 week window cannot be confirmed")
        elif not isinstance(weeks, int) or isinstance(weeks, bool) or weeks < lo or (weeks > hi and not span_all):
            r.fail(_label(i, u), f"duration_weeks is {weeks!r}; it must be {lo} to {hi}")
    return r


def check_roles(payload: Any) -> CheckResult:
    r = CheckResult("D05", "Standard roles", "Role Standardization")
    for i, u in _units(payload):
        for j, t in _tasks(u):
            if t.get("role") not in ROLES:
                r.fail(f"{_label(i, u)}.tasks[{j}]", f"role {t.get('role')!r} is not one of {', '.join(ROLES)}")
    return r


def check_step_sequence(payload: Any) -> CheckResult:
    r = CheckResult("D06", "Step numbering", "(integrity: steps read 1..n in order)")
    for i, u in _units(payload):
        steps = [t.get("step") for _, t in _tasks(u)]
        if steps and steps != list(range(1, len(steps) + 1)):
            r.fail(_label(i, u), f"steps are {steps}; expected 1..{len(steps)} in order")
    return r


def check_dependency_mapping(payload: Any) -> CheckResult:
    r = CheckResult("D07", "Dependencies resolve", "Dependency Mapping")
    units = _graph_units(payload)
    for uid in dag.duplicate_ids(units):
        r.fail("$.mls_units", f"mls_id {uid!r} is used by more than one unit")
    for uid, dep in dag.missing_dependencies(units):
        r.fail(uid, f"depends on {dep!r}, which is not in mls_units")
    return r


def check_cycles(payload: Any) -> CheckResult:
    r = CheckResult("D08", "No dependency cycles", "Cycle Prevention")
    cycle = dag.find_cycle(_graph_units(payload))
    if cycle:
        r.fail("$.mls_units", "dependency cycle: " + " -> ".join(cycle))
    return r


def check_macro_alignment(payload: Any) -> CheckResult:
    r = CheckResult("D09", "Macro-objective link declared", "Macro Alignment")
    for i, u in _units(payload):
        link = u.get("macro_alignment")
        if not isinstance(link, str) or not link.strip():
            r.fail(_label(i, u), "macro_alignment is missing or empty")
    return r


def check_regional_terms(payload: Any, terms: list[str]) -> CheckResult:
    r = CheckResult("D10", "No regional terms", "Universal Taxonomy")
    patterns = [(t, _term_pattern(t)) for t in terms]
    for path, text in _strings(payload):
        found = [t for t, p in patterns if p.search(text)]
        if found:
            r.fail(path, "region-specific term(s): " + ", ".join(found))
    return r


def check_step_size(payload: Any, limits: dict) -> CheckResult:
    r = CheckResult("D11", "Step size", "Task Granularity")
    max_s, max_w = limits["max_sentences_per_step"], limits["max_words_per_step"]
    for i, u in _units(payload):
        for j, t in _tasks(u):
            action = t.get("action")
            if not isinstance(action, str):
                continue
            n_s, n_w = sentence_count(action), len(action.split())
            if n_s > max_s or n_w > max_w:
                r.fail(f"{_label(i, u)}.tasks[{j}]",
                       f"{n_s} sentences, {n_w} words; a step is one action (at most {max_s} sentences and "
                       f"{max_w} words). Split it into separate steps.")
    return r


def validate(payload: Any, schema: dict | None = None, config: dict | None = None,
             single_span: bool = False) -> Report:
    schema = schema if schema is not None else load_json(SCHEMA_PATH)
    config = config if config is not None else load_config()
    limits = config["limits"]
    return Report([
        check_schema(payload, schema),
        check_unit_cap(payload, limits),
        check_task_granularity(payload, limits),
        check_execution_window(payload, limits, single_span),
        check_roles(payload),
        check_step_sequence(payload),
        check_dependency_mapping(payload),
        check_cycles(payload),
        check_macro_alignment(payload),
        check_regional_terms(payload, config.get("regional_terms", [])),
        check_step_size(payload, limits),
    ])


# ---------------------------------------------------------------- CLI

def format_text(report: Report) -> str:
    lines = []
    for c in report.checks:
        mark = "PASS" if c.passed else "FAIL"
        lines.append(f"{mark}  {c.id}  {c.name}  [{c.critic_check}]")
        for issue in c.issues:
            lines.append(f"        {issue.where}: {issue.problem}")
    failed = report.failed_ids()
    lines.append("")
    lines.append("All checks pass." if not failed else f"{len(failed)} check(s) failed: {', '.join(failed)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m lsb.validate", description=__doc__.split("\n\n")[0])
    ap.add_argument("payload", type=Path, help="MLS_DAG_Sequence JSON file")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    args = ap.parse_args(argv)
    try:
        payload = load_json(args.payload)
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read {args.payload}: {e}", file=sys.stderr)
        return 2
    report = validate(payload)
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) if args.json else format_text(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
