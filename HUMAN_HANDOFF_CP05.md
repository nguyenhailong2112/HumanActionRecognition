# HUMAN HANDOFF — CP05 Research Workflow Specification

> **Superseded by the more explicit CP07 template.** Use `HUMAN_HANDOFF_CP07.md` for current workflow fields and `HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md` for current selected event review.

## Task
Provide the process-owner interpretation of the public IMPACT Disassembly_A procedure as a **Research Workflow Specification / Benchmark Procedure Interpretation**. This is not an official factory SOP and will not be represented as one.

## Why human input is required
The TAS-S action labels and example executions do not define which actions are required, permitted, optional, conditional, or rework, nor the completion rule. The official IMPACT PSR graph is explicitly mined as robust component-state prerequisites and is used by a different benchmark task; it is not a canonical TAS-S action route or approved factory procedure. Inferring a mapping from it, action frequency, sequence statistics, model output, or one video would fabricate process policy.

## Exact input
Use the authoritative public procedure documentation or a process-owner-approved interpretation. Record document/source title, revision/date, owner/reviewer, and any interpretation that cannot be resolved from that artifact. Current TAS-S vocabulary is in `configs/cp05.yaml` under `actions.class_order`; `NULL` is background, not a workflow step.

## Exact steps
1. Create `configs/workflows/disassembly_A.yaml` from the repository's workflow template.
2. Name the workflow and cite the source/revision and interpretation owner.
3. Provide each step ID, its meaning, expected action mapping, and expected order.
4. Identify optional steps, conditional branches and their triggers, valid alternative paths, and allowed retry/rework paths. If the source does not establish a rule, write `UNKNOWN / HUMAN REVIEW REQUIRED` rather than guessing.
5. Define completion from the source/owner interpretation.
6. Add duration policy only if an official source specifies it; otherwise leave timing limits empty.
7. Give every non-background action in `configs/cp05.yaml` a disposition (`required`, `optional`, `conditional`, `rework`, or `out_of_scope`) and cite the basis for conditional/out-of-scope decisions.
8. Leave workflow disabled if any semantic item remains unresolved.

## Expected output
`configs/workflows/disassembly_A.yaml`, plus cited source and approval metadata in the file. Do not edit model labels or silently alter the interpretation.

## Validation criteria
All configured action IDs exist in the CP05 vocabulary; paths and transitions are reachable and coherent; every action has an explicit disposition; completion is specified; branch/rework conditions are explicit; no unsupported duration threshold is present; source/revision and owner are recorded. Unknown policy remains disabled pending review.

## Resume point
After delivery, validate the specification, run deterministic workflow cases, connect the already-trained model's predicted events to the configured state machine, and keep process anomaly performance `NOT EVALUATED` unless held-out process-violation ground truth is separately reviewed.

