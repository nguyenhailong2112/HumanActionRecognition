# HUMAN HANDOFF — CP08

The required workflow and evidence tasks are separated into:

- [Research Workflow Specification handoff](experiments/CP08/HUMAN_HANDOFF_CP08.md)
- [Frozen action evidence review handoff](HUMAN_HANDOFF_CP08_EVIDENCE_REVIEW.md)

The workflow request is human-dependent because available TAS-S labels, PSR relations, and project reconstructions do not authorize normative `Disassembly_A` semantics. The evidence review is human-dependent because file existence and model confidence cannot determine whether the visible action and boundary are semantically correct.

Please return:

1. A completed, owner-reviewed candidate `configs/workflows/disassembly_A.yaml` using the exact field instructions and YAML form in the workflow handoff. Keep the status unapproved until the project owner has explicitly approved the semantics. The artifact name remains **Research Workflow Specification / Benchmark Procedure Interpretation**, not factory SOP.
2. A completed `experiments/CP08/human_evidence_review.csv` with one row for each of the 13 unique events listed in the evidence handoff. Do not edit training labels or the frozen benchmark.

Until these artifacts are returned and validated, workflow semantics remain `HUMAN_REVIEW_REQUIRED`, actual held-out workflow traces are not generated, and process compliance/anomaly metrics remain `NOT_EVALUATED`.
