from pathlib import Path
import html

ROOT = Path(__file__).parent
STYLE = "/assets/styles.css?v=20260714-search-capture"

NAV = '<nav class="nav" aria-label="Main navigation"><a href="/">Home</a><a href="/individual-coaching/">Individual Coaching</a><a href="/couples-coaching/">Couples Coaching</a><a href="/relationship-help/">Relationship Help</a><a href="/free-guides/">Free Guides</a><a href="/work-with-robert/">Work With Robert</a></nav>'
FOOTER_LINKS = '<a href="/">Home</a><a href="/individual-coaching/">Individual Coaching</a><a href="/couples-coaching/">Couples Coaching</a><a href="/relationship-help/">Relationship Help</a><a href="/free-guides/">Free Guides</a><a href="/work-with-robert/">Work With Robert</a>'

DISCLAIMER = "Coaching and education are not therapy, crisis support, or a substitute for medical or mental-health care. If there is abuse, coercion, violence, self-harm risk, addiction crisis, or immediate danger, prioritize safety and licensed professional/crisis support first."


def layout(title, description, canonical, body, scripts=''):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}" />
  <link rel="canonical" href="https://robertsawyer.co{canonical}" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(description)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://robertsawyer.co{canonical}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="stylesheet" href="{STYLE}" />
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/" aria-label="Robert Sawyer home"><span class="brand-mark">RS</span><span>Robert Sawyer</span></a>
    {NAV}
    <a class="nav-cta" href="/#find-your-pattern">Find Your Pattern</a>
  </header>
  <main>
{body}
  </main>
  <footer class="site-footer"><p>© <span id="year"></span> Robert Sawyer. Coaching and education, not therapy or crisis services.</p><div class="footer-links">{FOOTER_LINKS}</div></footer>
  {scripts}
  <script src="/assets/main.js"></script>
</body>
</html>
'''


def write_page(slug, title, description, body, scripts=''):
    content = layout(title, description, f'/{slug}/', body, scripts)
    d = ROOT / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(content, encoding='utf-8')
    (ROOT / f'{slug}.html').write_text(content, encoding='utf-8')
    print('wrote', slug)


def guide_form(form="individual"):
    if form == "couples":
        return '''<form action="https://app.kit.com/forms/9626927/subscriptions" class="lead-form kit-live-form seva-form formkit-form" method="post" data-sv-form="9626927" data-uid="40dd5a72c7" data-format="inline" data-version="5" data-email-tag="leadmagnet_same_fight" data-conversion-name="couples_guide_request" data-options='{"settings":{"after_subscribe":{"action":"message","success_message":"Welcome! Your Why You Keep Having the Same Fight guide will arrive in your e-mail shortly.","redirect_url":""},"recaptcha":{"enabled":false}},"version":"5"}'>
  <input type="hidden" name="form-name" value="Lead Magnet - Same Fight" />
  <label for="couples-first-name">First name</label><input class="formkit-input" id="couples-first-name" name="fields[first_name]" type="text" placeholder="First Name" autocomplete="given-name" required />
  <label for="couples-email">Email address</label><input class="formkit-input" id="couples-email" name="email_address" type="email" placeholder="Email Address" autocomplete="email" required />
  <button class="button primary formkit-submit" type="submit"><span>Send me the guide</span></button>
</form>'''
    return '''<form action="https://app.kit.com/forms/9626932/subscriptions" class="lead-form kit-live-form seva-form formkit-form" method="post" data-sv-form="9626932" data-uid="e6fc7c7ad0" data-format="inline" data-version="5" data-email-tag="leadmagnet_why_you_react_that_way" data-conversion-name="individual_guide_request" data-options='{"settings":{"after_subscribe":{"action":"message","success_message":"Welcome! Your Why You React That Way guide will arrive in your e-mail shortly.","redirect_url":""},"recaptcha":{"enabled":false}},"version":"5"}'>
  <input type="hidden" name="form-name" value="Lead Magnet - Why You React That Way" />
  <label for="individual-first-name">First name</label><input class="formkit-input" id="individual-first-name" name="fields[first_name]" type="text" placeholder="First Name" autocomplete="given-name" required />
  <label for="individual-email">Email address</label><input class="formkit-input" id="individual-email" name="email_address" type="email" placeholder="Email Address" autocomplete="email" required />
  <button class="button primary formkit-submit" type="submit"><span>Send me the guide</span></button>
</form>'''

hub_cards = [
    ('/relationship-coach-vs-therapist/', 'Relationship Coach vs Therapist', 'Which kind of help do you actually need?'),
    ('/marriage-coaching-vs-counseling/', 'Marriage Coaching vs Counseling', 'What changes when the work is coaching, not counseling?'),
    ('/couples-therapy-alternatives/', 'Couples Therapy Alternatives', 'Options when you need practical pattern work.'),
    ('/couples-therapy-not-working/', 'When Couples Therapy Is Not Working', 'Why insight may not be becoming behavior under pressure.'),
    ('/best-books-for-relationship-patterns/', 'Best Books for Relationship Patterns', 'Books can give language. Reps change the default.'),
    ('/attachment-style-quizzes/', 'Attachment Style Quizzes', 'Helpful signal or another way to avoid responsibility?'),
]

hub_body = f'''
    <section class="hero page-hero"><div class="eyebrow">Relationship Help Guides</div><h1>Choose the right kind of help before the pattern chooses for you.</h1><p class="hero-copy">These pages are for the person searching at midnight: therapy, coaching, books, quizzes, courses, or something else. The goal is not to sell every reader coaching. The goal is to help you tell the truth about what kind of help fits the pattern you keep repeating.</p><div class="hero-actions"><a class="button primary" href="/free-guides/">Start with a free guide</a><a class="button secondary" href="/work-with-robert/">Work With Robert</a></div></section>
    <section class="section split"><div><p class="section-kicker">Decision hub</p><h2>Stop collecting advice. Pick the next honest step.</h2></div><div class="stack"><p>Some people need licensed therapy. Some need crisis support. Some need couples counseling. Some need a direct coaching process that maps the loop and practices a different response.</p><p>These guides help you separate those paths without pretending one answer fits every relationship.</p><p class="trust-note">{DISCLAIMER}</p></div></section>
    <section class="section card-grid">{''.join(f'<article class="offer-card"><h3>{title}</h3><p>{desc}</p><a class="button secondary" href="{url}">Read the guide</a></article>' for url,title,desc in hub_cards)}</section>
    <section class="section dark-panel split"><div><p class="section-kicker">The conversion path</p><h2>If the guide names the problem, coaching gives you a next step.</h2></div><div class="stack"><p>Understanding the pattern is not the same as interrupting it while your body is activated. If the guide names the problem clearly, the next step is to explore coaching or start with the right free guide.</p><div class="pathway-actions"><a class="button primary" href="/work-with-robert/">Work With Robert</a><a class="button secondary" href="/free-guides/">Start with a free guide</a></div></div></section>
'''
write_page('relationship-help', 'Relationship Help Guides | Robert Sawyer', 'Plain-English guides that help you choose between therapy, coaching, books, quizzes, and practical pattern work.', hub_body)

pages = {
'relationship-coach-vs-therapist': {
'title':'Relationship Coach vs Therapist | Robert Sawyer',
'desc':'A plain-English guide to choosing between relationship coaching and therapy when patterns keep repeating.',
'kicker':'Relationship Help Guide',
'h1':'Relationship coach vs therapist: which kind of help do you actually need?',
'copy':'If you are searching this, you probably know something needs to change. The question is whether you need clinical treatment, couples therapy, or direct coaching that helps you map the pattern and practice different behavior.',
'lead':'individual',
'sections':[('Therapy is the better first step when safety or clinical care is the real issue.','If there is abuse, coercion, violence, self-harm risk, addiction crisis, severe untreated symptoms, or trauma work that needs clinical containment, start with licensed care. Coaching should not pretend to be treatment.'),('Coaching may fit when you are stable enough to practice responsibility.','Coaching is useful when you already see the pattern but keep losing access to a better move under pressure: shutting down, defending, controlling, people-pleasing, overexplaining, or repairing too late.'),('The honest question is not “which one sounds nicer?”','Ask: do I need diagnosis and treatment, or do I need pattern mapping, direct accountability, and repeated practice? Some people need both. Some need therapy first. Some are ready for coaching now.')],
'cta_title':'If your reaction is the part you keep cleaning up later, start here.',
'cta_copy':'Get the individual guide and see whether the pattern language fits what is happening in your life.'
},
'marriage-coaching-vs-counseling': {
'title':'Marriage Coaching vs Counseling | Robert Sawyer',
'desc':'A direct comparison of marriage coaching and marriage counseling for couples stuck in repeated fights.',
'kicker':'Relationship Help Guide','h1':'Marriage coaching vs counseling: what changes when the loop is the real problem?',
'copy':'Counseling and coaching can both help a marriage. But they do not do the same job. If you keep having the same fight, the next step depends on whether you need clinical support, emotional processing, or direct pattern interruption.',
'lead':'couples',
'sections':[('Counseling may be the right container for deeper clinical work.','Licensed counseling can support mental-health treatment, trauma care, diagnosis, crisis stabilization, and therapeutic repair. If safety is unstable, start there.'),('Marriage coaching is more practical and behavioral.','The work is to map the repeated loop, name each person’s role, identify the hidden rule, and practice a new response before the conversation becomes the same old fight.'),('The topic is usually not the only issue.','Money, sex, parenting, tone, chores, and phones may all become the stage. The pattern underneath is often the actual machine.')],
'cta_title':'If the subject keeps changing but the fight stays the same, get the couples guide.',
'cta_copy':'It will help you identify the loop before another conversation turns into the same ending.'
},
'couples-therapy-alternatives': {
'title':'Couples Therapy Alternatives | Robert Sawyer',
'desc':'Ethical alternatives to couples therapy for couples who need practical help interrupting repeated relationship patterns.',
'kicker':'Relationship Help Guide','h1':'Couples therapy alternatives for couples who keep repeating the same fight.',
'copy':'This is not anti-therapy. It is for couples who are not in immediate danger and are trying to decide what kind of support fits the actual problem.',
'lead':'couples',
'sections':[('Alternative does not mean replacement.','If there is abuse, coercion, violence, crisis, or clinical instability, therapy and safety support come first. Coaching is not the brave choice when safety is being ignored.'),('If the issue is repetition, look for pattern work.','A useful alternative should help you map the loop: who pursues, who withdraws, who manages, who resists, who repairs too late, and what each person’s system is trying to protect.'),('Books, courses, retreats, and coaching all work only if they become behavior.','The question is not “did this make sense?” The question is “can we do something different when pressure hits?”')],
'cta_title':'Start by naming the loop.',
'cta_copy':'Get the couples guide if the fight keeps returning in a different outfit.'
},
'couples-therapy-not-working': {
'title':'When Couples Therapy Is Not Working | Robert Sawyer',
'desc':'What to consider when couples therapy is not translating into different behavior during repeated fights.',
'kicker':'Relationship Help Guide','h1':'When couples therapy is not working, the problem may be the missing reps.',
'copy':'Sometimes therapy is not the problem. Sometimes the insight is real, but it is not becoming a different move in the moment that matters.',
'lead':'couples',
'sections':[('Do not use this page to avoid accountability.','If therapy is naming your part and you are resisting it, the issue may not be the therapist. The issue may be the part of you that wants change without surrendering the old protection.'),('Look for the transfer gap.','Can you describe the pattern in session but still repeat it in the kitchen, car, bedroom, or text thread? That is the transfer gap: insight is not transferring into behavior under pressure.'),('Coaching can help when the work is practice.','Pattern work focuses on the repeatable moments: the first defensive answer, the shutdown, the pursuing text, the contempt line, the late apology, the repair attempt that does not land.')],
'cta_title':'If the same fight keeps surviving good conversations, map the loop.',
'cta_copy':'Get the free guide and start identifying the pattern that keeps beating your intentions.'
},
'best-books-for-relationship-patterns': {
'title':'Best Books for Relationship Patterns | Robert Sawyer',
'desc':'A practical reading guide for understanding repeated relationship patterns, attachment, conflict, and repair.',
'kicker':'Relationship Help Guide','h1':'Best books for relationship patterns — and why reading more may not be enough.',
'copy':'Books can give you language. Language matters. But if you use reading to avoid the hard conversation, the book becomes another hiding place.',
'lead':'individual',
'sections':[('Read for mirrors, not ammunition.','The best relationship book is not the one that proves your partner is the problem. It is the one that makes your part harder to avoid.'),('Useful categories: attachment, conflict, nervous system, boundaries, repair.','Look for resources that help you name the loop, not just diagnose the other person. If the material never asks anything costly of you, be suspicious.'),('The next step after insight is a practiced interruption.','After the book names your pattern, write the move you will practice: pause, repair, boundary, direct ask, self-soothing, honest admission, or stopping the old management strategy.')],
'cta_title':'If you already understand too much and still repeat it, get the individual guide.',
'cta_copy':'It is built for the gap between “I know why” and “I did something different.”'
},
'attachment-style-quizzes': {
'title':'Attachment Style Quizzes | Helpful or Harmful? | Robert Sawyer',
'desc':'A direct guide to using attachment style quizzes without turning them into excuses or identity labels.',
'kicker':'Relationship Help Guide','h1':'Attachment style quizzes can help. They can also become a disguise.',
'copy':'An attachment quiz can give useful language. But if the label becomes your excuse, it stops helping. “I am anxious” is not a lifetime permission slip to control. “I am avoidant” is not a personality exemption from repair.',
'lead':'individual',
'sections':[('Use the label as a starting point, not a verdict.','The point is not to become fluent in your attachment style. The point is to notice what you do when closeness, distance, conflict, or uncertainty activates you.'),('Ask what the style protects.','Anxious strategies often protect against abandonment. Avoidant strategies often protect against engulfment, shame, or dependence. The protection made sense. It may still be causing damage.'),('The better question: what is my move in the loop?','Do you pursue, test, manage, withdraw, punish with distance, overexplain, collapse, criticize, or disappear? That is where the work starts.')],
'cta_title':'If the label explained you but did not change you, start here.',
'cta_copy':'Get the guide for the reaction you keep justifying, regretting, or cleaning up.'
},
}

for slug, p in pages.items():
    form = guide_form(p['lead'])
    body = f'''
    <section class="hero page-hero"><div class="eyebrow">{p['kicker']}</div><h1>{p['h1']}</h1><p class="hero-copy">{p['copy']}</p><div class="hero-actions"><a class="button primary" href="#next-step">Start with the free guide</a><a class="button secondary" href="/relationship-help/">Relationship Help Guides</a></div></section>
    <section class="section split"><div><p class="section-kicker">My read</p><h2>Do not pick the help that protects the pattern.</h2></div><div class="stack"><p>The right resource should make the repeated loop clearer and your responsibility harder to dodge. The wrong resource gives you more language while the same behavior keeps running your relationship.</p><p class="trust-note">{DISCLAIMER}</p></div></section>
    <section class="section process-grid">{''.join(f'<article class="process-card"><strong>{html.escape(title)}</strong><p>{html.escape(copy)}</p></article>' for title, copy in p['sections'])}</section>
    <section class="section dark-panel guide-offer-panel" id="next-step"><div class="lead-panel-grid"><div><p class="section-kicker">Next honest step</p><h2>{p['cta_title']}</h2><p class="lede">{p['cta_copy']}</p><p>If the guide names the pattern too clearly to ignore, the next step is the right free guide or a coaching conversation.</p><div class="pathway-actions"><a class="button secondary" href="/free-guides/">Start with a free guide</a><a class="button secondary" href="/work-with-robert/">Work With Robert</a></div></div><aside class="kit-card"><p class="card-label">Free guide</p><h3>{'Why You Keep Having the Same Fight' if p['lead']=='couples' else 'Why You React That Way'}</h3><p>Enter your first name and email below.</p>{form}<p class="form-note">You will get the guide by email. No spam. Unsubscribe anytime.</p></aside></div></section>
'''
    write_page(slug, p['title'], p['desc'], body, '<script src="https://f.convertkit.com/ckjs/ck.5.js"></script>')

# Mid-tier offer page is intentionally orphaned for now. Do not add it to nav/homepage until Rob revisits the offer/name.
lab_body = f'''
    <section class="hero page-hero"><div class="eyebrow">Pattern Interrupt Lab</div><h1>Stop understanding the pattern and start interrupting it.</h1><p class="hero-copy">A 6-week practice group for people who react, shut down, defend, control, people-please, overexplain, or keep repeating the same relational loop.</p><div class="hero-actions"><a class="button primary" href="#waitlist">Join the waitlist</a><a class="button secondary" href="/relationship-help/">Read the guides</a></div></section>
    <section class="section split"><div><p class="section-kicker">Who this is for</p><h2>You know the pattern. You still lose the moment.</h2></div><div class="stack"><p>This is for the person who can explain the problem afterward but cannot access the better move when pressure hits.</p><ul class="symptom-list"><li>You defend before you understand.</li><li>You shut down and call it staying calm.</li><li>You control details because uncertainty feels unsafe.</li><li>You people-please, then punish with resentment.</li><li>You overexplain instead of telling the truth cleanly.</li><li>You repair late, then repeat the same move.</li></ul></div></section>
    <section class="section dark-panel"><p class="section-kicker">6-week structure</p><h2>The work is reps, not more self-awareness.</h2><div class="process-grid two"><article class="process-card"><strong>1. Name the loop</strong><p>Write down what actually happens before, during, and after the reaction.</p></article><article class="process-card"><strong>2. Find the hidden rule</strong><p>Name what your system believes it must do to stay safe or in control.</p></article><article class="process-card"><strong>3. Track the body signal</strong><p>Catch the first moment your body decides the relationship is a threat.</p></article><article class="process-card"><strong>4. Interrupt the old move</strong><p>Practice the pause, sentence, boundary, repair, or ask you usually lose.</p></article><article class="process-card"><strong>5. Practice relational courage</strong><p>Tell the truth without collapsing, controlling, or making the other person responsible for your regulation.</p></article><article class="process-card"><strong>6. Build the new default</strong><p>Leave with a written pattern map, interruption plan, repair plan, and 30-day practice path.</p></article></div></section>
    <section class="section split"><div><p class="section-kicker">Positioning</p><h2>The Lab sits between free guides and private coaching.</h2></div><div class="stack"><p>Private coaching is deeper and more personalized. The Lab is a lower-friction way to get Robert's pattern-mapping method, group accountability, and practice structure.</p><p>This first version should be treated as a beta: small group, direct feedback, clear fit standards, and no promise that coaching replaces therapy.</p><p class="trust-note">{DISCLAIMER}</p></div></section>
    <section class="section dark-panel guide-offer-panel" id="waitlist"><div class="lead-panel-grid"><div><p class="section-kicker">Join the waitlist</p><h2>Be first in line for Pattern Interrupt Lab.</h2><p class="lede">Join below and get the individual guide now. When the beta opens, you will get first notice.</p><p>Best fit: people who are stable enough for coaching, willing to take responsibility for their part of the loop, and ready to practice instead of only understand.</p></div><aside class="kit-card"><p class="card-label">Waitlist + free guide</p><h3>Join the Lab waitlist</h3><p>Enter your first name and email below.</p><form action="https://app.kit.com/forms/9626932/subscriptions" class="lead-form kit-live-form seva-form formkit-form" method="post" data-sv-form="9626932" data-uid="e6fc7c7ad0" data-format="inline" data-version="5" data-email-tag="pattern_interrupt_lab_waitlist" data-conversion-name="pattern_interrupt_lab_waitlist" data-options='{{"settings":{{"after_subscribe":{{"action":"message","success_message":"You are on the Pattern Interrupt Lab interest list. Your Why You React That Way guide will arrive by email shortly.","redirect_url":""}},"recaptcha":{{"enabled":false}}}},"version":"5"}}'>\n  <input type="hidden" name="form-name" value="Pattern Interrupt Lab Waitlist" />\n  <input type="hidden" name="fields[interest]" value="Pattern Interrupt Lab" />\n  <label for="lab-first-name">First name</label><input class="formkit-input" id="lab-first-name" name="fields[first_name]" type="text" placeholder="First Name" autocomplete="given-name" required />\n  <label for="lab-email">Email address</label><input class="formkit-input" id="lab-email" name="email_address" type="email" placeholder="Email Address" autocomplete="email" required />\n  <button class="button primary formkit-submit" type="submit"><span>Join the waitlist</span></button>\n</form><p class="form-note">You will also get the individual guide by email. No spam. Unsubscribe anytime.</p></aside></div></section>
'''
write_page('pattern-interrupt-lab', 'Pattern Interrupt Lab | Robert Sawyer', 'A 6-week practice group for interrupting repeated relationship patterns in real time.', lab_body, '<script src="https://f.convertkit.com/ckjs/ck.5.js"></script>')

# Update nav/footer in existing HTML files.
old_navs = [
'<nav class="nav" aria-label="Main navigation"><a href="/">Home</a><a href="/individual-coaching/">Individual Coaching</a><a href="/couples-coaching/">Couples Coaching</a><a href="/free-guides/">Free Guides</a><a href="/about/">About</a><a href="/work-with-robert/">Work With Robert</a></nav>',
'<nav class="nav" aria-label="Main navigation"><a href="/">Home</a><a href="/courses/">Courses</a><a href="/work-with-robert/">Work With Robert</a><a href="/free/">Free Resources</a></nav>',
]
for path in ROOT.rglob('*.html'):
    if 'NOT USING' in path.parts or 'lead-magnets' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    original = text
    for old in old_navs:
        text = text.replace(old, NAV)
    text = text.replace('<a class="nav-cta" href="/#find-your-pattern">Find Your Pattern</a>', '<a class="nav-cta" href="/#find-your-pattern">Find Your Pattern</a>')
    text = text.replace('<div class="footer-links"><a href="/">Home</a><a href="/individual-coaching/">Individual Coaching</a><a href="/couples-coaching/">Couples Coaching</a><a href="/free-guides/">Free Guides</a><a href="/work-with-robert/">Work With Robert</a></div>', f'<div class="footer-links">{FOOTER_LINKS}</div>')
    text = text.replace('/assets/styles.css?v=20260706-humanized-pass', STYLE)
    if text != original:
        path.write_text(text, encoding='utf-8')
        print('updated', path.relative_to(ROOT))

# Add homepage bridge if missing.
index = ROOT / 'index.html'
text = index.read_text(encoding='utf-8')
needle = '    <section class="section dark-panel">\n      <p class="section-kicker">How coaching works</p>'
insert = '''    <section class="section split" id="relationship-help-guides">
      <div><p class="section-kicker">Relationship Help Guides</p><h2>Before you choose therapy, coaching, books, or another course, name what kind of help the pattern needs.</h2></div>
      <div class="stack"><p>Search-intent pages now give cold Google traffic a plain-English path into the business: relationship coach vs therapist, marriage coaching vs counseling, couples therapy alternatives, couples therapy not working, books, and attachment quizzes.</p><div class="pathway-actions"><a class="button primary" href="/relationship-help/">Explore Relationship Help Guides</a><a class="button secondary" href="/#find-your-pattern">Find Your Pattern</a></div></div>
    </section>

'''
if insert not in text:
    text = text.replace(needle, insert + needle)
    index.write_text(text, encoding='utf-8')
    print('added homepage bridge')
PYTHON_GENERATOR_COMMENT = 'done'
