"""Build a self-contained Youyou HTML deck and manifest from one reviewed JSON source."""
import argparse
import base64
import hashlib
import html
import json
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = {"cover", "section", "cards", "comparison", "process", "evidence", "image", "summary", "table"}


def esc(value):
    return html.escape(str(value or ""), quote=True)


def image_html(image_id, assets, source_dir, used, *, fallback=""):
    if not image_id:
        return f'<div class="blankvisual">{esc(fallback)}</div>'
    item = assets[image_id]
    path = (source_dir / item["path"]).resolve()
    if not path.is_relative_to(source_dir.resolve()) or not path.is_file():
        raise ValueError(f"Missing or out-of-tree image: {image_id}")
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    if digest in used and item.get("reuse_reason", "") == "":
        raise ValueError(f"Image reused without reuse_reason: {image_id}")
    used.add(digest)
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError(f"Unsupported image type: {path.name}")
    payload = base64.b64encode(content).decode("ascii")
    return f'<img class="visual" src="data:{mime};base64,{payload}" alt="{esc(item.get("purpose", ""))}">'


def render_slide(slide, index, total, assets, source_dir, used):
    layout = slide["layout"]
    kicker = f'<div class="kicker">{esc(slide.get("kicker", ""))}</div>'
    title = f'<h1>{esc(slide.get("title", ""))}</h1>'
    subtitle = f'<p>{esc(slide.get("subtitle", ""))}</p>' if slide.get("subtitle") else ""
    conclusion = f'<div class="conclusion">{esc(slide["conclusion"])}</div>' if slide.get("conclusion") else ""
    items = slide.get("items", [])
    if layout == "cover":
        if slide.get("title_accent"):
            title = f'<h1><span>{esc(slide["title"])}</span><em>{esc(slide["title_accent"])}</em></h1>'
        if slide.get("cover_quote"):
            tags = "".join(f'<b>{esc(x)}</b>' for x in slide.get("cover_tags", []))
            visual = f'<div class="cover-statement"><div>{esc(slide["cover_quote"])}</div><nav>{tags}</nav></div>'
        else:
            visual = image_html(slide.get("image"), assets, source_dir, used, fallback="优优 · 材料与空间")
        main = f'<main class="covermain{" sample-cover" if slide.get("cover_quote") else ""}"><div>{kicker}{title}{subtitle}</div>{visual}{conclusion}</main>'
    elif layout == "section":
        main = f'<main class="sectionmain">{kicker}{title}{subtitle}{conclusion}</main>'
    elif layout == "image":
        visual = image_html(slide.get("image"), assets, source_dir, used, fallback="此处放本页专属配图")
        cards = "".join(f'<div class="card">{esc(x)}</div>' for x in items)
        noimage = " noimage" if not slide.get("image") else ""
        main = f'<main class="imagemain{noimage}"><div>{kicker}{title}{subtitle}<div class="bodygrid">{cards}</div></div>{visual}</main>'
    elif layout == "table":
        cells = "".join(f'<div class="tablecell"><strong>{i:02d}</strong><span>{esc(x)}</span></div>' for i, x in enumerate(items, 1))
        main = f'<main class="tablemain" style="--rows:{(len(items)+1)//2}">{kicker}{title}{subtitle}<div class="tablegrid">{cells}</div>{conclusion}</main>'
    else:
        count = len(items)
        cls = "cards-8" if count > 6 else "cards-6" if count > 4 else f"cards-{min(max(count, 2), 4)}"
        cols = count if layout == "process" else min(count, 4)
        cards = "".join(f'<div class="card"><span class="num">{i:02d}</span><span>{esc(x)}</span></div>' for i, x in enumerate(items, 1))
        density = " dense" if max(map(len, items), default=0) > 65 else ""
        main = f'<main class="{layout}{density}" style="--cols:{cols}">{kicker}{title}{subtitle}<div class="bodygrid {cls}">{cards}</div>{conclusion}</main>'
    return (f'<section class="slide" data-slide-id="{esc(slide["id"])}" data-layout="{layout}">'
            f'<div class="head"><span>YOUYOU INORGANIC BOARD</span><span>{esc(slide.get("kicker", ""))}</span></div>'
            f'{main}<div class="foot"><span>优优无机板 · 本页内容需按项目核准</span><b>{index:02d} / {total:02d}</b></div>'
            f'<aside class="speaker-notes">{esc(slide.get("notes", ""))}</aside></section>')


def build(source, output, allow_hold=False):
    data = json.loads(source.read_text(encoding="utf-8"))
    slides, claims, assets = data.get("slides", []), data.get("claims", {}), data.get("assets", {})
    if not slides:
        raise ValueError("slides must not be empty")
    ids = [s.get("id") for s in slides]
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(x or "")) for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("slides require unique stable kebab-case IDs")
    hold = []
    used = set()
    for s in slides:
        if s.get("layout") not in LAYOUTS:
            raise ValueError(f"Unsupported layout in {s['id']}")
        if not s.get("title"):
            raise ValueError(f"Missing title in {s['id']}")
        n = len(s.get("items", []))
        if s["layout"] in {"cards", "comparison", "process", "evidence", "summary", "table"} and not 2 <= n <= 8:
            raise ValueError(f"{s['id']} needs 2–8 items")
        if s["layout"] == "comparison" and n != 2:
            raise ValueError(f"{s['id']} comparison needs exactly 2 sides")
        if s["layout"] == "evidence" and n != 3:
            raise ValueError(f"{s['id']} evidence needs claim, source and limitation")
        if s["layout"] == "process" and n > 6:
            raise ValueError(f"{s['id']} process supports at most 6 steps")
        if s["layout"] == "summary" and n > 4:
            raise ValueError(f"{s['id']} summary supports at most 4 actions")
        if s.get("image") and s["image"] not in assets:
            raise ValueError(f"Unknown image ID in {s['id']}")
        if s.get("image"):
            image_record = assets[s["image"]]
            if image_record.get("rights") != "approved" or not image_record.get("purpose"):
                hold.append(f"image {s['image']} in {s['id']} lacks rights/purpose approval")
        for cid in s.get("claim_ids", []):
            if cid not in claims:
                raise ValueError(f"Unknown claim ID {cid} in {s['id']}")
            c = claims[cid]
            if c.get("status") != "approved" or not all(c.get(k) for k in ("text", "source", "scope", "limitations")):
                hold.append(f"claim {cid} in {s['id']} lacks approval/evidence")
        slide_text = " ".join(str(s.get(k, "")) for k in ("title", "subtitle", "conclusion")) + " " + " ".join(map(str, s.get("items", [])))
        if re.search(r"八零|甲醛|A级不燃|全系标配|使用年限|释放周期|成本|利润|销量|价格|认证|检测报告", slide_text) and not s.get("claim_ids"):
            hold.append(f"potential claim in {s['id']} has no claim_ids")
    text = json.dumps(data, ensure_ascii=False)
    if re.search(r"七零|7\s*零|七项零", text):
        hold.append("old seven-zero wording")
    version = data.get("content_version", {})
    visible = " ".join(" ".join(str(s.get(k, "")) for k in ("title", "subtitle", "conclusion")) + " " + " ".join(map(str, s.get("items", []))) for s in slides)
    if "平权" in visible:
        taxonomy = version.get("five_rights")
        if (not isinstance(taxonomy, list) or len(taxonomy) != 5 or len(set(taxonomy)) != 5
                or any(not isinstance(x, str) or not x.endswith("平权") for x in taxonomy)
                or version.get("approval_status") != "approved" or not version.get("approval_source")):
            hold.append("five-rights taxonomy requires five approved names and a traceable source")
        else:
            mentioned = set(re.findall(r"[\u4e00-\u9fff]{2,8}平权", visible))
            known = set(taxonomy)
            if mentioned - known - {"五大平权"}:
                hold.append("five-rights wording conflicts with approved taxonomy: " + ",".join(sorted(mentioned - known - {"五大平权"})))
    if hold and not allow_hold:
        raise ValueError("CONTENT_HOLD: " + "; ".join(sorted(set(hold))))
    pages = [render_slide(s, i, len(slides), assets, source.parent, used) for i, s in enumerate(slides, 1)]
    css = (ROOT / "assets" / "deck.css").read_text(encoding="utf-8")
    css += ".covermain .blankvisual{border:0;border-top:4px solid var(--red);border-bottom:4px solid var(--red);background:transparent}.imagemain.noimage{grid-template-columns:1fr}.imagemain.noimage .blankvisual{display:none}.imagemain.noimage .bodygrid{grid-template-columns:repeat(2,1fr)}.imagemain.noimage .card{min-height:210px;font-size:36px}.cards-6{grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)}.process .bodygrid{grid-template-rows:1fr}.tablegrid{display:grid;grid-template-columns:repeat(2,1fr);grid-template-rows:repeat(var(--rows),1fr);gap:16px;flex:1;min-height:0;margin-top:24px}.tablecell{display:flex;align-items:center;background:var(--card);border-left:5px solid var(--red);padding:18px 26px;font-size:34px;font-weight:700}.tablecell strong{font-size:44px;color:var(--red);margin-right:25px}"
    css += ".summary .bodygrid{grid-template-columns:repeat(var(--cols),1fr);grid-template-rows:1fr}"
    css += "#notes-panel{position:fixed;right:20px;top:20px;bottom:20px;width:min(420px,40vw);padding:25px;background:#171815;color:#fff;z-index:5;overflow:auto;font-size:20px;line-height:1.5;box-shadow:0 12px 40px #0007}#notes-panel[hidden]{display:none!important}#notes-panel h2{font-size:25px;margin:0 0 18px;color:#fff}@media print{#notes-panel{display:none!important}}"
    js = """const slides=[...document.querySelectorAll('.slide')],panel=document.querySelector('#notes-panel');let at=0,last=0;function fit(){const s=Math.min(innerWidth/1920,innerHeight/1080);document.querySelector('#stage').style.transform=`scale(${s})`;document.querySelector('#stage').style.left=`${(innerWidth-1920*s)/2}px`;document.querySelector('#stage').style.top=`${(innerHeight-1080*s)/2}px`;}function show(n){at=Math.max(0,Math.min(slides.length-1,n));slides.forEach((x,i)=>x.classList.toggle('active',i===at));panel.querySelector('p').textContent=slides[at].querySelector('.speaker-notes').textContent;}addEventListener('resize',fit);addEventListener('keydown',e=>{if(e.key==='p'||e.key==='P'){panel.hidden=!panel.hidden;return}if(e.key==='Escape'&&!panel.hidden){panel.hidden=true;return}if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(at+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(at-1)}});addEventListener('wheel',e=>{if(e.target.closest('#notes-panel')||Math.abs(e.deltaY)<18||Date.now()-last<420)return;last=Date.now();show(at+(e.deltaY>0?1:-1))},{passive:true});fit();show(0);"""
    document = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(data.get("title", "优优演讲"))}</title><style>{css}</style></head><body><div id="viewport"><div id="stage">{"".join(pages)}</div></div><aside id="notes-panel" hidden><h2>演讲者备注 · 按 P 关闭</h2><p></p></aside><script>{js}</script></body></html>'
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(document, encoding="utf-8")
    manifest = {"title": data.get("title", ""), "status": "CONTENT_HOLD" if hold else "STRUCTURE_PASS_CONTENT_NOT_VERIFIED", "holds": sorted(set(hold)), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "content_version": version, "claims": claims, "assets": assets, "slides": [{"id": s["id"], "title": s["title"], "title_accent": s.get("title_accent", ""), "layout": s["layout"], "notes": s.get("notes", ""), "items": s.get("items", []), "subtitle": s.get("subtitle", ""), "conclusion": s.get("conclusion", ""), "claim_ids": s.get("claim_ids", []), "image": s.get("image")} for s in slides]}
    (output / "deck-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {len(slides)} slides: {output / 'index.html'}; {manifest['status']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--allow-hold", action="store_true")
    a = p.parse_args()
    build(a.source, a.output, a.allow_hold)
