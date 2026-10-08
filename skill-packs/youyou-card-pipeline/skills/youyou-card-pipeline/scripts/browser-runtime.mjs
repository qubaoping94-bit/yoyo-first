import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

export function options(argv){
  const result={};
  for(let i=0;i<argv.length;i++){
    if(!argv[i].startsWith('--')||!argv[i+1]||argv[i+1].startsWith('--'))throw new Error('Arguments must be --name value pairs');
    const name=argv[i].slice(2);
    if(!['html','output','report','playwright-module','channel'].includes(name))throw new Error(`Unknown option: ${name}`);
    result[name]=argv[++i];
  }
  if(!result.html)throw new Error('--html is required');
  return result;
}

export async function openDocument(opts){
  let api;
  try{api=opts['playwright-module']?await import(pathToFileURL(path.resolve(opts['playwright-module'])).href):await import('playwright');}
  catch(error){throw new Error('Playwright unavailable. Run npm install in the skill folder, or pass --playwright-module with a verified existing entry file. '+error.message);}
  const chromium=api.chromium??api.default?.chromium;
  const browser=await chromium.launch({headless:true,...(opts.channel?{channel:opts.channel}:{})});
  const page=await browser.newPage({viewport:{width:1200,height:1600},deviceScaleFactor:1});
  try{
    await page.route('**/*',route=>/^https?:/.test(route.request().url())?route.abort():route.continue());
    await page.goto(pathToFileURL(path.resolve(opts.html)).href,{waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    return {browser,page};
  }catch(error){await browser.close();throw error;}
}

export async function inspect(page){
  return page.evaluate(()=>{
    const issues=[],warnings=[],cards=Array.from(document.querySelectorAll('.poster.xhs'));
    if(cards.length!==8)issues.push(`Expected 8 cards, found ${cards.length}`);
    const sizes={'.node-title':48,'.node-body':30,'.ledger-num':100,'.ledger-lbl':52,'.sub':28,'.mod-title':46,'.mod-bullets li':32,'.lead':38,'.t-cat':25,'.chrome-min':20};
    const metrics=cards.map((card,i)=>{
      const box=card.getBoundingClientRect(),id=card.id;
      if(id!==`xhs-${String(i+1).padStart(2,'0')}`)issues.push(`Unexpected card id/order: ${id}`);
      if(Math.abs(box.width-1080)>.1||Math.abs(box.height-1440)>.1)issues.push(`${id}: canvas ${box.width}×${box.height}`);
      if(card.scrollHeight>card.clientHeight+1||card.scrollWidth>card.clientWidth+1)issues.push(`${id}: canvas overflow`);
      for(const [selector,size] of Object.entries(sizes)){
        for(const el of card.querySelectorAll(selector))if(Math.abs(parseFloat(getComputedStyle(el).fontSize)-size)>.1)issues.push(`${id}: ${selector} must be ${size}px`);
      }
      for(const el of card.querySelectorAll('.h-xl')){
        const expected=el.closest('.closing-block')?52:112;
        if(Math.abs(parseFloat(getComputedStyle(el).fontSize)-expected)>.1)issues.push(`${id}: title font must be ${expected}px`);
      }
      for(const el of card.querySelectorAll('.title-line,.node-title,.node-body,.node-sub,.ledger-num,.ledger-lbl,.sub,.mod-title,li,.lead,.t-cat,.chrome-min')){
        if(!el.textContent.trim())continue;
        const r=el.getBoundingClientRect();
        if(r.width<=0||r.height<=0||r.left<box.left+55||r.right>box.right-55||r.top<box.top+55||r.bottom>box.bottom-55)issues.push(`${id}: text block outside content boundary (${el.className||el.tagName})`);
        const range=document.createRange();range.selectNodeContents(el);
        const text=range.getBoundingClientRect();
        // Font glyph bounds can extend beyond a CSS line box, especially CJK.
        // Preserve a small em-relative vertical allowance; horizontal spill is not allowed.
        const glyphAllowance=Math.ceil(parseFloat(getComputedStyle(el).fontSize)*0.2)+1;
        if(text.right>r.right+2||text.left<r.left-2||text.bottom>r.bottom+glyphAllowance||text.top<r.top-glyphAllowance)issues.push(`${id}: text exceeds its own block (${el.className||el.tagName})`);
        const container=el.closest('.node,.card-ink,.card-fill,.ledger-row,.closing-block');
        if(container){const p=container.getBoundingClientRect();if(r.top<p.top-1||r.bottom>p.bottom+1||r.left<p.left-1||r.right>p.right+1)issues.push(`${id}: text outside panel (${el.className||el.tagName})`);}
      }
      const panel=card.querySelector('.fill');
      if(panel&&panel.getBoundingClientRect().height<430)warnings.push(`${id}: short main panel; review density visually`);
      if(card.classList.contains('closing')){
        const closing=card.querySelector('.closing-block');
        if(!closing||getComputedStyle(closing).backgroundColor!=='rgb(0, 47, 167)')issues.push(`${id}: closing blue block missing`);
      }
      return {id,width:box.width,height:box.height,scrollHeight:card.scrollHeight};
    });
    return {ok:issues.length===0,issues:[...new Set(issues)],warnings,metrics};
  });
}

export async function saveReport(file,data){
  await fs.mkdir(path.dirname(path.resolve(file)),{recursive:true});
  await fs.writeFile(file,JSON.stringify(data,null,2),'utf8');
}
