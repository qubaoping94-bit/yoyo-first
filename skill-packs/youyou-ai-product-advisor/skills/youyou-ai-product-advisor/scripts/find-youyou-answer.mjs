import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, "..");
const knowledge = JSON.parse(fs.readFileSync(path.join(skillRoot, "references", "knowledge-data.json"), "utf8"));
const routes = JSON.parse(fs.readFileSync(path.join(skillRoot, "references", "standard-question-routes.json"), "utf8"));

const args = process.argv.slice(2);
const question = args.filter((arg) => !arg.startsWith("--")).join(" ").trim();
const limitArg = args.find((arg) => arg.startsWith("--limit="));
const limitIndex = args.indexOf("--limit");
const limit = Number(limitArg?.split("=")[1] || (limitIndex >= 0 ? args[limitIndex + 1] : 3)) || 3;
const json = args.includes("--json");

if (!question) {
  console.error('Usage: node scripts/find-youyou-answer.mjs "<customer question>" --limit 3 [--json]');
  process.exit(2);
}

function normalize(value) {
  return String(value || "").toLowerCase().replace(/[^\p{Script=Han}a-z0-9]+/gu, "");
}

const q = normalize(question);
const routeHits = new Map();
for (const route of routes.routes || []) {
  const rn = normalize(route.normalized || route.question);
  if (!rn) continue;
  let score = 0;
  if (rn === q) score = 10000;
  else if (q.includes(rn) || rn.includes(q)) score = Math.min(8000, 4000 + Math.min(q.length, rn.length) * 20);
  if (score > 0) {
    const prev = routeHits.get(route.expectedEntryId) || { score: 0, routes: [] };
    prev.score = Math.max(prev.score, score);
    prev.routes.push(route.question);
    routeHits.set(route.expectedEntryId, prev);
  }
}

const hardRules = [
  { idIncludes: ["five", "equality"], terms: ["五大平权", "平权", "豪华平权", "技术平权", "健康平权", "安装平权", "定制平权"], score: 3500 },
  { idIncludes: ["fire", "safety"], terms: ["A级不燃", "不燃", "防火", "阻燃", "消防", "火烧"], score: 3000 },
  { idIncludes: ["moisture", "water"], terms: ["防潮耐水", "防潮", "防水", "回南天", "梅雨季", "厨房", "卫生间", "地下室"], score: 3000 },
  { idIncludes: ["odor", "smell"], terms: ["味道", "异味", "胶味", "刺鼻", "低异味"], score: 3200 },
  { idIncludes: ["company", "profile"], terms: ["公司介绍", "企业介绍", "公司简介", "你们公司"], score: 3200 },
  { idIncludes: ["organic", "inorganic"], terms: ["有机无机", "有机和无机", "吃有机", "用无机"], score: 3200 },
  { idIncludes: ["environmental"], terms: ["甲醛", "环保", "儿童房", "入住", "健康"], score: 3600 },
  { idIncludes: ["zero", "pure"], terms: ["七零", "零添加", "木头", "塑料", "石棉"], score: 3000 },
  { idIncludes: ["mildew", "antibacterial"], terms: ["发霉", "霉菌", "抗菌", "防霉"], score: 2600 },
  { idIncludes: ["density", "impact", "deformation"], terms: ["高密度", "1.2", "抗冲击", "抗变形", "高强度"], score: 2600 },
];

function hardRuleScore(entry) {
  let score = 0;
  const haystack = normalize([entry.id, entry.title, entry.intent, ...(entry.keywords || [])].join(" "));
  for (const rule of hardRules) {
    if (!rule.terms.some((term) => q.includes(normalize(term)))) continue;
    const idHit = rule.idIncludes.some((part) => haystack.includes(normalize(part)));
    if (idHit) score += rule.score;
  }
  return score;
}

function lexicalScore(entry) {
  let score = 0;
  const title = normalize(entry.title);
  const id = normalize(entry.id);
  if (title && (q.includes(title) || title.includes(q))) score += 1200;
  if (id && q.includes(id)) score += 800;
  for (const sample of entry.questionExamples || []) {
    const s = normalize(sample);
    if (!s) continue;
    if (s === q) score += 1600;
    else if (q.includes(s) || s.includes(q)) score += 500;
  }
  for (const kw of entry.keywords || []) {
    const k = normalize(kw);
    if (!k) continue;
    if (q.includes(k)) score += Math.min(900, 120 + k.length * 20);
  }
  const body = normalize(entry.answerMarkdown).slice(0, 12000);
  for (const token of Array.from(new Set(q.match(/[\p{Script=Han}]{2,6}|[a-z0-9]{2,}/gu) || []))) {
    if (body.includes(token)) score += 8;
  }
  return score;
}

const results = knowledge.entries.map((entry) => {
  const routeHit = routeHits.get(entry.id);
  const score = (routeHit?.score || 0) + hardRuleScore(entry) + lexicalScore(entry);
  return {
    id: entry.id,
    title: entry.title,
    intent: entry.intent,
    score,
    matchedQuestions: (routeHit?.routes || []).slice(0, 5),
    answerMarkdown: entry.answerMarkdown,
    safeBoundary: entry.safeBoundary,
    nextAction: entry.nextAction,
    recommendedLinks: entry.recommendedLinks || [],
  };
}).filter((item) => item.score > 0).sort((a, b) => b.score - a.score).slice(0, limit);

if (json) {
  console.log(JSON.stringify({ question, results }, null, 2));
} else {
  console.log(`问题：${question}`);
  console.log(`命中结果：${results.length}`);
  for (const [index, item] of results.entries()) {
    console.log(`\n#${index + 1} ${item.title}`);
    console.log(`ID: ${item.id}`);
    console.log(`Intent: ${item.intent}`);
    console.log(`Score: ${item.score}`);
    if (item.matchedQuestions.length) console.log(`Matched routes: ${item.matchedQuestions.join(" / ")}`);
    console.log("\n标准回答：");
    console.log(item.answerMarkdown || "暂无");
    if (item.safeBoundary) {
      console.log("\n合规边界：");
      console.log(item.safeBoundary);
    }
    if (item.nextAction) {
      console.log("\n下一步建议：");
      console.log(item.nextAction);
    }
  }
}
