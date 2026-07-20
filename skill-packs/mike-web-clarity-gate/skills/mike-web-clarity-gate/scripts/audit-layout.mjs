#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { createRequire } from "node:module";

const [targetUrl, outputArg = "clarity-audit"] = process.argv.slice(2);
if (!targetUrl) {
  console.error("Usage: node audit-layout.mjs <url> [output-directory]");
  process.exit(2);
}

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  try {
    const requireFromProject = createRequire(path.join(process.cwd(), "package.json"));
    ({ chromium } = requireFromProject("playwright"));
  } catch {
    try {
      const moduleRoot = process.env.CODEX_NODE_MODULES || process.env.NODE_PATH?.split(path.delimiter).find(Boolean);
      if (!moduleRoot) throw new Error("No external module root configured");
      const requireFromRuntime = createRequire(path.join(path.dirname(moduleRoot), "package.json"));
      ({ chromium } = requireFromRuntime("playwright"));
    } catch {
      console.error("Playwright is required. Install it in the current project or set CODEX_NODE_MODULES to a Node modules directory.");
      process.exit(2);
    }
  }
}

const outputDir = path.resolve(outputArg);
await fs.mkdir(outputDir, { recursive: true });

const viewports = [
  { name: "desktop-1440x900", width: 1440, height: 900 },
  { name: "tablet-1024x768", width: 1024, height: 768 },
  { name: "mobile-390x844", width: 390, height: 844 },
  { name: "mobile-360x800", width: 360, height: 800 },
];

let browser;
try {
  browser = await chromium.launch({ headless: true });
} catch (error) {
  if (!String(error).includes("Executable doesn't exist")) throw error;
  browser = await chromium.launch({ headless: true, channel: "chrome" });
}
const results = [];

for (const viewport of viewports) {
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();
  const consoleErrors = [];
  const requestFailures = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("requestfailed", (request) => {
    requestFailures.push({ url: request.url(), error: request.failure()?.errorText ?? "unknown" });
  });

  let status = null;
  let navigationError = null;
  try {
    const response = await page.goto(targetUrl, { waitUntil: "networkidle", timeout: 30000 });
    status = response?.status() ?? null;
  } catch (error) {
    navigationError = String(error);
  }

  const metrics = await page.evaluate(() => {
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
    };
    const lineCount = (element) => {
      const range = document.createRange();
      range.selectNodeContents(element);
      const tops = [...range.getClientRects()]
        .filter((rect) => rect.width > 1 && rect.height > 1)
        .map((rect) => Math.round(rect.top));
      return new Set(tops).size || 1;
    };
    const headings = [...document.querySelectorAll("h1,h2,h3")].filter(visible).map((element) => {
      const rect = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      return {
        tag: element.tagName.toLowerCase(),
        text: element.textContent.replace(/\s+/g, " ").trim(),
        selector: element.id ? `#${element.id}` : element.className ? `${element.tagName.toLowerCase()}.${String(element.className).trim().split(/\s+/).join(".")}` : element.tagName.toLowerCase(),
        lines: lineCount(element),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        fontSize: style.fontSize,
        lineHeight: style.lineHeight,
        manualBreaks: element.querySelectorAll("br").length,
      };
    });
    const main = document.querySelector("main") || document.body;
    const firstSection = main.querySelector(":scope > section, :scope > header, section, header");
    const heroRect = firstSection?.getBoundingClientRect();
    const candidates = [...document.querySelectorAll("main > *, main section, main article")].filter(visible).slice(0, 30);
    const leftEdges = candidates.map((element) => Math.round(element.getBoundingClientRect().left));
    const alignmentFrequency = Object.entries(leftEdges.reduce((acc, value) => ({ ...acc, [value]: (acc[value] || 0) + 1 }), {}))
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([left, count]) => ({ left: Number(left), count }));
    return {
      title: document.title,
      documentWidth: document.documentElement.scrollWidth,
      viewportWidth: window.innerWidth,
      horizontalOverflow: Math.max(0, document.documentElement.scrollWidth - window.innerWidth),
      heroHeight: heroRect ? Math.round(heroRect.height) : null,
      heroViewportRatio: heroRect ? Number((heroRect.height / window.innerHeight).toFixed(2)) : null,
      headings,
      multiLineDesktopHeadings: window.innerWidth >= 1024 ? headings.filter((heading) => heading.lines > 1) : [],
      manualHeadingBreaks: headings.filter((heading) => heading.manualBreaks > 0),
      alignmentFrequency,
    };
  });

  const screenshot = path.join(outputDir, `${viewport.name}.png`);
  await page.screenshot({ path: screenshot, fullPage: true });
  results.push({ viewport, url: targetUrl, status, navigationError, consoleErrors, requestFailures, screenshot, metrics });
  await context.close();
}

await browser.close();

const summary = {
  generatedAt: new Date().toISOString(),
  targetUrl,
  gateSignals: {
    navigationFailures: results.filter((item) => item.navigationError || (item.status && item.status >= 400)).length,
    overflowViewports: results.filter((item) => item.metrics.horizontalOverflow > 0).length,
    desktopMultiLineHeadings: results.reduce((sum, item) => sum + item.metrics.multiLineDesktopHeadings.length, 0),
    manualHeadingBreaks: results.reduce((sum, item) => sum + item.metrics.manualHeadingBreaks.length, 0),
    consoleErrors: results.reduce((sum, item) => sum + item.consoleErrors.length, 0),
    requestFailures: results.reduce((sum, item) => sum + item.requestFailures.length, 0),
  },
  results,
};

await fs.writeFile(path.join(outputDir, "clarity-audit.json"), JSON.stringify(summary, null, 2), "utf8");
const lines = [
  "# Website clarity audit",
  "",
  `- URL: ${targetUrl}`,
  `- Generated: ${summary.generatedAt}`,
  `- Desktop multi-line headings: ${summary.gateSignals.desktopMultiLineHeadings}`,
  `- Manual heading breaks: ${summary.gateSignals.manualHeadingBreaks}`,
  `- Overflow viewports: ${summary.gateSignals.overflowViewports}`,
  `- Console errors: ${summary.gateSignals.consoleErrors}`,
  `- Request failures: ${summary.gateSignals.requestFailures}`,
  "",
  "Automation reports signals only. Complete the human non-AI-language and layout-coordination review from references/rubric.md.",
];
await fs.writeFile(path.join(outputDir, "clarity-audit.md"), lines.join("\n"), "utf8");
console.log(JSON.stringify(summary.gateSignals, null, 2));
