# CP07 Action Error Structure

Scope is the frozen CP05 seed-17 MS-TCN prediction stream on four held-out executions. Source artifacts are CP06 `action_metrics.json`, `action_error_events.json`, the four CP05 prediction timelines, and the frozen test annotations loaded through the existing CP05 config. No test result was used to tune a model or workflow. Machine-readable per-execution and per-action support/frequency/duration/mismatch measurements are in `action_error_structure.json`.

## Observed facts

- Execution 001 is the weakest of the four on frame accuracy (.278), macro-F1 (.123), Edit (39.29), and segment F1; it has 28 predicted versus 23 GT action segments.
- Executions 003 and 004 have higher frame accuracy (.770/.743) and macro-F1 (.507/.562), with 18/15 predicted versus 23/23 GT segments. Execution 002 has .486 accuracy and 18 versus 28 segments.
- Three executions have fewer predicted action segments than GT; execution 001 has more. Thus segment-count bias changes by execution.
- The largest repeated frame confusions are NULL→EXTRACT_BEARING_PLATE_ASSEMBLY (179), STORE_BEARING_PLATE_ASSEMBLY→DETACH_ADAPTER_PLATE (169), and REMOVE_LOCKING_LEVER_ASSEMBLY→EXTRACT_BEARING_PLATE_ASSEMBLY (138), per CP06.
- The CP06 error-run tags include NULL/background leakage (96 tagged runs), class confusion (63), boundary error (135), short-action failure (30), and rare-class failure (71). Tags may overlap. Raw-vs-decoded comparison records 3 frames correct before decoding but wrong after, and 2 frames corrected by decoding.
- Per execution, JSON includes GT NULL share, GT/predicted segment count, duration, boundary density, mismatch runs/frames and largest confusion pairs. Per action, it includes GT support frames, GT segment frequency/duration, predicted segment frequency/duration, and framewise false-negative/false-positive counts. GT frequencies/durations use the same frozen aligned annotation labels; predicted frequencies/durations use the cached CP05 timeline.

## Interpretation limits

The execution-level comparison is descriptive with n=4. It does not show that duration, support, boundary density, NULL share, rare-class status, or a particular pair caused the metric differences. The timeline output does not retain framewise probabilities; framewise GT/prediction confusion comes from CP06's frozen evaluation report. Human inspection is required before assigning visually ambiguous causes, data/annotation fault, or observation limits. The CP07 evidence review manifest remains `HUMAN_REVIEW_REQUIRED`.

## Current inference

The records show substantial execution heterogeneity, both over- and under-segmentation, and recurrent class-pair/background confusion. They do not isolate model capacity as the root cause. Keep the current MS-TCN baseline for comparison and INVESTIGATE annotation/observation/representation through the prepared review before changing architecture.
