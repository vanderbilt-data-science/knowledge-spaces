# Validation Criteria -- Extended Reference

This reference provides detailed rationale for educational plausibility checks, empirical validation methodology, polytomous validation details, and quality metric interpretation. Consult this for the reasoning behind the criteria in the SKILL.md.

---

## 1. Educational Plausibility Rationale

### 1.1 Miller's Law and Prerequisite Load

**Miller's Law (1956):** Working memory can hold approximately 7 +/- 2 chunks of information simultaneously.

**Application to KST:** When an item has more than ~7 direct prerequisites, a student must hold awareness of all prerequisite concepts to integrate them into mastery of the target item. Exceeding this threshold suggests:

- The item may be too broadly defined and should be decomposed into smaller items
- Some listed prerequisites are actually transitive (mediated through other items) and should not be listed as direct
- The item genuinely requires broad integration (acceptable in some domains, but should be consciously designed)

**Thresholds:**
- 1-5 direct prerequisites: Normal
- 6-7 direct prerequisites: Acceptable but review for possible decomposition
- 8-9 direct prerequisites: Warning -- likely needs restructuring
- 10+ direct prerequisites: Strong warning -- almost certainly needs decomposition

**Total prerequisite load** (including transitive): If an item requires more than 70% of all domain items as prerequisites (directly or transitively), it sits at an extreme position in the hierarchy. This is mathematically valid but pedagogically concerning -- it means the student must master nearly the entire domain before attempting this item. Such items may be better classified as assessment milestones or capstone items rather than individual knowledge items.

### 1.2 Bloom's Taxonomy Consistency

**Rationale:** Bloom's Revised Taxonomy (Anderson & Krathwohl, 2001) describes a generally hierarchical model of cognitive processes: Remember < Understand < Apply < Analyze < Evaluate < Create. While exceptions exist (a "remember" item can legitimately depend on "apply" if, say, remembering a procedure's output requires first applying it), consistent inversions suggest structural problems.

**Level inversion types:**

1. **Strong inversion (WARN):** A "remember" item has an "evaluate" or "create" item as a prerequisite. This almost always indicates either:
   - The items are mis-classified (the "remember" item actually requires higher-order thinking)
   - The prerequisite relationship is incorrect

2. **Mild inversion (INFO):** A "understand" item has an "apply" item as a prerequisite. This can be legitimate (e.g., understanding a concept may require first applying a simpler procedure to see it in action).

3. **Cross-type inversion (REVIEW):** A "factual/remember" item depends on a "procedural/apply" item. This pattern sometimes reflects legitimate pedagogical design (learn-by-doing followed by reflection) but should be verified.

**Implementation:** Compare Bloom's ordinal levels across each prerequisite pair. Flag cases where the prerequisite has a strictly higher level than the target.

### 1.3 Structural Balance

**Orphaned items:** Items with no prerequisite relationships at all (neither prerequisite of nor dependent on any other item) are disconnected from the knowledge structure. This means:
- The adaptive assessment cannot reach them through fringe-based navigation
- They represent isolated facts/skills that do not integrate into the domain's structure
- Some orphans are legitimate (e.g., a safety protocol in a chemistry course that is independent of chemistry content), but most indicate incomplete structure construction

**Bottleneck items:** If a single item is a prerequisite for >50% of all other items, it represents a critical chokepoint. Pedagogical concerns:
- Students who struggle with this item are blocked from most of the domain
- The item may be too coarse-grained (combining multiple prerequisite skills)
- Assessment accuracy for this item becomes disproportionately important

**Balanced branching:** The ratio of maximum to minimum outer fringe size across states indicates how much "choice" varies across the knowledge space. Extreme ratios (>10:1) suggest that some parts of the space are well-structured (many options at each step) while others are bottlenecked (only one option). This is not necessarily wrong but should be a conscious design choice.

### 1.4 Coverage Analysis

When original course materials are available, check:

- **Topic coverage:** Every major topic/unit in the syllabus should be represented by at least one item. Missing topics indicate gaps in Phase 1 extraction.
- **Bloom's distribution:** A well-designed course typically spans at least 3 Bloom's levels. A domain with only "remember" items lacks higher-order assessment; one with only "create" items lacks foundational grounding.
- **Knowledge type distribution:** Items should span at least 2 of the 4 knowledge types (factual, conceptual, procedural, metacognitive). Purely factual domains miss procedural skills; purely procedural domains miss conceptual understanding.

---

## 2. Empirical Validation Methods

### 2.1 BLIM Fit Assessment

The **Basic Local Independence Model** (BLIM; Doignon & Falmagne, 1999; implemented in the `pks` R package by Wickelmaier & Heller, 2024) is the standard probabilistic model for KST.

**Model parameters:**
- For each knowledge state K: P(K) = probability that a randomly selected student is in state K
- For each item i: beta_i = P(correct response | item not mastered) -- the lucky guess rate
- For each item i: eta_i = P(incorrect response | item mastered) -- the careless error rate

**Fitting procedure:**
1. Collect binary response data (students x items)
2. Specify the knowledge space (the family of feasible states)
3. Estimate P(K), beta_i, eta_i via maximum likelihood (EM algorithm)
4. Evaluate goodness-of-fit

**R code example:**
```r
library(pks)

# response_data: binary matrix (students x items)
# knowledge_states: list of item sets (each a character vector)

fit <- blim(response_data, knowledge_states)
summary(fit)

# Key outputs:
# - Log-likelihood
# - AIC/BIC
# - Parameter estimates (state probabilities, lucky guess rates, careless error rates)
# - Goodness-of-fit test (chi-squared)
```

**Interpreting BLIM fit:**
- **Good fit (p > 0.05 on chi-squared test):** The knowledge structure is consistent with observed student behavior
- **Poor fit (p < 0.05):** The structure does not match student response patterns. Possible causes:
  - Missing knowledge states (the space is too restrictive)
  - Incorrect prerequisite relations
  - Items that are poorly discriminating (very high guess rates or error rates)
  - Violations of local independence (students' responses to items are correlated even within a fixed knowledge state)

**PoLIM extension:** The Polytomous Local Independence Model (Stefanutti et al., 2020) extends BLIM to polytomous data. Use when items have graded mastery levels.

### 2.2 IITA Comparison

After fitting IITA to student response data (see the building-surmise-relations reference for IITA algorithm details), compare the empirically derived surmise relation with the expert-derived one.

**Comparison methodology:**
1. Run IITA (minimized corrected variant, v=3) on the response data
2. Extract the empirical surmise relation
3. Compare with the expert-derived relation:
   - **Agreement set:** Relations in both (strong support)
   - **Expert-only set:** Relations the expert asserted but IITA did not find (review)
   - **IITA-only set:** Relations IITA found but the expert did not assert (evaluate)
4. Compute agreement statistics:
   - Jaccard similarity: |Agreement| / |Expert union IITA|
   - Expert coverage: |Agreement| / |Expert|
   - IITA coverage: |Agreement| / |IITA|

**Thresholds:**
- Jaccard > 0.7: Good agreement; expert structure is empirically supported
- Jaccard 0.4-0.7: Moderate agreement; investigate discrepancies
- Jaccard < 0.4: Poor agreement; significant structural revision may be needed

### 2.3 Discrepancy Index and Gamma-Index

**Discrepancy index (DI):** Measures the proportion of students whose observed response patterns are not consistent with any knowledge state in the space. Lower is better.

- DI < 0.05: Excellent fit
- DI 0.05-0.10: Acceptable fit
- DI 0.10-0.20: Marginal; review structure
- DI > 0.20: Poor fit; significant revision needed

**Gamma-index:** A standardized measure of fit that accounts for the expected discrepancy under the null model. Values closer to 1 indicate better fit.

**R code:**
```r
library(kst)

# Compute discrepancy
di <- discrepancy_index(response_data, knowledge_states)

# Compute gamma
gamma <- gamma_index(response_data, knowledge_states)
```

---

## 3. Polytomous Validation -- Extended Details

### 3.1 Polytomous Knowledge Structures (Stefanutti et al., 2020, 2022)

In the polytomous generalization, items have ordered mastery levels: 0, 1, ..., L_i for item i. A polytomous knowledge state is a tuple (l_1, l_2, ..., l_n) specifying each item's mastery level.

**Key axioms for polytomous structures:**

1. **Downward closure (generalized):** If state s = (l_1, ..., l_n) is feasible, then for any item i and any level l'_i < l_i, the state s' = (l_1, ..., l'_i, ..., l_n) must also be feasible (possibly with adjustments to dependent items).

2. **Level-specific prerequisites:** The surmise relation specifies that reaching level k in item i requires at least level m in item j. This generalizes binary prerequisites to level-dependent ones.

3. **Monotonicity:** If level k in item i requires level m in item j, then level k+1 in item i requires at least level m in item j. Higher levels cannot have relaxed prerequisites.

### 3.2 Validation Checks for Polytomous Structures

**Level range consistency:**
- Each item should have levels 0, 1, ..., L_i with no gaps
- Level 0 should represent "not mastered" for all items
- The maximum level should represent "fully mastered"

**Level description quality:**
- Each level should have a clear, distinguishable description
- Adjacent levels should represent a meaningful increment in mastery
- Levels should not overlap in scope (e.g., level 2 should not be a subset of level 1)

**Surmise relation level consistency:**
- If (item-a, level-2) -> (item-b, level-3), then (item-a, level-1) -> (item-b, level-2) should also hold unless there is a documented reason for the asymmetry
- Level prerequisites should form a consistent partial order on the product of all level ranges

**State space validation:**
- Verify that the zero tuple (0, 0, ..., 0) is a feasible state
- Verify that the maximum tuple (L_1, L_2, ..., L_n) is a feasible state
- Check that the number of feasible polytomous states is reasonable given the level ranges

---

## 4. Quality Metric Formulas and Interpretation

### Discrimination Index

```
DI = |K| / 2^|Q|
```

Where |K| is the number of feasible knowledge states and |Q| is the number of items.

**Interpretation:**
- DI = 1.0: No constraints; every subset is a valid state. The knowledge space has no structure (useless).
- DI ~ 0.5: Moderate constraints. The surmise relation eliminates about half of possible states.
- DI < 0.1: Highly constrained. The surmise relation imposes strong structure. This is typical of well-designed domains.
- DI ~ |Q|/2^|Q| (approaching minimum): The space is essentially a single chain. Every item has a unique position in the hierarchy with no branching.

### Average Path Length

The average number of items in a learning path from the empty set to Q, averaged across all maximal chains in the knowledge space.

**Interpretation:**
- Equal to |Q|: All paths include every item (well-graded space). This is always the case for spaces derived from quasi-orders.
- Variance in path length (across different orderings): Indicates how much flexibility exists in sequencing.

### Bottleneck Score

```
Bottleneck = max over all items i of (|{j : i -> j directly or transitively}| / |Q|)
```

**Interpretation:**
- < 0.3: No significant bottlenecks
- 0.3-0.5: Moderate bottleneck; review the high-scoring items
- > 0.5: Severe bottleneck; the item may need decomposition

### Fringe Compactness

```
FC = mean(|outer_fringe(K)| / |K|) for all non-empty states K
```

**Interpretation:**
- Low FC (< 0.3): Fringes are compact relative to state size. This is ideal for adaptive assessment efficiency (fewer candidate items to assess).
- High FC (> 0.5): Fringes are large relative to state size. The space has high branching factor, which means more assessment questions may be needed to pinpoint the student's state.
- ALEKS empirical data (Cosyn et al., 2021) shows FC values in practice tend to be quite low even for large domains.

### Competence Coverage Ratio

```
CCR = |{items with non-empty required_competences}| / |items|
```

Should be 1.0 in a complete CbKST model. Values below 1.0 indicate items not grounded in the competence layer.

### Competence Utilization

```
CU = |{competences required by at least one item}| / |competences|
```

Should be 1.0. Unused competences (CU < 1.0) are dead weight in the model and should be either mapped to items or removed.

---

## References

- Anderson, L. W. & Krathwohl, D. R. (Eds.) (2001). *A Taxonomy for Learning, Teaching, and Assessing*. Longman.
- Cosyn, E., Uzun, H., Doble, C. & Matayoshi, J. (2021). "A practical perspective on knowledge space theory: ALEKS and its data." *Journal of Mathematical Psychology*, 101.
- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. Springer.
- Heller, J. & Stefanutti, L. (Eds.) (2024). *Knowledge Structures: Recent Developments in Theory and Application*. World Scientific.
- Hockemeyer, C. (2002). "A comparison of non-deterministic procedures for the adaptive assessment of knowledge." *Psychologische Beitrage*, 44, 172-183.
- Miller, G. A. (1956). "The magical number seven, plus or minus two: Some limits on our capacity for processing information." *Psychological Review*, 63(2), 81-97.
- Sargin, A. & Unlu, A. *DAKS: Data Analysis and Knowledge Spaces*. R package v2.1-3. CRAN.
- Stahl, C. & Hockemeyer, C. (2022). *kst: Knowledge Space Theory*. R package v0.5-4. CRAN.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2020). "Extending the Basic Local Independence Model to Polytomous Data." *Psychometrika*, 85, 684-715.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2022). "Notes on the polytomous generalization of knowledge space theory." *Journal of Mathematical Psychology*, 108.
- Wickelmaier, F. & Heller, J. (2024). *pks: Probabilistic Knowledge Structures*. R package v0.6-1. CRAN.

See `references/bibliography.md` for the complete bibliography.
