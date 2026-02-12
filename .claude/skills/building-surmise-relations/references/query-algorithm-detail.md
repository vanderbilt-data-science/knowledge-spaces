# QUERY Algorithm and Data-Driven Approaches -- Detailed Reference

This reference provides full algorithm mechanics, reasoning framework examples, IITA algorithm variants, and integration protocols for the `/building-surmise-relations` skill. Consult this for deep technical detail beyond the concise methodology in the SKILL.md.

---

## 1. The QUERY Algorithm (Koppen & Doignon, 1990)

### Formal Specification

The QUERY algorithm systematically elicits a surmise relation from a domain expert by posing a structured sequence of questions about prerequisite relationships.

**Inputs:**
- Q = {q1, q2, ..., qn} -- a finite set of knowledge items
- An expert who can answer prerequisite queries about Q

**Output:**
- A quasi-order (reflexive, transitive relation) S on Q representing the surmise relation

**Algorithm:**

```
Initialize S = identity relation (reflexivity only)
For each ordered pair (a, b) where a != b:
    If S already implies a -> b (by transitivity): skip
    If S already implies a and b are independent: skip
    QUERY the expert: "If a student masters b, can we surmise mastery of a?"
    If YES: add (a, b) to S; compute transitive closure of S
    If NO: record independence; propagate independence constraints
```

### Query Reduction Strategies

The naive algorithm requires O(n^2) queries. Koppen & Doignon (1990) describe strategies to reduce this:

**Transitivity exploitation:**
- If a -> b and b -> c have been established, a -> c is automatic. Do not query it.
- After each YES answer, recompute the transitive closure and remove now-redundant queries from the queue.

**Contrapositive reasoning:**
- If the expert says mastery of c does NOT surmise mastery of a (i.e., a is NOT a prerequisite of c), then for any d where d -> c, mastery of d also does not surmise mastery of a. This prunes queries.

**Topological ordering:**
- If items can be roughly ordered by difficulty or conceptual level, query pairs where the potential prerequisite is at a lower level. Pairs at the same level are less likely to have prerequisite relationships.

**Cluster-based reduction:**
- Group items by topic/subdomain. Within-cluster queries are more likely to find prerequisites than across-cluster queries. Query within clusters first, then selectively across clusters.

### Expected Query Count

For n items:
- Worst case: O(n^2) queries
- Typical case with good strategies: O(n log n) to O(n * sqrt(n))
- Highly structured domains (clear layering): closer to O(n)

### Reasoning Framework -- Expanded Examples

#### Example 1: Strong prerequisite (YES, confidence 1.0)

```
QUERY: Does mastery of "solve quadratic equations" surmise mastery of
       "solve linear equations"?
REASONING:
  - Cognitive Task Analysis: Solving quadratics requires factoring, applying
    the quadratic formula, or completing the square -- all of which assume
    the ability to isolate variables and perform algebraic manipulation,
    which is exactly what solving linear equations entails.
  - Logical Necessity: The quadratic formula reduces to a linear equation
    in degenerate cases. Factoring a quadratic requires solving the resulting
    linear factors. This is definitionally required.
  - Empirical Plausibility: It is essentially impossible to reliably solve
    quadratic equations without being able to solve linear ones.
  - Granularity Check: This is a direct prerequisite (no intermediate item
    mediates this relationship in the current item set).
DECISION: YES
CONFIDENCE: 1.0
```

#### Example 2: Helpful but not prerequisite (NO)

```
QUERY: Does mastery of "interpret regression output" surmise mastery of
       "compute descriptive statistics by hand"?
REASONING:
  - Cognitive Task Analysis: Interpreting regression output requires
    understanding coefficients, p-values, and R-squared -- concepts that
    relate to understanding variability and relationships, not to hand
    computation of means/medians.
  - Logical Necessity: A student can learn to interpret regression output
    using software without ever computing a mean by hand. The concepts
    are related but the specific skill of hand computation is not required.
  - Empirical Plausibility: Many data science students interpret regression
    output fluently without strong hand-computation skills.
  - Granularity Check: N/A (decision is NO).
DECISION: NO
CONFIDENCE: N/A
```

#### Example 3: Uncertain case (YES, flag for review)

```
QUERY: Does mastery of "design a controlled experiment" surmise mastery of
       "identify confounding variables"?
REASONING:
  - Cognitive Task Analysis: Designing a controlled experiment requires
    anticipating and controlling for confounders. This seems to require
    the ability to identify them.
  - Logical Necessity: One could argue that a student might follow a
    template for experimental design without deeply understanding
    confounders -- but such mastery would be shallow.
  - Empirical Plausibility: In practice, some students can design
    acceptable experiments by following protocols without being able to
    independently identify confounders in novel situations.
  - Granularity Check: Direct prerequisite if the relationship holds.
DECISION: YES (flagged for review)
CONFIDENCE: 0.5
```

---

## 2. IITA -- Inductive Item Tree Analysis

### Overview

IITA (Schrepp, 1999; extended by Sargin & Unlu in the DAKS package) extracts surmise relations from binary student response data. It identifies which items are prerequisites of which by analyzing response pattern frequencies.

### Algorithm Variants

#### Original IITA

1. **Input:** Binary response matrix R (students x items), where R[s,i] = 1 if student s answered item i correctly.
2. **For each item pair (i, j):** Compute the violation rate -- the proportion of students who answered j correctly but i incorrectly (which would violate i -> j).
3. **Threshold selection:** Use a global threshold on violation rates. Pairs below the threshold are accepted as prerequisite relations.
4. **Model selection:** Test multiple threshold values; select the one that minimizes the discrepancy between the observed response patterns and those predicted by the resulting knowledge structure.

#### Corrected IITA

The corrected version (Sargin & Unlu) accounts for the expected violation rate under the null hypothesis (no prerequisite relationship). It computes:

- Observed violations: proportion of students violating a -> b
- Expected violations under independence: product of marginal probabilities
- Corrected score: observed minus expected

This reduces false positives from items that happen to have similar difficulty levels.

#### Minimized Corrected IITA

The minimized corrected variant further refines the corrected version by:

1. Computing the corrected violation rates for all pairs
2. Selecting the relation set that minimizes the overall discrepancy
3. Applying transitivity constraints to ensure the result is a valid quasi-order

This is generally the recommended variant for practical use.

### DAKS R Package Usage

```r
library(DAKS)

# Load response data (binary matrix: students x items)
data <- read.csv("responses.csv")

# Run minimized corrected IITA
result <- iita(data, v = 3)  # v=1: original, v=2: corrected, v=3: minimized corrected

# Extract the surmise relation
relation <- result$implications
# Format: list of (prerequisite, target) pairs

# Evaluate fit
result$diff  # Discrepancy index (lower = better fit)
```

### Python learning_spaces Usage

```python
from learning_spaces.kst import iita

# response_data: pandas DataFrame (students x items, binary)
result = iita(response_data, v=3)

# result contains:
# - 'implications': list of (prerequisite, target) tuples
# - 'diff': discrepancy index
# - 'selection_set_index': which threshold was selected
```

---

## 3. Integration Protocol: Expert + IITA

When both expert-derived (QUERY algorithm) and data-derived (IITA) relations are available, use the following integration protocol:

### Category 1: Agreement (high confidence -- keep)

Relations found by both methods. These have strong support from both theory and data.

- Set `confidence` to max of the two individual confidence scores
- Set `source` to `"expert-and-iita"`
- No further review needed

### Category 2: Expert-Only (flag for review)

Relations the expert asserted but IITA did not find. Possible explanations:
- The data sample is too small to detect the relationship
- The relationship is theoretically sound but students in this population bypass it
- The expert is wrong (rare but possible)

**Action:** Keep the relation but lower its confidence. Flag for review. Consider collecting more targeted data.

### Category 3: IITA-Only (evaluate carefully)

Relations IITA found but the expert did not assert. Possible explanations:
- The expert overlooked a genuine prerequisite
- The relation is a statistical artifact (e.g., correlated difficulty without causal prerequisite)
- The relation is an artifact of the assessment design (items share surface features)

**Action:** Present to the expert for adjudication. If the expert agrees after reflection, add with `source: "iita-confirmed"`. If the expert disagrees with good reason, discard.

### Category 4: Disagreement (contradictions)

Cases where one method says a -> b and the other says b -> a, or where the methods produce conflicting structures.

**Action:** Investigate the specific items. Resolve by examining the cognitive task analysis more carefully and/or collecting additional data.

---

## 4. FCA Constructive Method -- Detailed Steps

Formal Concept Analysis provides an alternative constructive approach to building surmise relations, particularly useful within CbKST (Huang et al., 2025; Li et al., 2024).

### Step 1: Build the Formal Context

Construct a formal context (G, M, I) where:
- G = set of items (objects)
- M = set of competences (attributes)
- I = incidence relation: (g, m) in I iff item g requires competence m (from `required_competences`)

### Step 2: Compute Formal Concepts

A formal concept is a pair (A, B) where:
- A is a set of items (extent)
- B is a set of competences (intent)
- A = {g in G : for all m in B, (g,m) in I} (all items having all competences in B)
- B = {m in M : for all g in A, (g,m) in I} (all competences shared by all items in A)

### Step 3: Build the Concept Lattice

Order concepts by inclusion on extents (or dually, reverse inclusion on intents). This produces a complete lattice.

### Step 4: Derive Knowledge Structure

The knowledge structure is the family of extents of all formal concepts, ordered by set inclusion. This yields:
- A closure system on items (closed under intersection)
- Dually, a knowledge space if the complements form a union-closed family

### Step 5: Extract Surmise Relations

From the concept lattice, the surmise relation is:
- a -> b if the extent containing a is a subset of the extent containing b in every concept where b appears

This means: every formal concept that includes item b also includes item a, so mastery of b surmises mastery of a.

### Advantages of FCA-Based Construction

- **Provably consistent with competence model:** The resulting structure is guaranteed to be compatible with the CbKST skill function
- **Constructive:** No expert queries needed -- the structure is derived mechanically from the competence-item mapping
- **Reveals hidden structure:** The concept lattice may reveal item groupings and competence clusters that were not apparent

### Limitations

- **Depends on competence mapping quality:** If `required_competences` assignments are inaccurate, the derived structure will be wrong
- **May be too fine or too coarse:** The FCA-derived structure captures only the competence-induced dependencies, missing cognitive dependencies not represented in the competence model

---

## 5. Handling Edge Cases

### Items with No Prerequisites (Root Items)

These are foundational items -- no item must be mastered before them. They should appear at the base of the Hasse diagram. Common for:
- Definitions and terminology
- Basic facts
- Entry-level procedural knowledge

Verify that items at the lowest Bloom's level ("remember") are among the root items.

### Items with Many Prerequisites (>5 direct)

Flag these for review. Possible issues:
- Item is too broad and should be decomposed
- Some prerequisites are actually mediated by intermediate items
- The domain genuinely requires broad foundation for this item (less common)

### Equivalent Items (Mutual Prerequisites)

If a -> b and b -> a (detected as a 2-cycle), the items are equivalent in the quasi-order. Options:
1. **Merge** the items into one
2. **Re-examine** -- usually one direction is weaker and should be removed
3. **Keep both** only if they are genuinely interchangeable in all assessment contexts (rare)

### Disconnected Components

If the surmise relation has multiple connected components, the domain has independent sub-domains. This is valid but should be verified:
- Is the independence genuine (e.g., "statistics" and "ethics" in a research methods course)?
- Or is a linking relationship missing?

---

## References

- Koppen, M. & Doignon, J.-P. (1990). "How to build a knowledge space by querying an expert." *Journal of Mathematical Psychology*, 34(3), 311-331.
- Schrepp, M. (1999). "On the empirical construction of implications between bi-valued test items." *Mathematical Social Sciences*, 38(3), 361-375.
- Sargin, A. & Unlu, A. *DAKS: Data Analysis and Knowledge Spaces*. R package v2.1-3. CRAN.
- Segedinac, M. *learning_spaces*. Python package. GitHub: milansegedinac/kst.
- Ganter, B. & Wille, R. (1999). *Formal Concept Analysis: Mathematical Foundations*. Springer.
- Huang, B., Li, J., Li, Q., Zhou, Y. & Chen, H. (2025). "Competence-based knowledge space theory from the perspective of formal concept analysis." *International Journal of Machine Learning and Cybernetics*.
- Li, J. et al. (2024). "Knowledge structures construction and learning paths recommendation based on formal contexts." *International Journal of Machine Learning and Cybernetics*.
- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer.
- Heller, J. & Stefanutti, L. (Eds.) (2024). *Knowledge Structures: Recent Developments in Theory and Application*. World Scientific.
- Cosyn, E., Uzun, H., Doble, C. & Matayoshi, J. (2021). "A practical perspective on knowledge space theory: ALEKS and its data." *Journal of Mathematical Psychology*, 101.
- Hockemeyer, C. (2002). "A comparison of non-deterministic procedures for the adaptive assessment of knowledge." *Psychologische Beitrage*, 44, 172-183.

See `references/bibliography.md` for the complete bibliography.
