from pathlib import Path
import argparse,json
from note_validation import inspect_note

def main():
    ap=argparse.ArgumentParser();ap.add_argument('note',type=Path);args=ap.parse_args()
    try:report=inspect_note(args.note.read_text(encoding='utf-8-sig'))
    except (OSError,UnicodeError) as error:report={'ok':False,'issues':[str(error)]}
    print(json.dumps(report,ensure_ascii=False))
    return 0 if report['ok'] else 1

if __name__=='__main__':raise SystemExit(main())
