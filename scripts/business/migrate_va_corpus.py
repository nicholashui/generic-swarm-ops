# -*- coding: utf-8 -*-
"""Copy ALL va-agent-swarm content files into business/video/corpus (migration_plan.md)."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VA = Path(r"C:\Project\va-agent-swarm")
DEFAULT_DEST = ROOT / "business" / "video" / "corpus"
EXCLUDE_NAMES = {".DS_Store"}
EXCLUDE_DIR_PARTS = {".git"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def should_skip(path: Path, va_root: Path) -> bool:
    try:
        rel_parts = path.relative_to(va_root).parts
    except ValueError:
        return True
    if any(p in EXCLUDE_DIR_PARTS for p in rel_parts):
        return True
    if path.name in EXCLUDE_NAMES:
        return True
    return False


def map_dest(rel: Path, dest: Path) -> Path:
    """Map va relative path to corpus destination."""
    parts = rel.parts
    if parts[0] == "study":
        return dest / rel
    if parts[0] == "plan":
        return dest / rel
    # root-level content files
    return dest / "root" / rel.name


def git_sha(va_root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(va_root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--va-root", type=Path, default=DEFAULT_VA)
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args()
    va_root: Path = args.va_root.resolve()
    dest: Path = args.dest.resolve()
    if not va_root.is_dir():
        print(f"VA root missing: {va_root}", file=sys.stderr)
        return 1

    files = [
        p
        for p in va_root.rglob("*")
        if p.is_file() and not should_skip(p, va_root)
    ]
    files.sort(key=lambda p: str(p.relative_to(va_root)).replace("\\", "/"))

    sha = git_sha(va_root)
    now = datetime.now(timezone.utc).isoformat()
    if not args.dry_run:
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "SOURCE_COMMIT.txt").write_text(sha + "\n", encoding="utf-8")
        (dest / "SOURCE_URL.txt").write_text(
            "https://github.com/nicholashui/va-agent-swarm\n", encoding="utf-8"
        )
        (dest / "SOURCE_COPIED_AT.txt").write_text(now + "\n", encoding="utf-8")

    manifest: list[dict] = []
    log_lines: list[str] = []
    copied = 0
    skipped = 0
    for src in files:
        rel = src.relative_to(va_root)
        rel_posix = rel.as_posix()
        target = map_dest(rel, dest)
        dest_rel = target.relative_to(dest).as_posix() if not args.dry_run else str(target)
        entry = {
            "source_relpath": rel_posix,
            "dest_relpath": dest_rel if args.dry_run else target.relative_to(dest).as_posix(),
            "bytes": src.stat().st_size,
        }
        if args.dry_run:
            entry["sha256"] = sha256_file(src)
            entry["action"] = "would_copy"
            manifest.append(entry)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not args.force:
            # still hash dest for manifest
            entry["sha256"] = sha256_file(target)
            entry["action"] = "exists_skip"
            skipped += 1
        else:
            shutil.copy2(src, target)
            entry["sha256"] = sha256_file(target)
            entry["action"] = "copied"
            copied += 1
        manifest.append(entry)
        log_lines.append(json.dumps(entry, ensure_ascii=False))

    if args.dry_run:
        print(f"DRY_RUN files={len(files)} va={va_root}")
        return 0

    (dest / "MANIFEST.json").write_text(
        json.dumps(
            {
                "source_commit": sha,
                "copied_at": now,
                "va_root": str(va_root),
                "file_count": len(manifest),
                "files": manifest,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (dest / "COPY_LOG.jsonl").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    (dest / "MANIFEST.planned.txt").write_text(
        "\n".join(m["source_relpath"] for m in manifest) + "\n", encoding="utf-8"
    )
    print(f"MIGRATE_OK count={len(manifest)} copied={copied} skipped_existing={skipped} dest={dest}")
    if len(manifest) < 300:
        print("WARNING: expected ~325 content files", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
