"""Read-only guide QA. Default local; --base https://robertsawyer.co for production.
Run: uv run --with beautifulsoup4 --with playwright python tests/check_guide_browser.py
Does not submit forms. Screenshots/reports stay in .git/guide-copy-qa.
"""
import argparse
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright
from check_guide_humanization import ROOT, FILES

parser = argparse.ArgumentParser()
parser.add_argument('--base')
args = parser.parse_args()
server = None
if args.base:
    origin = args.base.rstrip('/')
    label = 'production'
else:
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass
        def copyfile(self, source, outputfile):
            try:
                super().copyfile(source, outputfile)
            except (BrokenPipeError, ConnectionResetError):
                pass
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_address[1]}'
    label = 'local'
OUT = ROOT / '.git' / 'guide-copy-qa' / label
OUT.mkdir(parents=True, exist_ok=True)
report = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        # Keep form rendering script, block external telemetry and all writes.
        def safe_route(route):
            request = route.request
            if request.method != 'GET' or any(x in request.url for x in ['google-analytics', 'googletagmanager', '/collect', 'facebook.com/tr', 'doubleclick']):
                return route.abort()
            if request.url.startswith(origin) or request.url.startswith('https://f.convertkit.com/ckjs/'):
                return route.continue_()
            return route.abort()
        context.route('**/*', safe_route)
        for width in [320, 390, 768, 1440]:
            page = context.new_page()
            page.set_viewport_size({'width': width, 'height': 900})
            for file in FILES:
                route = '/' + file.replace('/index.html', '/')
                response = page.goto(origin + route, wait_until='networkidle')
                assert response.status == 200, route
                expected = 'One message from them, and you’re thinking about it all day.' if 'react' in file else 'You’ve explained why it hurts. Somehow, you’re having the argument again.'
                assert page.locator('h1').text_content() == expected, route
                assert page.locator('form').count() == 1
                metrics = page.evaluate('''() => ({width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
                  overflowingText: [...document.querySelectorAll('h1,h2,h3,p,li,a')].filter(e => e.clientWidth && e.scrollWidth > e.clientWidth + 1).map(e => e.textContent),
                  brokenWords: [...document.querySelectorAll('h1,h2,h3')].flatMap(e => {const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n;const out=[];while(n=walker.nextNode()){for(const m of n.textContent.matchAll(/\\S+/g)){const r=document.createRange();r.setStart(n,m.index);r.setEnd(n,m.index+m[0].length);if(new Set([...r.getClientRects()].map(x=>Math.round(x.y))).size>1)out.push(m[0]);}}return out;})})''')
                assert metrics['scrollWidth'] <= width, (route, metrics)
                assert not metrics['overflowingText'], (route, metrics)
                assert not metrics['brokenWords'], (route, metrics)
                screenshot = OUT / (file.replace('/', '-') + f'-{width}.png')
                page.screenshot(path=str(screenshot), full_page=True)
                page.locator('.hero-actions .primary').click()
                assert page.url.endswith('#get-guide')
                assert page.locator('#get-guide').is_visible()
                destination = '/individual-coaching/' if 'react' in file else '/couples-coaching/'
                page.locator('.hero-actions .secondary').click()
                assert page.url == origin + destination
                assert page.locator('h1').is_visible()
                report.append({'route': route, 'width': width, 'status': response.status, 'metrics': metrics, 'coaching_destination': destination, 'screenshot': str(screenshot)})
            page.close()
        browser.close()
finally:
    if server:
        server.shutdown()
        server.server_close()
    (OUT/'report.json').write_text(json.dumps(report, indent=2))
assert len(report) == 16
print(json.dumps({'label':label, 'checked':len(report), 'broken_words': [r for r in report if r['metrics']['brokenWords']], 'report':str(OUT/'report.json')}, indent=2))
