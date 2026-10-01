# CP11 Research Semantic Decision Record

**Artifact:** Research Workflow Specification / Benchmark Procedure Interpretation, `research-v1`  
**Approval boundary:** project research approval delegated by the owner in the CP11 master prompt. This is not official IMPACT author ground truth and is not a factory SOP.

## Provenance labels

- **DG — Dataset/documentation-grounded:** explicitly present in an official release or benchmark artifact.
- **DO — Dataset observation:** measured or observed in this project's data, descriptive only.
- **RD — Research decision:** project-level interpretation authorized by the CP11 delegation.
- **POL — Policy choice:** conservative behavior selected for this executable research workflow.

## Decisions

| Decision | Evidence and provenance | Reason | Does not claim |
|---|---|---|---|
| Workflow scope is `Disassembly_A`, IMPACT v1.1 TAS-S, front view, project model vocabulary. | Official label map at `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/TAS/mapping_TAS-S.txt` (**DG**); frozen project class order in `configs/cp01_1.yaml` (**DG**). | The executable workflow must use exactly the project's 17 modeled non-NULL actions, while keeping the full official mapping distinct. (**RD**) | It does not expand the model vocabulary or reproduce the official benchmark in full. |
| Required core actions are `UNSCREW_ANTI_VIBRATION_HANDLE`, `REMOVE_LOCKING_LEVER_ASSEMBLY`, `EXTRACT_BEARING_PLATE_ASSEMBLY`, `DETACH_ADAPTER_PLATE`, `REMOVE_ROTOR_ASSEMBLY`. | TAS-S names (**DG**); source-grounded and reconstructed CP08 worksheets (**RD**) and the explicit owner-delegated CP11 decisions (**RD**). | These are the five process-relevant observations selected for research workflow v1. | It does not assert a universal physical teardown procedure or one-to-one TAS-S/PSR state equivalence. |
| `START_ANGLE_GRINDER_ASSEMBLY` is a procedure-boundary marker, not a completion requirement. | CP11 explicit decision (**RD**). | Procedure start metadata does not represent a core disassembly state change in this workflow. | Missing START alone does not imply an incomplete procedure. |
| Twelve store/retrieve/install/attach/tool actions are `out_of_scope`. | TAS-S vocabulary (**DG**); CP08 semantic audit plus CP11 explicit decisions (**RD/POL**). | Preserve their observations without treating logistics/recovery-like labels as normal-disassembly violations. | Out of scope does not mean unexpected, incorrect, or a human mistake. |
| `STORE_GEARBOX_HOUSING` does not satisfy a gearbox-removal state. | TAS-S action name and separate PSR state `Remove gearbox_housing` in official release materials (**DG**); conservative CP11 decision (**POL**). | A store action does not establish the distinct PSR remove state. | It does not map TAS-S labels to PSR states or claim PSR is a TAS-S ground-truth contract. |
| `UNSCREW_ANTI_VIBRATION_HANDLE` is a prerequisite for each of the four major component-removal actions; the four removal actions have no mutual prerequisites. | CP11 defines UNSCREW as mechanical preparation/state-changing and explicitly prohibits invented mutual dependencies among the four major removal actions (**RD**). CP08 observed order variation (**DO**) is descriptive only and was not used to set edges. | Encode the minimum prerequisite implied by the delegated “mechanical preparation” semantics while preserving order flexibility across removals. (**RD/POL**) | This is not an official IMPACT author graph, a factory-validated safety rule, or proof that every physical order is valid. |
| Completion means all five core actions accepted. | CP11 explicit decision (**RD**). | This is the narrow observable target supported by the project workflow semantics. | This is research-defined observable subprocedure completion, not full physical teardown completion. |
| Repeating an already accepted required action produces `REPEATED_STEP`. | CP11 explicit decision (**RD/POL**). | Preserve the observed event and report a workflow interpretation without a repeat limit. | It does not mean mistake or automatic recovery. |
| Duration and timeout checks are disabled. | No authoritative timing rule identified in CP08/CP10 source audits (**DG: absent from reviewed sources**); CP11 explicit policy (**POL**). | Avoid invented thresholds. | No duration violation or timeout metric is available. |
| Confidence, evidence sufficiency and workflow acceptance remain separate. Unknown/ambiguous evidence does not advance the workflow. | ActionEvent contract and CP11 explicit policy (**RD/POL**). | Keep perception observations auditable and avoid confidence-based evidence promotion. | Existing evidence links do not validate visual correctness. |
| Workflow status is `RESEARCH_APPROVED`, scope `PROJECT_RESEARCH`; factory SOP validation is explicitly false. | Owner's CP11 delegation (**RD**). | Permit deterministic project research interpretation under explicit scope. | No factory owner, factory reviewer, official SOP, or factory validation is represented. |

## Workflow-engine behavior authorized by this record

- A valid, sufficient-evidence UNSCREW event enables the four major removal actions; those four may then be accepted in any order. A removal before UNSCREW yields a deterministic invalid transition.
- A valid, sufficient-evidence core ActionEvent may advance the deterministic research workflow subject to that prerequisite.
- An out-of-scope event remains in `observations`, has status `out_of_scope_ignored`, does not advance state, and does not create a workflow violation.
- Unknown, ambiguous, or insufficient evidence remains observable and does not advance state.
- An explicit procedure-end signal before all core actions produces `INCOMPLETE_PROCEDURE`; video observation ending alone remains unconfirmed.
- No statistical process performance is inferred from deterministic synthetic checks or the frozen prediction stream.
