# CP09 Semantic Gate Audit

## Human approval state

**HUMAN_REVIEW_REQUIRED.** `configs/workflows/disassembly_A.yaml` is absent; the only config is `disassembly_A.draft.yaml`, marked unapproved and containing no executable transitions. `HumanSemanticWorksheet.md` remains the human-owned worksheet and was inspected, not completed. No genuine owner, version/date, disposition set, route/prerequisites, completion rule, or approval metadata is available. CP09 must stop before activation.

## Provenance boundary

| Provenance | Current use | May it authorize executable workflow rules? |
|---|---|---|
| DG — official dataset ground truth | Official class IDs/names and released data structure | Only the fact represented by the source; labels do not define normative process policy. |
| DO — direct observation | Annotation order/repetition and event/media link facts | No; descriptive only. |
| RD — research-derived interpretation | Project reconstruction and source synthesis | No, until reviewed and approved by the owner. |
| POL — project policy | Candidate engineering policy | No, until the owner approves it. |
| HUMAN — process/project-owner decision | Required dispositions, semantics, completion, uncertainty, evidence, timing/rework rules | Yes, after recorded review and validator acceptance. |

PSR prerequisite relations remain auxiliary component-state research and are not promoted to TAS-S workflow order. PPR phase labels are not event-level process-violation truth. Repetition/order statistics remain descriptive.

## Vocabulary scope audit

The official mapping at `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/TAS/mapping_TAS-S.txt` contains **26 total labels: 25 non-NULL action labels plus NULL**. `configs/cp01_1.yaml` preserves the frozen **17 non-NULL project model actions plus NULL**. Eight official actions are not modeled in this frozen scope: `FINISH_ANGLE_GRINDER_ASSEMBLY`, `INSERT_BEARING_PLATE_ASSEMBLY`, `INSTALL_LOCKING_LEVER_ASSEMBLY`, `RETRIEVE_ADAPTER_PLATE`, `RETRIEVE_ANTI_VIBRATION_HANDLE`, `RETRIEVE_GEARBOX_HOUSING`, `RETRIEVE_ROTOR_ASSEMBLY`, and `SCREW_ON_ANTI_VIBRATION_HANDLE`. The machine-readable source-to-model comparison is `action_vocabulary_scope.json`.

No frozen model class order was modified. Validator CLI and errors now explicitly call the supplied vocabulary the configured project/model scope; a regression test ensures an official-but-unmodeled label is rejected as outside that scope. This avoids implying that the 17-class model represents all official TAS-S labels.

## Action semantics still requiring owner decisions

The existing CP08 `semantic_action_ledger.json` covers all 17 project-scoped labels with provenance and conservative state/evidence boundaries; every entry remains `executable: false`. The eight official-but-unmodeled labels are explicitly listed as outside current model scope, not silently treated as absent from IMPACT. Mandatory/optional/conditional/rework/out-of-scope dispositions, valid order/prerequisites, repeat/recovery/restart, completion, evidence sufficiency, uncertainty handling, and any timing policy still require human values. In particular, UNSCREW does not prove removal, STORE does not prove REMOVE, STORE_GEARBOX_HOUSING is distinct from PSR Remove gearbox_housing, and RETRIEVE/INSTALL/ATTACH roles remain undecided.

Until those values and real approval are provided, no executable workflow or real trace is safe. Process metrics remain `NOT EVALUATED`.
