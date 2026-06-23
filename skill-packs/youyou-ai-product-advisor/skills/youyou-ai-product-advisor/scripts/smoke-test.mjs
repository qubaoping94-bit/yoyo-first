import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const script = path.join(__dirname, "find-youyou-answer.mjs");
const cases = [
  ["五大平权", "equality"],
  ["优优无机板防潮耐水吗", "moisture"],
  ["有没有味道", "odor"],
  ["公司介绍", "company"],
  ["有机无机怎么讲", "organic"],
  ["有没有甲醛", "environmental"],
];

let issueCount = 0;
for (const [question, expectedPart] of cases) {
  const run = spawnSync(process.execPath, [script, question, "--limit", "1", "--json"], { encoding: "utf8" });
  if (run.status !== 0) {
    issueCount += 1;
    console.error(`FAIL ${question}: script exited ${run.status}`);
    console.error(run.stderr);
    continue;
  }
  const data = JSON.parse(run.stdout);
  const top = data.results?.[0];
  const haystack = [top?.id, top?.title, top?.intent].join(" ").toLowerCase();
  const ok = Boolean(top) && haystack.includes(expectedPart);
  console.log(`${ok ? "OK" : "FAIL"} ${question} -> ${top?.id || "NO_MATCH"}`);
  if (!ok) issueCount += 1;
}

if (issueCount > 0) {
  console.error(`issueCount=${issueCount}`);
  process.exit(1);
}
console.log("issueCount=0");
