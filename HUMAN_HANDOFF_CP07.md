# HUMAN HANDOFF — CP07 Research Workflow Specification

## Why this requires owner input

The repository identifies TAS-S actions and labels but does not specify which observed actions are mandatory, optional, conditional, recoverable, or acceptable in a process route. The IMPACT PSR graph is a separately mined component-state relation and is not an authoritative TAS-S compliance procedure. No executable `configs/workflows/disassembly_A.yaml` exists. Do not infer these rules from frequencies or model output.

The requested artifact is a **Research Workflow Specification / Benchmark Procedure Interpretation** for the IMPACT `Disassembly_A` benchmark. It is not an official factory SOP.

## Exact owner task

1. Open `configs/workflows/disassembly_A.draft.yaml` and `experiments/CP06/workflow_sources.md`.
2. Use authoritative procedure material where available. Fill in the YAML template below. For a fact not defined by a source, enter `null` and explain the gap under `unresolved`; do not invent a rule.
3. For action meaning/mapping, mark each released non-NULL TAS-S action as `required`, `optional`, `conditional`, `rework`, or `out_of_scope`. Give the source and your interpretation. If an action does not correspond to a workflow step, state that explicitly.
4. Enumerate each accepted route as ordered action IDs. Include optional and conditional routes explicitly. For each branch, provide a condition that can be decided from permitted evidence. List repeat/rework/restart behavior as explicit routes or policy objects.
5. Set `status: HUMAN_VALIDATED` only after reviewing every decision. Fill `approved_by`, `approved_on` (ISO date), `version`, and `completion.condition`. Otherwise keep `HUMAN_REVIEW_REQUIRED` and do not submit it as executable.
6. Save the completed candidate to `configs/workflows/disassembly_A.yaml`. Do not overwrite the draft.

## YAML response template

`REQUIRED` means CP07 validator requires a concrete value before activation. `OPTIONAL` may be omitted only if the behavior is unsupported/not defined. `HUMAN DECISION` must reflect your interpretation. `UNSUPPORTED / UNKNOWN` should remain `null` or disabled with a source-backed note; do not make up policy.

```yaml
workflow:
  artifact_type: Research Workflow Specification / Benchmark Procedure Interpretation
  status: HUMAN_REVIEW_REQUIRED # change to HUMAN_VALIDATED only after all decisions below
  enabled: false # REQUIRED boolean; only set true after human validation and validator PASS
  id: Disassembly_A
  version: REQUIRED # revision or source edition
  approved_by: REQUIRED HUMAN DECISION
  approved_on: REQUIRED YYYY-MM-DD
  source_references: REQUIRED # list of repository/external source + page/section; explain owner interpretation

  action_vocabulary: # REQUIRED; exact TAS-S non-NULL action IDs; remove any owner-classified out_of_scope action
    - START_ANGLE_GRINDER_ASSEMBLY
    - UNSCREW_ANTI_VIBRATION_HANDLE
    - STORE_ANTI_VIBRATION_HANDLE
    - REMOVE_LOCKING_LEVER_ASSEMBLY
    - STORE_LOCKING_LEVER_ASSEMBLY
    - EXTRACT_BEARING_PLATE_ASSEMBLY
    - STORE_BEARING_PLATE_ASSEMBLY
    - DETACH_ADAPTER_PLATE
    - REMOVE_ROTOR_ASSEMBLY
    - STORE_ROTOR_ASSEMBLY
    - STORE_GEARBOX_HOUSING
    - STORE_ADAPTER_PLATE
    - INSTALL_ROTOR_ASSEMBLY
    - ATTACH_ADAPTER_PLATE
    - RETRIEVE_BEARING_PLATE_ASSEMBLY
    - RETRIEVE_LOCKING_LEVER_ASSEMBLY
    - STORE_TOOL
  action_disposition: REQUIRED # fill status, meaning, source for every action
    START_ANGLE_GRINDER_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    UNSCREW_ANTI_VIBRATION_HANDLE: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    STORE_ANTI_VIBRATION_HANDLE: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    REMOVE_LOCKING_LEVER_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    STORE_LOCKING_LEVER_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    EXTRACT_BEARING_PLATE_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    STORE_BEARING_PLATE_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    DETACH_ADAPTER_PLATE: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    REMOVE_ROTOR_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    STORE_ROTOR_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    STORE_GEARBOX_HOUSING: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    STORE_ADAPTER_PLATE: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    INSTALL_ROTOR_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    ATTACH_ADAPTER_PLATE: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    RETRIEVE_BEARING_PLATE_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    RETRIEVE_LOCKING_LEVER_ASSEMBLY: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}
    STORE_TOOL: {status: HUMAN DECISION, meaning: HUMAN DECISION, source: HUMAN DECISION}

  valid_paths: REQUIRED # each route ordered; these are the executable semantics
    - id: HUMAN DECISION
      steps: [ACTION_ID, ACTION_ID]
  optional_steps: OPTIONAL # action IDs and the route(s) where omission is valid
  conditional_paths: OPTIONAL # path_id + condition_id + condition + permitted evidence
    - path_id: HUMAN DECISION
      condition_id: HUMAN DECISION
      condition: HUMAN DECISION
      evidence: HUMAN DECISION
  repeat_policy: REQUIRED # forbidden | bounded | allowed_until_condition; specify bound/condition
  rework_paths: OPTIONAL # explicit route IDs and re-entry state; null if unsupported/unknown
  restart_policy: REQUIRED # explicit reset trigger and state; null means owner says unknown
  completion:
    condition: REQUIRED HUMAN DECISION
    terminal_paths: REQUIRED # valid_path IDs that count as complete

  timeout_policy:
    enabled: false # keep false unless an authoritative timeout is defined
    seconds: null # UNSUPPORTED / UNKNOWN unless explicitly sourced
    source: null
  duration_policy:
    enabled: false # keep false unless official timing rule exists
    source: null
    rules: {} # action_id: {min: seconds, max: seconds}; no experimental thresholds
  uncertainty_policy: REQUIRED # behavior for unknown / ambiguous / out-of-view / low evidence
  evidence_requirements: REQUIRED # required evidence per decision, or explicitly none/unknown
  unresolved: [] # every source gap and ambiguity; use UNKNOWN / HUMAN REVIEW REQUIRED
```

## Exact output and validation

- Output path: `configs/workflows/disassembly_A.yaml`.
- Preserve `HUMAN_REVIEW_REQUIRED` if any mandatory field is undecided. Do not mark it validated merely to enable code execution.
- The implementation team will run `tools/validate_workflow.py`, report every validator error, and run workflow golden tests after receipt. A syntactically valid file is not enough: route/action mappings, branches, restart/completion, uncertainty, and evidence meaning need owner approval.
- Duration and timeout remain disabled unless an official source defines them. Unknown or camera-out-of-view actions must not become deviations by default.

Resume point: once the file exists, validate it, run golden tests, then decide whether actual frozen CP05 ActionEvents can be interpreted without test-set tuning. Until then, workflow semantics remain `HUMAN_REVIEW_REQUIRED` and process compliance remains `NOT_EVALUATED`.
