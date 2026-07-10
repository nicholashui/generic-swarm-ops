import fs from "node:fs/promises";
import path from "node:path";

import { scaffoldRepository } from "./lib/scaffold.mjs";

function parseArgs(argv) {
  const args = {
    name: null,
    outputPath: null,
    purpose: "Trae IDE starter repository",
    stack: "Node.js 20+, plain JavaScript, no runtime dependencies for bootstrap scripts",
    noDownload: false,
    force: false
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--name") {
      args.name = argv[index + 1];
      index += 1;
    } else if (arg === "--path") {
      args.outputPath = argv[index + 1];
      index += 1;
    } else if (arg === "--purpose") {
      args.purpose = argv[index + 1];
      index += 1;
    } else if (arg === "--stack") {
      args.stack = argv[index + 1];
      index += 1;
    } else if (arg === "--no-download") {
      args.noDownload = true;
    } else if (arg === "--force") {
      args.force = true;
    }
  }

  return args;
}

async function copyRecursive(sourcePath, targetPath) {
  const stat = await fs.stat(sourcePath);
  if (stat.isDirectory()) {
    await fs.mkdir(targetPath, { recursive: true });
    const entries = await fs.readdir(sourcePath);
    for (const entry of entries) {
      await copyRecursive(path.join(sourcePath, entry), path.join(targetPath, entry));
    }
    return;
  }
  await fs.mkdir(path.dirname(targetPath), { recursive: true });
  await fs.copyFile(sourcePath, targetPath);
}

export async function createProject(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);
  if (!options.name || !options.outputPath) {
    throw new Error("Usage: --name <project-name> --path <target-path>");
  }

  const rootDir = process.cwd();
  const targetDir = path.resolve(rootDir, options.outputPath);
  const entries = await fs.readdir(targetDir).catch(() => []);
  if (entries.length > 0 && !options.force) {
    throw new Error("Refusing to overwrite a non-empty target directory without --force.");
  }

  await fs.mkdir(targetDir, { recursive: true });
  await scaffoldRepository(targetDir, {
    projectName: options.name,
    projectPurpose: options.purpose,
    stack: options.stack
  });

  for (const relativePath of ["package.json", "starter.md", "scripts"]) {
    await copyRecursive(path.join(rootDir, relativePath), path.join(targetDir, relativePath));
  }

  console.log(`Created project at ${targetDir}`);
  if (options.noDownload) {
    console.log("Skipped source download because --no-download was used.");
  } else {
    console.log("Next step: run npm run bootstrap");
  }
}

if (process.argv[1] && path.basename(process.argv[1]) === "create-project.mjs") {
  createProject().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
