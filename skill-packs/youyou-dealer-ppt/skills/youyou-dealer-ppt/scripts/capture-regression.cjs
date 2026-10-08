// Capture every candidate page at 1920×1080 for visual comparison with the approved sample.
const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
const fs = require('fs');
const path = require('path');

async function main() {
  const [html, out, browserPath] = process.argv.slice(2);
  if (!html || !out || !browserPath) throw new Error('Usage: node capture-regression.cjs <index.html> <output-dir> <browser-path>');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: browserPath, headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(path.resolve(html)).href);
    const ids = await page.locator('.slide').evaluateAll(nodes => nodes.map(n => n.dataset.slideId));
    for (let i = 0; i < ids.length; i++) {
      await page.evaluate(index => show(index), i);
      await page.screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, '0')}-${ids[i]}.png`) });
    }
    const errors = await page.locator('.slide.active').count() !== 1 ? ['active slide count'] : [];
    fs.writeFileSync(path.join(out, 'capture-report.json'), JSON.stringify({ ids, errors, status: errors.length ? 'FAIL' : 'PASS' }, null, 2));
    if (errors.length) process.exitCode = 1;
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
