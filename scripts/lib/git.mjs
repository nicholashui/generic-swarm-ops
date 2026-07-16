import { execFile } from "node:child_process";
import { rm } from "node:fs/promises";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isTransientGitFailure(message) {
  return /Could not connect to server|Failed to connect|Connection timed out|Operation timed out|Connection reset|HTTP 5\d\d|TLS|SSL/i.test(message);
}

export async function runGit(args, options = {}) {
  const { stdout, stderr } = await execFileAsync("git", args, {
    cwd: options.cwd,
    maxBuffer: 1024 * 1024 * 20
  });
  return {
    stdout: stdout.trim(),
    stderr: stderr.trim()
  };
}

async function runGitWithRetry(args, options = {}) {
  const retries = options.retries ?? 3;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      return await runGit(args, options);
    } catch (error) {
      if (attempt === retries || !isTransientGitFailure(error.message)) {
        throw error;
      }
      await sleep(attempt * 1000);
    }
  }
  throw new Error("git retry loop exhausted unexpectedly");
}

export async function gitAvailable() {
  try {
    await runGit(["--version"]);
    return true;
  } catch {
    return false;
  }
}

export async function isShallowRepository(target) {
  const result = await runGit(["-C", target, "rev-parse", "--is-shallow-repository"]);
  return result.stdout === "true";
}

async function resolveOriginTip(target) {
  try {
    const head = (await runGit(["-C", target, "symbolic-ref", "refs/remotes/origin/HEAD"])).stdout;
    // e.g. refs/remotes/origin/main -> origin/main
    if (head.startsWith("refs/remotes/")) {
      return head.slice("refs/remotes/".length);
    }
  } catch {
    // fall through
  }
  const branch = (await runGit(["-C", target, "branch", "--show-current"])).stdout;
  if (branch) {
    return `origin/${branch}`;
  }
  return "origin/main";
}

async function recloneSource(source) {
  await rm(source.target, { recursive: true, force: true });
  await runGitWithRetry([
    "-c",
    "core.longpaths=true",
    "clone",
    "--depth",
    "1",
    source.url,
    source.target
  ]);
}

/**
 * Clone or refresh a vendored external source.
 * Updates always hard-reset to the remote tip: these trees are disposable mirrors
 * (import_policy curated-only). pull --ff-only fails after shallow/unshallow history skew.
 * On any update failure (diverged history, untracked conflicts, Windows long-path
 * damage), fall back to delete + shallow reclone.
 */
export async function cloneOrUpdateSource(source, mode = "download") {
  if (mode === "download") {
    await runGitWithRetry([
      "-c",
      "core.longpaths=true",
      "clone",
      "--depth",
      "1",
      source.url,
      source.target
    ]);
    return;
  }

  try {
    const branch = (await runGit(["-C", source.target, "branch", "--show-current"])).stdout || "main";
    // Depth-1 tip refresh only — avoid --unshallow (creates diverging local history).
    await runGitWithRetry([
      "-c",
      "core.longpaths=true",
      "-C",
      source.target,
      "fetch",
      "--depth",
      "1",
      "origin",
      branch
    ]);

    let tip = `origin/${branch}`;
    try {
      await runGit(["-C", source.target, "rev-parse", "--verify", tip]);
    } catch {
      tip = await resolveOriginTip(source.target);
    }

    // Disposable mirrors: hard-reset + clean so shallow skew / leftover untracked
    // files cannot block refresh (checkout alone fails on untracked conflicts).
    await runGit(["-c", "core.longpaths=true", "-C", source.target, "checkout", "-B", branch]);
    await runGit(["-c", "core.longpaths=true", "-C", source.target, "reset", "--hard", tip]);
    await runGit(["-c", "core.longpaths=true", "-C", source.target, "clean", "-fd"]);
  } catch (error) {
    // Broken working trees (esp. Windows MAX_PATH) are cheaper to reclone than repair.
    await recloneSource(source);
  }
}

export async function readGitMetadata(target) {
  const resolvedUrl = (await runGit(["-C", target, "remote", "get-url", "origin"])).stdout;
  const commit = (await runGit(["-C", target, "rev-parse", "HEAD"])).stdout;
  const branch = (await runGit(["-C", target, "branch", "--show-current"])).stdout || "HEAD";
  const lastCommitAt = (await runGit(["-C", target, "log", "-1", "--format=%cI"])).stdout;
  const lastCommitSubject = (await runGit(["-C", target, "log", "-1", "--format=%s"])).stdout;
  return {
    resolvedUrl,
    commit,
    branch,
    lastCommitAt,
    lastCommitSubject
  };
}
