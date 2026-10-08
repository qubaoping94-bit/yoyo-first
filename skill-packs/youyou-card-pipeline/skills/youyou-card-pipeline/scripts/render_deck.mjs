import path from 'node:path';
import fs from 'node:fs/promises';
import {options,openDocument,inspect,saveReport} from './browser-runtime.mjs';

async function main(){
  const opts=options(process.argv.slice(2));
  if(!opts.output)throw new Error('--output is required');
  const {browser,page}=await openDocument(opts);
  try{
    const report=await inspect(page);
    if(report.ok){
      await fs.mkdir(opts.output,{recursive:true});
      report.files=[];
      for(const card of report.metrics){
        const destination=path.join(opts.output,`${card.id}.png`);
        await page.locator(`#${card.id}`).screenshot({path:destination});
        const bytes=await fs.readFile(destination),width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);
        if(width!==1080||height!==1440){report.ok=false;report.issues.push(`${card.id}: PNG ${width}×${height}`);}
        report.files.push({name:path.basename(destination),width,height});
      }
    }
    await saveReport(opts.report??path.join(opts.output,'validation.json'),report);
    console.log(JSON.stringify(report,null,2));
    process.exitCode=report.ok?0:1;
  }finally{await browser.close();}
}
main().catch(error=>{console.error(error.message);process.exitCode=2;});
