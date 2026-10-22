#!/usr/bin/env python3
"""V171 : header, « ONG » au-dessus de « Holly Services » (idempotent).

- HTML (19 pages) : <span class="navbar__brand-sub">ONG Internationale</span>
  placé sous le nom -> <span class="navbar__brand-sub">ONG</span> placé AVANT le nom.
- CSS (19 feuilles) : retrait de `.navbar__brand-sub{display:none}` (≤ 479 px) :
  « ONG » est court, il reste visible sur mobile.
Le pied de page (.footer__logo-tag) n'est pas touché.
"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
pat = re.compile(
    r'(?P<i>[ \t]*)<strong class="navbar__brand-name">Holly Services</strong>\s*\n'
    r'[ \t]*<span class="navbar__brand-sub">ONG Internationale</span>')
html_n = css_n = 0
for p in list(root.glob('*.html')) + list(root.glob('pages/*.html')):
    s = p.read_text(encoding='utf-8')
    n = pat.sub(lambda m: f'{m["i"]}<span class="navbar__brand-sub">ONG</span>\n'
                          f'{m["i"]}<strong class="navbar__brand-name">Holly Services</strong>', s)
    if n != s:
        p.write_text(n, encoding='utf-8'); html_n += 1
for p in root.glob('styles/*.css'):
    s = p.read_text(encoding='utf-8')
    n = s.replace('.navbar__brand-sub{display:none}', '')
    if n != s:
        p.write_text(n, encoding='utf-8'); css_n += 1
print(f'HTML modifiés : {html_n} | CSS modifiés : {css_n}')
