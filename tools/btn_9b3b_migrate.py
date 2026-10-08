"""T9B3b - boutons du footer -> systeme .btn. Usage : python3 tools/btn_9b3b_migrate.py"""
import re, glob, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from css_rules import rules

HTML = [
 ('class="footer__mission-cta footer__mission-cta--ghost"', 'class="btn btn--ghost-light"'),
 ('class="footer__mission-cta"', 'class="btn btn--primary"'),
 ('class="footer__nl-btn"', 'class="btn btn--primary btn--sm"'),
]
for f in glob.glob('**/*.html', recursive=True):
    s = open(f, encoding='utf8').read(); o = s
    for a, b in HTML: s = s.replace(a, b)
    if s != o: open(f, 'w', encoding='utf8').write(s)

DEL = re.compile(r'(?<![\w-])\.(footer__mission-cta|footer__nl-btn)(--ghost)?(:hover)?(\s+svg(\s+polygon)?|\s+svg:not\(\.footer__cta-arrow\))?(\s+\.footer__cta-arrow)?$')
def should_delete(sel):
    parts = [p.strip() for p in sel.split(',')]
    return all(DEL.match(p) or p.startswith('.footer__mission-cta svg:not') or p.startswith('.footer__nl-btn svg')
               or p.startswith('.footer__mission-cta:hover') for p in parts)

LOCAL = ('\n/* Footer CTA (T9B3b) */\n'
         '.footer__nl-form .btn{flex-shrink:0;width:44px;padding:0;align-self:stretch;border-radius:0;box-shadow:none}\n'
         '.footer__nl-form .btn:hover{box-shadow:none}\n'
         '@media (max-width:640px){.footer__mission-right .btn{width:100%}}\n')

for f in sorted(glob.glob('styles/*.css')):
    s = open(f, encoding='utf8').read()
    if 'footer__mission-cta' not in s and 'footer__nl-btn' not in s: continue
    s2 = re.sub(r'/\*.*?\*/', lambda m: ' ' * len(m.group(0)), s, flags=re.S)
    cuts = []
    for med, sel, body, st, en in rules(s):
        if not should_delete(sel): continue
        ss = st + (len(s2[st:en]) - len(s2[st:en].lstrip()))
        cuts.append((ss, en))
    for ss, en in sorted(cuts, reverse=True):
        if s[en:en+1] == '\n': en += 1
        s = s[:ss] + s[en:]
    # selecteurs partages : reduced-motion et focus-visible
    s = s.replace('.footer__mission-cta:focus-visible,.footer__nl-btn:focus-visible,', '.footer .btn:focus-visible,')
    s = s.replace('.footer__mission-cta,.footer__social,', '.footer .btn,.footer__social,')
    s = re.sub(r'@media[^{}]*\{\s*\}\n?', '', s)
    s = s.rstrip('\n') + '\n' + LOCAL
    open(f, 'w', encoding='utf8').write(s)
