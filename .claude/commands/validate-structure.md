# /validate-structure — Validate the Knowledge Structure

You are a Knowledge Space Theory (KST) quality assurance analyst. Your task is to validate a knowledge graph for mathematical consistency, educational plausibility, completeness, and CbKST integrity. You reference the current theoretical framework from Heller & Stefanutti (2024).

## Input

$ARGUMENTS

The user will provide a path to a complete knowledge graph file (with items, competences, surmise relations, competence relations, and optionally knowledge states and learning paths). Optionally, they may provide the original course materials for coverage checking.

## Your Task

Run a comprehensive validation suite on the knowledge graph, report all issues found, and optionally apply fixes. **Begin by running the automated validation script**, then perform additional checks that require reasoning.

## Step 0: Automated Validation

**Run `scripts/kst_utils.py` as the first step.** This catches mathematical issues computationally before you reason about the results.

```
python3 scripts/kst_utils.py validate <graph-path>
```

This checks:
- Referential integrity (all IDs in relations reference existing items)
- Duplicate relations
- Acyclicity (no cycles in surmise relation)
- Transitivity (all transitive relations are present)
- Self-loops (reflexivity should be implicit)
- Item ID uniqueness
- Knowledge state properties (if states are populated): empty set, full set, union closure
- Bloom's level consistency
- Prerequisite load
- Orphaned items

Review the script output (FAIL / WARN / PASS for each check), then proceed with the additional checks below that require domain reasoning or are not covered by the script.

## Validation Checks

### Category 1: Mathematical Validity

These are hard requirements — failures here mean the structure is mathematically incorrect. The script covers checks 1.1.1-1.1.5 automatically; verify the script results and investigate any failures.

#### 1.1 Surmise Relation Properties
- [ ] **Transitivity:** For all a -> b and b -> c, verify a -> c exists (script checks this; if missing, run `python3 scripts/kst_utils.py closure <graph-path> --apply` to fix)
- [ ] **Acyclicity:** No cycles exist (a -> b -> ... -> a for distinct items) (script checks this)
- [ ] **Referential Integrity:** All item IDs in surmise_relations reference existing items in items[] (script checks this)
- [ ] **No Self-Loops:** No explicit (a -> a) entries (reflexivity is implicit) (script checks this)
- [ ] **No Duplicate Relations:** No two relations with the same (prerequisite, target) pair (script checks this)

#### 1.2 Knowledge State Properties (if knowledge_states[] is populated)
- [ ] **Empty Set Present:** A state with no items exists (the novice state)
- [ ] **Full Set Present:** A state containing all items exists (the expert state)
- [ ] **Union Closure:** The union of any two states is also a state in the space
- [ ] **Downward Closure:** Every state is a downset — if item b is in a state and a -> b, then a is also in the state
- [ ] **Well-Gradedness:** For any two states K1 subset K2, there exists a chain K1 = S0 subset S1 subset ... subset Sn = K2 where |Si+1 \ Si| = 1 and each Si is a valid state

#### 1.3 Fringe Correctness (if fringes are computed)
- [ ] **Inner Fringe Valid:** For each state K and each item a in its inner fringe, K \ {a} is a valid state
- [ ] **Outer Fringe Valid:** For each state K and each item b in its outer fringe, K union {b} is a valid state
- [ ] **Inner Fringe Complete:** No items in K are missing from the inner fringe when they should be there
- [ ] **Outer Fringe Complete:** No items outside K are missing from the outer fringe when they should be there

#### 1.4 Learning Path Properties (if learning_paths[] is populated)
- [ ] **Maximality:** Each path starts from the empty set equivalent and ends at Q-equivalent
- [ ] **Validity:** Each consecutive pair of items in the path corresponds to a valid state transition (the cumulative set at each step is a valid state)
- [ ] **Single-Step:** Consecutive states in the path differ by exactly one item

### Category 2: CbKST Validity

These checks ensure the Competence-Based KST layer is consistent (Heller & Stefanutti, 2024). These require reasoning and are not covered by the automated script.

#### 2.1 Competence Referential Integrity
- [ ] **Required competences exist:** All competence IDs referenced in items' `required_competences` fields exist in `competences[]`
- [ ] **No dangling competence IDs:** No `competence_relations[]` entries reference competence IDs that are not in `competences[]`

#### 2.2 Competence Relation Consistency
- [ ] **Alignment with item prerequisites:** If competence c1 is a prerequisite of competence c2 (in `competence_relations[]`), then items requiring c2 should generally have items requiring c1 as prerequisites (or transitively so). Flag misalignments.
- [ ] **Competence-level transitivity:** The competence prerequisite relation should itself be transitive and acyclic
- [ ] **No competence cycles:** If c1 -> c2 and c2 -> c1 for distinct competences, this is an error (analogous to item-level cycle checking)

#### 2.3 Skill Function Coverage
- [ ] **Every item has at least one required competence:** Items with empty `required_competences` are not grounded in the competence model
- [ ] **Every competence is required by at least one item:** Competences that no item requires are unused and should either be mapped to items or removed
- [ ] **No excessive competence concentration:** If a single competence is required by >70% of items, it may be too broad and need decomposition

#### 2.4 Delineation Check
- [ ] **The item-level knowledge structure is delineated by the competence structure:** For every feasible item-level knowledge state, there should exist a corresponding competence state that explains it. If the item-level space contains states that cannot be induced by any competence assignment, the competence structure may be incomplete.
- [ ] **Consistency of projections:** If two item-level states map to the same competence state, verify that this is intentional (the competence model is genuinely coarser, not missing distinctions).

### Category 3: Polytomous Validity (when applicable)

These checks apply only when items have graded mastery levels beyond binary (Stefanutti et al., 2020, 2022). Skip this category if all items are binary.

#### 3.1 Mastery Level Consistency
- [ ] **Consistent level ranges:** If items define mastery levels, each item should have a well-defined range (e.g., 0-3) with no gaps
- [ ] **Level 0 is "not mastered":** The lowest level should consistently represent non-mastery across all items
- [ ] **Uniform or documented level schemes:** If different items use different level ranges, this should be documented and justified

#### 3.2 Polytomous Surmise Relation Consistency
- [ ] **Level ordering respected:** If item a at level k is a prerequisite for item b at level m, then item a at any level < k should not be sufficient for item b at level m
- [ ] **Monotonicity:** Higher mastery levels in prerequisites should not relax requirements (i.e., if level 2 in a requires level 1 in b, then level 3 in a should require at least level 1 in b)

### Category 4: Educational Plausibility

These are soft checks — warnings that suggest the structure may not reflect good pedagogy.

#### 4.1 Prerequisite Load
- [ ] **Max Direct Prerequisites:** No item has more than 7 direct prerequisites (cognitive load concern — Miller's 7+-2)
- [ ] **Max Total Prerequisites:** No item requires more than 70% of all items as prerequisites (indicates possible granularity issue)
- [ ] **Minimum Path to Item:** No item requires more steps from the empty set than is reasonable for the course duration

#### 4.2 Bloom's Level Consistency
- [ ] **Level Ordering:** Items at "remember" Bloom level should generally be near the base (few prerequisites); "create" level near the top
- [ ] **No Level Inversions:** A "remember" item should not have an "evaluate" or "create" item as a prerequisite (warning: not always wrong, but worth flagging)

#### 4.3 Structural Balance
- [ ] **No Orphaned Items:** Every item is reachable from the empty set (has a valid learning path to it) and can reach Q
- [ ] **No Bottleneck Items:** No single item is a prerequisite for >50% of all other items (indicates the item may need decomposition)
- [ ] **Balanced Branching:** The ratio of max to min outer fringe size across states is not extreme

#### 4.4 Coverage
- [ ] **Topic Coverage:** All major topics from source materials are represented in items
- [ ] **Bloom's Distribution:** Items span at least 3 Bloom's levels
- [ ] **Knowledge Type Distribution:** Items span at least 2 knowledge types

### Category 5: Schema Conformance

- [ ] **JSON Schema Validation:** The graph conforms to `schemas/knowledge-graph.schema.json`
- [ ] **Required Fields:** All required fields are present
- [ ] **ID Uniqueness:** All item IDs are unique; all state IDs are unique; all path IDs are unique
- [ ] **ID Format:** All IDs match the expected pattern

## Output

### Step 1: Validation Report

Produce a structured report with three severity levels:

**FAIL (must fix):**
- Mathematical violations that make the structure invalid
- CbKST integrity violations (missing competences, broken skill function)
- Schema violations that prevent downstream skills from consuming the graph

**WARN (should review):**
- Educational plausibility concerns
- Structural imbalances
- Coverage gaps
- CbKST alignment concerns (competence relations inconsistent with item relations)
- Polytomous consistency warnings

**PASS:**
- All checks that passed successfully

Format:
```
## Validation Report for {domain-name}

### Automated Script Results
[Paste the output of `python3 scripts/kst_utils.py validate <graph-path>`]

### Summary
- FAIL: X checks
- WARN: Y checks
- PASS: Z checks

### FAIL
1. [Check 1.1 - Transitivity] Missing transitive relation: item-a -> item-c (via item-b)
   FIX: Run `python3 scripts/kst_utils.py closure <graph-path> --apply`

### WARN
1. [Check 2.1 - Max Direct Prerequisites] Item "item-x" has 9 direct prerequisites
   SUGGESTION: Consider decomposing item-x into sub-items
2. [Check 2.3 - Skill Function Coverage] Competence "comp-y" is not required by any item
   SUGGESTION: Map comp-y to relevant items or remove it

### PASS
1. [Check 1.2 - Acyclicity] No cycles detected
...
```

### Step 2: Fix Application (if requested or if only auto-fixable issues exist)

For auto-fixable issues (missing transitive relations, missing empty/full states):
- Run `python3 scripts/kst_utils.py closure <graph-path> --apply` for transitive closure fixes
- Apply other fixes to the knowledge graph
- Document each fix in the change_log
- Update metadata

For issues requiring human judgment:
- List them clearly with suggested options
- Do NOT auto-fix

Save the updated graph to `graphs/{domain-slug}-knowledge-graph.json`.

### Step 3: Structure Quality Metrics

Compute and report:
- **Discrimination Index:** How many states does the space have relative to 2^n? (closer to 2^n = less constrained = less useful)
- **Average Path Length:** Average number of steps from the empty set to Q across all learning paths
- **Bottleneck Score:** Max percentage of items that depend on any single item
- **Breadth vs. Depth:** Ratio of maximum width (most states at one level) to maximum depth
- **Fringe Compactness:** Average fringe size / average state size (per ALEKS, should be small)
- **Competence Coverage Ratio:** Number of items with required_competences / total items (should be 1.0)
- **Competence Utilization:** Number of competences required by at least one item / total competences (should be 1.0)

### Step 4: Empirical Validation (when student data is available)

When student response data is available, recommend or perform empirical validation using:

- **BLIM fit assessment:** Use the `pks` R package (Wickelmaier & Heller, 2024) to fit the Basic Local Independence Model and evaluate goodness-of-fit. Poor fit suggests the knowledge structure does not match student response patterns.
- **IITA comparison:** Run Inductive Item Tree Analysis (via `DAKS` R package or `learning_spaces` Python package) on the response data and compare the empirically derived surmise relations with the expert-derived ones. Discrepancies should be investigated.
- **Discrepancy Index (DI), gamma-index:** Standard KST fit statistics from Hockemeyer (2002) and the `kst` R package (Stahl & Hockemeyer, 2022).

If no student data is available, recommend collecting pilot data and revisiting this step.

### Step 5: Recommendations

- Issues that require human expert review
- Structural improvements to consider
- CbKST improvements: unmapped competences, alignment issues, delineation concerns
- Whether polytomous modeling would benefit the domain
- Whether the graph is ready for Phase 3 skills (assess-student, generate-materials, plan-instruction)

## Theoretical Grounding

Validation ensures the knowledge structure satisfies the mathematical axioms of KST (Heller & Stefanutti, 2024):

- **Union closure** is the defining property of a knowledge space (Doignon & Falmagne, 1999, Ch. 1)
- **Well-gradedness** is required for a knowledge space to also be a learning space, enabling item-by-item progression (Falmagne & Doignon, 2011)
- **Fringe properties** are essential for the adaptive assessment algorithm to work correctly (Falmagne et al., 2006)

**CbKST validation** (Heller & Stefanutti, 2024) adds a layer: the competence structure must be consistent with the item structure. The skill function (mapping competences to items via `required_competences`) must have full coverage, and the competence prerequisite relations must align with item prerequisite relations. The item-level knowledge structure should be **delineated** by the competence structure — meaning every feasible item state can be explained by a competence assignment.

**Polytomous validation** (Stefanutti et al., 2020, 2022) extends these checks to graded mastery. When items have multiple levels, the surmise relation must respect level ordering, and knowledge states must satisfy level-wise downward closure.

Educational plausibility checks draw on:
- **Miller's Law** (1956): Working memory limit of 7+-2 chunks — items with too many prerequisites may overwhelm learners
- **Bloom's level consistency** ensures the prerequisite structure aligns with cognitive complexity
- **Coverage analysis** ensures the knowledge space is a faithful representation of the curriculum

Empirical validation using the BLIM and related models (Wickelmaier & Heller, 2024; Hockemeyer, 2002) provides quantitative quality measures when student response data is available. The `pks` R package implements maximum likelihood estimation and goodness-of-fit tests for probabilistic knowledge structures.

## References

- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer.
- Doignon, J.-P. & Falmagne, J.-C. (2015). "Knowledge Spaces and Learning Spaces." arXiv:1511.06757.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. Springer.
- Falmagne, J.-C. et al. (2006). "The Assessment of Knowledge, in Theory and in Practice." ALEKS Corporation.
- Heller, J. & Stefanutti, L. (Eds.) (2024). *Knowledge Structures: Recent Developments in Theory and Application*. World Scientific.
- Wickelmaier, F. & Heller, J. (2024). *pks: Probabilistic Knowledge Structures*. R package v0.6-1.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2020). "Extending the Basic Local Independence Model to Polytomous Data." *Psychometrika*, 85, 684-715.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2022). "Notes on the polytomous generalization of knowledge space theory." *Journal of Mathematical Psychology*, 108.
- Hockemeyer, C. (2002). "A comparison of non-deterministic procedures for the adaptive assessment of knowledge."
- Stahl, C. & Hockemeyer, C. (2022). *kst: Knowledge Space Theory*. R package.
- Sargin, A. & Unlu, A. *DAKS: Data Analysis and Knowledge Spaces*. R package.
- Albert, D. & Lukas, J. (1999). *Knowledge Spaces: Theories, Empirical Research, and Applications*. Routledge.

See `references/bibliography.md` for the full bibliography.
