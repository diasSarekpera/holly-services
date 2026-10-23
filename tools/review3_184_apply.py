#!/usr/bin/env python3
"""V184 : fin de l'effet « verre » sur les boutons du header / menu mobile. Idempotent.
Burger, bouton fermer, sélecteur de langue (menu mobile + navbar) : fonds pleins."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
CSS = '''
/* V184 Header et menu mobile : boutons en fonds pleins (fin de l'effet verre) */
.navbar__hamburger{background:#1B3355;border-color:#35588A}
.mobile-menu__close{background:#1B3355;border-color:#2D4B76}
.mobile-menu__lang{background:#1B3355;border-color:#2D4B76;color:#C3CFE1}
.navbar__lang{background:#1B3355;border-color:#2D4B76}
@media (hover:hover){
  .navbar__hamburger:hover,.mobile-menu__close:hover,.mobile-menu__lang:hover,.navbar__lang:hover{background:#264670}
  .mobile-menu__lang:hover{color:#EAF0F8}
}
'''
n = 0
for p in root.glob('styles/*.css'):
    s = p.read_text(encoding='utf-8')
    if '.navbar__hamburger{' in s and 'V184' not in s:
        p.write_text(s.rstrip('\n') + '\n' + CSS, encoding='utf-8'); n += 1
print('feuilles modifiées :', n)
