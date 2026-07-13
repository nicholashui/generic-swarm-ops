"""Multi-generation coevolution helpers (sandbox-only, deterministic).

Pairs agent genomes (e.g. planner × aesthetics/QC) for Wave 3 learning experiments.
Does not write production workflow DNA.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any


SUITE_WEIGHT = 0.6
GROWTH_WEIGHT = 0.2
REUSE_WEIGHT = 0.2


def default_agent_pair(domain_id: str = "video") -> tuple[str, str]:
    d = (domain_id or "video").strip() or "video"
    return (f"{d}.planner", f"{d}.aiqaconsistency")


def composite_fitness(
    suite_pass_rate: float,
    knowledge_growth_count: float = 0.0,
    lesson_reuse_rate: float = 0.0,
) -> dict[str, float]:
    """Deterministic composite fitness with ALC enrichment norms."""
    suite = max(0.0, min(1.0, float(suite_pass_rate or 0.0)))
    growth_norm = min(1.0, float(knowledge_growth_count or 0.0) / 10.0)
    reuse_norm = min(1.0, float(lesson_reuse_rate or 0.0) / 5.0)
    composite = round(SUITE_WEIGHT * suite + GROWTH_WEIGHT * growth_norm + REUSE_WEIGHT * reuse_norm, 4)
    return {
        "suite_pass_rate": round(suite, 4),
        "knowledge_growth": float(knowledge_growth_count or 0.0),
        "lesson_reuse": float(lesson_reuse_rate or 0.0),
        "knowledge_growth_norm": round(growth_norm, 4),
        "lesson_reuse_norm": round(reuse_norm, 4),
        "composite_fitness": composite,
    }


def enrich_fitness_with_alc(
    fitness: dict[str, Any] | None,
    alc_metrics: dict[str, Any] | None,
) -> dict[str, Any]:
    base = dict(fitness or {})
    alc = alc_metrics or {}
    growth = float(alc.get("knowledge_growth_count") or base.get("knowledge_growth") or 0.0)
    reuse = float(alc.get("lesson_reuse_rate") or base.get("lesson_reuse") or 0.0)
    suite = float(base.get("suite_pass_rate") or 0.0)
    merged = composite_fitness(suite, growth, reuse)
    # Preserve non-ALC suite structural metrics
    for key, value in base.items():
        if key not in merged:
            merged[key] = value
    return merged


def mutate_genome(parent: dict[str, Any] | None, generation: int) -> dict[str, Any]:
    """Lite deterministic genome mutation for sandbox coevolution."""
    genome = deepcopy(parent) if isinstance(parent, dict) else {}
    genome["generation"] = int(generation)
    genome["version"] = int(genome.get("version") or 0) + 1
    temp = float(genome.get("temperature") or 0.2)
    genome["temperature"] = round(min(1.0, temp + 0.05 * generation), 4)
    genome["sandbox_only"] = True
    genome.setdefault("traits", {})
    if isinstance(genome["traits"], dict):
        genome["traits"]["exploration"] = round(min(1.0, 0.1 * generation), 4)
    return genome


def build_genome_propose_payload(
    *,
    agent_id: str,
    generation: int,
    parent_genome: dict[str, Any] | None,
    base_workflow_id: str | None,
    dna: dict[str, Any] | None,
    role: str,
    parent_variant_id: str | None = None,
) -> dict[str, Any]:
    genome = mutate_genome(parent_genome, generation)
    genome["role"] = role
    genome["agent_id"] = agent_id
    dna_copy = deepcopy(dna) if isinstance(dna, dict) else {}
    if dna_copy:
        dna_copy["production_ready"] = False
        dna_copy["auto_promote"] = False
        dna_copy["status"] = "sandbox"
        if not dna_copy.get("domain") and agent_id and "." in agent_id:
            dna_copy["domain"] = agent_id.split(".", 1)[0]
    payload: dict[str, Any] = {
        "variant_type": "agent_genome",
        "agent_id": agent_id,
        "genome": genome,
        "name": f"coevo_g{generation}_{role}_{agent_id}",
        "changes": [f"coevolution generation {generation}", f"role={role}"],
        "sandbox_only": True,
        "direct_production_mutation": False,
        "dna": dna_copy,
        "lineage": [parent_variant_id] if parent_variant_id else ([base_workflow_id] if base_workflow_id else []),
    }
    if base_workflow_id:
        payload["base_workflow_id"] = base_workflow_id
    return payload


def select_elite(variants: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not variants:
        return None

    def score(v: dict[str, Any]) -> float:
        fm = v.get("fitness_metrics") or (v.get("evaluation") or {}).get("fitness_metrics") or {}
        return float(fm.get("composite_fitness") or fm.get("suite_pass_rate") or 0.0)

    return max(variants, key=score)


def summarize_generation(generation: int, variants: list[dict[str, Any]]) -> dict[str, Any]:
    elite = select_elite(variants)
    elite_fm = {}
    if elite:
        elite_fm = elite.get("fitness_metrics") or (elite.get("evaluation") or {}).get("fitness_metrics") or {}
    return {
        "generation": generation,
        "variant_ids": [v.get("id") for v in variants],
        "elite_variant_id": elite.get("id") if elite else None,
        "elite_fitness": float(elite_fm.get("composite_fitness") or elite_fm.get("suite_pass_rate") or 0.0),
        "fitness_metrics": elite_fm,
        "variant_count": len(variants),
    }


def load_pack_workflow_dna(repo_root: Any, domain_id: str, workflow_id: str) -> dict[str, Any] | None:
    """Load DNA JSON from business/<domain>/workflows when not in runtime store."""
    from pathlib import Path
    import json

    root = Path(repo_root)
    path = root / "business" / domain_id / "workflows" / f"{workflow_id}.dna.json"
    if not path.is_file():
        # also try without .dna suffix pattern
        alt = root / "business" / domain_id / "workflows" / f"{workflow_id}.json"
        path = alt if alt.is_file() else path
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None
