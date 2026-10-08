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
    const issues = [];
    for (let i = 0; i < ids.length; i++) {
      await page.evaluate(index => show(index), i);
      const slideIssues = await page.evaluate(() => {
        const active = document.querySelector('.slide.active');
        const main = active.querySelector('main');
        const footTop = active.querySelector('.foot').getBoundingClientRect().top;
        const result = [];
        for (const el of main.querySelectorAll('h1,p,.card,.tablecell,.conclusion')) {
          const rect = el.getBoundingClientRect();
          if (rect.right > innerWidth + 2 || rect.left < -2 || rect.bottom > footTop - 4 || el.scrollWidth > el.clientWidth + 8 || (el.tagName !== 'H1' && el.scrollHeight > el.clientHeight + 16)) result.push({ element: el.tagName.toLowerCase(), text: (el.textContent || '').slice(0, 28), excessX: el.scrollWidth - el.clientWidth, excessY: el.scrollHeight - el.clientHeight });
        }
        return result;
      });
      for (const issue of slideIssues) issues.push({ slide: ids[i], ...issue });
      await page.screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, '0')}-${ids[i]}.png`) });
    }
    for (const viewport of [{ width: 1440, height: 900 }, { width: 1280, height: 720 }]) {
      await page.setViewportSize(viewport);
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      for (let i = 0; i < ids.length; i++) {
        await page.evaluate(index => show(index), i);
        const problems = await page.evaluate(() => {
          const active = document.querySelector('.slide.active');
          const footTop = active.querySelector('.foot').getBoundingClientRect().top;
          return [...active.querySelectorAll('main h1,main p,main .card,main .tablecell,main .conclusion')].filter(el => {
            const r = el.getBoundingClientRect();
            return r.right > innerWidth + 2 || r.left < -2 || r.bottom > footTop - 4 || el.scrollWidth > el.clientWidth + 8 || (el.tagName !== 'H1' && el.scrollHeight > el.clientHeight + 16);
          }).map(el => ({ element: el.tagName.toLowerCase(), text: (el.textContent || '').slice(0, 28) }));
        });
        for (const issue of problems) issues.push({ slide: ids[i], viewport: `${viewport.width}x${viewport.height}`, ...issue });
      }
    }
    if (await page.locator('.slide.active').count() !== 1) issues.push({ slide: ids.at(-1), element: 'active-state', text: 'unexpected active slide count' });
    fs.writeFileSync(path.join(out, 'capture-report.json'), JSON.stringify({ ids, issues, status: issues.length ? 'FAIL' : 'PASS' }, null, 2));
    if (issues.length) { console.error(`${issues.length} visual overflow issues; see capture-report.json`); process.exitCode = 1; }
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
