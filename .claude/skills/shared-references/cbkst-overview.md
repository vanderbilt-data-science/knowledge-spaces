# Competence-Based Knowledge Space Theory (CbKST)

This reference describes the Competence-Based Knowledge Space Theory framework, which extends classical KST by introducing a latent competence layer beneath the observable item layer. CbKST provides a principled mechanism for constructing knowledge structures from domain expertise about skills and competences, rather than relying solely on empirical item-response data or direct expert judgments about item prerequisites.

---

## Two-Level Architecture

Classical KST operates at a single level: a domain of items Q and a knowledge structure on those items. CbKST introduces a second, latent level:

1. **Competence level (latent):** A set of competences (skills) S that represent unobservable cognitive abilities, dispositions, or knowledge components.
2. **Item level (observable):** A set of items Q that are directly assessable (e.g., test questions, tasks, exercises).

The key insight is that items are solved by applying competences. A student who possesses certain competences will be able to solve exactly those items that require (subsets of) those competences. This two-level architecture allows domain experts to reason about competences — which are often more natural to articulate — and then derive the item-level knowledge structure mathematically.

### Why Two Levels?

- **Expert elicitation is easier at the competence level.** Experts can more naturally state "understanding derivatives requires understanding limits" than "item 17 requires mastery of item 9."
- **The same competence structure can generate knowledge structures for different item sets.** If you change your assessment items, you only need to update the skill map, not rebuild the entire prerequisite structure.
- **Competences provide explanatory power.** When a student fails an item, CbKST can attribute the failure to specific missing competences.

---

## Skill Map and Skill Function

The bridge between the competence and item levels is the **skill map** (also called the **skill function** or **problem function**).

### Disjunctive Skill Map

In the **disjunctive** model, each item q in Q is associated with a collection of subsets of competences. Each subset represents a *sufficient* combination of competences for solving q. Formally:

- **mu: Q -> 2^(2^S)** maps each item to a family of competence subsets.
- A student with competence state C (a subset of S) can solve item q if and only if there exists at least one subset T in mu(q) such that T is a subset of C.

This means there may be *multiple alternative paths* to solving an item — a student can solve it if they possess any one of the sufficient competence combinations.

### Conjunctive Skill Map

In the **conjunctive** model, each item q is associated with a single set of *required* competences:

- **mu: Q -> 2^S** maps each item to the set of competences required to solve it.
- A student with competence state C can solve item q if and only if mu(q) is a subset of C.

The conjunctive model is simpler and is the one used in the knowledge graph schema's `required_competences` field. It states: to solve item q, a student must possess *all* competences in mu(q).

### Choosing Between Models

| Model | Assumption | Resulting Structure |
|-------|-----------|-------------------|
| **Conjunctive** | Each item requires all of a specific set of competences | Knowledge structure is closed under union and intersection (a *knowledge space* that is also a *simple closure space*) |
| **Disjunctive** | Each item can be solved via any of several alternative competence sets | Knowledge structure is closed under union (a *knowledge space*) |

In practice, many implementations (including the ALEKS system) use the conjunctive model or a hybrid approach.

---

## Delineation: From Competences to Knowledge States

**Delineation** is the process by which the competence structure induces the item-level knowledge structure.

### Procedure

1. **Define the competence set S** — the set of all relevant competences.
2. **Define the competence structure** — a family of subsets of S representing plausible competence states (which combinations of competences a student might possess).
3. **Define the skill map mu** — the mapping from items to required competences.
4. **Delineate** — for each competence state C in the competence structure, compute the corresponding knowledge state: the set of all items q such that the student with competences C can solve q.

Formally, the **delineated knowledge state** for a competence state C is:

- K(C) = { q in Q : mu(q) is a subset of C } (conjunctive model)
- K(C) = { q in Q : there exists T in mu(q) such that T is a subset of C } (disjunctive model)

The **delineated knowledge structure** is the family { K(C) : C is a competence state in the competence structure }.

### Properties

- If the competence structure is closed under union, the delineated knowledge structure is also closed under union (i.e., it is a knowledge space).
- If both the conjunctive model and a union-closed competence structure are used, the delineated knowledge structure is closed under both union and intersection.
- Different competence states may map to the same knowledge state (the mapping is generally surjective but not injective).

---

## Competence States vs. Knowledge States

| Aspect | Competence State | Knowledge State |
|--------|-----------------|-----------------|
| **Level** | Latent (unobservable) | Observable (through item responses) |
| **Elements** | Competences (skills, abilities) | Items (test questions, tasks) |
| **Assessment** | Cannot be directly measured | Directly measurable via item responses |
| **Granularity** | Typically fewer competences than items | Derived from competence states via delineation |
| **Multiplicity** | Multiple competence states may map to the same knowledge state | Each knowledge state may correspond to multiple competence states |

A key consequence: assessment at the item level determines the knowledge state, but the underlying competence state remains uncertain. Probabilistic models (e.g., BLIM applied at the competence level, called the **Competence-based BLIM**) can estimate the most likely competence state given observed responses.

---

## Competence Prerequisite Relations

Just as items have prerequisite relations (the surmise relation), competences can have their own prerequisite structure:

- A **competence prerequisite relation** is a quasi-order on S: a reflexive, transitive relation where s1 <= s2 means "competence s1 is a prerequisite for competence s2."
- The **competence structure** can be derived from this quasi-order analogously to how the knowledge structure is derived from the surmise relation: competence states are downward-closed sets (downsets) of the competence prerequisite relation.

### Relationship to Item-Level Structure

The competence prerequisite relation, combined with the skill map, induces the item-level surmise relation:

- Item q1 is a prerequisite for item q2 if, whenever a competence state allows solving q2, it also allows solving q1.
- Equivalently (conjunctive model): if every competence required for q1 is also required for q2, or is a prerequisite of some competence required for q2.

This means domain experts can specify prerequisites at the competence level, and the item-level prerequisite structure is derived automatically — a significant advantage for maintainability.

---

## Integration with Formal Concept Analysis (Huang et al., 2025)

Formal Concept Analysis (FCA) provides a mathematical framework that aligns naturally with CbKST.

### The Skill Map as a Formal Context

The conjunctive skill map can be represented as a **formal context** (G, M, I):

- **G** (objects) = the set of items Q
- **M** (attributes) = the set of competences S
- **I** (incidence relation) = q I s if and only if competence s is required to solve item q (i.e., s is in mu(q))

### Concept Lattice Construction

From this formal context, FCA constructs a **concept lattice**:

- Each **formal concept** is a pair (A, B) where A is a subset of Q (the extent) and B is a subset of S (the intent), such that A is exactly the set of items requiring only competences in B, and B is exactly the set of competences required by all items in A.
- The concept lattice organizes all such concepts in a hierarchical structure ordered by inclusion of extents (or dually, reverse inclusion of intents).

### Benefits of the FCA Integration

1. **Automatic structure discovery:** The concept lattice reveals the inherent structure in the skill map without additional expert input.
2. **Attribute implications:** FCA can extract implications among competences (e.g., "every item requiring competence A also requires competence B"), which can validate or refine the competence prerequisite relation.
3. **Basis computation:** The Duquenne-Guigues basis provides a minimal set of implications that generates all others — useful for validating completeness of the competence structure.
4. **Visualization:** The Hasse diagram of the concept lattice provides an intuitive visualization of the domain structure.

### Practical Workflow (Huang et al., 2025)

1. Experts define items and competences and construct the skill map.
2. The skill map is encoded as a formal context.
3. FCA algorithms compute the concept lattice and attribute implications.
4. Implications are reviewed by experts to validate or refine the competence model.
5. The refined model is used to delineate the knowledge structure.

---

## Polytomous Extensions (Stefanutti et al., 2020, 2022)

Classical KST uses dichotomous items: a student either can or cannot solve each item. Polytomous extensions generalize this to items with multiple response levels or graded mastery.

### Polytomous Knowledge States

In the polytomous framework:

- Each item q has a set of possible **response values** L_q = {0, 1, ..., m_q}, where 0 represents no mastery and m_q represents full mastery.
- A **polytomous knowledge state** is a function that assigns to each item a response value: K: Q -> product of L_q values.
- The **polytomous knowledge structure** is the collection of all plausible polytomous states.

### Ordering of States

Polytomous states are ordered componentwise: state K1 <= K2 if and only if K1(q) <= K2(q) for all items q. This generalizes the subset ordering of dichotomous states.

### Granularity and Graded Mastery

Polytomous extensions are particularly valuable when:

- **Partial credit** is meaningful (e.g., a student solves 2 out of 5 parts of a multi-step problem).
- **Proficiency levels** are tracked (e.g., novice / competent / expert for a skill).
- **Progressive mastery** is the pedagogical model (e.g., a student moves from recognition to recall to application of a concept).

### Polytomous Competence Model (Stefanutti et al., 2022)

The CbKST framework extends naturally to the polytomous case:

- Competences can have graded levels (e.g., a competence mastered at level 0, 1, or 2).
- The skill map specifies, for each item response level, the minimum competence levels required.
- Delineation proceeds analogously: a competence state (now a vector of competence levels) determines a polytomous knowledge state.

---

## Summary: CbKST Workflow

```
1. Identify competences S
         |
2. Define competence prerequisite relation on S
         |
3. Derive competence structure (downsets of the prerequisite relation)
         |
4. Define skill map mu: Q -> 2^S (conjunctive) or Q -> 2^(2^S) (disjunctive)
         |
5. Delineate: compute knowledge states from competence states
         |
6. Validate via FCA: check concept lattice and attribute implications
         |
7. Optionally extend to polytomous model if graded mastery is needed
```

---

## References

- Doignon, J.-P., & Falmagne, J.-C. (1999). *Knowledge spaces*. Springer.
- Falmagne, J.-C., & Doignon, J.-P. (2011). *Learning spaces: Interdisciplinary applied mathematics*. Springer.
- Heller, J., & Stefanutti, L. (2024). *Knowledge structures: Recent developments*. In D. Ifenthaler, P. Isaias, & D. G. Sampson (Eds.), *Open and inclusive educational practice in the digital world*. Springer.
- Huang, H., Sun, X., Li, M., & Wang, S. (2025). Construction of knowledge structures based on formal concept analysis and knowledge space theory. *Journal of Mathematical Psychology, 124*, 102886.
- Li, M., Sun, X., Huang, H., & Wang, S. (2024). Knowledge assessment based on skill map and formal concept analysis. *British Journal of Mathematical and Statistical Psychology, 77*(3), 555–578.
- Stefanutti, L., de Chiusole, D., Gondan, M., & Maurer, A. (2020). Modeling misconceptions in knowledge space theory. *Journal of Mathematical Psychology, 94*, 102306.
- Stefanutti, L., de Chiusole, D., & Spoto, A. (2022). Exploiting response times in knowledge space theory. *Journal of Mathematical Psychology, 110*, 102718.
- Wille, R. (1982). Restructuring lattice theory: An approach based on hierarchies of concepts. In I. Rival (Ed.), *Ordered sets* (pp. 445–470). Reidel.
