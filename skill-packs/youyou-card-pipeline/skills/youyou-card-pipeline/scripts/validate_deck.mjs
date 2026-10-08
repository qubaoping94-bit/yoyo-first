import path from 'node:path';
import {options,openDocument,inspect,saveReport} from './browser-runtime.mjs';

async function main(){
  const opts=options(process.argv.slice(2));
  const {browser,page}=await openDocument(opts);
  try{
    const report=await inspect(page);
    await saveReport(opts.report??path.join(path.dirname(path.resolve(opts.html)),'validation.json'),report);
    console.log(JSON.stringify(report,null,2));
    process.exitCode=report.ok?0:1;
  }finally{await browser.close();}
}
main().catch(error=>{console.error(error.message);process.exitCode=2;});
