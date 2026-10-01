from __future__ import annotations

import argparse
from datetime import date
import math
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.config import load_config  # noqa: E402


def validate_workflow(workflow_config: dict, action_vocabulary: set[str]) -> list[str]:
    errors = []
    workflow = workflow_config.get("workflow", workflow_config)
    if "enabled" in workflow and not isinstance(workflow["enabled"], bool):
        errors.append("workflow.enabled must be a boolean")
    if workflow.get("status") != "HUMAN_VALIDATED":
        errors.append("workflow.status must be HUMAN_VALIDATED before executable validation")
    if not workflow.get("id"):
        errors.append("workflow.id is required")
    if not workflow.get("version") or str(workflow.get("version")).startswith("<"):
        errors.append("workflow.version must identify the reviewed specification/source revision")
    for field in ("approved_by", "approved_on"):
        if not workflow.get(field) or str(workflow.get(field)).startswith("<"):
            errors.append(f"workflow.{field} is required")
    if workflow.get("approved_on"):
        try:
            date.fromisoformat(str(workflow["approved_on"]))
        except ValueError:
            errors.append("workflow.approved_on must use ISO YYYY-MM-DD")
    raw_actions = workflow.get("action_vocabulary", [])
    if not isinstance(raw_actions, list) or any(not isinstance(x, str) for x in raw_actions):
        errors.append("workflow.action_vocabulary must be a list of action IDs")
        raw_actions = []
    actions = set(raw_actions)
    if len(raw_actions) != len(actions):
        errors.append("workflow.action_vocabulary contains duplicate action IDs")
    if not actions:
        errors.append("workflow.action_vocabulary is required")
    project_model_actions = set(action_vocabulary)
    unknown_actions = actions - project_model_actions
    if unknown_actions:
        errors.append(f"workflow contains actions outside the supplied project/model action scope: {sorted(unknown_actions)}")
    disposition = workflow.get("action_disposition", {})
    if set(disposition) != project_model_actions:
        errors.append(f"action_disposition must classify every non-background action in the supplied project/model scope; missing={sorted(project_model_actions - set(disposition))}, extra={sorted(set(disposition) - project_model_actions)}")
    allowed_dispositions = {"required", "optional", "conditional", "rework", "out_of_scope"}
    statuses = {}
    for action, entry in disposition.items():
        status = entry.get("status") if isinstance(entry, dict) else entry
        statuses[action] = status
        if status not in allowed_dispositions:
            errors.append(f"action_disposition for {action} must be one of {sorted(allowed_dispositions)}")
        if status in {"conditional", "out_of_scope"} and isinstance(entry, dict) and not entry.get("reason"):
            errors.append(f"action_disposition for {action} needs a reason")
    partial_order = "prerequisites" in workflow
    paths = workflow.get("valid_paths", [])
    if not isinstance(paths, list):
        errors.append("workflow.valid_paths must be a list")
        paths = []
    if not paths and not partial_order:
        errors.append("workflow.valid_paths must define at least one process-owner-approved path")
    if paths and partial_order:
        errors.append("choose one workflow representation: valid_paths or prerequisites, not both")
    path_ids = [path.get("id") for path in paths]
    if any(not value for value in path_ids) or len(path_ids) != len(set(path_ids)):
        errors.append("valid_paths need unique, non-empty ids")
    for path in paths:
        if not isinstance(path, dict):
            errors.append(f"valid path entry must be a mapping; found {path!r}")
            continue
        steps = path.get("steps", [])
        if not isinstance(steps, list) or any(not isinstance(step, str) for step in steps):
            errors.append(f"valid path {path.get('id')} steps must be a list of action IDs")
            steps = []
        if not steps:
            errors.append(f"valid path {path.get('id')} has no steps")
        invalid = set(steps) - actions
        if invalid:
            errors.append(f"valid path {path.get('id')} uses unknown actions: {sorted(invalid)}")
        out_of_scope_steps = set(steps) & {name for name, status in statuses.items() if status == "out_of_scope"}
        if out_of_scope_steps:
            errors.append(f"valid path {path.get('id')} uses actions marked out_of_scope: {sorted(out_of_scope_steps)}")
    required_actions = set()
    if partial_order:
        raw_required = workflow.get("required_actions")
        if not isinstance(raw_required, list) or not raw_required or any(not isinstance(x, str) for x in raw_required):
            errors.append("workflow.required_actions must be a non-empty list of action IDs for prerequisite workflows")
        else:
            required_actions = set(raw_required)
            if len(raw_required) != len(required_actions):
                errors.append("workflow.required_actions contains duplicates")
            if required_actions - actions:
                errors.append(f"required_actions contains unknown/out-of-scope actions: {sorted(required_actions - actions)}")
        raw_prerequisites = workflow.get("prerequisites")
        if not isinstance(raw_prerequisites, dict) or not raw_prerequisites:
            errors.append("workflow.prerequisites must be a non-empty action-to-prerequisite mapping")
            raw_prerequisites = {}
        if required_actions and set(raw_prerequisites) != required_actions:
            errors.append("prerequisites must define every and only required action")
        graph = {}
        for action, prerequisites in raw_prerequisites.items():
            if action not in actions:
                errors.append(f"prerequisites defines unknown action: {action}")
            if not isinstance(prerequisites, list) or any(not isinstance(item, str) for item in prerequisites):
                errors.append(f"prerequisites for {action} must be a list of action IDs")
                continue
            if len(prerequisites) != len(set(prerequisites)):
                errors.append(f"prerequisites for {action} contains duplicates")
            if action in prerequisites:
                errors.append(f"action {action} cannot be its own prerequisite")
            unknown = set(prerequisites) - actions
            if unknown:
                errors.append(f"prerequisites for {action} references unknown actions: {sorted(unknown)}")
            if required_actions and (set(prerequisites) - required_actions):
                errors.append(f"prerequisites for {action} references actions not in required_actions: {sorted(set(prerequisites) - required_actions)}")
            graph[action] = set(prerequisites)
        visiting, visited = set(), set()
        def visit(action):
            if action in visiting:
                return True
            if action in visited:
                return False
            visiting.add(action)
            cyclic = any(visit(item) for item in graph.get(action, set()) if item in graph)
            visiting.remove(action)
            visited.add(action)
            return cyclic
        if any(visit(action) for action in graph if action not in visited):
            errors.append("prerequisites contains a cycle; no valid completion order exists")
    workflow_actions = {name for name, status in statuses.items() if status != "out_of_scope"}
    if actions != workflow_actions:
        errors.append(
            "action_vocabulary must list exactly project/model actions whose disposition is not out_of_scope; "
            f"missing={sorted(workflow_actions - actions)}, extra={sorted(actions - workflow_actions)}"
        )
    completion = workflow.get("completion", {})
    if not isinstance(completion, dict) or not completion.get("condition"):
        errors.append("workflow.completion.condition must describe the process-owner-approved completion criterion")
    optional_steps = workflow.get("optional_steps", [])
    if not isinstance(optional_steps, list):
        errors.append("optional_steps must be a list")
        optional_steps = []
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
    if "valid_transitions" in workflow and not partial_order:
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
        entries = workflow.get(field, [])
        if not isinstance(entries, list):
            errors.append(f"{field} must be a list")
            entries = []
        for entry in entries:
            if not isinstance(entry, dict) or not entry.get("path_id") or not entry.get("condition"):
                errors.append(f"{field} entries require path_id and a process-owner-supported condition")
                continue
            if field == "conditional_paths" and not entry.get("condition_id"):
                errors.append("conditional_paths entries also require a stable condition_id for the explicit runtime decision input")
            references.add(entry["path_id"])
            if entry["path_id"] not in path_ids:
                errors.append(f"{field} references undefined valid path {entry['path_id']}")
        if len(references) != len(workflow.get(field, [])):
            errors.append(f"{field} contains duplicate or malformed path references")
    limits = workflow.get("duration_limits_seconds", {})
    if limits is None:
        limits = {}
    if not isinstance(limits, dict):
        errors.append("duration_limits_seconds must be a mapping or null (disabled)")
        limits = {}
    for action, bounds in limits.items():
        if action not in action_vocabulary:
            errors.append(f"duration rule references unknown action: {action}")
        if not isinstance(bounds, dict) or "min" not in bounds or "max" not in bounds:
            errors.append(f"duration rule for {action} needs min and max")
        else:
            try:
                minimum, maximum = float(bounds["min"]), float(bounds["max"])
                if not math.isfinite(minimum) or not math.isfinite(maximum) or minimum < 0 or maximum < minimum:
                    errors.append(f"duration rule for {action} has invalid finite bounds (require 0 <= min <= max)")
            except (TypeError, ValueError):
                errors.append(f"duration rule for {action} bounds must be numeric")
    timeout = workflow.get("timeout_policy", {"enabled": bool(limits)})
    if not isinstance(timeout, dict) or not isinstance(timeout.get("enabled"), bool):
        errors.append("timeout_policy must be a mapping with boolean enabled")
    elif timeout["enabled"]:
        if not timeout.get("source"):
            errors.append("enabled timeout_policy requires a source")
        try:
            seconds = float(timeout.get("seconds"))
            if not math.isfinite(seconds) or seconds <= 0:
                errors.append("enabled timeout_policy.seconds must be a positive finite number")
        except (TypeError, ValueError):
            errors.append("enabled timeout_policy.seconds must be a positive finite number")
    duration_policy = workflow.get("duration_policy")
    if duration_policy is not None:
        if not isinstance(duration_policy, dict) or not isinstance(duration_policy.get("enabled"), bool):
            errors.append("duration_policy must be a mapping with boolean enabled")
        elif duration_policy["enabled"]:
            if not duration_policy.get("source"):
                errors.append("enabled duration_policy requires an authoritative source")
            rules = duration_policy.get("rules")
            if not isinstance(rules, dict):
                errors.append("enabled duration_policy.rules must be a mapping")
            else:
                for action, bounds in rules.items():
                    if action not in action_vocabulary:
                        errors.append(f"duration rule references unknown action: {action}")
                    if not isinstance(bounds, dict) or "min" not in bounds or "max" not in bounds:
                        errors.append(f"duration rule for {action} needs min and max")
                        continue
                    try:
                        lo, hi = float(bounds["min"]), float(bounds["max"])
                        if not math.isfinite(lo) or not math.isfinite(hi) or lo < 0 or hi < lo:
                            errors.append(f"duration rule for {action} has invalid finite bounds (require 0 <= min <= max)")
                    except (TypeError, ValueError):
                        errors.append(f"duration rule for {action} bounds must be numeric")

    # Optional graph form supports explicit state IDs and transition endpoints.
    # The current engine executes approved valid_paths; graph form is validated
    # when supplied so malformed future specs fail before being consumed.
    if "states" in workflow or "transitions" in workflow:
        states = workflow.get("states", [])
        transitions = workflow.get("transitions", [])
        if not isinstance(states, list) or not isinstance(transitions, list):
            errors.append("states and transitions must both be lists")
            states, transitions = [], []
        state_ids = [s.get("id") for s in states if isinstance(s, dict)]
        if len(state_ids) != len(states):
            errors.append("every state must be a mapping with an id")
        if any(not sid for sid in state_ids) or len(state_ids) != len(set(state_ids)):
            errors.append("state IDs must be unique and non-empty")
        state_map = {s.get("id"): s for s in states if isinstance(s, dict) and s.get("id")}
        state_ids_by_action = {}
        for sid, state in state_map.items():
            action = state.get("action")
            if action is not None and action not in actions:
                errors.append(f"state {sid} references unknown action {action}")
            if action is not None:
                state_ids_by_action.setdefault(action, set()).add(sid)
        edges = []
        for edge in transitions:
            if not isinstance(edge, dict) or not edge.get("from") or not edge.get("to"):
                errors.append("each transition must be a mapping with from and to state IDs")
                continue
            pair = (edge["from"], edge["to"])
            edges.append(pair)
            if pair[0] not in state_map or pair[1] not in state_map:
                errors.append(f"transition {pair!r} references an undefined state")
            if edge.get("conditional") is True and not edge.get("condition"):
                errors.append(f"conditional transition {pair!r} requires an explicit condition")
            if edge.get("conditional") not in (None, True, False):
                errors.append(f"transition {pair!r} conditional must be boolean")
        if len(edges) != len(set(edges)):
            errors.append("transitions contains duplicate from/to edges")
        for path in paths:
            if not isinstance(path, dict) or not isinstance(path.get("steps"), list):
                continue
            steps = path["steps"]
            for action in steps:
                if action not in state_ids_by_action:
                    errors.append(f"valid path {path.get('id')} action {action} has no configured state")
            for before, after in zip(steps, steps[1:]):
                possible_pairs = {(left, right) for left in state_ids_by_action.get(before, set()) for right in state_ids_by_action.get(after, set())}
                if possible_pairs and not possible_pairs.intersection(set(edges)):
                    errors.append(f"valid path {path.get('id')} transition {before} -> {after} is missing from transitions")
        start, terminals = workflow.get("start_state"), workflow.get("terminal_states", [])
        if start not in state_map:
            errors.append("start_state must reference a defined state")
        if not isinstance(terminals, list) or not terminals or set(terminals) - set(state_map):
            errors.append("terminal_states must be a non-empty list of defined state IDs")
            terminals = []
        reachable = set()
        if start in state_map:
            todo = [start]
            while todo:
                current = todo.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                todo.extend(target for source, target in edges if source == current and target in state_map)
        unreachable = set(state_map) - reachable
        if unreachable:
            errors.append(f"unreachable states: {sorted(unreachable)}")
        if terminals and not (set(terminals) & reachable):
            errors.append("no configured terminal state is reachable from start_state")
        outgoing = {source for source, _ in edges}
        if terminals and any(terminal in outgoing for terminal in terminals):
            errors.append("terminal states cannot have outgoing transitions")
        if not terminals or not any(terminal in reachable for terminal in terminals):
            errors.append("impossible terminal configuration: at least one reachable terminal state is required")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a human-reviewed research workflow against the configured project model action scope.")
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
    print(f"[ok] approved workflow {workflow_config.get('workflow', workflow_config)['id']} covers {len(vocabulary)} configured project/model actions (from {args.actions_config})")


if __name__ == "__main__":
    main()
