"""Regression check: uv run --with beautifulsoup4 python tests/check_no_community.py."""
from pathlib import Path
import re
import subprocess
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = 'a9bf37d'
PAIRS = {
    'work-with-robert': 'work-with-me.html',
    'group-coaching': 'group-coaching.html',
    'individual-coaching': 'individual-coaching.html',
    'couples-coaching': 'couples-coaching.html',
    'apply': 'apply.html',
}
files = sorted(ROOT.glob('*.html')) + sorted(ROOT.glob('*/index.html'))
failures = []
for file in files:
    path = str(file.relative_to(ROOT))
    current = BeautifulSoup(file.read_text(), 'html.parser')
    previous = BeautifulSoup(subprocess.check_output(
        ['git', 'show', f'{BASE}:{path}'], cwd=ROOT).decode(), 'html.parser')
    # Historical accounts are evidence, not current offer promises: preserve verbatim.
    for selector in ['.testimonial-section', 'video', 'form', 'a', 'script', 'link']:
        assert [str(x) for x in current.select(selector)] == [str(x) for x in previous.select(selector)], (path, selector)
    for price in ['$997', '$2,500', '$3,500']:
        assert current.get_text().count(price) == previous.get_text().count(price), (path, price)
    for testimonial in current.select('.testimonial-section'):
        testimonial.decompose()
    text = current.get_text(' ', strip=True)
    if re.search(r'community|weekly implementation prompts|\bPodia\b|peer platform', text, re.I):
        failures.append(path)
assert not failures, f'Stale community/off-session offer copy: {failures}'
for route, source in PAIRS.items():
    assert (ROOT / route / 'index.html').read_bytes() == (ROOT / source).read_bytes(), source
work = (ROOT / 'work-with-me.html').read_text()
group = (ROOT / 'group-coaching.html').read_text()
assert 'Facilitated practice, short teaching, and selected coaching during live sessions' in work
assert 'Facilitated practice, short teaching, and selected coaching during live sessions' in group
assert 'Group coaching is for individuals, whether single or partnered.' in group
assert 'Coaching happens during scheduled live sessions.' in group
assert 'between-session exercises' in (ROOT / 'couples-coaching.html').read_text()
assert 'private message, text, and voice coaching are not included' in (ROOT / 'apply.html').read_text()
for path in ['assets', 'CNAME', '.nojekyll']:
    assert not subprocess.check_output(['git', 'diff', BASE, '--', path], cwd=ROOT), path
print(f'PASS: {len(files)} public HTML files; no community/off-session offer promises; 5 synchronized pairs; testimonials, prices, session headers, assets and links unchanged.')
