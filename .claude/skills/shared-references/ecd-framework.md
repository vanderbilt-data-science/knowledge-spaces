# Evidence-Centered Design (ECD) Framework

This reference describes Evidence-Centered Design and its integration with Knowledge Space Theory. Skills that extract knowledge items, decompose learning objectives, or conduct adaptive assessment should use ECD principles to ensure that every assessment item is grounded in a coherent evidentiary argument connecting student knowledge to observable performance.

---

## Overview of Evidence-Centered Design

Evidence-Centered Design (ECD) is a principled framework for assessment design developed by Mislevy, Steinberg, and Almond (2003). ECD treats assessment as an *evidentiary argument*: the goal is to make defensible claims about what a student knows based on what they do in assessment situations.

The central question of ECD is:

> What observable evidence (student responses, performances, products) supports what inferences about what aspects of student knowledge, skill, or ability?

ECD decomposes this question into a structured set of models that, together, form the assessment argument.

---

## The Three Core Models

### 1. Student Model

The **Student Model** specifies the aspects of student knowledge, skill, or ability that the assessment is designed to measure.

- **What it contains:** Variables representing student proficiency, knowledge, competences, or cognitive attributes.
- **In KST terms:** The student model corresponds to the student's **knowledge state** (the set of mastered items) or, in CbKST, the student's **competence state** (the set of possessed competences).
- **Grain size:** The student model defines the granularity of measurement. A coarse model might have a single proficiency variable; KST provides a fine-grained model where each item or competence is a separate variable.
- **Structure:** In KST, the student model is structured by the surmise relation — not all combinations of item mastery are plausible, only those that form valid knowledge states.

#### Student Model Design Questions

1. What are the knowledge components (items, competences) being measured?
2. What is the prerequisite structure among them?
3. What are the plausible states of knowledge?
4. What level of granularity is needed for the intended instructional decisions?

### 2. Evidence Model

The **Evidence Model** specifies how student performances on tasks constitute evidence about the student model variables. It has two components:

#### a. Evidence Rules (Scoring)

- **What they do:** Map raw student responses to observable variables (scores, classifications, features).
- **In KST terms:** Evidence rules determine whether a student's response to an item indicates mastery or non-mastery of that item.
- **Examples:** Correct/incorrect scoring for multiple-choice; rubric-based scoring for constructed response; partial credit models; classification of error types.

#### b. Statistical Model (Measurement)

- **What it does:** Specifies how observable variables (scored responses) update beliefs about the student model variables.
- **In KST terms:** This corresponds to probabilistic assessment models:
  - **BLIM (Basic Local Independence Model):** Each item has a *careless error rate* (probability of incorrect response despite mastery) and a *lucky guess rate* (probability of correct response despite non-mastery). Given a knowledge state, responses are locally independent.
  - **PoLIM (Polytomous Local Independence Model):** Extension of BLIM to polytomous items with graded response levels.
- **Updating mechanism:** In KST adaptive assessment, the statistical model uses Bayesian updating — the prior distribution over knowledge states is updated after each item response to produce a posterior distribution.

#### Evidence Model Design Questions

1. How will student responses be scored? (Dichotomous? Partial credit? Rubric-based?)
2. What error rates are plausible? (Careless errors? Lucky guesses?)
3. What statistical model connects scored responses to knowledge state estimates?
4. How many items are needed for reliable state identification?

### 3. Task Model

The **Task Model** specifies the situations (tasks, questions, problems) presented to students to elicit evidence.

- **What it contains:** Specifications for tasks including content, format, difficulty, context, and any features that affect the evidence the task provides.
- **In KST terms:** Each task (item) is an element of the knowledge domain Q. The task model specifies:
  - What knowledge the item is intended to assess (which competences are required, per the CbKST skill map).
  - The item's position in the surmise relation (what prerequisites it has).
  - The item's format and presentation (multiple-choice, free-response, performance task, etc.).
  - The item's difficulty characteristics (DOK level, Bloom's level, expected error rates).
- **Item design features:** The task model should specify features that make the item a good piece of evidence — features that ensure the item discriminates between students who have and have not mastered the targeted knowledge.

#### Task Model Design Questions

1. What knowledge component(s) does this item target?
2. What is the item's position in the prerequisite structure?
3. What format will best elicit the targeted evidence?
4. What distractors or scaffolding are appropriate?
5. What is the expected difficulty (careless error rate, lucky guess rate)?

---

## The Assessment Argument Structure

ECD structures assessment as a chain of reasoning:

```
Task Model                Evidence Model              Student Model
(What we ask)    --->     (What we observe)    --->   (What we conclude)

Tasks/Items        -->    Scored Responses     -->    Knowledge/Competence State
                          (evidence rules)            (statistical model)
```

### The Argument in Detail

1. **Tasks are designed** (Task Model) to elicit specific performances.
2. **Performances are scored** (Evidence Rules) to produce observable data.
3. **Observable data updates beliefs** (Statistical Model) about student knowledge.
4. **Updated beliefs inform decisions** about instruction, placement, or certification.

### Validity Through Design

ECD ensures **construct validity** by design rather than post-hoc analysis:
- Every task is designed to target specific student model variables.
- The evidence model explicitly links task performance to student knowledge.
- The statistical model is transparent about assumptions (error rates, independence, etc.).

---

## Mapping ECD to KST

| ECD Component | KST Equivalent | CbKST Extension |
|---------------|----------------|------------------|
| **Student Model variables** | Items in domain Q | Competences in S |
| **Student Model structure** | Surmise relation (quasi-order on Q) | Competence prerequisite relation on S |
| **Student Model state** | Knowledge state K (subset of Q) | Competence state C (subset of S) |
| **Evidence Rules** | Correct/incorrect scoring | Polytomous scoring (PoLIM) |
| **Statistical Model** | BLIM (Basic Local Independence Model) | Competence-based BLIM; PoLIM |
| **Task Model** | Items q in Q with prerequisite positions | Items q with required_competences mu(q) |
| **Assessment argument** | Adaptive assessment via fringe-based item selection | Same, with competence-level inference |

### BLIM Parameters

For each item q, the BLIM specifies two parameters:

- **beta_q (careless error rate):** P(incorrect response | q is in the student's knowledge state). Typical range: 0.01–0.15.
- **eta_q (lucky guess rate):** P(correct response | q is not in the student's knowledge state). Typical range: 0.01–0.15.

The likelihood of a response pattern R given knowledge state K is:

> P(R | K) = product over q in Q of P(R_q | K)

where:
- P(correct | q in K) = 1 - beta_q
- P(correct | q not in K) = eta_q

### Adaptive Assessment Flow

1. Initialize a prior distribution over all knowledge states (often uniform or informed by population data).
2. Select an item from the outer fringe of the most likely state(s) — this maximizes information gain.
3. Present the item; score the response.
4. Update the posterior distribution over knowledge states using BLIM.
5. Repeat until the posterior is sufficiently concentrated (typically 15–25 items).
6. Report the maximum a posteriori (MAP) knowledge state.

---

## Expanded ECD for Learning Systems (Arieli-Attali et al., 2019)

The expanded ECD (e-ECD) framework extends classical ECD beyond summative assessment to encompass continuous learning systems — contexts where assessment and instruction are interleaved.

### Key Extensions

#### 1. Activity Model (extending the Task Model)

In e-ECD, the Task Model is expanded to an **Activity Model** that encompasses not just assessment items but all learning activities:

- **Instructional activities:** Lessons, readings, worked examples, practice problems.
- **Assessment activities:** Quizzes, tests, performance tasks.
- **Exploratory activities:** Simulations, investigations, projects.

Each activity is characterized by the knowledge it targets and the evidence it can provide about student learning.

#### 2. Feedback Model

e-ECD adds an explicit **Feedback Model** that specifies:

- What feedback to provide based on the student's estimated knowledge state.
- When to provide feedback (immediate, delayed, on-demand).
- What form feedback should take (correctness, hints, explanations, worked examples).
- How feedback targets the outer fringe — directing the student toward items they are ready to learn.

#### 3. Learning Model

The **Learning Model** describes how the student model is expected to change over time:

- How instruction is expected to move the student from one knowledge state to a more advanced one.
- The expected learning trajectory through the knowledge space.
- How the system monitors whether actual progress matches expected progress.

### e-ECD and KST Integration

| e-ECD Component | KST Implementation |
|-----------------|-------------------|
| **Activity Model** | Items in Q plus associated learning materials; activities target outer fringe items |
| **Feedback Model** | Feedback targets the outer fringe; materials are generated for fringe items using UDL principles |
| **Learning Model** | Learning paths through the knowledge space; expected transitions between knowledge states |
| **Continuous Student Model** | Knowledge state updated after every activity, not just formal assessments |

---

## Practical Guidance: Articulating Evidence Models

When creating knowledge items and assessment tasks, each item should have an explicit evidence model. The following template supports this:

### Per-Item Evidence Specification

For each item q in the knowledge domain:

1. **Target knowledge:** What specific knowledge component(s) does this item assess? (In CbKST: what competences are required?)

2. **Observable evidence:** What does a correct response look like? What does an incorrect response look like? Are there partial-credit categories?

3. **Scoring rule:** How is the response mapped to a score?
   - Dichotomous: correct (1) or incorrect (0).
   - Polytomous: levels 0, 1, ..., m with defined criteria for each level.

4. **Error model:**
   - Estimated careless error rate (beta): How likely is a knowledgeable student to make a mistake on this item?
   - Estimated lucky guess rate (eta): How likely is a non-knowledgeable student to answer correctly by chance?
   - Factors affecting error rates: item format, number of response options, partial knowledge applicability.

5. **Discriminating features:** What aspects of the item design ensure it differentiates between students who have and have not mastered the target knowledge?
   - Distractor design (for multiple-choice): distractors should reflect common misconceptions.
   - Scaffolding removal: items should not provide so much scaffolding that non-knowledgeable students can succeed.
   - Context specificity: items should require the targeted knowledge, not allow workarounds.

6. **Prerequisite alignment:** Does the item's position in the surmise relation accurately reflect its cognitive demands? Items with more prerequisites should genuinely require mastery of those prerequisite items.

### Example Evidence Specification

```
Item: "Compute the derivative of f(x) = 3x^2 + 2x - 5"

Target knowledge: Power rule for differentiation, constant rule,
                  sum/difference rule
Required competences: {power-rule, constant-rule, sum-rule}
Prerequisites: {limits-concept, function-notation, polynomial-algebra}

Observable evidence:
  - Correct: f'(x) = 6x + 2
  - Common errors: f'(x) = 6x (forgot constant term derivative),
                   f'(x) = 3x^2 + 2 (did not reduce power),
                   f'(x) = 6x + 2 - 5 (did not differentiate constant)

Scoring: Dichotomous (correct/incorrect)
Estimated beta (careless error): 0.05 (arithmetic slips)
Estimated eta (lucky guess): 0.02 (very low — hard to guess)

Discriminating features: Requires applying multiple differentiation
rules in combination; common errors reveal specific missing competences.
```

---

## References

- Arieli-Attali, M., Ward, S., Thomas, J., Deonovic, B., & von Davier, A. A. (2019). The expanded Evidence-Centered Design (e-ECD) for learning and assessment systems: A framework for incorporating learning goals and processes within assessment design. *Frontiers in Psychology, 10*, 853.
- Doignon, J.-P., & Falmagne, J.-C. (1999). *Knowledge spaces*. Springer.
- Falmagne, J.-C., & Doignon, J.-P. (2011). *Learning spaces: Interdisciplinary applied mathematics*. Springer.
- Heller, J., & Stefanutti, L. (2024). *Knowledge structures: Recent developments*. In D. Ifenthaler, P. Isaias, & D. G. Sampson (Eds.), *Open and inclusive educational practice in the digital world*. Springer.
- Mislevy, R. J., Steinberg, L. S., & Almond, R. G. (2003). On the structure of educational assessments. *Measurement: Interdisciplinary Research and Perspectives, 1*(1), 3–62.
- Stefanutti, L., de Chiusole, D., Gondan, M., & Maurer, A. (2020). Modeling misconceptions in knowledge space theory. *Journal of Mathematical Psychology, 94*, 102306.
