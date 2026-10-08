"""Create a local 21-page side-by-side visual review of approved source and candidate."""
import argparse
import html
import json
from pathlib import Path


def build(source_images, candidate, output):
    manifest = json.loads((candidate / "deck-manifest.json").read_text(encoding="utf-8"))
    rows = []
    for index, slide in enumerate(manifest["slides"], 1):
        original = source_images / f"slide-{index:02d}.png"
        frames = list((candidate / "frames").glob(f"slide-{index:02d}-*.png"))
        if not original.is_file() or len(frames) != 1:
            raise ValueError(f"Missing original/candidate image for page {index}")
        rows.append(f'<section id="p{index:02d}"><h2>{index:02d} · {html.escape(slide["title"])}</h2><div class="pair"><a href="{original.as_uri()}"><img loading="lazy" src="{original.as_uri()}" alt="正式样例第{index}页"></a><a href="{frames[0].as_uri()}"><img loading="lazy" src="{frames[0].as_uri()}" alt="候选第{index}页"></a></div></section>')
    page = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>优优演讲 · 21页同视口对照</title><style>body{font-family:Microsoft YaHei,Arial,sans-serif;background:#f4f1e8;color:#171815;margin:0;padding:24px}header{position:sticky;top:0;background:#f4f1e8;border-bottom:3px solid #e63b2e;padding:12px 0;z-index:2}h1{font-size:32px;margin:0 0 6px}p{font-size:18px;margin:0}section{margin:28px 0 48px}h2{font-size:22px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.pair img{width:100%;border:1px solid #aaa;display:block}a:focus{outline:4px solid #e63b2e}@media(max-width:1000px){.pair{grid-template-columns:1fr}}</style><header><h1>正式样例 → 21页候选</h1><p>左右同为1920×1080；点击图片查看原尺寸。四页方向已确认，全稿仍待视觉审阅；内容状态 CONTENT_HOLD。</p></header>' + ''.join(rows) + '</html>'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(f"Review page: {output}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source_images", type=Path)
    p.add_argument("candidate", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    build(a.source_images, a.candidate, a.output)
