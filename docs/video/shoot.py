import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
here = Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=2)
    for name in sys.argv[1:]:
        pg.goto((here / f"{name}.html").as_uri(), wait_until="networkidle")
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(here / f"{name}.png"))
        print("shot", name)
    b.close()
