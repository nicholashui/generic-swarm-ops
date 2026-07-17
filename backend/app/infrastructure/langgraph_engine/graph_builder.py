"""Build real LangGraph StateGraph apps — LG-04."""

from __future__ import annotations

from typing import Any, Callable

from langgraph.graph import END, START, StateGraph


def build_pipeline_graph(step_ids: list[str], node_fn: Callable[[str], Callable[[dict], dict]]) -> Any:
    """Compile a linear StateGraph; each step_id is a node."""
    builder = StateGraph(dict)
    if not step_ids:

        def _empty(state: dict) -> dict:
            return {**state, "status": "completed"}

        builder.add_node("empty", _empty)
        builder.add_edge(START, "empty")
        builder.add_edge("empty", END)
        return builder.compile()

    for sid in step_ids:
        builder.add_node(sid, node_fn(sid))

    builder.add_edge(START, step_ids[0])
    for i in range(len(step_ids) - 1):
        builder.add_edge(step_ids[i], step_ids[i + 1])
    builder.add_edge(step_ids[-1], END)
    return builder.compile()
