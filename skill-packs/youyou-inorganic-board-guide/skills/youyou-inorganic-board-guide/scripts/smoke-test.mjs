#!/usr/bin/env node

import { readFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const requiredFiles = [
  'SKILL.md',
  'agents/openai.yaml',
  'references/knowledge-map.md',
  'references/audience-playbooks.md',
  'references/website-router.md',
  'references/faq-and-sales-scripts.md',
  'references/response-templates.md',
  'references/claim-safety-checklist.md',
  'references/sample-outputs.md',
  'scripts/check-links.mjs',
  'scripts/smoke-test.mjs',
];

const issues = [];

for (const rel of requiredFiles) {
  if (!existsSync(join(root, rel))) {
    issues.push(`Missing ${rel}`);
  }
}

function read(rel) {
  return readFileSync(join(root, rel), 'utf8');
}

if (issues.length === 0) {
  const skill = read('SKILL.md');
  const contentFiles = requiredFiles.filter((rel) => rel.endsWith('.md') || rel.endsWith('.yaml'));
  const allText = contentFiles
    .map((rel) => `${rel}\n${read(rel)}`)
    .join('\n\n');

  const requiredPhrases = [
    '优优无机板产品顾问',
    'Service Modes',
    'Output Contracts',
    'Common Pitfalls',
    'claim-safety-checklist.md',
    'response-templates.md',
    'audience-playbooks.md',
    'youyou-sites-list.pages.dev',
    'youyou-ai-gallery.pages.dev/product-evolution',
    '$youyou-inorganic-board-guide',
  ];

  for (const phrase of requiredPhrases) {
    if (!allText.includes(phrase)) {
      issues.push(`Missing required phrase: ${phrase}`);
    }
  }

  const forbidden = [
    '[TODO',
    'Create only the resource directories',
    'Examples from other skills',
    'Appropriate for:',
    'Cookie',
    'Token',
    'API Key',
  ];

  for (const phrase of forbidden) {
    if (allText.includes(phrase)) {
      issues.push(`Forbidden placeholder or sensitive phrase found: ${phrase}`);
    }
  }

  if ((skill.match(/^## /gm) || []).length < 7) {
    issues.push('SKILL.md should have a complete top-level structure.');
  }
}

if (issues.length > 0) {
  for (const issue of issues) {
    console.error(`[FAIL] ${issue}`);
  }
  process.exit(1);
}

console.log('Smoke test passed.');
