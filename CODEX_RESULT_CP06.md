CP06 FINAL REPORT
Status: PARTIAL. Action evaluation and deterministic workflow infrastructure are complete. Workflow semantics and visual evidence review still require the human engineer, so process compliance was not evaluated.
Context recovery and CP05 audit
CP05’s frozen subset and reported action metrics are supported by its config, training report, checkpoints, test outputs and evidence index. The models remain our baselines on a procedure-scoped IMPACT subset, not an official IMPACT benchmark reproduction.
The newly supplied I3D ZIP passed SHA-256 verification against the release manifest and the official IMPACT archive structure/CRC verifier. SHA-256: 97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111. The ZIP contains 560 feature files—112 per view—and its filenames match the 560 extracted files. CP05’s separate target audit reports 48/48 front-view sequences as finite, float32 T×1024 and annotation-aligned. Numeric validation of all 560 arrays was not repeated.
During the seed runs, I detected that the initial runner reused CP05’s Framewise checkpoint paths. I preserved the seed-41 Framewise checkpoints under CP06 paths and reproduced CP05’s seed-17 Framewise checkpoint from its frozen config. Best and final validation losses and every stored held-out metric match CP05. CP05 evaluation files were not modified; the correction is recorded in the audit artifacts.
Environment and dataset
Python 3.12.14, PyTorch 2.14.0+cu132, CUDA available, RTX 5060 Ti with 16,311 MiB reported memory, driver 596.21. Both new seed runs completed on CUDA.
The experiment uses Disassembly_A/front; no left/right/ego video download is needed for this front-view scope. Those raw video views remain absent; the I3D archive does contain features for all five views.
Workflow semantics and handoffs
Available IMPACT TAS-S documentation establishes action labels and split membership. The separate PSR prerequisite graph is mined from data and does not establish a canonical TAS-S workflow. No reviewed configs/workflows/disassembly_A.yaml was supplied.
A clearly non-executable, HUMAN_REVIEW_REQUIRED draft and source audit are ready. The handoff requests explicit, source-backed steps, ordering, branches, rework, restart, completion, timing, evidence and uncertainty policies. The artifact is a Research Workflow Specification / Benchmark Procedure Interpretation, not an official factory SOP.
- [Workflow sources](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP06/workflow_sources.md)
- [Workflow draft](C:/Users/Admin/PycharmProjects/HumanActionRecognition/configs/workflows/disassembly_A.draft.yaml)
- [Workflow handoff](C:/Users/Admin/PycharmProjects/HumanActionRecognition/HUMAN_HANDOFF_CP06.md)
- [Evidence-review handoff](C:/Users/Admin/PycharmProjects/HumanActionRecognition/HUMAN_HANDOFF_CP06_EVIDENCE_REVIEW.md)
The existing workflow engine and validator were extended. Synthetic tests cover accepted and invalid transitions, skip, repeat, recovery paths, optional and conditional branches, reset, worker isolation, unknown/ambiguous/insufficient evidence, malformed/overlapping events, completion, and disabled or explicitly configured timing policies. 44 repository tests passed, including 20 CP06 workflow tests. These validate logic only; they are not process performance.
Action metrics and seed reliability
Definitions are audited in [metric_definition_audit.md](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP06/metric_definition_audit.md). Per-execution, equal-execution mean, sample standard deviation and pooled results for both models are in [action_metrics.json](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP06/action_metrics.json). Pooled sequence metrics preserve execution boundaries.
Held-out execution	MS-TCN accuracy	Macro-F1	Edit	F1@10 / @25 / @50	GT/pred segments
SS07EL13…001	.278	.123	39.29	.275 / .275 / .078	23/28
SS07EL13…002	.486	.367	53.57	.391 / .391 / .087	28/18
SS07EL13…003	.770	.507	52.17	.537 / .537 / .293	23/18
SS07EL13…004	.743	.562	56.52	.579 / .579 / .368	23/15


MS-TCN equal-execution means are .569 accuracy, .390 Macro-F1, 50.39 Edit, and .445/.445/.207 F1@10/25/50. Framewise means are .445/.319/11.70 and .149/.094/.032. MS-TCN pooled results are .522 accuracy, .361 Macro-F1, 50.00 Edit, and .432/.432/.193 F1@10/25/50.
MS-TCN seed means (17 from CP05; 23 and 41 newly trained) were:
Seed	Best validation epoch/loss	Accuracy	Macro-F1	Edit	F1@10 / @25 / @50
17	11 / 1.2703	.569	.390	50.39	.445 / .445 / .207
23	11 / 1.5317	.574	.405	46.48	.488 / .421 / .330
41	6 / 1.2537	.550	.310	32.30	.357 / .318 / .215


Across-seed sample SD was .0125 accuracy, .0509 Macro-F1, 9.52 Edit, and .067/.068/.069 F1@10/25/50. Checkpoint selection used validation only; test results were not used for tuning. [Seed reliability report](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP06/seed_reliability.md).
Error analysis, evidence and integration
The held-out MS-TCN analysis found 159 contiguous mismatch runs. Largest frame confusions were NULL→EXTRACT_BEARING_PLATE_ASSEMBLY (179 frames), STORE_BEARING_PLATE_ASSEMBLY→DETACH_ADAPTER_PLATE (169), and REMOVE_LOCKING_LEVER_ASSEMBLY→EXTRACT_BEARING_PLATE_ASSEMBLY (138). There were 79 predicted versus 97 GT action segments pooled; one execution over-segmented by count and three under-segmented. Post-decoding changed 3 raw-correct frames to wrong and corrected 2 raw-wrong frames.
Strong supported classes included EXTRACT_BEARING_PLATE_ASSEMBLY (F1 .683), DETACH_ADAPTER_PLATE (.656) and REMOVE_ROTOR_ASSEMBLY (.653). STORE_GEARBOX_HOUSING and STORE_TOOL had zero F1; their test support was 6 and 30 frames. Visual cause and bottleneck attribution remain unknown pending review.
All 69 CP05 evidence records have unique event keys and existing snapshots/clips; each remains workflow NOT EVALUATED. The review package selects 21 review entries across confidence, boundary, rare-action, confusion, NULL-leakage and possible-ambiguity categories. These are candidates for human review, not corrected labels.
Actual ActionEvent→workflow traces were not run because workflow semantics are not validated. Process compliance, anomaly performance, and duration violations are NOT EVALUATED. CP06 did not measure streaming latency; cached-feature offline timing must not be interpreted as real-time performance.
Decision and next checkpoint
Decision: INVESTIGATE. Keep MS-TCN as the current temporal baseline, but do not escalate model size. Seed variability and errors warrant human visual/annotation review before attributing the bottleneck to data, representation or temporal capacity.
Human actions required: review the selected evidence and provide the source-backed workflow YAML. CP07: validate that YAML, rerun workflow golden tests, then trace actual held-out ActionEvents through workflow state and evidence. Keep process scoring disabled unless valid process-violation ground truth is also supplied.
Key artifacts: [CP06 experiment](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/EXP-CP06.md), [context and audit](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP06/CP06_context_and_audit.md), [action error analysis](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP06/action_error_analysis.md), and [CHECKSHEET](C:/Users/Admin/PycharmProjects/HumanActionRecognition/CHECKSHEET.md).