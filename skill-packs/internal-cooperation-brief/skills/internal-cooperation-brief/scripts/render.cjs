#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function text(v,name,fallback){if(v==null&&fallback!==undefined)return fallback;if(typeof v!=='string'||!v.trim()||v.length>12000)throw Error(name+'需为非空文字');return v;}
function tokens(v){if(v==null)return [];if(!Array.isArray(v)||v.length>20)throw Error('片段需为文字数组');return v.map(t=>text(t,'片段'));}
function normalize(v){
  if(!v||typeof v!=='object'||Array.isArray(v))throw Error('输入需为JSON对象');
  if(!v.focus||!Array.isArray(v.focus.lines)||!v.focus.lines.length||v.focus.lines.length>3)throw Error('首要任务需要1–3行');
  if(!Array.isArray(v.sections)||!v.sections.length||v.sections.length>6)throw Error('需要1–6章节');
  return {title:text(v.title,'标题'),meta:text(v.meta,'状态','内部经营汇报 · 合作沟通中'),focus:{label:text(v.focus.label,'任务标题','目前首要任务'),lines:v.focus.lines.map(t=>text(t,'任务')),keepTogether:tokens(v.focus.keepTogether)},sections:v.sections.map(s=>{
    if(!s||!Array.isArray(s.items)||!s.items.length||s.items.length>6)throw Error('每章需1–6条');
    return {title:text(s.title,'章名'),status:text(s.status,'章节状态'),decision:s.decision===true,items:s.items.map(i=>{if(!i||typeof i!=='object')throw Error('条目无效');return {label:text(i.label,'条目名称'),text:text(i.text,'正文'),keepTogether:tokens(i.keepTogether),emphasis:tokens(i.emphasis)};}),shared:s.shared==null?'':text(s.shared,'共同要求')};
  }),note:v.note==null?'':text(v.note,'备注')};
}
function inline(value,keep=[],emphasis=[]){
  const parts=[...new Set([...keep,...emphasis])].sort((a,b)=>b.length-a.length);let out='',i=0;
  while(i<value.length){const match=parts.find(p=>value.startsWith(p,i));if(match){out+='<span class="'+(emphasis.includes(match)?'amount':'unit')+'">'+esc(match)+'</span>';i+=match.length;}else{out+=esc(value[i]);i++;}}
  return out;
}
function render(input){
  const d=normalize(input),nums=['一','二','三','四','五','六'],css=fs.readFileSync(path.resolve(__dirname,'../assets/approved-style.css'),'utf8');
  const head='<header><div class="meta">'+esc(d.meta)+'</div><h1>'+esc(d.title)+'</h1><p class="focus"><b>'+esc(d.focus.label.replace(/[:：]$/,''))+'：</b><br>'+d.focus.lines.map(l=>inline(l,d.focus.keepTogether)).join('<br>')+'</p></header>';
  const sections=d.sections.map((s,n)=>'<section'+(s.decision?' class="decision"':'')+'><h2><span>'+nums[n]+'、'+esc(s.title)+'</span><span class="status">'+esc(s.status)+'</span></h2><ol>'+s.items.map((i,j)=>'<li><span class="num">（'+(j+1)+'）</span><div class="copy"><span class="label">'+esc(i.label.replace(/[:：]$/,''))+'：</span>'+inline(i.text,i.keepTogether,i.emphasis)+'</div></li>').join('')+'</ol>'+(s.shared?'<p class="shared">'+esc(s.shared)+'</p>':'')+'</section>').join('');
  return {data:d,html:'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(d.title)+'</title><style>'+css+'</style></head><body><article class="report" id="report">'+head+sections+(d.note?'<p class="note">'+esc(d.note)+'</p>':'')+'</article><div class="tools"><button onclick="window.print()">打印 / 保存 PDF</button></div></body></html>'};
}
function generate(input,output){
  const result=render(JSON.parse(fs.readFileSync(input,'utf8').replace(/^\uFEFF/,''))),dir=path.resolve(output),html=path.join(dir,'report.html'),json=path.join(dir,'report.json');
  if(fs.existsSync(html)||fs.existsSync(json))throw Error('输出已存在，请使用新目录');
  fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(json,JSON.stringify(result.data,null,2)+'\n',{flag:'wx'});fs.writeFileSync(html,result.html,{flag:'wx'});
  return {html,json,sha256:crypto.createHash('sha256').update(result.html).digest('hex')};
}
if(require.main===module){try{const [input,out]=process.argv.slice(2);if(!input||!out)throw Error('用法：node render.cjs 输入.json 输出目录');console.log(JSON.stringify(generate(input,out),null,2));}catch(e){console.error('生成失败：'+e.message);process.exitCode=1;}}
module.exports={normalize,render,generate};
