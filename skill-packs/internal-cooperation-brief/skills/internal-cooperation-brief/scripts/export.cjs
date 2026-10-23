#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {pathToFileURL}=require('node:url');
function loadPlaywright(explicit){
  if(explicit)return require(path.resolve(explicit));
  try{return require('playwright');}catch{}
  const cache=path.join(process.env.LOCALAPPDATA||path.join(os.homedir(),'AppData','Local'),'npm-cache','_npx');
  if(fs.existsSync(cache))for(const d of fs.readdirSync(cache)){const p=path.join(cache,d,'node_modules','playwright');if(fs.existsSync(path.join(p,'package.json')))try{return require(p);}catch{}}
  throw Error('未找到Playwright，安装或传 --playwright-path 包目录；不会自动联网安装');
}
async function exportReport(file,explicit){
  const input=path.resolve(file),dir=path.dirname(input),outputs=['report.png','report.pdf','mobile-390.png','checks.json'];
  if(!fs.existsSync(input))throw Error('HTML不存在');
  for(const name of outputs)if(fs.existsSync(path.join(dir,name)))throw Error(name+'已存在，请使用新目录');
  const {chromium}=loadPlaywright(explicit);let browser;
  for(const channel of [null,'msedge','chrome'])try{browser=await chromium.launch({headless:true,...(channel?{channel}:{})});break;}catch{}
  if(!browser)throw Error('没有可启动的Chromium/Edge/Chrome，请安装浏览器后重试');
  try{
    const context=await browser.newContext({viewport:{width:450,height:1000},deviceScaleFactor:2});
    await context.route(/^https?:\/\//,r=>r.abort());
    const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(pathToFileURL(input).href,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
    const report=page.locator('#report');if(await report.count()!==1)throw Error('报告根节点缺失或重复');
    const dimensions=await report.evaluate(e=>({width:e.offsetWidth,height:e.offsetHeight,font:getComputedStyle(e).fontSize}));
    if(dimensions.height>1800)throw Error('图长超过1800 CSS px，请压短重复内容，不缩小正文');
    if(dimensions.font!=='21px')throw Error('450px主图正文未保持21px');
    const png=await report.screenshot();await page.emulateMedia({media:'print'});
    const pdf=await page.pdf({preferCSSPageSize:true,printBackground:true}),pages=(pdf.toString('latin1').match(/\/Type\s*\/Page\b/g)||[]).length;
    if(pages!==1)throw Error('PDF检测到'+pages+'页，请精简内容或修正打印布局');
    await page.emulateMedia({media:'screen'});const checks=[];let mobile;
    for(const width of [360,390,430]){await page.setViewportSize({width,height:844});const state=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,font:getComputedStyle(document.querySelector('#report')).fontSize}));if(state.scroll>width)throw Error(width+'px横向溢出');checks.push(state);if(width===390)mobile=await report.screenshot();}
    if(errors.length)throw Error('页面错误：'+errors.join('; '));
    const result={dimensions,pdfPages:pages,mobile:checks,network:'remote requests blocked',wechat:'actual sending/compression not tested'};
    for(const [name,value] of [['report.png',png],['report.pdf',pdf],['mobile-390.png',mobile],['checks.json',JSON.stringify(result,null,2)+'\n']])fs.writeFileSync(path.join(dir,name),value,{flag:'wx'});
    return result;
  }finally{await browser.close();}
}
if(require.main===module){const [html,...args]=process.argv.slice(2),flag=args.indexOf('--playwright-path');if(!html){console.error('用法：node export.cjs report.html [--playwright-path 包目录]');process.exitCode=1;}else exportReport(html,flag>=0?args[flag+1]:undefined).then(r=>console.log(JSON.stringify(r,null,2))).catch(e=>{console.error('导出失败：'+e.message);process.exitCode=1;});}
module.exports={loadPlaywright,exportReport};
