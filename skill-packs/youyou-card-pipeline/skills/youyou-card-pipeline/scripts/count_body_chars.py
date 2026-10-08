"""Count body characters between exact note headings, excluding whitespace."""
from pathlib import Path
import argparse
import re

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('note',type=Path)
    parser.add_argument('--limit',type=int,default=1000)
    args=parser.parse_args()
    if not 1<=args.limit<=1000:
        parser.error('--limit must be between 1 and 1000; do not raise the delivery cap')
    contents=args.note.read_text(encoding='utf-8-sig')
    matches=list(re.finditer(r'^### 正文内容\s*\r?\n(.*?)^### 推荐标签\s*$',contents,re.S|re.M))
    if len(matches)!=1:
        print('ERROR: require exactly one body block between ### 正文内容 and ### 推荐标签')
        return 2
    length=len(re.sub(r'\s','',matches[0].group(1)))
    print(f'{"OK" if length<=args.limit else "OVER"} ({length} chars, limit {args.limit})')
    return 0 if length<=args.limit else 1

if __name__=='__main__':
    raise SystemExit(main())
