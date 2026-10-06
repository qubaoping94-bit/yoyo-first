"""Static preflight for Youyou HTML/PPTX/PDF decks; visual review is still required."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZipFile


def check(html_path, pptx_path=None, pdf_path=None, claim_ledger=None):
    html = html_path.read_text(encoding="utf-8")
    findings = []

    def add(code, severity, evidence):
        findings.append({"code": code, "severity": severity, "evidence": evidence})

    stage = re.search(r"(?:\.slide|#stage)\s*\{[^}]*?width:\s*(\d+)px\s*;\s*height:\s*(\d+)px", html, re.S)
    if not stage:
        add("STAGE_UNKNOWN", "block", "Cannot find fixed .slide width/height; inspect implementation manually")
        width = None
    else:
        width, height = map(int, stage.groups())
        if abs(width / height - 16 / 9) > 0.005:
            add("STAGE_RATIO", "block", f"{width}x{height} is not 16:9")
    if not re.search(r"\.slide\s*\{[^}]*border-left:\s*\d+px\s+solid\s+(?:var\(--red\)|#e63b2e)", html, re.I | re.S):
        add("RED_SPINE_MISSING", "block", "Current 21-slide sample has a left red spine, not a top red stripe")
    if not re.search(r"background-size:\s*(?:96px\s+96px|64px\s+64px)", html, re.I):
        add("GRID_UNKNOWN", "review", "Expected subtle regular grid; inspect screenshot")

    ids = re.findall(r"data-slide-id=[\"']([^\"']+)[\"']", html)
    if not ids:
        add("SLIDE_IDS_MISSING", "block", "No stable data-slide-id values")
    if len(ids) != len(set(ids)):
        add("SLIDE_IDS_DUPLICATE", "block", "data-slide-id values repeat")
    if re.search(r"七零|7\s*零|七项零", html):
        add("OUTDATED_SEVEN_ZERO", "block", "Contains old seven-zero wording; verify source/context")

    body_px = [float(x) for x in re.findall(r"<p\b[^>]*style=[\"'][^\"']*font-size:\s*([\d.]+)px", html, re.I)]
    if width and body_px:
        minimum = min(body_px) * 1920 / width
        if minimum < 27:
            add("BODY_FONT_TOO_SMALL", "block", f"Minimum explicit paragraph size {minimum:.1f}px in 1920 design units (floor 27px)")

    external = re.findall(r"<(?:script|link)[^>]+(?:src|href)=[\"'](https?://[^\"']+)", html, re.I)
    if external:
        add("EXTERNAL_RUNTIME_ASSET", "block", external)
    if "prefers-reduced-motion" not in html:
        add("REDUCED_MOTION_MISSING", "block", "HTML does not declare reduced-motion handling")
    if "wheel" not in html or "keydown" not in html:
        add("NAVIGATION_UNKNOWN", "block", "Cannot find wheel and keyboard handlers")

    rights_a = ["安全平权", "功能平权", "品质平权", "空间平权", "环保平权"]
    rights_b = ["技术平权", "功能平权", "豪华平权", "生活平权", "环保平权"]
    deck_text = re.sub(r"<[^>]+>", " ", html)
    if all(x in deck_text for x in rights_b) and not all(x in deck_text for x in rights_a):
        add("FIVE_RIGHTS_VERSION_CONFLICT", "block", "Uses technology/function/luxury/life/environment taxonomy, different from the 21-slide sample; requires approved source")

    risky = [x for x in ("全系标配", "不必为", "3–15 年", "3-15 年", "甲醛含量为 0", "甲醛含量0", "A级不燃") if x in deck_text]
    if risky and not claim_ledger:
        add("CLAIM_LEDGER_REQUIRED", "block", f"Potentially report/model/policy-dependent claims without ledger: {', '.join(risky)}")
    if claim_ledger and not claim_ledger.is_file():
        add("CLAIM_LEDGER_MISSING", "block", str(claim_ledger))

    counts = {"html": len(re.findall(r"<section\b[^>]*class=[\"'][^\"']*\bslide\b|<div\b[^>]*class=[\"'][^\"']*\bslide\b", html, re.I))}
    if pptx_path:
        with ZipFile(pptx_path) as z:
            names = z.namelist()
            counts["pptx"] = sum(bool(re.fullmatch(r"ppt/slides/slide\d+\.xml", n)) for n in names)
            counts["pptx_notes"] = sum(bool(re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)) for n in names)
        if counts["pptx"] != counts["html"]:
            add("PPTX_PAGE_MISMATCH", "block", counts)
        if counts["pptx_notes"] != counts["pptx"]:
            add("PPTX_NOTES_MISMATCH", "block", counts)
    if pdf_path:
        try:
            info = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, timeout=30)
            match = re.search(rb"^Pages:\s*(\d+)", info.stdout, re.M)
            if not match:
                raise ValueError("pdfinfo did not return page count")
            counts["pdf"] = int(match.group(1))
            if counts["pdf"] != counts["html"]:
                add("PDF_PAGE_MISMATCH", "block", counts)
        except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
            add("PDF_COUNT_UNVERIFIED", "review", str(exc))
    return {"counts": counts, "findings": findings, "static_preflight_pass": not any(x["severity"] == "block" for x in findings), "visual_review_required": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--pptx", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--claim-ledger", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = check(args.html, args.pptx, args.pdf, args.claim_ledger)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    raise SystemExit(0 if result["static_preflight_pass"] else 1)


if __name__ == "__main__":
    main()
