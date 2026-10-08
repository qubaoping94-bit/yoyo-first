"""Build an eight-card document from trusted structured content; no network."""
from pathlib import Path
import argparse
import json
import html
import shutil

def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Text fields must be nonempty strings')
    return html.escape(value, quote=True)

def lines(values):
    if not isinstance(values, list) or not 1 <= len(values) <= 2:
        raise ValueError('Titles require one or two explicit lines')
    return ''.join('<span class="title-line">'+text(v)+'</span>' for v in values)

def nodes(items, count, accent_last=False):
    if not isinstance(items, list) or len(items) != count:
        raise ValueError(f'Expected {count} nodes')
    return ''.join('<div class="node'+(' accent' if accent_last and i == count-1 else '')+'"><p class="node-sub">'+text(n['label'])+'</p><p class="node-title">'+text(n['title'])+'</p><p class="node-body">'+text(n['body'])+'</p></div>' for i,n in enumerate(items))

def card(c, i):
    kind=c['type']
    if kind=='cover':
        ns=nodes(c['nodes'],2,True)
        parts=ns.split('</div>',1)
        panel='<div class="panel sys-diagram fill">'+parts[0]+'</div><div class="arrow">→</div>'+parts[1]+'</div>'
    elif kind=='two':
        if len(c['modules'])!=2:
            raise ValueError('two requires two modules')
        panel='<div class="panel two-mod fill">'
        for j,n in enumerate(c['modules']):
            if not 1<=len(n['bullets'])<=4:
                raise ValueError('Each module requires one to four bullets')
            panel+='<div class="'+('card-ink' if j==0 else 'card-fill')+'"><p class="t-cat">'+text(n['label'])+'</p><h3 class="mod-title">'+text(n['title'])+'</h3><ul class="mod-bullets">'+''.join('<li>'+text(v)+'</li>' for v in n['bullets'])+'</ul></div>'
        panel+='</div>'
    elif kind in ('tri','quad'):
        panel='<div class="panel '+kind+'-grid fill">'+nodes(c['nodes'],3 if kind=='tri' else 4,kind=='quad')+'</div>'
    elif kind in ('ledger','closing'):
        if len(c['rows'])!=3:
            raise ValueError('Ledger cards require three rows')
        panel='<div class="stacked-ledger fill">'+''.join('<div class="ledger-row"><p class="ledger-num">'+f'{j+1:02}'+'</p><div class="ledger-text"><p class="ledger-lbl">'+text(n['title'])+'</p><p class="sub">'+text(n['body'])+'</p></div></div>' for j,n in enumerate(c['rows']))+'</div>'
        if kind=='closing':
            panel+='<div class="closing-block"><p class="t-cat">Takeaway · 核心结论</p><h2 class="h-xl">'+lines(c['closing'])+'</h2></div>'
    else:
        raise ValueError(f'Unsupported card type: {kind}')
    return '<section class="poster xhs '+kind+'" id="xhs-'+f'{i:02}'+'"><div class="content"><div class="chrome-min"><span>YOUYOU · SOCIAL CARDS</span><span>'+f'{i:02} / 08'+'</span></div><div class="heading"><p class="t-cat">'+text(c['eyebrow'])+'</p><h2 class="h-xl">'+lines(c['title'])+'</h2></div>'+panel+'<p class="lead">'+text(c['lead'])+'</p></div></section>'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True,type=Path)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    data=json.loads(args.input.read_text(encoding='utf-8-sig'))
    cards=data['cards']
    if len(cards)!=8:
        raise ValueError('Exactly eight cards are required')
    kinds=[c['type'] for c in cards]
    if kinds[0]!='cover' or kinds[6:]!=['ledger','closing'] or 'tri' not in kinds[1:6] or 'quad' not in kinds[1:6] or any(k not in ('two','tri','quad') for k in kinds[1:6]):
        raise ValueError('Expected cover, five two/tri/quad cards including tri and quad, ledger, closing')
    template=(Path(__file__).resolve().parent.parent/'assets/template.html').read_text(encoding='utf-8')
    document=template.replace('{{TITLE}}',text(data['title'])).replace('{{CARDS}}',''.join(card(c,i+1) for i,c in enumerate(cards)))
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'index.html').write_text(document,encoding='utf-8')
    destination=args.output/'deck.json'
    if destination.resolve()!=args.input.resolve():
        shutil.copy2(args.input,destination)
    print(f'BUILT 8 cards: {args.output / "index.html"}')

if __name__=='__main__':
    main()
