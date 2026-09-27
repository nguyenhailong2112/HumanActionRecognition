# CP05 Metric Definition Audit

Source of truth: `src/human_action/metrics.py` and `tools/compare_baselines.py`.

| Metric | Implemented definition | Aggregation caveat |
|---|---|---|
| Frame Accuracy | Number of equal frame labels divided by evaluated frame count; sequences are truncated to the shorter length by `action_metrics` (the dataset path separately enforces alignment). | CP05 comparison is unweighted mean of per-execution values. Pooled accuracy concatenates all frames and weights by length. |
| Macro-F1 | Per-class F1 from frame counts; arithmetic mean over non-background classes with at least one GT frame in that execution. A class with GT support but no prediction contributes zero. Unsupported GT classes are excluded from that execution's macro denominator. | Per-execution mean differs from pooled macro F1; pooled calculation uses every non-background class supported anywhere in pooled GT. |
| Edit | RLE action-label sequence Levenshtein similarity: `100*(1-distance/max(number_gt_segments, number_pred_segments, 1))`. Background/NULL segments are removed before sequence comparison. | Computed separately per execution; CP05 reports unweighted mean. |
| Segmental F1@10/25/50 | RLE segments excluding background; same-class segment pairs only; intersection-over-union threshold 0.10/0.25/0.50; each predicted segment matched at most once. For each GT segment implementation takes its highest-IoU still-unmatched same-class prediction, then computes `2TP/(2TP+FP+FN)`. | Greedy GT-order matching, per execution. CP05 averages four execution F1 values equally. This is not framewise F1. |
| Segment counts | Number of RLE non-background GT/prediction segments. | Per execution. |

The implementation is explicit and internally consistent with the documented CP05 protocol. Caveats: the edit score is a normalized sequence score in [0,100]; it is not the official IMPACT leaderboard metric. Segment matching is greedy rather than a global assignment. The CP05 mean is not a pooled result. CP06 pooled frame accuracy/per-class metrics use all frames; pooled Edit sums each execution's Levenshtein distance and normalization denominator before recomputing the normalized score; pooled segment F1 sums per-execution TP/FP/FN. Sequence boundaries are preserved for pooled sequence metrics. CP06 also reports equal-execution mean/sample SD; no metric change or test tuning is introduced.
