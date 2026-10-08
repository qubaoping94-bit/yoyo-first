"""Prevent an image-only folder from passing a paired delivery gate."""
from pathlib import Path
import argparse,json,struct
from note_validation import inspect_note,publication_text

def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--mode',choices=['paired','copy-only'],default='paired');args=ap.parse_args()
    root=args.directory;issues=[];note_report=None
    note=root/'xhs-note.md'
    if not note.is_file():issues.append('Missing xhs-note.md: image-only delivery is incomplete')
    else:
        try:
            text=note.read_text(encoding='utf-8-sig');note_report=inspect_note(text)
            issues.extend(note_report['issues'])
            post=root/'小红书发布文案.txt'
            if not post.is_file():issues.append('Missing publication copy')
            elif note_report['ok'] and post.read_text(encoding='utf-8-sig')!=publication_text(text):issues.append('Publication copy does not match xhs-note.md')
        except (OSError,UnicodeError) as error:issues.append(str(error))
    if args.mode=='paired':
        for name in ('deck.json','index.html'):
            if not (root/name).is_file():issues.append('Missing '+name)
        for i in range(1,9):
            p=root/'output'/f'xhs-{i:02}.png'
            if not p.is_file():issues.append('Missing '+p.name);continue
            with p.open('rb') as f:header=f.read(24)
            if len(header)!=24 or header[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',header[16:24])!=(1080,1440):issues.append('Invalid PNG dimensions: '+p.name)
        reports=[]
        for p in (root/'output').glob('*.json'):
            try:r=json.loads(p.read_text(encoding='utf-8-sig'))
            except (ValueError,OSError):continue
            if r.get('ok') is True and len(r.get('metrics',[]))==8 and len(r.get('files',[]))==8:reports.append(p.name)
        if not reports:issues.append('Missing successful eight-card layout report in output/')
    report={'ok':not issues,'mode':args.mode,'issues':issues,'note':note_report}
    if root.is_dir():(root/'delivery-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));return 0 if report['ok'] else 1

if __name__=='__main__':raise SystemExit(main())
