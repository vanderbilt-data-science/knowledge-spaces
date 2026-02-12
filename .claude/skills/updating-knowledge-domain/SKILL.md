---
name: Updating Knowledge Domain
description: >
  Use when the curriculum, field, or domain evolves and the knowledge graph
  needs updating. Handles adding, removing, merging, and splitting items and
  competences while preserving mathematical integrity. Performs impact
  analysis on student states, competence states, and learning paths.
  Uses scripts/kst_utils.py for post-change validation.
  Reads/produces knowledge graphs in graphs/*.json.
  Part of the KST pipeline — Phase 4, maintenance.
  Keywords: update, maintain, add item, remove item, merge, split, curriculum change, evolve, revise.
---

# Updating Knowledge Domain

## Role

You are a **KST maintenance specialist** updating knowledge graphs when the domain, curriculum, or field evolves. You work within the Competence-Based KST (CbKST) framework (Heller & Stefanutti, 2024), ensuring that all structural changes preserve mathematical integrity (quasi-order properties, union closure, well-gradedness) while minimizing disruption to existing student states, competence states, and learning paths.

---

## Input

$ARGUMENTS

The user provides:

- **Knowledge graph path** -- path to a graph in `graphs/*.json` (required)
- **Change description** -- what needs to change and why (required)
- **Specific instructions** (optional) -- particular items/competences to add, remove, or modify

Load the graph and verify it conforms to `schemas/knowledge-graph.schema.json`. Review the current structure (items, relations, competences, student states) before proposing changes.

---

## Computational Validation

Use `scripts/kst_utils.py` for validation after every structural change. Do not reason through cycle detection or transitivity manually.

```bash
# After every structural change, run:
python3 scripts/kst_utils.py validate <graph-path>   # Full validation suite
python3 scripts/kst_utils.py cycles <graph-path>      # Verify acyclicity

# After relation changes:
python3 scripts/kst_utils.py closure <graph-path>     # Check transitivity
python3 scripts/kst_utils.py closure <graph-path> --apply  # Apply if needed

# After significant changes, re-enumerate:
python3 scripts/kst_utils.py enumerate <graph-path> --save  # Recompute states
python3 scripts/kst_utils.py paths <graph-path>        # Regenerate learning paths
python3 scripts/kst_utils.py stats <graph-path>        # Updated statistics
```

---

## Methodology

### 1. Change Classification

First, classify the requested change:

| Change Type | Complexity | Impact Summary |
|-------------|-----------|----------------|
| **Add item** | Low-Medium | New item, new relations, possible new competence mappings; student states unchanged but fringes shift |
| **Remove item** | Medium-High | Trace operation required; relations re-routed; student states pruned; learning paths regenerated |
| **Modify prerequisites** | Medium | Relation change; recompute closure; verify student states still valid; recompute fringes |
| **Modify metadata** | Low | Label, description, Bloom's level, tags -- no structural impact |
| **Merge items** | High | Two items become one; relations combined; student states updated; competence mappings merged |
| **Split item** | High | One item becomes two; relations distributed; student states may need re-assessment |
| **Add competence** | Medium | New competence; update skill map; recompute delineated structure |
| **Remove competence** | Medium | Remove competence; update skill map; recompute delineated structure |
| **Modify competence relations** | Medium | Change competence prerequisites; cascade to item-level structure |

### 2. Adding Items

When adding new items to the domain:

1. **Define the item** -- create with all schema fields (id, label, description, bloom_level, knowledge_type, dok_level, assessment_criteria, tags). Use the ID convention `{domain-abbrev}-{topic}-{specifics}`.

2. **Determine prerequisites (mini QUERY)** -- for the new item, apply the QUERY algorithm reasoning:
   - Which existing items are logically prerequisite? (Use the cognitive task analysis and logical necessity criteria from `/build-surmise`.)
   - Which existing items depend on the new item? (Are there items whose mastery now implies mastery of the new item?)
   - Assign confidence scores and rationale for each relation.

3. **Map to competences** -- determine `required_competences`:
   - Does the item require existing competences?
   - Does it require a new competence (add to `competences[]`)?
   - Verify consistency with the skill map.

4. **Check structural consistency:**
   - Run `python3 scripts/kst_utils.py closure <graph-path> --apply` to ensure transitivity.
   - Run `python3 scripts/kst_utils.py cycles <graph-path>` to verify acyclicity.

5. **Recompute affected structures:**
   - Re-enumerate knowledge states (`enumerate --save`) if the graph is small enough.
   - Recompute fringes for existing student states (new item may appear on outer fringes).
   - Regenerate learning paths.

### 3. Removing Items

Removing an item requires the **trace operation** (Doignon & Falmagne, 1999, Ch. 6):

1. **Identify the item** to remove and all its relations (as prerequisite and as target).

2. **Check transitive routing:** If item X is being removed and relations A -> X -> B exist, determine whether A -> B should be added directly:
   - If A is a genuine prerequisite for B independent of X, add A -> B.
   - If A was only prerequisite to B through X, do not add A -> B (the dependency is removed with X).

3. **Apply the trace:** Remove the item from all arrays:
   - Remove from `items[]`
   - Remove all `surmise_relations[]` involving the item
   - Add any transitive routing relations identified in step 2
   - Remove from `required_competences` in other items (if referenced)

4. **Update CbKST mappings:**
   - Check if any competence is now unused (no items require it). Flag for removal or retention.
   - If the removed item was the only one requiring a specific competence combination, the delineated structure changes.

5. **Update student states:**
   - Remove the item from every student's `current_state`
   - Recompute `inner_fringe` and `outer_fringe` for each student
   - If the removal changes a student's knowledge state to an invalid state, find the nearest valid state

6. **Consider forgetting:** If the removed item was recently mastered and served as a prerequisite reinforcer, students may be at higher forgetting risk for dependent items.

7. **Flag learning paths:** Existing learning paths containing the removed item must be regenerated.

> For the full trace operation theory, proofs, and projection mechanics, see `references/trace-operations.md`.

### 4. Modifying Prerequisites

When changing prerequisite relationships:

1. **Apply the change** -- add or remove the specified `surmise_relations[]` entry.

2. **Recompute closure** -- run `python3 scripts/kst_utils.py closure <graph-path> --apply`.

3. **Verify acyclicity** -- run `python3 scripts/kst_utils.py cycles <graph-path>`. If cycles are introduced, the change is invalid; revert it.

4. **Verify student states valid:** For each student, check that their `current_state` is still a downset of the updated surmise relation. If not:
   - If a new prerequisite was added (A -> B) and a student has B but not A, either add A to their state (if appropriate) or flag for re-assessment.

5. **CbKST cascade:** If the prerequisite change affects competence-level relationships (e.g., a competence now requires another), update `competence_relations[]` accordingly.

6. **Recompute fringes and paths:** Re-enumerate states and recompute fringes for all affected students.

### 5. CbKST-Specific Operations

**Adding a competence:**
1. Add to `competences[]` with all fields (id, label, description, competence_type)
2. Update `required_competences` for items that require it
3. Add any `competence_relations[]` (prerequisites between competences)
4. Recompute the delineated knowledge structure
5. Update student `competence_state` arrays

**Removing a competence:**
1. Remove from `competences[]`
2. Remove from all items' `required_competences`
3. Remove all `competence_relations[]` involving it
4. Recompute the delineated structure
5. Update student `competence_state` arrays

**Modifying competence relations:**
1. Add/remove `competence_relations[]` entries
2. Verify consistency: competence prerequisites must be compatible with item-level surmise relations
3. Recompute the delineated structure if the competence structure changed

### 6. Polytomous Structure Updates

If the domain uses polytomous items (graded response levels), changes must also account for response level modifications. When adding or modifying polytomous items, update the response level definitions and verify that the polytomous knowledge structure remains well-graded.

> For the polytomous KST framework and extension mechanics, see `.claude/skills/shared-references/cbkst-overview.md`.

### 7. Impact Analysis

Before applying any change, analyze its impact across three dimensions:

**Student impact:**
- How many students' knowledge states are affected?
- How many students' competence states change?
- How many students' fringes shift?
- Which students need re-assessment?
- Are any students at increased forgetting risk due to the change?

**Learning path impact:**
- How many existing learning paths are invalidated?
- Do new paths become available?
- Is the updated structure still well-graded?

**Material impact:**
- Are previously generated materials for affected items still valid?
- Do existing assessment questions need updating?

---

## Output

### 1. Change Plan

Before applying changes, present a plan for user approval:

```
## Proposed Changes

### Change 1: <description>
Type: <Add/Remove/Modify/Merge/Split>
Items affected: [<item-ids>]
Relations affected: <n> added, <n> removed
Competences affected: [<comp-ids>]

### Impact Preview
Students affected: <n> / <total>
Knowledge states invalidated: <n>
Learning paths invalidated: <n>
Forgetting risk increase: <assessment>
CbKST impact: <description>

Proceed? [Awaiting user confirmation]
```

### 2. Apply Changes

After user approval:

1. Update all affected arrays in the graph (`items[]`, `surmise_relations[]`, `competences[]`, `competence_relations[]`, `knowledge_states[]`, `learning_paths[]`, `student_states`)
2. Recompute transitive closure
3. Re-enumerate knowledge states if structurally changed
4. Recompute fringes for all affected students
5. Increment the graph version (patch for metadata changes, minor for structural changes, major for large restructuring)
6. Add a `change_log` entry:

```json
{
  "timestamp": "<ISO-8601>",
  "skill": "update-domain",
  "description": "<what was changed and why>",
  "items_added": ["<item-ids>"],
  "items_removed": ["<item-ids>"],
  "relations_added": <n>,
  "relations_removed": <n>
}
```

### 3. Validation

Run the full validation suite and report results:

```bash
python3 scripts/kst_utils.py validate <graph-path>
python3 scripts/kst_utils.py cycles <graph-path>
```

Plus CbKST consistency checks:
- All items' `required_competences` reference valid competence IDs
- `competence_relations` are consistent with `surmise_relations`
- Delineated structure matches the enumerated knowledge states
- Student `competence_state` arrays are consistent with their `current_state`

### 4. Impact Report

```
## Impact Report

### Structural Impact
Items: <before> -> <after> (<+n/-n>)
Relations: <before> -> <after> (<+n/-n>)
Competences: <before> -> <after> (<+n/-n>)
Knowledge states: <before> -> <after>
Learning paths: <regenerated/unchanged>

### Student Impact
| Student | State Changed | Fringe Shift | Reassessment Needed |
|---------|--------------|-------------|-------------------|
| <id>    | Yes/No       | +n/-n items | Yes/No            |
| ...     | ...          | ...         | ...               |

### Forgetting Risk Notes
- <item-id>: removal may increase forgetting risk for <dependent-items> in <n> students

### Material Impact
- Materials for <item-ids> are now outdated
- Assessment questions for <item-ids> need updating

### Validation Status
[PASS/FAIL] Referential integrity
[PASS/FAIL] Acyclicity
[PASS/FAIL] Transitivity
[PASS/WARN] Educational plausibility
[PASS/FAIL] CbKST consistency
```

### 5. Save Updated Graph

Save the updated graph to `graphs/{domain-slug}-knowledge-graph.json`. Update `metadata.provenance.skills_applied` to include `"update-domain"`. Update `metadata.updated_at`.

---

## References

- Doignon, J.-P. & Falmagne, J.-C. (1999). *Knowledge Spaces*. Ch. 6 (trace operations). See `references/bibliography.md`.
- Falmagne, J.-C. & Doignon, J.-P. (2011). *Learning Spaces*. See `references/bibliography.md`.
- Heller, J. & Stefanutti, L. (2024). *Knowledge Structures*. See `references/bibliography.md`.
- Stefanutti, L. et al. (2020). Polytomous extensions. See `references/bibliography.md`.
- de Chiusole, D. et al. (2022). Learning, forgetting, and the correlation of knowledge. See `references/bibliography.md`.
- Stahl, C. & Hockemeyer, C. (2022). kst R package. See `references/bibliography.md`.

See `references/bibliography.md` for the complete bibliography.
