#!/usr/bin/env python3
"""V183 : relecture exigeante de l'accueil (2/n) : fin de l'effet « verre » sur Contact et footer. Idempotent.
Fonds translucides (blanc 6-7 %, overlays) remplacés par des fonds pleins."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
CONTACT = '''
/* V183 Contact : pastilles d'icônes et carte d'engagement en fonds pleins (fin de l'effet verre) */
.contact__detail-icon{background:#1B3355;border-color:#2D4B76}
.contact__commitment{background:#1A3047;border-color:#34564F}
.contact__commitment-icon{background:#2A4B47}
'''
FOOTER = '''
/* V183 Footer : pastilles d'icônes en fonds pleins (fin de l'effet verre) */
.footer__social,.footer__contact-icon{background:#1B3355;border-color:#2D4B76}
@media (hover:hover){.footer__social:hover{background:#264670;border-color:#3A5F94}}
.footer__social:active{background:#2A4B47}
.footer__support-icon--donate{background:#3A1B3B}
.footer__support-icon--volunteer{background:#22403A}
.footer__support-icon--partner{background:#1D3A63}
.footer__support-icon--campagne{background:#22403A}
'''
n = {'contact': 0, 'footer': 0}
for p in root.glob('styles/*.css'):
    s = p.read_text(encoding='utf-8'); t = s
    if p.name == 'home.css' and 'V183 Contact' not in t:
        t = t.rstrip('\n') + '\n' + CONTACT; n['contact'] += 1
    if '.footer__contact-icon{' in t and 'V183 Footer' not in t:
        t = t.rstrip('\n') + '\n' + FOOTER; n['footer'] += 1
    if t != s: p.write_text(t, encoding='utf-8')
print(n)
