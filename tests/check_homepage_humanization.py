"""Exact approved homepage text changes; all other production bytes frozen."""
from pathlib import Path
import subprocess
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = '967af1b'
APPROVED = {
    '.hero h1': 'You don’t want to keep feeling like this.',
    '.hero .hero-copy': 'You still miss them, even after everything that happened. Or you’re still together, but you keep wondering whether this is the relationship you want. You’ve talked it through, watched the videos, and tried to make sense of it. You want to know what to do now. I’m Robert. I help people work through what’s happening in their relationships and figure out what moving forward looks like for them.',
    '#find-your-pattern .choice-card:nth-child(1) span': 'Individual',
    '#find-your-pattern .choice-card:nth-child(1) strong': '“I keep ending up here.”',
    '#find-your-pattern .choice-card:nth-child(1) p': 'You reread the messages, explain away what hurt, or say yes when you want to say no. This guide helps you look at how you respond when a relationship feels uncertain.',
    '#find-your-pattern .choice-card:nth-child(2) span': 'Couples',
    '#find-your-pattern .choice-card:nth-child(2) strong': '“We’ve had this conversation before.”',
    '#find-your-pattern .choice-card:nth-child(2) p': 'You start talking about what happened today and end up in the same argument. This guide helps you see where the conversation keeps going wrong.',
}


def baseline_home():
    return subprocess.check_output(['git', 'show', f'{BASE}:index.html'], cwd=ROOT).decode()


def normalize_approved_choice_text(soup):
    """Only the six approved choice text nodes; preserve every anchor attribute."""
    previous = BeautifulSoup(baseline_home(), 'html.parser')
    for selector, expected in APPROVED.items():
        if not selector.startswith('#find-your-pattern '):
            continue
        nodes = soup.select(selector)
        assert len(nodes) == 1 and nodes[0].string == expected, selector
        nodes[0].string.replace_with(previous.select_one(selector).string)


def check():
    previous = baseline_home()
    current = (ROOT / 'index.html').read_text()
    old, new = [BeautifulSoup(x, 'html.parser') for x in (previous, current)]
    expected = previous
    for selector, approved in APPROVED.items():
        before, after = old.select(selector), new.select(selector)
        assert len(before) == len(after) == 1, selector
        assert before[0].string is not None and after[0].string == approved, selector
        original = str(before[0].string)
        assert expected.count(original) == 1, selector
        expected = expected.replace(original, approved, 1)
    assert current == expected, 'Changes outside the eight approved text nodes'
    assert [(x.name, x.attrs) for x in old.find_all(True)] == [(x.name, x.attrs) for x in new.find_all(True)]
    files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines()
    # Later approved guide copy has its own exact, production-baseline guard.
    from check_guide_humanization import FILES as GUIDE_FILES, check as check_guides
    check_guides()
    for path in files:
        if path == 'index.html' or path.startswith('tests/') or path in GUIDE_FILES:
            continue
        assert (ROOT / path).read_bytes() == subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT), path
    production = [p for p in subprocess.check_output(['git', 'ls-files'], cwd=ROOT).decode().splitlines() if not p.startswith('tests/')]
    assert set(production) == {p for p in files if not p.startswith('tests/')}, 'Added/removed production files'
    print(f'PASS: eight exact approved text nodes; DOM/attributes and all other homepage bytes unchanged; {len(production)} production files checked (assets, testimonials, links, prices, deployment config preserved).')


if __name__ == '__main__':
    check()
