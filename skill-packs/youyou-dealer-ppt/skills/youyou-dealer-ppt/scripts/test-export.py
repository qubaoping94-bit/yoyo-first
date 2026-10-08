"""Optional browser smoke: image asset, three-format parity, and editable image object."""
import copy
import importlib.util
import json
import os
import tempfile
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

root = Path(__file__).resolve().parents[1]


def load(name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, Path(__file__).with_name(name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = load("build-deck.py", "build_deck")
export = load("export-deck.py", "export_deck")
audit = load("audit-output.py", "audit_output")
data = json.loads((root / "assets" / "deck-example.json").read_text(encoding="utf-8"))
data["assets"]["synthetic-test"] = {"path": "synthetic-test.png", "purpose": "synthetic test image", "rights": "approved"}
data["slides"][7]["image"] = "synthetic-test"

with tempfile.TemporaryDirectory() as temp:
    folder = Path(temp)
    Image.new("RGB", (800, 500), (218, 223, 216)).save(folder / "synthetic-test.png")
    source = folder / "deck.json"
    source.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    out = folder / "out"
    build.build(source, out)
    browser = Path(os.environ["YOUYOU_BROWSER_PATH"]) if os.environ.get("YOUYOU_BROWSER_PATH") else None
    export.export(out / "index.html", out, editable=True, browser_path=browser)
    result = audit.audit(out)
    assert result["parity_pass"], result["errors"]
    with ZipFile(out / "presentation-editable.pptx") as pptx:
        assert any(x.startswith("ppt/media/") for x in pptx.namelist()), "editable PPTX dropped image object"
print("export smoke passed")
