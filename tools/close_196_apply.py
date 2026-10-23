#!/usr/bin/env python3
"""V196 : bouton de fermeture du menu mobile aligné sur le bouton burger.
Avant : 44 px, croix 18 px, trait 1,75 px à 65 % d'opacité, bordure #2D4B76.
Après : 48 px (comme le burger), croix de même étendue que la croix du burger ouvert
(barres de 26 px, soit 18,4 px de côté), trait 2,5 px à 95 %, même bordure #35588A.
Idempotent."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
CSS = '''
/* Bouton de fermeture du menu mobile = même gabarit que le burger (V196) */
.mobile-menu__close{width:48px;height:48px;border-color:#35588A}
.mobile-menu__close svg{width:36.77px;height:36.77px;overflow:visible;stroke:rgba(255,255,255,0.95);stroke-width:2.5px}
.mobile-menu__close svg line{vector-effect:non-scaling-stroke}
'''
c = 0
for p in root.glob('styles/*.css'):
    s = p.read_text(encoding='utf-8')
    if '.mobile-menu__close{width:44px' in s and 'V196' not in s:
        p.write_text(s.rstrip('\n') + '\n' + CSS, encoding='utf-8'); c += 1
print(f'CSS : {c}')
