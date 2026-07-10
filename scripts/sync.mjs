import path from "node:path";

import { buildGrokFiles } from "./adapters/grok.mjs";
import { buildTraeFiles } from "./adapters/trae.mjs";
import { pathExists, writeText } from "./lib/fs-safe.mjs";

function parseArgs(argv) {
  return {
    dryRun: argv.includes("--dry-run"),
    check: argv.includes("--check")
  };
}

function mergeFiles(...maps) {
  const merged = {};
  for (const map of maps) {
    for (const [relativePath, content] of Object.entries(map)) {
      if (Object.hasOwn(merged, relativePath)) {
        throw new Error(`duplicate sync output path: ${relativePath}`);
      }
      merged[relativePath] = content;
    }
  }
  return merged;
}

async function main() {
  const rootDir = process.cwd();
  const options = parseArgs(process.argv.slice(2));
  const files = mergeFiles(buildTraeFiles(), buildGrokFiles({ rootDir }));

  if (options.check) {
    let missing = 0;
    for (const relativePath of Object.keys(files)) {
      const exists = await pathExists(path.join(rootDir, relativePath));
      if (!exists) {
        missing += 1;
        console.error(`missing ${relativePath}`);
      }
    }
    if (missing > 0) {
      process.exitCode = 1;
      return;
    }
    console.log("sync check passed");
    return;
  }

  for (const [relativePath, content] of Object.entries(files)) {
    if (options.dryRun) {
      console.log(`DRY RUN: write ${relativePath}`);
      continue;
    }
    await writeText(path.join(rootDir, relativePath), content);
    console.log(`wrote ${relativePath}`);
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
