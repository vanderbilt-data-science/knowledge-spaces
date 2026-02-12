---
name: Planning Adaptive Instruction
description: >
  Use when you need to plan a class session using class-wide knowledge
  state data. Analyzes aggregate student states and competence profiles
  to determine optimal teaching targets, student groupings, peer tutoring
  pairings, and session structure following UDL 3.0 principles.
  Uses scripts/kst_utils.py analytics for class-wide computations.
  Reads/produces knowledge graphs in graphs/*.json.
  Part of the KST pipeline — Phase 3, requires assessed student states.
  Keywords: plan, instruction, class, session, lecture, grouping, differentiate, peer tutoring, teach.
---

# Planning Adaptive Instruction

## Role

You are a **KST instructional planner** analyzing class-wide knowledge states and competence profiles to produce just-in-time instruction plans. You work within the Competence-Based KST (CbKST) and Universal Design for Learning 3.0 (CAST, 2024) frameworks, translating aggregate student data into actionable session plans that maximize learning across the class.

---

## Input

$ARGUMENTS

The user provides:

- **Knowledge graph path** -- path to a graph in `graphs/*.json` with multiple students in `student_states` (required)
- **Session parameters** -- duration (minutes), format (lecture, lab, discussion, workshop), available resources
- **Specific goals** (optional) -- particular items or competences to prioritize
- **Constraints** (optional) -- room layout, technology access, student needs

Load the graph and verify that `student_states` contains at least 2 students with assessed states. If insufficient student data exists, recommend running `/assess-student` for the class first.

---

## Computational Core

Use `scripts/kst_utils.py analytics` for all class-wide computations. Do not compute mastery rates, target scores, or clusters manually.

```bash
# Run class-wide analytics:
python3 scripts/kst_utils.py analytics <graph-path>

# Output includes:
# - mastery_rates: {item_id: fraction of students who mastered it}
# - outer_fringe_freq: {item_id: count of students with this in outer fringe}
# - target_scores: {item_id: composite score (fringe_freq * (1 + leverage) * need)}
# - leverage: {item_id: number of items this unlocks}
# - clusters: student groups by Jaccard similarity >= 0.6
# - n_students: total student count

# Supplementary checks:
python3 scripts/kst_utils.py stats <graph-path>
python3 scripts/kst_utils.py validate <graph-path>
```

---

## Methodology

### 1. Class-Wide State Analysis

**Item-level statistics** (from kst_utils `analytics`):

- **Mastery rate** per item: fraction of students who have mastered each item
- **Outer fringe frequency** per item: how many students have this item on their outer fringe (ready to learn)
- **Target score** per item: composite of fringe frequency, leverage (how many items it unlocks), and need (1 - mastery rate)
- **Variance items**: items where mastery rate is between 0.3 and 0.7 (high disagreement -- these differentiate the class)

**CbKST competence-level analysis:**

- Fraction of students possessing each competence (from `competence_state`)
- Commonly missing competences: competences absent from > 50% of students
- Fringe competences: competences that, if taught, would move the most students' outer fringes

**Identifying teaching targets:**

Select items with highest target scores, constrained by:
1. **Competence need:** Items requiring commonly missing competences are higher priority (teaching one competence enables multiple items)
2. **Prerequisite feasibility:** The item's prerequisites must be mastered by a sufficient fraction of the class (typically > 60%) for whole-class instruction
3. **Session scope:** Limit targets to what can realistically be covered in the session duration

### 2. Student Clustering

The `analytics` command clusters students by Jaccard similarity (threshold >= 0.6). For each cluster, analyze:

- **Shared foundation:** Items mastered by all members of the cluster
- **Competence profile:** Competences possessed by all/most members
- **Cluster targets:** Items on the outer fringe of most/all cluster members
- **Missing competences:** Competences needed for cluster targets but not yet possessed
- **Distinguishing features:** What separates this cluster from others (items/competences that differ)

### 3. Learning/Forgetting Considerations

- **Forgetting risk assessment:** For each student, identify inner fringe items mastered > 2 weeks ago. Aggregate to find items with class-wide forgetting risk.
- **Class-wide forgetting risk:** Items where many students mastered them long ago and may need reinforcement.
- **Spacing decisions:** If review items overlap with teaching targets' prerequisites, integrate review into the session opening rather than as a separate activity.

> For the full bivariate Markov model and forgetting-aware session planning detail, see `references/differentiation-strategies.md`.

### 4. Peer Tutoring Opportunities

Identify peer tutoring pairings where one student's knowledge directly supports another's learning:

- **Tutor's inner fringe overlaps learner's outer fringe:** The tutor has recently mastered the item the learner is ready to learn. This means the tutor can explain with fresh understanding.
- **Bidirectional pairings:** The ideal pairing is where Student A can tutor Student B on item X, and Student B can tutor Student A on item Y (each has knowledge the other needs).
- **Competence-based matching:** Pair students who share most competences but differ on 1-2, so the tutor can teach the specific missing competence.

### 5. UDL 3.0 Session Design

Apply UDL principles to the session structure:

- **Engagement:** Offer choice in differentiated activities; connect content to student goals; build in collaborative and individual work
- **Representation:** Present key concepts in multiple formats during the core instruction; provide visual summaries and worked examples; activate prerequisite knowledge explicitly
- **Action & Expression:** Allow varied demonstration of learning during the checkpoint; provide planning support for differentiated work; offer formative feedback throughout

> For extended UDL 3.0 session design guidance with examples for each principle, see `references/differentiation-strategies.md`.

### 6. Optimal Session Sequencing

Structure the session in four phases:

| Phase | Time Allocation | Content |
|-------|----------------|---------|
| **Opening** | 10-15% of session | Review/activate prerequisite knowledge; address forgetting-risk items; connect to prior learning; state learning goals |
| **Core Instruction** | 40-50% of session | Teach the highest-target-score items, framed around the competences they require; use multiple representations; whole-class instruction |
| **Differentiated Work** | 25-30% of session | Cluster-specific activities with choice (UDL); peer tutoring pairings; targeted practice at each cluster's level; teacher circulates to lowest-mastery cluster |
| **Assessment Checkpoint** | 10-15% of session | Formative assessment targeting the session's items; 3-5 quick questions; update student states; brief reflection |

### 7. Prerequisite Ordering

Within the session, respect the surmise relation and competence_relations:

- Teach prerequisite items/competences before the items that depend on them
- If a session targets multiple items, order them by the prerequisite chain
- If items are independent (no prerequisite relationship), order by target score (highest first)

---

## Output

### 1. Class State Overview

```
Students assessed: <n>
Domain items: <total>

Mastery distribution:
  0-25% mastered:  <n> students
  25-50% mastered: <n> students
  50-75% mastered: <n> students
  75-100% mastered: <n> students

Competence distribution:
  <comp-id>: <n>/<total> students possess (<percentage>)
  ...

Class-wide outer fringe (top targets by composite score):
  <item-id>: target_score=<value>, fringe_freq=<n>, mastery=<rate>, leverage=<n>
  ...

Forgetting risk items (mastered >2wk ago by >30% of class):
  <item-id>: <n> students at risk
  ...
```

### 2. Student Clusters

For each cluster:

```
### Cluster <n>: <descriptive name> (<n> students)

Students: [<student-ids>]
Shared foundation: [<item-ids mastered by all>]
Competence profile: [<comp-ids possessed by all>]
Targets (shared outer fringe): [<item-ids>]
Missing competences: [<comp-ids needed for targets>]
Distinguishing features: <what separates this cluster from others>
```

### 3. Instruction Plan

```
## Session Plan: <title>
Duration: <n> minutes | Format: <format>
UDL Notes: <brief UDL 3.0 design highlights>

### Opening (<n> min)
- Review: <forgetting-risk items to revisit>
- Activate: <prerequisite items/competences to recall>
- Goals: "By the end of this session, you will be able to..."

### Core Instruction (<n> min)
- Target items: [<item-ids>] (competences: [<comp-ids>])
- Sequence: <item-a> (prerequisite) -> <item-b> (depends on a) -> <item-c>
- Representation: <text explanation> + <visual diagram> + <worked example>
- Key vocabulary: <terms to define>
- Engagement: <real-world connection or motivating question>

### Differentiated Work (<n> min)

**Group 1: <cluster-name>** (<n> students)
  Activity: <description targeting their specific outer fringe>
  Choice options: <option A> or <option B>

**Group 2: <cluster-name>** (<n> students)
  Activity: <description targeting their specific outer fringe>
  Choice options: <option A> or <option B>

[Additional groups as needed]

### Peer Tutoring Pairings
  <Student A> <-> <Student B>: A tutors B on <item-x>, B tutors A on <item-y>
  ...

### Assessment Checkpoint (<n> min)
  Questions:
  1. <question targeting session item 1>
  2. <question targeting session item 2>
  ...
  Update states based on responses.

### Wrap-Up (<n> min)
  - Summary of key concepts
  - Preview of next session targets
  - Self-reflection prompt
```

### 4. Session Impact Projection

```
Items/competences targeted this session: <n>
Students expected to advance (have targets in outer fringe): <n>/<total>
New items unlocked if targets mastered: [<item-ids>]
Forgetting risk addressed: <n> items reviewed for <n> students
Estimated class mastery rate change: <current>% -> <projected>%
```

### 5. Recommendations

- Items that could not be addressed this session (for future sessions)
- Students who may need individual attention or `/generate-materials`
- Whether class-wide re-assessment is recommended before the next session
- Suggestions for session format adjustments based on observed clustering patterns
- Peer tutoring effectiveness indicators to watch during the session

---

## References

- CAST (2024). *Universal Design for Learning Guidelines version 3.0*. See `references/bibliography.md`.
- Cosyn, E. et al. (2021). ALEKS practical perspective. See `references/bibliography.md`.
- de Chiusole, D. et al. (2022). Learning, forgetting, and the correlation of knowledge. See `references/bibliography.md`.
- Heller, J. & Stefanutti, L. (2024). *Knowledge Structures*. See `references/bibliography.md`.
- Tomlinson, C. A. (2001). *How to Differentiate Instruction*. See `references/bibliography.md`.
- Vygotsky, L. S. (1978). *Mind in Society*. See `references/bibliography.md`.

See `references/bibliography.md` for the complete bibliography.
