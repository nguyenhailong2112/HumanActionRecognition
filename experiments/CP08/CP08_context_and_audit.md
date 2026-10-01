# CP08 Context and Audit

Audit performed 2026-10-01 before implementation changes. The repository and its current artifacts were inspected directly.

## Current repository and baseline

- `.git/HEAD` points to `refs/heads/main`; `.git/refs/heads/main` is **`a3de0d822dbcf364f291fd67cdf340a1a887c3b1`**, matching the supplied current HEAD.
- Baseline command: `\.venv-cp05\Scripts\python.exe -m unittest discover -s tests -v`.
- Baseline result observed before CP08 changes: **63 tests passed**.
- Existing experiment is IMPACT v1.1 TAS-S, S2/split 2, `Disassembly_A/front`, 39/5/4 executions, held-out worker `SS07EL13`; CP05 seed-17 MS-TCN is the frozen action baseline.
- Environment versions/GPU listed in prior experiment reports are historical recorded environment evidence; this audit did not rerun the hardware inventory.

## CP05/CP06 provenance and frozen artifacts

- CP05, CP06 and CP07 reports, training/evaluation outputs, timelines, seed records and model checkpoints exist. No retraining is in CP08 scope.
- Historical CP05 report says the I3D ZIP was absent at that checkpoint; CP06 later records successful SHA-256/official structure and CRC verification. This is a resolved historical status, not a current acquisition blocker.
- Frozen-file hashes captured for audit reference:
  - `models/cp05_mstcn_best.pt`: `2e1f06a248973dad925f449ad9588064bbade4f9c2f4ed9c961a5196008f567d`
  - `models/cp05_framewise_best.pt`: `c3f0089d2d942856420954a636a3f02ec8ba661dcc531ae7afa2e8e37c7739a3`
  - `experiments/CP06/action_metrics.json`: `9179bccc5698e242fe628944b66b07abab4b23d14861a97ff3e690a441aa7605`
  - `experiments/CP06/seed_reliability.json`: `f1119402de1338208ad4a4188e1adf2b49ff0d4b41367a01d45e042bfc024ea3`
- CP08 will not write into CP05/CP06 result directories or replace checkpoints.

## Current ActionEvent, workflow, and evidence path

- `ActionEvent` in `src/human_action/schemas.py` carries worker, action, interval, confidence, execution/video ID, frames, evidence status, view, deterministic event ID and evidence references. `to_action_events()` excludes NULL, emits evidence status `unknown`, and does not infer evidence sufficiency from confidence.
- Frozen CP05 MS-TCN timelines contain 24, 18, 13 and 14 action events for held-out executions 001–004 respectively (**69 total**). These are saved CP05 prediction products; CP08 may serialize them without rerunning inference.
- `experiments/CP05/evidence_index.json` contains **69** evidence records. Matching the frozen events by `(video_id, action, start_frame)` yields a unique one-to-one match for all 69; all indexed source videos, snapshots and clips exist. Matching is a technical link, not a semantic review.
- CP07 evidence review manifest contains 21 category selections deduplicated to **13** unique events, all `HUMAN_REVIEW_REQUIRED`. No `human_evidence_review.csv` or equivalent reviewer judgment artifact was found. The CP07 handoff is a request, not completed review.
- Workflow code is separated from prediction code and consumes structured events. The current finalizer, however, emits `INCOMPLETE_PROCEDURE` for every non-completed state at finalization. The API does not establish that a video/observation boundary means the physical procedure ended; this conflates an unconfirmed/incomplete observation with a proven procedure ending early. CP08 will correct this with an explicit end-of-procedure signal and a neutral unconfirmed-observation status.

## Workflow validation state

- `configs/workflows/disassembly_A.yaml` is absent.
- `configs/workflows/disassembly_A.draft.yaml` is present, explicitly `HUMAN_REVIEW_REQUIRED`, with no executable transitions.
- `configs/cp05.yaml` keeps workflow `enabled: false` and `status: HUMAN_REVIEW_REQUIRED`.
- CP07.1 implemented route and prerequisite-DAG capabilities, but neither representation supplies approved `Disassembly_A` semantics. Real workflow execution remains gated; process metrics remain `NOT_EVALUATED`.

## Semantic document authority and reconciliation

1. `HumanSemanticWorksheet.md` is the human-owned blank review/gating form. It remains `HUMAN_REVIEW_REQUIRED`; its semantic fields and final decision are unfilled.
2. `HumanSemanticWorksheet_CP07_source_grounded_draft.md` is a research-prepared proposal that distinguishes DG, DO, INT and HUMAN. It carefully labels semantic workflow roles as human decisions and says it is not executable.
3. `HumanSemanticWorksheetReconstructedProjectGroundTruth.md` is a richer **research-derived/project-level reconstruction** (RD/POL), not official IMPACT author ground truth and not owner approval. It proposes core component objectives, partial ordering, recovery and terminal-state semantics; these cannot be silently promoted to executable policy.

Direct official-source inspection confirms:

- Official TAS-S mapping has 25 non-background IDs plus NULL. The local project uses the observed 17 non-background action subset; absence from this subset is not proof that other official labels are irrelevant.
- Official PSR graph metadata (`procedure_graph.json`) states edges are robust prerequisites mined from data and a missing edge means flexible ordering. It contains distinct `*_remove_ok` and `*_recover_ok` nodes. The inspected `adapter_plate__recover_ok` and `bearing_plate__recover_ok` have prerequisites, whereas their corresponding `*_remove_ok` entries are empty. Recovery prerequisites therefore cannot be copied into normal removal rules.
- PSR is a component-state task separate from TAS-S; PPR labels NORMAL/ANOMALY/RECOVERY are procedural-phase labels, not matching event-level process-violation ground truth.
- TAS-S `STORE_GEARBOX_HOUSING` is a storage action. The label is not itself the separate PSR `Remove gearbox_housing` event. A gearbox-removed objective is not certifiable from this action alone without an explicit reviewed bridge or another observation.

## Contradictions / limitations found

- CP05's ZIP status is stale only when read without the later CP06 resolution; the chronology is consistent.
- The reconstructed worksheet uses the phrase “project-level reconstructed semantic specification/ground truth” and includes a compact intended semantic specification, but its final section explicitly says executable workflow is not activated and process compliance is not evaluated. CP08 treats its content as RD/POL proposals, not approval.
- No matching process ground truth or evidence reviewer judgments exist in the inspected repository. No process metric can be evaluated.
- CP07.1 did not resolve the observation-end vs procedure-end finalization distinction; this is a confirmed implementation issue addressed in CP08.

## CP08 execution boundary

Proceed on the no-validated-workflow branch. Reconcile semantics without activating them; generate ActionEvents from the frozen CP05 prediction timelines and verify their existing evidence links; prepare exact human workflow/evidence handoffs; correct finalization semantics and test it. Do not create executable YAML, infer state effects from storage labels, convert PSR recover prerequisites to remove prerequisites, modify official annotations, retrain, change frozen metrics, or claim real process traces/compliance.
