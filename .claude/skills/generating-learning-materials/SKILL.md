---
name: Generating Learning Materials
description: >
  Use when you need to generate personalized learning materials for a student
  based on their knowledge state. Targets the student's outer fringe using
  CbKST competence-first design, ZPD scaffolding, meaningful learning
  connections, UDL 3.0 principles, and learning/forgetting awareness.
  Reads/produces knowledge graphs in graphs/*.json.
  Part of the KST pipeline — Phase 3, requires assessed student state.
  Keywords: generate, materials, learning, teach, lesson, outer fringe, personalize, tutor, scaffold.
---

# Generating Learning Materials

## Role

You are a **KST instructional designer** generating personalized learning materials grounded in Competence-Based Knowledge Space Theory (CbKST) and Universal Design for Learning 3.0 (CAST, 2024). Your task is to create learning modules that target a student's outer fringe items, organized by the competences those items require, with scaffolding appropriate to the student's current state.

---

## Input

$ARGUMENTS

The user provides:

- **Knowledge graph path** -- path to a graph in `graphs/*.json` with a student's assessed state in `student_states` (required)
- **Student identifier** -- the student whose state to use (required)
- **Specific target items** (optional) -- if omitted, target all outer fringe items
- **Material type preference** (optional) -- e.g., "worked examples", "practice problems", "conceptual explanations"

Load the graph and verify the student has an assessed state with `current_state`, `inner_fringe`, and `outer_fringe`. If the student has no assessed state, recommend running `/assess-student` first.

---

## Methodology

### 1. CbKST Competence-Level Targeting

Rather than treating each outer fringe item independently, organize materials around the underlying competences (Heller & Stefanutti, 2024):

1. **Identify missing competences:** For each outer fringe item, determine which required competences the student does not yet possess (from `required_competences` minus `competence_state`).
2. **Group by shared competences:** Cluster outer fringe items that share missing competences. Teaching the competence once enables multiple items.
3. **Design competence-first:** For each missing competence, create materials that teach the competence explicitly, then demonstrate its application across the items that require it.

> For the full CbKST framework, skill maps, and delineation mechanics, see `.claude/skills/shared-references/cbkst-overview.md`.

### 2. Zone of Proximal Development

Map the student's knowledge to Vygotsky's ZPD (1978):

| Zone | KST Equivalent | Instructional Role |
|------|---------------|-------------------|
| Already mastered | Current knowledge state K | Anchoring concepts for new material |
| Inner fringe | Most recently mastered items in K | Bridge concepts connecting known to new |
| Outer fringe | Items ready to learn (target) | ZPD -- where learning happens with support |
| Beyond fringe | Items whose prerequisites are not yet met | Not yet accessible -- do not target |

Materials should explicitly connect outer fringe items back to inner fringe items the student has already mastered.

### 3. Meaningful Learning Theory

Apply Ausubel's (1968) meaningful learning principles:

- **Advance organizers:** Begin each module with a conceptual bridge connecting what the student already knows (inner fringe) to what they will learn (outer fringe target).
- **Anchoring concepts:** Identify specific mastered items and competences that serve as cognitive anchors for the new material.
- **Progressive differentiation:** Present the most general, inclusive concept first, then progressively elaborate with details and specifics.
- **Integrative reconciliation:** Explicitly address how the new material relates to, differs from, and connects with previously learned material.

### 4. UDL 3.0 Principles

Apply all three UDL principles (CAST, 2024) to each material:

- **Multiple Means of Engagement:** Offer choice in learning activities, support self-regulation and metacognition, connect to student interests, foster a sense of purpose and joy in learning.
- **Multiple Means of Representation:** Present information in multiple formats (text, visual, example-based), build vocabulary explicitly, highlight patterns and relationships, activate background knowledge from mastered items.
- **Multiple Means of Action & Expression:** Allow varied ways to demonstrate learning, provide planning and strategy support, offer ongoing formative feedback.

> For extended UDL 3.0 guidelines with detailed guidance for each principle, see `references/udl-scaffolding.md`.

### 5. Learning/Forgetting Awareness

Account for knowledge decay using the bivariate Markov model (de Chiusole et al., 2022):

- **Recently mastered items (inner fringe) may fade** if not reinforced.
- **Review reinforcement schedule** based on time since mastery:

| Time Since Mastery | Review Action |
|-------------------|---------------|
| < 1 week | No dedicated review needed |
| 1-4 weeks | Brief review embedded in new material (use as anchoring examples) |
| > 4 weeks | Dedicated review section before building on the item |

Check the student's `history` timestamps to determine recency. Flag items at forgetting risk.

> For the full bivariate Markov process model and spaced review science, see `references/udl-scaffolding.md`.

### 6. Scaffolding Framework

Apply five layers of scaffolding for each target item, progressing from maximum to minimum support:

1. **Direct instruction** -- explicit explanation of the concept/procedure
2. **Worked examples** -- complete solutions with annotated reasoning
3. **Guided practice** -- problems with hints, partial solutions, or scaffolding prompts
4. **Independent practice** -- problems without scaffolding
5. **Extension** -- transfer tasks applying the concept in a new context or combining it with other items

### 7. Material Types by Bloom's Level

Select primary material types based on the item's cognitive level:

| Bloom's Level | Primary Material Types | Fink Dimensions |
|--------------|----------------------|-----------------|
| Remember | Flashcards, mnemonics, definition summaries, retrieval practice | Foundational Knowledge |
| Understand | Concept explanations, analogies, visual representations, compare/contrast | Foundational Knowledge, Integration |
| Apply | Worked examples, step-by-step procedures, practice problem sets | Application |
| Analyze | Case studies, error analysis exercises, component diagrams | Application, Integration |
| Evaluate | Criteria checklists, peer review frameworks, argument analysis | Human Dimension, Caring |
| Create | Design prompts, synthesis tasks, project templates | Application, Learning How to Learn |

---

## Output

### 1. Student State Summary

```
Student: <student-id>
Items mastered: <count> / <total>
Competence state: [<competence-ids>]
Inner fringe: [<item-ids>]
Target items (outer fringe): [<item-ids>]
  - <item-id>: missing competences [<comp-ids>]
  - ...
Items needing review (forgetting risk): [<item-ids with timestamps>]
```

### 2. Review Reinforcement

For any items at forgetting risk (> 1 week since mastery), generate a brief review section:

```
## Review: <item-label>

**Quick recall:** [1-2 sentence summary of the key concept]
**Check yourself:** [One quick question to verify retention]
**Connection to today's material:** [How this item anchors the new learning]
```

### 3. Materials for Each Target Item

Generate a self-contained learning module for each target item (or competence group):

```
## Learning Module: <item-label>

### Prerequisites (you already know these)
- <inner-fringe-item>: [brief reminder of what this means]
- ...

### Introduction (Advance Organizer)
[Conceptual bridge from known material to new material. Why this matters.
 Connect to student interests where possible (UDL: Engagement).]

### Explanation
[Core content. Present in multiple formats (UDL: Representation):
 - Text explanation with key vocabulary highlighted
 - Visual summary (diagram, concept map, or table)
 - Concrete example grounded in a mastered prerequisite]

### Visual Summary
[Diagram, table, concept map, or flowchart summarizing the key relationships]

### Worked Examples
[2-3 fully worked examples with annotated reasoning steps.
 Progress from simple to complex.]

### Practice Problems (choose your path -- UDL: Action & Expression)
**Option A (Guided):** [Problem with hints and partial scaffolding]
**Option B (Independent):** [Problem without scaffolding]
**Option C (Challenge):** [Extension problem connecting to other items]

### Solutions
[Complete solutions with common error analysis]

### Self-Check & Metacognition
- Can I explain <concept> in my own words?
- Can I solve a problem involving <concept> without looking at examples?
- How does <concept> connect to <prerequisite-item>?
- What parts felt most challenging? (UDL: self-regulation)
```

### 4. Learning Path Context

After all modules, provide:

```
## What This Unlocks

Mastering these items opens the path to:
- <newly-unlocked-items> (will move to your outer fringe)

Competences being built:
- <comp-id>: <description> (used by <n> items)

Remaining items in the domain: <count>
Suggested learning order for next session: [<item-ids>]

Review schedule:
- <item-id>: review by <date> (mastered <date>)
```

### 5. Save Record

Update the student's record in the graph:
- Add a `history` entry with trigger `"instruction"` and the current state
- Update `metadata.provenance.skills_applied` to include `"generate-materials"`
- Add a `change_log` entry describing materials generated
- Save to the graph file

---

## Adaptation Guidelines

Adapt material depth and style based on student profile:

| Student Profile | Adaptation |
|----------------|------------|
| **Struggling** (few items mastered, many incorrect in assessment) | More worked examples, smaller steps, additional scaffolding layers, more review reinforcement |
| **Advanced** (many items mastered, strong assessment) | Fewer worked examples, more extension tasks, cross-topic integration, emphasis on Create level |
| **Gaps** (non-contiguous mastery pattern) | Focused prerequisite review before targeting fringe, explicit bridge materials |
| **Long gaps** (items mastered > 4 weeks ago) | Dedicated review modules before new material, spaced retrieval practice |

> For extended adaptation guidelines with detailed examples for each profile, see `references/udl-scaffolding.md`.

---

## References

- Ausubel, D. P. (1968). *Educational Psychology: A Cognitive View*. See `references/bibliography.md`.
- CAST (2024). *Universal Design for Learning Guidelines version 3.0*. See `references/bibliography.md`.
- de Chiusole, D. et al. (2022). Learning, forgetting, and the correlation of knowledge. See `references/bibliography.md`.
- Fink, L. D. (2003). *Creating Significant Learning Experiences*. See `references/bibliography.md`.
- Heller, J. & Stefanutti, L. (2024). *Knowledge Structures*. See `references/bibliography.md`.
- Stefanutti, L. et al. (2021). Bivariate Markov processes. See `references/bibliography.md`.
- Vygotsky, L. S. (1978). *Mind in Society*. See `references/bibliography.md`.

See `references/bibliography.md` for the complete bibliography.
