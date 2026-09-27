# CP07 ActionEvent Contract

The existing event type is extended in place in `src/human_action/schemas.py`; perception and workflow remain separate.

| Field | Meaning / source |
|---|---|
| `worker_id` | Worker identifier from the selected execution. |
| `video_id` | Source execution identifier (the established code field). |
| `view` | Source camera/view from dataset configuration; e.g. `front`. |
| `action` | Decoded action label; NULL/background is not emitted as an action event. |
| `start_frame`, `end_frame` | Inclusive source frame indices from the segment decoder. |
| `start_time`, `end_time`, `duration` | Seconds in the source execution; end is exclusive by decoder convention. |
| `confidence` | Mean predicted probability of the predicted class over the decoded segment. This describes model confidence, not workflow validity. |
| `evidence_status` | `sufficient`, `unknown`, `ambiguous`, or `insufficient`; model-generated events default to `unknown` because CP07 has no validated confidence/evidence threshold. Non-sufficient events do not advance workflow state. |
| `event_id` | Deterministic `video_id:start-end:action` key, stable for the frozen decoded event. |
| `evidence_refs` | Optional tuple of snapshot/clip or other evidence references. CP05 stored 69 linked evidence events, but the current inference pipeline does not yet populate these references on newly generated ActionEvents. |

`to_dict` uses dataclass serialization; `ActionEvent.from_dict` restores tuple evidence references and supports round-trip. Pipeline conversion now passes configured view and populates stable event IDs. Existing positional constructor calls remain compatible because new fields are optional. Workflow output must preserve model confidence and event evidence separately from transition validity. The contract test covers conversion and serialization round-trip.

The runtime workflow gate is opt-in: omitted/false `workflow.enabled` disables process logic; `workflow.enabled: true` requires `workflow.status: HUMAN_VALIDATED`. Model-generated events carry `unknown` evidence status unless a future validated evidence policy explicitly changes it; confidence alone does not qualify evidence. CP07 also removed illustrative routes and invented duration bounds from the legacy CP01 executable config. These guards prevent an example procedure or unqualified prediction from producing apparent compliance results.
