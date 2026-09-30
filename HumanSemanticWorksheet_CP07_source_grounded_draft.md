# Human Semantic Worksheet — IMPACT v1.1 / TAS-S / Disassembly_A / Front
## Research-prepared semantic draft — CP07.1 → CP08 human gate

> **Document status:** `HUMAN_REVIEW_REQUIRED`
>
> This document separates:
> - **DG — Dataset Ground Truth:** explicitly released by IMPACT.
> - **DO — Direct Dataset Observation:** directly observed in released annotations; descriptive, not normative.
> - **INT — Engineering Interpretation:** a reasoned mapping proposed for this project; not an official IMPACT rule.
> - **HUMAN — Human/Process Decision:** must be confirmed by the project owner/process owner before becoming executable workflow semantics.
>
> **Important:** This worksheet is intentionally not marked `HUMAN_VALIDATED`. Its purpose is to remove the need for the project owner to invent semantics while preserving the required human approval gate.

---

# A. Procedure scope

| Field | Current entry | Status |
|---|---|---|
| Dataset | IMPACT v1.1 | DG |
| Task | TAS-S — Temporal Action Segmentation at Step Level | DG |
| Procedure | `Disassembly_A` | DG / project scope |
| View | `front` | DG / project scope |
| Evaluation setting | S2 / cross-subject | DG |
| Project subset | 48 selected front-view Disassembly_A executions: 39 train / 5 val / 4 held-out test | Project experiment scope |
| Current action vocabulary | 17 non-NULL TAS-S classes observed in the project subset | Project-derived scope |
| Official TAS-S vocabulary | 26 non-NULL coarse step classes + `NULL` background | DG |
| Workflow interpretation | Not yet executable | HUMAN |
| Process compliance metric | `NOT_EVALUATED` until approved procedure semantics and matching process ground truth exist | Engineering policy |

### Scope notes

1. The 17 actions in this worksheet are **not the complete official TAS-S vocabulary**. They are the procedure-scoped observed union used by the current project slice.
2. The official TAS-S label space includes additional actions such as `RETRIEVE_GEARBOX_HOUSING`, `RETRIEVE_ROTOR_ASSEMBLY`, `RETRIEVE_ADAPTER_PLATE`, `INSERT_BEARING_PLATE_ASSEMBLY`, `RETRIEVE_LOCKING_LEVER_ASSEMBLY`, `SCREW_ON_ANTI_VIBRATION_HANDLE`, `FINISH_ANGLE_GRINDER_ASSEMBLY`, etc. Their absence from this 17-action project vocabulary must not be interpreted as proof that they are semantically irrelevant to the overall procedure.
3. IMPACT's paper explicitly distinguishes coarse TAS-S step annotations from PSR completion/state reasoning. TAS-S is frame-level coarse procedural labeling; PSR uses a separate prerequisite graph and state representation.

---

# B. Action semantic review

## B1. Source-grounded action semantics

The official TAS-S mapping supplies the released class names. The plain-language descriptions below are deliberately conservative expansions of those names rather than invented SOP descriptions.

| # | TAS-S action | Plain-language meaning | Object / component | Direct PSR relation | Observed repetition | Provisional semantic category | Status |
|---:|---|---|---|---|---|---|---|
| 1 | `START_ANGLE_GRINDER_ASSEMBLY` | Start/initialize the angle-grinder procedure. The label name itself contains “ASSEMBLY”; this should not be rewritten as a physical assembly operation solely because of the name. | Procedure / angle grinder | None directly represented as a PSR component event | Not observed repeated in inspected executions | Boundary / auxiliary marker | DG + INT; workflow role HUMAN |
| 2 | `UNSCREW_ANTI_VIBRATION_HANDLE` | Unscrew/loosen the anti-vibration handle attachment. | `anti_vibration_handle` | PSR contains `remove anti_vibration_handle`, but this is **not equivalent** to proving that every UNSCREW segment is itself the removal transition. | Repeated in at least one inspected execution | Mechanical / state-changing candidate | DG + INT; state semantics HUMAN |
| 3 | `STORE_ANTI_VIBRATION_HANDLE` | Move/store the anti-vibration handle at its storage location. | `anti_vibration_handle` | No direct PSR storage/location state | Not repeated in inspected examples | Auxiliary / logistics action | DG + INT; workflow role HUMAN |
| 4 | `REMOVE_LOCKING_LEVER_ASSEMBLY` | Remove the locking-lever assembly. At PSR granularity this coarse action aligns with multiple component removals. | Locking-lever assembly | Strong direct data-supported alignment to `screw_lever`, `spring`, `lever`, `washer` removal events in the inspected execution | Repeated in inspected executions | State-changing action | DG + DO + INT; workflow role HUMAN |
| 5 | `STORE_LOCKING_LEVER_ASSEMBLY` | Move/store the locking-lever assembly after removal. | Locking-lever assembly | No direct PSR storage/location state | Repeated in at least one inspected execution | Auxiliary / logistics action | DG + INT; workflow role HUMAN |
| 6 | `EXTRACT_BEARING_PLATE_ASSEMBLY` | Extract/remove the bearing-plate assembly. | Bearing-plate assembly | Strong direct data-supported alignment to `bearing_plate`, `bearing_screw_lowright`, `bearing_screw_topleft` removal events in the inspected execution | Repeated in inspected executions | State-changing action | DG + DO + INT; workflow role HUMAN |
| 7 | `STORE_BEARING_PLATE_ASSEMBLY` | Move/store the bearing-plate assembly. | Bearing-plate assembly | No direct PSR storage/location state | Repeated in inspected executions | Auxiliary / logistics action | DG + DO + INT; workflow role HUMAN |
| 8 | `DETACH_ADAPTER_PLATE` | Detach/remove the adapter plate and its associated fastening elements. | Adapter-plate assembly | Strong direct data-supported alignment to `adapter_plate`, `screw_adaptor_lowright`, `M4_nut_plate_lowright`, and later `screw_adaptor_topleft`, `M4_nut_plate_topleft` events in the inspected execution | Repeated in inspected executions | State-changing action | DG + DO + INT; workflow role HUMAN |
| 9 | `REMOVE_ROTOR_ASSEMBLY` | Remove/extract the rotor assembly. | Rotor assembly | Strong direct data-supported alignment to `drive_shaft`, `bevel_gear`, and `M6_nut` removal events in the inspected execution | Repeated many times in inspected executions | State-changing action | DG + DO + INT; workflow role HUMAN |
| 10 | `STORE_ROTOR_ASSEMBLY` | Move/store the rotor assembly after removal. | Rotor assembly | No direct PSR storage/location state | Repeated in inspected executions | Auxiliary / logistics action | DG + DO + INT; workflow role HUMAN |
| 11 | `STORE_GEARBOX_HOUSING` | Move/store the gearbox housing. | `gearbox_housing` | PSR separately contains `remove gearbox_housing`; the TAS-S STORE event itself is not the same event as the PSR removal transition. | Not observed repeated in inspected examples | Auxiliary / logistics action | DG + DO + INT; workflow role HUMAN |
| 12 | `STORE_ADAPTER_PLATE` | Move/store the adapter plate. | `adapter_plate` | No direct PSR storage/location state | Repeated in inspected executions | Auxiliary / logistics action | DG + DO + INT; workflow role HUMAN |
| 13 | `INSTALL_ROTOR_ASSEMBLY` | Install/reinstall the rotor assembly. | Rotor assembly | PSR has installation states for lower-level components, but the release does not provide a one-line TAS-S → exact PSR component-set mapping for this coarse label. | Not characterized from the inspected examples | State-changing / reassembly candidate | DG + INT; exact mapping HUMAN |
| 14 | `ATTACH_ADAPTER_PLATE` | Attach/reinstall the adapter plate. | Adapter-plate assembly | PSR has installation states for adapter-related components, but exact coarse-label grouping is not explicitly stated. | Not characterized from the inspected examples | State-changing / reassembly candidate | DG + INT; exact mapping HUMAN |
| 15 | `RETRIEVE_BEARING_PLATE_ASSEMBLY` | Retrieve the bearing-plate assembly from a storage/location state. | Bearing-plate assembly | No direct PSR retrieve/location state | Not characterized from the inspected examples | Auxiliary / preparatory action | DG + INT; workflow role HUMAN |
| 16 | `RETRIEVE_LOCKING_LEVER_ASSEMBLY` | Retrieve the locking-lever assembly from a storage/location state. | Locking-lever assembly | No direct PSR retrieve/location state | Not characterized from the inspected examples | Auxiliary / preparatory action | DG + INT; workflow role HUMAN |
| 17 | `STORE_TOOL` | Move/store a tool. Exact tool identity is not encoded in this coarse TAS-S label name. | Tool (unspecified) | Not represented as one of the 17 PSR component instances | Not characterized from the inspected examples | Auxiliary / logistics action | DG + INT; workflow role HUMAN |

### B2. Critical semantic interpretation rule

The official release does **not** give us a normative statement such as:

> "`REMOVE_LOCKING_LEVER_ASSEMBLY` = one mandatory procedure step that must occur exactly once."

It gives us a coarse TAS-S annotation class.

Therefore the following fields must remain human-owned:

- mandatory / optional / conditional / out-of-scope;
- exact workflow acceptance condition;
- legal order relative to other coarse actions;
- repeat limit;
- recovery/rework interpretation;
- restart semantics;
- completion contribution.

---

# C. Semantic classification

The following classification is a **descriptive project proposal**, not official IMPACT ground truth.

| Action | Proposed primary category | Why |
|---|---|---|
| `START_ANGLE_GRINDER_ASSEMBLY` | auxiliary_action / procedure_boundary | Marks the beginning of an annotated coarse procedure interval rather than a PSR component transition. |
| `UNSCREW_ANTI_VIBRATION_HANDLE` | state_change_action | A mechanical loosening operation on a named component, but exact state transition is not directly defined by TAS-S. |
| `STORE_ANTI_VIBRATION_HANDLE` | auxiliary_action | Location/logistics action; PSR does not encode storage location. |
| `REMOVE_LOCKING_LEVER_ASSEMBLY` | state_change_action | Directly aligned with multiple PSR component removals in inspected data. |
| `STORE_LOCKING_LEVER_ASSEMBLY` | auxiliary_action | Location/logistics action. |
| `EXTRACT_BEARING_PLATE_ASSEMBLY` | state_change_action | Directly aligned with bearing plate/screw removal events in inspected data. |
| `STORE_BEARING_PLATE_ASSEMBLY` | auxiliary_action | Location/logistics action. |
| `DETACH_ADAPTER_PLATE` | state_change_action | Directly aligned with adapter-plate fastening/component removal events in inspected data. |
| `REMOVE_ROTOR_ASSEMBLY` | state_change_action | Directly aligned with rotor-related component removal events in inspected data. |
| `STORE_ROTOR_ASSEMBLY` | auxiliary_action | Location/logistics action. |
| `STORE_GEARBOX_HOUSING` | auxiliary_action | Location/logistics action; the PSR removal event is separate. |
| `STORE_ADAPTER_PLATE` | auxiliary_action | Location/logistics action. |
| `INSTALL_ROTOR_ASSEMBLY` | state_change_action | Opposite-direction assembly/reinstallation semantics are explicit in the TAS-S class name; exact PSR grouping requires human validation. |
| `ATTACH_ADAPTER_PLATE` | state_change_action | Attachment/reinstallation semantics are explicit in the class name; exact PSR grouping requires human validation. |
| `RETRIEVE_BEARING_PLATE_ASSEMBLY` | auxiliary_action | Retrieval/logistics action. |
| `RETRIEVE_LOCKING_LEVER_ASSEMBLY` | auxiliary_action | Retrieval/logistics action. |
| `STORE_TOOL` | auxiliary_action | Tool handling/location action, not represented by a PSR component state. |

### Categories deliberately NOT assigned automatically

`required_procedural_action`, `optional_action`, `condition_dependent_action`, `recovery_action`, `corrective_action`, `anomaly_related_action`, and `completion_action` are **workflow-policy meanings**, not safely inferable from the TAS-S label name alone.

---

# D. Component / state mapping

## D1. Official PSR component vocabulary

The released PSR component instances are:

1. `anti_vibration_handle`
2. `gearbox_housing`
3. `drive_shaft`
4. `bevel_gear`
5. `adapter_plate`
6. `bearing_plate`
7. `screw_lever`
8. `screw_adaptor_topleft`
9. `screw_adaptor_lowright`
10. `bearing_screw_topleft`
11. `bearing_screw_lowright`
12. `M4_nut_plate_topleft`
13. `M4_nut_plate_lowright`
14. `spring`
15. `lever`
16. `washer`
17. `M6_nut`

PSR metadata defines 51 procedure-state categories around these components: install / incorrectly-installed / remove variants.

## D2. High-confidence coarse-to-fine correspondences

### Locking lever assembly

`REMOVE_LOCKING_LEVER_ASSEMBLY`

Observed direct PSR alignment in `LE06AS03_Disassembly_A_001_front`:

- `Remove screw_lever`
- `Remove spring`
- `Remove lever`
- `Remove washer`

All four PSR events occur at the same recorded transition time (`1293.jpg`) while the TAS-S coarse label spans the surrounding interval.

**Status:** `DO + strong INT`  
**Human decision still required:** whether this mapping should be treated as the canonical semantic decomposition for workflow acceptance.

### Bearing plate assembly

`EXTRACT_BEARING_PLATE_ASSEMBLY`

Observed direct PSR alignment:

- `Remove bearing_plate`
- `Remove bearing_screw_lowright`
- `Remove bearing_screw_topleft`

at the corresponding coarse TAS-S intervals.

**Status:** `DO + strong INT`  
**Human decision still required:** whether all three are required evidence for accepting the coarse action or whether the coarse action may be accepted from a higher-level visual event.

### Adapter plate assembly

`DETACH_ADAPTER_PLATE`

Observed direct PSR alignment:

- `Remove adapter_plate`
- `Remove screw_adaptor_lowright`
- `Remove M4_nut_plate_lowright`
- later: `Remove screw_adaptor_topleft`
- later: `Remove M4_nut_plate_topleft`

**Status:** `DO + strong INT`  
**Important:** the coarse TAS-S label spans more than one fine-grained state-changing event. Do not force a one-to-one mapping.

### Rotor assembly

`REMOVE_ROTOR_ASSEMBLY`

Observed direct PSR alignment:

- `Remove drive_shaft`
- `Remove bevel_gear`
- `Remove M6_nut`

**Status:** `DO + strong INT`  
**Human decision still required:** whether the project workflow treats these three component states as the acceptance decomposition of `REMOVE_ROTOR_ASSEMBLY`.

### Gearbox housing

`STORE_GEARBOX_HOUSING`

PSR contains a distinct:

- `Remove gearbox_housing`

The observed TAS-S STORE event occurs later than the PSR remove event in the inspected execution.

**Conclusion:** the TAS-S STORE event must **not** be interpreted as the PSR state transition itself.

---

# E. Ordering constraints

## E1. Official structural fact

IMPACT explicitly states that PSR handles **non-unique valid orders** using a prerequisite graph. The released graph metadata says its edges are robust prerequisites mined from data, and a missing edge means flexible ordering.

**This is a PSR component-state graph, not a TAS-S route specification.**

The released graph should therefore be treated as an evidence source for component-state structure, not copied verbatim into the TAS-S workflow.

## E2. Direct TAS-S evidence against a single fixed sequence

The inspected released TAS-S annotations demonstrate different coarse action orders.

Example 1 — `LE06AS03_Disassembly_A_001_front`:

- `REMOVE_LOCKING_LEVER_ASSEMBLY`
- then `EXTRACT_BEARING_PLATE_ASSEMBLY`

Example 2 — `SS07EL13_Disassembly_A_001_front`:

- `EXTRACT_BEARING_PLATE_ASSEMBLY`
- then `REMOVE_LOCKING_LEVER_ASSEMBLY`

Therefore:

`REMOVE_LOCKING_LEVER_ASSEMBLY` and `EXTRACT_BEARING_PLATE_ASSEMBLY` cannot be declared a fixed total-order pair from the annotation data.

Another observed variation:

- `LE06AS03_Disassembly_A_001_front`: `DETACH_ADAPTER_PLATE` precedes the main `REMOVE_ROTOR_ASSEMBLY` interval.
- `SS07EL13_Disassembly_A_002_front`: a `REMOVE_ROTOR_ASSEMBLY` interval appears before `DETACH_ADAPTER_PLATE`.

Therefore the pair also must not be encoded as an unconditional total order solely from observed annotations.

## E3. Repeat behavior is observed

Repeated coarse TAS-S segments occur in real annotations, including:

- repeated `REMOVE_LOCKING_LEVER_ASSEMBLY`;
- repeated `EXTRACT_BEARING_PLATE_ASSEMBLY`;
- repeated `DETACH_ADAPTER_PLATE`;
- repeated `REMOVE_ROTOR_ASSEMBLY`;
- repeated storage actions.

### Important conclusion

`Repeated observation ≠ officially allowed repeat`.

It only proves that repetition exists in the released data. Whether repetition means:

- legitimate repeat,
- rework,
- correction,
- recovery,
- annotation fragmentation,
- or an anomalous action

must be decided semantically.

## E4. Required human decisions

The following remain unresolved:

- Which action pairs have true prerequisites.
- Which pairs are intentionally flexible.
- Which actions are optional.
- Which actions are conditional.
- Which repeats are legal.
- Which repeated segments indicate recovery/rework.
- Whether any action may be repeated indefinitely or only until a state condition is satisfied.
- Whether an out-of-order action should be called an invalid transition or a legitimate alternative route.

---

# F. Repeat / recovery / rework / restart

## F1. What the dataset establishes

The official IMPACT benchmark includes explicit `NORMAL`, `ANOMALY`, and `RECOVERY` phase labels at the bimanual procedural-phase level. The paper defines recovery as behavior that resolves a preceding anomaly.

This establishes that recovery is a first-class dataset concept.

## F2. What the dataset does NOT establish automatically

It does not provide a universal rule of:

`TAS-S action X = recovery`

nor:

`Repeated TAS-S action X = mistake`.

The coarse action layer and the anomaly/recovery layer are separate annotation levels.

## F3. Human decisions required

For each repeated/reinstalled/retrieved action, determine whether it is:

- allowed repeat;
- corrective action;
- recovery action;
- rework;
- branch/alternative route;
- anomaly-related;
- restart/reset;
- or unknown.

`Deviation != Mistake` remains a project invariant.

---

# G. Completion criterion

## Source-grounded status

The official TAS-S vocabulary includes a `FINISH_ANGLE_GRINDER_ASSEMBLY` class, but this project slice's observed 17-action vocabulary does not include it.

Therefore:

- it is unsafe to infer completion from “the last observed 17-action label”;
- it is unsafe to define completion simply as “video ended”;
- it is unsafe to import a fixed terminal route from action frequency.

### Current entry

```text
completion.condition: HUMAN_REQUIRED
completion.terminal_paths: HUMAN_REQUIRED
```

### What the human owner must decide

Choose a rule such as:

- all required coarse actions accepted;
- required final component states satisfied;
- an explicit terminal action observed;
- or a combination.

The chosen rule must be documented as a project interpretation, not presented as official IMPACT ground truth unless a source explicitly supports it.

---

# H. Evidence / uncertainty policy

## H1. Dataset fact

TAS-S provides a coarse procedural label per frame. IMPACT explicitly addresses partial observability and synchronized multi-view observation.

## H2. What is not supplied as a universal rule

The release does not define the project's production-style threshold for:

- sufficient visual evidence;
- ambiguous action;
- occluded action;
- out-of-view action;
- model-confidence acceptance;
- cross-view evidence fusion;
- minimum evidence duration.

## H3. Recommended engineering interpretation for this project

Keep these concepts separate:

```text
Model confidence
        ≠
Visual evidence sufficiency
        ≠
Workflow acceptance
        ≠
Process compliance
```

An observed ActionEvent should remain auditable even if evidence is uncertain.

The workflow state should advance only when the approved evidence policy says the observation is sufficient.

This is an engineering rule already implemented in CP07.1; it is not claimed as an IMPACT ground-truth rule.

### Human decisions required

Confirm:

1. what evidence is sufficient for each coarse action;
2. whether one view is enough;
3. whether multiple views can jointly establish an event;
4. how to treat full/partial occlusion;
5. whether `UNKNOWN` and `AMBIGUOUS` are non-violating states;
6. how out-of-view actions are handled;
7. whether insufficient evidence blocks workflow progress without declaring a process violation.

---

# I. Timing policy

## Current evidence status

No authoritative per-action duration threshold has been identified in the checked public IMPACT benchmark protocol, TAS-S mapping, PSR metadata, or workflow-related release material.

Therefore:

```yaml
timeout_policy:
  enabled: false
  seconds: null

duration_policy:
  enabled: false
  source: null
  rules: {}
```

### Do NOT derive timing rules from observed video durations

A duration measured from the released dataset can be used for:

- descriptive statistics;
- experimental analysis;
- model debugging.

It should not automatically become an authoritative process limit.

### Human decision

Only define timing thresholds if a valid source exists, such as:

- process owner specification;
- industrial SOP;
- manufacturer procedure;
- experimentally pre-registered engineering criterion.

---

# J. Human validation gate

## Current status

`HUMAN_REVIEW_REQUIRED`

## Required before `HUMAN_VALIDATED`

The owner must explicitly confirm/reject:

### Action-level decisions
- exact meaning of each ambiguous/high-level action;
- required / optional / conditional / out-of-scope status;
- whether logistics actions count as workflow steps.

### State-level decisions
- exact TAS-S → PSR component mapping;
- which state transition is required for acceptance;
- whether a coarse action may be accepted without all lower-level state events.

### Workflow-level decisions
- mandatory action set;
- prerequisite relations;
- valid flexible orders;
- conditional branches;
- repeat policy;
- rework/recovery policy;
- restart policy;
- completion condition.

### Evidence-level decisions
- sufficient evidence;
- ambiguous/unknown handling;
- out-of-view handling;
- cross-view evidence rule.

### Timing-level decisions
- whether authoritative duration/timeout rules exist.

### Governance
- `approved_by`;
- `approved_on`;
- specification version;
- final semantic review statement.

---

# K. Current unresolved human decisions — reduced to explicit questions

This list is intentionally the **smallest useful human workload**. The project owner does not need to rediscover the dataset. The owner only needs to approve/reject the evidence-backed interpretation.

| ID | Question | Current evidence | Human answer needed |
|---|---|---|---|
| H1 | Is `START_ANGLE_GRINDER_ASSEMBLY` only a procedure-start marker, rather than a physical assembly step? | Label name + TAS-S role | YES / NO / CLARIFY |
| H2 | Is `UNSCREW_ANTI_VIBRATION_HANDLE` accepted as a genuine mechanical state-changing step, and is it mandatory? | Label name + PSR handle component exists | YES / NO / CLARIFY |
| H3 | Are the STORE actions formal workflow steps or only auxiliary logistics? | TAS-S label names; no PSR storage state | STEP / AUXILIARY / CONTEXT-DEPENDENT |
| H4 | Does `REMOVE_LOCKING_LEVER_ASSEMBLY` semantically correspond to the four PSR removals: screw_lever + spring + lever + washer? | Direct cross-annotation evidence | APPROVE / MODIFY |
| H5 | Does `EXTRACT_BEARING_PLATE_ASSEMBLY` correspond to bearing_plate + two bearing screws? | Direct cross-annotation evidence | APPROVE / MODIFY |
| H6 | Does `DETACH_ADAPTER_PLATE` correspond to adapter_plate + four associated fastener/nut state changes? | Direct cross-annotation evidence | APPROVE / MODIFY |
| H7 | Does `REMOVE_ROTOR_ASSEMBLY` correspond to drive_shaft + bevel_gear + M6_nut? | Direct cross-annotation evidence | APPROVE / MODIFY |
| H8 | Are INSTALL/ATTACH actions normal steps in `Disassembly_A`, or only rework/recovery/conditional paths? | Label semantics + separate recovery annotations | HUMAN |
| H9 | Are RETRIEVE actions normal logistics, recovery, or conditional actions? | Label semantics; no PSR retrieve state | HUMAN |
| H10 | Which action pairs have real prerequisites? | Dataset proves non-unique order; PSR graph is separate | HUMAN |
| H11 | Which repeats are legal? | Repetition is directly observed | HUMAN |
| H12 | What constitutes recovery/rework? | PPR explicitly has recovery, but coarse mapping is separate | HUMAN |
| H13 | What constitutes restart? | Not defined in checked benchmark sources | HUMAN |
| H14 | What constitutes procedure completion? | Official TAS-S has a finish class, but current subset does not contain it | HUMAN |
| H15 | What evidence is sufficient for workflow advancement? | Not defined by benchmark as project policy | HUMAN |
| H16 | What happens when evidence is insufficient/ambiguous/out-of-view? | Engineering architecture prepared in CP07.1 | HUMAN |
| H17 | Is there an authoritative duration/timeout rule? | None identified in checked public release material | HUMAN / NONE |

---

# L. Proposed final semantic model after human approval

The approved workflow should conceptually be:

```text
TAS-S ActionEvent
        │
        ├── observation identity
        ├── confidence
        ├── evidence sufficiency
        └── temporal interval
                │
                ▼
        semantic action mapping
                │
                ▼
        component/state interpretation
                │
                ▼
       prerequisite / partial-order logic
                │
                ▼
        accepted workflow state
                │
        ┌───────┴────────┐
        ▼                ▼
   process progress   violation / uncertainty
        │                │
        └───────┬────────┘
                ▼
        evidence-backed trace
```

The AI perception layer should not own SOP semantics. The workflow specification should remain explicit, auditable, configurable, and versioned.

---

# M. Final status for CP08

```text
CP07.1
PASS / HARDENING COMPLETE

Human Semantic Worksheet
SOURCE-GROUNDED DRAFT COMPLETE

Human Semantic Validation
PENDING

Executable Disassembly_A workflow
NOT APPROVED

Process compliance metrics
NOT EVALUATED

CP08
PENDING HUMAN SEMANTIC GATE
```

## M1. What has already been solved by research / source extraction

- official TAS-S vocabulary;
- official PSR component vocabulary;
- official PSR state categories;
- official PSR prerequisite-graph semantics;
- direct coarse-to-fine mapping evidence for the main assembly groups;
- direct evidence that the observed TAS-S order is not a single fixed total sequence;
- direct evidence that some actions repeat;
- official existence and definition of anomaly/recovery phase annotations;
- absence of an identified authoritative timing rule in the checked public benchmark release.

## M2. What must still be decided by the project owner

- normative workflow semantics;
- mandatory/optional/conditional status;
- exact prerequisite graph for the project's TAS-S workflow;
- legal repeats and recovery/rework behavior;
- restart semantics;
- completion condition;
- evidence-sufficiency policy;
- final approval identity/version/date.

---

# N. Sources used

## Primary IMPACT sources

1. Official IMPACT repository.
2. Official `dataset/TAS/mapping_TAS-S.txt`.
3. Official TAS-S ground-truth files under `dataset/TAS/groundTruth_TAS-S/`.
4. Official `dataset/PSR/labels/component_names.json`.
5. Official `dataset/PSR/labels/procedure_info_IMPACT.json`.
6. Official PSR example labels under `dataset/PSR/labels/.../*/PSR_labels.csv`.
7. Official `tasks/PSR/gemini_3_1_pro/configs/procedure_graph.json`.
8. Official `dataset/PPR/mapping_PPR.txt`.
9. Official benchmark protocol `docs/BENCHMARK.md`.
10. Official v1.1 release/changelog documentation.

## Academic source

Wen et al., “IMPACT: A Dataset for Multi-Granularity Human Procedural Action Understanding in Industrial Assembly”, arXiv:2604.10409 (2026).

---

# O. Review notation

Use the following when the human owner reviews a row:

- `APPROVE` — evidence-backed interpretation accepted.
- `MODIFY` — interpretation needs correction.
- `UNKNOWN` — source is insufficient and no rule should be invented.
- `OUT_OF_SCOPE` — action exists in TAS-S but is not part of the selected workflow policy.
- `HUMAN_POLICY` — decision is project/process policy, not dataset ground truth.
- `SOURCE_GAP` — public release checked but no authoritative statement located.

**Do not set `HUMAN_VALIDATED` until all required decisions are resolved.**
