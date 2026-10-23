#!/usr/bin/env python3
"""V192 : titres de cartes et petits titres harmonisés sur le style « Écouter avant d'agir » (Outfit 500, marche h4).
Idempotent. (1) marche h4 du bloc T7 : ajout de font-family:var(--font-body) dans toutes les feuilles.
(2) titres de cartes de la marche h3 passés en Outfit (taille inchangée). (3) titres sans classe des cartes de nos-missions,
partager-temoignage, rejoindre-equipe."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent / 'styles'
OLD = '{font-size:var(--fs-h4);font-weight:var(--fw-h4);line-height:var(--lh-h4);letter-spacing:var(--ls-h4)}'
NEW = '{font-family:var(--font-body);font-size:var(--fs-h4);font-weight:var(--fw-h4);line-height:var(--lh-h4);letter-spacing:var(--ls-h4)}'
EXTRA = ':root body .actualites-card__title,:root body .article-card__title,:root body .campagne-card__title,:root body .benevolat-mission-card__title{font-family:var(--font-body)}'
CARD = '{font-family:var(--font-body);font-size:var(--fs-h4);font-weight:var(--fw-h4);line-height:var(--lh-h4);letter-spacing:var(--ls-h4)}'
PAGE = {
 'nos-missions.css': ':root body .card-besoin h3,:root body .card-soutien h3' + CARD + '\n:root body .mission-text h3{font-family:var(--font-body);font-weight:var(--fw-h4)}',
 'partager-temoignage.css': ':root body .reason-card h3,:root body .temoignage-grid > div > h3' + CARD,
 'rejoindre-equipe.css': ':root body .why-card h3,:root body .job-info h3' + CARD,
}
n = 0
for f in sorted(root.glob('*.css')):
    c = f.read_text(encoding='utf-8')
    if 'V192' in c:
        continue
    lines = c.split('\n')
    for i, l in enumerate(lines):
        if l.startswith(':root body h4:not([class]),:root body h5,:root body h6') and l.endswith(OLD):
            lines[i] = l[:-len(OLD)] + NEW + '\n' + EXTRA
            break
    else:
        continue
    c = '\n'.join(lines).rstrip('\n') + '\n\n/* V192 titres de cartes et petits titres : style « Écouter avant d\'agir » (Outfit, marche h4) */\n'
    if f.name in PAGE:
        c += PAGE[f.name] + '\n'
    f.write_text(c, encoding='utf-8'); n += 1
print('feuilles modifiées :', n)
