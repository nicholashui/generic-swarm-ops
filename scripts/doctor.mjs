import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import { ensureDir, pathExists } from "./lib/fs-safe.mjs";
import { gitAvailable } from "./lib/git.mjs";

async function checkWritePermissions(rootDir) {
  const tempFile = path.join(rootDir, ".doctor-write-test.tmp");
  await fs.writeFile(tempFile, "ok", "utf8");
  await fs.unlink(tempFile);
}

async function checkSymlinkSupport(rootDir) {
  const targetFile = path.join(rootDir, ".doctor-symlink-target.tmp");
  const linkFile = path.join(rootDir, ".doctor-symlink-link.tmp");
  try {
    await fs.writeFile(targetFile, "ok", "utf8");
    await fs.symlink(targetFile, linkFile);
    return true;
  } catch {
    return false;
  } finally {
    await fs.unlink(linkFile).catch(() => {});
    await fs.unlink(targetFile).catch(() => {});
  }
}

async function main() {
  const rootDir = process.cwd();
  const manifestPath = path.join(rootDir, "sources", "manifest.json");
  const scriptsDir = path.join(rootDir, "scripts");
  const externalDir = path.join(rootDir, "external");
  const nodeMajor = Number(process.versions.node.split(".")[0]);
  const results = [];

  results.push({ label: "Node", ok: nodeMajor >= 20, detail: process.versions.node });
  results.push({ label: "Git", ok: await gitAvailable(), detail: "git" });

  try {
    await ensureDir(externalDir);
    results.push({ label: "External dir", ok: true, detail: externalDir });
  } catch (error) {
    results.push({ label: "External dir", ok: false, detail: error.message });
  }

  results.push({ label: "Manifest", ok: await pathExists(manifestPath), detail: manifestPath });
  results.push({ label: "Scripts", ok: await pathExists(scriptsDir), detail: scriptsDir });

  try {
    await checkWritePermissions(rootDir);
    results.push({ label: "Write", ok: true, detail: rootDir });
  } catch (error) {
    results.push({ label: "Write", ok: false, detail: error.message });
  }

  const symlinkSupported = await checkSymlinkSupport(rootDir);
  results.push({ label: "Symlink", ok: symlinkSupported, detail: symlinkSupported ? "supported" : "not supported" });

  console.log("starter doctor\n");
  for (const result of results) {
    console.log(`${result.label}: ${result.ok ? "OK" : `FAIL (${result.detail})`}`);
  }
  console.log(`OS: ${os.platform()}`);

  const failures = results.filter((result) => !result.ok && result.label !== "Symlink");
  console.log(`Result: ${failures.length === 0 ? "OK" : "FAIL"}`);

  if (failures.length > 0) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
