#!/usr/bin/env node

const BASE_URL = 'https://youyou-ai-gallery.pages.dev';
const DATA_URL = `${BASE_URL}/assets/gallery-data.js`;
const OCR_URL = `${BASE_URL}/assets/gallery-ocr-data.js`;

const PROFILE_LABELS = {
  waterproof: '防水防潮',
  mildew: '防霉洁净',
  fire: '阻燃防火',
  sound: '隔音静音',
  stability: '稳定耐用',
  product: '产品结构',
  door: '无机门',
  wall: '无机墙板',
  dealer: '经销商转发',
  case: '项目案例',
  ai: 'AI企业赋能',
};

const PERFORMANCE_PROFILE_NAMES = new Set(['waterproof', 'mildew', 'fire', 'sound', 'stability']);

const TOPIC_PROFILES = [
  {
    name: 'waterproof',
    triggers: ['防水', '防潮', '潮湿', '回南天', '厨卫', '湿区'],
    keywords: ['防水', '防潮', '潮湿', '回南天', '厨卫', '湿区', '无机板', '不怕潮'],
    categoryBoost: { 'cat-06': 14, 'cat-08': 8, 'cat-02': 4 },
  },
  {
    name: 'mildew',
    triggers: ['防霉', '抗菌', '霉', '卫生', '洁净'],
    keywords: ['防霉', '抗菌', '卫生', '潮湿', '洁净', '无机板', '易清洁'],
    categoryBoost: { 'cat-06': 14, 'cat-08': 8 },
  },
  {
    name: 'fire',
    triggers: ['阻燃', '不燃', '防火', 'a级', 'A级', '安全'],
    keywords: ['阻燃', '不燃', '防火', 'A级', '安全', '无机板', '核心材料'],
    categoryBoost: { 'cat-06': 14, 'cat-08': 8 },
  },
  {
    name: 'sound',
    triggers: ['隔音', '降噪', '静音', '噪音', '安静'],
    keywords: ['隔音', '降噪', '静音', '无机门', '门板', '酒店', '芯材'],
    categoryBoost: { 'cat-06': 10, 'cat-02': 8, 'cat-08': 4 },
  },
  {
    name: 'stability',
    triggers: ['不开裂', '不变形', '开裂', '变形', '冷热', '极干', '极潮', '稳定', '寿命', '耐用'],
    keywords: ['不开裂', '不变形', '稳定', '冷热', '极干', '极潮', '寿命', '耐用', '结构'],
    categoryBoost: { 'cat-06': 12, 'cat-02': 8, 'cat-08': 6 },
  },
  {
    name: 'product',
    triggers: ['产品', '样板', '结构', '厚度', '截面', '板材', '无机板', '玄武岩', '材料'],
    keywords: ['产品', '样板', '结构', '厚度', '截面', '板材', '无机板', '玄武岩', '材料', '复合'],
    categoryBoost: { 'cat-02': 14, 'cat-06': 8, 'cat-08': 6 },
  },
  {
    name: 'door',
    triggers: ['无机门', '门板', '门'],
    keywords: ['无机门', '门板', '静音', '芯材', '门墙柜', '门套'],
    categoryBoost: { 'cat-02': 12, 'cat-08': 8, 'cat-06': 4 },
  },
  {
    name: 'wall',
    triggers: ['墙板', '墙面', '墙'],
    keywords: ['墙板', '墙面', '12mm', '空间', '无机墙板', '护墙'],
    categoryBoost: { 'cat-02': 10, 'cat-05': 8, 'cat-08': 6 },
  },
  {
    name: 'dealer',
    triggers: ['经销商', '招商', '朋友圈', '转发', '渠道', '代理'],
    keywords: ['经销商', '招商', '朋友圈', '渠道', '转发', '代理', '优优无机板'],
    categoryBoost: { 'cat-01': 14, 'cat-08': 8, 'cat-06': 4 },
  },
  {
    name: 'case',
    triggers: ['案例', '项目', '现场', '落地', '应用'],
    keywords: ['项目', '案例', '现场', '空间', '应用', '落地'],
    categoryBoost: { 'cat-05': 16, 'cat-08': 8 },
  },
  {
    name: 'ai',
    triggers: ['AI', 'ai', '赋能', '企业', '增长', '系统'],
    keywords: ['AI', '赋能', '企业', '增长', '系统', '优优', '训练样本'],
    categoryBoost: { 'cat-07': 18, 'cat-08': 6 },
  },
];

function parseArgs(argv) {
  const args = argv.slice(2);
  const options = { limit: 3, json: false };
  const queryParts = [];
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === '--limit') {
      options.limit = Math.max(1, Math.min(8, Number(args[index + 1] || 3)));
      index += 1;
    } else if (arg === '--json') {
      options.json = true;
    } else {
      queryParts.push(arg);
    }
  }
  return { query: queryParts.join(' ').trim(), options };
}

function normalizeUrl(path) {
  if (!path) return '';
  if (/^https?:\/\//i.test(path)) return path;
  return `${BASE_URL}${path.startsWith('/') ? '' : '/'}${path}`;
}

function parseAssignment(text, variableNames) {
  const alternatives = variableNames.map((name) => name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  const assignment = new RegExp(`window\\.(${alternatives})\\s*=\\s*`, 'm').exec(text);
  if (!assignment) {
    throw new Error(`Could not find assignment for ${variableNames.join(' or ')}`);
  }

  const start = findJsonStart(text, assignment.index + assignment[0].length);
  if (start < 0) {
    throw new Error(`Could not find JSON payload for ${assignment[1]}`);
  }

  const end = findJsonEnd(text, start);
  return JSON.parse(text.slice(start, end + 1));
}

function findJsonStart(text, startIndex) {
  for (let index = startIndex; index < text.length; index += 1) {
    if (text[index] === '{' || text[index] === '[') return index;
    if (!/\s/.test(text[index])) return -1;
  }
  return -1;
}

function findJsonEnd(text, startIndex) {
  const opener = text[startIndex];
  const closer = opener === '{' ? '}' : ']';
  let depth = 0;
  let quote = '';
  let escaped = false;

  for (let index = startIndex; index < text.length; index += 1) {
    const char = text[index];
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (char === '\\') {
        escaped = true;
      } else if (char === quote) {
        quote = '';
      }
      continue;
    }

    if (char === '"' || char === "'") {
      quote = char;
    } else if (char === opener) {
      depth += 1;
    } else if (char === closer) {
      depth -= 1;
      if (depth === 0) return index;
    }
  }

  throw new Error('Could not find end of JSON assignment');
}

async function fetchAssignmentJson(url, variableNames) {
  const response = await fetch(url, {
    headers: { 'user-agent': 'youyou-inorganic-board-guide-image-router/1.1' },
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status}`);
  }
  return parseAssignment(await response.text(), variableNames);
}

async function loadGalleryBundle() {
  const [galleryData, ocrData] = await Promise.all([
    fetchAssignmentJson(DATA_URL, ['YOUYOU_GALLERY_DATA']),
    fetchAssignmentJson(OCR_URL, ['YOUYOU_GALLERY_OCR', 'YOUYOU_GALLERY_OCR_DATA']),
  ]);
  return { images: galleryData.images || [], ocrIndex: buildOcrIndex(ocrData) };
}

function buildOcrIndex(ocrData) {
  const index = new Map();
  if (Array.isArray(ocrData)) {
    for (const item of ocrData) addOcrItem(index, item?.id, item);
    return index;
  }

  for (const [key, value] of Object.entries(ocrData || {})) {
    addOcrItem(index, key, value);
  }

  for (const key of ['images', 'items', 'ocr']) {
    const items = ocrData?.[key];
    if (Array.isArray(items)) {
      for (const item of items) addOcrItem(index, item?.id || item?.imageId || item?.src, item);
    }
  }
  return index;
}

function addOcrItem(index, key, item) {
  if (!item) return;
  if (key) index.set(String(key), item);
  if (item.id) index.set(String(item.id), item);
  if (item.src) index.set(String(item.src), item);
}

function enrichWithOcr(image, ocrIndex) {
  const ocr = ocrIndex.get(String(image.id)) || ocrIndex.get(String(image.src)) || {};
  return {
    ...image,
    ocrText: ocr.text || '',
    ocrConfidence: typeof ocr.confidence === 'number' ? ocr.confidence : null,
  };
}

function normalizeForMatch(text) {
  return String(text || '')
    .normalize('NFKC')
    .toLowerCase()
    .replace(/[\s\r\n\t|,，。；;、/\\()（）【】\[\]{}:：!！?？“”"'‘’·.\-—_]+/g, '');
}

function tokenize(text) {
  return Array.from(
    new Set(
      String(text || '')
        .normalize('NFKC')
        .toLowerCase()
        .split(/[\s,，。；;、/\\()（）【】\[\]{}:：!！?？“”"'‘’·.\-—_]+/)
        .filter((token) => token.length >= 2),
    ),
  );
}

function findProfiles(query) {
  const normalizedQuery = normalizeForMatch(query);
  return TOPIC_PROFILES.filter((profile) =>
    profile.triggers.some((trigger) => normalizedQuery.includes(normalizeForMatch(trigger))),
  );
}

function queryTerms(query, profiles) {
  const terms = new Set(tokenize(query));
  const normalizedQuery = normalizeForMatch(query);
  for (const profile of profiles) {
    for (const term of [...profile.triggers, ...profile.keywords]) {
      const normalized = normalizeForMatch(term);
      if (normalized.length >= 2 && normalizedQuery.includes(normalized)) terms.add(term);
    }
  }
  if (terms.size === 0 && normalizedQuery.length >= 2) {
    terms.add(query);
  }
  return Array.from(terms)
    .map((term) => ({ raw: String(term), normalized: normalizeForMatch(term) }))
    .filter((term) => term.normalized.length >= 2);
}

function wantsHistoricStyle(query) {
  const normalized = normalizeForMatch(query);
  return ['国风', '古代', '古风', '诗词', '古人'].some((term) => normalized.includes(normalizeForMatch(term)));
}

function hasHistoricSignal(image) {
  const normalized = normalizeForMatch([
    image.title,
    image.category,
    image.series,
    image.useCase,
    image.prompt,
    image.sourceName,
  ].filter(Boolean).join('\n'));
  return ['古代人物', '古代风景', '诗词', '国风', '古风'].some((term) => normalized.includes(normalizeForMatch(term)));
}

function profileHasPerformanceTopic(profiles) {
  return profiles.some((profile) => PERFORMANCE_PROFILE_NAMES.has(profile.name));
}

function scoreImage(image, query, terms, profiles) {
  const enriched = image;
  const ocrText = enriched.ocrText || '';
  const ocrNorm = normalizeForMatch(ocrText);
  const metaText = [
    enriched.title,
    enriched.category,
    enriched.series,
    enriched.useCase,
    enriched.prompt,
    enriched.notes,
    enriched.sourceName,
  ].filter(Boolean).join('\n');
  const metaNorm = normalizeForMatch(metaText);

  let score = 0;
  const matchedOcrTerms = [];

  for (const term of terms) {
    if (ocrNorm.includes(term.normalized)) {
      score += 24;
      matchedOcrTerms.push(term.raw);
    }
    if (metaNorm.includes(term.normalized)) score += 5;
  }

  for (const profile of profiles) {
    for (const keyword of profile.keywords) {
      const normalizedKeyword = normalizeForMatch(keyword);
      if (ocrNorm.includes(normalizedKeyword)) {
        score += 14;
        matchedOcrTerms.push(keyword);
      }
      if (metaNorm.includes(normalizedKeyword)) score += 3;
    }
    score += profile.categoryBoost?.[enriched.categorySlug] || 0;
  }

  if (ocrText.trim()) score += 7;
  else score -= 12;

  if (typeof enriched.ocrConfidence === 'number') {
    score += Math.max(0, Math.min(4, Math.floor(enriched.ocrConfidence / 25)));
  }

  if (profileHasPerformanceTopic(profiles)) {
    if (enriched.categorySlug === 'cat-06') score += 10;
    if (['材料结构', '结构剖面', '工程可信', '参数', '核心材料'].some((term) => ocrNorm.includes(normalizeForMatch(term)) || metaNorm.includes(normalizeForMatch(term)))) {
      score += 5;
    }
  }

  if (!wantsHistoricStyle(query) && hasHistoricSignal(enriched)) score -= 18;
  if (enriched.width && enriched.height) score += 2;

  return {
    score,
    matchedOcrTerms: uniqueTermsByNormalized(matchedOcrTerms).slice(0, 6),
  };
}

function uniqueTermsByNormalized(terms) {
  const seen = new Set();
  const result = [];
  for (const term of terms) {
    const normalized = normalizeForMatch(term);
    if (!normalized || seen.has(normalized)) continue;
    seen.add(normalized);
    result.push(term);
  }
  return result;
}

function compactOcrPreview(text, matchedTerms = []) {
  const compact = String(text || '')
    .replace(/\s+/g, ' ')
    .replace(/\s*([，。；：、,.!?！？])\s*/g, '$1')
    .trim();
  if (!compact) return '';

  for (const term of matchedTerms) {
    const index = compact.indexOf(String(term));
    if (index >= 0) {
      const start = Math.max(0, index - 45);
      return compact.slice(start, start + 120);
    }
  }
  return compact.slice(0, 120);
}

function reasonFor(image, profiles, matchedOcrTerms) {
  const category = image.category || '优优图库';
  const labels = profiles.map((profile) => PROFILE_LABELS[profile.name] || profile.name).join('、');
  if (matchedOcrTerms.length > 0) {
    return `图片文字命中「${matchedOcrTerms.slice(0, 4).join('、')}」，适合补充${labels || '产品'}主题，来源：${category}`;
  }
  return `来源：${category}，与${labels || '产品'}主题的标题、分类或提示词相近`;
}

function selectImages(images, ocrIndex, query, limit) {
  const profiles = findProfiles(query);
  const fallbackProfiles = profiles.length > 0
    ? profiles
    : [TOPIC_PROFILES.find((profile) => profile.name === 'product')];
  const terms = queryTerms(query, fallbackProfiles);

  const scored = images
    .map((rawImage) => {
      const image = enrichWithOcr(rawImage, ocrIndex);
      const result = scoreImage(image, query, terms, fallbackProfiles);
      return { image, ...result };
    })
    .filter((entry) => entry.score > 0 && entry.image.src && entry.image.thumb)
    .sort((a, b) => b.score - a.score || String(a.image.id).localeCompare(String(b.image.id)));

  const selected = [];
  const seenCategories = new Map();
  for (const entry of scored) {
    const categoryCount = seenCategories.get(entry.image.categorySlug) || 0;
    if (categoryCount >= Math.max(2, Math.ceil(limit / 2))) continue;
    selected.push({
      id: entry.image.id,
      title: entry.image.title,
      category: entry.image.category,
      score: entry.score,
      ocrConfidence: entry.image.ocrConfidence,
      ocrMatchedTerms: entry.matchedOcrTerms,
      imageText: compactOcrPreview(entry.image.ocrText, entry.matchedOcrTerms),
      reason: reasonFor(entry.image, fallbackProfiles, entry.matchedOcrTerms),
      imageUrl: normalizeUrl(entry.image.src),
      thumbUrl: normalizeUrl(entry.image.thumb),
    });
    seenCategories.set(entry.image.categorySlug, categoryCount + 1);
    if (selected.length >= limit) break;
  }
  return selected;
}

const { query, options } = parseArgs(process.argv);
if (!query) {
  console.error('Usage: node scripts/find-gallery-images.mjs "<customer question or topic>" [--limit 3] [--json]');
  process.exit(2);
}

const { images, ocrIndex } = await loadGalleryBundle();
const results = selectImages(images, ocrIndex, query, options.limit);

if (results.length === 0) {
  console.error(`No matching gallery images found for: ${query}`);
  process.exit(1);
}

if (options.json) {
  console.log(JSON.stringify({ query, count: results.length, results }, null, 2));
} else {
  console.log(`配套图片建议：${query}\n`);
  results.forEach((result, index) => {
    console.log(`${index + 1}. ${result.title}`);
    console.log(`   理由：${result.reason}`);
    if (result.ocrMatchedTerms.length > 0) {
      console.log(`   图片文字命中：${result.ocrMatchedTerms.join('、')}`);
    }
    if (result.imageText) {
      console.log(`   图片文字摘录：${result.imageText}`);
    }
    console.log(`   缩略图：${result.thumbUrl}`);
    console.log(`   高清图：${result.imageUrl}`);
    console.log(`   Markdown：[![${result.title}](${result.thumbUrl})](${result.imageUrl})`);
  });
}
