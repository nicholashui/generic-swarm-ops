"""Memory read + ALC inject for LangGraph pipeline — LG-08."""

from __future__ import annotations

from typing import Any


def inject_memory_hits(
    runtime: Any,
    *,
    organization_id: str,
    agent: dict[str, Any],
    workflow: dict[str, Any],
    actor_user_id: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Load scoped memory / lessons into hits list (best-effort, never raises)."""
    hits: list[dict[str, Any]] = []
    scope_aliases = {
        "event_log": "workflow_memory",
        "decision_memory": "organization_memory",
        "lessons_learned": "organization_memory",
        "contract_rules": "organization_memory",
        "customer_exceptions": "organization_memory",
        "past_failures": "organization_memory",
    }
    agent_id = agent.get("id")

    # ALC lessons (same store as legacy path)
    try:
        from app.infrastructure.self_improvement.lessons import LessonLibrary

        org_lessons = [
            i
            for i in runtime.store.collection("improvement_lessons")
            if i.get("organization_id") == organization_id
        ]
        lib = LessonLibrary(org_lessons)
        injected = lib.retrieve(
            agent_id=agent_id,
            workflow_id=workflow.get("id"),
            k=limit,
            increment_uses=False,
        )
        for lesson in injected:
            d = lesson.to_dict() if hasattr(lesson, "to_dict") else dict(lesson)
            hits.append(
                {
                    "kind": "alc_lesson",
                    "agent_id": agent_id,
                    "title": d.get("title") or d.get("summary") or "lesson",
                    "content": (d.get("content") or d.get("body") or "")[:500],
                    "id": d.get("id"),
                }
            )
    except Exception:  # noqa: BLE001
        pass

    # Workflow memory_reads
    for raw_scope in workflow.get("memory_reads") or []:
        if len(hits) >= limit * 2:
            break
        read_scope = scope_aliases.get(raw_scope, raw_scope)
        try:
            runtime.assert_memory_scope_allowed(
                agent=agent,
                scope=read_scope,
                action="read",
                organization_id=organization_id,
                actor_user_id=actor_user_id,
            )
            items = [
                m
                for m in runtime.store.collection("memory_items")
                if m.get("organization_id") == organization_id and m.get("scope") == read_scope
            ]
            for mem in items[:3]:
                hits.append(
                    {
                        "kind": "memory",
                        "scope": read_scope,
                        "title": mem.get("title") or raw_scope,
                        "content": (mem.get("content") or "")[:400],
                        "id": mem.get("id"),
                    }
                )
        except Exception:  # noqa: BLE001
            continue
    return hits
