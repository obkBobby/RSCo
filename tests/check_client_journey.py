from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import functools
import http.server
import json
import threading

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('/Users/obk/rsco-client-journey-qa')
OUT.mkdir(exist_ok=True)
PAGES = ['/', '/free-guides/', '/why-you-react-that-way/', '/why-you-keep-having-the-same-fight/', '/work-with-robert/', '/individual-coaching/', '/couples-coaching/', '/group-coaching/', '/apply/']
SOURCE_PAIRS = [
    ('work-with-me.html','work-with-robert/index.html'),
    ('individual-coaching.html','individual-coaching/index.html'),
    ('couples-coaching.html','couples-coaching/index.html'),
    ('group-coaching.html','group-coaching/index.html'),
    ('apply.html','apply/index.html'),
    ('free.html','free-guides/index.html'),
]
report = {'static': {}, 'browser': [], 'screenshots': []}
for a,b in SOURCE_PAIRS:
    assert (ROOT/a).read_bytes() == (ROOT/b).read_bytes(), (a,b)

broken=[]; parsed=0; refs=set()
for file in ROOT.rglob('*.html'):
    soup=BeautifulSoup(file.read_text(), 'html.parser'); parsed+=1
    assert soup.html and soup.head and soup.body and len(soup.select('h1'))==1, file
    for tag in soup.select('[href], [src], [poster]'):
        for attr in ['href','src','poster']:
            href=tag.get(attr)
            if not href: continue
            u=urlsplit(href)
            if u.scheme or u.netloc: continue
            target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else file.parent/unquote(u.path)
            if not u.path: target=file
            if target.is_dir(): target=target/'index.html'
            if not target.is_file():
                broken.append([str(file.relative_to(ROOT)), href]); continue
            refs.add(str(target.relative_to(ROOT)))
            if u.fragment and target.suffix=='.html':
                dest=BeautifulSoup(target.read_text(),'html.parser')
                if not dest.find(id=unquote(u.fragment)): broken.append([str(file.relative_to(ROOT)), href])
assert not broken, broken
home=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
sections=[s.find(['h1','h2']).get_text(' ',strip=True) for s in home.select('main > section') if s.find(['h1','h2'])]
text=home.get_text(' ',strip=True)
assert sections[:4] == ['Start with the pattern.', 'Which pattern keeps repeating?', 'The fight is expensive even when it only lasts 20 minutes.', 'If you keep explaining it afterward, start here.'], sections[:4]
assert 'If dating is where it shows up' not in text
assert text.count('Individual path') == 1 and text.count('Couples path') == 1
assert '$997' not in text and '$2,500' not in text and '$3,500' not in text
work=BeautifulSoup((ROOT/'work-with-robert/index.html').read_text(),'html.parser').get_text(' ',strip=True)
assert '$997 per person' not in work and '$2,500' not in work and '$3,500 per couple' not in work
for route, price in [('/group-coaching/','$997'),('/individual-coaching/','$2,500'),('/couples-coaching/','$3,500')]:
    page=BeautifulSoup((ROOT/route.strip('/')/'index.html').read_text(),'html.parser').get_text(' ',strip=True)
    assert price in page, route
assert 'Community support' not in work
report['static']={'html_parsed': parsed, 'reference_targets': len(refs), 'source_pairs': len(SOURCE_PAIRS), 'broken_links': broken, 'homepage_sections': sections, 'prices_removed_from_home_and_work_overview': True}

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
    def copyfile(self, source, outputfile):
        try: super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin=f'http://127.0.0.1:{server.server_address[1]}'
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        ctx=browser.new_context()
        ctx.route('**/*', lambda route: route.continue_() if route.request.url.startswith(origin) else route.abort())
        for width in [390, 1440]:
            page=ctx.new_page()
            page.set_viewport_size({'width': width, 'height': 900})
            for route in PAGES:
                r=page.goto(origin+route, wait_until='load')
                assert r.status == 200, route
                sizes=page.evaluate('({w:innerWidth,sw:document.documentElement.scrollWidth})')
                assert sizes['sw'] <= sizes['w'], (route,width,sizes)
                videos=page.locator('video').count()
                if route in ['/', '/work-with-robert/', '/individual-coaching/','/couples-coaching/']:
                    assert videos==4, (route, videos)
                if route in ['/', '/why-you-react-that-way/', '/why-you-keep-having-the-same-fight/']:
                    path=OUT/((route.strip('/').replace('/','-') or 'home')+f'-{width}.png')
                    page.screenshot(path=str(path), full_page=True)
                    report['screenshots'].append(str(path))
                report['browser'].append({'route':route,'width':width,'status':r.status,'overflow':False,'videos':videos})
            page.goto(origin+'/')
            page.get_by_role('link', name='Get the free guide: Why You React That Way').click()
            assert page.url == origin + '/why-you-react-that-way/'
            page.goto(origin+'/')
            page.get_by_role('link', name='Get the free guide: Why You Keep Having the Same Fight').click()
            assert page.url == origin + '/why-you-keep-having-the-same-fight/'
            page.goto(origin+'/')
            page.get_by_role('link', name='See how coaching works').click()
            assert page.url == origin + '/work-with-robert/'
            page.close()
        browser.close()
finally:
    server.shutdown(); server.server_close()
(OUT/'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
