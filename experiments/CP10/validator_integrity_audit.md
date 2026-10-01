# CP10 Validator Integrity Audit

## Scope layers

The validator's `action_vocabulary` parameter is the **supplied project/model action scope**, populated by CLI from the configured action class order with background removed. In this project that means 17 project model actions. The official IMPACT TAS-S mapping has 25 non-NULL actions plus NULL; the model scope must not be silently broadened. See `experiments/CP09/action_vocabulary_scope.json`.

Within that project/model scope, workflow semantics use two separate sets:

- `action_disposition`: classify every project/model action, including actions explicitly excluded from this workflow.
- `action_vocabulary`: list exactly the actions considered by the workflow: every project/model action whose disposition is not `out_of_scope`.

Thus:

```text
keys(action_disposition) = project_model_action_scope
set(action_vocabulary) = {a | disposition[a].status != out_of_scope}
```

Paths, prerequisites and other executable references remain restricted to `action_vocabulary`. Paths cannot use actions marked `out_of_scope`. Actions outside the supplied project/model scope remain invalid even if they exist in official TAS-S.

## Confirmed defect and minimal correction

The previous validator required complete dispositions for the model scope, rejected model actions omitted from `action_vocabulary` before considering their disposition, and separately required vocabulary to equal all non-`out_of_scope` actions. The early action subset check made a valid `out_of_scope` disposition impossible. CP10 retains complete disposition coverage, retains rejection of unknown/out-of-scope references, and directly checks vocabulary equality against the non-`out_of_scope` set. No other workflow rule was relaxed.

## Regression coverage

The synthetic valid case uses project scope A/B/C/D with required/optional/rework/out_of_scope dispositions and vocabulary A/B/C. It passes only when remaining approval, path, optional-step and completion metadata are valid. Regression cases reject: missing D disposition; D included in vocabulary; unknown X; path step D; and a known official TAS-S label that lies outside project model scope.

These are validator engineering fixtures only. Their synthetic `HUMAN_VALIDATED` metadata does not represent actual owner approval of `Disassembly_A`.

## Current workflow validation state

There is no `configs/workflows/disassembly_A.yaml`. The draft remains `HUMAN_REVIEW_REQUIRED` with empty transitions. Therefore the executable workflow validator is run against the draft only to confirm it fails safely; no `workflow_validation.json` or process trace is emitted. Human approval remains the controlling gate.
