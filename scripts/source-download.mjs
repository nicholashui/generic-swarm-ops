import fs from "node:fs/promises";
import path from "node:path";

import { cloneOrUpdateSource, gitAvailable, readGitMetadata } from "./lib/git.mjs";
import { ensureDir, isGitRepository, readJson, writeJson } from "./lib/fs-safe.mjs";
import { selectSources, validateSourceManifest } from "./lib/manifest.mjs";

function parseArgs(argv) {
  const args = {
    profile: "all",
    dryRun: false,
    strict: false,
    check: false,
    update: false
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--profile") {
      args.profile = argv[index + 1] || "all";
      index += 1;
    } else if (arg === "--dry-run") {
      args.dryRun = true;
    } else if (arg === "--strict") {
      args.strict = true;
    } else if (arg === "--check") {
      args.check = true;
    } else if (arg === "--update") {
      args.update = true;
    }
  }

  return args;
}

async function collectRootMatches(targetPath, matcher) {
  const entries = await fs.readdir(targetPath, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isFile() && matcher(entry.name))
    .map((entry) => entry.name);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const rootDir = process.cwd();
  const manifestPath = path.join(rootDir, "sources", "manifest.json");
  const lockPath = path.join(rootDir, "sources", "source-lock.json");
  const manifest = await readJson(manifestPath);

  validateSourceManifest(manifest);
  const selectedSources = selectSources(manifest, options.profile);

  if (options.check) {
    console.log(`Validated ${selectedSources.length} enabled sources for profile ${options.profile}.`);
    return;
  }

  if (!(await gitAvailable())) {
    throw new Error("BLOCKED: cannot download sources because network/shell execution is unavailable.");
  }

  await ensureDir(path.join(rootDir, "external", "sources"));
  const lock = {
    schema_version: "1.0",
    generated_at: new Date().toISOString(),
    sources: [],
    failures: []
  };

  for (const source of selectedSources) {
    const absoluteTarget = path.join(rootDir, source.target);
    await ensureDir(path.dirname(absoluteTarget));
    const exists = await fs.access(absoluteTarget).then(() => true).catch(() => false);

    try {
      if (options.dryRun) {
        console.log(`DRY RUN: ${exists ? "update" : "clone"} ${source.id}`);
      } else if (!exists) {
        await cloneOrUpdateSource({ ...source, target: absoluteTarget }, "download");
      } else if (await isGitRepository(absoluteTarget)) {
        await cloneOrUpdateSource({ ...source, target: absoluteTarget }, "update");
      } else {
        throw new Error(`Target exists and is not a git repository: ${source.target}`);
      }

      const metadata = options.dryRun
        ? {
            resolvedUrl: source.url,
            commit: "dry-run",
            branch: "dry-run",
            lastCommitAt: new Date().toISOString(),
            lastCommitSubject: "dry-run"
          }
        : await readGitMetadata(absoluteTarget);

      const licenseFiles = options.dryRun
        ? []
        : await collectRootMatches(absoluteTarget, (name) => /^license/i.test(name));
      const packageFiles = options.dryRun
        ? []
        : await collectRootMatches(absoluteTarget, (name) => /package(-lock)?\.json$/i.test(name));

      lock.sources.push({
        id: source.id,
        name: source.name,
        url: source.url,
        resolved_url: metadata.resolvedUrl,
        target: source.target,
        status: options.dryRun ? "dry-run" : "downloaded",
        commit: metadata.commit,
        branch: metadata.branch,
        last_commit_at: metadata.lastCommitAt,
        last_commit_subject: metadata.lastCommitSubject,
        license_files: licenseFiles,
        package_files: packageFiles,
        quarantine: source.quarantine,
        import_policy: source.import_policy
      });

      console.log(`${exists ? "updated" : "downloaded"} ${source.id}`);
    } catch (error) {
      lock.failures.push({
        id: source.id,
        target: source.target,
        priority: source.priority,
        message: error.message
      });
      console.error(`failed ${source.id}: ${error.message}`);
      if (source.priority === "required" || options.strict) {
        await writeJson(lockPath, lock);
        process.exitCode = 1;
        return;
      }
    }
  }

  await writeJson(lockPath, lock);
  console.log(`Wrote ${path.relative(rootDir, lockPath)}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
