"""Evolving lesson library with utility scoring (self-evolving agents §7.3).

Wave 1: optional agent_id for Agent Learning Contract (ALC) scoping.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Lesson:
    id: str
    text: str
    source_run_id: str | None = None
    workflow_id: str | None = None
    agent_id: str | None = None
    uses: int = 0
    wins: int = 0
    tags: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)

    @property
    def utility(self) -> float:
        return (self.wins + 1) / (self.uses + 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "source_run_id": self.source_run_id,
            "workflow_id": self.workflow_id,
            "agent_id": self.agent_id,
            "uses": self.uses,
            "wins": self.wins,
            "utility": round(self.utility, 4),
            "tags": list(self.tags),
            "provenance": dict(self.provenance),
        }


def lesson_from_dict(data: dict[str, Any]) -> Lesson:
    return Lesson(
        id=str(data.get("id") or ""),
        text=str(data.get("text") or data.get("lesson_text") or ""),
        source_run_id=data.get("source_run_id"),
        workflow_id=data.get("workflow_id"),
        agent_id=data.get("agent_id"),
        uses=int(data.get("uses") or 0),
        wins=int(data.get("wins") or 0),
        tags=list(data.get("tags") or []),
        provenance=dict(data.get("provenance") or {}),
    )


class LessonLibrary:
    def __init__(self, items: list[dict[str, Any]] | None = None, capacity: int = 200):
        self.capacity = capacity
        self.lessons: list[Lesson] = [lesson_from_dict(i) for i in (items or []) if i.get("text") or i.get("lesson_text")]

    def add(self, lesson: Lesson) -> Lesson | None:
        for existing in self.lessons:
            if (
                existing.text == lesson.text
                and existing.workflow_id == lesson.workflow_id
                and (existing.agent_id or None) == (lesson.agent_id or None)
            ):
                return existing
        self.lessons.append(lesson)
        self._consolidate()
        return lesson

    def retrieve(
        self,
        *,
        workflow_id: str | None = None,
        agent_id: str | None = None,
        k: int = 5,
        increment_uses: bool = True,
    ) -> list[Lesson]:
        pool = self.lessons
        if agent_id:
            pool = [l for l in pool if l.agent_id == agent_id]
        if workflow_id:
            scoped = [l for l in pool if l.workflow_id == workflow_id]
            # When agent_id is set, do not fall back to other agents' lessons
            if agent_id:
                pool = scoped
            else:
                pool = scoped or pool
        ranked = sorted(pool, key=lambda l: l.utility, reverse=True)[:k]
        if increment_uses:
            for lesson in ranked:
                lesson.uses += 1
        return ranked

    def record_outcome(self, used: list[Lesson], success: bool) -> None:
        if not success:
            return
        for lesson in used:
            lesson.wins += 1

    def _consolidate(self) -> None:
        if len(self.lessons) <= self.capacity:
            return
        self.lessons.sort(key=lambda l: l.utility, reverse=True)
        self.lessons = self.lessons[: self.capacity]

    def to_list(self) -> list[dict[str, Any]]:
        return [l.to_dict() for l in self.lessons]
