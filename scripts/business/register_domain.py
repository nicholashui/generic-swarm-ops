# -*- coding: utf-8 -*-
"""Wave 0 domain register stub — validate domain-manifest only (draft)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "business" / "schemas" / "domain-manifest.schema.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validate import SchemaError, validate  # noqa: E402


def register_manifest(manifest_path: Path, *, dry_run: bool = True) -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate(data, schema)
    receipt = {
        "status": "draft",
        "domain_id": data["domain_id"],
        "version": data["version"],
        "requires_alc": data["requires_alc"],
        "agent_count": len(data.get("agents") or []),
        "dry_run": dry_run,
        "message": "Wave 0 stub: manifest valid; runtime catalog load deferred to Wave 1",
    }
    if not dry_run:
        out = manifest_path.parent / ".register-receipt.json"
        out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        receipt["receipt_path"] = str(out.as_posix())
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Domain pack register stub (Wave 0)")
    parser.add_argument("--manifest", required=True, help="Path to domain manifest.json")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--write-receipt", action="store_true", help="Write .register-receipt.json")
    args = parser.parse_args()
    path = Path(args.manifest)
    if not path.is_file():
        print(f"missing manifest: {path}", file=sys.stderr)
        return 1
    try:
        receipt = register_manifest(path, dry_run=not args.write_receipt)
    except (SchemaError, json.JSONDecodeError, OSError) as e:
        print(f"REGISTER FAIL: {e}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
