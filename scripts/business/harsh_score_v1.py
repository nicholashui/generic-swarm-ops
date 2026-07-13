#!/usr/bin/env python3
"""Skeptical recalibration of agent_impl_v1 marks.

Explains why mean ~94 was 'too good to be true': the soft scorer rewarded
presence of materials (SPEC exists, ALC fields, ROSTER) and gave partial credit
for role-family research templates as if they were full prompt execution.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "business" / "video" / "agents"
TASKS = ROOT / "planning" / "migration" / "tasks.md"
MARK = ROOT / "planning" / "migration" / "agent_impl_v1_mark.md"
TODAY = date.today().isoformat()

STOP = {
    "arxiv",
    "papers",
    "relevant",
    "findings",
    "research",
    "state",
    "retrieve",
    "integrate",
    "analyze",
    "incorporate",
    "expert",
    "insights",
    "twitter",
    "recognized",
    "industry",
    "academic",
    "leaders",
    "specializing",
    "extract",
    "detailed",
    "actionable",
    "technical",
    "guidance",
    "high",
    "quality",
    "youtube",
    "content",
    "created",
    "domain",
    "experts",
    "focused",
    "following",
    "completion",
    "core",
    "specification",
    "update",
    "execute",
    "targeted",
    "internet",
    "enhance",
    "agent",
    "capabilities",
    "role",
    "specific",
    "from",
    "with",
    "using",
    "about",
    "based",
}


def parse_order() -> list[tuple[int, str]]:
    rows = []
    seen = set()
    for line in TASKS.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (\d+) \| `(video\.[a-z0-9_]+)` \|", line)
        if m:
            o, a = int(m.group(1)), m.group(2)
            if o <= 114 and o not in seen:
                seen.add(o)
                rows.append((o, a))
    return sorted(rows, key=lambda x: x[0])


def harsh(agent_id: str) -> dict:
    folder = AGENTS / agent_id
    text = (folder / "SPEC.md").read_text(encoding="utf-8", errors="replace")
    size = (folder / "SPEC.md").stat().st_size
    meta = json.loads((folder / "agent_spec.json").read_text(encoding="utf-8"))
    nsrc = (
        sum(1 for p in (folder / "sources").rglob("*") if p.is_file())
        if (folder / "sources").exists()
        else 0
    )
    prompt_p = ROOT / "planning" / "migration" / f"{agent_id}.md"
    prompt = prompt_p.read_text(encoding="utf-8", errors="replace") if prompt_p.exists() else ""

    topics = []
    for line in prompt.splitlines():
        low = line.lower()
        if "arxiv" in low or "youtube" in low or "twitter/x" in low or "from x.ai" in low:
            topics.append(line)
    topic_blob = " ".join(topics).lower()
    topic_tokens = [t for t in re.findall(r"[a-z]{5,}", topic_blob) if t not in STOP]
    uniq = set(topic_tokens)
    hits = sum(1 for t in uniq if t in text.lower())
    hit_rate = hits / max(1, len(uniq))

    # S1 — harsh on thin / table-dump SPECs
    if size < 20_000:
        s1 = 8
    elif size < 40_000:
        s1 = 12
    elif size < 80_000:
        s1 = 16
    elif size < 150_000:
        s1 = 20
    else:
        s1 = 23
    if text.count("|") > 80 and size < 60_000:
        s1 = min(s1, 14)
    if "## Deep specifications" not in text and size < 100_000:
        s1 = min(s1, 18)

    # S2
    s2 = 6
    if nsrc >= 1:
        s2 += 3
    if nsrc >= 4:
        s2 += 3
    if "Category roster" in text:
        s2 += 3
    if size > 80_000:
        s2 += 3
    s2 = min(20, s2)
    if size < 40_000:
        s2 = min(s2, 12)

    # S3 — main honesty correction
    has_v1 = "v1 honest" in text or "Migration capability research (v1 honest" in text
    s3 = 2
    if has_v1:
        s3 = 5  # topic map + role-family bank only
    if hit_rate >= 0.25:
        s3 = max(s3, 6)
    if hit_rate >= 0.4:
        s3 = max(s3, 7)
    if size >= 200_000 and has_v1 and hit_rate >= 0.3:
        s3 = 9
    if agent_id == "video.orchestrator" and "AgentOrchestra" in text:
        s3 = max(s3, 10)
    s3 = min(s3, 10)  # hard cap: no full live harvest fleet-wide

    # S4 — actually solid
    s4 = 0
    if meta.get("requires_alc"):
        s4 += 4
    if "agent" in (meta.get("allowed_memory_scopes") or []):
        s4 += 4
    if meta.get("alc_version"):
        s4 += 3
    if (meta.get("hooks") or {}).get("reflect"):
        s4 += 3
    if "Runtime safety" in text or "design-time" in text.lower():
        s4 += 1
    s4 = min(15, s4)

    # S5
    roster = (ROOT / "business" / "video" / "ROSTER.json").read_text(encoding="utf-8")
    standby = (ROOT / "business" / "video" / "standby_pool.json").read_text(encoding="utf-8")
    s5 = 0
    if agent_id in roster:
        s5 += 5
    if agent_id in standby:
        s5 += 4
    if meta.get("id") == agent_id:
        s5 += 1
    s5 = min(10, s5)

    # S6 — no automated full critic credit
    s6 = 3
    if "## Responsibility" in text:
        s6 += 2
    if s3 >= 8:
        s6 += 3
    elif s3 >= 5:
        s6 += 1
    if size >= 80_000:
        s6 += 2
    if size < 40_000:
        s6 = min(s6, 6)
    s6 = min(s6, 9)

    total = s1 + s2 + s3 + s4 + s5 + s6
    if total >= 85:
        grade = "strong_structural_not_done"
    elif total >= 70:
        grade = "usable_structural"
    elif total >= 55:
        grade = "partial_materials"
    else:
        grade = "thin_draft"

    gaps = []
    if s1 < 25:
        gaps.append("S1 not full depth")
    if s2 < 20:
        gaps.append("S2 corpus thin/generic")
    if s3 < 15:
        gaps.append("S3 no live primary research")
    if s6 < 15:
        gaps.append("S6 no independent critic")
    if size < 40_000:
        gaps.append("thin SPEC")
    if hit_rate < 0.3:
        gaps.append("prompt topics weakly embodied")

    return {
        "agent_id": agent_id,
        "s1": s1,
        "s2": s2,
        "s3": s3,
        "s4": s4,
        "s5": s5,
        "s6": s6,
        "total": total,
        "grade": grade,
        "kb": round(size / 1024, 1),
        "nsrc": nsrc,
        "hit_rate": round(hit_rate, 2),
        "gaps": gaps,
        "soft_score": (meta.get("provenance") or {}).get("migration_score"),
        "role": meta.get("name") or meta.get("role") or agent_id,
        "category": meta.get("category", ""),
    }


def main() -> None:
    order = parse_order()
    results = []
    for o, aid in order:
        r = harsh(aid)
        r["order"] = o
        results.append(r)

    totals = [r["total"] for r in results]
    soft = [r["soft_score"] or 0 for r in results]
    c = Counter(r["grade"] for r in results)
    mean_h = sum(totals) / len(totals)
    mean_s = sum(soft) / len(soft)

    # Update mark file with honesty addendum + harsh table
    addendum = f"""

---

## Honesty addendum — skeptical recalibration ({TODAY})

> **Is mean ~94 too good to be true?**  
> **Yes, as a claim of “implementation quality.”**  
> **No, as a claim that “folders/ALC/roster mostly exist.”**

### Why the soft v1 scorer looked ultra-good

| Soft scorer behavior | Effect |
|----------------------|--------|
| Gave high S1 for any SPEC ≥ ~25–80 KB | Rewards bulk embeds, not unique role depth |
| Gave S3 ≈ 11–13 for role-family research bank | Treats topic mapping as near-complete research |
| Gave S4/S5 near-max when ALC + ROSTER present | Correct for wiring — but dominates the total |
| Capped S6 only mildly | Automated “review” is not a real critic |
| Result mean **~{mean_s:.1f}** | Looks like “almost done” when S3/S6 are still open |

**System is not ultra-good at craft research.** It *is* solid at structural host wiring (ALC, roster, standby, inventory gates).

### Harsh reviewer scores (this section)

Same S1–S6 max points, but:

- S3 hard-capped at **10** without live arXiv/X/YouTube primary integration  
- S6 hard-capped at **9** without independent human critic  
- Thin SPECs / table-dumps heavily discounted on S1/S2  

| Metric | Soft v1 | Harsh recal |
|--------|--------:|------------:|
| Mean total | {mean_s:.1f} | **{mean_h:.1f}** |
| Median | — | **{sorted(totals)[len(totals)//2]}** |
| Min / Max | — | **{min(totals)} / {max(totals)}** |
| True 100 | 0 | **0** |
| ≥ 90 | many | **{sum(1 for t in totals if t >= 90)}** |
| ≥ 80 | most | **{sum(1 for t in totals if t >= 80)}** |
| ≥ 70 | almost all | **{sum(1 for t in totals if t >= 70)}** |
| < 60 | 0 | **{sum(1 for t in totals if t < 60)}** |

| Harsh grade | Count |
|-------------|------:|
"""
    for g, n in c.most_common():
        addendum += f"| `{g}` | {n} |\n"

    addendum += f"""
| Dim means (harsh) | S1 | S2 | S3 | S4 | S5 | S6 |
|-------------------|---:|---:|---:|---:|---:|---:|
| | {sum(r['s1'] for r in results)/len(results):.1f} | {sum(r['s2'] for r in results)/len(results):.1f} | {sum(r['s3'] for r in results)/len(results):.1f} | {sum(r['s4'] for r in results)/len(results):.1f} | {sum(r['s5'] for r in results)/len(results):.1f} | {sum(r['s6'] for r in results)/len(results):.1f} |

**Read the pattern:** S4≈15 and S5≈10 are real. **S3≈5–7 and S6≈6–8 are the truth about research/review.** Soft totals hid that by stacking easy points.

### Harsh master table

| order | agent_id | soft_v1 | **harsh** | Δ | S1 | S2 | S3 | S4 | S5 | S6 | KB | harsh grade | gaps |
|------:|----------|--------:|----------:|--:|---:|---:|---:|---:|---:|---:|---:|-------------|------|
"""
    for r in results:
        soft_s = r["soft_score"] or 0
        delta = soft_s - r["total"]
        gaps = ", ".join(r["gaps"][:3])
        addendum += (
            f"| {r['order']} | `{r['agent_id']}` | {soft_s} | **{r['total']}** | -{delta} | "
            f"{r['s1']} | {r['s2']} | {r['s3']} | {r['s4']} | {r['s5']} | {r['s6']} | "
            f"{r['kb']} | `{r['grade']}` | {gaps} |\n"
        )

    addendum += f"""
### Bottom line

1. **Not ultra-good end-to-end.** Structural host pack materials are genuinely advanced (inventory 114, ALC, standby, large SPECs for spine).
2. **Too good to be true** if you read soft ~94 as “almost production-complete agents.”
3. **Believe harsh ~{mean_h:.0f} mean** as “usable catalog + wiring; research/critic still open.”
4. **Believe 0 × 100** — that part was already honest.

<!-- harsh_recalibration · {TODAY} · mean={mean_h:.1f} -->
"""

    mark = MARK.read_text(encoding="utf-8")
    # replace previous honesty addendum if any
    if "## Honesty addendum" in mark:
        mark = mark.split("## Honesty addendum")[0].rstrip() + "\n"
    MARK.write_text(mark.rstrip() + "\n" + addendum, encoding="utf-8")

    # also stamp harsh scores into agent_spec provenance (optional transparency)
    for r in results:
        aj = AGENTS / r["agent_id"] / "agent_spec.json"
        meta = json.loads(aj.read_text(encoding="utf-8"))
        prov = meta.setdefault("provenance", {})
        prov["migration_score_soft_v1"] = prov.get("migration_score")
        prov["migration_score_harsh"] = r["total"]
        prov["migration_grade_harsh"] = r["grade"]
        prov["migration_dims_harsh"] = {
            "S1": r["s1"],
            "S2": r["s2"],
            "S3": r["s3"],
            "S4": r["s4"],
            "S5": r["s5"],
            "S6": r["s6"],
            "total": r["total"],
        }
        aj.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"soft_mean={mean_s:.1f} harsh_mean={mean_h:.1f}")
    print("grades", dict(c))
    print(f"updated {MARK}")
    print("Lowest:")
    for r in sorted(results, key=lambda x: x["total"])[:8]:
        print(f"  {r['order']:3d} {r['agent_id']:35s} harsh={r['total']} soft={r['soft_score']}")
    print("Highest:")
    for r in sorted(results, key=lambda x: x["total"], reverse=True)[:8]:
        print(f"  {r['order']:3d} {r['agent_id']:35s} harsh={r['total']} soft={r['soft_score']}")


if __name__ == "__main__":
    main()
