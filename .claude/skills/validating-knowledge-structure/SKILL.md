---
name: Validating Knowledge Structure
description: >
  Use when you need to validate a knowledge graph for mathematical
  consistency, educational plausibility, CbKST integrity, and schema
  conformance. Runs automated validation via scripts/kst_utils.py then
  performs reasoning-based checks. Produces a structured PASS/WARN/FAIL
  report. Reads/produces knowledge graphs in graphs/*.json.
  Part of the KST pipeline — Phase 2, follows /constructing-knowledge-space.
---

# Validating Knowledge Structure

## Role

You are a KST quality assurance analyst validating knowledge graphs for mathematical consistency, educational plausibility, completeness, and CbKST integrity. You ensure the knowledge structure satisfies KST axioms (Doignon & Falmagne, 1999), CbKST alignment (Heller & Stefanutti, 2024), and educational soundness before the graph enters Phase 3 application skills.

## Input

$ARGUMENTS

The user provides:
- A path to a complete knowledge graph file (with items, surmise relations, and optionally competences, competence relations, knowledge states, learning paths)
- Optionally, original course materials for coverage checking

Load the graph and verify it conforms to `schemas/knowledge-graph.schema.json`.

## Step 0: Automated Validation

Run the automated validation script as the first step:

```bash
python3 scripts/kst_utils.py validate <graph-path>
```

This checks:
- Referential integrity (all IDs in relations reference existing items)
- Duplicate relations
- Acyclicity (no cycles in surmise relation)
- Transitivity (all transitive relations present)
- Self-loops (reflexivity should be implicit)
- Item ID uniqueness
- Knowledge state properties (if populated): empty set, full set, union closure
- Bloom's level consistency
- Prerequisite load (>7 direct prerequisites)
- Orphaned items

Review the FAIL/WARN/PASS output, then perform the additional reasoning-based checks below.

## Validation Checks

### Category 1: Mathematical Validity

Hard requirements -- failures mean the structure is mathematically incorrect. See `shared-references/kst-foundations.md` for formal definitions.

**1.1 Surmise Relation Properties:**
- [ ] Transitivity: for all a -> b and b -> c, a -> c exists. Fix: `python3 scripts/kst_utils.py closure <graph-path> --apply`
- [ ] Acyclicity: no cycles among distinct items
- [ ] Referential integrity: all IDs in surmise_relations reference items in items[]
- [ ] No self-loops: no explicit (a -> a) entries
- [ ] No duplicate relations: no repeated (prerequisite, target) pairs

**1.2 Knowledge State Properties** (if knowledge_states[] populated):
- [ ] Empty set present (novice state)
- [ ] Full set present (expert state, containing all items)
- [ ] Union closure: the union of any two states is also a valid state
- [ ] Downward closure: every state is a downset of the surmise relation
- [ ] Well-gradedness: between any two states K1 subset K2, there exists a chain where consecutive states differ by exactly one item

**1.3 Fringe Correctness** (if fringes computed):
- [ ] Inner fringe valid: for each item a in a state's inner fringe, removing a yields a valid state
- [ ] Outer fringe valid: for each item b in a state's outer fringe, adding b yields a valid state
- [ ] Inner fringe complete: no missing removable items
- [ ] Outer fringe complete: no missing addable items

**1.4 Learning Path Properties** (if learning_paths[] populated):
- [ ] Maximality: each path starts from the empty-set-equivalent and ends at Q
- [ ] Validity: the cumulative item set at each step is a valid state
- [ ] Single-step: consecutive items add exactly one item to the cumulative set

### Category 2: CbKST Validity

Reasoning-based checks for Competence-Based KST consistency. Not covered by the automated script. See `shared-references/cbkst-overview.md`.

**2.1 Competence Referential Integrity:**
- [ ] All competence IDs in items' `required_competences` fields exist in `competences[]`
- [ ] All IDs in `competence_relations[]` reference competences in `competences[]`

**2.2 Competence Relation Consistency:**
- [ ] Alignment: if c1 -> c2 in competence_relations, items requiring c2 should generally have items requiring c1 as prerequisites. Flag misalignments.
- [ ] Competence-level transitivity: competence prerequisites are transitive and acyclic
- [ ] No competence cycles

**2.3 Skill Function Coverage:**
- [ ] Every item has at least one `required_competences` entry
- [ ] Every competence is required by at least one item
- [ ] No excessive concentration: no single competence required by >70% of items

**2.4 Delineation Check:**
- [ ] Every feasible item-level state is consistent with some competence assignment
- [ ] If multiple item states map to the same competence state, verify this is intentional (genuine coarseness, not missing distinctions)

### Category 3: Polytomous Validity (When Applicable)

Skip if all items are binary. See `shared-references/cbkst-overview.md` for polytomous theory.

**3.1 Level Consistency:**
- [ ] Each item has a well-defined mastery level range with no gaps
- [ ] Level 0 consistently represents non-mastery
- [ ] Different level ranges across items are documented and justified

**3.2 Surmise Relation Consistency:**
- [ ] Level ordering respected: if level k in a requires level m in b, then level < k in a does not require level > m in b
- [ ] Monotonicity: higher prerequisite levels do not relax requirements

### Category 4: Educational Plausibility

Soft checks -- warnings suggesting possible pedagogical issues. See `references/validation-criteria.md` for extended rationale and thresholds.

**4.1 Prerequisite Load:**
- [ ] Max direct prerequisites: no item has >7 direct prerequisites (Miller's 7 +/- 2)
- [ ] Max total prerequisites: no item requires >70% of all items as prerequisites
- [ ] Minimum path length to item is reasonable for course duration

**4.2 Bloom's Level Consistency:**
- [ ] "Remember" items are generally near the base (few prerequisites)
- [ ] No level inversions: "remember" items should not have "evaluate" or "create" prerequisites

**4.3 Structural Balance:**
- [ ] No orphaned items (every item is reachable and can reach Q)
- [ ] No bottleneck items (no single item is a prerequisite for >50% of all others)
- [ ] Balanced branching: ratio of max to min outer fringe size is not extreme

**4.4 Coverage:**
- [ ] All major topics from source materials are represented
- [ ] Items span at least 3 Bloom's levels
- [ ] Items span at least 2 knowledge types

### Category 5: Schema Conformance

- [ ] JSON schema validation against `schemas/knowledge-graph.schema.json`
- [ ] All required fields present
- [ ] ID uniqueness: all item IDs unique, all state IDs unique, all path IDs unique
- [ ] ID format: all IDs match the `^[a-z0-9][a-z0-9-]*[a-z0-9]$` pattern

## Output

### 1. Validation Report

```
## Validation Report for {domain-name}

### Automated Script Results
[Paste output of python3 scripts/kst_utils.py validate <graph-path>]

### Summary
- FAIL: X checks
- WARN: Y checks
- PASS: Z checks

### FAIL
1. [Check 1.1 - Transitivity] Missing transitive relation: item-a -> item-c (via item-b)
   FIX: Run `python3 scripts/kst_utils.py closure <graph-path> --apply`

### WARN
1. [Check 4.1 - Prerequisite Load] Item "item-x" has 9 direct prerequisites
   SUGGESTION: Consider decomposing item-x into sub-items
2. [Check 2.3 - Skill Function Coverage] Competence "comp-y" is not required by any item
   SUGGESTION: Map comp-y to relevant items or remove it

### PASS
1. [Check 1.1 - Acyclicity] No cycles detected
...
```

### 2. Fix Application

**Auto-fixable issues:**
- Run `python3 scripts/kst_utils.py closure <graph-path> --apply` for transitive closure
- Apply other mechanical fixes directly to the graph
- Document each fix in `metadata.provenance.change_log`

**Manual issues:**
- List clearly with suggested options
- Do NOT auto-fix issues requiring human judgment

Save the updated graph to `graphs/{domain-slug}-knowledge-graph.json`.

### 3. Structure Quality Metrics

| Metric | Formula/Description | Interpretation |
|--------|-------------------|----------------|
| Discrimination index | |K| / 2^|Q| | Closer to 0 = more constrained = more useful |
| Average path length | Mean steps from empty set to Q | Reflects domain depth |
| Bottleneck score | Max % of items depending on any single item | >50% suggests decomposition |
| Fringe compactness | Mean fringe size / mean state size | Should be small (per ALEKS data) |
| Competence coverage | Items with required_competences / total items | Should be 1.0 |
| Competence utilization | Competences required by >= 1 item / total competences | Should be 1.0 |

### 4. Empirical Validation (When Student Data Available)

See `references/validation-criteria.md` for detailed methodology.

- **BLIM fit:** Use the `pks` R package (Wickelmaier & Heller, 2024) for goodness-of-fit. Poor fit suggests the structure does not match student response patterns.
- **IITA comparison:** Compare empirically derived surmise relations (via `DAKS` or `learning_spaces`) with expert-derived ones. Investigate discrepancies.
- **Discrepancy index (DI), gamma-index:** Standard KST fit statistics from the `kst` R package (Stahl & Hockemeyer, 2022).

If no student data is available, recommend collecting pilot data.

### 5. Recommendations

- Issues requiring human expert review
- Structural improvements to consider
- CbKST improvements: unmapped competences, alignment issues, delineation concerns
- Whether polytomous modeling would benefit the domain
- Whether the graph is ready for Phase 3 skills (`/assessing-knowledge-state`, `/generating-learning-materials`, `/planning-adaptive-instruction`)

## References

- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. See `references/bibliography.md`.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. See `references/bibliography.md`.
- Heller, J. & Stefanutti, L. (2024). *Knowledge Structures*. See `references/bibliography.md`.
- Wickelmaier, F. & Heller, J. (2024). `pks` R package. See `references/bibliography.md`.
- Stahl, C. & Hockemeyer, C. (2022). `kst` R package. See `references/bibliography.md`.
- Stefanutti, L. et al. (2020, 2022). Polytomous extensions. See `references/bibliography.md`.

See `references/bibliography.md` for the complete bibliography.
