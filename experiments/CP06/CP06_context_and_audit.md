# CP06 Context and CP05 Audit

## What CP05 claims

CP05 froze IMPACT v1.1 TAS-S, S2 split 2, `Disassembly_A/front` (39 train, 5 validation, 4 held-out test executions; test worker SS07EL13). It reports CUDA training and held-out evaluation of FramewiseBaseline and our MS-TCN, 48/48 aligned feature/video readiness, 24 passing tests, action timelines, and 69 timestamp-linked MS-TCN evidence events. Workflow semantics and process compliance remained human-dependent / not evaluated. CP05 says its feature ZIP was absent at that time.

## Direct repository evidence

- `configs/cp05.yaml`, `experiments/CP05/training_report.json`, `test_metrics.json`, `baseline_comparison.json`, `per_class_and_confusion.json`, `feature_readiness.json`, `video_readiness.json`, `evidence_index.json`, and the best/final model checkpoint files support the protocol and artifact claims. The test report contains four executions per model and records process workflow as NOT EVALUATED.
- `experiments/EXP-CP05.md` reports the same fixed subset and metrics (MS-TCN mean-per-execution: accuracy .569, macro F1 .390, edit 50.39, F1@10 .445, F1@25 .445, F1@50 .207; Framewise .445/.319/11.70/.149/.094/.032). CP05 is explicitly our baseline on a procedure-scoped IMPACT subset, not official baseline reproduction.
- `src/human_action/workflow.py` and `tools/validate_workflow.py` already provide a deterministic valid-path engine and a process-owner configuration validator. Existing tests cover basic accepted routes, skip/wrong order, repeat, unexpected action, reset, finite rework path and duration violations. CP06 extends the same engine with explicit branch-decision input and ambiguity handling; it does not add a second engine.
- `src/human_action/metrics.py` implements action metrics; `tools/compare_baselines.py` averages metrics equally across videos. Exact definitions are audited in `metric_definition_audit.md`.
- `HUMAN_HANDOFF_CP05.md` and `configs/cp05.yaml` show no approved Research Workflow Specification; workflow is disabled. CP05 outputs do not contain process ground-truth violations.
- Current `.venv-cp05` verification: Python 3.12.14, NumPy 2.5.3, OpenCV 4.14.0, PyTorch 2.14.0+cu132, CUDA available (PyTorch CUDA 13.2), NVIDIA GeForce RTX 5060 Ti / 16,311 MiB, driver 596.21. CP06 CUDA seed training completed.
- CP05 evidence index contains 69 unique held-out MS-TCN event keys; all 69 snapshot and clip paths exist and all remain `NOT EVALUATED` for workflow. Maximum recorded timestamp-to-frame delta is 6.11 microseconds.

## Archive audit update

The previously absent archive is now present at `D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1\features\IMPACT-v1.1-features-I3D.zip` (16,887,238,161 bytes). Its locally computed SHA-256 is `97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`, matching the documented release manifest. Official IMPACT `verify_release.py` completed successfully with `[ok] archive structure and CRC`; all 564 ZIP members passed structure/CRC checks. ZIP contains 560 `.npy` feature files (112 each for front/top/left/right/ego); extracted I3D directory has the same 560 basenames with zero missing/extra names. The CP05 target feature QA remains separate evidence for extracted target shapes/alignment (48/48 target sequences, float32 `T×1024`, finite and annotation-aligned); full-array numeric validation of all five-view files was not repeated in CP06.

## Discrepancies and allowed CP06 foundation

Two CP05 context discrepancies were actively reconciled. First, the archive previously recorded as absent was supplied; its hash, structure and CRC now pass. Second, CP06 initially generated paired seed runs with Framewise checkpoint paths inherited from CP05. The mismatch was detected by comparing per-execution predictions; the seed-41 Framewise checkpoints were copied into CP06-specific files, and the CP05 seed-17 Framewise checkpoint was reproduced from frozen `configs/cp05.yaml`. Best epoch/loss, final validation loss, and every stored held-out action metric (including class/segment statistics) match the existing CP05 records. CP05 evaluation files were not modified. The seed-run configs as executed are preserved and hash-checked; convenience configs and the seed runner now use CP06-specific Framewise output paths. Current reports align on the frozen split and process metrics being unevaluated. CP06 may build on CP05 metrics after this verified restoration; it may not infer process semantics from action order, prediction, or mined statistics. No test-set tuning was performed.

## CP06 execution boundary

CP06 covers deterministic workflow infrastructure and synthetic logic tests, metric-definition audit, per-execution/pooled test reporting, three-seed MS-TCN reliability using the unchanged CP05 recipe, held-out action-error analysis, and a review package for actual model evidence. Until a human-reviewed workflow YAML is available, actual action-to-workflow compliance remains NOT EVALUATED. Human visual judgments remain review-only and never auto-correct labels.
