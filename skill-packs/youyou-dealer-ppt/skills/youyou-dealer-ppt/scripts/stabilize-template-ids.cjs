const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..','assets');
for(const name of ['approved-black-red-template.html','approved-black-red-density.css']){
  const file=path.join(root,name);let s=fs.readFileSync(file,'utf8');
  for(let n=9;n>=2;n--)s=s.replaceAll(`.slide:nth-of-type(${n})`,`.slide[data-slide-id="s${String(n).padStart(2,'0')}"]`);
  fs.writeFileSync(file,s,'utf8');
}
console.log('template page-specific selectors stabilized');
