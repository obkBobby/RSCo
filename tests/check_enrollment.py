"""Run with python3 tests/check_enrollment.py; requires beautifulsoup4."""
from pathlib import Path
import json
import subprocess
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = '3f269842'
PAIRS = {'work-with-robert': 'work-with-me.html', 'individual-coaching': 'individual-coaching.html', 'couples-coaching': 'couples-coaching.html', 'group-coaching': 'group-coaching.html', 'apply': 'apply.html'}

def before(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT).decode()

def soup(text):
    return BeautifulSoup(text, 'html.parser')

for route, source in PAIRS.items():
    assert (ROOT / route / 'index.html').read_bytes() == (ROOT / source).read_bytes(), source

for route in ['', *list(PAIRS)[:-1]]:
    path = f'{route}/index.html' if route else 'index.html'
    text = (ROOT / path).read_text()
    current, previous = soup(text), soup(before(path))
    for forbidden in ['Before you enroll', 'Program terms', 'Stripe', 'nonrefundable', 'reschedule up to']:
        assert forbidden not in text, (path, forbidden)
    assert not current.select('#program-policy')
    for selector in ['video', 'form', '.testimonial-section', '#program-details li', '#coaching-options li']:
        assert [str(x) for x in current.select(selector)] == [str(x) for x in previous.select(selector)], (path, selector)
    if route:
        assert len(current.select('main a.button[href="/apply/"]')) == 1, path
        assert len(current.select('a[href="/apply/#enrollment-faq"]')) == 1, path
        assert '16 weeks' in text and '8 ' in text
    for price in ['$997', '$2,500', '$3,500']:
        assert text.count(price) == before(path).count(price)

faq = soup((ROOT / 'apply/index.html').read_text()).select_one('#enrollment-faq')
assert len(faq.select('article')) == 8
for phrase in ['up to 2 private sessions', '24 hours notice for each', 'within 14 days', 'within 18 weeks', '8 fixed cohort dates', 'do not include private makeup sessions', 'Payment is due in full', 'voluntary withdrawal', 'Mandatory legal rights', 'refund for the undelivered service', 'full coaching terms to review and sign before payment', 'private message, text, and voice coaching are not included']:
    assert phrase in faq.get_text(), phrase

files = list(ROOT.glob('*.html')) + list(ROOT.glob('*/index.html'))
links = 0
for file in files:
    doc = soup(file.read_text())
    assert len(doc.select('h1')) == 1, file
    for block in doc.select('script[type="application/ld+json"]'):
        json.loads(block.string)
    for tag in doc.select('[href], [src], [poster]'):
        for attr in ['href', 'src', 'poster']:
            url = tag.get(attr)
            if not url:
                continue
            assert not any(x in url.lower() for x in ['buy.stripe.com', 'checkout.stripe.com', 'klarna', 'afterpay'])
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            target = ROOT / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/') else file.parent / unquote(parsed.path)
            if not parsed.path:
                target = file
            if target.is_dir():
                target /= 'index.html'
            assert target.exists(), (file, url)
            if parsed.fragment and target.suffix == '.html':
                assert soup(target.read_text()).find(id=unquote(parsed.fragment)), (file, url)
            links += 1
assert (ROOT / 'CNAME').read_text() == before('CNAME')
assert not subprocess.check_output(['git', 'diff', BASE, '--', 'assets'], cwd=ROOT)
print(f'PASS: {len(files)} HTML pages, {links} local links/assets/anchors; 5 synchronized pairs; discovery, prices, inclusions, videos, forms, FAQ, and deployment invariants.')
