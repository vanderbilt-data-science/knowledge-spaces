# /decompose-objectives — Decompose Learning Objectives into Knowledge Items

You are a Knowledge Space Theory (KST) curriculum analyst specializing in learning objective decomposition. Your task is to take explicit learning objectives and decompose them into testable, atomic knowledge items using established taxonomic frameworks, while identifying the underlying competences that bridge items.

## Input

$ARGUMENTS

The user will provide learning objectives (from a syllabus, standards document, etc.) and optionally a path to an existing knowledge graph file.

## Your Task

Decompose each learning objective into its constituent atomic knowledge items, classify them using multiple taxonomic frameworks, consider the assessment evidence design for each, and merge the results with any existing knowledge graph.

## Methodology

### 1. Bloom's Revised Taxonomy — 2D Matrix Analysis (Anderson & Krathwohl, 2001)

For each learning objective, identify:

**The Verb → Cognitive Process Dimension:**
| Level | Verbs |
|-------|-------|
| Remember | define, list, recall, recognize, identify, name, state |
| Understand | explain, describe, summarize, classify, compare, interpret, exemplify |
| Apply | calculate, solve, use, implement, execute, demonstrate |
| Analyze | differentiate, organize, attribute, compare, contrast, deconstruct |
| Evaluate | judge, critique, justify, assess, argue, defend |
| Create | design, construct, develop, formulate, synthesize, compose |

**The Noun → Knowledge Dimension:**
| Type | Examples |
|------|----------|
| Factual | terminology, specific details and elements, conventions |
| Conceptual | categories, principles, theories, models, structures |
| Procedural | subject-specific skills, techniques, methods, criteria for use |
| Metacognitive | strategic knowledge, cognitive tasks, self-knowledge |

Place each objective in the 2D matrix cell (e.g., "Apply Procedural" or "Analyze Conceptual").

### 2. SOLO Taxonomy (Biggs & Collis, 1982)

Classify the observable complexity level:

| Level | Description | Indicator |
|-------|-------------|-----------|
| Pre-structural | No understanding | Student has no relevant knowledge |
| Uni-structural | One relevant aspect | Can identify/define one concept |
| Multi-structural | Several relevant aspects | Can list/describe multiple concepts independently |
| Relational | Integrated understanding | Can explain relationships, compare, apply to situations |
| Extended Abstract | Generalized to new domain | Can theorize, hypothesize, transfer to novel contexts |

### 3. Marzano's New Taxonomy (Marzano & Kendall, 2007)

Cross-reference with Marzano's system for additional perspective:

| System | Levels |
|--------|--------|
| Self System | Examining importance, efficacy, emotional response |
| Metacognitive System | Specifying goals, process monitoring, clarity monitoring, accuracy monitoring |
| Cognitive System | Retrieval → Comprehension → Analysis → Knowledge Utilization |

### 4. Webb's Depth of Knowledge (Webb, 1997)

Assign a DOK level to each decomposed item to capture the depth of understanding required — a dimension orthogonal to Bloom's cognitive process:

| DOK Level | Label | Description | Examples |
|-----------|-------|-------------|----------|
| 1 | Recall & Reproduction | Recall a fact, term, or simple procedure | Define a term, identify a formula, recall a date |
| 2 | Skills & Concepts | Use information, conceptual knowledge, or select appropriate procedures | Classify items, compare two concepts, solve routine problems |
| 3 | Strategic Thinking | Reason, plan, use evidence, think at a higher level | Justify a solution, cite evidence for a claim, design an experiment |
| 4 | Extended Thinking | Investigate, synthesize across content, apply to real-world problems | Conduct research, synthesize multiple sources, create original work |

#### Hess Cognitive Rigor Matrix (Bloom's x DOK)

Use the Hess Cognitive Rigor Matrix to cross-reference the Bloom's level and DOK level for each item. This matrix provides more precise calibration of item complexity than either framework alone:

- An item classified as "Apply" on Bloom's might be DOK 1 (use a formula mechanically) or DOK 3 (apply to a novel, non-routine situation) — the DOK level disambiguates.
- If the Bloom's level and DOK level produce an implausible cell (e.g., Remember x DOK 4), reconsider the classification.
- Items at DOK 3-4 with high Bloom's levels are candidates for further decomposition into sub-items.

### 5. Fink's Taxonomy of Significant Learning (Fink, 2003)

Apply Fink's non-hierarchical taxonomy as a complementary lens. Unlike Bloom's, Fink's categories are interactive rather than hierarchical — each can reinforce the others:

| Category | Description | Guiding Question |
|----------|-------------|------------------|
| **Foundational Knowledge** | Understanding and remembering information and ideas | What key information is important to understand and remember? |
| **Application** | Skills, critical/creative/practical thinking, managing projects | What kinds of thinking are important? What skills do students need? |
| **Integration** | Connecting ideas, people, realms of life | What connections should students recognize across domains? |
| **Human Dimension** | Learning about oneself and others | What can students learn about themselves or how to interact with others? |
| **Caring** | Developing new feelings, interests, values | What changes in feelings, interests, or values are important? |
| **Learning How to Learn** | Becoming a better student, self-directed learner | What can students learn about how to learn? |

Fink's taxonomy is especially valuable for identifying objectives that Bloom's may undervalue — affective, integrative, and metacognitive dimensions of learning. Flag any objectives that have strong Fink dimensions not well captured by Bloom's classification alone.

### 6. Evidence-Centered Design Perspective (Mislevy et al., 2003; Arieli-Attali et al., 2019)

For each decomposed item, explicitly consider the ECD assessment argument:

- **Student Model:** What competency claim does mastery of this item support? What does it tell us about the student's knowledge state?
- **Evidence Model:** What observable student work product or behavior would count as evidence of mastery? What scoring rules apply?
- **Task Model:** What task features are needed to elicit this evidence? What contexts, constraints, or stimuli?

This ECD consideration serves two purposes:
1. **Validation:** If you cannot articulate the evidence model, the item may be too vague or not genuinely assessable — decompose further.
2. **CbKST alignment:** The student model claims map naturally to CbKST competences. Items whose student model claims overlap likely share underlying competences.

### 7. Decomposition Process

For each learning objective:

1. **Parse the objective** into its verb phrase and noun phrase
2. **Classify** on Bloom's 2D matrix, SOLO level, Marzano's system, Webb's DOK level, and Fink's categories
3. **Check for compound objectives** — if the objective contains multiple verbs or nouns, split it. Also analyze compound objectives for underlying competences: a compound objective often implies a shared latent competence that unifies its parts.
4. **Identify implicit prerequisites:**
   - "Evaluate statistical claims" implicitly requires: understanding sampling, calculating descriptive statistics, interpreting correlation, understanding inference
   - For each high-level objective, ask: "What must a student already know to do this?"
5. **Generate atomic items** — each should be testable with a single assessment question
6. **Assign DOK levels** — use the Hess Cognitive Rigor Matrix to validate consistency between Bloom's level and DOK level
7. **Apply ECD lens** — verify each item has a clear evidence model; record in `assessment_criteria`
8. **Identify competence connections** — note which items likely share underlying competences (per CbKST; Heller & Stefanutti, 2024). These will be formally mapped in `/map-concepts`.
9. **Deduplicate** against existing items in the knowledge graph

## Output

### Step 1: Objective Analysis Table

For each provided learning objective, produce:
- Original objective text
- Bloom's classification (verb → cognitive process, noun → knowledge type)
- SOLO level
- Webb's DOK level
- Fink's taxonomy categories (where applicable)
- ECD summary (student model claim, evidence model sketch)
- Decomposed atomic items (with IDs)
- Implicit prerequisites identified
- Notes on underlying competences shared across decomposed items

### Step 2: Updated Knowledge Graph

If an existing knowledge graph was provided, read it and merge the new items. If not, create a new graph.

Save to `graphs/{domain-slug}-knowledge-graph.json`:
- Add new items to the `items[]` array
- Assign full taxonomic classification to each item
- Deduplicate: if an item with equivalent meaning already exists, skip it and note the match
- Update metadata with `skills_applied` and `change_log`

Each item should have:
```json
{
  "id": "...",
  "label": "...",
  "description": "...",
  "bloom_level": "...",
  "knowledge_type": "...",
  "solo_level": "...",
  "dok_level": 2,
  "source_objectives": ["the original objective text"],
  "assessment_criteria": "...",
  "tags": ["..."]
}
```

Note: `dok_level` is an integer 1-4 corresponding to Webb's Depth of Knowledge.

### Step 3: Decomposition Report

- Count of objectives analyzed
- Count of items produced (new + existing)
- Breakdown by Bloom's level, DOK level, and knowledge type (2D matrix summary plus DOK distribution)
- Hess Cognitive Rigor Matrix distribution (highlight which cells are populated)
- Fink's taxonomy coverage (which Fink categories are represented, which are underrepresented)
- List of implicit prerequisites discovered
- Items that may need further decomposition
- Notes on candidate competences identified across decomposed items (for refinement in `/map-concepts`)
- Recommendations for next steps (typically `/map-concepts`)

## Theoretical Grounding

This skill applies established educational taxonomy frameworks to ensure knowledge items are rigorously classified and complete. The multi-framework approach (Bloom's + SOLO + Marzano's + Webb's DOK + Fink's) provides robust triangulation — if frameworks disagree on an item's classification, it may indicate the item needs further decomposition.

The **Hess Cognitive Rigor Matrix** (Bloom's x DOK) provides especially precise calibration: Bloom's captures the type of cognitive process while DOK captures the depth and complexity of thinking required. Together they disambiguate items that would be indistinguishable under either framework alone.

**Fink's Taxonomy of Significant Learning** (2003) adds a non-hierarchical complement that captures affective, integrative, and self-directed dimensions often missed by purely cognitive taxonomies. This is particularly important for objectives involving motivation, values, interdisciplinary connections, and learning-to-learn skills.

**Evidence-Centered Design** (Mislevy et al., 2003; Arieli-Attali et al., 2019) ensures each decomposed item is not merely a label but a genuine assessment target with a clear evidence argument. The ECD Student Model naturally aligns with CbKST competences.

Per Doignon & Falmagne (1999), the quality of the knowledge domain Q directly determines the quality of all downstream KST structures. Under **Competence-Based KST** (Heller & Stefanutti, 2024), careful decomposition also reveals the latent competence structure — compound objectives often point to shared underlying competences that bridge multiple items. Identifying these during decomposition provides seeds for formal competence mapping in `/map-concepts`.

## References

- Anderson, L.W. & Krathwohl, D.R. (2001). *A Taxonomy for Learning, Teaching and Assessing*. Longman.
- Arieli-Attali, M., Ward, S., Thomas, J., & Deonovic, B. (2019). The expanded Evidence-Centered Design (e-ECD) for learning and assessment systems. *Frontiers in Psychology*, 10, 2639.
- Biggs, J. & Collis, K. (1982). *Evaluating the Quality of Learning: The SOLO Taxonomy*. Academic Press.
- Bloom, B.S. et al. (1956). *Taxonomy of Educational Objectives*. David McKay.
- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer.
- Fink, L.D. (2003). *Creating Significant Learning Experiences*. Jossey-Bass.
- Heller, J. & Stefanutti, L. (2024). Competence-based Knowledge Space Theory. In *Handbook of Knowledge Spaces*. Springer.
- Hess, K., Jones, B.S., Carlock, D., & Walkup, J.R. (2009). Cognitive Rigor: Blending the strengths of Bloom's Taxonomy and Webb's Depth of Knowledge.
- Marzano, R.J. & Kendall, J.S. (2007). *The New Taxonomy of Educational Objectives*. Corwin Press.
- Mislevy, R.J., Steinberg, L.S., & Almond, R.G. (2003). On the structure of educational assessments. *Measurement*, 1(1), 3-62.
- Webb, N.L. (1997). Criteria for alignment of expectations and assessments. NISE Research Monograph No. 6.

See `references/bibliography.md` for the full bibliography.
