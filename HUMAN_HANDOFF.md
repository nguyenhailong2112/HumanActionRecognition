# HUMAN ACTION REQUIRED — CP01.1 procedure validation

> **CP02 clarification:** IMPACT v1.1 does include PPR-L/R phase labels (`NORMAL`, `ANOMALY`, `RECOVERY`) and ATR annotations. These are real task-specific anomaly/phase annotations, but they are not SOP-grounded workflow labels for skip, wrong order, repeat, timeout, or compliance. See `HUMAN_HANDOFF_CP02.md` for the separate CP02 data and process handoff.

## Task

Approve the operational meaning and legal sequence for the single target procedure **IMPACT angle-grinder Disassembly A**. The current CP01 route is illustrative, is disabled in `configs/cp01_1.yaml`, and must not produce compliance claims.

## Why a human decision is required

TAS-S records observed action labels and their frame intervals; it does not define which order/repetition/recovery is allowed by the factory procedure. Several Disassembly A executions contain rare `RETRIEVE_*`, `INSTALL_ROTOR_ASSEMBLY`, or `ATTACH_ADAPTER_PLATE` observations. Treating them as errors from frequency or a guessed canonical order would make the evaluation ground truth circular and potentially wrong. No approved work instruction/SOP was present in this repository.

## Inputs

- Versioned, checksum-verified source: `data/raw/impact/v1.1/annotations/IMPACT-v1.1-annotations.zip`.
- Full per-execution audit and split status: `experiments/CP01.1/dataset_audit_CP01.1.csv` and `.md`.
- Official S2 test worker and executions are listed in `experiments/CP01.1/dataset_audit_CP01.1.json`.
- Official TAS-S mapping: `ResearchDocuments/01_IMPACT/code/IMPACT/dataset/TAS/mapping_TAS-S.txt`.
- Annotated example GT timelines: `results/cp01_1/ground_truth/*.svg`.
- Dataset has CC BY-NC-SA 4.0 terms and is for non-commercial research/education. Current local video availability is only 2/48 target trials; obtain process truth from the approved work instruction or process owner, not by guessing unseen footage.

## Exact human steps

1. Ask the angle-grinder Disassembly A process owner to provide or review the approved work instruction/version used by this dataset.
2. Review whether each observed TAS-S action below is a valid Disassembly A operation, a conditional/recovery operation, a label ambiguity, or out of scope. Do not infer “mistake” solely because an action is rare.
3. Give the ordered required steps and action labels. Mark each step required/optional/conditional, identify legal alternate paths, retries/rework, and the condition/transition that permits each alternative.
4. State how a procedure starts and completes. In particular, tell us whether `START_ANGLE_GRINDER_ASSEMBLY`/`FINISH_ANGLE_GRINDER_ASSEMBLY` are required in the operational Disassembly A process or only in another annotation context.
5. Give min/max duration bounds only if they come from an approved SOP or process-owner policy. Otherwise mark them `NOT SET`; we will not estimate thresholds from this tiny validation set.
6. Save the approved response as `configs/workflows/disassembly_A.yaml` using the schema below, and include SOP identifier/revision plus reviewer/date. If policy cannot be confirmed, save a short note stating what evidence/owner is missing; leave CP01.1 workflow disabled.

## Observed action inventory to classify

Labels are the official TAS-S vocabulary; number in parentheses is their count as annotated segments across the 48 selected front-view Disassembly A executions. `NULL` is background, not a procedure step.

- `START_ANGLE_GRINDER_ASSEMBLY` (48)
- `UNSCREW_ANTI_VIBRATION_HANDLE` (50)
- `STORE_ANTI_VIBRATION_HANDLE` (48)
- `REMOVE_LOCKING_LEVER_ASSEMBLY` (95)
- `STORE_LOCKING_LEVER_ASSEMBLY` (73)
- `EXTRACT_BEARING_PLATE_ASSEMBLY` (143)
- `STORE_BEARING_PLATE_ASSEMBLY` (107)
- `DETACH_ADAPTER_PLATE` (201)
- `REMOVE_ROTOR_ASSEMBLY` (184)
- `STORE_ROTOR_ASSEMBLY` (101)
- `STORE_GEARBOX_HOUSING` (40)
- `STORE_ADAPTER_PLATE` (134)
- `STORE_TOOL` (88)
- `RETRIEVE_BEARING_PLATE_ASSEMBLY` (1)
- `RETRIEVE_LOCKING_LEVER_ASSEMBLY` (3)
- `INSTALL_ROTOR_ASSEMBLY` (1)
- `ATTACH_ADAPTER_PLATE` (1)

## Required output format

Create `configs/workflows/disassembly_A.yaml`:

```yaml
workflow:
  id: angle_grinder_disassembly_A
  version: "<SOP ID and revision>"
  approved_by: "<process owner>"
  approved_on: "YYYY-MM-DD"
  procedure: Disassembly_A
  action_disposition:
    UNSCREW_ANTI_VIBRATION_HANDLE: {status: required}
    STORE_ANTI_VIBRATION_HANDLE: {status: required}
    # Include every observed action label from the inventory; each status is:
    # required | optional | conditional | rework | out_of_scope.
    RARE_LABEL_FROM_INVENTORY: {status: conditional, reason: "<SOP-backed condition>"}
  action_vocabulary: [<all in-scope action labels from the disposition map>]
  valid_paths:
    - id: canonical
      steps: [<ordered TAS-S action labels>]
    # Add an explicit alternate path only when the SOP allows it.
  optional_steps: [] # list step IDs only when policy permits skipping them
  conditional_transitions: [] # {from_step: ..., to_step: ..., condition: "SOP clause"}
  repeat_or_rework_rules: [] # bounded explicit repeats with their SOP trigger
  duration_limits_seconds: {}
```

Every label in the inventory must be classified as a required/optional/conditional/rework action, background, or explicitly out of scope with a reason. If time bounds are not approved, leave the duration map empty. If retries imply loops rather than a small list of paths, describe the bounded repeat rule in `repeat_or_rework_rules`; do not invent a large graph.

## Acceptance criteria

- The named SOP/revision and reviewer are recorded.
- The required order, completion condition and all legal variants are explicit.
- Every observed action label has a documented disposition.
- Every disposition is one of required/optional/conditional/rework/out_of_scope; conditional/out-of-scope entries cite a reason.
- Repeated/recovery actions are policy-backed; no frequency-based guess is used.
- Durations are either source-backed or explicitly unset.
- `tools/validate_workflow.py --config configs/workflows/disassembly_A.yaml` passes after the engineer resumes CP01.1.

## After completion

Resume CP01.1 by validating the YAML against the observed action vocabulary, enabling workflow evaluation only after review, adding legal/recovery workflow tests, and reporting process metrics only if matching ground-truth violation labels are available. No full manual video re-annotation is requested for the action baseline; review action boundaries only if the process owner finds concrete errors in the versioned TAS-S examples.
