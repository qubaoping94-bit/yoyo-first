"""Browser QA for every generated slide: overflow, obscured text, image loading and sparse body."""
import argparse
import json
import os
from pathlib import Path


def audit(html, report, browser_path=None):
    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as p:
        kwargs = {"headless": True}
        if browser_path:
            kwargs["executable_path"] = str(browser_path)
        browser = p.chromium.launch(**kwargs)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, reduced_motion="reduce")
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(html.resolve().as_uri())
        count = page.locator(".slide").count()
        for width, height in ((1920, 1080), (1440, 900), (1280, 720)):
          page.set_viewport_size({"width": width, "height": height})
          page.evaluate("fit()")
          for i in range(count):
            page.evaluate("i => show(i)", i)
            result = page.evaluate("""i => {
              const s=document.querySelectorAll('.slide')[i],m=s.querySelector('main'),sr=s.getBoundingClientRect(),mr=m.getBoundingClientRect();
              const texts=[...s.querySelectorAll('main h1,main p,main .kicker,main .card,main .tablecell,main .conclusion')];
              const bad=[]; for(const el of texts){const r=el.getBoundingClientRect(); if(r.width<1||r.height<1)continue;
                if(r.left<sr.left-2||r.right>sr.right+2||r.top<sr.top-2||r.bottom>sr.bottom+2)bad.push('overflow '+el.textContent.slice(0,20));
                const x=r.left+r.width/2,y=r.top+r.height/2,top=document.elementFromPoint(x,y);
                if(top && top!==el && !el.contains(top))bad.push('obscured '+el.textContent.slice(0,20));
              }
              for(const img of s.querySelectorAll('img'))if(!img.complete||img.naturalWidth===0)bad.push('image missing');
              const cards=[...m.querySelectorAll('.card,.tablecell')].map(e=>e.getBoundingClientRect());
              if(cards.length){const b=Math.max(...cards.map(r=>r.bottom));if(mr.bottom-b>mr.height*.29)bad.push('sparse lower body');}
              return {id:s.dataset.slideId,issues:bad}; }""", i)
            result["viewport"] = f"{width}x{height}"
            results.append(result)
        page.evaluate("show(0)")
        page.keyboard.press("p")
        panel_open = page.locator("#notes-panel").is_visible()
        before = page.locator(".slide.active").get_attribute("data-slide-id")
        page.locator("#notes-panel").evaluate("el => el.dispatchEvent(new WheelEvent('wheel',{deltaY:200,bubbles:true}))")
        note_wheel_safe = page.locator(".slide.active").get_attribute("data-slide-id") == before
        page.keyboard.press("Escape")
        panel_closed = not page.locator("#notes-panel").is_visible()
        if not (panel_open and note_wheel_safe and panel_closed):
            errors.append("speaker notes open/scroll/Escape behavior failed")
        browser.close()
    outcome = {"slides": count, "results": results, "browser_errors": errors, "pass": not errors and all(not x["issues"] for x in results), "visual_review_required": True}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(outcome, ensure_ascii=False, indent=2), encoding="utf-8")
    return outcome


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--browser-path", type=Path, default=Path(os.environ["YOUYOU_BROWSER_PATH"]) if os.environ.get("YOUYOU_BROWSER_PATH") else None)
    args = parser.parse_args()
    result = audit(args.html, args.report, args.browser_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
