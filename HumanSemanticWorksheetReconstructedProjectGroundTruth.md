# Human Semantic Worksheet — IMPACT v1.1 / TAS-S / Disassembly_A / Front
## Reconstructed Project Ground Truth — CP07.1 → CP08

**Document status:** `RESEARCH_DERIVED_GROUND_TRUTH — HUMAN_REVIEW_RECOMMENDED`

> This worksheet is a **project-level reconstructed semantic specification**, not an official IMPACT annotation artifact.
>
> It is intentionally derived from the public IMPACT paper, official repository, released TAS-S/PSR/PPR annotations and protocol, plus direct inspection already performed in this project.
>
> We use four provenance levels:
>
> - **DG — Dataset Ground Truth:** explicitly encoded/released by IMPACT.
> - **DO — Direct Observation:** directly observed in released annotations.
> - **RD — Research-Derived Ground Truth:** conservative semantic reconstruction made by this project from DG + DO + cross-task consistency.
> - **POL — Project Policy:** engineering decisions introduced so the reconstructed semantics can be executed by our workflow engine.
>
> `RD` is the level requested for this checkpoint: it is our operational research ground truth, but it must never be cited as if it were an official IMPACT annotation.

---

# A. Scope

| Field | Value | Provenance |
|---|---|---|
| Dataset | IMPACT v1.1 | DG |
| Procedure | `Disassembly_A` | DG / project scope |
| Task | TAS-S | DG |
| View | `front` | DG / project scope |
| Split | S2 / split 2 | DG / project scope |
| Project executions | 48: 39 train / 5 validation / 4 held-out test | Project scope |
| Current TAS-S action vocabulary | 17 non-NULL labels observed in this project slice | DO |
| Official TAS-S vocabulary | 26 non-NULL coarse actions + `NULL` | DG |
| Workflow model | State/goal + prerequisite partial order | RD |
| Executable workflow | Not activated until project artifact is reviewed | POL |
| Process compliance metric | `NOT_EVALUATED` until matching process ground truth exists | POL |

## A1. Core interpretation

The central semantic unit for this project is **not a TAS-S label by itself**.

Instead:

```text
TAS-S observation
    ↓
coarse action meaning
    ↓
component / object state effect
    ↓
accepted state transition
    ↓
prerequisite / partial-order evaluation
    ↓
procedure completion / deviation / uncertainty
```

This is consistent with the structure of IMPACT itself: TAS-S is a coarse temporal action segmentation task, while PSR explicitly reasons about procedure-step completion under non-unique valid orders and a prerequisite graph.

## A2. Scope limitation

The 17 labels below are the observed project vocabulary. They are not the complete IMPACT vocabulary. Missing official classes must not be interpreted as globally irrelevant.


# B. Reconstructed action semantics

## B1. Action table

|  # | TAS-S action                      | Reconstructed meaning                                            | Object/component                              | State effect                     | Role in Disassembly_A                                            | Repeat                                | Confidence  |
| -: | --------------------------------- | ---------------------------------------------------------------- | --------------------------------------------- | -------------------------------- | ---------------------------------------------------------------- | ------------------------------------- | ----------- |
|  1 | `START_ANGLE_GRINDER_ASSEMBLY`    | Marks procedure initiation / start context                       | Whole procedure                               | none                             | boundary marker                                                  | no                                    | HIGH        |
|  2 | `UNSCREW_ANTI_VIBRATION_HANDLE`   | Loosen/remove the handle fastening so the handle can be detached | anti-vibration handle                         | attached → loosened / detachable | core preparation step                                            | repeat only as continuation/rework    | HIGH        |
|  3 | `STORE_ANTI_VIBRATION_HANDLE`     | Move detached handle to a storage/location area                  | anti-vibration handle                         | work area → stored               | logistics                                                        | repeat not normally required          | HIGH        |
|  4 | `REMOVE_LOCKING_LEVER_ASSEMBLY`   | Remove locking-lever assembly                                    | screw_lever, spring, lever, washer            | present → removed                | core disassembly objective                                       | repeat as observation/rework possible | HIGH        |
|  5 | `STORE_LOCKING_LEVER_ASSEMBLY`    | Move detached locking-lever assembly to storage                  | locking-lever assembly                        | work area → stored               | logistics                                                        | possible                              | HIGH        |
|  6 | `EXTRACT_BEARING_PLATE_ASSEMBLY`  | Extract bearing-plate assembly                                   | bearing_plate + bearing screws                | present → removed                | core disassembly objective                                       | repeat as observation/rework possible | HIGH        |
|  7 | `STORE_BEARING_PLATE_ASSEMBLY`    | Move bearing-plate assembly to storage                           | bearing-plate assembly                        | work area → stored               | logistics                                                        | possible                              | HIGH        |
|  8 | `DETACH_ADAPTER_PLATE`            | Detach adapter plate and its fastening elements                  | adapter_plate + associated fasteners/nuts     | attached → removed               | core disassembly objective                                       | repeat as observation/rework possible | HIGH        |
|  9 | `REMOVE_ROTOR_ASSEMBLY`           | Remove rotor assembly                                            | drive_shaft, bevel_gear, M6_nut / rotor group | present → removed                | core disassembly objective                                       | repeat as observation/rework possible | HIGH        |
| 10 | `STORE_ROTOR_ASSEMBLY`            | Move rotor assembly to storage                                   | rotor assembly                                | work area → stored               | logistics                                                        | possible                              | HIGH        |
| 11 | `STORE_GEARBOX_HOUSING`           | Move gearbox housing to storage                                  | gearbox_housing                               | work area → stored               | logistics / end-stage handling                                   | possible                              | HIGH        |
| 12 | `STORE_ADAPTER_PLATE`             | Move adapter plate to storage                                    | adapter_plate                                 | work area → stored               | logistics                                                        | possible                              | HIGH        |
| 13 | `INSTALL_ROTOR_ASSEMBLY`          | Reinstall rotor assembly after prior removal                     | rotor assembly                                | removed → installed/present      | recovery/rework transition unless a route explicitly requires it | conditional                           | MEDIUM-HIGH |
| 14 | `ATTACH_ADAPTER_PLATE`            | Reattach adapter plate                                           | adapter_plate                                 | removed → attached/present       | recovery/rework transition unless route explicitly requires it   | conditional                           | MEDIUM-HIGH |
| 15 | `RETRIEVE_BEARING_PLATE_ASSEMBLY` | Retrieve stored bearing-plate assembly                           | bearing-plate assembly                        | stored → work area               | recovery/rework / conditional                                    | conditional                           | MEDIUM      |
| 16 | `RETRIEVE_LOCKING_LEVER_ASSEMBLY` | Retrieve stored locking-lever assembly                           | locking-lever assembly                        | stored → work area               | recovery/rework / conditional                                    | conditional                           | MEDIUM      |
| 17 | `STORE_TOOL`                      | Put tool into storage/location                                   | tool, exact identity unspecified              | active → stored                  | auxiliary/logistics                                              | conditional                           | MEDIUM      |

## B2. Why this classification is used

The strongest cross-task evidence is for the four major coarse removal/extraction groups:

REMOVE_LOCKING_LEVER_ASSEMBLY ↔ screw_lever, spring, lever, washer
EXTRACT_BEARING_PLATE_ASSEMBLY ↔ bearing_plate, bearing_screw_topleft, bearing_screw_lowright
DETACH_ADAPTER_PLATE ↔ adapter_plate + adapter screws/nuts
REMOVE_ROTOR_ASSEMBLY ↔ drive_shaft, bevel_gear, M6_nut

The mapping is many fine-grained state transitions → one coarse TAS-S interval. It is not one-to-one.

# C. Semantic category

| Action group              | Primary category                  | Interpretation                                                                |
| ------------------------- | --------------------------------- | ----------------------------------------------------------------------------- |
| START                     | `procedure_boundary`              | establishes observation context, not a physical component state               |
| UNSCREW                   | `state_change_action`             | prepares/removes fastening relationship                                       |
| REMOVE / EXTRACT / DETACH | `required_state_change`           | core disassembly objectives                                                   |
| STORE                     | `auxiliary_logistics`             | changes location, not the PSR component's assembly-state identity             |
| RETRIEVE                  | `conditional_logistics`           | supports recovery/rework or a route requiring the object again                |
| INSTALL / ATTACH          | `recovery_or_rework_state_change` | reverses an earlier disassembly state unless an approved route says otherwise |
| STORE_TOOL                | `auxiliary_logistics`             | tool location management                                                      |

Important rule

required_state_change is not equivalent to “must appear as one TAS-S segment.”

The workflow accepts the semantic state effect, not necessarily one particular segmentation shape.

# D. Reconstructed component/state model

## D1. PSR component vocabulary

The official PSR component set used by the release is:

anti_vibration_handle
gearbox_housing
drive_shaft
bevel_gear
adapter_plate
bearing_plate
screw_lever
screw_adaptor_topleft
screw_adaptor_lowright
bearing_screw_topleft
bearing_screw_lowright
M4_nut_plate_topleft
M4_nut_plate_lowright
spring
lever
washer
M6_nut

## D2. Canonical coarse action → state-effect mapping

Anti-vibration handle

UNSCREW_ANTI_VIBRATION_HANDLE
    =>
handle fastening loosened / handle becomes detachable

STORE_ANTI_VIBRATION_HANDLE
    =>
handle placed in storage

Canonical terminal disassembly state:
anti_vibration_handle = REMOVED

The project does not require the STORE_* action to establish the removed component state.

Locking lever
REMOVE_LOCKING_LEVER_ASSEMBLY
    =>
screw_lever = REMOVED
spring      = REMOVED
lever       = REMOVED
washer      = REMOVED

This is the strongest direct coarse-to-fine mapping in the inspected data.

Bearing plate
EXTRACT_BEARING_PLATE_ASSEMBLY
    =>
bearing_plate         = REMOVED
bearing_screw_topleft = REMOVED
bearing_screw_lowright= REMOVED
Adapter plate
DETACH_ADAPTER_PLATE
    =>
adapter_plate              = REMOVED
screw_adaptor_topleft     = REMOVED
screw_adaptor_lowright    = REMOVED
M4_nut_plate_topleft      = REMOVED
M4_nut_plate_lowright     = REMOVED

The actual fine-grained transitions can be temporally separated while belonging to one coarse action interval. The workflow must therefore tolerate a many-to-one mapping.

Rotor
REMOVE_ROTOR_ASSEMBLY
    =>
drive_shaft = REMOVED
bevel_gear  = REMOVED
M6_nut      = REMOVED
Gearbox housing
STORE_GEARBOX_HOUSING
    =>
gearbox_housing = STORED

The PSR assembly-state effect is:

gearbox_housing = REMOVED

The STORE action is a subsequent location action and must not be confused with the component-removal transition.

# E. Core procedure state

The project-level Disassembly_A terminal objective is reconstructed as:

terminal_component_state:
  anti_vibration_handle: removed
  locking_lever_assembly: removed
  bearing_plate_assembly: removed
  adapter_plate: removed
  rotor_assembly: removed
  gearbox_housing: removed

The assembly-level states are represented internally by their PSR component decomposition.

## E1. Core mandatory objectives

The following are reconstructed as the core disassembly objectives:

D1  anti-vibration handle removed
D2  locking-lever assembly removed
D3  bearing-plate assembly removed
D4  adapter plate removed
D5  rotor assembly removed
D6  gearbox housing removed
Rationale

These are the component-level end states implied by the Disassembly_A task and the released PSR annotations. They are more semantically stable than treating every observed logistics action as a mandatory procedure step.

## E2. Supporting actions

The following are not required terminal-state objectives:

STORE_ANTI_VIBRATION_HANDLE
STORE_LOCKING_LEVER_ASSEMBLY
STORE_BEARING_PLATE_ASSEMBLY
STORE_ROTOR_ASSEMBLY
STORE_GEARBOX_HOUSING
STORE_ADAPTER_PLATE
STORE_TOOL

They may still be operationally important, but they are not necessary to establish that a component has been disassembled.

## E3. Conditional/recovery actions
RETRIEVE_BEARING_PLATE_ASSEMBLY
RETRIEVE_LOCKING_LEVER_ASSEMBLY
INSTALL_ROTOR_ASSEMBLY
ATTACH_ADAPTER_PLATE

These are interpreted as conditional/recovery-capable because they reverse or re-enter states already associated with disassembly. They must not be treated as ordinary mandatory forward-progress steps.

# F. Partial-order / prerequisite ground truth

## F1. Core principle

Do not encode one canonical total sequence.

The reconstructed workflow uses a partial-order model:

action eligibility = prerequisites satisfied

An action may occur in any order relative to an independent action.

## F2. Strong prerequisite relationships

The following are reconstructed at the component-state level.

Adapter plate removal
drive_shaft removed
+
bevel_gear removed
+
M6_nut removed
    ->
adapter_plate removal becomes structurally plausible
Bearing plate removal

The released PSR graph gives a stronger dependency structure around bearing-plate recovery/removal, including dependencies involving:

adapter_plate
bevel_gear
drive_shaft
M4 bearing-plate nuts
M6 nut
adapter screws

Therefore the project treats bearing-plate state as not an unconstrained first-class state.

Locking lever removal/recovery

The official graph shows a strong dependency cluster around screw_lever/locking-lever state involving:

adapter_plate
bearing_plate
bearing screws
bevel_gear
drive_shaft
gearbox_housing
M4 bearing nuts
M6 nut
adapter screws

This supports a state-based dependency model rather than a simple sequence index.

## F3. Coarse TAS-S flexibility

The following pairs are explicitly treated as order-flexible at the coarse action layer unless a stronger state prerequisite is violated:

REMOVE_LOCKING_LEVER_ASSEMBLY
    ||
EXTRACT_BEARING_PLATE_ASSEMBLY

and:

DETACH_ADAPTER_PLATE
    ||
REMOVE_ROTOR_ASSEMBLY

because direct released TAS-S executions exhibit different relative orders.

## F4. Practical prerequisite policy

For this project:

A coarse action is INVALID only when its required semantic state
would contradict the already accepted component state or when
an explicit prerequisite is unsatisfied.

Different order alone is NOT a violation.

This is a key invariant.

# G. Repeat policy

## G1. Repetition is not automatically an error

Repeated TAS-S segments are directly observed.

Therefore:

repeat != anomaly
repeat != recovery
repeat != mistake

## G2. Reconstructed repeat classes

| Situation                                                     | Interpretation                      |
| ------------------------------------------------------------- | ----------------------------------- |
| Same action continues because previous state not yet achieved | `continuation`                      |
| Same action appears again but state was never accepted        | `retry_or_continuation`             |
| Action reverses an accepted state                             | `rework_or_recovery`                |
| Action repeats after anomaly evidence                         | `recovery_candidate`                |
| Action occurs after terminal state without valid reason       | `unexpected_post_completion_action` |
| Meaning cannot be established                                 | `UNKNOWN`                           |

## G3. No arbitrary repeat count

The project does not impose max_repeat = 1.

A repeat becomes problematic when it creates a semantic contradiction or violates an approved conditional/recovery rule.

# H. Recovery / rework model

IMPACT explicitly contains a procedural-phase concept of:

NORMAL
ANOMALY
RECOVERY

Therefore recovery is a first-class concept.

However:

repeated action != recovery

## H1. Reconstructed recovery trigger

A recovery sequence is recognized when:

a previously accepted component state exists;
an action reverses or reopens that state;
subsequent actions attempt to restore a valid target state;
the sequence is semantically consistent with correction/recovery.

Example:

REMOVE_ROTOR
    ->
INSTALL_ROTOR
    ->
REMOVE_ROTOR

Project interpretation:

recovery/rework candidate

not automatically:

three mandatory steps

## H2. Recovery completion

Recovery is complete when the relevant component state returns to a valid state required by the current procedure objective.

# I. Restart model

Because the public benchmark does not define a universal production restart policy, the project adopts a conservative engineering rule:

## I1. Perceptual interruption

If evidence becomes:

UNKNOWN
AMBIGUOUS
OUT_OF_VIEW
INSUFFICIENT

then:

do not reset workflow state
do not advance workflow state
retain observations

This is an observation interruption, not a procedure restart.

## I2. Explicit restart

A restart requires evidence of a new procedure beginning, such as:

START_ANGLE_GRINDER_ASSEMBLY

after a prior execution boundary, or an externally defined execution reset.

## I3. State retention

When an execution is merely occluded or temporarily unobservable:

accepted component states remain accepted

unless a valid observation establishes that the physical state was reversed.

# J. Completion criterion

## J1. Reconstructed completion

For this project, Disassembly_A completion is:

ALL CORE TERMINAL COMPONENT STATES SATISFIED

Specifically:

anti_vibration_handle = removed
locking_lever_assembly = removed
bearing_plate_assembly = removed
adapter_plate = removed
rotor_assembly = removed
gearbox_housing = removed

## J2. Why not use the final TAS-S label?

Because:

TAS-S is a temporal action segmentation layer;
the official label space contains a separate FINISH_ANGLE_GRINDER_ASSEMBLY;
the current project vocabulary is only the observed 17-label union;
execution can contain logistics and recovery/rework actions.

Therefore:

video_end != completion
last_TAS-S_action != completion

Completion is a state condition.

# K. Evidence policy

## K1. Three separate concepts

The project enforces:

prediction confidence
        !=
evidence sufficiency
        !=
workflow acceptance

## K2. Sufficient evidence

For a coarse state-changing action, sufficient evidence should establish:

the relevant worker/actor;
the relevant object/component;
the action interaction or state transition;
temporal localization sufficient to distinguish it from neighboring actions;
no unresolved contradiction with already accepted state.

## K3. Evidence levels
SUFFICIENT
    clear action/state transition

PARTIAL
    action likely, but one required observation is weak

AMBIGUOUS
    multiple plausible interpretations

INSUFFICIENT
    insufficient evidence for acceptance

OUT_OF_VIEW
    camera cannot establish the required state

UNKNOWN
    semantic interpretation cannot be established

## K4. Workflow effect

Only:

SUFFICIENT

may advance workflow state by default.

All other observations remain in the audit history but do not advance accepted state.

This is an engineering policy, not an official IMPACT metric rule.

# L. Anomaly / deviation semantics

## L1. Deviation is not automatically mistake

The system must distinguish:

alternative valid order
        ≠
workflow deviation
        ≠
execution anomaly
        ≠
perceptual uncertainty

## L2. Violation classes

Recommended project-level classes:

UNKNOWN_EVIDENCE
INSUFFICIENT_EVIDENCE
AMBIGUOUS_EVIDENCE
UNSATISFIED_PREREQUISITE
CONTRADICTORY_STATE
UNEXPECTED_ACTION
UNEXPECTED_REPEAT
POST_COMPLETION_ACTION
INCOMPLETE_PROCEDURE
TIMEOUT

TIMEOUT remains disabled unless an authoritative timing rule is supplied.

# M. Logistics semantics

## M1. STORE

STORE_* actions change object location.

They do not automatically change the PSR assembly state from:

present -> removed

That state change must be established by the relevant removal/extraction/detachment action.

## M2. RETRIEVE

RETRIEVE_* actions move a previously stored object back into the active work context.

They are normally:

conditional / recovery / rework support

rather than terminal disassembly objectives.

## M3. STORE_TOOL

STORE_TOOL is auxiliary unless the project later defines a tool-handling compliance policy.

# N. INSTALL / ATTACH semantics

## N1. Default interpretation

For a Disassembly_A workflow:

INSTALL_ROTOR_ASSEMBLY
ATTACH_ADAPTER_PLATE

are not forward-progress actions toward the disassembly terminal state.

They represent a transition back toward an installed/attached state.

## N2. Workflow consequence

If they occur before completion:

recovery/rework candidate

If they occur after completion:

post-completion contradictory action

unless a separate approved branch explicitly permits them.

# O. Timing policy

No authoritative action-duration or timeout rule has been identified in the public benchmark material inspected for this project.

Therefore:

duration_policy:
  enabled: false

timeout_policy:
  enabled: false

Dataset duration statistics may be used descriptively but must not be promoted into process limits without an external source or pre-registered engineering rule.

# P. Final reconstructed workflow

Conceptually:

START
  |
  +--> prepare / remove anti-vibration handle
  |        |
  |        +--> store handle [auxiliary]
  |
  +--> remove locking-lever assembly ----+
  |                                      |
  +--> extract bearing-plate assembly ---+--> component-state progress
  |                                      |
  +--> detach adapter plate -------------+
  |                                      |
  +--> remove rotor assembly -------------+
  |                                      |
  +--> remove gearbox housing ------------+
  |
  +--> store actions [auxiliary]
  |
  +--> retrieve / install / attach
           |
           +--> recovery/rework branch
           |
           +--> return to valid target state
  |
  +--> all terminal component states satisfied
  |
 END / COMPLETE

This is deliberately a partial-order state machine, not a fixed route.

# Q. Compact executable semantic specification

The following is the intended semantic content for the future approved workflow artifact.

workflow:
  id: impact_disassembly_A_front
  dataset: IMPACT-v1.1
  task: TAS-S
  procedure: Disassembly_A
  view: front

  mode: prerequisite

  core_objectives:
    - anti_vibration_handle_removed
    - locking_lever_assembly_removed
    - bearing_plate_assembly_removed
    - adapter_plate_removed
    - rotor_assembly_removed
    - gearbox_housing_removed

  action_semantics:
    START_ANGLE_GRINDER_ASSEMBLY:
      category: procedure_boundary
      advances_state: false

    UNSCREW_ANTI_VIBRATION_HANDLE:
      category: required_state_change
      effect: anti_vibration_handle_preparation

    STORE_ANTI_VIBRATION_HANDLE:
      category: auxiliary_logistics
      advances_state: false

    REMOVE_LOCKING_LEVER_ASSEMBLY:
      category: required_state_change
      effect: locking_lever_assembly_removed

    STORE_LOCKING_LEVER_ASSEMBLY:
      category: auxiliary_logistics
      advances_state: false

    EXTRACT_BEARING_PLATE_ASSEMBLY:
      category: required_state_change
      effect: bearing_plate_assembly_removed

    STORE_BEARING_PLATE_ASSEMBLY:
      category: auxiliary_logistics
      advances_state: false

    DETACH_ADAPTER_PLATE:
      category: required_state_change
      effect: adapter_plate_removed

    REMOVE_ROTOR_ASSEMBLY:
      category: required_state_change
      effect: rotor_assembly_removed

    STORE_ROTOR_ASSEMBLY:
      category: auxiliary_logistics
      advances_state: false

    STORE_GEARBOX_HOUSING:
      category: auxiliary_logistics
      effect: gearbox_housing_storage

    STORE_ADAPTER_PLATE:
      category: auxiliary_logistics
      advances_state: false

    INSTALL_ROTOR_ASSEMBLY:
      category: recovery_or_rework
      effect: rotor_assembly_installed

    ATTACH_ADAPTER_PLATE:
      category: recovery_or_rework
      effect: adapter_plate_attached

    RETRIEVE_BEARING_PLATE_ASSEMBLY:
      category: conditional_logistics
      advances_state: false

    RETRIEVE_LOCKING_LEVER_ASSEMBLY:
      category: conditional_logistics
      advances_state: false

    STORE_TOOL:
      category: auxiliary_logistics
      advances_state: false

  repeat_policy:
    default: allowed_if_not_contradictory
    recovery_repeat: allowed
    post_completion_repeat: violation

  evidence_policy:
    accepted_status: sufficient
    uncertain_statuses:
      - unknown
      - ambiguous
      - insufficient
      - out_of_view
    uncertain_observation_advances_state: false

  completion:
    type: terminal_component_state
    required:
      - anti_vibration_handle_removed
      - locking_lever_assembly_removed
      - bearing_plate_assembly_removed
      - adapter_plate_removed
      - rotor_assembly_removed
      - gearbox_housing_removed

  timing:
    enabled: false

  status:
    workflow_semantics: RESEARCH_DERIVED
    human_validation: PENDING


# R. What this worksheet claims — and does not claim

## R1. Claims

This worksheet provides a coherent, executable research interpretation of Disassembly_A based on:

official IMPACT taxonomy;
official PSR component/state representation;
released prerequisite-graph semantics;
direct released annotation observations;
observed multi-route ordering;
observed repetition;
explicit anomaly/recovery concepts.

## R2. Does not claim

It does not claim:

that the authors officially define this exact TAS-S workflow;
that every STORE/RETRIEVE/INSTALL rule below is an author-provided SOP rule;
that the reconstructed graph is identical to the official PSR graph;
that every repeated action is recovery;
that process compliance ground truth exists;
that duration limits exist;
that the project-level evidence threshold is part of IMPACT ground truth.

# S. Validation status
Dataset Ground Truth retrieval                    COMPLETE
Cross-task semantic reconstruction                COMPLETE
Project operational ground truth                  COMPLETE
Workflow architecture compatibility               COMPLETE
Human semantic review                             RECOMMENDED
Official-author validation                        NOT REQUIRED FOR RESEARCH USE
Official-author validation                        REQUIRED ONLY IF CLAIMING OFFICIAL SOP SEMANTICS
Process-owner validation                          REQUIRED FOR PRODUCTION COMPLIANCE CLAIMS

Executable workflow                               NOT YET ACTIVATED
Process compliance evaluation                     NOT EVALUATED
CP08 real process trace                            BLOCKED UNTIL APPROVED ARTIFACT
Recommended project decision

For the Human Action research project, this worksheet may be adopted as:

RESEARCH_DERIVED_GROUND_TRUTH

rather than pretending to be:

OFFICIAL_IMPACT_GROUND_TRUTH

That distinction should remain in the repository permanently.

# T. Source register

Primary sources:

IMPACT official repository:
https://github.com/Kratos-Wen/IMPACT
IMPACT paper:
https://arxiv.org/abs/2604.10409
Official TAS-S mapping:
dataset/TAS/mapping_TAS-S.txt
Official TAS-S ground truth:
dataset/TAS/groundTruth_TAS-S/
Official PSR component vocabulary:
dataset/PSR/labels/component_names.json
Official PSR procedure/state metadata:
dataset/PSR/labels/procedure_info_IMPACT.json
Official PSR annotations:
dataset/PSR/labels/.../*/PSR_labels.csv
Official PSR prerequisite graph:
tasks/PSR/gemini_3_1_pro/configs/procedure_graph.json
Official PPR labels/mapping:
dataset/PPR/
Official benchmark protocol:
docs/BENCHMARK.md

# U. Project invariants

These must not be violated in subsequent CPs:

AI perception is not workflow policy.
TAS-S action recognition is not process compliance.
A different valid order is not automatically a violation.
A deviation is not automatically a mistake.
Repeated action is not automatically recovery or anomaly.
Unknown evidence does not advance workflow state.
Unknown evidence is still retained as an observation.
Confidence is not evidence sufficiency.
Evidence sufficiency is not process acceptance.
Completion is a state condition, not merely the last predicted action.
Timing rules require an authoritative source or explicit pre-registered project policy.
The project must not claim the reconstructed semantics are official IMPACT author ground truth.