#!/usr/bin/env python3
"""V172 : menu mobile, « ONG » au-dessus de « Holly Services » (idempotent)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
pat = re.compile(r'(?P<i>[ 	]*)<span class="mobile-menu__brand-name">Holly Services</span>')
def rep(m):
    i = m['i']
    return (f'{i}<div class="mobile-menu__brand-text">\n'
            f'{i}  <span class="mobile-menu__brand-sub">ONG</span>\n'
            f'{i}  <span class="mobile-menu__brand-name">Holly Services</span>\n'
            f'{i}</div>')
CSS = ('\n/* Menu mobile : ONG au-dessus du nom (V172) */\n'
       '.mobile-menu__brand-text{display:flex;flex-direction:column;gap:0.25rem}\n'
       '.mobile-menu__brand-sub{font-size:var(--fs-xs);font-weight:500;letter-spacing:0.16em;'
       'text-transform:uppercase;line-height:var(--lh-none);'
       'color:color-mix(in srgb,var(--clr-accent) 80%,var(--clr-white))}\n')
h = c = 0
for p in list(root.glob('*.html')) + list(root.glob('pages/*.html')):
    s = p.read_text(encoding='utf-8')
    if 'mobile-menu__brand-text' in s: continue  # déjà appliqué
    n = pat.sub(rep, s)
    if n != s: p.write_text(n, encoding='utf-8'); h += 1
for p in root.glob('styles/*.css'):
    s = p.read_text(encoding='utf-8')
    if '.mobile-menu__brand-name' in s and 'mobile-menu__brand-sub' not in s:
        p.write_text(s.rstrip('\n') + '\n' + CSS, encoding='utf-8'); c += 1
print(f'HTML : {h} | CSS : {c}')
