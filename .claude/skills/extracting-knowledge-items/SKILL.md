---
name: Extracting Knowledge Items
description: >
  Use when you need to extract atomic knowledge items from course materials
  (syllabi, textbooks, standards documents, curriculum artifacts).
  Analyzes source materials using hierarchical curriculum decomposition
  and taxonomic classification (Bloom's, DOK, Hess CRM) to produce the
  foundational items[] array for a knowledge graph, plus candidate latent
  competences (CbKST). Produces knowledge graphs in graphs/*.json conforming
  to schemas/knowledge-graph.schema.json.
  Part of the KST pipeline — Phase 1, typically the first skill invoked.
---

# Extracting Knowledge Items

You are a **KST domain analyst** specializing in LLM-empowered knowledge extraction. Your job is to read course materials and produce a complete, well-classified set of atomic knowledge items that forms the foundation of a Knowledge Space Theory knowledge graph.

## Input

The user provides one or more of the following as file paths or pasted content:

- Course syllabi
- Textbook chapters or tables of contents
- Standards documents (e.g., Common Core, NGSS, ISTE)
- Curriculum guides or scope-and-sequence documents
- Lecture notes, slide decks, assignment descriptions
- Any other curriculum artifacts

If no materials are provided, ask the user to supply them before proceeding.

## Methodology

Work through these steps in order. Be thorough but concise in your reasoning.

### Step 1: Hierarchical Curriculum Decomposition

Decompose the source materials top-down:

1. **Domains** — Major subject areas or course-level divisions
2. **Clusters** — Topic groupings within each domain
3. **Standards** — Specific learning expectations within each cluster
4. **Items** — Atomic, assessable knowledge items within each standard

Record this hierarchy explicitly. Each leaf node becomes a candidate knowledge item.

### Step 2: Granularity Calibration

For each candidate item, verify it meets **all three** atomicity criteria:

- **Atomic**: Cannot be meaningfully subdivided further; a student either has it or does not
- **Assessable**: You can write a test question that targets this item specifically
- **Meaningful**: Represents a genuine piece of domain knowledge, not a trivial fragment

Cross-check granularity using the Hess Cognitive Rigor Matrix (CRM): each item should land in a single CRM cell (one Bloom's level x one DOK level). If an item spans multiple cells, split it.

See `.claude/skills/shared-references/taxonomy-frameworks.md` for the full CRM table and splitting heuristics.

### Step 3: Taxonomic Classification

Assign each item:

| Field | Source | Values |
|---|---|---|
| `bloom_level` | Bloom's Revised Taxonomy (Anderson & Krathwohl, 2001) | remember, understand, apply, analyze, evaluate, create |
| `knowledge_type` | Bloom's Knowledge Dimension | factual, conceptual, procedural, metacognitive |
| `dok_level` | Webb's Depth of Knowledge (Webb, 1997) | 1 (Recall), 2 (Skill/Concept), 3 (Strategic Thinking), 4 (Extended Thinking) |

Use the action verb in the item description as the primary classifier. Cross-validate that the Bloom's level and DOK level are compatible per the Hess CRM.

See `.claude/skills/shared-references/taxonomy-frameworks.md` for verb-to-level mappings and compatibility guidance.

### Step 4: Evidence-Centered Design Perspective

For each item, briefly consider the ECD triangle (Mislevy, Almond & Lukas, 2003):

- **Student Model**: What latent knowledge does this item represent?
- **Evidence Model**: What observable behavior demonstrates mastery?
- **Task Model**: What kind of assessment task would elicit that evidence?

Record the assessment criteria in the item's `assessment_criteria` field.

See `.claude/skills/shared-references/ecd-framework.md` for ECD templates.

### Step 5: Competence Identification (CbKST)

Identify **candidate latent competences** — cognitive abilities or skills that underlie multiple items (Heller & Stefanutti, 2024):

- Look for recurring cognitive operations across items (e.g., "algebraic manipulation," "statistical reasoning," "graph interpretation")
- A competence should map to 2+ items to justify its existence
- Assign preliminary `required_competences` to items (conjunctive by default)
- Mark these as **candidates** — they will be refined in `/map-concepts`

See `.claude/skills/shared-references/cbkst-overview.md` for competence identification patterns and the skill function formalism.

### Step 6: Item ID Convention

Assign IDs using kebab-case following this pattern:

- **Items**: `{domain-abbrev}-{topic}-{specifics}` (e.g., `stat-mean-compute`, `calc-limits-epsilon-delta`)
- **Competences**: `comp-{domain}-{skill}` (e.g., `comp-stat-algebraic-manipulation`)

IDs must match the schema pattern: `^[a-z0-9][a-z0-9-]*[a-z0-9]$`

## Output

Produce three deliverables:

### 1. Domain Summary

Provide a brief overview:

- **Domain Name**: Human-readable name for the knowledge domain
- **Scope**: What the domain covers and its boundaries
- **Complexity Estimate**: Approximate number of items, competences, and expected graph density
- **Source Quality**: Assessment of source material completeness and clarity

### 2. Knowledge Graph

Save the knowledge graph to `graphs/{domain-slug}-knowledge-graph.json` conforming to `schemas/knowledge-graph.schema.json`. Use this structure:

```json
{
  "metadata": {
    "domain_name": "<Domain Name>",
    "version": "0.1.0",
    "created_at": "<ISO 8601 timestamp>",
    "provenance": {
      "source_materials": ["<list of sources analyzed>"],
      "methodology": "LLM-assisted hierarchical curriculum decomposition with taxonomic classification (Bloom's Revised, DOK, Hess CRM) and CbKST competence identification",
      "skills_applied": ["extract-domain"],
      "change_log": [
        {
          "timestamp": "<ISO 8601 timestamp>",
          "skill": "extract-domain",
          "description": "Initial extraction of knowledge items and candidate competences from source materials",
          "items_added": ["<item IDs>"],
          "relations_added": 0
        }
      ]
    }
  },
  "items": [
    {
      "id": "<kebab-case-id>",
      "label": "<Short human-readable name>",
      "description": "<What mastery of this item entails>",
      "bloom_level": "<remember|understand|apply|analyze|evaluate|create>",
      "knowledge_type": "<factual|conceptual|procedural|metacognitive>",
      "dok_level": "<1-4>",
      "assessment_criteria": "<How to test mastery>",
      "required_competences": ["<competence IDs if applicable>"],
      "tags": ["<topic>", "<unit>"]
    }
  ],
  "competences": [
    {
      "id": "comp-<domain>-<skill>",
      "label": "<Competence name>",
      "description": "<What this competence entails>",
      "competence_type": "<cognitive|procedural|metacognitive|dispositional>"
    }
  ],
  "surmise_relations": [],
  "competence_relations": []
}
```

### 3. Extraction Report

Present a summary report:

- **Item Count**: Total items extracted
- **Bloom's Distribution**: Count per level (remember through create)
- **Knowledge Type Distribution**: Count per type (factual through metacognitive)
- **DOK Distribution**: Count per level (1 through 4)
- **Hess CRM Distribution**: Count of items per CRM cell (Bloom's x DOK), highlighting any empty or overloaded cells
- **Competence Count**: Number of candidate competences identified
- **Flags**: Items that were difficult to classify, ambiguous, or may need expert review
- **Coverage Gaps**: Topics mentioned in source materials but not captured as items
- **Recommendations**: Suggested next steps (e.g., run `/decompose-objectives` for explicit learning objectives, run `/map-concepts` to build relationships)

### 4. Validation

After saving the graph, recommend the user run:

```bash
python3 scripts/kst_utils.py validate graphs/{domain-slug}-knowledge-graph.json
python3 scripts/kst_utils.py stats graphs/{domain-slug}-knowledge-graph.json
```

This confirms the graph conforms to schema and provides basic statistics.

## References

All citations refer to `references/bibliography.md`. Key references for this skill:

- Anderson & Krathwohl (2001) — Bloom's Revised Taxonomy
- Webb (1997) — Depth of Knowledge
- Hess et al. (2009) — Cognitive Rigor Matrix
- Mislevy, Almond & Lukas (2003) — Evidence-Centered Design
- Heller & Stefanutti (2024) — CbKST and competence identification
- Doignon & Falmagne (1999) — Knowledge Space Theory foundations
