# HUMAN HANDOFF — CP04 official data and process grounding

CP04 has two independent human dependencies: official features enable a reproducible action experiment; the process owner establishes the meaning of compliance. Do not infer one from the other.

## A. Official I3D feature archive

### Artifact

- Official release: IMPACT v1.1
- Exact file: `features/IMPACT-v1.1-features-I3D.zip`
- Official size: 15.7 GiB
- Published SHA-256: `97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`
- Official sources: [Google Drive release folder](https://drive.google.com/drive/folders/1P7vBnxSVH9g_lQc5n0c0WA47QAGEhE_U?usp=sharing), [Hugging Face IMPACT dataset](https://huggingface.co/datasets/KratosWen/IMPACT), [official data release guide](https://github.com/Kratos-Wen/IMPACT/blob/main/docs/DATA_RELEASE.md).
- Canonical destination: `data/raw/impact/v1.1/features/IMPACT-v1.1-features-I3D.zip`.
- Keep the ZIP compressed. The repository loader reads arrays from the official ZIP directly; extracting it creates unnecessary extra disk use. The current C: free space is only about 17.6 GiB, so choose a volume with adequate download/temp headroom. If using a different volume, report its path so the config can point there before preflight.

### Exact human steps

1. Open the official Google Drive folder (or official Hugging Face dataset) and download the exact I3D file above. Do not use third-party copies.
2. Save it directly at the canonical destination, creating the parent folders if needed. Do not rename or extract it.
3. In PowerShell, verify its checksum:

   ```powershell
   Get-FileHash -Algorithm SHA256 data/raw/impact/v1.1/features/IMPACT-v1.1-features-I3D.zip
   ```

   The hash must exactly equal the value above. Stop if it differs.
4. Verify official archive metadata, structure and CRC against the already verified release manifest:

   ```powershell
   .\.venv\Scripts\python.exe ResearchDocuments/01_IMPACT/code/IMPACT/tools/verify_release.py data/raw/impact/v1.1/features/IMPACT-v1.1-features-I3D.zip --checksums data/raw/impact/v1.1/SHA256SUMS
   ```

   Expected output includes `[ok] archive structure and CRC` and a checksum match.
5. Tell Codex the path, SHA-256, and verifier result. Codex resumes with:

   ```powershell
   .\.venv\Scripts\python.exe tools/cp02_preflight.py --config configs/cp01_1.yaml --output experiments/CP04_data_readiness.json
   ```

   Acceptance: split PASS; annotations 48/48 PASS; target S2 feature sequences 48/48 present, finite, frame-aligned and 1024-D. The archive layout is `IMPACT-v1.1/features/I3D/<execution_id>_<view>.npy`.

The official Google Drive link could not be read by the current web retrieval tool. The official Hugging Face selective-download route was attempted in earlier checkpoints without a verifiable full archive; CP04 did not repeat those same failed transfers. If browser/mounted Drive access is unavailable too, report the exact access error and do not substitute another source.

### Extraction and hardware boundary

- The official I3D extractor is `ResearchDocuments/01_IMPACT/code/IMPACT/tools/features/extract_i3d.py`; it emits frame-aligned `T×1024` descriptors from centered 16-frame RGB clips, 224-pixel crop, RGB `[-1,1]` normalization.
- The reference implementation calls `.cuda()` directly. CP04 hardware check found PyTorch `2.14.0+cpu`, `torch.cuda.is_available() == False`, zero CUDA devices, and no `nvidia-smi` command. Thus official I3D extraction is not executable on this laptop as configured. Do not claim local extraction/reproduction.
- The CP04 target model heads consume released precomputed features. CPU training may be attempted only after full features arrive and feasibility is observed; the future RTX 5060 PC can be used if CPU training is impractical. Do not wait for that PC to alter or fabricate data readiness.

## B. Process-owner SOP for Disassembly_A

Process owner: provide the current approved **angle-grinder Disassembly A** SOP and revision. Fill and save as `configs/workflows/disassembly_A.yaml`; cite the document and approval metadata. Edit the template to reflect policy exactly.

```yaml
workflow:
  id: angle_grinder_disassembly_A
  procedure: Disassembly_A
  version: "<SOP identifier and revision>"
  approved_by: "<process owner>"
  approved_on: "YYYY-MM-DD"
  action_vocabulary: []
  action_disposition: {}
  valid_paths:
    - id: canonical
      steps: []
  valid_transitions: []
  optional_steps: []
  conditional_paths: []
  rework_paths: []
  completion:
    condition: "<observable, SOP-backed completion condition>"
  duration_limits_seconds: {}
```

Requirements for the owner:

1. State ordered required actions and the completion condition.
2. List optional steps, conditional branches, valid alternatives, and retry/rework paths only where the SOP permits them; cite each trigger/clause.
3. Give every configured non-background TAS-S action a disposition: `required`, `optional`, `conditional`, `rework`, or `out_of_scope` (include the SOP-backed reason for `conditional`/`out_of_scope`). Do not treat `NULL` as a step.
4. Leave duration limits empty unless an official timing requirement exists. Do not invent thresholds.
5. Mark any ambiguous action semantics for review instead of guessing.

Codex will validate names, paths, transitions and completion without changing policy meaning. Workflow stays disabled until that validation passes.

## C. Optional held-out workflow-violation ground truth

To report real workflow anomaly precision/recall, the process owner must also review the four held-out S2 test executions after approving the SOP:

- `SS07EL13_Disassembly_A_001_front`
- `SS07EL13_Disassembly_A_002_front`
- `SS07EL13_Disassembly_A_003_front`
- `SS07EL13_Disassembly_A_004_front`

Review the official front-view recordings and TAS-S timeline. For each deviation interval (and reviewed clean interval), record `execution, start_time_s, end_time_s, violation_type, expected_step, observed_action, SOP_clause, reviewer, review_status` in `experiments/CP04/process_ground_truth.csv`. Use half-open intervals `[start,end)` and labels `WRONG_SEQUENCE`, `SKIPPED_STEP`, `REPEATED_STEP`, `UNEXPECTED_ACTION`, `NO_VIOLATION`, or `AMBIGUOUS`. Add `TOO_FAST`/`TOO_SLOW` only when the approved SOP has timing limits. A process owner must review the semantic label. This annotation is optional for action baseline metrics; absent it, real process precision/recall stays **NOT EVALUATED**.

## Resume sequence

After the feature archive passes preflight: run the retained FramewiseBaseline and our MS-TCN on the frozen procedure-scoped subset; select checkpoints on validation only; freeze configuration; then run final test once, calculate compatible segmentation metrics, and save per-class and timeline outputs. Do not call our MS-TCN an official IMPACT TAS-S baseline. If CPU runtime is not practical, provide the ready-to-run command/log and repeat on the RTX 5060 PC when available.
