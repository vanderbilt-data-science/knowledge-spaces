# Knowledge Space Theory — Skill Suite

This project implements a suite of Claude Code slash commands (skills) that guide an AI agent through the full Knowledge Space Theory (KST) pipeline: from raw course materials to a usable knowledge graph that supports student assessment, adaptive instruction, and curriculum maintenance.

The suite supports both **classical item-based KST** and the newer **Competence-Based KST (CbKST)** framework (Heller & Stefanutti, 2024), which adds a latent skill/competence layer beneath observable items.

## Skill Pipeline

### Phase 1: Domain Analysis
- `/extract-domain` — Extract atomic knowledge items from course materials
- `/decompose-objectives` — Decompose learning objectives into testable items using taxonomic frameworks (Bloom's, DOK, SOLO, Marzano's, Fink's)
- `/map-concepts` — Build a concept map showing relationships between items; identify latent competences (CbKST)

### Phase 2: Knowledge Structure Construction
- `/build-surmise` — Construct the surmise relation (prerequisite quasi-order) via the QUERY algorithm, with CbKST competence relations
- `/construct-space` — Derive the full knowledge space (states, fringes, learning paths)
- `/validate-structure` — Validate mathematical consistency, educational plausibility, and CbKST alignment

### Phase 3: Application
- `/assess-student` — Adaptive assessment of a student's knowledge state (BLIM/PoLIM)
- `/generate-materials` — Generate bespoke learning materials targeting a student's outer fringe (UDL 3.0 aligned)
- `/plan-instruction` — JIT lecture/instruction planning from class-wide state analysis

### Phase 4: Maintenance
- `/update-domain` — Update the knowledge structure when the field or curriculum evolves

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
schemas/                          # JSON Schema for knowledge graph format
scripts/                          # Python computational utilities (kst_utils.py)
references/                       # Consolidated bibliography
graphs/                           # Output directory for knowledge graphs
.claude/commands/                 # Skill files (slash commands)
```

## Theoretical Foundation

This suite is grounded in:
- **Doignon & Falmagne (1999)** *Knowledge Spaces* — classical KST foundations
- **Falmagne & Doignon (2011)** *Learning Spaces* — well-graded spaces and learning paths
- **Heller & Stefanutti (2024)** *Knowledge Structures: Recent Developments* — current state-of-the-art including CbKST, polytomous extensions, and probabilistic models
- **Cosyn et al. (2021)** — practical KST at scale (ALEKS system)

See `references/bibliography.md` for the complete bibliography.
