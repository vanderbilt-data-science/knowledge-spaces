# BLIM and PoLIM — Probabilistic Assessment Models

This reference provides the full mathematical detail for the probabilistic models used in adaptive KST assessment. The SKILL.md file references this document for formulas, parameter estimation, and advanced extensions.

---

## BLIM — Basic Local Independence Model

### Model Specification

The BLIM (Doignon & Falmagne, 1999, Ch. 7; Heller & Stefanutti, 2024) is the standard probabilistic model for KST assessment. It defines the probability of observing a response pattern given a knowledge state.

**Parameters for each item q in Q:**

- **beta_q (careless error rate):** P(incorrect response | q is in the student's knowledge state K). The student knows the item but makes a mistake. Typical range: 0.01-0.15.
- **eta_q (lucky guess rate):** P(correct response | q is NOT in the student's knowledge state K). The student does not know the item but answers correctly by chance. Typical range: 0.01-0.15.

**Local independence assumption:** Given the knowledge state K, responses to different items are conditionally independent.

### Likelihood Function

For a response pattern R = (R_1, R_2, ..., R_n) where R_q is in {0, 1} (0 = incorrect, 1 = correct), and a knowledge state K:

```
P(R | K) = product over all q in Q of P(R_q | K)
```

where:

```
P(R_q = 1 | K) = (1 - beta_q)  if q is in K     [correct despite mastery: no careless error]
P(R_q = 1 | K) = eta_q          if q is not in K  [correct despite non-mastery: lucky guess]
P(R_q = 0 | K) = beta_q         if q is in K      [incorrect despite mastery: careless error]
P(R_q = 0 | K) = (1 - eta_q)    if q is not in K  [incorrect despite non-mastery: expected]
```

### Bayesian State Updating

Given a prior distribution P(K) over knowledge states and a response R_q to item q, the posterior is computed via Bayes' theorem:

```
P(K | R_q) = P(R_q | K) * P(K) / P(R_q)
```

where the normalizing constant is:

```
P(R_q) = sum over all states K' of P(R_q | K') * P(K')
```

**Sequential updating:** In adaptive assessment, responses arrive one at a time. After each response, the posterior becomes the prior for the next update. This is mathematically equivalent to computing the posterior from all responses simultaneously (due to local independence), but sequential updating is computationally more efficient.

**Implementation in kst_utils.py:** The `blim_update()` function performs this computation:

```python
blim_update(
    state_probs,       # Current distribution over states
    states,            # {state_id: set of item IDs}
    item_id,           # Which item was assessed
    response_correct,  # True/False
    lucky_guess=0.1,   # eta_q default
    careless_error=0.1 # beta_q default
)
```

### Derivation of the Update

**For a correct response (R_q = 1):**

```
P(K | R_q=1) = P(R_q=1 | K) * P(K) / Z

If q in K:  P(R_q=1 | K) = 1 - beta_q
If q not in K:  P(R_q=1 | K) = eta_q

Z = sum_K' [(1-beta_q) * P(K') * I(q in K') + eta_q * P(K') * I(q not in K')]
```

States containing q are upweighted by factor (1 - beta_q); states not containing q are downweighted to factor eta_q. Since typically (1 - beta_q) >> eta_q (e.g., 0.9 >> 0.1), a correct response strongly favors states containing the item.

**For an incorrect response (R_q = 0):**

```
P(K | R_q=0) = P(R_q=0 | K) * P(K) / Z

If q in K:  P(R_q=0 | K) = beta_q
If q not in K:  P(R_q=0 | K) = 1 - eta_q

Z = sum_K' [beta_q * P(K') * I(q in K') + (1-eta_q) * P(K') * I(q not in K')]
```

States containing q are downweighted to factor beta_q; states not containing q are upweighted by factor (1 - eta_q).

### Parameter Estimation

BLIM parameters can be estimated by:

1. **Expert judgment:** Set beta_q and eta_q based on item characteristics:
   - Multiple-choice with k options: eta_q approximately 1/k (e.g., 0.25 for 4-option MC)
   - Free-response: eta_q approximately 0.01-0.05 (very hard to guess)
   - Procedural items with common slips: beta_q approximately 0.05-0.15
   - Well-defined factual items: beta_q approximately 0.01-0.05

2. **Maximum likelihood estimation (MLE):** From population response data, estimate parameters using the EM algorithm (Heller & Stefanutti, 2024):
   - E-step: compute expected state assignments given current parameters
   - M-step: update beta_q and eta_q from expected assignments
   - Iterate until convergence

3. **MDML estimation:** Minimum Discrepancy Maximum Likelihood (Heller & Wickelmaier, 2013) provides joint estimation of the knowledge structure and BLIM parameters from response data.

**R package support:** The `pks` package (Wickelmaier & Heller, 2024) provides `blim()` for fitting BLIM models, including EM-based parameter estimation and goodness-of-fit tests.

---

## MOCLIM — Multiple Observed Classifications Local Independence Model

### Extension Rationale

The standard BLIM assumes a single set of item parameters (beta_q, eta_q) for all students. MOCLIM (Anselmi et al., 2025) extends this by allowing multiple classification systems -- different groups of students may have systematically different error patterns.

### Model Structure

MOCLIM introduces G classification groups (e.g., based on prior coursework, language proficiency, or demographic factors):

```
P(R | K, group=g) = product over q of P_g(R_q | K)
```

where P_g denotes group-specific parameters:

- **beta_{q,g}:** Careless error rate for item q in group g
- **eta_{q,g}:** Lucky guess rate for item q in group g

### When to Use MOCLIM

- When different student populations interact with items differently (e.g., language-related careless errors for non-native speakers)
- When item formats vary across administrations and different formats yield different error rates
- When prior data reveals systematic parameter differences across identifiable groups

### Integration with Assessment

During assessment, if the student's group membership is known:
1. Use group-specific parameters for Bayesian updating
2. If group membership is uncertain, marginalize over groups weighted by prior group probabilities

---

## PoLIM — Polytomous Local Independence Model

### Motivation

Classical BLIM uses dichotomous (correct/incorrect) responses. PoLIM (Stefanutti et al., 2020) extends this to items with multiple response categories, supporting:

- Partial credit scoring (e.g., 0, 1, 2, 3 points)
- Graded mastery levels (e.g., novice, competent, expert)
- Multi-step problems with partial solutions

### Model Specification

For a polytomous item q with response categories L_q = {0, 1, ..., m_q}:

**Category-specific parameters:**

- **pi_{q,l|M}:** P(response = l | q mastered), for each category l. These must sum to 1 over l.
- **pi_{q,l|~M}:** P(response = l | q not mastered), for each category l. These must sum to 1 over l.

For mastered items, probability mass concentrates on higher categories. For non-mastered items, probability mass concentrates on lower categories.

### Polytomous Bayesian Update

For a response R_q = l to polytomous item q:

```
P(K | R_q = l) = P(R_q = l | K) * P(K) / Z

If q in K:    P(R_q = l | K) = pi_{q,l|M}
If q not in K: P(R_q = l | K) = pi_{q,l|~M}
```

The update structure is identical to BLIM; only the likelihood values change from the dichotomous case.

### Relationship to BLIM

BLIM is a special case of PoLIM where m_q = 1 for all items:
- pi_{q,1|M} = 1 - beta_q (correct given mastery)
- pi_{q,0|M} = beta_q (careless error)
- pi_{q,1|~M} = eta_q (lucky guess)
- pi_{q,0|~M} = 1 - eta_q (incorrect given non-mastery)

### When to Use PoLIM

- Items involve multi-step procedures where partial completion is informative
- Constructed-response items where rubric-based scoring provides more than binary information
- Skill demonstrations with observable proficiency levels
- When partial credit information would reduce the number of questions needed for state determination

---

## Procedural KST

### When to Use

Procedural KST (Stefanutti, 2021) applies when the domain involves problem-solving procedures -- sequences of steps that students execute to solve problems, where the order and correctness of individual steps is observable.

### Markov Solution Process Models

Rather than assessing items as isolated units, procedural KST models the student's solution process as a Markov chain:

- **States:** Intermediate problem states during solution
- **Transitions:** Steps taken by the student (correct or incorrect)
- **Absorbing states:** Correct solution or abandonment

The transition probabilities depend on the student's competence state, providing richer evidence than binary correct/incorrect scoring.

### Integration with Standard Assessment

Procedural KST items can be incorporated into a standard BLIM/PoLIM assessment:
1. Model the procedure as a polytomous item where the response category reflects solution quality
2. Use the Markov process analysis for detailed diagnostic information
3. Feed the polytomous score into the standard Bayesian update

> See Stefanutti (2021) and Stefanutti et al. (2023, 2025) for formal model definitions, algorithms for adaptive procedural assessment, and the two Markov solution process variants.

---

## Item Selection Algorithms

### Information-Theoretic Basis

The goal of item selection is to minimize the expected posterior entropy -- equivalently, to maximize the expected information gain from the next item.

**Expected information gain** for item q:

```
IG(q) = H(prior) - E[H(posterior | R_q)]
     = H(prior) - [P(R_q=1) * H(posterior | R_q=1) + P(R_q=0) * H(posterior | R_q=0)]
```

where H denotes Shannon entropy:

```
H(P) = -sum over K of P(K) * log2(P(K))
```

**Implementation in kst_utils.py:** The `entropy()` function computes H(P) and `select_assessment_item()` uses the 50/50 heuristic as a computationally efficient approximation of maximum information gain.

### The 50/50 Heuristic

Computing exact expected information gain requires simulating both possible responses for every candidate item, which is O(|Q| * |K|). The 50/50 heuristic approximates this efficiently:

1. For each unassessed item q, compute P(mastered) = sum of P(K) over states K containing q.
2. Select the item where P(mastered) is closest to 0.5.

**Rationale:** An item with 50% mastery probability maximally splits the state space -- a correct response eliminates roughly half the probability mass, and an incorrect response eliminates the other half. This is analogous to binary search.

**Empirical validation:** The ALEKS system uses this heuristic and typically converges in 15-25 items for domains of 200-500 items (Cosyn et al., 2021), demonstrating its practical effectiveness.

### Refinements

Beyond the 50/50 heuristic, secondary item selection criteria include:

1. **Fringe preference:** Prefer items on the outer fringe of the current MAP state, as these are at the knowledge boundary and thus most informative about the student's exact position.
2. **Bloom's level diversity:** Avoid consecutive items at the same cognitive level; alternate between recall, application, and analysis.
3. **Topic coverage:** Ensure items span multiple content clusters when assessing broad domains.
4. **Recency avoidance:** Do not re-assess items that were recently assessed (in the current session or recent prior sessions).

---

## RNN-Augmented Stopping

### Motivation

Traditional stopping criteria (entropy threshold, confidence threshold) are fixed and may not optimally balance assessment accuracy against length for individual students. Matayoshi & Cosyn (2021) proposed training a recurrent neural network to predict when additional items will not change the state estimate.

### Approach

1. **Training data:** Historical assessment sessions with known final states.
2. **Input features:** Sequence of (item_id, response, current_entropy, current_top_state_prob) tuples.
3. **Output:** Binary prediction -- will the final state estimate change if more items are presented?
4. **Architecture:** LSTM or GRU network processing the response sequence.

### Results

The RNN-based stopping algorithm:
- Reduced average assessment length by 15-20% compared to fixed thresholds
- Maintained or improved state identification accuracy
- Adapted stopping point to individual response patterns (stopping earlier for students with clear states, continuing longer for ambiguous cases)

### Practical Recommendation

For production systems processing many students, training an RNN stopping model is recommended. For single-use or small-scale assessment, the fixed threshold criteria are sufficient.

---

## References

- Anselmi, P., Heller, J., Stefanutti, L. & Robusto, E. (2025). An extension of the basic local independence model to multiple observed classifications. *British Journal of Mathematical and Statistical Psychology*.
- Cosyn, E., Uzun, H., Doble, C. & Matayoshi, J. (2021). A practical perspective on knowledge space theory: ALEKS and its data. *Journal of Mathematical Psychology, 101*.
- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer. Ch. 7-8.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. Springer.
- Heller, J. & Stefanutti, L. (2024). *Knowledge Structures: Recent Developments*. World Scientific.
- Hockemeyer, C. (2002). A comparison of non-deterministic procedures for the adaptive assessment of knowledge. *Psychologische Beitrage, 44*, 172-183.
- Matayoshi, J. & Cosyn, E. (2021). Are we there yet? Evaluating the effectiveness of a recurrent neural network-based stopping algorithm for an adaptive assessment. *International Journal of Artificial Intelligence in Education, 31*, 714-737.
- Stefanutti, L. (2021). Markov solution processes: Modeling human problem solving with procedural knowledge space theory. *Journal of Mathematical Psychology, 101*.
- Stefanutti, L., de Chiusole, D., Anselmi, P. & Spoto, A. (2020). Extending the basic local independence model to polytomous data. *Psychometrika, 85*, 684-715.
- Stefanutti, L., Anselmi, P. & de Chiusole, D. (2023). Algorithms for the adaptive assessment of procedural knowledge and skills. *Behavior Research Methods, 55*, 4412-4436.
- Stefanutti, L. et al. (2025). Two Markov solution process models for the assessment of planning in problem solving. *Psychometrika, 90*, 717-733.
- Wickelmaier, F. & Heller, J. (2024). *pks: Probabilistic Knowledge Structures*. R package v0.6-1. CRAN.
