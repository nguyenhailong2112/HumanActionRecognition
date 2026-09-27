# HUMAN HANDOFF — CP06 Research Workflow Specification

> **Superseded by CP07 for the current owner response.** Use the exact action disposition and YAML schema in `HUMAN_HANDOFF_CP07.md`; preserve this file as the CP06 handoff history.

**Purpose:** Complete a Research Workflow Specification / Benchmark Procedure Interpretation for IMPACT v1.1 `Disassembly_A`. This is not an official factory SOP. The dataset supplies annotated actions and separate PSR component prerequisites, but it does not establish all compliance semantics. Please use the artifact's authoritative procedure/source material and your domain judgment; do not infer order from model outputs or action frequency.

## Exact work requested

1. Review `configs/workflows/disassembly_A.draft.yaml` and `experiments/CP06/workflow_sources.md`.
2. For every non-background TAS-S action, assign its process meaning/status under `action_disposition`: `required`, `optional`, `conditional`, `rework`, or `out_of_scope`. `action_vocabulary` lists only actions kept in executable routes (exclude those marked `out_of_scope`). If a label cannot be interpreted, use `UNKNOWN` in its `meaning` and explain it; do not guess.
3. Fill `configs/workflows/disassembly_A.yaml` using the schema below. Supply every mandatory field. Cite source/revision for each process rule. Use state IDs equal to their action IDs because the current approved-path engine consumes action-ID paths. `valid_paths.steps` must list action/state IDs. Represent conditional alternatives as named paths plus explicit condition text. Rework must be finite and explicit in paths; no implicit loop.
4. For timeout and duration, set `enabled: false` unless an authoritative source defines the rule. Do not create experimental timing thresholds.
5. Save the reviewed YAML at the exact output path above. Do not change TAS-S annotations or model evidence.

## YAML to complete

```yaml
workflow:
  artifact_type: Research Workflow Specification / Benchmark Procedure Interpretation
  status: HUMAN_VALIDATED
  procedure_id: Disassembly_A
  dataset_version: IMPACT v1.1
  task: TAS-S
  view: front
  version: "<source document revision or interpretation revision>"       # MANDATORY
  approved_by: "<reviewer name or project role>"                        # MANDATORY
  approved_on: "YYYY-MM-DD"                                             # MANDATORY
  source_refs:                                                           # MANDATORY
    - path: "<repository document or supplied source>"
      revision: "<revision/page/section>"
      supports: "<specific rule>"
  action_vocabulary: ["<applicable actions; exclude out_of_scope>"]     # MANDATORY
  action_disposition:                                                   # MANDATORY, one entry per non-background TAS-S action
    ACTION_ID:
      status: required  # required|optional|conditional|rework|out_of_scope
      meaning: "<procedure meaning; use UNKNOWN if unresolved>"
      source_ref: "<source_refs item or UNKNOWN>"
      condition: null # MANDATORY text when status is conditional; otherwise null
  states:                                                               # MANDATORY
    - id: "<unique state ID>"
      action: "<action ID>"
  start_state: "<state ID>"                                             # MANDATORY
  terminal_states: ["<state ID>"]                                       # MANDATORY
  transitions:                                                          # MANDATORY, [] only if no transition has been validated
    - from: "<state ID>"
      to: "<state ID>"
      conditional: false
      condition: null # required when conditional=true
      source_ref: "<source_refs item>"
  valid_paths:                                                          # MANDATORY; each route explicit
    - id: "<unique route ID>"
      steps: ["<state ID>"]
  optional_steps: []                                                     # OPTIONAL; every item must be disposition=optional
  conditional_paths: []                                                  # OPTIONAL; entries {path_id, condition_id, condition, source_ref}
  rework_paths: []                                                       # OPTIONAL; entries {path_id, condition, source_ref}
  restart_policy:                                                        # MANDATORY
    behavior: "<resume/restart/unknown and exact trigger>"
    source_ref: "<reference or UNKNOWN>"
  completion:                                                           # MANDATORY
    condition: "<observable completion condition or UNKNOWN>"
    source_ref: "<reference or UNKNOWN>"
  timeout_policy:                                                        # MANDATORY
    enabled: false
    seconds: null
    source: null
    behavior: "<disabled / source-backed timeout behavior>"
  duration_policy:                                                       # MANDATORY
    enabled: false
    rules: {}
    source: null
    behavior: "<report-only / source-backed rule>"
  evidence_requirements:                                                 # MANDATORY
    required: "<evidence needed to support a decision or UNKNOWN>"
    source_ref: "<reference or UNKNOWN>"
  uncertainty_policy:                                                    # MANDATORY
    unknown_action: "<hold/review behavior>"
    ambiguous_evidence: "<hold/review behavior>"
    insufficient_evidence: "<hold/review behavior>"
    out_of_view: "<hold/review behavior>"
    source_ref: "<reference or HUMAN_DECISION>"
```

## Mandatory / optional / unavailable

- **Mandatory:** all fields marked `MANDATORY`; per-action disposition and meaning; explicit route and branch/rework rules; source for every process rule; completion/restart/uncertainty behavior.
- **Optional:** optional/conditional/rework path collections may be empty only when the reviewer confirms none apply or cannot be established; record unknowns explicitly.
- **Unavailable from current dataset docs:** authoritative compliance ordering, completion, restart, timeout/duration thresholds, and evidence policy. These remain UNKNOWN until you supply an interpretation/source. No timing threshold is requested unless officially defined.

## Validation / resume

Run from project root:

```powershell
.\.venv-cp05\Scripts\python.exe tools\validate_workflow.py --config configs\workflows\disassembly_A.yaml --actions-config configs\cp05.yaml
```

The validator must report no errors. Send the saved YAML back in this repository. Resume point: validate the approved state/transition/path structure, run synthetic golden tests, and only then produce workflow traces from actual held-out CP05 ActionEvents. Until accepted and validated, process compliance stays **NOT EVALUATED**.
