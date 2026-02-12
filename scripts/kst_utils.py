"""
KST Utility Functions — Knowledge Space Theory Computations

Provides computational functions for the KST skill pipeline:
- Graph loading/saving with schema awareness
- Transitive closure of surmise relations
- Downset (knowledge state) enumeration
- Fringe computation (inner and outer)
- Learning path generation
- BLIM Bayesian state updating for adaptive assessment
- Validation checks
- Class-wide analytics

Usage from skills:
    Read and adapt the code in scripts/kst_utils.py. Run with:
    python3 scripts/kst_utils.py <command> <graph-path> [options]

Dependencies: Python 3.9+ standard library only (json, itertools, collections).
"""

import json
import sys
from collections import defaultdict
from itertools import combinations
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Graph I/O
# ---------------------------------------------------------------------------

def load_graph(path: str) -> dict:
    """Load a knowledge graph JSON file."""
    with open(path) as f:
        return json.load(f)


def save_graph(graph: dict, path: str) -> None:
    """Save a knowledge graph JSON file with pretty formatting."""
    with open(path, "w") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"Saved graph to {path}")


# ---------------------------------------------------------------------------
# Surmise Relation Operations
# ---------------------------------------------------------------------------

def build_adjacency(graph: dict) -> dict[str, set[str]]:
    """Build prerequisite adjacency: adj[target] = {prerequisites}."""
    adj: dict[str, set[str]] = defaultdict(set)
    for rel in graph.get("surmise_relations", []):
        adj[rel["target"]].add(rel["prerequisite"])
    return adj


def build_successor_map(graph: dict) -> dict[str, set[str]]:
    """Build successor adjacency: succ[prerequisite] = {targets}."""
    succ: dict[str, set[str]] = defaultdict(set)
    for rel in graph.get("surmise_relations", []):
        succ[rel["prerequisite"]].add(rel["target"])
    return succ


def transitive_closure(graph: dict) -> list[dict]:
    """
    Compute the transitive closure of surmise relations.
    Returns list of new relations to add (only those not already present).
    Uses Warshall's algorithm.
    """
    item_ids = [item["id"] for item in graph["items"]]
    n = len(item_ids)
    idx = {iid: i for i, iid in enumerate(item_ids)}

    # Build reachability matrix from existing relations
    reach = [[False] * n for _ in range(n)]
    existing_pairs = set()
    for rel in graph.get("surmise_relations", []):
        p, t = rel["prerequisite"], rel["target"]
        if p in idx and t in idx:
            reach[idx[p]][idx[t]] = True
            existing_pairs.add((p, t))

    # Warshall's algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True

    # Collect new transitive relations
    new_relations = []
    for i in range(n):
        for j in range(n):
            if i != j and reach[i][j]:
                pair = (item_ids[i], item_ids[j])
                if pair not in existing_pairs:
                    new_relations.append({
                        "prerequisite": pair[0],
                        "target": pair[1],
                        "confidence": 1.0,
                        "rationale": f"Transitive closure",
                        "relation_type": "prerequisite-of",
                        "source": "transitive-closure"
                    })

    return new_relations


def detect_cycles(graph: dict) -> list[list[str]]:
    """
    Detect cycles in the surmise relation using DFS.
    Returns list of cycles found (each cycle is a list of item IDs).
    An empty list means the relation is acyclic (valid).
    """
    adj = build_successor_map(graph)
    item_ids = {item["id"] for item in graph["items"]}

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {iid: WHITE for iid in item_ids}
    parent = {}
    cycles = []

    def dfs(u, path):
        color[u] = GRAY
        path.append(u)
        for v in adj.get(u, set()):
            if v not in color:
                continue
            if color[v] == GRAY:
                # Found cycle: extract it from path
                cycle_start = path.index(v)
                cycles.append(path[cycle_start:] + [v])
            elif color[v] == WHITE:
                dfs(v, path)
        path.pop()
        color[u] = BLACK

    for iid in item_ids:
        if color[iid] == WHITE:
            dfs(iid, [])

    return cycles


# ---------------------------------------------------------------------------
# Knowledge State Enumeration
# ---------------------------------------------------------------------------

def enumerate_downsets(graph: dict, max_states: int = 10000) -> list[frozenset[str]]:
    """
    Enumerate all downward-closed sets (feasible knowledge states)
    of the surmise relation.

    A set K is downward-closed if: for every item b in K,
    all prerequisites of b are also in K.

    Uses BFS from the empty set, adding one valid item at a time.
    Stops if max_states is exceeded (returns partial results with warning).
    """
    adj = build_adjacency(graph)
    item_ids = {item["id"] for item in graph["items"]}

    # Items with no prerequisites can be added first
    states: set[frozenset[str]] = set()
    queue = [frozenset()]
    states.add(frozenset())

    while queue:
        if len(states) >= max_states:
            print(f"WARNING: State enumeration stopped at {max_states} states. "
                  f"Domain may be too large for full enumeration.", file=sys.stderr)
            break

        current = queue.pop(0)
        # Find items that can be added (all prerequisites satisfied)
        for iid in item_ids - current:
            prereqs = adj.get(iid, set())
            if prereqs <= current:  # All prerequisites in current state
                new_state = current | {iid}
                if new_state not in states:
                    states.add(new_state)
                    queue.append(new_state)

    return sorted(states, key=lambda s: (len(s), sorted(s)))


def compute_fringes(
    state: frozenset[str],
    all_states: set[frozenset[str]],
    item_ids: set[str]
) -> tuple[list[str], list[str]]:
    """
    Compute inner and outer fringes of a knowledge state.

    Inner fringe: items in state whose removal yields another valid state.
    Outer fringe: items outside state whose addition yields another valid state.
    """
    inner = []
    for item in state:
        candidate = state - {item}
        if candidate in all_states:
            inner.append(item)

    outer = []
    for item in item_ids - state:
        candidate = state | {item}
        if candidate in all_states:
            outer.append(item)

    return sorted(inner), sorted(outer)


# ---------------------------------------------------------------------------
# Learning Path Generation
# ---------------------------------------------------------------------------

def generate_learning_paths(
    graph: dict,
    all_states: list[frozenset[str]],
    strategy: str = "breadth-first",
    max_paths: int = 5
) -> list[list[str]]:
    """
    Generate learning paths (maximal chains from empty set to Q).

    Strategies:
    - 'breadth-first': prefer items from underrepresented topics
    - 'depth-first': prefer items continuing current topic
    - 'max-unlock': prefer items that unlock the most new items
    """
    adj = build_adjacency(graph)
    succ = build_successor_map(graph)
    item_ids = {item["id"] for item in graph["items"]}
    state_set = set(all_states)

    full_domain = frozenset(item_ids)
    if full_domain not in state_set:
        print("WARNING: Full domain is not a valid state. Paths may be partial.",
              file=sys.stderr)

    paths = []

    def build_path(score_fn) -> list[str]:
        """Build a single path using a scoring function for item selection."""
        current = frozenset()
        path = []
        while current != full_domain:
            # Find addable items
            candidates = []
            for iid in item_ids - current:
                prereqs = adj.get(iid, set())
                if prereqs <= current:
                    candidate_state = current | {iid}
                    if candidate_state in state_set:
                        candidates.append(iid)
            if not candidates:
                break
            # Score and select
            candidates.sort(key=lambda x: (-score_fn(x, current, path), x))
            chosen = candidates[0]
            path.append(chosen)
            current = current | {chosen}
        return path

    def score_max_unlock(item, current, path):
        """Score by how many new items this unlocks."""
        new_state = current | {item}
        count = 0
        for candidate in item_ids - new_state:
            prereqs = adj.get(candidate, set())
            if prereqs <= new_state:
                count += 1
        return count

    def score_depth_first(item, current, path):
        """Score by tag overlap with most recent item."""
        if not path:
            return 0
        items_by_id = {it["id"]: it for it in graph["items"]}
        last_tags = set(items_by_id.get(path[-1], {}).get("tags", []))
        item_tags = set(items_by_id.get(item, {}).get("tags", []))
        return len(last_tags & item_tags)

    def score_breadth_first(item, current, path):
        """Score by inverse frequency of item's tags in path so far."""
        items_by_id = {it["id"]: it for it in graph["items"]}
        tag_counts = defaultdict(int)
        for p in path:
            for t in items_by_id.get(p, {}).get("tags", []):
                tag_counts[t] += 1
        item_tags = items_by_id.get(item, {}).get("tags", [])
        if not item_tags:
            return 0
        return -sum(tag_counts.get(t, 0) for t in item_tags) / len(item_tags)

    scorers = {
        "breadth-first": score_breadth_first,
        "depth-first": score_depth_first,
        "max-unlock": score_max_unlock,
    }

    for name, scorer in scorers.items():
        path = build_path(scorer)
        if path:
            paths.append(path)

    return paths[:max_paths]


# ---------------------------------------------------------------------------
# BLIM — Bayesian Assessment
# ---------------------------------------------------------------------------

def blim_update(
    state_probs: dict[str, float],
    states: dict[str, set[str]],
    item_id: str,
    response_correct: bool,
    lucky_guess: float = 0.1,
    careless_error: float = 0.1
) -> dict[str, float]:
    """
    Bayesian update of knowledge state probabilities given a response.

    Parameters:
    - state_probs: {state_id: probability} current distribution
    - states: {state_id: set of item IDs in that state}
    - item_id: which item was assessed
    - response_correct: whether the student answered correctly
    - lucky_guess (g): P(correct | not mastered)
    - careless_error (s): P(incorrect | mastered)

    Returns updated state probabilities (normalized).
    """
    updated = {}
    for sid, prob in state_probs.items():
        item_in_state = item_id in states[sid]
        if response_correct:
            likelihood = (1 - careless_error) if item_in_state else lucky_guess
        else:
            likelihood = careless_error if item_in_state else (1 - lucky_guess)
        updated[sid] = prob * likelihood

    # Normalize
    total = sum(updated.values())
    if total > 0:
        for sid in updated:
            updated[sid] /= total
    return updated


def select_assessment_item(
    state_probs: dict[str, float],
    states: dict[str, set[str]],
    assessed_items: set[str],
    all_item_ids: set[str]
) -> str | None:
    """
    Select the next item to assess for maximum information gain.

    Heuristic: choose the item where ~50% of probability mass has it
    mastered and ~50% doesn't (maximum discrimination).
    """
    best_item = None
    best_score = float("inf")  # Closest to 0.5

    for item_id in all_item_ids - assessed_items:
        prob_mastered = sum(
            prob for sid, prob in state_probs.items()
            if item_id in states[sid]
        )
        # Score = distance from 0.5 (lower is better)
        score = abs(prob_mastered - 0.5)
        if score < best_score:
            best_score = score
            best_item = item_id

    return best_item


def entropy(probs: dict[str, float]) -> float:
    """Compute Shannon entropy of a probability distribution."""
    import math
    return -sum(p * math.log2(p) for p in probs.values() if p > 0)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_graph(graph: dict) -> dict[str, list[str]]:
    """
    Run validation checks on a knowledge graph.

    Returns: {"fail": [...], "warn": [...], "pass": [...]}
    """
    results: dict[str, list[str]] = {"fail": [], "warn": [], "pass": []}
    item_ids = {item["id"] for item in graph["items"]}

    # --- Mathematical checks ---

    # Referential integrity
    bad_refs = []
    for rel in graph.get("surmise_relations", []):
        if rel["prerequisite"] not in item_ids:
            bad_refs.append(rel["prerequisite"])
        if rel["target"] not in item_ids:
            bad_refs.append(rel["target"])
    if bad_refs:
        results["fail"].append(
            f"Referential integrity: {len(bad_refs)} relation(s) reference "
            f"non-existent items: {bad_refs[:5]}")
    else:
        results["pass"].append("Referential integrity: all relation IDs valid")

    # Duplicate relations
    pairs = [(r["prerequisite"], r["target"]) for r in graph.get("surmise_relations", [])]
    dupes = len(pairs) - len(set(pairs))
    if dupes:
        results["fail"].append(f"Duplicate relations: {dupes} duplicate(s) found")
    else:
        results["pass"].append("No duplicate relations")

    # Cycles
    cycles = detect_cycles(graph)
    if cycles:
        results["fail"].append(
            f"Acyclicity: {len(cycles)} cycle(s) detected: {cycles[:3]}")
    else:
        results["pass"].append("Acyclicity: no cycles detected")

    # Transitivity
    new_transitive = transitive_closure(graph)
    if new_transitive:
        results["warn"].append(
            f"Transitivity: {len(new_transitive)} implied relation(s) missing "
            f"from explicit surmise_relations")
    else:
        results["pass"].append("Transitivity: relation is transitively closed")

    # Self-loops
    self_loops = [r for r in graph.get("surmise_relations", [])
                  if r["prerequisite"] == r["target"]]
    if self_loops:
        results["warn"].append(
            f"Self-loops: {len(self_loops)} explicit self-loop(s) found "
            f"(reflexivity should be implicit)")
    else:
        results["pass"].append("No explicit self-loops")

    # Unique IDs
    ids = [item["id"] for item in graph["items"]]
    if len(ids) != len(set(ids)):
        results["fail"].append("Item ID uniqueness: duplicate IDs found")
    else:
        results["pass"].append("Item IDs are unique")

    # --- Educational plausibility ---

    adj = build_adjacency(graph)

    # Max direct prerequisites
    for iid in item_ids:
        prereq_count = len(adj.get(iid, set()))
        if prereq_count > 7:
            results["warn"].append(
                f"Prerequisite load: '{iid}' has {prereq_count} direct "
                f"prerequisites (>7, cognitive load concern)")

    # Orphan check
    has_prereq = set()
    is_prereq = set()
    for rel in graph.get("surmise_relations", []):
        has_prereq.add(rel["target"])
        is_prereq.add(rel["prerequisite"])
    orphans = item_ids - has_prereq - is_prereq
    if orphans and len(item_ids) > 1:
        results["warn"].append(
            f"Orphaned items: {len(orphans)} item(s) with no prerequisite "
            f"relationships: {sorted(orphans)[:5]}")

    # Bloom's level consistency
    items_by_id = {item["id"]: item for item in graph["items"]}
    bloom_order = {"remember": 0, "understand": 1, "apply": 2,
                   "analyze": 3, "evaluate": 4, "create": 5}
    inversions = []
    for rel in graph.get("surmise_relations", []):
        prereq = items_by_id.get(rel["prerequisite"], {})
        target = items_by_id.get(rel["target"], {})
        p_level = bloom_order.get(prereq.get("bloom_level", ""), -1)
        t_level = bloom_order.get(target.get("bloom_level", ""), -1)
        if p_level > t_level and t_level >= 0:
            inversions.append((rel["prerequisite"], rel["target"]))
    if inversions:
        results["warn"].append(
            f"Bloom's level inversions: {len(inversions)} case(s) where "
            f"prerequisite has higher Bloom's level than target: "
            f"{inversions[:3]}")

    # Knowledge states validation (if present)
    ks = graph.get("knowledge_states", [])
    if ks:
        state_sets = [frozenset(s["items"]) for s in ks]
        # Empty set present
        if frozenset() not in state_sets:
            results["warn"].append(
                "Knowledge states: empty set (novice state) not present")
        # Full set present
        if frozenset(item_ids) not in state_sets:
            results["warn"].append(
                "Knowledge states: full domain (expert state) not present")
        # Union closure (sample check for performance)
        if len(state_sets) <= 500:
            state_set = set(state_sets)
            union_failures = 0
            for s1, s2 in combinations(state_sets, 2):
                if (s1 | s2) not in state_set:
                    union_failures += 1
                    if union_failures >= 3:
                        break
            if union_failures:
                results["fail"].append(
                    f"Union closure: {union_failures}+ pair(s) whose union "
                    f"is not a valid state")
            else:
                results["pass"].append("Union closure: verified")

    return results


# ---------------------------------------------------------------------------
# Class-Wide Analytics
# ---------------------------------------------------------------------------

def class_analytics(graph: dict) -> dict[str, Any]:
    """
    Compute class-wide analytics from student states.

    Returns dict with:
    - mastery_rates: {item_id: fraction of students who mastered it}
    - outer_fringe_freq: {item_id: count of students with this in outer fringe}
    - target_scores: {item_id: composite score for instruction targeting}
    - clusters: list of student groups by state similarity
    """
    students = graph.get("student_states", {})
    item_ids = {item["id"] for item in graph["items"]}
    succ = build_successor_map(graph)

    if not students:
        return {"error": "No student states found"}

    # Mastery rates
    mastery_counts: dict[str, int] = defaultdict(int)
    for sid, sdata in students.items():
        state = sdata.get("current_state", [])
        if isinstance(state, list):
            for iid in state:
                mastery_counts[iid] += 1

    n_students = len(students)
    mastery_rates = {iid: mastery_counts.get(iid, 0) / n_students
                     for iid in item_ids}

    # Outer fringe frequency
    fringe_counts: dict[str, int] = defaultdict(int)
    for sid, sdata in students.items():
        for iid in sdata.get("outer_fringe", []):
            fringe_counts[iid] += 1

    # Leverage: how many items does mastering this unlock?
    leverage = {}
    for iid in item_ids:
        leverage[iid] = len(succ.get(iid, set()))

    # Composite target score
    target_scores = {}
    for iid in item_ids:
        fringe_freq = fringe_counts.get(iid, 0) / max(n_students, 1)
        lev = leverage.get(iid, 0) / max(len(item_ids), 1)
        need = 1 - mastery_rates.get(iid, 0)
        target_scores[iid] = fringe_freq * (1 + lev) * need

    # Student clustering by Jaccard similarity
    student_ids = list(students.keys())
    student_sets = {}
    for sid in student_ids:
        state = students[sid].get("current_state", [])
        student_sets[sid] = set(state) if isinstance(state, list) else set()

    # Simple greedy clustering (for small class sizes)
    clusters = []
    assigned = set()
    for sid in student_ids:
        if sid in assigned:
            continue
        cluster = [sid]
        assigned.add(sid)
        for other in student_ids:
            if other in assigned:
                continue
            s1, s2 = student_sets[sid], student_sets[other]
            union = s1 | s2
            jaccard = len(s1 & s2) / len(union) if union else 1.0
            if jaccard >= 0.6:
                cluster.append(other)
                assigned.add(other)
        clusters.append(cluster)

    return {
        "mastery_rates": mastery_rates,
        "outer_fringe_freq": dict(fringe_counts),
        "target_scores": target_scores,
        "leverage": leverage,
        "clusters": clusters,
        "n_students": n_students,
    }


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 kst_utils.py <command> <graph-path> [options]")
        print()
        print("Commands:")
        print("  validate          Run validation checks")
        print("  closure           Compute transitive closure")
        print("  enumerate         Enumerate knowledge states")
        print("  paths             Generate learning paths")
        print("  analytics         Compute class-wide analytics")
        print("  cycles            Detect cycles in surmise relation")
        print("  stats             Print graph statistics")
        sys.exit(1)

    command = sys.argv[1]
    graph_path = sys.argv[2]
    graph = load_graph(graph_path)

    if command == "validate":
        results = validate_graph(graph)
        for level in ["fail", "warn", "pass"]:
            for msg in results[level]:
                print(f"[{level.upper()}] {msg}")
        n_fail = len(results["fail"])
        n_warn = len(results["warn"])
        n_pass = len(results["pass"])
        print(f"\nSummary: {n_fail} FAIL, {n_warn} WARN, {n_pass} PASS")
        sys.exit(1 if n_fail > 0 else 0)

    elif command == "closure":
        new_rels = transitive_closure(graph)
        if new_rels:
            print(f"Found {len(new_rels)} missing transitive relations:")
            for r in new_rels:
                print(f"  {r['prerequisite']} -> {r['target']}")
            if "--apply" in sys.argv:
                graph["surmise_relations"].extend(new_rels)
                save_graph(graph, graph_path)
                print(f"Applied {len(new_rels)} relations to graph.")
        else:
            print("Relation is already transitively closed.")

    elif command == "enumerate":
        max_states = 10000
        if "--max" in sys.argv:
            idx = sys.argv.index("--max")
            max_states = int(sys.argv[idx + 1])
        states = enumerate_downsets(graph, max_states)
        print(f"Enumerated {len(states)} feasible knowledge states")
        print(f"Domain size: {len(graph['items'])} items")
        print(f"Density: {len(states)} / {2**len(graph['items'])} = "
              f"{len(states) / (2**len(graph['items'])):.4f}")
        if "--save" in sys.argv:
            item_ids = {item["id"] for item in graph["items"]}
            all_states_set = set(states)
            ks = []
            for i, state in enumerate(states):
                inner, outer = compute_fringes(state, all_states_set, item_ids)
                ks.append({
                    "id": f"state-{i:04d}",
                    "items": sorted(state),
                    "inner_fringe": inner,
                    "outer_fringe": outer
                })
            graph["knowledge_states"] = ks
            save_graph(graph, graph_path)

    elif command == "paths":
        states = enumerate_downsets(graph)
        paths = generate_learning_paths(graph, states)
        for i, path in enumerate(paths):
            strategies = ["breadth-first", "depth-first", "max-unlock"]
            name = strategies[i] if i < len(strategies) else f"path-{i}"
            print(f"\n{name}: {' -> '.join(path)}")
            print(f"  Length: {len(path)} items")

    elif command == "analytics":
        results = class_analytics(graph)
        if "error" in results:
            print(results["error"])
            sys.exit(1)
        print(f"Students: {results['n_students']}")
        print(f"Clusters: {len(results['clusters'])}")
        print("\nTop teaching targets (by composite score):")
        sorted_targets = sorted(results["target_scores"].items(),
                                key=lambda x: -x[1])
        for iid, score in sorted_targets[:10]:
            rate = results["mastery_rates"].get(iid, 0)
            freq = results["outer_fringe_freq"].get(iid, 0)
            print(f"  {iid}: score={score:.3f} mastery={rate:.0%} "
                  f"fringe_freq={freq}")

    elif command == "cycles":
        cycles = detect_cycles(graph)
        if cycles:
            print(f"FAIL: {len(cycles)} cycle(s) detected:")
            for c in cycles:
                print(f"  {' -> '.join(c)}")
            sys.exit(1)
        else:
            print("PASS: No cycles detected (valid quasi-order)")

    elif command == "stats":
        n_items = len(graph["items"])
        n_rels = len(graph.get("surmise_relations", []))
        n_states = len(graph.get("knowledge_states", []))
        n_paths = len(graph.get("learning_paths", []))
        n_students = len(graph.get("student_states", {}))
        n_competences = len(graph.get("competences", []))
        print(f"Domain: {graph['metadata'].get('domain_name', 'unknown')}")
        print(f"Version: {graph['metadata'].get('version', 'unknown')}")
        print(f"Items: {n_items}")
        print(f"Surmise relations: {n_rels}")
        print(f"Knowledge states: {n_states}")
        print(f"Learning paths: {n_paths}")
        print(f"Students tracked: {n_students}")
        print(f"Competences (CbKST): {n_competences}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
