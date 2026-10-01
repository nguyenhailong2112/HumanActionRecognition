# CP08 Semantic Integrity Audit

## Authority and interpretation layers

The three worksheets are not interchangeable:

| Artifact | Role | Authority for executable rules |
|---|---|---|
| `HumanSemanticWorksheet.md` | Human-owned blank decision form; currently `HUMAN_REVIEW_REQUIRED`. | Human decisions are still absent. Do not edit/fill this file in CP08. |
| `HumanSemanticWorksheet_CP07_source_grounded_draft.md` | Research-prepared descriptions with DG, DO, INT and HUMAN provenance. It explicitly says it is not executable. | Useful source-grounded draft; its mandatory/optional/workflow fields remain human-owned. |
| `HumanSemanticWorksheetReconstructedProjectGroundTruth.md` | Expanded RD/POL project reconstruction; it proposes objective states, flexible order, repeats/recovery, completion and evidence policy. | Research-derived project interpretation, not official IMPACT author ground truth and not automatically process-owner-approved. |

The action ledger is in `semantic_action_ledger.json`. It answers conservatively what each of the 17 project TAS-S labels can currently establish. Every row has `executable: false` because no validated workflow or evidence policy exists.

## Official release facts checked locally

Sources inspected:

1. `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/TAS/mapping_TAS-S.txt`: official TAS-S class-name mapping; it contains 25 non-background class IDs plus NULL. The project `configs/cp05.yaml` uses the 17 non-background classes observed in its scoped 48-execution subset.
2. `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/PSR/README.md`: identifies PSR as a separate component metadata / prerequisite-graph task.
3. `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/PSR/labels/component_names.json` and `procedure_info_IMPACT.json`: component vocabulary and install/incorrectly-installed/remove state categories.
4. `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/tasks/PSR/gemini_3_1_pro/configs/procedure_graph.json`: graph metadata says edges are robust prerequisites mined from data and a missing edge means flexible ordering. The graph has 53 nodes and 102 edges. It has distinct `*_remove_ok` and `*_recover_ok` states. In the inspected graph, `bearing_plate__recover_ok` and `adapter_plate__recover_ok` have prerequisite entries, while the corresponding `*_remove_ok` entries are empty. A recover prerequisite is therefore not evidence of a normal remove prerequisite.
5. `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/PPR/README.md` and `tasks/PPR/README.md`: PPR-L/R labels are `NORMAL`, `ANOMALY`, and `RECOVERY` phases. They are not aligned event-level workflow-violation truth for this TAS-S test subset.
6. `HumanSemanticWorksheet_CP07_source_grounded_draft.md` and `HumanSemanticWorksheetReconstructedProjectGroundTruth.md`: research interpretation and known gaps; these are cited as project interpretations, not promoted to DG.
7. Frozen CP05 TAS-S labels loaded from `configs/cp05.yaml` and the official S2 split: descriptive order/repetition counts below.

## Semantic decisions that remain unresolved

- `UNSCREW_ANTI_VIBRATION_HANDLE` proves the labeled unscrewing/loosening action was predicted. It does not alone prove the handle has been removed.
- `STORE_*` is a location action; it does not automatically prove removal. In particular, `STORE_GEARBOX_HOUSING` is not the separate PSR `Remove gearbox_housing` transition. The reconstructed worksheet proposes gearbox-removed as a terminal objective, but the scoped TAS-S label set has no explicit gearbox-removal label. A storage event alone cannot certify that objective. The owner must decide whether the objective is unsupported/unknown for this observation path or provide an explicit reviewed bridge and evidence rule.
- Coarse `REMOVE_*`, `EXTRACT_*`, and `DETACH_*` labels directly describe predicted action classes. Some source-grounded worksheet examples align these with PSR component events in inspected annotations, but that alignment is DO/INT/RD, not an official universal TAS-S → PSR state-effect contract.
- `RETRIEVE_*` is not automatically a required step or recovery. `INSTALL_*`/`ATTACH_*` may reverse component state, but exact component sets and workflow role need human confirmation.
- Repeated TAS-S intervals are observed. They do not identify continuation, retry, recovery, rework, error, or post-completion behavior by themselves.
- The reconstructed terminal component state and sufficient-evidence policy are RD/POL proposals. Video end is not procedure completion, and no authoritative duration threshold was found.

## Observed order and repeat facts — descriptive only

The 48 local project executions were run through the existing annotation loader. Consecutive identical frame labels were collapsed into labeled runs; NULL/background runs were excluded from action ordering. These are **DO**, not normative ordering evidence:

| Pair | Relative order observed in executions containing both |
|---|---|
| `REMOVE_LOCKING_LEVER_ASSEMBLY` vs `EXTRACT_BEARING_PLATE_ASSEMBLY` | remove before extract: 47; extract before remove: 1 |
| `DETACH_ADAPTER_PLATE` vs `REMOVE_ROTOR_ASSEMBLY` | detach before remove: 43; remove before detach: 4 |
| `EXTRACT_BEARING_PLATE_ASSEMBLY` vs `DETACH_ADAPTER_PLATE` | extract before detach: 46; detach before extract: 1 |

Repeated action labels occur in the annotations and were independently counted after run collapse. Execution counts with more than one run include: `DETACH_ADAPTER_PLATE` 47, `REMOVE_ROTOR_ASSEMBLY` 47, `EXTRACT_BEARING_PLATE_ASSEMBLY` 46, `STORE_ADAPTER_PLATE` 40, `STORE_ROTOR_ASSEMBLY` 36, `STORE_BEARING_PLATE_ASSEMBLY` 35, `REMOVE_LOCKING_LEVER_ASSEMBLY` 31, `STORE_TOOL` 29, `STORE_LOCKING_LEVER_ASSEMBLY` 19, and `UNSCREW_ANTI_VIBRATION_HANDLE` 2. These repetitions are annotation/run observations and do not determine process repeat semantics.

The opposite orders show that one total action order cannot be inferred from the dataset. They do not establish which transitions are allowed or why an order varies. Frequency, relative ordering and repetition are not converted to workflow rules.

## State-effect architecture decision

The CP07.1 prerequisite engine can represent accepted action prerequisites, but cannot by itself encode state reversal, conflicting component states, semantic certification, or a state-based completion objective. Those concepts appear in the RD/POL reconstruction, but there is no human-approved mapping contract yet. Therefore CP08 does **not** add a state-effect framework or workflow rules. If the owner confirms that state-reversal/rework/completion semantics are part of the intended research specification, the smallest next design should be an explicit action→state-effect mapping consumed by the existing workflow layer, with unknown effects remaining unknown. The gate remains human validation; no state change is currently authorized by CP08.

## Human gate

The human must resolve the exact fields in `HUMAN_HANDOFF_CP08.md`. Until then:

- workflow semantic status: `HUMAN_REVIEW_REQUIRED`;
- executable `configs/workflows/disassembly_A.yaml`: absent;
- workflow execution: disabled / not run on real held-out events;
- process compliance and process anomaly metrics: `NOT_EVALUATED`.
