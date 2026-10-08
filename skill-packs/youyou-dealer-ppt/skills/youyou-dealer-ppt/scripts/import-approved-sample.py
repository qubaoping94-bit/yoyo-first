"""Import all 21 pages of a local approved sample into a CONTENT_HOLD regression deck.

This is a QA bridge, not a business-copy approval or a replacement for the source.
Requires beautifulsoup4. The source files stay read-only and are never packaged.
"""
import argparse
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


def clean(value):
    return re.sub(r"\s+", " ", value).strip()


def item_text(node):
    parts = []
    for child in node.find_all("b", recursive=False):
        value = clean(child.get_text(" ", strip=True))
        if value and not value.isdecimal():
            parts.append(value)
    for child in node.find_all(["h3", "p"], recursive=True):
        value = clean(child.get_text(" ", strip=True))
        if value:
            parts.append(value)
    if not parts:
        parts = [clean(node.get_text(" ", strip=True))]
    return "｜".join(parts)


def import_sample(html_path, ledger_path, output):
    source = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    notes = {slide["id"]: slide["notes"] for slide in ledger["slides"]}
    slides = []
    for section in source.select("section.slide"):
        sid = section["data-slide-id"]
        main = section.select_one("main")
        heading = main.select_one("h1, h2")
        if not heading or sid not in notes:
            raise ValueError(f"Missing title or ledger notes: {sid}")
        title = clean(heading.get_text("", strip=True))
        kicker = clean(section.select_one("header span").get_text(" ", strip=True))
        slide = {"id": sid, "source_slide_id": sid, "kicker": kicker, "title": title, "notes": notes[sid], "claim_ids": ["historic-sample"]}
        if sid == "cover":
            slide.update({"layout": "cover", "kicker": clean(main.select_one(".kicker").get_text(" ", strip=True)), "title": "优优无机板", "title_accent": "功能与经营演讲手册", "subtitle": clean(main.select_one(".cover-left p").get_text(" ", strip=True)), "cover_quote": main.select_one(".cover-quote").get_text("\n", strip=True), "cover_tags": [clean(x.get_text(" ", strip=True)) for x in main.select(".cover-index b")]})
        else:
            articles = main.select("article")
            if articles:
                nodes = articles
            elif main.select_one(".table4"):
                nodes = main.select(".table4 > div")
            elif main.select_one(".compare"):
                nodes = main.select(".compare > div")
            else:
                raise ValueError(f"Cannot infer content groups: {sid}")
            items = [item_text(x) for x in nodes]
            if not 2 <= len(items) <= 8 or any(not x for x in items):
                raise ValueError(f"Unsupported group count or empty group: {sid}")
            classes = set()
            for node in main.find_all("div", recursive=True):
                classes.update(node.get("class", []))
            layout = "process" if "flow" in classes else "table" if classes & {"grid8", "grid7", "table4"} else "comparison" if "compare" in classes else "summary" if sid == "closing" else "cards"
            slide.update({"layout": layout, "items": items})
            callout = main.select_one(".callout, .reason-callout, .closing-quote")
            if callout:
                slide["conclusion"] = clean(callout.get_text(" ", strip=True))
            extras = []
            for p in main.select("p"):
                if p.find_parent("article") or (callout and p.find_parent(lambda x: x is callout)):
                    continue
                value = clean(p.get_text(" ", strip=True))
                if value and value not in " ".join(items):
                    extras.append(value)
            if extras:
                slide["subtitle"] = " ".join(dict.fromkeys(extras))
            represented = "".join(str(slide.get(k, "")) for k in ("title", "subtitle", "conclusion")) + "".join(items)
            unrepresented = [clean(value) for value in main.stripped_strings if clean(value) and not clean(value).isdecimal() and clean(value) not in represented]
            if unrepresented:
                slide["subtitle"] = " ".join([slide.get("subtitle", ""), *dict.fromkeys(unrepresented)]).strip()
        slides.append(slide)
    if len(slides) != 21 or [s["id"] for s in slides] != [s["id"] for s in ledger["slides"]]:
        raise ValueError("Expected exact 21-page source order")
    deck = {"title": "正式21页样例回归候选（仅供视觉对照）", "imported_from_sample": True, "source_reference": "local approved 2026-09-27 sample", "content_version": {"five_rights": "unresolved", "approval_source": ""}, "claims": {"historic-sample": {"text": "历史21页样例文案，仅用于样式回归", "source": str(html_path), "status": "hold", "scope": "本地候选视觉测试", "limitations": "不证明当前商业主张、认证或检测报告仍有效"}}, "assets": {}, "slides": slides}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(deck, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Imported {len(slides)} slides to {output}; CONTENT_HOLD")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source_html", type=Path)
    p.add_argument("source_ledger", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    import_sample(a.source_html, a.source_ledger, a.output)
