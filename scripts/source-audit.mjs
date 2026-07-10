import fs from "node:fs/promises";
import path from "node:path";

import { listFilesRecursive, readJson, writeText } from "./lib/fs-safe.mjs";

async function readPackageScripts(targetDir) {
  const packageJsonPath = path.join(targetDir, "package.json");
  try {
    const packageJson = JSON.parse(await fs.readFile(packageJsonPath, "utf8"));
    return packageJson.scripts || {};
  } catch {
    return {};
  }
}

async function hasBroadMcpAccess(targetDir) {
  try {
    const files = await listFilesRecursive(targetDir);
    const configFiles = files.filter((filePath) => filePath.endsWith(".json") && /mcp/i.test(filePath));
    for (const filePath of configFiles.slice(0, 20)) {
      const content = await fs.readFile(filePath, "utf8");
      if (/filesystem|network/i.test(content)) {
        return true;
      }
    }
    return false;
  } catch {
    return false;
  }
}

async function main() {
  const rootDir = process.cwd();
  const manifest = await readJson(path.join(rootDir, "sources", "manifest.json"));
  const lock = await readJson(path.join(rootDir, "sources", "source-lock.json"));
  const failuresById = new Map((lock.failures || []).map((failure) => [failure.id, failure]));
  const downloadedById = new Map((lock.sources || []).map((source) => [source.id, source]));

  const lines = ["# Source Audit", ""];

  for (const source of manifest.sources) {
    const downloaded = downloadedById.get(source.id);
    const failure = failuresById.get(source.id);
    const absoluteTarget = path.join(rootDir, source.target);
    const packageScripts = downloaded ? await readPackageScripts(absoluteTarget) : {};
    const securityNotes = [];

    if (!downloaded?.license_files?.length) {
      securityNotes.push("Unsafe for automatic import: no license file found.");
    }
    if (source.priority === "archived") {
      securityNotes.push("Unsafe for automatic import: source is archived.");
    }
    if (Object.keys(packageScripts).some((name) => /postinstall/i.test(name))) {
      securityNotes.push("Unsafe for automatic import: suspicious postinstall script found.");
    }
    if (Object.values(packageScripts).some((value) => /curl\s*\|\s*bash|irm.+\|\s*iex/i.test(value))) {
      securityNotes.push("Unsafe for automatic import: remote command execution pattern found.");
    }
    if (downloaded && await hasBroadMcpAccess(absoluteTarget)) {
      securityNotes.push("Review required: MCP-related files may request broad filesystem or network access.");
    }
    if (failure) {
      securityNotes.push(`Download failure recorded: ${failure.message}`);
    }

    const selectedComponents =
      source.id === "andrej-karpathy-skills" && downloaded?.license_files?.length
        ? "candidate rule snippets after human review"
        : "none yet";

    lines.push(`## ${source.id}`);
    lines.push("");
    lines.push(`- Name: ${source.name}`);
    lines.push(`- URL: ${source.url}`);
    lines.push(`- Target: ${source.target}`);
    lines.push(`- Status: ${failure ? "failed" : downloaded?.status || "not-downloaded"}`);
    lines.push(`- Commit: ${downloaded?.commit || "n/a"}`);
    lines.push(`- Branch: ${downloaded?.branch || "n/a"}`);
    lines.push(`- License files: ${(downloaded?.license_files || []).join(", ") || "none"}`);
    lines.push(`- Package files: ${(downloaded?.package_files || []).join(", ") || "none"}`);
    lines.push(`- Priority: ${source.priority}`);
    lines.push(`- Tier: ${source.tier}`);
    lines.push(`- Quarantine: ${source.quarantine}`);
    lines.push(`- Import policy: ${source.import_policy}`);
    lines.push(`- Purpose: ${source.purpose}`);
    lines.push(`- Selected components: ${selectedComponents}`);
    lines.push("- Rejected components: bulk import rejected until human review");
    lines.push(`- Security notes: ${securityNotes.join(" | ") || "No additional notes."}`);
    lines.push("");
  }

  await writeText(path.join(rootDir, "docs", "source-audit.md"), `${lines.join("\n")}\n`);
  console.log("Generated docs/source-audit.md");
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
