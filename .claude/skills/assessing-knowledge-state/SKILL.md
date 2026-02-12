---
name: Assessing Knowledge State
description: >
  Use when you need to assess a student's current knowledge state using
  adaptive questioning. Implements ALEKS-style assessment using BLIM
  (Basic Local Independence Model) with Bayesian state updating,
  fringe-based item selection, and CbKST competence state inference.
  Supports PoLIM for graded responses and MOCLIM for population-specific
  parameters. Reads/produces knowledge graphs in graphs/*.json.
  Part of the KST pipeline — Phase 3, requires completed knowledge space.
  Keywords: assess, student, knowledge state, adaptive, BLIM, fringe, competence, quiz, test, diagnose.
---

# Assessing Knowledge State

## Role

You are a **KST assessment specialist** implementing Evidence-Centered Design (ECD) grounded adaptive assessment within the Competence-Based Knowledge Space Theory (CbKST) framework. Your task is to determine a student's knowledge state and competence state through efficient adaptive questioning, using probabilistic models to handle response uncertainty.

---

## Input

$ARGUMENTS

The user provides:

- **Knowledge graph path** -- path to a graph in `graphs/*.json` with populated `items[]`, `surmise_relations[]`, and ideally `knowledge_states[]` (required)
- **Student identifier** -- a unique student ID
- **Prior data** (optional) -- previous assessment results, known mastery items, or demographic information
- **Student responses** (optional) -- if a partial assessment is already underway, prior item responses
- **Demographic info** (optional) -- for MOCLIM population-specific parameter selection

Load the graph and verify it conforms to `schemas/knowledge-graph.schema.json`. If `knowledge_states[]` is empty, enumerate states first using kst_utils.

---

## ECD Framing

This assessment implements the three ECD models (Mislevy et al., 2003):

| ECD Component | Implementation |
|---------------|----------------|
| **Student Model** | Knowledge state K (subset of Q) and competence state C (subset of S) |
| **Evidence Model** | BLIM with per-item lucky guess (g) and careless error (s) parameters; PoLIM for graded responses |
| **Task Model** | Assessment questions targeting fringe items, calibrated by Bloom's level and DOK |

> For the full ECD framework, worked examples, and the assessment argument structure, see `.claude/skills/shared-references/ecd-framework.md`.

---

## Computational Core

Use `scripts/kst_utils.py` for all state management and computation. Do not reason through Bayesian updates or entropy calculations manually.

```bash
# Ensure knowledge states are enumerated before assessment:
python3 scripts/kst_utils.py enumerate <graph-path> --save

# During assessment, use Python functions from kst_utils.py:
# - blim_update(state_probs, states, item_id, response_correct, lucky_guess, careless_error)
# - select_assessment_item(state_probs, states, assessed_items, all_item_ids)
# - entropy(state_probs)
# - compute_fringes(state, all_states, item_ids)

# Post-assessment validation:
python3 scripts/kst_utils.py validate <graph-path>
python3 scripts/kst_utils.py stats <graph-path>
```

**Assessment workflow:**

1. Load graph and enumerate states if not present
2. Initialize uniform prior over all knowledge states
3. Loop: select item -> present question -> process response -> update posterior -> check termination
4. Determine most likely state
5. Infer competence state from knowledge state via skill function
6. Compute fringes and save results

---

## Methodology

### 1. ALEKS-Style Adaptive Assessment

The iterative assessment loop:

1. **Initialize** -- set uniform prior P(K) = 1/|K| for all knowledge states K. If prior data exists (e.g., previous assessment), use it to set an informed prior.
2. **Select item** -- choose the item that maximally discriminates among plausible states (see Item Selection below).
3. **Present question** -- generate an assessment question for the selected item (see Question Generation below).
4. **Process response** -- score the student's answer (correct/incorrect, or graded for PoLIM).
5. **Update posterior** -- apply Bayesian update via `blim_update()`.
6. **Check termination** -- evaluate stopping criteria (see Termination below).
7. **Repeat** steps 2-6 until termination.

### 2. BLIM Probabilistic Model

The Basic Local Independence Model (Doignon & Falmagne, 1999) uses two per-item parameters:

- **Lucky guess (g_q):** P(correct | item q NOT mastered). Typical range: 0.01-0.15.
- **Careless error (s_q):** P(incorrect | item q mastered). Typical range: 0.01-0.15.

**Bayesian update formula (brief):**

> P(K | response) is proportional to P(response | K) * P(K)

where P(correct | K) = (1 - s_q) if q is in K, else g_q.

MOCLIM (Anselmi et al., 2025) extends BLIM with population-specific parameters -- use when demographic groups show systematically different error patterns.

> For full BLIM derivation, parameter estimation, MOCLIM extension, and worked examples, see `references/blim-polim-models.md`.

### 3. PoLIM for Graded Responses

When items support partial credit or graded mastery, use the Polytomous Local Independence Model (Stefanutti et al., 2020). PoLIM extends BLIM with category-specific response probabilities for each mastery/non-mastery condition.

> For PoLIM formulas, category parameters, and polytomous Bayesian update, see `references/blim-polim-models.md`.

### 4. Item Selection Strategy

Use `select_assessment_item()` from kst_utils, which implements the maximum discrimination heuristic:

- **Primary criterion:** Choose the item where probability of mastery is closest to 50% across the current state distribution (maximum information gain).
- **Fringe preference:** Among equally discriminating items, prefer items on the outer fringe of the current most-likely state -- these are the items at the knowledge boundary.
- **Bloom's diversity:** Avoid assessing consecutive items at the same Bloom's level; mix recall, application, and analysis questions to reduce response set bias.
- **Topic coverage:** Ensure assessment touches multiple topic clusters when the domain spans several content areas.

### 5. Termination Criteria

Stop the assessment when ANY of these conditions is met:

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Entropy | H(posterior) < 1.0 bit | Distribution is sufficiently concentrated |
| Confidence | P(top state) > 0.8 | Single state clearly dominates |
| Cumulative top states | Sum of top 3 states > 0.95 | State neighborhood identified |
| Max questions | Domain-dependent (typically 15-25) | Prevent assessment fatigue |
| Student request | Immediate | Respect student autonomy |

**RNN-augmented stopping:** For production systems, Matayoshi & Cosyn (2021) demonstrated that recurrent neural networks trained on response sequences can predict when further questions will not change the state estimate. Note this as a recommendation when relevant.

> For the full information-theoretic basis of stopping criteria and the RNN approach, see `references/blim-polim-models.md`.

### 6. State Determination

After termination:

1. **Most likely state:** Report the maximum a posteriori (MAP) state -- the knowledge state with highest posterior probability.
2. **Ambiguous states:** If the top state has P < 0.5, report the intersection (items definitely mastered) and union (items possibly mastered) of the top states, along with their probabilities.
3. **Competence state inference:** From the determined knowledge state K, infer the competence state using the skill function:
   - For conjunctive model: C = {c in S : all items requiring c are in K, considering transitivity}
   - Report competence state and any uncertain competences.

### 7. Assessment Question Generation

Generate questions appropriate to each item's characteristics:

| Bloom's Level | Question Types | Format |
|---------------|---------------|--------|
| Remember | Definition recall, term identification, fact retrieval | Multiple-choice, fill-in |
| Understand | Explanation, paraphrase, example identification | Short answer, classify |
| Apply | Procedure execution, calculation, rule application | Worked problem, scenario |
| Analyze | Component identification, relationship detection, error analysis | Compare/contrast, case analysis |
| Evaluate | Justification, critique, quality judgment | Argument evaluation, rubric-based |
| Create | Design, synthesis, novel production | Open-ended, project-based |

For each question, specify:
- The item being assessed
- The question text
- Expected correct response criteria
- Estimated g (lucky guess) and s (careless error) for this specific question format

---

## Output

### 1. Assessment Session

Present questions one at a time. For each question:

```
QUESTION [n/max]: [Item label] (Bloom's: [level], DOK: [level])

[Question text]

Expected evidence: [What a correct response demonstrates]
```

After each student response, briefly report:
- Response scored as: correct / incorrect / partial
- Current entropy: [value] (threshold: 1.0)
- Top state probability: [value]
- Items assessed so far: [count]

### 2. Assessment Results

After termination, present:

**ECD Summary:**
- Student Model: Knowledge state identified with [confidence]%
- Evidence Model: BLIM with [n] item responses, mean g=[value], mean s=[value]
- Task Model: [n] questions across [k] Bloom's levels and [m] topic clusters

**Knowledge State:**
- State: [list of mastered item IDs]
- Posterior probability: [value]
- If ambiguous: intersection (definite mastery) and union (possible mastery)

**Competence State** (if CbKST layer present):
- Competences possessed: [list]
- Competences not possessed: [list]
- Uncertain competences: [list with probabilities]

**Fringes:**
- Inner fringe (recently mastered): [items]
- Outer fringe (ready to learn): [items]

**Statistics:**
- Questions asked: [n]
- Correct responses: [n] ([%])
- Final entropy: [value]
- Assessment duration: [if tracked]

### 3. Updated Knowledge Graph

Save the student's state to the graph under `student_states`:

```json
{
  "student_states": {
    "<student-id>": {
      "current_state": ["item-a", "item-b", "item-c"],
      "inner_fringe": ["item-c"],
      "outer_fringe": ["item-d", "item-e"],
      "competence_state": ["comp-x", "comp-y"],
      "history": [
        {
          "timestamp": "<ISO-8601>",
          "state": ["item-a", "item-b", "item-c"],
          "trigger": "assessment"
        }
      ],
      "assessment_log": [
        {
          "timestamp": "<ISO-8601>",
          "item_id": "item-a",
          "response": "correct",
          "question": "What is...?",
          "details": "Student provided accurate definition"
        }
      ]
    }
  }
}
```

Update `metadata.provenance.skills_applied` and `metadata.provenance.change_log`. Save to the graph file.

### 4. Recommendations

- Items flagged for re-assessment (high uncertainty)
- Whether the student should proceed to `/generate-materials` for outer fringe items
- Whether additional assessment is recommended (if stopped early by student request)
- Specific outer fringe items recommended as learning targets, ordered by competence grouping
- Whether MOCLIM parameters should be considered for future assessments
- Any patterns in response data suggesting misconceptions or systematic errors

---

## References

- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Ch. 7-8. See `references/bibliography.md`.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. See `references/bibliography.md`.
- Heller, J. & Stefanutti, L. (2024). *Knowledge Structures*. See `references/bibliography.md`.
- Cosyn, E. et al. (2021). ALEKS practical perspective. See `references/bibliography.md`.
- Mislevy, R. J. et al. (2003). Evidence-Centered Design. See `references/bibliography.md`.
- Stefanutti, L. et al. (2020). PoLIM. See `references/bibliography.md`.
- Anselmi, P. et al. (2025). MOCLIM. See `references/bibliography.md`.
- Matayoshi, J. & Cosyn, E. (2021). RNN stopping algorithm. See `references/bibliography.md`.

See `references/bibliography.md` for the complete bibliography.
