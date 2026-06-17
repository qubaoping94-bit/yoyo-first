#!/usr/bin/env node

const checks = [
  { label: 'Website hub', url: 'https://youyou-sites-list.pages.dev/', mustContain: '优优智构网站总汇' },
  { label: 'AI gallery', url: 'https://youyou-ai-gallery.pages.dev/', mustContain: '优优AI图库' },
  { label: 'Product-evolution hub', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/' },
  { label: 'Moments copy site', url: 'https://youyou-ai-gallery.pages.dev/moments/', mustContain: '优优AI朋友圈文案站' },
  { label: 'Industry sample', url: 'https://youyou-ai-growth-advisor.pages.dev/youyou-board/', mustContain: '产业样本' },
  { label: 'Core board', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-wuji-board/' },
  { label: 'Environmental cognition', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-wuji-environmental-demo/' },
  { label: 'Indoor panel material evolution', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/indoor-panel-eco-material-evolution-demo/' },
  { label: 'Diet to living awareness', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/diet-to-living-material-awareness-demo/' },
  { label: 'A-class noncombustible', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-a-class-noncombustible-demo/' },
  { label: 'Core raw material', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-core-raw-material-demo/' },
  { label: 'Waterproof and moisture-proof', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-waterproof-moisture-proof-demo/' },
  { label: 'Antibacterial mildew-proof', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-antibacterial-mildew-proof-demo/' },
  { label: 'Thermal storage humidity', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-thermal-storage-humidity-demo/' },
  { label: 'Dry-humid thermal cycle', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-thermal-cycle-dry-humid-crack-resistant-demo/' },
  { label: 'Sound insulation', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-sound-insulation-noise-reduction-demo/' },
  { label: 'Impact deformation', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-1-2-density-impact-deformation-demo/' },
  { label: 'Functional panorama', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-functional-panorama-summary-demo/' },
  { label: 'Lifetime performance', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-composite-product-lifetime-performance-demo/' },
  { label: 'Core material', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-core-material-demo/' },
  { label: 'Three-in-one dual wheel', url: 'https://youyou-ai-gallery.pages.dev/product-evolution/youyou-three-in-one-dual-wheel-demo/' },
];

function timeoutSignal(ms) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  return { signal: controller.signal, cancel: () => clearTimeout(timer) };
}

async function checkUrl(check) {
  const timeout = timeoutSignal(20000);
  try {
    const response = await fetch(check.url, {
      method: 'GET',
      redirect: 'follow',
      signal: timeout.signal,
      headers: { 'user-agent': 'youyou-inorganic-board-guide-link-check/1.1' },
    });
    const body = await response.text();
    const contentType = response.headers.get('content-type') || '';
    const result = {
      ...check,
      ok: response.ok,
      status: response.status,
      contentType,
      length: body.length,
    };

    if (!response.ok) return result;
    if (!contentType.includes('text/html')) {
      return { ...result, ok: false, error: `unexpected content-type: ${contentType}` };
    }
    if (body.length < 500) {
      return { ...result, ok: false, error: `short html body: ${body.length}` };
    }
    if (check.mustContain && !body.includes(check.mustContain)) {
      return { ...result, ok: false, error: `missing expected text: ${check.mustContain}` };
    }
    return result;
  } catch (error) {
    return { ...check, ok: false, status: 'ERROR', error: error.message };
  } finally {
    timeout.cancel();
  }
}

const results = await Promise.all(checks.map(checkUrl));
const failed = results.filter((result) => !result.ok);

for (const result of results) {
  const status = result.ok ? 'OK' : 'FAIL';
  const detail = result.error ? ` ${result.error}` : ` ${result.length || 0} chars`;
  console.log(`[${status}] ${result.status} ${result.label} ${result.url}${detail}`);
}

if (failed.length > 0) {
  console.error(`\n${failed.length} link(s) failed.`);
  process.exit(1);
}

console.log(`\nAll ${results.length} link(s) passed.`);
