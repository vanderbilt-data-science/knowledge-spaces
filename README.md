<div align="center">

# Knowledge Spaces

### AI-Powered Knowledge Space Theory for Adaptive Education

**Build mathematically rigorous knowledge graphs from any course materials.<br>Assess students adaptively. Generate personalized instruction. Plan smarter lectures.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org)

[Quick Start](#quick-start) · [Skills Reference](#skills-reference) · [How It Works](#how-it-works) · [Using the Skills](#using-the-skills) · [Schema](#knowledge-graph-schema) · [Bibliography](#bibliography)

</div>

---

## What Is This?

**Knowledge Spaces** is a suite of 10 AI-powered skills (slash commands) that implement the full [Knowledge Space Theory](https://en.wikipedia.org/wiki/Knowledge_space) (KST) pipeline. Give it your course materials — a syllabus, textbook, standards document — and it will:

1. **Extract** atomic knowledge items from your materials
2. **Discover** prerequisite relationships between items
3. **Construct** the mathematical knowledge space (all feasible learning states)
4. **Assess** individual students adaptively (like [ALEKS](https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf))
5. **Generate** personalized learning materials targeting what each student is ready to learn
6. **Plan** class-wide instruction using data from every student's knowledge state

The output is a **knowledge graph** — a structured JSON file that captures everything: items, prerequisites, competences, learning paths, and student states. It's the mathematical backbone for adaptive education.

### Who Is This For?

- **Instructors** who want to understand prerequisite structure and plan differentiated instruction
- **Instructional designers** building adaptive courses or assessments
- **EdTech developers** who need a principled knowledge model (not ad hoc tagging)
- **Researchers** in Knowledge Space Theory, educational data mining, or learning analytics
- **Anyone using Claude Code** who wants to explore KST with real course materials

### What Makes This Different?

Unlike keyword tagging or simple topic trees, this suite is grounded in **50+ years of mathematical learning theory**:

- **Knowledge Space Theory** (Doignon & Falmagne, 1999) — the mathematical framework behind ALEKS, used by millions of students
- **Competence-Based KST** (Heller & Stefanutti, 2024) — the current state-of-the-art, adding a latent skill layer that explains *why* prerequisites exist
- **Formal Concept Analysis** — rigorous lattice-theoretic methods for discovering concept hierarchies
- **Evidence-Centered Design** — principled assessment architecture (Mislevy et al., 2003)

Every skill embeds its theoretical grounding and academic references inline. Using the skills teaches you the theory.

---

## Quick Start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.9+ (for the computational utilities — standard library only, no pip installs needed)

### Installation

```bash
# Clone the repository
git clone https://github.com/vanderbilt-data-science/knowledge-spaces.git
cd knowledge-spaces

# That's it. No dependencies to install.
# The skills are Claude Code slash commands in .claude/commands/
# The Python utilities use only the standard library.
```

### Your First Knowledge Graph

```bash
# Start Claude Code in the project directory
claude

# Step 1: Extract knowledge items from your course materials
> /extract-domain path/to/your/syllabus.pdf

# Step 2: Build the concept map and discover prerequisites
> /map-concepts graphs/your-domain-knowledge-graph.json

# Step 3: Construct the formal prerequisite relation
> /build-surmise graphs/your-domain-knowledge-graph.json

# Step 4: Derive the full knowledge space
> /construct-space graphs/your-domain-knowledge-graph.json

# Step 5: Validate everything
> /validate-structure graphs/your-domain-knowledge-graph.json
```

You now have a mathematically validated knowledge space. Use it to assess students, generate materials, or plan instruction.

---

## The Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 1: Domain Analysis                        │
│                                                                     │
│  /extract-domain ──→ /decompose-objectives ──→ /map-concepts        │
│  Course materials    Learning objectives       Concept map &        │
│  → knowledge items   → atomic items            competences          │
│                      (Bloom's, DOK, SOLO,                           │
│                       Fink's, ECD)                                  │
├─────────────────────────────────────────────────────────────────────┤
│                PHASE 2: Structure Construction                      │
│                                                                     │
│  /build-surmise ──→ /construct-space ──→ /validate-structure        │
│  QUERY algorithm     Enumerate states,   Mathematical &             │
│  → prerequisites     fringes, paths      educational checks         │
├─────────────────────────────────────────────────────────────────────┤
│                    PHASE 3: Application                             │
│                                                                     │
│  /assess-student    /generate-materials    /plan-instruction        │
│  Adaptive BLIM      Personalized content   Class-wide JIT           │
│  assessment          for outer fringe      lecture planning          │
├─────────────────────────────────────────────────────────────────────┤
│                    PHASE 4: Maintenance                             │
│                                                                     │
│  /update-domain                                                     │
│  Evolve the structure when curriculum changes                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Skills Reference

### Phase 1: Domain Analysis

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `/extract-domain` | Extract atomic knowledge items from course materials | Syllabus, textbook, standards | `items[]` with Bloom's, DOK, competences |
| `/decompose-objectives` | Decompose learning objectives into testable items | Learning objectives | Refined `items[]` with 5-framework classification |
| `/map-concepts` | Build concept map, identify competences (CbKST) | Knowledge graph + materials | `competences[]`, preliminary prerequisites, Mermaid diagrams |

### Phase 2: Structure Construction

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `/build-surmise` | Construct the prerequisite relation (QUERY algorithm) | Knowledge graph with items | `surmise_relations[]`, `competence_relations[]` |
| `/construct-space` | Derive all feasible knowledge states | Knowledge graph with relations | `knowledge_states[]`, `learning_paths[]`, Hasse diagram |
| `/validate-structure` | Validate mathematical and educational properties | Complete knowledge graph | Validation report (PASS/WARN/FAIL) |

### Phase 3: Application

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `/assess-student` | Adaptive assessment using BLIM/PoLIM | Knowledge graph + student ID | Student knowledge state, fringes, competence state |
| `/generate-materials` | Generate personalized learning materials | Knowledge graph + student state | Explanations, examples, problems (UDL 3.0) |
| `/plan-instruction` | JIT lecture planning from class data | Knowledge graph + all students | Session plan with groupings, targets, peer tutoring |

### Phase 4: Maintenance

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `/update-domain` | Update structure for curriculum changes | Knowledge graph + change description | Updated graph + impact analysis |

---

## How It Works

### The Core Idea

A **knowledge space** is the set of all feasible knowledge states for a domain. Not every combination of items is feasible — if you know calculus, you must also know algebra. The prerequisite relationships (the *surmise relation*) constrain which combinations are possible.

```
Student who knows {algebra, geometry, trig}     ← feasible state
Student who knows {calculus, but not algebra}    ← NOT feasible (violates prerequisites)
```

### Key Concepts

**Knowledge Items (Q):** The atomic units of knowledge in a domain. Each is testable with a single assessment question. The skills extract these from your course materials and classify them using Bloom's Revised Taxonomy, Webb's Depth of Knowledge, SOLO Taxonomy, and Fink's Taxonomy of Significant Learning.

**Surmise Relation:** The prerequisite quasi-order. If item A is a prerequisite for item B, then any student who has mastered B must also have mastered A. This is built using the QUERY algorithm (Koppen & Doignon, 1990), with Claude acting as the domain expert.

**Knowledge States:** Feasible subsets of items — sets that are downward-closed under the surmise relation. The family of all such states forms the knowledge space.

**Fringes:** For any knowledge state:
- The **inner fringe** is the set of most-recently mastered items (remove any one and the state is still feasible)
- The **outer fringe** is the set of items the student is ready to learn next (add any one and the state is still feasible)

Fringes are remarkably compact — ALEKS research shows a state with 80 items typically has only ~9 fringe items.

**Competences (CbKST):** Latent skills that explain *why* items cluster together. A student might struggle with 5 different items not because they're missing 5 things, but because they're missing one underlying competence. The Competence-Based KST framework (Heller & Stefanutti, 2024) adds this explanatory layer.

### The Assessment Model

The `/assess-student` skill implements an ALEKS-style adaptive assessment:

1. Start with uniform probability over all feasible states
2. Ask a question about the item that maximally discriminates between states (~50/50 split)
3. Update probabilities using the Basic Local Independence Model (BLIM) with lucky-guess and careless-error parameters
4. Repeat until entropy drops below threshold (~20-30 questions for moderate domains)

This is orders of magnitude more efficient than testing every item individually.

---

## Using the Skills

### In Claude Code (CLI)

The skills are standard [Claude Code custom slash commands](https://docs.anthropic.com/en/docs/claude-code/tutorials/custom-slash-commands). Clone this repo and work from within it:

```bash
cd knowledge-spaces
claude

# Use any skill with /skill-name and pass arguments
> /extract-domain path/to/syllabus.pdf
> /build-surmise graphs/my-course-knowledge-graph.json
> /assess-student graphs/my-course-knowledge-graph.json student-alice
```

**To use the skills in a different project**, copy the `.claude/commands/` directory, the `scripts/` directory, and the `schemas/` directory into your project:

```bash
# From your project directory
cp -r path/to/knowledge-spaces/.claude/commands/ .claude/commands/
cp -r path/to/knowledge-spaces/scripts/ scripts/
cp -r path/to/knowledge-spaces/schemas/ schemas/
mkdir -p graphs
```

### In Claude Code (VS Code / JetBrains)

The skills work identically in Claude Code's IDE integrations. Open the project in your IDE, open the Claude Code panel, and type `/extract-domain` (or any skill name) to invoke it.

### With Claude Cowork (Multi-Agent)

The pipeline has natural parallelism that [Cowork](https://docs.anthropic.com/en/docs/claude-code/cowork) can exploit:

**Phase 1 — Parallel domain analysis:**
```
You can run /extract-domain, /decompose-objectives, and /map-concepts in parallel
if they operate on different source materials. They all contribute to the same
knowledge graph and will be merged.
```

**Phase 2 — Sequential (each step depends on the previous):**
```
/build-surmise → /construct-space → /validate-structure
These must run in order.
```

**Phase 3 — Parallel per student:**
```
Run /assess-student for multiple students simultaneously.
Run /generate-materials for multiple students simultaneously.
Each operates on its own student state independently.
```

**Example Cowork session:**
```
Start 3 agents:
  Agent 1: /extract-domain syllabus.pdf
  Agent 2: /decompose-objectives objectives.md
  Agent 3: /extract-domain textbook-ch1.pdf

When all complete, merge results and run:
  Agent 4: /map-concepts graphs/combined-knowledge-graph.json
  → /build-surmise → /construct-space → /validate-structure

Then fan out for assessment:
  Agent 5: /assess-student graphs/course-kg.json student-alice
  Agent 6: /assess-student graphs/course-kg.json student-bob
  Agent 7: /assess-student graphs/course-kg.json student-carol

Finally, plan instruction:
  Agent 8: /plan-instruction graphs/course-kg.json
```

### On Other Platforms (Claude.ai, API, etc.)

The skill files are self-contained markdown prompts. You can use them on any platform that supports Claude:

1. **Copy the skill text** from any `.claude/commands/*.md` file
2. **Paste it as a system prompt** or prepend it to your message
3. **Replace `$ARGUMENTS`** with your actual input
4. **Include `scripts/kst_utils.py`** in the conversation if the skill references it (for computational validation)

The skills are designed so that an agent with no prior context can execute them — all theoretical grounding, methodology, and output format specifications are embedded in each skill file.

### With the Claude API (Programmatic)

```python
import anthropic

client = anthropic.Anthropic()

# Read the skill prompt
with open(".claude/commands/extract-domain.md") as f:
    skill_prompt = f.read()

# Replace $ARGUMENTS with your input
skill_prompt = skill_prompt.replace("$ARGUMENTS", "Analyze the attached syllabus...")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=8096,
    messages=[{"role": "user", "content": skill_prompt}]
)
```

---

## Knowledge Graph Schema

All skills produce and consume a shared JSON format defined in [`schemas/knowledge-graph.schema.json`](schemas/knowledge-graph.schema.json).

```
KnowledgeGraph
├── metadata                    # Domain name, version, provenance, change log
├── items[]                     # The knowledge domain Q
│   ├── id, label, description
│   ├── bloom_level             # remember/understand/apply/analyze/evaluate/create
│   ├── knowledge_type          # factual/conceptual/procedural/metacognitive
│   ├── dok_level               # Webb's Depth of Knowledge (1-4)
│   ├── solo_level              # SOLO taxonomy level
│   ├── required_competences[]  # CbKST: which competences this item needs
│   ├── source_objectives[]     # Original learning objectives
│   ├── assessment_criteria     # How to test mastery
│   └── tags[]
├── surmise_relations[]         # Prerequisite pairs with confidence & rationale
├── competences[]               # CbKST: latent skills (optional)
├── competence_relations[]      # CbKST: competence prerequisites (optional)
├── knowledge_states[]          # All feasible states with fringes (optional)
├── learning_paths[]            # Named sequences through the space
└── student_states{}            # Per-student tracking
    └── [student-id]
        ├── current_state       # Mastered items
        ├── competence_state    # CbKST: possessed competences
        ├── inner_fringe        # Most advanced mastered items
        ├── outer_fringe        # Ready to learn next
        ├── history[]           # State transitions over time
        └── assessment_log[]    # Assessment interactions
```

The CbKST fields (`competences`, `competence_relations`, `required_competences`, `competence_state`) are optional — omit them for a purely item-based workflow.

---

## Computational Utilities

The `scripts/kst_utils.py` module provides Python functions for KST math that skills call during execution. It requires only Python 3.9+ standard library — no pip installs.

```bash
python3 scripts/kst_utils.py validate <graph.json>     # Validate structure
python3 scripts/kst_utils.py closure <graph.json>       # Transitive closure
python3 scripts/kst_utils.py enumerate <graph.json>     # Enumerate knowledge states
python3 scripts/kst_utils.py paths <graph.json>         # Generate learning paths
python3 scripts/kst_utils.py analytics <graph.json>     # Class-wide analytics
python3 scripts/kst_utils.py cycles <graph.json>        # Detect cycles
python3 scripts/kst_utils.py stats <graph.json>         # Print summary statistics
```

---

## Project Structure

```
knowledge-spaces/
├── README.md
├── LICENSE                              # MIT License
├── CLAUDE.md                            # Project context for Claude agents
├── .claude/commands/                    # The 10 skill files
│   ├── extract-domain.md               # Phase 1: Extract items
│   ├── decompose-objectives.md         # Phase 1: Decompose objectives
│   ├── map-concepts.md                 # Phase 1: Concept map & competences
│   ├── build-surmise.md               # Phase 2: QUERY algorithm
│   ├── construct-space.md             # Phase 2: Knowledge space
│   ├── validate-structure.md          # Phase 2: Validation
│   ├── assess-student.md             # Phase 3: Adaptive assessment
│   ├── generate-materials.md         # Phase 3: Learning materials
│   ├── plan-instruction.md           # Phase 3: Lecture planning
│   └── update-domain.md              # Phase 4: Maintenance
├── schemas/
│   └── knowledge-graph.schema.json    # JSON Schema for the graph format
├── scripts/
│   └── kst_utils.py                   # Python computational utilities
├── references/
│   └── bibliography.md                # Consolidated academic bibliography (60+ refs)
└── graphs/                            # Output directory for knowledge graphs
```

---

## Theoretical Foundations

This suite implements methods from a mature body of mathematical learning theory spanning 40+ years:

| Area | Key References | Used In |
|------|---------------|---------|
| Knowledge Space Theory | Doignon & Falmagne (1999), Falmagne & Doignon (2011) | All skills |
| Competence-Based KST | Heller & Stefanutti (2024), Stefanutti & de Chiusole (2017) | All skills (CbKST layer) |
| QUERY Algorithm | Koppen & Doignon (1990), Cosyn et al. (2021) | `/build-surmise` |
| BLIM / PoLIM Assessment | Falmagne et al. (2006), Stefanutti et al. (2020) | `/assess-student` |
| Formal Concept Analysis | Ganter & Wille (1999), Huang et al. (2025) | `/map-concepts`, `/build-surmise` |
| Bloom's Revised Taxonomy | Anderson & Krathwohl (2001) | `/extract-domain`, `/decompose-objectives` |
| Webb's Depth of Knowledge | Webb (1997), Hess et al. (2009) | `/extract-domain`, `/decompose-objectives` |
| Evidence-Centered Design | Mislevy et al. (2003) | `/assess-student`, `/decompose-objectives` |
| Universal Design for Learning | CAST (2024) UDL 3.0 | `/generate-materials`, `/plan-instruction` |
| Learning & Forgetting | de Chiusole et al. (2022) | `/plan-instruction`, `/update-domain` |

The complete bibliography with 60+ references is in [`references/bibliography.md`](references/bibliography.md).

---

## Example Workflow

Here's what a complete workflow looks like for an Introductory Statistics course:

```bash
# Start Claude Code
claude

# 1. Feed in the syllabus
> /extract-domain Here is my Intro Stats syllabus: [paste or provide path]
# → Creates graphs/intro-statistics-knowledge-graph.json with ~30-50 items

# 2. Refine with explicit learning objectives
> /decompose-objectives graphs/intro-statistics-knowledge-graph.json
#   "Students will be able to: 1) Calculate descriptive statistics..."
# → Adds/refines items with Bloom's, DOK, SOLO classification

# 3. Build the concept map and identify competences
> /map-concepts graphs/intro-statistics-knowledge-graph.json
# → Adds competences[], concept relationships, Mermaid diagrams

# 4. Construct the formal prerequisite structure
> /build-surmise graphs/intro-statistics-knowledge-graph.json
# → Adds surmise_relations[] with confidence scores and rationales

# 5. Derive the knowledge space
> /construct-space graphs/intro-statistics-knowledge-graph.json
# → Adds knowledge_states[], learning_paths[], Hasse diagram

# 6. Validate everything
> /validate-structure graphs/intro-statistics-knowledge-graph.json
# → Reports PASS/WARN/FAIL for mathematical and educational checks

# 7. Assess a student
> /assess-student graphs/intro-statistics-knowledge-graph.json student-alice
# → Adaptive quiz → determines Alice's knowledge state and outer fringe

# 8. Generate personalized materials for Alice
> /generate-materials graphs/intro-statistics-knowledge-graph.json student-alice
# → Custom explanations, examples, practice problems for her outer fringe

# 9. Plan next lecture using all student states
> /plan-instruction graphs/intro-statistics-knowledge-graph.json
# → Session plan: review targets, groupings, peer tutoring pairings
```

---

## Contributing

Contributions are welcome! Some areas where help is especially valuable:

- **New skills** for specialized workflows (e.g., exam generation, curriculum alignment)
- **Empirical validation** — testing the pipeline against real student data
- **Integration with LMS** platforms (Canvas, Moodle, Blackboard)
- **Additional computational utilities** (e.g., IITA implementation, concept lattice computation)
- **Translations** of skill prompts for non-English instruction

Please open an issue to discuss your idea before submitting a PR.

---

## Citation

If you use this in academic work:

```bibtex
@software{knowledge_spaces_2025,
  title={Knowledge Spaces: AI-Powered Knowledge Space Theory for Adaptive Education},
  author={{Vanderbilt Data Science Institute}},
  year={2025},
  url={https://github.com/vanderbilt-data-science/knowledge-spaces},
  note={A suite of Claude Code skills implementing the full KST pipeline}
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built at the [Vanderbilt Data Science Institute](https://www.vanderbilt.edu/datascience/)

</div>
