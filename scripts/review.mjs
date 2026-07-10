import fs from "node:fs/promises";
import path from "node:path";

async function countEntries(dirPath) {
  try {
    return (await fs.readdir(dirPath)).length;
  } catch {
    return 0;
  }
}

async function main() {
  const rootDir = process.cwd();
  const pending = await countEntries(path.join(rootDir, "suggestions", "pending"));
  const approved = await countEntries(path.join(rootDir, "suggestions", "approved"));
  const rejected = await countEntries(path.join(rootDir, "suggestions", "rejected"));

  console.log("review summary");
  console.log(`pending: ${pending}`);
  console.log(`approved: ${approved}`);
  console.log(`rejected: ${rejected}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
