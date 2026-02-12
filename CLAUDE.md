# Knowledge Space Theory — Skill Suite

This project implements a suite of 10 [Agent Skills](https://agentskills.io) that guide an AI agent through the full Knowledge Space Theory (KST) pipeline: from raw course materials to a usable knowledge graph that supports student assessment, adaptive instruction, and curriculum maintenance.

The skills follow the Agent Skills open standard and work across Claude Code, Codex, Cursor, GitHub Copilot, and other compatible platforms.

The suite supports both **classical item-based KST** and the newer **Competence-Based KST (CbKST)** framework (Heller & Stefanutti, 2024), which adds a latent skill/competence layer beneath observable items.

## Skill Pipeline

### Phase 1: Domain Analysis
- **Extracting Knowledge Items** (`/extracting-knowledge-items`) — Extract atomic knowledge items from course materials
- **Decomposing Learning Objectives** (`/decomposing-learning-objectives`) — Decompose learning objectives into testable items using taxonomic frameworks (Bloom's, DOK, SOLO, Marzano's, Fink's)
- **Mapping Concepts and Competences** (`/mapping-concepts-and-competences`) — Build a concept map showing relationships between items; identify latent competences (CbKST)

### Phase 2: Knowledge Structure Construction
- **Building Surmise Relations** (`/building-surmise-relations`) — Construct the surmise relation (prerequisite quasi-order) via the QUERY algorithm, with CbKST competence relations
- **Constructing Knowledge Space** (`/constructing-knowledge-space`) — Derive the full knowledge space (states, fringes, learning paths)
- **Validating Knowledge Structure** (`/validating-knowledge-structure`) — Validate mathematical consistency, educational plausibility, and CbKST alignment

### Phase 3: Application
- **Assessing Knowledge State** (`/assessing-knowledge-state`) — Adaptive assessment of a student's knowledge state (BLIM/PoLIM)
- **Generating Learning Materials** (`/generating-learning-materials`) — Generate bespoke learning materials targeting a student's outer fringe (UDL 3.0 aligned)
- **Planning Adaptive Instruction** (`/planning-adaptive-instruction`) — JIT lecture/instruction planning from class-wide state analysis

### Phase 4: Maintenance
- **Updating Knowledge Domain** (`/updating-knowledge-domain`) — Update the knowledge structure when the field or curriculum evolves

## Parallelism with Cowork
- Phase 1 skills can run in parallel (they operate on independent source materials)
- Phase 2 skills are sequential (each depends on the previous)
- Phase 3 skills can run in parallel per-student

## Computational Utilities

The `scripts/kst_utils.py` module provides Python functions for KST computations that skills reference for mathematical operations:

```bash
python3 scripts/kst_utils.py validate <graph-path>    # Run validation checks
python3 scripts/kst_utils.py closure <graph-path>      # Compute transitive closure
python3 scripts/kst_utils.py enumerate <graph-path>    # Enumerate knowledge states
python3 scripts/kst_utils.py paths <graph-path>        # Generate learning paths
python3 scripts/kst_utils.py analytics <graph-path>    # Class-wide analytics
python3 scripts/kst_utils.py cycles <graph-path>       # Detect cycles
python3 scripts/kst_utils.py stats <graph-path>        # Print graph statistics
```

Skills should use these utilities for computation rather than reasoning through math manually. The script requires only Python 3.9+ standard library.

## Conventions

- **Schema:** All knowledge graphs conform to `schemas/knowledge-graph.schema.json`
- **Storage:** All knowledge graphs are stored as JSON in `graphs/`
- **Naming:** Graph files are named `{domain-slug}-knowledge-graph.json` (e.g., `intro-statistics-knowledge-graph.json`)
- **Persistence:** Skills always read/write the graph file — never hold state in conversation only
- **References:** Full citations are in `references/bibliography.md`; skills reference this shared bibliography
- **CbKST:** The `competences[]`, `competence_relations[]`, and `required_competences` fields are optional — omit them for purely item-based KST workflows

## Key Directories

```
schemas/                                    # JSON Schema for knowledge graph format
scripts/                                    # Python computational utilities (kst_utils.py)
references/                                 # Consolidated bibliography
graphs/                                     # Output directory for knowledge graphs
.claude/skills/                             # Agent Skills (open standard format)
  ├── shared-references/                    # Shared reference files used across skills
  │   ├── taxonomy-frameworks.md            #   Bloom's, DOK, SOLO, Marzano's, Fink's
  │   ├── cbkst-overview.md                 #   CbKST theory (Heller & Stefanutti, 2024)
  │   ├── kst-foundations.md                #   Core KST definitions and axioms
  │   └── ecd-framework.md                  #   Evidence-Centered Design framework
  └── <skill-name>/                         # Each skill in its own directory
      ├── SKILL.md                          #   YAML frontmatter + instructions
      └── references/                       #   Optional per-skill reference files
```

## Theoretical Foundation

This suite is grounded in:
- **Doignon & Falmagne (1999)** *Knowledge Spaces* — classical KST foundations
- **Falmagne & Doignon (2011)** *Learning Spaces* — well-graded spaces and learning paths
- **Heller & Stefanutti (2024)** *Knowledge Structures: Recent Developments* — current state-of-the-art including CbKST, polytomous extensions, and probabilistic models
- **Cosyn et al. (2021)** — practical KST at scale (ALEKS system)

See `references/bibliography.md` for the complete bibliography.
