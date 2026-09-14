"""Regression checks for the focused guide-first entry pages. No submissions."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = '520afbd'

def previous(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT, text=True)

home = (ROOT / 'index.html').read_text()
assert len(re.findall(r'class="choice-card\b', home)) == 2
assert 'id="dating-uncertainty"' not in home
assert 'dating spirals' in home
assert home.index('choice-grid') < home.index('id="about-robert"') < home.index('id="client-stories"')
proof = r'<section class="section testimonial-section".*?</section>'
assert re.search(proof, home, re.S).group() == re.search(proof, previous('index.html'), re.S).group()
for slug in ['why-you-react-that-way', 'why-you-keep-having-the-same-fight']:
    assert f'href="/{slug}/#get-guide"' in home
    for path in [slug + '.html', slug + '/index.html']:
        current = (ROOT / path).read_text()
        form = r'<form.*?</form>'
        assert re.search(form, current, re.S).group() == re.search(form, previous(path), re.S).group(), path
        assert 'id="get-guide"' in current
        assert current.index('<form') < current.index('guide-coaching')
        assert current.count('<h1>') == 1
    # Preserve the pre-existing aria-invalid defaults on clean-route copies.
    assert (ROOT / (slug + '.html')).read_text() == (ROOT / slug / 'index.html').read_text().replace(' aria-invalid="false"', '')
assert (ROOT / 'free.html').read_bytes() == (ROOT / 'free-guides/index.html').read_bytes()
for path in ['assets/styles.css', 'assets/main.js', 'CNAME', 'work-with-me.html', 'work-with-robert/index.html', 'apply.html', 'apply/index.html', 'individual-coaching.html', 'individual-coaching/index.html', 'couples-coaching.html', 'couples-coaching/index.html', 'group-coaching.html', 'group-coaching/index.html']:
    assert (ROOT / path).read_text() == previous(path), path
print('PASS: two choices, direct signup anchors, exact Kit forms, testimonial markup, clean routes, and unchanged paid pages/settings.')
