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
case["content_version"] = {"five_rights": ["安全平权", "功能平权", "品质平权", "空间平权", "环保平权"], "approval_status": "approved", "approval_source": "reviewed-record"}
run_case(case, False, "approved taxonomy")
case["slides"][0]["title"] = "技术平权"; run_case(case, True, "conflicting taxonomy")
case = copy.deepcopy(baseline); case["assets"]["demo"] = {"path": "test.png", "purpose": "tiny regression image", "rights": "approved"}; case["slides"][0]["image"] = "demo"
run_case(case, False, "approved image", with_image=True)
case["assets"]["demo"]["rights"] = "hold"; run_case(case, True, "image rights hold", with_image=True)
case["assets"]["demo"]["rights"] = "approved"
case["slides"][7]["image"] = "demo"; run_case(case, True, "image reused without reason", with_image=True)
case["assets"]["demo"]["reuse_reason"] = "same deck identity"; run_case(case, False, "explicit image reuse", with_image=True)
sample = {"id": "hierarchy-test", "layout": "cards", "title": "样例", "kicker": "MATERIAL FOUNDATION", "items": ["无机矿物｜提供稳定底座。", "玄武岩纤维｜参与增强。"]}
markup = module.render_slide(sample, 1, 2, {}, root, set())
assert '<strong class="card-title">无机矿物</strong>' in markup
assert '<span class="card-detail">提供稳定底座。</span>' in markup
assert markup.count("MATERIAL FOUNDATION") == 1, "interior section label should not repeat above title"
five = dict(sample, items=[f"项目{i}｜解释{i}" for i in range(5)])
assert 'class="bodygrid cards-5"' in module.render_slide(five, 1, 2, {}, root, set())
four = dict(sample, layout="table", items=[f"层级{i}｜依据{i}｜边界{i}" for i in range(4)])
table_markup = module.render_slide(four, 1, 2, {}, root, set())
assert 'class="tablemain table-4"' in table_markup
assert table_markup.count('class="tablecell"') == 4
assert table_markup.count('class="table-detail"') == 8
print("build-deck regression checks passed")
