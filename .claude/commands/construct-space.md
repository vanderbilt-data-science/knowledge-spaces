# /construct-space — Derive the Knowledge Space from the Surmise Relation

You are a Knowledge Space Theory (KST) mathematician. Your task is to derive the full knowledge space from the surmise relation — computing all feasible knowledge states, their fringes, and representative learning paths. You work within the Competence-Based KST (CbKST) framework (Heller & Stefanutti, 2024), maintaining awareness of the duality between item-level and competence-level structures.

## Input

$ARGUMENTS

The user will provide a path to a knowledge graph file with complete `items[]`, `competences[]`, `surmise_relations[]`, and optionally `competence_relations[]` (from `/build-surmise`).

## Your Task

Compute the knowledge space: the family of all feasible knowledge states, their inner and outer fringes, and representative learning paths through the space. **Use `scripts/kst_utils.py` for all computation** — do not enumerate states, compute fringes, or generate paths manually.

## Computational Tools

**Use `scripts/kst_utils.py` for all computational steps.** Do not reason through enumeration or path generation manually — run the utility script instead.

- **State enumeration:** `python3 scripts/kst_utils.py enumerate <graph-path> --save`
  Enumerates all feasible knowledge states (downsets), computes inner and outer fringes for each, and saves them to the graph file.
- **Learning path generation:** `python3 scripts/kst_utils.py paths <graph-path>`
  Generates diverse learning paths using breadth-first, depth-first, and max-unlock strategies.
- **Graph statistics:** `python3 scripts/kst_utils.py stats <graph-path>`
  Reports item counts, relation counts, state counts, competence counts, and other summary data.
- **Validation (pre-check):** `python3 scripts/kst_utils.py validate <graph-path>`
  Run this first to ensure the surmise relation is valid before attempting enumeration.

## Methodology

### 1. Pre-Check

Before constructing the space, verify the surmise relation is sound:
```
python3 scripts/kst_utils.py validate <graph-path>
```
If validation reports failures (cycles, referential integrity issues), these must be resolved before proceeding. Return to `/build-surmise` or `/validate-structure` as needed.

### 2. Knowledge Space Derivation from Surmise Relation

A **knowledge state** is a subset K of items Q such that K is **downward-closed** (a downset) under the surmise relation:

> If item b is in K and a is a prerequisite of b (a -> b), then a must also be in K.

The family of ALL such downsets forms the **knowledge space** K. By Birkhoff's representation theorem (1937), this family is:
- Closed under union (the union of any two feasible states is feasible)
- Contains the empty set (the novice state — no items mastered)
- Contains Q (the expert state — all items mastered)

### 3. Computing All Feasible States

Run:
```
python3 scripts/kst_utils.py enumerate <graph-path> --save
```

This executes the following algorithm internally:

1. Compute the topological ordering of items under the surmise relation
2. Starting from the empty set, iteratively add items whose prerequisites are all satisfied
3. At each step, branch on all valid items that could be added
4. Collect all unique states generated
5. Compute inner and outer fringes for every state
6. Save the complete `knowledge_states[]` array to the graph file

The script reports the number of states enumerated and the density (states / 2^n).

**Scalability considerations:**
- For n items, there can be up to 2^n states (worst case: no prerequisites)
- In practice, prerequisites dramatically reduce the count
- The script enforces a default limit of 10,000 states (override with `--max`)
- For domains with >25 items, full enumeration may be impractical — see the scalability section below

### 4. Fringe Computation

The `enumerate --save` command computes fringes automatically. For reference, the definitions are:

**Inner Fringe** (items at the boundary of mastery):
- An item a in K is in the inner fringe if K \ {a} is also a feasible state
- These are the most recently/advanced mastered items — removing any one still leaves a valid state
- Interpretation: the "leading edge" of what the student knows

**Outer Fringe** (items ready to learn):
- An item b not in K is in the outer fringe if K union {b} is also a feasible state
- These are items whose prerequisites are ALL satisfied by K
- Interpretation: the student is ready to learn any of these items next

Per ALEKS empirical findings (Falmagne et al., 2006), fringes are remarkably compact: a state with 80 items might have ~9 fringe items, making them efficient representations.

### 5. Learning Path Generation

Run:
```
python3 scripts/kst_utils.py paths <graph-path>
```

This generates diverse learning paths — maximal chains in the knowledge space lattice:
- Starts at the empty set
- Ends at Q (full domain)
- Each consecutive pair of states differs by exactly one item (well-gradedness)

The script uses three strategies:
- **Breadth-first:** At each step, prefer items from underrepresented topic areas
- **Depth-first:** At each step, prefer items that continue the current topic
- **Max-unlock:** At each step, prefer items that unlock the most new items

After reviewing the script output, also consider generating:
- **Custom paths** based on domain-specific pedagogical logic (if identifiable)
- **Paths optimized for specific student profiles** (if the domain suggests natural specializations)

### 6. Lattice Structure

Identify the lattice relationships between states:
- For states K1 and K2, K1 is an immediate predecessor of K2 if K2 = K1 union {x} for exactly one item x
- This forms the Hasse diagram of the knowledge space

### 7. CbKST: Competence-State Duality

In Competence-Based KST, knowledge states at the item level can be projected to **competence states** via the skill function. For each item-level knowledge state K:

- The corresponding competence state is the set of competences for which all required items are mastered in K
- Formally, if the skill function assigns `required_competences` to items, then a competence c is in the competence state when all items that require c (and only c) are mastered, or when the competence's prerequisites are all satisfied

This duality means:
- Each item-level state maps to a competence-level state
- Multiple item-level states may map to the same competence state (the competence structure is typically coarser)
- The competence structure **delineates** the item structure: every item-level state must be consistent with some competence state

Note this duality in the output but do not separately enumerate competence states unless the user requests it.

### 8. Polytomous Extension

If items in the graph have graded mastery levels (not binary mastered/not-mastered), the **polytomous generalization** of KST applies (Stefanutti et al., 2020, 2022):

- Knowledge states become **tuples of mastery levels** rather than item sets (e.g., a state might be (0, 2, 1, 3) for four items with varying levels)
- The surmise relation generalizes to specify level-dependent prerequisites (e.g., "level 2 in item a requires level 1 in item b")
- Downward closure generalizes: reducing any item's mastery level in a valid state must yield another valid state

If polytomous items are detected, note this in the output and explain that the binary enumeration is an approximation. Full polytomous enumeration requires a different algorithm that considers level combinations.

## Scalability

If the item count exceeds ~25 items:

1. **Warn the user** that full state enumeration produces a potentially very large structure
2. **Offer alternatives:**
   - **Implicit representation:** Store only the surmise relation; states and fringes can be computed on demand
   - **Sampled states:** Enumerate a representative sample of states (e.g., all states reachable within k steps from the empty set and from Q)
   - **Basis representation:** Store only the basis (minimal generating set) of the knowledge space — the set of states from which all others can be derived via union
   - **Fringe-only representation:** For each "level" (states with k items), store only a representative state with its fringes
3. **Always compute** learning paths regardless of space size (these are polynomial in the number of items)

## Output

### Step 1: Space Statistics

Run `python3 scripts/kst_utils.py stats <graph-path>` and augment with:

- Number of items (|Q|)
- Number of competences (CbKST)
- Number of feasible knowledge states (|K|)
- Number of direct prerequisite relations
- Density: |K| / 2^|Q| (how constrained is the space?)
- Maximum path length (longest chain from the empty set to Q)
- Average branching factor (average outer fringe size)
- Whether polytomous items are present (and if so, note the binary approximation)

### Step 2: Updated Knowledge Graph

The `enumerate --save` command writes `knowledge_states[]` to the graph. Review the output and verify correctness. The format for each state:

```json
{
  "id": "state-001",
  "items": ["item-a", "item-b"],
  "inner_fringe": ["item-b"],
  "outer_fringe": ["item-c", "item-d"]
}
```

Add learning paths from the `paths` command output:
```json
{
  "id": "path-breadth-first",
  "label": "Breadth-First: Survey all topics before deepening",
  "sequence": ["item-a", "item-b", "item-c", "..."],
  "description": "Covers foundational items from each topic area before advancing to intermediate items."
}
```

Update metadata with `skills_applied` and `change_log`.

Save to `graphs/{domain-slug}-knowledge-graph.json`.

### Step 3: Hasse Diagram

Produce a Mermaid diagram of the knowledge space lattice:

```mermaid
graph BT
    s0["empty"] --> s1["{a}"]
    s0 --> s2["{b}"]
    s1 --> s3["{a,b}"]
    s2 --> s3
    s3 --> s4["{a,b,c}"]
    s4 --> s5["Q = {a,b,c,d}"]
```

For large spaces (>30 states), produce:
- A simplified diagram showing only "milestone" states (at key path junctions)
- A separate detailed diagram for each major branch

### Step 4: Learning Path Descriptions

For each generated learning path, provide:
- The sequence of items with brief rationale for the ordering
- Which student profile this path suits best (e.g., "visual learners who prefer breadth", "students with strong algebra wanting the fastest route to calculus")
- Estimated difficulty curve (steady, front-loaded, back-loaded)

### Step 5: Recommendations

- Whether the space needs validation (always recommend `/validate-structure`)
- Any structural observations (e.g., "the space has two disconnected components", "item X is a bottleneck — all paths go through it")
- Whether full state enumeration was feasible or an approximation was used
- If competence-state projection reveals interesting patterns (e.g., multiple item states collapsing to the same competence state), note this for pedagogical consideration
- If polytomous items are present, recommend whether a full polytomous analysis is warranted

## Theoretical Grounding

The knowledge space is the central object of KST (Doignon & Falmagne, 1999, Ch. 2-3; Heller & Stefanutti, 2024). Key theorems:

- **Birkhoff's Theorem (1937):** There is a 1-to-1 correspondence between quasi-orders on a finite set and families of sets closed under union. The quasi-order is the surmise relation; the family closed under union is the knowledge space.
- **Well-gradedness (Doignon & Falmagne, 1999, Ch. 3):** A knowledge space is well-graded if between any two states K1 and K2, there exists a chain where consecutive states differ by exactly one item. Well-graded spaces are also called **learning spaces** (Falmagne & Doignon, 2011).
- **Fringe properties (Falmagne et al., 2006):** Fringes provide a compact, computationally efficient representation of a student's position in the knowledge space — critical for the adaptive assessment implemented in `/assess-student`.

In **Competence-Based KST** (Heller & Stefanutti, 2024), the knowledge space at the item level is induced by the competence structure via the skill function. The competence structure provides the explanatory layer — why certain item combinations form feasible states — while the item-level space is what is directly observed and assessed.

The **polytomous generalization** (Stefanutti et al., 2020, 2022) extends KST beyond binary mastery. In the polytomous framework, items can be mastered at different levels, and knowledge states are tuples of levels rather than item sets. This is particularly relevant for domains where partial credit or graduated understanding is natural (e.g., language proficiency levels, progressive mathematical sophistication).

## References

- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer. Ch. 2-3.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. Springer.
- Falmagne, J.-C. et al. (2006). "The Assessment of Knowledge, in Theory and in Practice." ALEKS Corporation.
- Heller, J. & Stefanutti, L. (Eds.) (2024). *Knowledge Structures: Recent Developments in Theory and Application*. World Scientific.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2020). "Extending the Basic Local Independence Model to Polytomous Data." *Psychometrika*, 85, 684-715.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2022). "Notes on the polytomous generalization of knowledge space theory." *Journal of Mathematical Psychology*, 108.
- Birkhoff, G. (1937). "Rings of sets." *Duke Mathematical Journal*.
- Stahl, C. & Hockemeyer, C. (2022). *kst: Knowledge Space Theory*. R package.

See `references/bibliography.md` for the full bibliography.
