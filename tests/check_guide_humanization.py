"""Guide copy release: exact text edits and immutable production baseline.
Run: uv run --with beautifulsoup4 python tests/check_guide_humanization.py
"""
from pathlib import Path
import subprocess
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = '1b243159b9fb60ac36d11357cfce189c18ac2a4a'
COPY = {
    'why-you-react-that-way': {
        'A free guide to the protection patterns that take over when relationships feel unsafe.': 'A free guide to understanding how you respond when a relationship feels uncertain and what you could try differently.',
        'Your reaction is not random.': 'One message from them, and you’re thinking about it all day.',
        'It is usually a protection pattern that learned how to keep you safe before it learned how to keep you connected.': 'This free guide helps you look at what happens in those moments, why you respond the way you do, and what you could try differently.',
        'For the reaction you keep explaining after the fact.': 'You wish you’d handled it differently.',
        'If you can understand your reaction after the fact but still cannot interrupt it in real time, that is where coaching begins.': 'You replay what you said, or what you wish you’d said. If you want help putting what you notice into practice, individual coaching is an option.',
        'The reaction is a signal. The pattern is the work.': 'What happens when you feel unsure?',
        'This guide helps you name the protective reactions that take over when connection feels unsafe.': 'You might reread a message, go quiet, or agree to something you do not want. The guide helps you notice how you respond and what tends to happen next.',
        'Overthinking and reassurance loops': 'Rereading messages and asking for reassurance',
        'Defensive reactions': 'Defending yourself before you’ve heard them out',
        'Shutdown and avoidance': 'Going quiet or avoiding the conversation',
        'Control and people-pleasing': 'Trying to manage everything or keep them happy',
        'Overexplaining and self-abandonment': 'Explaining yourself again or ignoring what you need',
        'Repair that does not stick': 'Apologizing, then doing the same thing again',
        'A free guide for the protective reactions that take over when relationships feel unsafe.': 'A free guide to understanding your reactions when a relationship feels uncertain.',
        'If you can see the reaction after the fact but cannot interrupt it in real time, start here.': 'If there is abuse or coercion, prioritize your safety and seek specialist support. Their harmful behavior is not yours to fix.',
    },
    'why-you-keep-having-the-same-fight': {
        'A free guide to the hidden pattern underneath repeated couple conflict.': 'A free guide to seeing where the same argument goes wrong and choosing one thing to try differently.',
        'The topic changes. The pattern stays the same.': 'You’ve explained why it hurts. Somehow, you’re having the argument again.',
        'This free guide helps you identify the hidden loop underneath the fight so you can stop fighting the symptom and start understanding the pattern.': 'This free guide helps you trace how the conversation goes wrong and choose one thing to try differently next time.',
        'No villain required, but responsibility is required.': 'You wanted them to understand.',
        'If you can see the loop but cannot change it together, couples coaching helps you map the pattern and practice new ways of relating.': 'Instead, you’re defending what you meant or giving up on the conversation. Couples coaching offers space to work through those moments and practice a different response together.',
        'Repeated fights are usually outputs.': 'Where does the conversation turn?',
        'The guide helps you notice the structure underneath conflict, shutdown, control, distance, and resentment.': 'Look at what each person says or does, where the conversation gets harder, and what happens afterward. The guide helps you put those moments in order.',
        'Repeated fights in different forms': 'Different topics that end in the same argument',
        'Pursuer / withdrawer loops': 'One person pushing to talk while the other pulls away',
        'Manager / employee dynamics': 'One person doing the planning and reminding',
        'Parent / child dynamics': 'Feeling lectured, corrected, or checked up on',
        'Anxiety and reassurance loops': 'Asking for reassurance but still feeling unsure',
        'Repair attempts that do not last': 'Making up without resolving what happened',
        'If the topic changes but the structure of the fight stays the same, start here.': 'Abuse and coercion are not a shared communication problem. Prioritize safety and seek specialist support rather than trying to work through them together with this guide.',
    },
}
# Legacy pages have different historical copy and attributes. Match text slots
# against each page's own baseline rather than overwriting it with the clean route.
FILES = {}
for slug, changes in COPY.items():
    canonical = subprocess.check_output(['git', 'show', f'{BASE}:{slug}/index.html'], cwd=ROOT).decode()
    legacy = subprocess.check_output(['git', 'show', f'{BASE}:{slug}.html'], cwd=ROOT).decode()
    old_clean, old_legacy = [BeautifulSoup(x, 'html.parser') for x in (canonical, legacy)]
    # Main content has identical structure; navigation intentionally differs.
    selectors = ['meta[name="description"]', 'meta[property="og:description"]',
                 '.hero h1', '.hero-copy', '.guide-preview-card h2', '.guide-preview-card p',
                 '.section.split h2', '.section.split .stack > p', '#get-guide .lede',
                 '#get-guide .lead-panel-grid > div > p:last-child']
    selectors += [f'.symptom-list li:nth-child({i})' for i in range(1, 7)]
    legacy_changes = {}
    for selector in selectors:
        a, b = old_clean.select_one(selector), old_legacy.select_one(selector)
        a_text = a.get('content') if a.name == 'meta' else str(a.string)
        b_text = b.get('content') if b.name == 'meta' else str(b.string)
        if a_text in changes:
            legacy_changes[b_text] = changes[a_text]
    FILES[slug+'/index.html'] = changes
    FILES[slug+'.html'] = legacy_changes


def before(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def check():
    for path, changes in FILES.items():
        original = before(path).decode()
        expected = original
        for old, new in changes.items():
            assert old in expected, (path, 'missing baseline text', old)
            assert not any(mark in new for mark in ['—', '–']), new
            expected = expected.replace(old, new)
        current = (ROOT/path).read_text()
        assert current == expected, (path, 'must contain only the approved text replacements')
        old, new = [BeautifulSoup(x, 'html.parser') for x in (original, current)]
        def structure(doc):
            result = []
            for tag in doc.find_all(True):
                attrs = dict(tag.attrs)
                if tag.name == 'meta' and (tag.get('name') == 'description' or tag.get('property') == 'og:description'):
                    attrs.pop('content', None)
                result.append((tag.name, attrs))
            return result
        assert structure(old) == structure(new), (path, 'DOM/attributes')
        for selector in ['form', 'a', 'script', 'style', 'link', 'video', '.testimonial-section', 'title']:
            assert [str(x) for x in old.select(selector)] == [str(x) for x in new.select(selector)], (path, selector)
        assert new.select_one('.hero-actions .secondary')['href'] == ('/individual-coaching/' if 'react' in path else '/couples-coaching/')
        assert 'abuse' in new.get_text().lower() and 'coercion' in new.get_text().lower()
    production = [p for p in subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines() if not p.startswith('tests/')]
    tracked = [p for p in subprocess.check_output(['git', 'ls-files'], cwd=ROOT).decode().splitlines() if not p.startswith('tests/')]
    assert set(tracked) == set(production), 'Production file inventory changed'
    for path in production:
        if path not in FILES:
            assert (ROOT/path).read_bytes() == before(path), (path, 'outside guide-only scope')
    assert '$2,500' in (ROOT/'individual-coaching/index.html').read_text()
    print(f'PASS: {len(FILES)} guide files; exact copy, DOM, forms, links and routing; all {len(production)} production files checked against {BASE[:7]}.')


if __name__ == '__main__':
    check()
