# Trace Operations in Knowledge Space Theory

This reference provides the detailed theory of trace operations for projecting and updating knowledge structures when items are added, removed, merged, or split. The SKILL.md file references this document for the mathematical foundations and algorithms underlying domain updates.

---

## Trace Definition (Doignon & Falmagne, 1999, Ch. 6)

### Formal Definition

Given a knowledge structure (Q, K) and a subset Q' of Q, the **trace** of K on Q' is:

```
K|Q' = { K intersect Q' : K in K }
```

The trace restricts every knowledge state to the items in Q' and collects all resulting subsets. Each resulting subset is a knowledge state in the projected structure.

### Properties of the Trace

**Theorem (Doignon & Falmagne, 1999):** The trace preserves key structural properties:

1. **Union closure is preserved:** If K is closed under union (i.e., K is a knowledge space), then K|Q' is also closed under union. Proof: If K1 intersect Q' and K2 intersect Q' are in K|Q', then (K1 union K2) intersect Q' = (K1 intersect Q') union (K2 intersect Q') is also in K|Q', since K1 union K2 is in K by union closure of K.

2. **Empty set and full set:** The empty set is in K|Q' (since the empty set is in K and intersect Q' = empty set). Q' is in K|Q' (since Q is in K and Q intersect Q' = Q').

3. **Well-gradedness is preserved:** If K is well-graded (a learning space), then K|Q' is also well-graded. This ensures that adaptive learning paths remain valid after projection.

4. **Consistency of iterated traces:** (K|Q')|Q'' = K|Q'' when Q'' is a subset of Q'. Traces compose correctly.

### Relationship to Surmise Relation

The trace on Q' induces a surmise relation on Q' that is consistent with the original:

```
For p, q in Q': p <= q in the traced structure
  if and only if
for every K in K, q in (K intersect Q') implies p in (K intersect Q')
```

This may differ from simply restricting the original surmise relation to Q', because removing intermediate items can change which prerequisites are "visible."

---

## Projection Mechanics for Removing Items

### Single Item Removal

To remove item x from domain Q:

1. Set Q' = Q \ {x}
2. Compute K|Q' = { K intersect Q' : K in K } = { K \ {x} : K in K }
3. The result is automatically a valid knowledge structure on Q'

**Effect on surmise relations:**

Consider the removal of item x with:
- Prerequisites of x: items p such that p -> x
- Dependents of x: items d such that x -> d

For each (p, d) pair where p -> x -> d:
- **If p -> d holds in the traced structure** (i.e., every state containing d also contains p after removing x), then the direct relation p -> d should be recorded. This is the case when p is a genuine prerequisite of d independent of x.
- **If p -> d does not hold in the traced structure** (i.e., there exists a state containing d but not p after removing x), then the relation p -> d should NOT be added. The dependency was mediated entirely through x.

**Algorithm:**
1. Remove x from items[]
2. Remove all surmise_relations involving x
3. For each pair (p, d) where p was a prerequisite of x and x was a prerequisite of d:
   a. Check if p -> d already exists (then no action needed)
   b. Check if there is another path from p to d not through x (then no action needed -- transitivity handles it)
   c. If p is a direct cognitive prerequisite of d (apply QUERY reasoning), add p -> d explicitly
   d. Otherwise, do not add the relation
4. Recompute transitive closure
5. Verify acyclicity

### Multiple Item Removal

For removing a set X = {x1, x2, ...} simultaneously:

1. Set Q' = Q \ X
2. Compute K|Q' in one step (rather than iterating single removals, which could produce different results if items in X have relations to each other)
3. Reconstruct the surmise relation from the traced knowledge structure

**Caution:** Removing items one at a time may produce a different result than removing them simultaneously, because the trace of a trace may differ from a direct trace on the union of removed sets when the removed items have prerequisite relations among themselves.

---

## Projection Mechanics for Adding Items

### Adding a Single Item

Adding item y to domain Q involves constructing a knowledge structure on Q' = Q union {y}:

1. **Define the item** with all required attributes
2. **Determine prerequisites:** Which existing items are prerequisites of y? Which items have y as a prerequisite?
3. **Extend each knowledge state:** For each K in K, determine whether y should be in the extended state:
   - If all prerequisites of y are in K, then K union {y} is a candidate state
   - If some prerequisites of y are not in K, then K (without y) remains a state
4. **Verify structure:** The extended family must satisfy union closure, contain the empty set, and contain Q'

**Efficient approach:** Rather than explicitly extending every state:
1. Add the item and its surmise relations to the graph
2. Re-enumerate knowledge states using `kst_utils.py enumerate --save`
3. Verify well-gradedness of the result

### Adding Multiple Items

When adding items {y1, y2, ...} that may have prerequisites among themselves:
1. Add all items
2. Add all relations (both to existing items and among new items)
3. Compute transitive closure
4. Verify acyclicity
5. Re-enumerate states

---

## Item Merging Algorithm

### When to Merge

Two items a and b should be merged when:
- They are mutual prerequisites (a -> b and b -> a), violating antisymmetry
- They are empirically indistinguishable (students always master both or neither)
- The domain has been refined and two formerly distinct items are now recognized as a single concept

### Merging Procedure

To merge items a and b into new item m:

1. **Create merged item m:**
   - ID: new unique ID (or one of the original IDs)
   - Label/description: combine information from both
   - Bloom's level: take the higher level (since m encompasses both)
   - Required competences: union of a's and b's required competences

2. **Update surmise relations:**
   - For every item p that was a prerequisite of a OR b: add p -> m (unless p is a or b)
   - For every item d that had a OR b as prerequisite: add m -> d (unless d is a or b)
   - Remove all relations involving a or b

3. **Update student states:**
   - For each student: if a OR b is in their state, add m; remove a and b
   - Recompute fringes

4. **Update competence mappings:**
   - If a and b had different required competences, m requires the union
   - Verify skill map consistency

5. **Validate:** Run full validation suite

### Merge Impact

Merging always reduces the domain size by 1 and typically reduces the number of knowledge states (some formerly distinct states become identical).

---

## Item Splitting Algorithm

### When to Split

An item x should be split when:
- Assessment data shows that students can master part of x without the rest
- Curriculum revision has decomposed the topic into finer-grained objectives
- The item spans multiple Bloom's cells or DOK levels

### Splitting Procedure

To split item x into new items x1 and x2:

1. **Create split items x1 and x2:**
   - Each gets appropriate subset of x's attributes
   - Determine if x1 -> x2 or x2 -> x1 or they are independent

2. **Distribute prerequisites:**
   - For each prerequisite p of x: determine if p should be prerequisite of x1, x2, or both
   - Heuristic: if p is prerequisite due to a competence required by x1 but not x2, then p -> x1 only

3. **Distribute dependents:**
   - For each dependent d of x: determine if d depends on x1, x2, or both
   - If d depends on both: add both x1 -> d and x2 -> d

4. **Distribute competences:**
   - Partition x's required competences between x1 and x2 based on which sub-concept each competence supports

5. **Update student states:**
   - For each student: if x was mastered, determine whether x1 and/or x2 should be mastered (default: both, but flag for re-assessment if uncertain)
   - If x was not mastered, neither x1 nor x2 is mastered

6. **Validate:** Run full validation suite

### Split Impact

Splitting always increases the domain size by 1 and typically increases the number of knowledge states (new distinctions become possible). This improves diagnostic granularity but increases assessment length.

---

## CbKST Maintenance Operations

### Skill Function Updates (Heller & Stefanutti, 2024)

When items or competences change, the skill map mu must be updated:

1. **After adding an item:** Define mu(new_item) = required competences
2. **After removing an item:** Remove mu(removed_item); check if any competence is now unused
3. **After adding a competence:** Update mu for items that require the new competence
4. **After removing a competence:** Remove the competence from all items' required_competences; verify no item has an empty required_competences set (unless intended)

### Delineation Revalidation

After any change to the skill map or competence structure:

1. **Recompute the delineated knowledge structure:**
   - For each competence state C in the competence structure, compute K(C) = { q : mu(q) is a subset of C }
   - Collect all such K(C) to form the delineated knowledge structure

2. **Compare with the item-level knowledge structure:**
   - If the delineated structure differs from the enumerated knowledge states, there is an inconsistency
   - Resolve by adjusting either the skill map or the surmise relations

3. **Check competence-item consistency:**
   - For every surmise relation p -> q: verify that every competence required by p is also required by q (or is a prerequisite of a competence required by q)
   - Flag violations for review

### Competence State Recalculation

After changes to competences or the skill map:

1. For each student, recompute competence state from their knowledge state:
   - A competence c is possessed if the student's knowledge state contains sufficient items that require c (conjunctive inference: if all items requiring c are mastered, c is possessed)
2. Update the `competence_state` field for each student
3. If a competence was removed, simply remove it from all competence states
4. If a competence was added, infer possession from the existing knowledge state

---

## Learning/Forgetting Interaction with Domain Changes

### Impact of Removing Items on Forgetting (de Chiusole et al., 2022)

When an item is removed from the domain:

1. **Dependent items lose a reinforcement pathway:** If students practiced the removed item as part of learning dependent items, those dependent items may be at higher forgetting risk.
2. **Inner fringe shifts:** Items that were deep in a student's state may now be on the inner fringe, increasing their forgetting vulnerability.
3. **Recommendation:** After removing items, flag dependent items for review reinforcement in the next session.

### Impact of Adding Items on Learning Trajectories

When items are added:

1. **New learning opportunities appear:** The new item may appear on students' outer fringes.
2. **Path diversity increases:** New learning paths through the space become available.
3. **Assessment scope increases:** Future assessments may need additional questions.

---

## Polytomous Trace Operations

### Polytomous Projection (Stefanutti et al., 2020)

For polytomous knowledge structures, the trace operation generalizes:

1. Each polytomous state K: Q -> product of L_q is restricted to Q' by simply dropping the components for items in Q \ Q'.
2. The resulting collection of restricted states forms a polytomous knowledge structure on Q'.
3. Properties (union closure, well-gradedness) are preserved, where "union" is interpreted as the componentwise maximum.

### Implications for Updates

When modifying polytomous items:
- Changing the number of response levels for an item requires recomputing all states involving that item
- Adding a response level increases the granularity of the structure
- Removing a response level requires collapsing states (multiple states may become identical)

---

## R Package Support (Stahl & Hockemeyer, 2022)

The `kst` R package provides functions for trace operations:

- `kstructure_trace()`: Compute the trace of a knowledge structure on a subset of items
- `kstructure()`: Construct a knowledge structure from a set of states
- `is.kspace()`: Verify that the result is a knowledge space (union closed)
- `reduction()`: Compute the surmise relation from a knowledge structure

For large-scale operations, using the R package may be more efficient than manual computation. Export the graph to R format, perform the trace, and import the result back to JSON.

---

## References

- de Chiusole, D., Stefanutti, L., Anselmi, P. & Robusto, E. (2022). Learning, forgetting, and the correlation of knowledge in knowledge space theory. *Journal of Mathematical Psychology, 108*.
- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer. Ch. 6.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. Springer.
- Heller, J. & Stefanutti, L. (2024). *Knowledge Structures: Recent Developments*. World Scientific.
- Stahl, C. & Hockemeyer, C. (2022). *kst: Knowledge Space Theory*. R package v0.5-4. CRAN.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2020). Extending the basic local independence model to polytomous data. *Psychometrika, 85*, 684-715.
