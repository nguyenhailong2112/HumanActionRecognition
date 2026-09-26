from __future__ import annotations

import argparse
from datetime import date
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config  # noqa: E402


def validate_workflow(workflow_config: dict, action_vocabulary: set[str]) -> list[str]:
    errors = []
    workflow = workflow_config.get("workflow", workflow_config)
    if not workflow.get("id"):
        errors.append("workflow.id is required")
    if not workflow.get("version") or str(workflow.get("version")).startswith("<"):
        errors.append("workflow.version must identify the approved SOP/revision")
    for field in ("approved_by", "approved_on"):
        if not workflow.get(field) or str(workflow.get(field)).startswith("<"):
            errors.append(f"workflow.{field} is required")
    if workflow.get("approved_on"):
        try:
            date.fromisoformat(str(workflow["approved_on"]))
        except ValueError:
            errors.append("workflow.approved_on must use ISO YYYY-MM-DD")
    actions = set(workflow.get("action_vocabulary", []))
    if not actions:
        errors.append("workflow.action_vocabulary is required")
    unknown_actions = actions - action_vocabulary
    if unknown_actions:
        errors.append(f"workflow contains actions outside the TAS-S vocabulary: {sorted(unknown_actions)}")
    disposition = workflow.get("action_disposition", {})
    if set(disposition) != action_vocabulary:
        errors.append(f"action_disposition must classify every non-background TAS-S action; missing={sorted(action_vocabulary - set(disposition))}, extra={sorted(set(disposition) - action_vocabulary)}")
    allowed_dispositions = {"required", "optional", "conditional", "rework", "out_of_scope"}
    statuses = {}
    for action, entry in disposition.items():
        status = entry.get("status") if isinstance(entry, dict) else entry
        statuses[action] = status
        if status not in allowed_dispositions:
            errors.append(f"action_disposition for {action} must be one of {sorted(allowed_dispositions)}")
        if status in {"conditional", "out_of_scope"} and isinstance(entry, dict) and not entry.get("reason"):
            errors.append(f"action_disposition for {action} needs a reason")
    paths = workflow.get("valid_paths", [])
    if not paths:
        errors.append("workflow.valid_paths must define at least one process-owner-approved path")
    path_ids = [path.get("id") for path in paths]
    if any(not value for value in path_ids) or len(path_ids) != len(set(path_ids)):
        errors.append("valid_paths need unique, non-empty ids")
    for path in paths:
        steps = path.get("steps", [])
        if not steps:
            errors.append(f"valid path {path.get('id')} has no steps")
        invalid = set(steps) - actions
        if invalid:
            errors.append(f"valid path {path.get('id')} uses unknown actions: {sorted(invalid)}")
        out_of_scope_steps = set(steps) & {name for name, status in statuses.items() if status == "out_of_scope"}
        if out_of_scope_steps:
            errors.append(f"valid path {path.get('id')} uses actions marked out_of_scope: {sorted(out_of_scope_steps)}")
    if any(status != "out_of_scope" for status in statuses.values()) and actions != {name for name, status in statuses.items() if status != "out_of_scope"}:
        errors.append("action_vocabulary must list exactly the actions whose disposition is not out_of_scope")
    completion = workflow.get("completion", {})
    if not isinstance(completion, dict) or not completion.get("condition"):
        errors.append("workflow.completion.condition must describe the SOP-approved completion criterion")
    optional_steps = workflow.get("optional_steps", [])
    if len(optional_steps) != len(set(optional_steps)):
        errors.append("optional_steps contains duplicates")
    if set(optional_steps) - actions:
        errors.append(f"optional_steps contains unknown/out-of-scope actions: {sorted(set(optional_steps) - actions)}")
    if set(optional_steps) - {name for name, status in statuses.items() if status == "optional"}:
        errors.append("every optional_steps entry must have optional disposition")
    route_edges = {
        (source, target)
        for path in paths
        for source, target in zip(path.get("steps", []), path.get("steps", [])[1:])
    }
    if "valid_transitions" in workflow:
        declared_edges = []
        for edge in workflow["valid_transitions"]:
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                errors.append(f"invalid transition {edge!r}; expected [from_action, to_action]")
                continue
            pair = (edge[0], edge[1])
            declared_edges.append(pair)
            if set(pair) - actions:
                errors.append(f"transition {pair!r} uses unknown/out-of-scope action")
        if len(declared_edges) != len(set(declared_edges)):
            errors.append("valid_transitions contains duplicates")
        if set(declared_edges) != route_edges:
            errors.append(f"valid_transitions must exactly match reachable adjacent route transitions; missing={sorted(route_edges - set(declared_edges))}, unreachable={sorted(set(declared_edges) - route_edges)}")
    for field in ("conditional_paths", "rework_paths"):
        references = set()
        for entry in workflow.get(field, []):
            if not isinstance(entry, dict) or not entry.get("path_id") or not entry.get("condition"):
                errors.append(f"{field} entries require path_id and an SOP-backed condition")
                continue
            references.add(entry["path_id"])
            if entry["path_id"] not in path_ids:
                errors.append(f"{field} references undefined valid path {entry['path_id']}")
        if len(references) != len(workflow.get(field, [])):
            errors.append(f"{field} contains duplicate or malformed path references")
    limits = workflow.get("duration_limits_seconds", {})
    for action, bounds in limits.items():
        if action not in action_vocabulary:
            errors.append(f"duration rule references unknown action: {action}")
        if not isinstance(bounds, dict) or "min" not in bounds or "max" not in bounds:
            errors.append(f"duration rule for {action} needs min and max")
        elif float(bounds["min"]) < 0 or float(bounds["max"]) < float(bounds["min"]):
            errors.append(f"duration rule for {action} has invalid bounds")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a process-owner-approved workflow against the CP01.1 action vocabulary.")
    parser.add_argument("--config", required=True, help="Approved workflow YAML")
    parser.add_argument("--actions-config", default="configs/cp01_1.yaml")
    args = parser.parse_args()
    workflow_config = load_config(Path(args.config).resolve())
    actions_config = load_config(Path(args.actions_config).resolve())
    vocabulary = set(actions_config["actions"]["class_order"]) - {actions_config["actions"]["background"]}
    errors = validate_workflow(workflow_config, vocabulary)
    if errors:
        print("Workflow validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"[ok] approved workflow {workflow_config.get('workflow', workflow_config)['id']} covers {len(vocabulary)} TAS-S action labels")


if __name__ == "__main__":
    main()
