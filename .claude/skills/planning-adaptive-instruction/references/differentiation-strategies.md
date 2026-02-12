# Differentiation Strategies for KST-Based Instruction

This reference provides extended detail on differentiated instruction, ZPD-based peer tutoring, forgetting model application for session planning, UDL 3.0 session design, formative assessment integration, and session format adaptations. The SKILL.md file references this document for detailed strategies and examples.

---

## Tomlinson's Differentiated Instruction Principles

### Core Framework (Tomlinson, 2001)

Differentiated instruction modifies four classroom elements based on student readiness, interest, and learning profile:

1. **Content:** What students learn
2. **Process:** How students make sense of the content
3. **Product:** How students demonstrate learning
4. **Learning environment:** The climate and physical/social arrangements

### Applying Differentiation to KST

KST provides precise data for each differentiation element:

#### Content Differentiation

- **By knowledge state:** Each student cluster has a different set of outer fringe items. Content is naturally differentiated by targeting each cluster's fringe.
- **By competence:** Students missing different competences receive content focused on their specific missing competences.
- **By depth:** Students with extensive prerequisites mastered receive deeper treatment; students with fragile prerequisites receive review-augmented treatment.
- **Practical example:** Cluster A (mastery rate 70%) receives content on advanced items; Cluster B (mastery rate 35%) receives content on foundational items with embedded prerequisite review.

#### Process Differentiation

- **By Bloom's level:** Match the cognitive process to the student's position in the knowledge space. Students at the frontier of their zone benefit from Apply/Analyze activities; students reinforcing knowledge benefit from Remember/Understand activities.
- **By scaffolding level:** Students closer to mastering a target item receive less scaffolded practice; students farther away receive more guided activities.
- **By grouping:** Flexible grouping based on KST clusters -- homogeneous for targeted instruction, heterogeneous for peer tutoring.
- **Practical example:** Cluster A does independent problem-solving with extension challenges; Cluster B does guided practice with worked examples and peer support.

#### Product Differentiation

- **By complexity:** Assessment checkpoint questions calibrated to each cluster's target items.
- **By format:** Students choose how to demonstrate mastery (written, verbal, visual, computational) -- aligned with UDL 3.0 Action & Expression.
- **By criterion:** Advanced students demonstrate Create/Evaluate level mastery; developing students demonstrate Apply/Understand level mastery.

#### Learning Environment Differentiation

- **Physical arrangement:** Clusters work in separate areas; peer tutoring pairs have dedicated space.
- **Social arrangement:** Mix of individual, paired, and small-group work based on the phase of the session.
- **Affective environment:** Normalize that different students are working on different items; frame this as personalized learning, not ability grouping.

---

## Vygotsky's ZPD and Peer Tutoring Theory

### Zone of Proximal Development (Vygotsky, 1978)

The ZPD is defined as the distance between:
- What a learner can do independently (current development level)
- What a learner can do with guidance (potential development level)

### ZPD in KST Terms

| Vygotsky Concept | KST Equivalent |
|-----------------|----------------|
| Current development level | Knowledge state K (mastered items) |
| Zone of Proximal Development | Outer fringe items (items ready to learn with support) |
| Potential development level | K union (outer fringe items) after instruction |
| "More knowledgeable other" | Peer tutor whose inner fringe overlaps the learner's outer fringe |

### Peer Tutoring Mechanisms

Peer tutoring is effective because:

1. **Tutor benefits (learning by teaching):** Explaining strengthens the tutor's own understanding of inner fringe items, reducing forgetting risk.
2. **Learner benefits (ZPD scaffolding):** The peer tutor provides just-in-time, personalized support calibrated to the learner's exact knowledge gap.
3. **Social learning:** Both students engage in collaborative meaning-making.
4. **Efficiency:** Multiple tutoring pairs work simultaneously, multiplying instruction capacity.

### Optimal Peer Tutoring Pair Selection from KST Data

**Algorithm for pair selection:**

1. For each student pair (A, B), compute:
   - Tutor_A_to_B = A's inner fringe intersected with B's outer fringe (items A recently mastered that B is ready to learn)
   - Tutor_B_to_A = B's inner fringe intersected with A's outer fringe

2. Score the pair:
   - Bidirectional score = |Tutor_A_to_B| + |Tutor_B_to_A| (higher is better -- both students benefit)
   - Unidirectional score = max(|Tutor_A_to_B|, |Tutor_B_to_A|) (for one-way tutoring)

3. Use greedy matching to maximize total tutoring benefit across the class (each student appears in at most one pair).

**Constraints:**
- Tutor must have mastered the item with reasonable confidence (assessment confidence > 0.7)
- Items should be mastered recently (inner fringe, not deep in the knowledge state) -- recent mastery means the tutor can articulate the learning process
- Both students should share enough common knowledge to communicate effectively (Jaccard similarity > 0.3)

### Reciprocal Peer Tutoring

The ideal KST scenario: Student A's inner fringe overlaps Student B's outer fringe on item X, while Student B's inner fringe overlaps Student A's outer fringe on item Y. Both students alternate roles, which:

- Distributes status (neither student is permanently "the one who needs help")
- Maximizes learning for both students
- Creates natural collaboration rather than asymmetric dependency

---

## Forgetting Model Application for Session Planning

### Bivariate Markov Model in Session Context

The bivariate Markov model (de Chiusole et al., 2022; Stefanutti et al., 2021) has specific implications for session planning:

#### Pre-Session Forgetting Assessment

Before each session, estimate forgetting risk for each student-item pair:

1. **Time since mastery:** Check `history` timestamps for when each inner fringe item was mastered.
2. **Reinforcement history:** Count how many times the item has been reviewed or used as a prerequisite.
3. **Forgetting probability estimate:** Items mastered once with no reinforcement have higher forgetting probability than items mastered and subsequently used.

**Heuristic forgetting risk categories:**

| Time Since Mastery | Reinforcement Count | Risk Level | Session Action |
|-------------------|-------------------|------------|----------------|
| < 1 week | Any | Low | No review needed |
| 1-2 weeks | >= 2 | Low | Brief mention in opening |
| 1-2 weeks | 0-1 | Medium | Quick recall question in opening |
| 2-4 weeks | >= 3 | Medium | Quick recall question |
| 2-4 weeks | 0-2 | High | Dedicated review activity |
| > 4 weeks | Any | High | Dedicated review + re-assessment recommended |

#### Forgetting Cascade Prevention

When a foundational item is at forgetting risk, all dependent items are also at risk. Session planning should:

1. Identify items at the base of prerequisite chains that are at forgetting risk
2. Prioritize review of these foundational items (they protect the entire chain)
3. Use the review as the opening activity, framing it as "building on what we know"

#### Spaced Practice Integration

During the session, embed spaced practice for at-risk items:
- Use at-risk items as examples or contexts for teaching new material
- Include at-risk items in warm-up questions
- Design differentiated activities that require applying at-risk items

---

## Extended UDL 3.0 Session Design

### Multiple Means of Engagement in Class Sessions

**Opening Phase:**
- State clear, achievable learning goals (e.g., "Today we will master items X and Y")
- Connect to student interests: "Here is why this matters in [context relevant to students]"
- Build anticipation: pose a motivating question that the session will answer

**Core Instruction Phase:**
- Offer choice within the instruction (e.g., "Would the class like to see an example from context A or context B?")
- Build in think-pair-share activities to sustain engagement
- Provide mastery-oriented framing: "You already know [prerequisites]; now we are extending that knowledge"

**Differentiated Phase:**
- Offer activity choice within each cluster (e.g., "Choose to work on problems, create a concept map, or explain to a partner")
- Foster collaboration through structured peer interactions
- Support self-regulation: "Before you begin, plan your approach. After 10 minutes, check your progress."

**Checkpoint Phase:**
- Frame assessment as learning ("Let's see what we've learned today") not judgment
- Provide immediate feedback where possible
- Celebrate collective progress: "As a class, we moved from X% to Y% mastery on these items"

### Multiple Means of Representation in Class Sessions

**Visual representations:**
- Hasse diagram showing where today's target items sit in the prerequisite structure
- Concept maps connecting new material to known material
- Tables comparing/contrasting related concepts

**Verbal representations:**
- Clear, concise explanations with domain-specific vocabulary defined
- Multiple analogies for abstract concepts
- Think-aloud demonstrations of problem-solving procedures

**Active representations:**
- Worked examples with annotated reasoning
- Interactive demonstrations or simulations
- Physical or digital manipulatives for concrete concepts

### Multiple Means of Action & Expression in Class Sessions

**During instruction:**
- Invite students to contribute examples, explanations, or questions
- Use polling or response systems for whole-class engagement
- Allow note-taking in preferred format (written, digital, sketch)

**During differentiated work:**
- Provide multiple ways to practice (problems, projects, explanations, diagrams)
- Offer templates and scaffolds for complex tasks
- Allow pair and individual work options

**During checkpoint:**
- Mix question formats (MC, short answer, diagram, explanation)
- Allow students to demonstrate mastery through their preferred modality
- Provide self-check opportunities before formal checkpoint

---

## Formative Assessment Integration

### Continuous Formative Assessment in KST Sessions

Unlike summative assessment, formative assessment during instruction serves to:
1. Monitor learning in real time
2. Adjust instruction based on observed responses
3. Update student states for planning the next session

### Quick Assessment Techniques

| Technique | Duration | Data Yielded | KST Use |
|-----------|----------|-------------|---------|
| Exit ticket (3-5 questions) | 5-10 min | Item-level mastery | Update student states for session targets |
| Think-pair-share observation | 2-3 min | Qualitative understanding | Identify students needing more scaffolding |
| Polling (MC question) | 1-2 min | Class-wide mastery rate | Decide whether to continue or re-teach |
| Mini-whiteboard | 2-3 min | Individual response | Identify specific errors per student |
| One-sentence summary | 2-3 min | Conceptual understanding | Gauge depth of understanding |

### Updating Student States from Formative Data

After the checkpoint:
1. Score responses per item
2. For each student, update the knowledge state using BLIM (with appropriate careless error and lucky guess parameters for the classroom context -- typically higher careless error due to time pressure)
3. Recompute fringes
4. Save updated states to the graph
5. Use updated states to plan the next session

---

## Session Format Adaptations

### Lecture Format (50-75 min)

- **Opening (10 min):** Warm-up questions on at-risk items; state objectives
- **Core (30-40 min):** Whole-class instruction on highest-target items; multiple representations; embedded engagement (think-pair-share every 10 min)
- **Differentiated (10-15 min):** Brief breakout for cluster-specific practice or peer tutoring
- **Checkpoint (5-10 min):** Exit ticket on session targets
- **Note:** Limited differentiation time; focus core instruction on items with highest class-wide target scores

### Lab/Workshop Format (75-120 min)

- **Opening (10-15 min):** Brief review and goal-setting
- **Core (20-30 min):** Compact instruction on key concepts and procedures
- **Differentiated (40-60 min):** Extended hands-on work by cluster; peer tutoring pairs; teacher circulates with targeted support
- **Checkpoint (10-15 min):** Practical demonstration or problem set
- **Note:** Maximum differentiation opportunity; ideal for procedural and application items

### Discussion Format (50-75 min)

- **Opening (10 min):** Pose a motivating question connected to target items
- **Core (15-20 min):** Structured discussion with scaffolded prompts (grounded in target items)
- **Differentiated (20-30 min):** Small-group discussion on cluster-specific topics; Socratic questioning by teacher
- **Checkpoint (10 min):** Written reflection or summary
- **Note:** Best for Analyze/Evaluate level items; requires students to have relevant prerequisite knowledge

### Workshop/Seminar Format (120+ min)

- **Opening (15 min):** Comprehensive review and connection to prior sessions
- **Core (30-40 min):** In-depth instruction with multiple examples and representations
- **Differentiated (50-60 min):** Extended project-based work by cluster; multiple peer tutoring rotations; individual consultations
- **Checkpoint (15-20 min):** Multi-format assessment (MC + short answer + demonstration)
- **Note:** Allows full cycle of instruction, practice, and assessment; ideal for covering multiple target items

---

## References

- CAST (2024). *Universal Design for Learning Guidelines version 3.0*. Wakefield, MA: CAST.
- de Chiusole, D., Stefanutti, L., Anselmi, P. & Robusto, E. (2022). Learning, forgetting, and the correlation of knowledge in knowledge space theory. *Journal of Mathematical Psychology, 108*.
- Stefanutti, L., de Chiusole, D. & Anselmi, P. (2021). Modeling learning in knowledge space theory through bivariate Markov processes. *Journal of Mathematical Psychology, 101*.
- Tomlinson, C. A. (2001). *How to Differentiate Instruction in Mixed-Ability Classrooms* (2nd ed.). ASCD.
- Vygotsky, L. S. (1978). *Mind in Society: The Development of Higher Psychological Processes*. Harvard University Press.
