# IMPACT Disassembly_A

## Human Semantic Grounding Worksheet

### Research Workflow Specification / Benchmark Procedure Interpretation

> This document is a human semantic review artifact.
> It is NOT an official factory SOP.
> It must not infer normative process rules solely from observed TAS-S frequency or model predictions.

---

## A. Procedure Scope

Dataset:
IMPACT v1.1

Task:
TAS-S

Procedure:
Disassembly_A

View:
front

Split:
S2

Purpose:
Define the semantics required to connect observed TAS-S ActionEvents to a research workflow/process interpretation.

---

## B. Action Semantic Review

For every action below, fill only what can be supported by source documentation and/or direct video review.

| Action                          | Plain-language meaning | Component / object affected | Procedural role | State effect | Repeat allowed? | Recovery-related? | Evidence/source | Reviewer confidence |
| ------------------------------- | ---------------------- | --------------------------- | --------------- | ------------ | --------------- | ----------------- | --------------- | ------------------- |
| START_ANGLE_GRINDER_ASSEMBLY    |                        |                             |                 |              |                 |                   |                 |                     |
| UNSCREW_ANTI_VIBRATION_HANDLE   |                        |                             |                 |              |                 |                   |                 |                     |
| STORE_ANTI_VIBRATION_HANDLE     |                        |                             |                 |              |                 |                   |                 |                     |
| REMOVE_LOCKING_LEVER_ASSEMBLY   |                        |                             |                 |              |                 |                   |                 |                     |
| STORE_LOCKING_LEVER_ASSEMBLY    |                        |                             |                 |              |                 |                   |                 |                     |
| EXTRACT_BEARING_PLATE_ASSEMBLY  |                        |                             |                 |              |                 |                   |                 |                     |
| STORE_BEARING_PLATE_ASSEMBLY    |                        |                             |                 |              |                 |                   |                 |                     |
| DETACH_ADAPTER_PLATE            |                        |                             |                 |              |                 |                   |                 |                     |
| REMOVE_ROTOR_ASSEMBLY           |                        |                             |                 |              |                 |                   |                 |                     |
| STORE_ROTOR_ASSEMBLY            |                        |                             |                 |              |                 |                   |                 |                     |
| STORE_GEARBOX_HOUSING           |                        |                             |                 |              |                 |                   |                 |                     |
| STORE_ADAPTER_PLATE             |                        |                             |                 |              |                 |                   |                 |                     |
| INSTALL_ROTOR_ASSEMBLY          |                        |                             |                 |              |                 |                   |                 |                     |
| ATTACH_ADAPTER_PLATE            |                        |                             |                 |              |                 |                   |                 |                     |
| RETRIEVE_BEARING_PLATE_ASSEMBLY |                        |                             |                 |              |                 |                   |                 |                     |
| RETRIEVE_LOCKING_LEVER_ASSEMBLY |                        |                             |                 |              |                 |                   |                 |                     |
| STORE_TOOL                      |                        |                             |                 |              |                 |                   |                 |                     |

---

## C. Semantic Classification

For each action, classify its role using exactly one primary category:

* required_procedural_action
* auxiliary_action
* completion_action
* state_change_action
* recovery_action
* corrective_action
* optional_action
* condition_dependent_action
* anomaly_related_action
* unknown

Action:

`_______________________________`

Primary category:

`_______________________________`

Reason:

`_______________________________`

Evidence:

`_______________________________`

---

## D. Component / State Mapping

Only fill when the relationship is semantically clear.

| TAS-S action | PSR component/event potentially related | Confidence | Evidence |
| ------------ | --------------------------------------- | ---------: | -------- |
|              |                                         |            |          |
|              |                                         |            |          |
|              |                                         |            |          |
|              |                                         |            |          |

Do NOT force a one-to-one mapping.

One TAS-S action may affect multiple components.
One component state may require several TAS-S actions.

---

## E. Ordering Constraints

Do NOT enter a complete sequence.

Enter only constraints that are actually justified.

| Constraint                        | Type           | Evidence | Confidence |
| --------------------------------- | -------------- | -------- | ---------: |
| A must precede B                  | prerequisite   |          |            |
| A must precede B                  | prerequisite   |          |            |
| A and B may occur in either order | flexible       |          |            |
| A may repeat before B             | repeat allowed |          |            |
| A is valid only after condition X | conditional    |          |            |

Allowed constraint types:

* prerequisite
* flexible
* optional
* conditional
* repeat
* recovery
* restart
* unknown

---

## F. Completion

What does “Disassembly_A completed” mean according to the available evidence?

Do not define completion from “last observed TAS-S label”.

Candidate evidence:

* PSR component completion state
* explicit FINISH label
* dataset documentation
* instruction/procedure document
* other authoritative source

Decision:

`____________________________________________`

Evidence:

`____________________________________________`

Confidence:

`HIGH / MEDIUM / LOW`

---

## G. Timing

Does the source provide an authoritative minimum/maximum action duration?

`YES / NO / UNKNOWN`

Source:

`____________________________________________`

If NO or UNKNOWN:

DO NOT define duration violations.

---

## H. Unknown / Ambiguous Evidence Policy

When the video does not provide sufficient visual evidence:

Choose:

* UNKNOWN
* AMBIGUOUS
* INSUFFICIENT_EVIDENCE
* HUMAN_REVIEW_REQUIRED

Decision:

`____________________________________________`

Reason:

`____________________________________________`

---

## I. Human Review Summary

Reviewed by:

`____________________________________________`

Date:

`____________________________________________`

Number of actions reviewed:

`____________________________________________`

Number with unresolved semantics:

`____________________________________________`

Major unresolved issues:

`____________________________________________`

---

## J. Final Semantic Gate

Do NOT approve executable workflow until all mandatory semantic questions are answered.

Workflow semantic status:

`HUMAN_REVIEW_REQUIRED`

or

`HUMAN_VALIDATED`

Validation notes:

`____________________________________________`
