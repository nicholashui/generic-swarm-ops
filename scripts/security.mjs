import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";

import { listFilesRecursive, pathExists } from "./lib/fs-safe.mjs";

const execFileAsync = promisify(execFile);

const SECRET_PATTERNS = [
  /-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----/,
  /ghp_[A-Za-z0-9]{20,}/,
  /sk-[A-Za-z0-9]{20,}/
];

/** Templates that are expected in-repo (placeholders only). */
function isEnvTemplate(relative) {
  return /(^|\/)\.env\.(example|sample|template)$/i.test(relative);
}

/** Real secret-bearing paths — only fail when git-tracked. */
function isSensitivePath(relative) {
  if (isEnvTemplate(relative)) {
    return false;
  }
  return /(^|\/)\.env($|\.)/i.test(relative) || /\.(pem|key|p12)$/i.test(relative);
}

function shouldSkipScan(relative) {
  const parts = relative.split("/");
  if (parts.includes("node_modules") || parts.includes(".git") || parts.includes(".next")) {
    return true;
  }
  if (relative.startsWith("external/sources/")) {
    return true;
  }
  if (relative.startsWith("tests/fixtures/")) {
    return true;
  }
  if (parts.includes("__pycache__") || parts.includes(".venv")) {
    return true;
  }
  return false;
}

async function listTrackedFiles(rootDir) {
  try {
    const { stdout } = await execFileAsync("git", ["-C", rootDir, "ls-files", "-z"], {
      maxBuffer: 1024 * 1024 * 40
    });
    const set = new Set();
    for (const entry of stdout.split("\0")) {
      if (entry) {
        set.add(entry.replace(/\\/g, "/"));
      }
    }
    return set;
  } catch {
    // Not a git checkout — fall back to path-based rules only.
    return null;
  }
}

function hasPostinstallScript(packageJsonText) {
  try {
    const pkg = JSON.parse(packageJsonText);
    return Boolean(pkg?.scripts?.postinstall);
  } catch {
    return /"postinstall"\s*:/.test(packageJsonText);
  }
}

async function main() {
  const rootDir = process.cwd();
  const warnings = [];
  const failures = [];
  const tracked = await listTrackedFiles(rootDir);

  const projectFiles = (await listFilesRecursive(rootDir)).filter((filePath) => {
    const relative = path.relative(rootDir, filePath).replace(/\\/g, "/");
    return !shouldSkipScan(relative);
  });

  for (const filePath of projectFiles) {
    const relative = path.relative(rootDir, filePath).replace(/\\/g, "/");

    if (isSensitivePath(relative)) {
      // Local gitignored .env is expected for development; only fail if tracked.
      if (tracked === null || tracked.has(relative)) {
        failures.push(`Sensitive file committed: ${relative}`);
      }
      continue;
    }

    // Env templates may still contain real secrets by mistake — scan content only.
    const content = await fs.readFile(filePath, "utf8").catch(() => "");
    for (const pattern of SECRET_PATTERNS) {
      if (pattern.test(content)) {
        failures.push(`Secret-like content found in ${relative}`);
        break;
      }
    }

    if (relative.startsWith("mcp-configs/") && /filesystem|network/i.test(content)) {
      warnings.push(`Review MCP access scope in ${relative}`);
    }
  }

  const externalSources = path.join(rootDir, "external", "sources");
  if (await pathExists(externalSources)) {
    const sourceRoots = await fs.readdir(externalSources, { withFileTypes: true }).catch(() => []);
    for (const entry of sourceRoots.filter((item) => item.isDirectory())) {
      const packageJsonPath = path.join(externalSources, entry.name, "package.json");
      const content = await fs.readFile(packageJsonPath, "utf8").catch(() => "");
      if (!content) {
        continue;
      }
      if (hasPostinstallScript(content)) {
        warnings.push(`Suspicious postinstall script in external/sources/${entry.name}/package.json`);
      }
      if (/curl\s*\|\s*bash|irm.+\|\s*iex/i.test(content)) {
        warnings.push(`Remote command execution pattern in external/sources/${entry.name}/package.json`);
      }
    }
  }

  console.log("security scan");
  console.log(`warnings: ${warnings.length}`);
  console.log(`failures: ${failures.length}`);
  for (const warning of warnings) {
    console.log(`WARN ${warning}`);
  }
  for (const failure of failures) {
    console.error(`FAIL ${failure}`);
  }

  if (failures.length > 0) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
