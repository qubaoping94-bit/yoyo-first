const {chromium}=require('playwright');
const fs=require('fs'),path=require('path');
(async()=>{
  const input=path.resolve(process.argv[2]||'index.html');
  const out=path.resolve(process.argv[3]||'deck-audit');fs.mkdirSync(out,{recursive:true});
  const browser=await chromium.launch({headless:true}),results=[];
  for(const [width,height] of [[1920,1080],[1440,900],[1280,720]]){
    const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'}),errors=[];
    page.on('pageerror',e=>errors.push(String(e)));await page.goto('file:///'+input.replace(/\\/g,'/'));await page.waitForTimeout(700);
    const count=await page.locator('.slide').count(),bad=[];
    const structure=await page.evaluate(()=>{const slides=[...document.querySelectorAll('.slide')],ids=slides.map(s=>s.dataset.slideId||'');return{ids,missingIds:ids.map((x,i)=>x?null:i+1).filter(Boolean),duplicateIds:ids.filter((x,i)=>x&&ids.indexOf(x)!==i),externalRefs:[...document.querySelectorAll('script[src],link[href],img[src]')].map(e=>e.src||e.href).filter(x=>/^https?:/i.test(x)),nthOfType:[...document.styleSheets].flatMap(s=>{try{return[...s.cssRules].map(r=>r.cssText).filter(x=>/nth-of-type\(/.test(x))}catch{return[]}})}});
    for(let i=0;i<count;i++){
      await page.evaluate(i=>deck.show(i),i);await page.waitForTimeout(420);
      const issue=await page.evaluate(i=>{const s=document.querySelectorAll('.slide')[i],sr=s.getBoundingClientRect(),els=[...s.querySelectorAll('h1,h2,h3,p,td,th,.hero-number,.quote,.kicker,.card,.stat,.step,article')].filter(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);return r.width>3&&r.height>3&&c.visibility!=='hidden'&&c.opacity!=='0'}),overflow=els.filter(e=>{const r=e.getBoundingClientRect();return r.left<sr.left-2||r.right>sr.right+2||r.top<sr.top-2||r.bottom>sr.bottom+2}).map(e=>(e.innerText||e.className||e.tagName).slice(0,60)),text=[...s.querySelectorAll('h1,h2,h3,p,td,th,.hero-number,.quote,.kicker')].filter(e=>{const r=e.getBoundingClientRect();return r.width>3&&r.height>3}),overlaps=[];for(let a=0;a<text.length;a++)for(let b=a+1;b<text.length;b++){const x=text[a],y=text[b];if(x.contains(y)||y.contains(x))continue;const A=x.getBoundingClientRect(),B=y.getBoundingClientRect(),ix=Math.min(A.right,B.right)-Math.max(A.left,B.left),iy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);if(ix>5&&iy>5)overlaps.push([(x.innerText||'').slice(0,24),(y.innerText||'').slice(0,24)])}const rects=els.map(e=>e.getBoundingClientRect()),top=Math.min(...rects.map(r=>r.top)),bottom=Math.max(...rects.map(r=>r.bottom));return{overflow,overlaps,verticalUse:Math.round((bottom-top)/sr.height*100)}} ,i);
      if(issue.overflow.length||issue.overlaps.length||issue.verticalUse<48)bad.push({slide:i+1,...issue});
      if(width===1920)await page.screenshot({path:path.join(out,`slide-${String(i+1).padStart(2,'0')}.png`)});
    }
    results.push({viewport:{width,height},count,structure,bad,errors});await page.close();
  }
  fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
