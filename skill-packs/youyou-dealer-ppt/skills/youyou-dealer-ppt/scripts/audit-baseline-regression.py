"""Check a four-page candidate's copy against the read-only 21-page sample."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path


def plain(fragment):
    return re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", "", fragment)))


def audit(candidate, source_html, source_ledger, output):
    deck = json.loads(candidate.read_text(encoding="utf-8"))
    ledger = json.loads(source_ledger.read_text(encoding="utf-8"))
    notes = {s["id"]: s["notes"] for s in ledger["slides"]}
    original = source_html.read_text(encoding="utf-8")
    findings = []
    rows = []
    for slide in deck["slides"]:
        sid = slide.get("source_slide_id")
        match = re.search(r'<section class="slide(?: active)?" data-slide-id="' + re.escape(sid or "") + r'".*?</section>', original, re.S)
        if not match:
            findings.append(f"{sid}: not found in approved sample")
            continue
        source_text = plain(match.group(0))
        for field in ("title", "title_accent", "subtitle", "conclusion", "cover_quote"):
            value = plain(slide.get(field, ""))
            if value and value not in source_text and not (deck.get("imported_from_sample") and field == "subtitle"):
                findings.append(f"{sid}: {field} changed from source")
        for item in slide.get("items", []):
            for part in item.split("｜"):
                if plain(part) not in source_text:
                    findings.append(f"{sid}: item part changed: {part}")
        for tag in slide.get("cover_tags", []):
            if plain(tag) not in source_text:
                findings.append(f"{sid}: cover tag changed: {tag}")
        main_match = re.search(r"<main(?:\s[^>]*)?>(.*?)</main>", match.group(0), re.S)
        candidate_text = plain("".join(str(slide.get(k, "")) for k in ("kicker", "title", "title_accent", "subtitle", "conclusion", "cover_quote")) + "".join(map(str, slide.get("items", []))) + "".join(map(str, slide.get("cover_tags", []))))
        if main_match:
            for fragment in re.findall(r">([^<>]+)<", main_match.group(1)):
                value = plain(fragment)
                if value and not value.isdecimal() and value not in candidate_text:
                    findings.append(f"{sid}: source text omitted: {value[:60]}")
        if slide.get("notes", "") != notes.get(sid, None):
            findings.append(f"{sid}: speaker notes changed")
        rows.append({"id": sid, "title": slide["title"], "matched_parts": 3 + len(slide.get("items", []))})
    report = {"status": "PASS" if not findings else "FAIL", "source_html_sha256": hashlib.sha256(source_html.read_bytes()).hexdigest(), "source_ledger_sha256": hashlib.sha256(source_ledger.read_bytes()).hexdigest(), "candidate_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(), "slides": rows, "findings": findings, "scope": "Four representative pages; does not approve claims or visuals"}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if findings:
        raise ValueError("Baseline copy regression failed: " + "; ".join(findings))
    print(f"Baseline copy regression PASS: {len(rows)} representative slides")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("candidate", type=Path)
    p.add_argument("source_html", type=Path)
    p.add_argument("source_ledger", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    audit(a.candidate, a.source_html, a.source_ledger, a.output)
