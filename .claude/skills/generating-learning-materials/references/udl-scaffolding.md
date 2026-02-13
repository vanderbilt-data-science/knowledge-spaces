# UDL 3.0, Scaffolding, and Learning/Forgetting Models

This reference provides extended detail on Universal Design for Learning 3.0, the bivariate Markov learning/forgetting model, Fink's Significant Learning dimensions, adaptation guidelines, and material customization by knowledge type. The SKILL.md file references this document for extended guidelines and examples.

---

## Universal Design for Learning 3.0 (CAST, 2024)

UDL 3.0 is organized around three principles, each with guidelines and checkpoints. When generating learning materials for KST outer fringe items, apply these guidelines to ensure materials are accessible, engaging, and effective for diverse learners.

### Principle 1: Multiple Means of Engagement

**Purpose:** Tap into learners' interests, challenge them appropriately, and motivate them to learn.

**Guidelines for KST materials:**

1. **Recruiting interest:**
   - Connect outer fringe items to real-world applications the student cares about
   - Offer choice in learning activities (e.g., "Choose Option A, B, or C for practice")
   - Minimize threats and distractions -- frame assessment as learning, not judgment
   - Vary the types of activities across modules to sustain novelty

2. **Sustaining effort and persistence:**
   - Make learning goals explicit: "After this module, you will be able to [item description]"
   - Vary demands and resources to maintain optimal challenge (calibrated to ZPD)
   - Foster collaboration and community where applicable (e.g., peer discussion prompts)
   - Provide mastery-oriented feedback: "You've mastered [n] items; [m] more are within reach"

3. **Self-regulation:**
   - Include metacognitive prompts: "What strategy are you using? Is it working?"
   - Provide self-assessment checklists at the end of each module
   - Help students set personal learning goals within the knowledge space
   - Celebrate progress through the learning path (items mastered, fringes crossed)

4. **Joy and purpose:**
   - Connect learning to the student's sense of purpose and identity
   - Design activities that invite creativity and exploration beyond the minimum requirements
   - Acknowledge the effort of learning, not just correctness

### Principle 2: Multiple Means of Representation

**Purpose:** Present information in ways that are perceptible, comprehensible, and meaningful.

**Guidelines for KST materials:**

1. **Perception:**
   - Offer alternatives for auditory and visual information (text + diagrams + examples)
   - Use clear formatting: headings, bullet points, white space
   - Provide key vocabulary definitions inline

2. **Language and symbols:**
   - Define domain-specific vocabulary explicitly at first use
   - Use multiple representations for mathematical notation (symbolic + verbal + visual)
   - Support decoding by showing how to read and interpret domain notation

3. **Comprehension:**
   - Activate background knowledge by explicitly referencing mastered prerequisite items
   - Highlight patterns, critical features, and big ideas
   - Guide information processing with advance organizers and summaries
   - Use progressive differentiation: general concept first, then elaboration
   - Maximize transfer by showing the same concept applied in multiple contexts

### Principle 3: Multiple Means of Action & Expression

**Purpose:** Allow learners to demonstrate their learning in diverse ways.

**Guidelines for KST materials:**

1. **Physical action:**
   - Provide multiple response formats: written, verbal, diagrammatic, computational
   - Offer alternatives to timed performance when assessing mastery

2. **Expression and communication:**
   - Allow students to demonstrate understanding through explanation, example generation, or problem solving
   - Provide templates and scaffolds for complex responses (e.g., proof templates, analysis frameworks)
   - Use graduated levels of support: worked example -> guided practice -> independent

3. **Executive functions:**
   - Provide planning support: "Here is the sequence of learning modules and estimated time"
   - Embed progress monitoring: "You are on module 3 of 5"
   - Facilitate self-monitoring: "Check your work against these criteria before moving on"
   - Support reflection: "What was the key insight from this module?"

---

## Learning/Forgetting: Bivariate Markov Process

### Model Overview (de Chiusole et al., 2022; Stefanutti et al., 2021)

The bivariate Markov model captures two simultaneous processes affecting a student's knowledge state:

1. **Learning:** The student transitions from a less advanced state to a more advanced one (adding items to their knowledge state).
2. **Forgetting:** The student transitions from a more advanced state to a less advanced one (losing items from their knowledge state).

### Formal Structure

At each time step t, the student's knowledge state K(t) is an element of the knowledge space K. The transition probability from state K_i to state K_j depends on:

- **Learning rate l_{ij}:** P(K(t+1) = K_j | K(t) = K_i) when K_i is a subset of K_j (learning)
- **Forgetting rate f_{ij}:** P(K(t+1) = K_j | K(t) = K_i) when K_j is a subset of K_i (forgetting)

**Key constraints:**
- Learning transitions only occur along the lattice of knowledge states (respecting the surmise relation)
- Forgetting transitions similarly respect the lattice structure -- students lose items from the inner fringe
- The probability of remaining in the same state at any time step is non-zero

### Correlation of Knowledge

De Chiusole et al. (2022) showed that learning and forgetting rates are not independent:
- Items learned in quick succession tend to be forgotten together (correlated forgetting)
- Items mastered over a long period with reinforcement are more resistant to forgetting
- The correlation structure depends on the prerequisite relationships between items

### Implications for Material Generation

1. **Review reinforcement timing:** Items mastered longer ago have higher forgetting probability. Check `history` timestamps.
2. **Prerequisite chain fragility:** If a student forgets a foundational item, all dependent items become invalid. Prioritize review of foundational items.
3. **Spaced practice:** Interleave review of at-risk items with new material, rather than treating them separately.
4. **State consistency:** After extended gaps, re-assess to verify the student's state before generating new materials.

### Spaced Review Science

The optimal review schedule depends on the desired retention interval (Ebbinghaus, 1885; Pimsleur, 1967; Cepeda et al., 2006):

| Review Number | Interval After Previous Review | Rationale |
|---------------|-------------------------------|-----------|
| 1st review | 1 day | Consolidation during sleep |
| 2nd review | 3 days | Beginning of forgetting curve decline |
| 3rd review | 1 week | Extending retention before major decay |
| 4th review | 2 weeks | Building long-term durability |
| 5th review | 1 month | Transition to long-term memory |
| Maintenance | 2-3 months | Periodic refresh |

In KST terms: embed brief recall prompts for inner fringe items using this schedule, integrated into materials for outer fringe items.

---

## Fink's Significant Learning Dimensions

### Detailed Application Guidance

Fink's taxonomy (2003) identifies six dimensions of significant learning that are interactive and synergistic. For KST materials, map each dimension to instructional strategies:

#### 1. Foundational Knowledge (Understanding and Remembering)

- **Application:** Core definitions, facts, principles, and frameworks
- **Material types:** Concept summaries, vocabulary lists, retrieval practice, flashcards
- **KST alignment:** Targets Remember and Understand Bloom's levels
- **Example:** For an item "Define the central limit theorem," provide a clear definition, key conditions, visual illustration, and retrieval practice questions

#### 2. Application (Skills, Critical/Creative/Practical Thinking)

- **Application:** Using knowledge to solve problems, make decisions, manage projects
- **Material types:** Worked examples, procedure guides, practice problem sets, case studies
- **KST alignment:** Targets Apply and Analyze Bloom's levels
- **Example:** For an item "Apply the t-test to compare two sample means," provide step-by-step procedure, worked example with real data, and practice problems with varying contexts

#### 3. Integration (Connecting Ideas, People, Domains)

- **Application:** Making connections between ideas, between courses, between academic and personal life
- **Material types:** Cross-reference tables, integrative essays, concept maps showing connections
- **KST alignment:** Leverages the surmise relation -- explicitly show how the current item connects to prerequisites and to items it will unlock
- **Example:** "How does your understanding of probability distributions (mastered) connect to this new item on hypothesis testing? Here is a concept map showing the relationship."

#### 4. Human Dimension (Learning About Self and Others)

- **Application:** Understanding how the knowledge affects the student's self-image and understanding of others
- **Material types:** Reflection prompts, self-assessment, peer discussion questions
- **KST alignment:** Supports metacognitive awareness of the student's position in the knowledge space
- **Example:** "You now understand [n] of [total] items in this domain. What does it feel like to see your knowledge growing? How might this knowledge change how you approach [real-world context]?"

#### 5. Caring (Developing New Feelings, Interests, Values)

- **Application:** Developing new interests, motivation, and values related to the subject
- **Material types:** Real-world impact stories, ethical scenarios, personal relevance prompts
- **KST alignment:** Supports engagement and intrinsic motivation for continued learning through the knowledge space
- **Example:** "Why does understanding statistical significance matter in everyday life? Consider how this knowledge might change how you read news articles."

#### 6. Learning How to Learn (Self-Directed Learning, Metacognition)

- **Application:** Becoming a better, more self-directed learner
- **Material types:** Study strategy guides, learning plan templates, metacognitive reflection prompts
- **KST alignment:** Help students understand the knowledge space itself -- "Here is your learning path; here is how to use fringes to guide your own study"
- **Example:** "Your outer fringe contains [n] items. Here is a strategy for deciding which to study first: look for items that share competences with multiple other items, so mastering one competence unlocks several."

---

## Extended Adaptation Guidelines

### Struggling Students (Few Items Mastered, Many Incorrect)

**Indicators:** Current state is small relative to domain; assessment had many incorrect responses; high-DOK items predominantly incorrect.

**Adaptations:**
- **More scaffolding layers:** Add an additional pre-instruction step with concrete manipulatives or analogies before direct instruction
- **Smaller steps:** Break each outer fringe item into micro-objectives (even if they are not separate KST items)
- **More worked examples:** Provide 4-5 worked examples instead of 2-3, with very gradual complexity increase
- **Explicit prerequisite review:** Even if inner fringe items are recent, provide explicit review since the student may have fragile mastery
- **Reduced choice:** Offer 2 options instead of 3 to reduce decision fatigue
- **Frequent check-ins:** Add comprehension checks after every major concept (not just at the end)
- **Success framing:** Emphasize what the student has already mastered, not what remains

**Example:** For a student who has mastered only 5 of 30 items, the outer fringe might contain 3 items. Generate materials for just 1-2 items per session, with extensive scaffolding and review.

### Advanced Students (Many Items Mastered, Strong Assessment)

**Indicators:** Large current state; assessment had few errors; student engaged with higher Bloom's levels.

**Adaptations:**
- **Fewer worked examples:** Provide 1 example then move to independent practice
- **More extension tasks:** Emphasize Create and Evaluate level activities
- **Cross-topic integration:** Design activities that connect multiple outer fringe items or bridge to other domains
- **Self-directed exploration:** Provide resources and prompts for the student to explore beyond the structured materials
- **Efficiency:** Cover multiple outer fringe items per session
- **Metacognitive challenge:** Ask the student to generate their own examples, create teaching materials, or identify connections

**Example:** For a student who has mastered 25 of 30 items, the outer fringe might contain 3-4 advanced items. Generate concise materials that connect these items and include extension challenges.

### Students with Gaps (Non-Contiguous Mastery)

**Indicators:** Current state has "holes" -- items at higher Bloom's levels are mastered but some lower-level prerequisites have low confidence.

**Adaptations:**
- **Prerequisite verification:** Before targeting outer fringe items, generate brief diagnostic questions for prerequisites that might be weak
- **Bridge materials:** Create explicit materials connecting the mastered advanced items back to the gap items
- **Concurrent repair:** Teach the gap item alongside its dependent item, showing why the prerequisite matters
- **Pattern analysis:** Look for missing competences that explain the gap pattern (a single missing competence might explain multiple gaps)

**Example:** A student who can "apply the t-test" but cannot "state the assumptions of the t-test" needs materials that teach the assumptions while connecting them to the procedure they already know.

### Students with Long Gaps (Items Mastered > 4 Weeks Ago)

**Indicators:** History timestamps show extended periods since last interaction; inner fringe items have old mastery dates.

**Adaptations:**
- **State re-verification:** Recommend running `/assessing-knowledge-state` before generating new materials, since forgetting may have altered the true state
- **Dedicated review modules:** For items mastered > 4 weeks ago, generate full review modules (not just brief reminders)
- **Forgetting-aware sequencing:** Review foundational items first (bottom of the prerequisite chain), then work upward, since forgetting cascades downward
- **Spaced practice integration:** Build a spaced review schedule into the new materials
- **Confidence calibration:** Help the student assess their own retention before providing answers

**Example:** A student returning after 6 weeks needs review materials for all inner fringe items before attempting new outer fringe items. Generate review modules in prerequisite order.

---

## Material Customization by Knowledge Type

### Factual Knowledge

- **Primary formats:** Definitions, lists, tables, flashcards, mnemonics
- **Scaffolding emphasis:** Retrieval practice with spaced repetition
- **Common errors:** Confusion between similar terms; incomplete recall
- **Assessment:** Recognition (MC) and recall (fill-in) formats

### Conceptual Knowledge

- **Primary formats:** Explanations, analogies, concept maps, compare/contrast tables, visual models
- **Scaffolding emphasis:** Building from concrete examples to abstract principles; connecting to prior concepts
- **Common errors:** Overgeneralization; failure to distinguish related concepts; surface-level understanding
- **Assessment:** Explanation, example generation, classification tasks

### Procedural Knowledge

- **Primary formats:** Step-by-step guides, worked examples, flowcharts, decision trees, practice problems
- **Scaffolding emphasis:** Worked examples with fading (gradually removing steps); error analysis of common mistakes
- **Common errors:** Step omission; incorrect sequencing; failure to check conditions
- **Assessment:** Problem execution, procedure replication in new contexts

### Metacognitive Knowledge

- **Primary formats:** Reflection prompts, strategy guides, self-monitoring checklists, planning templates
- **Scaffolding emphasis:** Modeling metacognitive processes; think-aloud demonstrations; strategy comparison
- **Common errors:** Applying strategies inflexibly; poor self-monitoring; overconfidence
- **Assessment:** Strategy selection justification, self-assessment accuracy, planning quality

---

## References

- Ausubel, D. P. (1968). *Educational Psychology: A Cognitive View*. Grune & Stratton.
- CAST (2024). *Universal Design for Learning Guidelines version 3.0*. Wakefield, MA: CAST.
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T. & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin, 132*(3), 354-380.
- de Chiusole, D., Stefanutti, L., Anselmi, P. & Robusto, E. (2022). Learning, forgetting, and the correlation of knowledge in knowledge space theory. *Journal of Mathematical Psychology, 108*.
- Fink, L. D. (2003). *Creating Significant Learning Experiences: An Integrated Approach to Designing College Courses*. Jossey-Bass.
- Stefanutti, L., de Chiusole, D. & Anselmi, P. (2021). Modeling learning in knowledge space theory through bivariate Markov processes. *Journal of Mathematical Psychology, 101*.
- Vygotsky, L. S. (1978). *Mind in Society: The Development of Higher Psychological Processes*. Harvard University Press.
