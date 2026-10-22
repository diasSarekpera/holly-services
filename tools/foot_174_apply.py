#!/usr/bin/env python3
"""V174 : pied de page, « ONG » au-dessus de « Holly Services » (idempotent)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
pat = re.compile(
    r'(?P<i>[ \t]*)<span class="footer__logo-name">Holly Services</span>\s*\n'
    r'[ \t]*<span class="footer__logo-tag">ONG Internationale</span>')
rep = lambda m: (f'{m["i"]}<span class="footer__logo-tag">ONG</span>\n'
                 f'{m["i"]}<span class="footer__logo-name">Holly Services</span>')
CSS = ('\n/* Pied de page : ONG au-dessus du nom (V174) */\n'
       '.footer__logo-tag{margin-top:0;margin-bottom:0.25rem;line-height:1}\n')
h = c = 0
for p in list(root.glob('*.html')) + list(root.glob('pages/*.html')):
    s = p.read_text(encoding='utf-8'); n = pat.sub(rep, s)
    if n != s: p.write_text(n, encoding='utf-8'); h += 1
for p in root.glob('styles/*.css'):
    s = p.read_text(encoding='utf-8')
    if '.footer__logo-tag' in s and 'V174' not in s:
        p.write_text(s.rstrip('\n') + '\n' + CSS, encoding='utf-8'); c += 1
print(f'HTML : {h} | CSS : {c}')
