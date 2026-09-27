# CP06 MS-TCN Action Error Analysis

Scope: frozen CP05 MS-TCN frame predictions versus official TAS-S labels on the four held-out S2 executions. This is action-label error analysis, not process compliance evaluation.

## Metrics

| Aggregation | Accuracy | Macro-F1 | Edit | F1@10 | F1@25 | F1@50 | GT segments | Predicted segments |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Framewise equal-execution mean | 0.445 | 0.319 | 11.70 | 0.149 | 0.094 | 0.032 | — | — |
| Framewise pooled | 0.412 | 0.306 | 10.52 | 0.135 | 0.087 | 0.031 | 97 | 865 |
| Equal-execution mean | 0.569 | 0.390 | 50.39 | 0.445 | 0.445 | 0.207 | — | — |
| Pooled frames | 0.522 | 0.361 | 50.00 | 0.432 | 0.432 | 0.193 | 97 | 79 |

Per-execution metrics, including segment counts, are in `action_metrics.json`. Sample standard deviation over the four execution metrics: 
frame_accuracy=0.233, macro_f1_actions=0.196, normalized_edit_score=7.620, F1@10=0.139, F1@25=0.139, F1@50=0.146.

## Mismatch runs

Detected **159** contiguous raw-frame mismatch runs. Counts by exclusive primary diagnostic label: NULL/background leakage 9, boundary error 67, class confusion 63, rare-class failure 2, short-action failure 18.

| Rank | GT → prediction | Mismatched frames |
|---:|---|---:|
| 1 | `NULL` → `EXTRACT_BEARING_PLATE_ASSEMBLY` | 179 |
| 2 | `STORE_BEARING_PLATE_ASSEMBLY` → `DETACH_ADAPTER_PLATE` | 169 |
| 3 | `REMOVE_LOCKING_LEVER_ASSEMBLY` → `EXTRACT_BEARING_PLATE_ASSEMBLY` | 138 |
| 4 | `NULL` → `DETACH_ADAPTER_PLATE` | 127 |
| 5 | `REMOVE_ROTOR_ASSEMBLY` → `NULL` | 86 |
| 6 | `EXTRACT_BEARING_PLATE_ASSEMBLY` → `REMOVE_LOCKING_LEVER_ASSEMBLY` | 76 |
| 7 | `NULL` → `REMOVE_ROTOR_ASSEMBLY` | 55 |
| 8 | `STORE_ADAPTER_PLATE` → `DETACH_ADAPTER_PLATE` | 45 |
| 9 | `NULL` → `STORE_ROTOR_ASSEMBLY` | 45 |
| 10 | `REMOVE_ROTOR_ASSEMBLY` → `EXTRACT_BEARING_PLATE_ASSEMBLY` | 38 |

## Class profile

| Group | Action | Support (frames) | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|
| Strong | `EXTRACT_BEARING_PLATE_ASSEMBLY` | 696 | 0.596 | 0.799 | 0.683 |
| Strong | `DETACH_ADAPTER_PLATE` | 418 | 0.511 | 0.916 | 0.656 |
| Strong | `REMOVE_ROTOR_ASSEMBLY` | 353 | 0.709 | 0.606 | 0.653 |
| Strong | `START_ANGLE_GRINDER_ASSEMBLY` | 36 | 0.571 | 0.556 | 0.563 |
| Weak | `STORE_GEARBOX_HOUSING` | 6 | 0.000 | 0.000 | 0.000 |
| Weak | `STORE_TOOL` | 30 | 0.000 | 0.000 | 0.000 |
| Weak | `STORE_ANTI_VIBRATION_HANDLE` | 34 | 0.111 | 0.029 | 0.047 |
| Weak | `STORE_BEARING_PLATE_ASSEMBLY` | 216 | 0.239 | 0.097 | 0.138 |
| Weak | `STORE_ROTOR_ASSEMBLY` | 39 | 0.175 | 0.359 | 0.235 |

Additional patterns: pooled predicted action segments = 79 versus 97 GT segments (net under-segmentation by count), while one of four executions has more predicted than GT segments. That is not proof that all errors are merges/fragments. See `execution_diagnostics` for counts. Rule-based multi-tags: NULL/background leakage 96, boundary error 135, class confusion 63, rare-class failure 71, short-action failure 30.

Post-decoding comparison: temporal smoothing/short-segment processing changed 3 raw-correct frames to decoded-wrong and corrected 2 raw-wrong frames. This is a descriptive sample-level observation, not a tuning decision.

`likely_visual_reason` and bottleneck attribution remain UNKNOWN / HUMAN_REVIEW_REQUIRED in `action_error_events.json`. Raw neural output cannot establish visibility, occlusion, annotation correctness, or camera ambiguity. Visual ambiguity and insufficient observation are reserved for human review. No duration or process anomaly metrics were evaluated.
