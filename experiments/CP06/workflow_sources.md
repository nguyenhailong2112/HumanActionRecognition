# Research Workflow Specification / Benchmark Procedure Interpretation — Sources

| Source | Location | Relevant information | Confidence | Unresolved interpretation |
|---|---|---|---|---|
| IMPACT v1.1 release documentation and task code | `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/` | Defines dataset tasks and released action/procedure data. TAS-S is temporal action segmentation with per-frame action labels and official split files. | High for dataset/task/split facts. | Does not establish a process-owner-approved compliance route for this research interpretation. |
| TAS-S labels and protocol | `.../dataset/TAS/` including `splits_TAS-S/`; locally frozen through `configs/cp05.yaml` | Supplies action vocabulary, annotations and S2 membership. CP05 subset has 17 observed non-background labels plus NULL. | High for labels and membership. | Labels describe observed action intervals; they do not by themselves define mandatory/optional steps, valid transitions, retries, or compliance. |
| IMPACT PSR documentation and graph | `ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/PSR/README.md`; `.../tasks/PSR/gemini_3_1_pro/configs/procedure_graph.json` | PSR is a distinct component-state relation task. Graph description says edges are robust prerequisites mined from data; absence of edge means flexible ordering. | High that this is a data-mined component prerequisite graph for PSR. | Not a canonical TAS-S workflow. It cannot be converted into accepted route/compliance rules. |
| CP05 experiment protocol | `experiments/EXP-CP05.md`, `configs/cp05.yaml` | Frozen procedure-scoped research subset, action vocabulary, view, split, training/evaluation protocol. | High for our experiment setup. | No process semantics supplied. |
| CP05 human handoff | `HUMAN_HANDOFF_CP05.md` | Records the outstanding need for process-owner interpretation. | High as current repository state. | Owner's answers remain pending. |

## Grounded facts versus decisions

Grounded: dataset/procedure identifier `Disassembly_A`; front-view TAS-S action vocabulary and S2 split; actions are annotation labels; the PSR material is a separate, mined prerequisite task. Engineering candidate state IDs may mirror the released action labels for review. Human decision required: which labels are actual procedure steps, meanings/action mapping, required/optional status, ordering, branches, retries, restart/completion, evidence, unknown/out-of-view handling and any officially defined timing. No transition semantics are asserted here.
