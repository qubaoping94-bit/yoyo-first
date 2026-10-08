"""Render agent-authored note JSON; this script does not generate prose or invent facts."""
from pathlib import Path
import argparse,json,re
from note_validation import inspect_note,publication_text

def line(value):
    if not isinstance(value,str) or not value.strip() or '\n' in value or '\r' in value:
        raise ValueError('Each field must be a nonempty single-line string')
    return value.strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True,type=Path)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    data=json.loads(args.input.read_text(encoding='utf-8-sig'))
    text='# 配套文案 · '+line(data['topic'])+'\n\n> 面向'+line(data['audience'])+'。口吻：'+line(data['voice'])+'。正文严格≤1000字符。\n\n'
    text+='### 推荐标题\n\n'+'\n'.join(f'{i}. {line(t)}' for i,t in enumerate(data['titles'],1))+'\n\n'
    text+='### 正文内容\n\n'+'\n\n'.join(line(p) for p in data['paragraphs'])+'\n\n'
    text+='### 推荐标签\n\n'+' '.join(line(t) for t in data['tags'])+'\n\n'
    text+='### 爆款来源\n\n'+line(data['source'])+'\n\n### 合规口径\n\n'+line(data['boundary'])+'\n'
    report=inspect_note(text)
    if not report['ok']:
        print(json.dumps(report,ensure_ascii=False));return 1
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'xhs-note.md').write_text(text,encoding='utf-8')
    (args.output/'小红书发布文案.txt').write_text(publication_text(text),encoding='utf-8')
    (args.output/'note.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (args.output/'note-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));return 0

if __name__=='__main__':raise SystemExit(main())
