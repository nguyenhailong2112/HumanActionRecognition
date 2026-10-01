# HUMAN HANDOFF — CP09 Semantic Gate

**Current state: `HUMAN_REVIEW_REQUIRED`.** No executable workflow file exists, so CP09 has not run and will not run a real held-out process trace. This handoff pre-fills the facts supported by repository/source evidence; the owner only needs to decide the unresolved semantics.

Artifact requested: `configs/workflows/disassembly_A.yaml`, named **Research Workflow Specification / Benchmark Procedure Interpretation**. This is not an official factory SOP.

| Decision | Evidence-backed current fact | Provenance | Why unresolved | Owner input required |
|---|---|---|---|---|
| Vocabulary scope | Official TAS-S: 25 non-NULL + NULL (26 labels); frozen project model: 17 non-NULL + NULL. Eight official actions are outside model scope. See `experiments/CP09/action_vocabulary_scope.json`. | DG | Model scope cannot establish which unmodeled steps matter to procedure semantics. | Confirm which workflow-relevant steps cannot be observed in this model scope and whether the procedure can be evaluated without them. Do not change model classes in this handoff. |
| Action dispositions | CP08 ledger describes all 17 project labels conservatively; all are non-executable. | DG/DO/RD + HUMAN | Dataset labels do not say mandatory/optional/conditional/rework/out-of-scope. | Assign one reviewed disposition to each project action; cite source or mark unknown. |
| Required order / partial order | Direct annotation has varying orders; statistics are descriptive. Official PSR graph is a separate task. | DO/DG | Neither observed order nor PSR establishes TAS-S process order. | Specify approved prerequisites or valid route(s), and any branch condition. Choose one supported representation. |
| State effects | UNSCREW, STORE, RETRIEVE, INSTALL, ATTACH and coarse REMOVE labels do not provide a complete approved component-state contract. STORE_GEARBOX_HOUSING is not PSR Remove gearbox_housing. | DG/RD/SOURCE GAP | No validated action-to-state/evidence bridge exists. | State exactly what each label proves, if anything; keep unsupported states unknown. |
| Repeat/rework/recovery/restart | Repeated labels exist; no approved repeat/recovery semantics. | DO + HUMAN | Frequency cannot establish allowed retries or state reversal. | Specify allowed repeat/recovery/rework transitions and reset behavior, or state none/unknown. Do not invent a repeat limit. |
| Completion | No owner-approved completion criterion. Video EOF is only observation end. | SOURCE GAP + HUMAN | Label/video end does not prove procedure termination or terminal physical state. | Define completion and how unobservable objectives are handled. |
| Evidence/uncertainty | Event confidence is descriptive; evidence sufficiency remains unknown. | DO + HUMAN | No calibrated confidence or approved evidence policy. | Define evidence requirement and handling for ambiguous, unknown, out-of-view, and insufficient evidence. Do not derive sufficiency from confidence alone. |
| Timeout/duration | No authoritative policy found; CP08 uses no enabled timing rules. | SOURCE GAP | No official threshold can be inferred. | Keep disabled unless an authoritative rule and citation are supplied. |
| Approval metadata | No approved reviewer/version/date exists. | HUMAN | Codex cannot create owner identity or approval. | Supply actual specification version, reviewer/owner, review date, and explicit approval after decisions are complete. |

Please edit/complete the human-owned `HumanSemanticWorksheet.md` yourself and provide the reviewed YAML at the path above. Do not set `status: HUMAN_VALIDATED` or `enabled: true` until you have approved all required decisions. Then CP10 can validate the file, run deterministic tests, and interpret the frozen ActionEvents. Process performance metrics will still require matching process ground truth.

The separate CP08 event visual review is still pending at `HUMAN_HANDOFF_CP08_EVIDENCE_REVIEW.md`; its output belongs at `experiments/CP08/human_evidence_review.csv`. Visual judgments must not be converted automatically into training labels or process-violation labels.
