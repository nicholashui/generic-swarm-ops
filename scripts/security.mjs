import fs from "node:fs/promises";
import path from "node:path";

import { listFilesRecursive, pathExists } from "./lib/fs-safe.mjs";

const SECRET_PATTERNS = [
  /-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----/,
  /ghp_[A-Za-z0-9]{20,}/,
  /sk-[A-Za-z0-9]{20,}/
];

async function main() {
  const rootDir = process.cwd();
  const warnings = [];
  const failures = [];

  const projectFiles = (await listFilesRecursive(rootDir)).filter((filePath) => {
    const relative = path.relative(rootDir, filePath).replace(/\\/g, "/");
    return !relative.startsWith("external/sources/") && !relative.startsWith("node_modules/") && !relative.startsWith("tests/fixtures/");
  });

  for (const filePath of projectFiles) {
    const relative = path.relative(rootDir, filePath).replace(/\\/g, "/");
    if (/\.env($|\.)/i.test(relative) || /\.(pem|key|p12)$/i.test(relative)) {
      failures.push(`Sensitive file committed: ${relative}`);
      continue;
    }

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
      if (/postinstall/i.test(content)) {
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
