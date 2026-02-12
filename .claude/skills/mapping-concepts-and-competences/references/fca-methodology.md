# Formal Concept Analysis Methodology for Knowledge Structure Construction

This reference details the Formal Concept Analysis (FCA) perspective used in the `/map-concepts` skill. FCA provides a mathematically rigorous framework for discovering structure in item-attribute relationships, and it connects directly to Competence-Based Knowledge Space Theory (CbKST).

## FCA Foundations

Formal Concept Analysis (Ganter & Wille, 1999) starts from a **formal context** — a triple (G, M, I) where:

- **G** (Objects): The set of knowledge items from the domain
- **M** (Attributes): Properties assigned to items — these may include topic tags, Bloom's levels, DOK levels, required competences, or any binary characteristic
- **I** (Incidence relation): A binary relation I ⊆ G x M, where (g, m) in I means object g has attribute m

From this formal context, FCA derives **formal concepts** and a **concept lattice** that reveals the hierarchical structure of the domain.

### Derivation Operators

For a set of objects A ⊆ G:
- A' = { m in M | (g, m) in I for all g in A } — the set of attributes shared by all objects in A

For a set of attributes B ⊆ M:
- B' = { g in G | (g, m) in I for all m in B } — the set of objects that have all attributes in B

### Formal Concepts

A **formal concept** is a pair (A, B) where:
- A ⊆ G (the **extent** — a set of objects/items)
- B ⊆ M (the **intent** — a set of attributes)
- A' = B and B' = A (mutual derivation)

The extent A is exactly the set of objects sharing all attributes in B, and the intent B is exactly the set of attributes shared by all objects in A.

### Concept Lattice

The set of all formal concepts forms a complete lattice under the ordering:
- (A1, B1) ≤ (A2, B2) if and only if A1 ⊆ A2 (equivalently, B1 ⊇ B2)

This lattice reveals the hierarchical organization of the domain: broader concepts (larger extents, fewer shared attributes) sit above narrower concepts (smaller extents, more shared attributes).

## CbKST-FCA Integration

Huang et al. (2025) establish a formal connection between CbKST and FCA, showing that the competence-based knowledge structure can be derived from the concept lattice of an appropriately defined formal context.

### Transforming the Skill Map to a Formal Context

Given a CbKST domain with:
- Items Q = {q1, q2, ..., qn}
- Competences S = {s1, s2, ..., sm}
- Skill function f: 2^S -> 2^Q (mapping competence states to knowledge states)

Construct the formal context (Q, S, I) where:
- Objects G = Q (knowledge items)
- Attributes M = S (competences)
- (q, s) in I if and only if competence s is required by item q

For the **conjunctive model**: item q requires ALL competences in its assigned set. The incidence I directly reflects the `required_competences` field on each item.

For the **disjunctive model**: item q can be solved by ANY of several competence subsets. The formal context construction is more nuanced — each alternative competence set defines a separate row in an expanded context.

### Concept Lattice Construction

From the formal context (Q, S, I):

1. Compute all formal concepts (A, B) where A ⊆ Q and B ⊆ S with A' = B and B' = A
2. Order them by extent inclusion to form the concept lattice

### What the Lattice Reveals

- **Formal concepts**: Each concept (A, B) represents a group of items A that share exactly the competences B. These correspond to natural "clusters" in the domain where the same skill set applies.
- **Lattice ordering**: If concept C1 ≤ C2, then the items in C1 are a subset of those in C2, and the competences of C1 are a superset of those in C2. This captures the idea that more specialized knowledge (fewer items, more competences required) sits below more general knowledge.
- **Knowledge structure correspondence**: Under the conjunctive model, the set of extents of the concept lattice forms a closure system on Q. This closure system is exactly the knowledge structure K induced by the skill map — i.e., the feasible knowledge states are precisely the extents of the formal concepts (Huang et al., 2025, Theorem 3.1). This provides a mathematically guaranteed way to derive knowledge states from the competence structure.

### Practical Implications for Concept Mapping

When applying FCA during concept mapping:

1. **Validate competence assignments**: If two items share all the same competences, they should appear in the same formal concept extent. If they behave differently in practice, a competence may be missing.
2. **Discover missing competences**: If the concept lattice has very few concepts relative to the number of items, the competence set may be too coarse. Consider splitting competences.
3. **Detect redundant competences**: If two competences always appear together in every intent, they may be a single competence described at different granularities. Consider merging.
4. **Identify natural item clusters**: The extents of formal concepts provide a principled grouping of items, which can validate or refine the hierarchical organization from Step 2 of the mapping methodology.

## FCA-Based Knowledge Structure Construction

Li et al. (2024) provide a complementary approach using FCA to construct knowledge structures directly, without requiring an explicit competence layer.

### Defining the Formal Context

Instead of using competences as attributes, define a formal context based on item properties:

- **Objects G**: Knowledge items
- **Attributes M**: Item properties such as topic, prerequisite skills, assessment type, DOK level, or any other domain-relevant characteristic
- **Incidence I**: Item g has property m

Alternatively, use a **student response context**:
- **Objects G**: Students (or student response patterns)
- **Attributes M**: Knowledge items
- **Incidence I**: Student g has mastered item m

### Computing the Concept Lattice

1. Apply the standard FCA algorithm (e.g., NextClosure by Ganter, 1984) to enumerate all formal concepts
2. Order concepts by extent inclusion

### Deriving the Knowledge Structure

The set of all extents { A | (A, B) is a formal concept } forms a **closure system** on Q (or on the student population). Key properties:

- The extents are closed under intersection: if two extents overlap, their intersection is also an extent
- The empty set and Q itself are extents (corresponding to the bottom and top of the lattice)
- This closure system is a **knowledge structure** in the KST sense (Doignon & Falmagne, 1999)

If the original data satisfies certain regularity conditions, the resulting knowledge structure is a **knowledge space** (closed under union as well as intersection), which is the standard KST requirement.

### Validating Closure Properties

After deriving the knowledge structure from extents:

1. **Union closure**: Check whether the union of any two extents is also an extent. If yes, the structure is a knowledge space. If not, it is a quasi-ordinal knowledge space or a more general knowledge structure.
2. **Wellgradedness**: Check whether between any two comparable states there exists a learning path that adds exactly one item at a time. This is the learning space property (Falmagne & Doignon, 2011).
3. **Consistency with surmise relation**: The knowledge states derived from FCA should be consistent with the surmise relations identified in concept mapping. Specifically, every knowledge state should be a downset of the surmise relation.

### Connecting FCA and Surmise Relations

The concept lattice provides an alternative derivation of the surmise relation:

- If item a appears in every extent that contains item b, then a is a prerequisite for b (a surmises b)
- The surmise relation derived this way should be consistent with the prerequisite-of relationships identified in the concept mapping step
- Discrepancies may indicate errors in either the relationship identification or the formal context definition

## When to Apply FCA

FCA is most valuable when:

- The domain has 15+ items and the relationship structure is not immediately obvious
- Competence assignments feel uncertain and need mathematical validation
- You want to verify that the concept map is consistent with the underlying mathematical structure
- The domain has been partially analyzed and you want to discover missing structure

For small domains (under 15 items), the overhead of FCA may not be justified — direct concept mapping is usually sufficient.

## References

All citations refer to `references/bibliography.md`:

- Ganter, B. & Wille, R. (1999) — Formal Concept Analysis: Mathematical Foundations
- Huang, B., Li, J., Li, Q., Zhou, Y. & Chen, H. (2025) — CbKST from the FCA perspective
- Li, J. et al. (2024) — Knowledge structures construction based on formal contexts
- Doignon, J.-P. & Falmagne, J.-C. (1999) — Knowledge Spaces
- Falmagne, J.-C. & Doignon, J.-P. (2011) — Learning Spaces
- Heller, J. & Stefanutti, L. (2024) — Knowledge Structures: Recent Developments
