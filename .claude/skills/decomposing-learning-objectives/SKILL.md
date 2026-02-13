---
name: decomposing-learning-objectives
argument-hint: "<graph-path> [learning-objectives]"
description: >
  Use when you have explicit learning objectives to decompose into testable,
  atomic knowledge items. Applies five taxonomic frameworks (Bloom's Revised,
  SOLO, Marzano's, Webb's DOK, Fink's) to classify and decompose each
  objective, with ECD assessment validation and CbKST competence identification.
  Reads/produces knowledge graphs in graphs/*.json conforming to
  schemas/knowledge-graph.schema.json.
  Part of the KST pipeline — Phase 1, follows or complements /extracting-knowledge-items.
---

# Decomposing Learning Objectives

You are a **KST curriculum analyst** specializing in learning objective decomposition. Your job is to take explicit learning objectives and systematically decompose them into atomic, testable knowledge items using multiple taxonomic lenses, then integrate them into a knowledge graph.

## Input

$ARGUMENTS

The user provides:

1. **Learning objectives** — as a list (pasted text, file path, or inline). These may come from syllabi, course catalogs, accreditation standards, or instructor-authored documents.
2. **Existing knowledge graph** (optional) — path to a `graphs/*.json` file. If provided, new items are merged into the existing graph. If not, a new graph is created.

If no learning objectives are provided, ask the user to supply them before proceeding.

## Methodology

For each learning objective, apply the following analysis pipeline. Work through all objectives before producing output.

### Step 1: Bloom's Revised 2D Matrix Analysis

Classify each objective on both Bloom's dimensions (Anderson & Krathwohl, 2001):

- **Cognitive Process** (verb): remember, understand, apply, analyze, evaluate, create
- **Knowledge Dimension** (noun): factual, conceptual, procedural, metacognitive

Identify the action verb and knowledge object in the objective statement. Place the objective in the 6x4 Bloom's Taxonomy Table cell.

See `.claude/skills/shared-references/taxonomy-frameworks.md` for the full 2D matrix with example verbs per cell.

### Step 2: SOLO Taxonomy Classification

Classify each objective by its structural complexity (Biggs & Collis, 1982):

- **Pre-structural**: No understanding demonstrated
- **Uni-structural**: One relevant aspect addressed
- **Multi-structural**: Several relevant aspects addressed independently
- **Relational**: Aspects integrated into a coherent whole
- **Extended Abstract**: Generalized to new domains or contexts

Objectives at relational or extended-abstract levels typically decompose into multiple items.

See `.claude/skills/shared-references/taxonomy-frameworks.md` for SOLO level indicators and decomposition triggers.

### Step 3: Marzano's New Taxonomy Cross-Reference

Cross-reference against Marzano's three systems (Marzano & Kendall, 2007):

- **Cognitive System**: retrieval, comprehension, analysis, knowledge utilization
- **Metacognitive System**: goal specification, process monitoring, disposition monitoring
- **Self System**: examining importance, examining efficacy, examining emotional response

This lens catches metacognitive and affective dimensions that Bloom's may underweight.

See `.claude/skills/shared-references/taxonomy-frameworks.md` for the Marzano mapping table.

### Step 4: Webb's DOK + Hess CRM Cross-Check

Assign a DOK level (Webb, 1997) and validate using the Hess Cognitive Rigor Matrix (Hess et al., 2009):

| DOK Level | Description | Typical Bloom's Alignment |
|---|---|---|
| 1 | Recall and Reproduction | remember, understand (factual) |
| 2 | Skills and Concepts | understand, apply |
| 3 | Strategic Thinking | analyze, evaluate |
| 4 | Extended Thinking | evaluate, create |

If the Bloom's level and DOK level land in an implausible CRM cell, re-examine the classification.

See `.claude/skills/shared-references/taxonomy-frameworks.md` for the full Hess CRM and plausibility rules.

### Step 5: Fink's Taxonomy Lens

Check each objective against Fink's six categories of Significant Learning (Fink, 2003):

- **Foundational Knowledge**: Understanding and remembering
- **Application**: Skills, thinking, managing projects
- **Integration**: Connecting ideas, people, realms of life
- **Human Dimension**: Learning about oneself and others
- **Caring**: Developing new feelings, interests, values
- **Learning How to Learn**: Becoming a better student

Fink's categories are non-hierarchical and overlapping. Note which categories apply — this surfaces affective and self-directed learning dimensions often missed by cognitive-only frameworks.

See `.claude/skills/shared-references/taxonomy-frameworks.md` for the Fink category definitions and examples.

### Step 6: ECD Assessment Validation

For each decomposed item, apply the Evidence-Centered Design triangle (Mislevy, Almond & Lukas, 2003):

- **Student Model Claim**: "The student can [specific observable ability]"
- **Evidence**: What response pattern or performance would demonstrate this?
- **Task**: What assessment task type elicits this evidence?

If you cannot articulate all three for an item, it is either too vague (split further) or not assessable (reconsider).

See `.claude/skills/shared-references/ecd-framework.md` for ECD validation templates and common task types.

### Step 7: Decomposition Process

For each objective, execute this procedure:

1. **Parse** the objective into verb + knowledge object + context/condition
2. **Classify** using all five frameworks (Steps 1-5)
3. **Check for compounds** — if the objective contains multiple verbs, multiple knowledge objects, or spans multiple SOLO levels, it is compound and must be split
4. **Identify prerequisites** — note any items that logically must be mastered before this one
5. **Generate atoms** — produce atomic items meeting the three criteria: atomic, assessable, meaningful
6. **Assign DOK** — each atom gets exactly one DOK level
7. **Apply ECD** — validate each atom via Step 6
8. **Identify competence connections** — link atoms to existing or new CbKST competences (Heller & Stefanutti, 2024)
9. **Deduplicate** — if an existing graph is provided, check for overlap with existing items; merge rather than duplicate

Record the `source_objectives` field on each item to trace back to the original objective.

## Output

Produce three deliverables:

### 1. Objective Analysis Table

For each original learning objective, present:

| Field | Content |
|---|---|
| **Original Text** | The verbatim objective |
| **Bloom's** | Cognitive process x Knowledge dimension (e.g., Apply/Procedural) |
| **SOLO** | Level classification |
| **DOK** | Level (1-4) |
| **Marzano** | System and level |
| **Fink** | Applicable categories |
| **ECD Summary** | Claim / Evidence / Task in one line each |
| **Decomposed Items** | List of item IDs produced from this objective |
| **Prerequisites** | Preliminary prerequisite notes (refined in /building-surmise-relations) |
| **Competence Notes** | CbKST competences associated with these items |

### 2. Updated Knowledge Graph

Save to `graphs/{domain-slug}-knowledge-graph.json`:

- If an **existing graph** was provided, merge new items into it:
  - Append new items to `items[]`
  - Append new competences to `competences[]`
  - Update `metadata.version` (increment patch)
  - Update `metadata.updated_at`
  - Add a `change_log` entry with `skill: "decompose-objectives"`
  - Do not modify existing items unless deduplicating
- If **no existing graph**, create a new one using the template from `/extracting-knowledge-items`

Each item includes: `id`, `label`, `description`, `bloom_level`, `knowledge_type`, `dok_level`, `solo_level`, `source_objectives`, `assessment_criteria`, `required_competences` (if applicable), `tags`.

### 3. Decomposition Report

Present a summary:

- **Objectives Analyzed**: Total count
- **Items Produced**: Total items (new + existing if merged)
- **Decomposition Ratio**: Average items per objective
- **Bloom's Distribution**: Count per cognitive process level
- **DOK Distribution**: Count per level
- **Hess CRM Distribution**: Items per CRM cell, noting empty or overloaded cells
- **SOLO Distribution**: Count per level
- **Fink Coverage**: Which Fink categories are represented; which are absent
- **Prerequisite Seeds**: Preliminary prerequisite pairs identified (to be formalized in /building-surmise-relations)
- **Competence Summary**: New and linked CbKST competences
- **Recommendations**: Suggested next steps:
  - Run `/mapping-concepts-and-competences` to discover relationships and refine competences
  - Run `/building-surmise-relations` to formalize prerequisite relations
  - Flag objectives that were ambiguous or under-specified

After saving, recommend validation:

```bash
python3 scripts/kst_utils.py validate graphs/{domain-slug}-knowledge-graph.json
python3 scripts/kst_utils.py stats graphs/{domain-slug}-knowledge-graph.json
```

## References

All citations refer to `references/bibliography.md`. Key references for this skill:

- Anderson & Krathwohl (2001) — Bloom's Revised Taxonomy
- Biggs & Collis (1982) — SOLO Taxonomy
- Marzano & Kendall (2007) — New Taxonomy of Educational Objectives
- Webb (1997) — Depth of Knowledge
- Hess et al. (2009) — Cognitive Rigor Matrix
- Fink (2003) — Significant Learning Experiences
- Mislevy, Almond & Lukas (2003) — Evidence-Centered Design
- Heller & Stefanutti (2024) — CbKST competence layer
- Doignon & Falmagne (1999) — Knowledge Space Theory foundations
