# CP08 Human Handoff — Research Workflow Specification

Status: **HUMAN_REVIEW_REQUIRED**. This request is for a **Research Workflow Specification / Benchmark Procedure Interpretation** for IMPACT v1.1 TAS-S `Disassembly_A`, `front`. It is not an official factory SOP. Do not mark the file human validated until the project owner/process owner has reviewed the semantics.

## Why a human decision is required

The official TAS-S class vocabulary identifies labeled actions, but does not by itself define which are mandatory, the accepted ordering, recovery/restart/completion semantics, or which video observations certify component state. The official PSR prerequisite graph is a different task and cannot be copied as this workflow. The research reconstruction worksheet contains proposals, not human approval. Codex has kept all action mappings non-executable.

## Exact task

1. Open `HumanSemanticWorksheet.md` and make semantic decisions there. This file is human-owned; Codex will not prefill it.
2. Use the scoped action IDs listed below. For every ID choose a workflow disposition and state whether any physical state effect is actually established by the visible action. Mark unsupported meanings `unknown`.
3. Complete the YAML response form below and save it as `configs/workflows/disassembly_A.yaml` only after review. Keep `status: HUMAN_REVIEW_REQUIRED` until the project owner explicitly approves it; approval metadata must identify reviewer and review date. Do not call it an official SOP.
4. Leave duration and timeout policies disabled unless an authoritative source supplies a rule. Experiment convenience thresholds are not policy.
5. Return any source citation used for a decision (document path/page/section or dataset release URL/page). If the source does not decide a field, mark `unknown` rather than infer from annotation counts or observed order.

## Decisions to provide

For each scoped action, select one disposition: `required`, `optional`, `conditional`, `rework_only`, `auxiliary`, `out_of_scope`, or `unknown`. These are workflow roles, not model labels.

Resolve the following explicitly:

- Whether `START_ANGLE_GRINDER_ASSEMBLY` is a boundary marker, required step, or out of scope.
- Whether `UNSCREW_ANTI_VIBRATION_HANDLE` means only loosening or certifies detachment; identify any separate evidence needed.
- Whether `REMOVE_LOCKING_LEVER_ASSEMBLY`, `EXTRACT_BEARING_PLATE_ASSEMBLY`, `DETACH_ADAPTER_PLATE`, and `REMOVE_ROTOR_ASSEMBLY` establish only labeled actions or approved component state effects. List component mappings only when supported.
- Treat each `STORE_*` action as storage/location unless you explicitly approve a sourced state bridge. In particular decide whether the procedure objective involving gearbox removal is unobservable/unknown from `STORE_GEARBOX_HOUSING` alone.
- Decide roles for `INSTALL_ROTOR_ASSEMBLY`, `ATTACH_ADAPTER_PLATE`, `RETRIEVE_BEARING_PLATE_ASSEMBLY`, `RETRIEVE_LOCKING_LEVER_ASSEMBLY`, and `STORE_TOOL`; do not assume they are mandatory or recovery.
- Define required action set, prerequisite relations/valid alternate orders, conditional branch guards, repeats, recovery/rework, reset/restart, and terminal completion.
- Define what happens on `unknown`, `ambiguous`, out-of-view, or insufficient evidence. Do not use model confidence as evidence sufficiency without a separately validated policy.
- Specify evidence requirements and whether a process can be marked complete when an objective is not visually certifiable.
- Confirm timing policy. Default is disabled; observed duration is descriptive only.

The following annotation observations are supplied only as descriptive context, not as rule suggestions: observed order varies for multiple action pairs, and repeated action labels occur. They must not be used alone to establish mandatory order or mistake/recovery meaning.

## YAML response form

Copy the following structure into the response file. Replace every `REQUIRED_HUMAN_VALUE` and explicitly fill `unknown` when evidence is unavailable. `action_dispositions` must contain all 17 IDs listed below. `prerequisites` may be empty only if the reviewer confirms that no required ordering constraints are established. This form is a review request, not a valid executable schema until checked by the repository validator.

```yaml
workflow:
  id: IMPACT-v1.1-TAS-S-Disassembly_A-front
  artifact_type: Research Workflow Specification / Benchmark Procedure Interpretation
  status: HUMAN_REVIEW_REQUIRED
  enabled: false
  reviewer: REQUIRED_HUMAN_VALUE
  review_date: REQUIRED_HUMAN_VALUE
  source_citations:
    - REQUIRED_HUMAN_VALUE
  action_dispositions:
    START_ANGLE_GRINDER_ASSEMBLY: REQUIRED_HUMAN_VALUE
    UNSCREW_ANTI_VIBRATION_HANDLE: REQUIRED_HUMAN_VALUE
    STORE_ANTI_VIBRATION_HANDLE: REQUIRED_HUMAN_VALUE
    REMOVE_LOCKING_LEVER_ASSEMBLY: REQUIRED_HUMAN_VALUE
    STORE_LOCKING_LEVER_ASSEMBLY: REQUIRED_HUMAN_VALUE
    EXTRACT_BEARING_PLATE_ASSEMBLY: REQUIRED_HUMAN_VALUE
    STORE_BEARING_PLATE_ASSEMBLY: REQUIRED_HUMAN_VALUE
    DETACH_ADAPTER_PLATE: REQUIRED_HUMAN_VALUE
    REMOVE_ROTOR_ASSEMBLY: REQUIRED_HUMAN_VALUE
    STORE_ROTOR_ASSEMBLY: REQUIRED_HUMAN_VALUE
    STORE_GEARBOX_HOUSING: REQUIRED_HUMAN_VALUE
    STORE_ADAPTER_PLATE: REQUIRED_HUMAN_VALUE
    INSTALL_ROTOR_ASSEMBLY: REQUIRED_HUMAN_VALUE
    ATTACH_ADAPTER_PLATE: REQUIRED_HUMAN_VALUE
    RETRIEVE_BEARING_PLATE_ASSEMBLY: REQUIRED_HUMAN_VALUE
    RETRIEVE_LOCKING_LEVER_ASSEMBLY: REQUIRED_HUMAN_VALUE
    STORE_TOOL: REQUIRED_HUMAN_VALUE
  required_actions: [REQUIRED_HUMAN_VALUE]
  prerequisites: {}
  conditional_branches: []
  repeat_policy:
    decision: REQUIRED_HUMAN_VALUE
    allowed_actions: []
    max_repeats: unknown
  recovery_policy:
    decision: REQUIRED_HUMAN_VALUE
    transitions: []
  restart_policy: REQUIRED_HUMAN_VALUE
  completion:
    condition: REQUIRED_HUMAN_VALUE
    unobservable_objective_behavior: REQUIRED_HUMAN_VALUE
  uncertainty_policy:
    unknown_action: REQUIRED_HUMAN_VALUE
    ambiguous_action: REQUIRED_HUMAN_VALUE
    out_of_view: REQUIRED_HUMAN_VALUE
    insufficient_evidence: REQUIRED_HUMAN_VALUE
  evidence_policy:
    required_references: REQUIRED_HUMAN_VALUE
    sufficiency_rule: REQUIRED_HUMAN_VALUE
  timing:
    timeout:
      enabled: false
      source: unknown
      rule: unknown
    duration_limits_seconds: {}
```

### Field status

- **Required human decisions:** reviewer/date; citations; all 17 dispositions; required actions; prerequisites/order; branch semantics; repeat/recovery/restart; completion; uncertainty/evidence behavior.
- **Optional:** conditional branches, repeat limits, explicit component state effects and evidence references, but if absent they must remain unsupported/unknown rather than guessed.
- **Not defined by inspected sources:** timing thresholds, confidence calibration, event-level process-violation ground truth for this test subset. Keep timing disabled and process performance `NOT_EVALUATED` absent a valid source/policy.
- **Human approval required:** `status: HUMAN_VALIDATED` and `enabled: true` must only be set by the owner after reviewing all fields and validating the resulting YAML. Codex should not promote this template.

## Validation and resume point

Provide the completed candidate at `configs/workflows/disassembly_A.yaml`. Then run `python tools/validate_workflow.py --config configs/workflows/disassembly_A.yaml`; resolve every validation error with the reviewer, not by weakening the validator. Resume CP08 at workflow validation, synthetic golden tests, then frozen ActionEvent trace generation. Do not produce process accuracy/violation metrics without matching semantically valid process ground truth.
