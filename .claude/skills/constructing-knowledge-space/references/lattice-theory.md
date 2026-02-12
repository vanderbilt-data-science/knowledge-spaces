# Lattice-Theoretic Foundations -- Detailed Reference

This reference provides the full lattice-theoretic underpinnings of knowledge space construction, including Birkhoff's theorem, well-gradedness, basis representation, and scalability strategies. Consult this for deep mathematical detail beyond the concise methodology in the SKILL.md.

---

## 1. Birkhoff's Representation Theorem

### Statement

**Birkhoff's Theorem (1937):** There is a one-to-one correspondence between:
- Quasi-orders (reflexive, transitive binary relations) on a finite set Q
- Families of subsets of Q that are closed under union and contain Q and the empty set

### Proof Sketch

**Direction 1: Quasi-order -> Union-closed family**

Given a quasi-order (Q, <=), define the family K as all downward-closed sets (downsets) of (Q, <=). A set K is a downset if: for all b in K and all a <= b, we have a in K.

- The empty set is trivially a downset (vacuously closed).
- Q itself is a downset (every element's prerequisites are in Q).
- **Union closure:** If K1 and K2 are downsets, then K1 union K2 is a downset. Proof: if b is in K1 union K2 and a <= b, then b is in K1 or K2. If b is in K1 (which is a downset), then a is in K1, hence in the union. Similarly for K2.

**Direction 2: Union-closed family -> Quasi-order**

Given a family K of subsets of Q that is closed under union and contains the empty set and Q, define a -> b (a is surmised by b) iff every set in K that contains b also contains a.

- **Reflexivity:** Every set containing a contains a.
- **Transitivity:** If every set containing b also contains a, and every set containing c also contains b, then every set containing c also contains a.
- **Recovery:** The downsets of this quasi-order are exactly the sets in K.

### Significance for KST

Birkhoff's theorem means that specifying the surmise relation (quasi-order) is mathematically equivalent to specifying the knowledge space (union-closed family). The `/building-surmise-relations` skill determines the quasi-order; the `/constructing-knowledge-space` skill derives the corresponding family of states. Neither contains more or less information than the other -- they are dual representations.

---

## 2. Lattice Structure of Knowledge Spaces

### Knowledge Space as a Lattice

The family of knowledge states, ordered by set inclusion, forms a **complete lattice**:
- **Join (least upper bound):** The join of two states K1 and K2 is K1 union K2 (which is in the space by union closure).
- **Meet (greatest lower bound):** The meet of K1 and K2 is the largest state K in the space such that K is a subset of both K1 and K2. This is not necessarily K1 intersection K2 (the intersection may not be in the space unless the space is also closed under intersection, making it a **knowledge structure** in the strict sense).
- **Bottom element:** The empty set.
- **Top element:** Q (the full domain).

### Distributive Lattices

When the knowledge space is derived from a quasi-order via Birkhoff's theorem, the resulting lattice is **distributive**: for all states K1, K2, K3:
- K1 union (K2 intersection K3) = (K1 union K2) intersection (K1 union K3)

Distributivity provides computational advantages -- distributive lattices can be compactly represented by their join-irreducible elements.

### Join-Irreducible Elements

A state K is **join-irreducible** if it cannot be expressed as the union of two strictly smaller states. In a knowledge space derived from a quasi-order, the join-irreducible elements correspond to the **principal downsets** -- the set of all prerequisites of a single item (plus the item itself).

This means:
- Number of join-irreducible states = number of items = |Q|
- Every state can be expressed as a union of join-irreducible states
- The lattice structure is fully determined by the join-irreducibles

---

## 3. Well-Gradedness

### Definition

A knowledge space K is **well-graded** if for any two states K1 and K2 with K1 a proper subset of K2, there exists a **tight path** from K1 to K2: a sequence K1 = S0, S1, ..., Sm = K2 where:
- Each Si is in K
- |Si+1 \ Si| = 1 (consecutive states differ by exactly one item)
- S0 is a proper subset of S1 is a proper subset of ... is a proper subset of Sm

### Properties of Well-Graded Spaces

Well-graded knowledge spaces are also called **learning spaces** (Falmagne & Doignon, 2011). Key properties:

1. **Every knowledge space derived from a quasi-order is well-graded.** This is because the quasi-order provides a topological ordering, and items can always be added one at a time respecting this ordering.

2. **Well-gradedness implies learnability.** Between any two states, there exists a step-by-step learning path where the student acquires one item at a time.

3. **Not all knowledge structures are well-graded.** A knowledge structure (closed under union but not necessarily derived from a quasi-order) may have "gaps" where no single-item transitions exist between certain pairs of states.

### Verification

To verify well-gradedness of a computed knowledge space:
1. Build the Hasse diagram of the lattice (edges between states differing by exactly one item)
2. Check connectivity: for every pair (K1, K2) with K1 a subset of K2, there must be a path in the Hasse diagram from K1 to K2

The `kst_utils.py enumerate` algorithm inherently produces well-graded spaces when starting from a quasi-order, so verification is primarily needed when importing externally constructed spaces.

---

## 4. Basis Representation

### The Basis of a Knowledge Space

The **basis** (or **base**) of a knowledge space K is the smallest subfamily B of K such that every state in K can be expressed as a union of states in B. Equivalently, B is the set of join-irreducible elements of the lattice.

### Properties

- |B| = |Q| for spaces derived from quasi-orders
- Each basis element corresponds to one item's "prerequisite closure" (the item plus all its transitive prerequisites)
- The full space can be reconstructed from the basis: K = {union of any subset of B} union {empty set}

### Computational Advantage

For a domain with n items:
- Full enumeration may produce up to 2^n states
- The basis has exactly n elements
- Storing just the basis reduces space from O(2^n * n) to O(n^2)

### Reconstruction Algorithm

To reconstruct any state from the basis:
1. Determine which items the student has mastered
2. For each mastered item, look up its basis element (prerequisite closure)
3. The student's knowledge state is the union of all relevant basis elements
4. This union is guaranteed to be a valid state (by union closure)

---

## 5. Scalability Strategies

### Problem Statement

For n items with no prerequisites, there are 2^n knowledge states. Practical domains with 20-30+ items can produce millions to billions of states, making full enumeration infeasible.

### Strategy 1: Implicit Representation

**Approach:** Store only the surmise relation; compute states and fringes on demand.

**Implementation:**
- Store the surmise relation (O(n^2) space)
- To check if a set K is a valid state: verify all items in K have their prerequisites in K (O(n * max_prereqs))
- To compute the outer fringe: for each item not in K, check if all its prerequisites are in K (O(n * max_prereqs))
- To compute the inner fringe: for each item in K, check if removing it still leaves all dependents' prerequisites satisfied (O(n * max_dependents))

**Tradeoffs:**
- Space: O(n^2) vs O(2^n * n)
- Time per operation: O(n^2) vs O(1) lookup
- Best for: Very large domains (50+ items) where full enumeration is impossible
- Not suitable for: Operations requiring enumeration of all states (e.g., BLIM with full state space)

### Strategy 2: Sampled States

**Approach:** Enumerate a representative subset of states rather than all states.

**Implementation options:**
- **Boundary sampling:** Enumerate all states reachable within k steps from the empty set AND within k steps from Q. This captures the "edges" of the space.
- **Level sampling:** For each cardinality k (0, 1, ..., n), enumerate a fixed number of states with exactly k items.
- **Random walk sampling:** Perform random walks from the empty set to Q, recording all intermediate states. Repeat until convergence (new walks rarely discover new states).

**Tradeoffs:**
- Provides a representative picture of the space structure
- Learning paths can still be generated from sampled states
- BLIM assessment may use sampled states as the candidate set (approximate)
- Cannot guarantee completeness

### Strategy 3: Basis Representation

**Approach:** Store only the n basis elements (join-irreducible states).

**Implementation:**
- Compute the basis: for each item, its basis element is the item plus all its transitive prerequisites
- Store these n sets
- Reconstruct any state on demand as a union of basis elements

**Tradeoffs:**
- Extremely compact: O(n^2) space
- Reconstruction is O(n^2)
- Full enumeration can be recovered if needed (generate all 2^n subsets of the basis, compute their unions)
- Does not directly provide fringe information

### Strategy 4: Fringe-Only Representation

**Approach:** For each "level" (states with the same number of items), store one representative state with its fringes.

**Implementation:**
- Enumerate states level by level
- At each level, store one or a few representative states with their inner and outer fringes
- This is sufficient for assessment (which primarily needs fringes) and learning path generation

**Tradeoffs:**
- Very compact for assessment applications
- Loses information about the full lattice structure
- Sufficient for adaptive assessment (BLIM can work with fringe-based state selection)
- Not suitable for full structural analysis

### Choosing a Strategy

| Domain size | Recommended strategy | Rationale |
|-------------|---------------------|-----------|
| 1-20 items | Full enumeration | Feasible and exact |
| 20-25 items | Full with --max limit | May hit limits; check density first |
| 25-40 items | Basis + sampled states | Compact core with representative coverage |
| 40+ items | Implicit + fringe-only | Only compute what is needed on demand |

---

## 6. Polytomous State Enumeration

### Overview

In the polytomous generalization (Stefanutti et al., 2020, 2022), items have mastery levels 0, 1, ..., L_i for each item i. A knowledge state is a tuple (l_1, l_2, ..., l_n) where l_i is the mastery level of item i.

### State Space Size

For n items each with L levels, the state space is bounded by the product of all (L_i + 1) values, which can be much larger than 2^n. For example, 10 items each with 4 levels gives 4^10 ~ 1 million possible tuples.

### Feasibility Constraint

A tuple is a feasible polytomous state if it satisfies the polytomous surmise relation: for each level-specific prerequisite "level k in item a requires level m in item b", the state must have l_b >= m whenever l_a >= k.

### Enumeration Algorithm

The binary BFS algorithm generalizes:
1. Start from the zero tuple (0, 0, ..., 0)
2. At each step, increment one item's level by 1 if all level-specific prerequisites are satisfied
3. Branch on all valid increments
4. Collect all unique tuples generated

### Practical Considerations

- Polytomous enumeration is typically much more expensive than binary
- Basis representation extends to the polytomous case but is less well-studied
- For practical purposes, consider enumerating the binary approximation first, then adding polytomous detail for items where graded mastery is most important

---

## 7. The Well-Graded Polytomous Case

Recent work ("Well-graded polytomous knowledge structures," 2023) extends well-gradedness to polytomous knowledge structures:
- A polytomous knowledge structure is well-graded if between any two states, there exists a tight path where consecutive states differ in exactly one item's level by exactly one step
- Well-gradedness in the polytomous case is a stronger requirement than in the binary case
- It ensures that learning can proceed incrementally in each item's mastery

---

## References

- Birkhoff, G. (1937). "Rings of sets." *Duke Mathematical Journal*, 3(3), 443-454.
- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer. Ch. 1-3.
- Doignon, J.-P. & Falmagne, J.-C. (2015). "Knowledge Spaces and Learning Spaces." arXiv:1511.06757.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. Springer. Ch. 2-4.
- Falmagne, J.-C., Albert, D., Doble, C., Eppstein, D. & Hu, X. (2013). *Knowledge Spaces: Applications in Education*. Springer.
- Heller, J. & Stefanutti, L. (Eds.) (2024). *Knowledge Structures: Recent Developments in Theory and Application*. World Scientific.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2020). "Extending the Basic Local Independence Model to Polytomous Data." *Psychometrika*, 85, 684-715.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2022). "Notes on the polytomous generalization of knowledge space theory." *Journal of Mathematical Psychology*, 108.
- "Well-graded polytomous knowledge structures." (2023). *Journal of Mathematical Psychology*, 114.
- Wang, S. et al. (2023). "CD-polytomous knowledge spaces and corresponding polytomous surmise systems." *British Journal of Mathematical and Statistical Psychology*.
- Cosyn, E., Uzun, H., Doble, C. & Matayoshi, J. (2021). "A practical perspective on knowledge space theory: ALEKS and its data." *Journal of Mathematical Psychology*, 101.

See `references/bibliography.md` for the complete bibliography.
