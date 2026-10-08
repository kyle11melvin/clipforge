import { spawn } from "node:child_process";

/** Run a command, stream nothing, resolve with {code, stdout, stderr}. Rejects on non-zero exit unless allowFail. */
export function run(cmd, args, { cwd, allowFail = false, stdin } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { cwd, stdio: [stdin ? "pipe" : "ignore", "pipe", "pipe"] });
    let stdout = "", stderr = "";
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("error", reject);
    child.on("close", (code) => {
      if (code !== 0 && !allowFail) {
        reject(new Error(`${cmd} ${args.join(" ")}\nexit ${code}\n${stderr.slice(-4000)}`));
      } else resolve({ code, stdout, stderr });
    });
    if (stdin) { child.stdin.write(stdin); child.stdin.end(); }
  });
}

export function log(step, msg) {
  const t = new Date().toISOString().slice(11, 19);
  console.log(`[${t}] ${step.padEnd(10)} ${msg}`);
}
