# HUMAN HANDOFF — CP02 data and procedure grounding

This handoff covers two independent human dependencies. Do not merge them: obtaining benchmark inputs enables action evaluation; process-owner input establishes the meaning of workflow compliance.

## A. Obtain the official CP02 action features

### Why a human handoff is needed

Across CP01.1 and CP02, the official I3D feature archive downloader was attempted three times and did not produce a file; the smaller official MViTv2 feature archive was attempted once in CP02 as an alternate path and also did not produce a verifiable file. This host has CPU-only PyTorch (`torch.cuda.is_available() == False`), only 2 of the 48 S2 target videos/features in the quick-start sample, and insufficient free space for the full front-view raw-video archive. The official I3D reference extractor requires CUDA and an external pretrained checkpoint. It is not a validated fallback on this host.

### Exact source and artifact

- Dataset: IMPACT v1.1, official Google Drive mirror: <https://drive.google.com/drive/folders/1P7vBnxSVH9g_lQc5n0c0WA47QAGEhE_U?usp=sharing>
- Also available from the official Hugging Face dataset: <https://huggingface.co/datasets/KratosWen/IMPACT>
- Download `v1.1/features/IMPACT-v1.1-features-I3D.zip` (official release documentation lists **15.7 GiB**).
- Expected SHA-256: `97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`
- Save the archive, without extracting it, to:
  `data/raw/impact/v1.1/features/IMPACT-v1.1-features-I3D.zip`
- Release terms: CC BY-NC-SA 4.0; non-commercial research/education use.

### Exact steps

1. Download the I3D archive from the official mirror above. The Hugging Face mirror is an alternative official source if the Drive transfer fails.
2. Verify SHA-256 in PowerShell:

   ```powershell
   Get-FileHash -Algorithm SHA256 data/raw/impact/v1.1/features/IMPACT-v1.1-features-I3D.zip
   ```

   The `Hash` must exactly equal the value above. If it does not, do not use the file.
3. Run the release archive structure/CRC/checksum verifier:

   ```powershell
   .\.venv\Scripts\python.exe ResearchDocuments/01_IMPACT/code/IMPACT/tools/verify_release.py data/raw/impact/v1.1/features/IMPACT-v1.1-features-I3D.zip --checksums data/raw/impact/v1.1/SHA256SUMS
   ```

   Expected: `[ok] archive structure and CRC`.
4. Tell Codex the archive is in place and report the SHA-256 and verifier output. Codex will run:

   ```powershell
   .\.venv\Scripts\python.exe tools/cp02_preflight.py --config configs/cp01_1.yaml
   ```

   Acceptance: split PASS; 48/48 annotation PASS; 48/48 I3D features present, finite, and exactly `num_frames × 1024`; train/validation/test counts remain 39/5/4.
5. Codex will then train both existing baselines using validation-only checkpoint selection, followed by a single final test evaluation after configuration freeze.

   ```powershell
   .\.venv\Scripts\python.exe tools/train_baseline.py --config configs/cp01_1.yaml --epochs 12 --defer-test-eval
   .\.venv\Scripts\python.exe tools/evaluate.py --config configs/cp01_1.yaml --split val --model both
   # Freeze/check the config and validation decision, then run the final test exactly once:
   .\.venv\Scripts\python.exe tools/evaluate.py --config configs/cp01_1.yaml --split test --model both
   .\.venv\Scripts\python.exe tools/compare_baselines.py --input results/cp01_1/evaluation/test_metrics.json
   ```

### Official extraction fallback assessment

The cloned official IMPACT code contains `tools/features/extract_i3d.py`; it documents 16-frame centered clips, 224-pixel center crop, RGB values normalized to `[-1,1]`, and `T × 1024` output. It imports `pytorch_i3d.py` from the upstream `piergiaj/pytorch-i3d` repository and requires an RGB pretrained checkpoint (`rgb_imagenet.pt`; upstream page lists 48.5 MB). The script calls CUDA directly. This machine has no CUDA-enabled PyTorch and the 29.3 GiB upper-size official front-video archive cannot fit alongside the current data on C:. Therefore extraction is a valid documented method in principle, but **not executable/reproducible in the present environment**. Prefer obtaining the already released, checksum-verifiable features.

### Video inspection/evidence input

The I3D archive enables feature-based action training/evaluation, but it does not contain image frames for snapshot/clip evidence. If CP02 requires evidence from a held-out video, provide at least the front-view MP4 for one or more S2 test executions (`SS07EL13_Disassembly_A_001_front` through `_004_front`) from the same official v1.1 release, or make the complete `videos/IMPACT-v1.1-videos-front.zip` available on a volume with enough free space. Preserve release checksums and do not substitute sample/train videos as held-out test evidence. The current sample has only two target-procedure videos, both train-side.

## B. Supply the approved Disassembly A procedure

### Why the process owner is required

TAS-S and PPR annotations describe observations and procedural phases; they do not specify the factory's approved order, valid alternatives, recovery rules, completion criterion, or allowed duration. Those semantics cannot safely be inferred from model output or action frequency.

### Required human input

Process owner: supply/review the actual **angle-grinder Disassembly A** SOP and revision. Save the response to `configs/workflows/disassembly_A.yaml`. Use this template (the owner may edit it, but must preserve the meaning and cite the SOP):

```yaml
workflow:
  id: angle_grinder_disassembly_A
  procedure: Disassembly_A
  version: "<SOP ID and revision>"
  approved_by: "<process owner>"
  approved_on: "YYYY-MM-DD"

  # Map every non-background action in configs/cp01_1.yaml to an explicit disposition.
  # Values: required | optional | conditional | rework | out_of_scope.
  # Conditional/out_of_scope must include an SOP-backed reason.
  action_disposition: {}
  action_vocabulary: []

  # Enumerate the canonical path and only SOP-permitted alternatives.
  # Finite valid_paths fit the current deterministic engine; explain any loop/rework.
  valid_paths:
    - id: canonical
      steps: []
  # Optional explicit edge list; must exactly match adjacent route edges.
  valid_transitions: []
  optional_steps: []
  # Each conditional/rework entry points to a valid_paths.id and cites its SOP trigger.
  conditional_paths: []
  rework_paths: []
  completion:
    condition: "<observable SOP-backed completion condition>"

  # Keep empty unless timing limits are explicitly required by the SOP.
  duration_limits_seconds: {}
```

The frozen action vocabulary is in `configs/cp01_1.yaml`. Action names retain the official uppercase TAS-S label, so current source-to-internal mapping is identity. Include every in-scope label, document out-of-scope labels with a reason, and do not classify `NULL` background as a procedure step. Do not invent durations.

### Acceptance and resume

Include the SOP/revision, owner, date, all action dispositions, ordered required steps, completion criterion, valid alternatives, and any repeat/rework conditions. After receipt, Codex will validate names and path IDs, check declared transitions against reachable adjacent route edges, verify finite routes and a stated completion condition, flag ambiguity instead of rewriting process meaning, add synthetic tests for approved alternatives/rework, render the workflow, and only then enable the workflow configuration. Keep real workflow anomaly precision/recall **NOT EVALUATED** until held-out ground-truth violations have been validated.

## C. Ground-truth boundary for process metrics

Official PPR-L/R frame-level labels are present for the S2 test executions and include `NORMAL`, `ANOMALY`, and `RECOVERY` for each hand. These are genuine labels for the PPR benchmark, but they are **not** labels for workflow violations such as skip, wrong order, repeat, or timeout. Do not score the current action/workflow engine against them as if they were equivalent.

If process-owner-approved workflow precision/recall is required, annotate only the four held-out test executions after SOP approval (not all 48 videos). Use official v1.1 front-view video and TAS-S timeline; inspect all four executions to identify both deviations and clean intervals. Save a CSV at `experiments/CP02/process_ground_truth.csv` with:

```text
video_id,start_time_s,end_time_s,violation_type,expected_step,observed_action,sop_clause,reviewer,review_status
```

Use `WRONG_SEQUENCE`, `SKIPPED_STEP`, `REPEATED_STEP`, `UNEXPECTED_ACTION`, `NO_VIOLATION`, or `AMBIGUOUS`; intervals are half-open `[start_time_s,end_time_s)`. Use `NO_VIOLATION` for reviewed clean executions/intervals and `AMBIGUOUS` rather than guessing. Add `TOO_FAST`/`TOO_SLOW` only when duration bounds are specified by the approved SOP. A process owner must review the semantic labels. Until then, process anomaly metrics remain **NOT EVALUATED**.
