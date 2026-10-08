"""Check single-source HTML/PDF/PPTX page and image parity after export."""
import argparse
import hashlib
import io
import json
import re
from pathlib import Path
from zipfile import ZipFile


def audit(folder):
    import fitz
    from PIL import Image, ImageChops, ImageStat

    manifest = json.loads((folder / "deck-manifest.json").read_text(encoding="utf-8"))
    n = len(manifest["slides"])
    frames = sorted((folder / "frames").glob("slide-*.png"))
    errors = []
    if len(frames) != n:
        errors.append(f"PNG count {len(frames)} != manifest {n}")
    pdf = fitz.open(folder / "presentation.pdf")
    if len(pdf) != n:
        errors.append(f"PDF count {len(pdf)} != manifest {n}")
    with ZipFile(folder / "presentation.pptx") as z:
        names = z.namelist()
        slides = [x for x in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", x)]
        notes = [x for x in names if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", x)]
        media = [hashlib.sha256(z.read(x)).hexdigest() for x in names if x.startswith("ppt/media/") and x.lower().endswith(".png")]
    if len(slides) != n or len(notes) != n:
        errors.append(f"PPTX slides/notes {len(slides)}/{len(notes)} != {n}")
    frame_hashes = [hashlib.sha256(x.read_bytes()).hexdigest() for x in frames]
    if sorted(media) != sorted(frame_hashes):
        errors.append("PPTX media not byte-identical to page PNGs")
    page_results = []
    for i, frame in enumerate(frames[:min(len(pdf), n)]):
        reference = Image.open(frame).convert("RGB")
        pix = pdf[i].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        rendered = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).resize(reference.size)
        diff = ImageChops.difference(reference, rendered)
        mae = sum(ImageStat.Stat(diff).mean) / 3
        page_results.append({"slide": i + 1, "pdf_mae": round(mae, 2)})
        if mae > 13:
            errors.append(f"PDF page {i+1} image delta {mae:.2f} > 13")
        reference.close(); rendered.close()
    result = {"pages": n, "page_results": page_results, "errors": errors, "parity_pass": not errors, "visual_review_required": True, "content_status": manifest["status"]}
    (folder / "parity-report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder", type=Path)
    a = p.parse_args()
    result = audit(a.folder)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["parity_pass"] else 1)
