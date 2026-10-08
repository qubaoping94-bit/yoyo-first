"""Dependency-free regression checks for the single-source builder."""
import copy
import base64
import importlib.util
import json
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_deck", Path(__file__).with_name("build-deck.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
baseline = json.loads((root / "assets" / "deck-example.json").read_text(encoding="utf-8"))


def run_case(data, should_fail, reason, with_image=False):
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp)
        if with_image:
            (folder / "test.png").write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lXcAAAAASUVORK5CYII="))
        source = folder / "deck.json"
        source.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        try:
            module.build(source, folder / "out")
        except ValueError:
            if not should_fail:
                raise
        else:
            if should_fail:
                raise AssertionError(f"Expected rejection: {reason}")


run_case(baseline, False, "valid example")
case = copy.deepcopy(baseline); case["slides"][1]["id"] = "cover"; run_case(case, True, "duplicate IDs")
case = copy.deepcopy(baseline); case["slides"][0]["title"] = "七零"; run_case(case, True, "old wording")
case = copy.deepcopy(baseline); case["slides"][0]["claim_ids"] = ["test"]
case["claims"]["test"] = {"text": "测试", "status": "hold", "source": "", "scope": "", "limitations": ""}
run_case(case, True, "unapproved claim")
case = copy.deepcopy(baseline); case["slides"][0]["image"] = "missing"; run_case(case, True, "missing image")
case = copy.deepcopy(baseline); case["slides"][0]["title"] = "五大平权"; run_case(case, True, "unresolved taxonomy")
case = copy.deepcopy(baseline); case["assets"]["demo"] = {"path": "test.png", "purpose": "tiny regression image", "rights": "approved"}; case["slides"][0]["image"] = "demo"
run_case(case, False, "approved image", with_image=True)
case["assets"]["demo"]["rights"] = "hold"; run_case(case, True, "image rights hold", with_image=True)
case["assets"]["demo"]["rights"] = "approved"
case["slides"][7]["image"] = "demo"; run_case(case, True, "image reused without reason", with_image=True)
case["assets"]["demo"]["reuse_reason"] = "same deck identity"; run_case(case, False, "explicit image reuse", with_image=True)
print("build-deck regression checks passed")
