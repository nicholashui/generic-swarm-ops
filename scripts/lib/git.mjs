import { execFile } from "node:child_process";
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

export async function cloneOrUpdateSource(source, mode = "download") {
  if (mode === "download") {
    await runGitWithRetry(["-c", "core.longpaths=true", "clone", "--depth", "1", source.url, source.target]);
  } else {
    if (await isShallowRepository(source.target)) {
      await runGitWithRetry(["-c", "core.longpaths=true", "-C", source.target, "fetch", "--unshallow", "origin"]);
    } else {
      await runGitWithRetry(["-c", "core.longpaths=true", "-C", source.target, "fetch", "--depth", "1", "origin"]);
    }
    await runGitWithRetry(["-c", "core.longpaths=true", "-C", source.target, "pull", "--ff-only"]);
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
