import { spawn } from "node:child_process";
import path from "node:path";

import { createProject } from "./create-project.mjs";
import { readJson, writeJson } from "./lib/fs-safe.mjs";
import { scaffoldRepository } from "./lib/scaffold.mjs";

function npmBin() {
  return process.platform === "win32" ? "npm.cmd" : "npm";
}

async function runNpmScript(script, extraArgs = []) {
  await new Promise((resolve, reject) => {
    const child = spawn(npmBin(), ["run", script, "--", ...extraArgs], {
      cwd: process.cwd(),
      stdio: "inherit",
      shell: process.platform === "win32"
    });

    child.on("error", reject);
    child.on("exit", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${script} failed with exit code ${code}`));
      }
    });
  });
}

async function bootstrap() {
  for (const [script, extraArgs] of [
    ["doctor", []],
    ["sources:download", []],
    ["sources:audit", []],
    ["security", []],
    ["sync", ["--dry-run"]],
    ["business:init", []],
    ["business:validate", []],
    ["business:governance", []],
    ["business:security", []],
    ["business:evolution:check", []],
    ["business:eval", ["--dry-run"]],
    ["test", []]
  ]) {
    console.log(`running ${script}`);
    await runNpmScript(script, extraArgs);
  }
}

async function init() {
  const result = await scaffoldRepository(process.cwd());
  console.log(`Initialized starter scaffold in ${result.root}`);
}

async function format() {
  for (const relativePath of ["package.json", "sources/manifest.json", "sources/docs-manifest.json"]) {
    const absolutePath = path.join(process.cwd(), relativePath);
    try {
      const json = await readJson(absolutePath);
      await writeJson(absolutePath, json);
      console.log(`formatted ${relativePath}`);
    } catch {
      // Ignore files that do not exist yet.
    }
  }
}

async function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);

  if (command === "bootstrap") {
    await bootstrap();
    return;
  }

  if (command === "create") {
    await createProject(args);
    return;
  }

  if (command === "init") {
    await init();
    return;
  }

  if (command === "format") {
    await format();
    return;
  }

  throw new Error("Unknown command. Use bootstrap, create, init, or format.");
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
