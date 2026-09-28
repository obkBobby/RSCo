"""Approved buyer-language copy plus strict production-baseline preservation.
Run: python3 tests/check_buyer_language.py
"""
from pathlib import Path
import re
import subprocess
from bs4 import BeautifulSoup
from check_homepage_humanization import check, normalize_approved_choice_text

check()

ROOT = Path(__file__).resolve().parents[1]
BASE = '866512f4d5229fbf7febd1dbe90c0427dc9e2479'
EDITABLE = {'index.html', 'individual-coaching.html', 'individual-coaching/index.html',
            'work-with-me.html', 'work-with-robert/index.html'}
files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines()
for path in files:
    previous = subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)
    current = (ROOT/path).read_bytes()
    # check() above verifies the later approved guide-only release separately.
    from check_guide_humanization import FILES as GUIDE_FILES
    if path.startswith('tests/') or path in GUIDE_FILES:
        continue
    if path not in EDITABLE:
        assert current == previous, f'Unapproved change: {path}'
        continue
    old, new = [BeautifulSoup(x, 'html.parser') for x in (previous, current)]
    # Identical DOM elements/attributes except approved SEO content values.
    def structure(soup):
        result = []
        for tag in soup.find_all(True):
            attrs = dict(tag.attrs)
            if tag.name == 'meta' and (tag.get('name') == 'description' or tag.get('property') in ('og:title', 'og:description')):
                attrs.pop('content', None)
            result.append((tag.name, attrs))
        return result
    assert structure(new) == structure(old), (path, 'design/structure/URLs changed')
    if path == 'index.html':
        normalize_approved_choice_text(new)
    for selector in ['.testimonial-section', 'form', 'script', 'style', 'a', 'video', '#program-details', '#coaching-options ul', '#coaching-options .lede', '.trust-note']:
        assert [str(x) for x in new.select(selector)] == [str(x) for x in old.select(selector)], (path, selector)
    assert re.findall(r'\$[\d,]+', new.get_text()) == re.findall(r'\$[\d,]+', old.get_text()), path
    for story in new.select('.testimonial-section'):
        story.decompose()
    assert not re.search(r'community|weekly implementation prompts|\bPodia\b|peer platform|\$999', new.get_text(), re.I), path
    hero = new.select_one('.hero').get_text(' ', strip=True).lower()
    if path == 'index.html':
        assert 'you still miss them' in hero and 'relationship' in hero, (path, 'approved buyer situations')
    else:
        assert 'breakup' in hero and 'relationship' in hero, (path, 'missing recognizable buyer situations')
    assert 'start with the pattern.' not in hero and 'old protection patterns' not in hero, path
    description = new.select_one('meta[name="description"]')['content'].lower()
    assert 'breakup' in description and 'relationship' in description, (path, 'metadata')
for legacy, clean in [('individual-coaching.html', 'individual-coaching/index.html'), ('work-with-me.html', 'work-with-robert/index.html')]:
    assert (ROOT/legacy).read_bytes() == (ROOT/clean).read_bytes()
individual = (ROOT/'individual-coaching.html').read_text()
assert '$2,500' in individual and '16 weeks · 8 private 60-minute sessions · Every two weeks' in individual
home = (ROOT/'index.html').read_text()
assert 'You still miss them, even after everything that happened.' in home
assert 'I’m Robert. I help people work through' in home
assert 'understand what is happening' in home and 'practical steps forward' in home
print(f'PASS: buyer-language copy on {len(EDITABLE)} files; all {len(files)} baseline tracked files checked; structure, URLs, forms, testimonials, offers, terms and assets preserved.')
