# Example Education Pack (Wave 4)

Lite third domain pack proving **N2** multi-pack hosting.

| Artifact | Path |
|----------|------|
| Manifest | `manifest.json` |
| Agents | `agents/example.edu_planner`, `agents/example.edu_reviewer` |
| DNA | `workflows/wf_example_education_v1.dna.json` |
| Golden | `evals/golden/example-education-brief.json` |

Does **not** count toward video inventory (114). Register via:

```bash
python scripts/business/register_domain.py --manifest business/example_education/manifest.json --dry-run
```

See `docs/add-domain-pack-runbook.md`.
