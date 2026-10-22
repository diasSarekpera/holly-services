#!/usr/bin/env python3
"""V176 : AMOUSSOU François Xavier est le fondateur de l'ONG (confirmé par l'utilisateur). Idempotent.
Seul le titre est ajouté ; rien de privé (voir docs/INFOS-ONG.md, section Histoire)."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
OLD_ROLE = '<p class="team-card__role">Trésorier général et Coordonnateur chargé de la mission sanitaire</p>'
NEW_ROLE = '<p class="team-card__role">Fondateur, Trésorier général et Coordonnateur chargé de la mission sanitaire</p>'
OLD_ALT = 'alt="Portrait de AMOUSSOU François Xavier, Trésorier général et Coordonnateur chargé de la mission sanitaire"'
NEW_ALT = 'alt="Portrait de AMOUSSOU François Xavier, Fondateur, Trésorier général et Coordonnateur chargé de la mission sanitaire"'
n = 0
for p in (root/'index.html', root/'pages'/'a-propos.html'):
    s = p.read_text(encoding='utf-8')
    t = s.replace(OLD_ROLE, NEW_ROLE).replace(OLD_ALT, NEW_ALT)
    if t != s: p.write_text(t, encoding='utf-8'); n += 1
print('pages modifiées :', n)
