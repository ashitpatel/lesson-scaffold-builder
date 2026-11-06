"""Dependency-graph checks for the `mls_units` array of an MLS_DAG_Sequence.

Each unit is a dict with an `mls_id` and a `dependencies` list of upstream ids.
An edge runs from a unit to each of its prerequisites.
"""

from __future__ import annotations

from collections import Counter


def _graph(mls_units: list[dict]) -> dict[str, list[str]]:
    """Map each id to its declared dependencies (first occurrence wins on duplicates)."""
    graph: dict[str, list[str]] = {}
    for unit in mls_units:
        graph.setdefault(unit["mls_id"], list(unit.get("dependencies", [])))
    return graph


def duplicate_ids(mls_units: list[dict]) -> list[str]:
    counts = Counter(unit["mls_id"] for unit in mls_units)
    return sorted(i for i, n in counts.items() if n > 1)


def missing_dependencies(mls_units: list[dict]) -> list[tuple[str, str]]:
    """(unit id, dependency id) pairs whose dependency is not in the collection."""
    ids = {unit["mls_id"] for unit in mls_units}
    return [
        (unit["mls_id"], dep)
        for unit in mls_units
        for dep in unit.get("dependencies", [])
        if dep not in ids
    ]


def find_cycle(mls_units: list[dict]) -> list[str] | None:
    """Return one dependency cycle as a closed path (e.g. ['A', 'B', 'A']), or None.

    A unit that depends on itself is a cycle of length one: ['A', 'A'].
    Dependencies on ids missing from the collection are ignored here; they are
    reported by `missing_dependencies`.
    """
    graph = _graph(mls_units)
    WHITE, GREY, BLACK = 0, 1, 2
    colour = dict.fromkeys(graph, WHITE)

    for root in graph:
        if colour[root] != WHITE:
            continue
        # Iterative DFS so deep chains cannot hit the recursion limit.
        path = [root]
        stack = [iter(graph[root])]
        colour[root] = GREY
        while stack:
            dep = next(stack[-1], None)
            if dep is None:
                colour[path.pop()] = BLACK
                stack.pop()
                continue
            if dep not in graph:
                continue
            if colour[dep] == GREY:
                return path[path.index(dep):] + [dep]
            if colour[dep] == WHITE:
                colour[dep] = GREY
                path.append(dep)
                stack.append(iter(graph[dep]))
    return None


def has_cycle(mls_units: list[dict]) -> bool:
    return find_cycle(mls_units) is not None


def topological_order(mls_units: list[dict]) -> list[str]:
    """Ids ordered so every unit comes after its prerequisites; ties keep input order.

    Raises ValueError if the graph has a cycle. Missing dependencies are ignored.
    """
    graph = _graph(mls_units)
    remaining = {uid: {d for d in deps if d in graph} for uid, deps in graph.items()}
    order: list[str] = []
    while remaining:
        ready = [uid for uid, deps in remaining.items() if not deps]
        if not ready:
            raise ValueError(f"dependency cycle: {find_cycle(mls_units)}")
        for uid in ready:
            order.append(uid)
            del remaining[uid]
        for deps in remaining.values():
            deps.difference_update(ready)
    return order
