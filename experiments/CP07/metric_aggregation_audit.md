# CP07 Metric Aggregation Audit

Source: `src/human_action/metrics.py::action_metrics` and `tools/analyze_cp06.py::summarize`.

| Quantity | Exact aggregation |
|---|---|
| Pooled Accuracy | Sum of correct frame predictions across executions / sum of evaluated frames. |
| Pooled Macro-F1 | Recompute class TP/FP/FN from the sum of each execution's confusion matrix; average class F1 for non-background classes with any pooled GT support. Unsupported classes are excluded; supported-but-never-predicted classes contribute zero. |
| Pooled Edit | For each execution independently, remove NULL segments, compute sequence Levenshtein distance `d_i` and denominator `max(GT_segments_i, Pred_segments_i, 1)`. Report `100 * (1 - sum(d_i)/sum(denominator_i))`. No cross-execution adjacency. |
| Pooled F1@10/25/50 | Sum each execution's same-class greedy segment-match TP/FP/FN at the IoU threshold, then `2ΣTP/(2ΣTP+ΣFP+ΣFN)`. Matching never crosses executions. |
| Equal-execution mean | Arithmetic mean of the four independently computed execution metrics. |
| Sample standard deviation | `numpy.std(values, ddof=1)` across the four executions. |

`summarize` currently concatenates labels only to obtain frame confusion counts. That operation cannot create temporal matches for reported Edit/F1: those are overwritten from per-execution aggregates before return. The deterministic test `test_pooled_temporal_metrics_keep_execution_boundaries` uses two separate `[A,A]` executions: correct aggregation retains two GT action segments, while naïve concatenation merges them into one, demonstrating the boundary error directly.

Current frozen CP06 pooled values remain the source results: accuracy .522, macro-F1 .361, Edit 50.00, F1@10/.25/.50 .432/.432/.193. Equal-execution mean and sample SD are recorded in `experiments/CP06/action_metrics.json`; no metric definition changed in CP07.
