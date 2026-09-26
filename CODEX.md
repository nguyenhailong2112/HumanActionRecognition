# CODEX.md

# Human Action & Procedure Understanding for Industrial Vision

## 1. PROJECT PURPOSE

Human Action is an R&D project for building a practical industrial Vision AI system capable of understanding human activities and procedures from video/CCTV.

Target pipeline:

```text
Video
  ↓
Scene Understanding
  ↓
Person / Object / Tool / Hand / Pose / Tracking
  ↓
Action Understanding
  ↓
Temporal Understanding
  ↓
Action Events
  ↓
Workflow / Process State
  ↓
Compliance / Anomaly
  ↓
Evidence / Output
```

The project supports two main operating profiles:

```text
A. Fine-Grained / Small-FOV
   Hand / Object / Tool / Fine Manipulation

B. Large-Scale / Large-FOV
   Person / Pose / Zone / Activity / Equipment
```

The final goal is not merely Action Recognition.

The system should understand:

```text
WHO, WHAT, WHEN, WHERE, WITH WHAT, IN WHICH STEP, EXPECTED WHAT, ACTUALLY WHAT, HOW LONG, COMPLIANT OR NOT, WHY, EVIDENCE
```

---

# 2. CORE ENGINEERING PRINCIPLE

Always prefer:

```text
CORRECT → SUFFICIENT → SIMPLE → EFFECTIVE
```

The project is practical R&D.

Do not make the system more complicated than the real problem requires.

---

# 3. CODE QUALITY

All code must be:

* Clean.
* Readable.
* Easy to understand.
* Easy to review.
* Easy to debug.
* Easy to modify.
* Easy to audit.

Prefer straightforward code over clever code.

Avoid:

```text
Unnecessary abstraction
Deep inheritance
Complex generic frameworks
Huge utility layers
Magic behavior
Hidden side effects
Overly clever one-liners
Premature optimization
```

A future engineer should be able to read the code and quickly understand what it does.

---

# 4. ARCHITECTURE QUALITY

The system architecture must remain:

```text
Clear
Modular
Predictable
Controllable
Small enough to understand
```

Preferred conceptual modules:

```text
perception/
tracking/
action/
temporal/
workflow/
anomaly/
evidence/
runtime/
```

Keep module responsibilities clear.

Do not create a new module merely because a small function exists.

Do not create abstractions before there is a real need.

---

# 5. NO OVER-ENGINEERING

Do not introduce complexity only because:

* A newer model exists.
* A paper uses it.
* A framework is fashionable.
* A technology is academically interesting.
* It looks more “professional”.

Before adding complexity, answer:

```text
What real problem does it solve?
Why is the current solution insufficient?
How will we measure the improvement?
What new complexity/risk does it introduce?
```

If there is no clear answer, do not add it.

---

# 6. PROBLEM FIRST, MODEL SECOND

Use this direction:

```text
Industrial Problem
→ Observable Evidence
→ Required Information
→ Representation
→ Algorithm
→ Model
→ Implementation
→ Validation
```

Never start from:

```text
New Model
→ Find a use for it
```

---

# 7. PERCEPTION VS PROCESS LOGIC

Keep these responsibilities separate:

```text
AI Perception
≠
Workflow / Process Logic
```

Perception should answer:

```text
What is visible?
What is happening?
Who is doing it?
What object/tool is involved?
When did it happen?
```

Process logic should answer:

```text
Which step is expected?
Is the transition valid?
Is the duration valid?
Is the procedure compliant?
```

Use deterministic logic when deterministic logic is sufficient.

---

# 8. ACTION HIERARCHY

Conceptually use:

```text
Gesture / Motion
    ↓
Interaction
    ↓
Atomic Action
    ↓
Task
    ↓
Activity
    ↓
Procedure / Workflow
```

Examples:

```text
Reach
Pick
Place
Insert
Remove
Press
Scan
Tighten
Inspect
Assembly
Maintenance
```

Use only the level of granularity required by the use case.

Do not create hundreds of classes without a real requirement.

---

# 9. ACTION EVENT

Whenever practical, convert model outputs into structured temporal events.

Conceptually:

```text
ActionEvent
{
    worker_id,
    action,
    object,
    tool,
    zone,
    start_time,
    end_time,
    duration,
    confidence
}
```

The exact schema may evolve.

The principle should remain:

> Downstream process logic should consume structured events rather than raw frame predictions.

---

# 10. TEMPORAL UNDERSTANDING

Human Action is a temporal problem.

The system should understand:

```text
Action Start
Action Progress
Action End
Duration
Transition
Idle
Unknown
```

Avoid unstable outputs such as:

```text
PICK
UNKNOWN
PICK
PICK
UNKNOWN
```

Use temporal smoothing/debouncing or stronger temporal models when required.

Do not introduce a complex temporal architecture before checking whether a simple temporal method is sufficient.

---

# 11. WORKFLOW ENGINE

Workflow should be configuration-driven.

Do not hard-code procedures throughout the source code.

Conceptually:

```yaml
workflow: assembly_A

steps:
  - id: S1
    action: PICK

  - id: S2
    action: PLACE

  - id: S3
    action: SCAN

  - id: S4
    action: ASSEMBLE

  - id: S5
    action: INSPECT
```

Workflow may support:

```text
Sequential steps
Optional steps
Conditional steps
Branches
Alternative valid paths
Rework
Restart
Timeout
Completion
```

Only implement these when the use case requires them.

---

# 12. ANOMALY TYPES

Core anomaly categories:

```text
Wrong Sequence
Skipped Step
Repeated Step
Unexpected Action
Backward Transition
Too Slow
Too Fast
Idle
Timeout
Incomplete Procedure
Wrong Object
Wrong Tool
Wrong Zone
Wrong Interaction
```

Do not add anomaly categories without a practical requirement.

---

# 13. DEVIATION ≠ MISTAKE

Never assume:

```text
Deviation from one sequence
=
Mistake
```

A procedure may allow:

```text
Multiple valid paths
Optional steps
Conditional steps
Rework
Recovery
```

Represent valid alternatives when required.

---

# 14. UNKNOWN IS VALID

The system may return:

```text
UNKNOWN
AMBIGUOUS
OCCLUDED
OUT_OF_VIEW
TRANSITION
IDLE
INSUFFICIENT_EVIDENCE
```

Do not force a low-confidence observation into a known action class.

Prefer:

```text
Correct uncertainty
>
False certainty
```

---

# 15. HUMAN / OBJECT / TOOL / ZONE

For industrial actions, reason about relationships when useful:

```text
Human
+
Object
+
Tool
+
Zone
+
Time
```

Examples:

```text
Near
Contact
Holding
Moving-With
Released
Inside-Zone
Interacting
```

Do not assume pose alone is sufficient for fine-grained manipulation.

---

# 16. MULTI-PERSON

Every process-related event must remain associated with the correct worker.

Conceptually:

```text
Worker A
    PICK
    PLACE
    SCAN

Worker B
    MOVE
    INSPECT
```

Do not merge events from different workers into one workflow.

Tracking quality is therefore part of process understanding.

---

# 17. CAMERA IS PART OF THE SYSTEM

Before increasing model complexity, ask:

```text
Can the camera actually see the required evidence?
```

Check:

```text
View
FOV
Distance
Angle
Resolution
FPS
Lighting
Occlusion
Background
```

If the required evidence is not visible, improve observation first.

A better camera view may solve a problem that a larger model cannot solve reliably.

---

# 18. RESEARCH WORKFLOW

Every meaningful research question follows:

```text
Question
→ Hypothesis
→ Experiment
→ Measurement
→ Error Analysis
→ Decision
```

Decision:

```text
KEEP
CHANGE
DROP
INVESTIGATE
```

A failed experiment is still a valid R&D result when properly measured and documented.

---

# 19. BASELINE FIRST

Use a simple baseline before an advanced method.

Preferred progression:

```text
Rule / Heuristic
→ Simple Baseline
→ Temporal Baseline
→ Strong Baseline
→ Advanced Method only if justified
```

Candidate temporal baselines may include:

```text
MS-TCN / MS-TCN++
ASFormer
ActionFormer
```

Do not benchmark many models without a research question.

---

# 20. ADVANCED MODELS

Do not automatically introduce:

```text
Large Video Foundation Models
VLM / LLM
World Models
Reinforcement Learning
Complex Graph Networks
Universal End-to-End Models
```

Use them only when experiments show a real limitation that simpler approaches cannot solve sufficiently.

Any advanced proposal must state:

```text
Problem solved
Evidence
Expected gain
Cost
Risk
Evaluation method
```

---

# 21. RESEARCH SOURCES

For external research, prioritize:

```text
Official Paper
Official Project Page
Official GitHub
Official Dataset Documentation
Supplementary Material
Official Benchmark
```

Do not treat:

```text
Search snippets
Blogs
Copied repositories
AI summaries
```

as primary evidence.

---

# 22. RESEARCH UNDERSTANDING

For important research, inspect:

```text
Problem
Dataset
Annotation
Representation
Architecture
Training
Inference
Evaluation
Failure Cases
Limitations
Code
```

Do not claim full understanding from an abstract alone.

---

# 23. EXPERIENCE.md

Each major research folder should have:

```text
EXPERIENCE.md
```

It should capture:

```text
Problem
Input / Output
Dataset
Annotation
Representation
Temporal Method
Procedure
Mistake / Anomaly
Model
Implementation
Evaluation
Limitations
Reusable Ideas
Non-Reusable Ideas
Relevance to Human Action
Evidence
Understanding Status
```

Understanding status:

```text
VERIFIED
PARTIAL
BLOCKED
```

Do not mark VERIFIED without sufficient evidence.

---

# 24. SOURCE TRUTH

Clearly distinguish:

```text
Verified Fact
Author-Reported Result
Our Interpretation
Hypothesis
Unknown
```

Never turn an assumption into a fact.

Never invent:

```text
Citation
Benchmark result
Implementation behavior
Dataset property
Model capability
```

---

# 25. CODE REUSE

Before reusing external code:

```text
Read
Understand
Check dependencies
Check license
Check assumptions
Run baseline
```

Do not blindly copy code.

Document important external dependencies and origins.

---

# 26. DATA

Keep:

```text
Raw
Processed
Annotation
Train
Validation
Test
Outputs
Evidence
```

separate.

Do not modify raw data destructively.

Version important datasets:

```text
dataset_v0.1
dataset_v0.2
dataset_v1.0
```

---

# 27. DATA SPLIT

Do not rely only on random splitting.

When relevant, evaluate:

```text
Random
Cross-Worker
Cross-Session
Cross-Camera
Cross-Location
```

The goal is to understand real generalization.

---

# 28. EXPERIMENT TRACKING

Every significant experiment should record:

```text
Experiment ID
Objective
Hypothesis
Dataset Version
Code Version
Model
Configuration
Hardware
Metrics
Result
Failure Cases
Conclusion
```

Do not overwrite important previous results.

---

# 29. REPRODUCIBILITY

Important experiments should be reproducible from:

```text
Code Version
+
Dataset Version
+
Model Version
+
Config
+
Environment
```

Avoid undocumented manual steps.

---

# 30. CONFIGURATION

Keep important runtime parameters outside business logic where practical:

```text
Camera
Model
Threshold
Workflow
Class Mapping
Paths
Runtime Parameters
```

Use:

```text
configs/
```

Do not spread configuration constants throughout the source code.

---

# 31. ERROR ANALYSIS

Do not stop at:

```text
Accuracy
Precision
Recall
F1
mAP
```

Always inspect failures such as:

```text
False Positive
False Negative
Occlusion
Motion Blur
Small Object
Similar Action
Tracking Failure
Poor Camera View
Lighting
Worker Variation
Object Variation
Ambiguous Action
```

The goal is to understand:

> Why does the system fail?

---

# 32. PROCESS METRICS

Final evaluation must include process-level metrics.

Examples:

```text
Sequence Accuracy
Step Accuracy
Skip Detection
Wrong-Order Detection
Repeat Detection
Duration Anomaly Detection
False Alarm Rate
Miss Rate
Detection Latency
```

Model metrics are not sufficient by themselves.

---

# 33. PROCESS KPI > MODEL KPI

A model with excellent benchmark metrics is not automatically a useful factory system.

Always ask:

```text
Does the system detect meaningful process violations?
Does it produce too many false alarms?
Is the evidence sufficient?
Is the latency acceptable?
Can engineers trust and debug it?
```

---

# 34. EVIDENCE

Important results should provide evidence when practical:

```text
Worker
Workflow
Expected Step
Observed Action
Timestamp
Duration
Confidence
Frame
Video Clip
Reason
```

A violation should be explainable.

---

# 35. PRODUCTION THINKING

Even during R&D, consider:

```text
RTSP
Frame Buffer
Inference
Tracking
Logging
Recovery
Configuration
Evidence
Health
```

But do not build production infrastructure before the core technical hypothesis works.

Prototype first.

Industrialize progressively.

---

# 36. MULTIMODAL BOUNDARY

Do not force Vision to infer information better measured by:

```text
PLC
Sensor
Scanner
Tester
Machine Status
MES
Traceability
```

When appropriate:

```text
Vision
+
Sensor / PLC / Scanner / MES
```

is the correct system architecture.

---

# 37. SOFTWARE DESIGN

Prefer:

```text
Small modules
Clear interfaces
Simple data flow
Explicit behavior
Limited dependencies
```

Avoid:

```text
Huge classes
Huge functions
Global mutable state
Hidden dependencies
Deep abstraction chains
Unnecessary design patterns
```

A simple implementation that can be audited is preferred over a sophisticated implementation that is difficult to control.

---

# 38. RUNTIME DESIGN

Runtime should be predictable.

Handle:

```text
Camera failure
Empty frame
Inference failure
Invalid data
Model loading failure
Unexpected exceptions
Storage failure
```

Use graceful handling and logging.

Do not hide failures.

---

# 39. CHANGE MANAGEMENT

Before making a significant architectural change, ask:

```text
What problem does this change solve?
What evidence supports it?
What can it break?
How will it be validated?
```

Important decisions should be recorded.

---

# 40. REGRESSION

Maintain a small Golden Scenario Set.

At minimum:

```text
Correct
Wrong Sequence
Skipped Step
Repeated Step
Too Slow
Too Fast
Idle
Timeout
Unexpected Action
Wrong Object
Wrong Zone
Incomplete
Valid Branch
Occlusion
Multi-Person
```

Run regression after meaningful changes.

---

# 41. DEFINITION OF DONE

A coding task is not complete because the code runs.

When applicable, completion means:

```text
Implementation
+
Test
+
Validation
+
Evidence
+
Documentation
```

For research:

```text
Experiment
+
Result
+
Error Analysis
+
Decision
```

---

# 42. PROJECT DOCUMENTS

Important project documents:

```text
ROADMAP.md
SCOPEOFWORK.md
PROJECTREADINESSPACKAGE.md
CHECKSHEET.md
CODEX.md
```

Before significant work:

```text
Read relevant project documentation
Understand current state
Check current scope
Check current task
Avoid unrelated changes
```

---

# 43. PROJECT STATE

Do not invent project state.

Use repository files, experiment records and project documentation as the source of truth.

When uncertain:

```text
Inspect
Verify
Then act
```

---

# 44. HUMAN ENGINEER + CODEX

The human engineer owns final engineering decisions.

Codex should:

```text
Research
Analyze
Implement
Measure
Test
Explain
Challenge assumptions
Find evidence
Identify risks
Suggest alternatives
```

For important decisions, present:

```text
Problem
Options
Evidence
Trade-offs
Recommendation
```

Do not silently make major architecture decisions.

---

# 45. WORKING STYLE

When implementing:

```text
Understand existing code first.
Reuse working components when appropriate.
Change the smallest necessary surface.
Keep changes focused.
Test after changes.
```

Avoid large rewrites unless clearly justified.

---

# 46. DEBUGGING

When something fails:

```text
Reproduce
→ Isolate
→ Identify root cause
→ Fix
→ Test
→ Document if important
```

Do not patch symptoms repeatedly without understanding the underlying issue.

---

# 47. OPTIMIZATION

Do not optimize before measuring.

First establish:

```text
Baseline
```

Then measure:

```text
Latency
FPS
CPU
GPU
Memory
Accuracy
```

Only optimize bottlenecks that matter.

---

# 48. ROBUSTNESS

Important robustness dimensions:

```text
Lighting
Occlusion
Motion Blur
Worker Variation
Object Variation
Camera Variation
Background
Tracking Stability
```

Use real failure cases to decide what needs improvement.

Do not optimize theoretical edge cases before real ones.

---

# 49. RESEARCH BACKLOG

Keep advanced or non-critical ideas in backlog rather than interrupting the Core Roadmap.

Examples:

```text
Multi-Camera Fusion
Action Quality Assessment
Few-Shot Adaptation
Cross-Site Generalization
VLM
Foundation Models
Advanced Multimodal Learning
```

Backlog does not mean “must implement”.

---

# 50. FINAL NORTH STAR

Build:

> **The simplest reliable Vision AI system that can understand industrial human activities and procedures well enough to detect meaningful process deviations in real operational environments.**

Always remember:

```text
Understand before implementing.
Measure before optimizing.
Observe before inferring.
Validate before claiming.
Simplify before complicating.
```
