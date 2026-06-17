#!/usr/bin/env node

const urls = [
  'https://youyou-sites-list.pages.dev/',
  'https://youyou-ai-gallery.pages.dev/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/',
  'https://youyou-ai-gallery.pages.dev/moments/',
  'https://youyou-ai-growth-advisor.pages.dev/youyou-board/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-wuji-board/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-wuji-environmental-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/indoor-panel-eco-material-evolution-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/diet-to-living-material-awareness-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-a-class-noncombustible-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-core-raw-material-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-waterproof-moisture-proof-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-antibacterial-mildew-proof-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-thermal-storage-humidity-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-thermal-cycle-dry-humid-crack-resistant-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-sound-insulation-noise-reduction-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-1-2-density-impact-deformation-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-functional-panorama-summary-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-composite-product-lifetime-performance-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-core-material-demo/',
  'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-three-in-one-dual-wheel-demo/',
];

async function checkUrl(url) {
  for (const method of ['HEAD', 'GET']) {
    try {
      const response = await fetch(url, {
        method,
        redirect: 'follow',
        headers: { 'user-agent': 'youyou-inorganic-board-guide-link-check/1.0' },
      });
      if (response.ok) {
        return { url, ok: true, status: response.status, method };
      }
      if (method === 'GET') {
        return { url, ok: false, status: response.status, method };
      }
    } catch (error) {
      if (method === 'GET') {
        return { url, ok: false, status: 'ERROR', error: error.message, method };
      }
    }
  }
}

const results = await Promise.all(urls.map(checkUrl));
const failed = results.filter((result) => !result.ok);

for (const result of results) {
  const status = result.ok ? 'OK' : 'FAIL';
  const extra = result.error ? ` ${result.error}` : '';
  console.log(`[${status}] ${result.status} ${result.method} ${result.url}${extra}`);
}

if (failed.length > 0) {
  console.error(`\n${failed.length} link(s) failed.`);
  process.exit(1);
}

console.log(`\nAll ${results.length} link(s) passed.`);
