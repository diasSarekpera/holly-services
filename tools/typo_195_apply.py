#!/usr/bin/env python3
"""V195 : règle typographique. Grands titres (h1, h2 de section) = Cormorant Garamond ; tous les titres secondaires
(h3-h6, titres de cartes/blocs, intitulés) = Outfit sans empattements. Idempotent. Bloc ajouté en fin des feuilles du bloc T7."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent / 'styles'
SEL = ','.join(':root body ' + s for s in [
 'h3','h4','h5','h6',
 'h2.article-cta__title','h2.contact-form__title','h2.legal-section__title',
 '.erreur404-sitemap__toggle','.cta-card__title','.mission__objectives-intro','.legal-toc__title',
 '.approach__title','.camp-card__title','.contact__form-title','.mission__title','.partenariats-why__title',
 '.soutenir__right-title','.transp-h3','.value-item__title'])
BLOCK = ('\n\n/* V195 règle typographique : grands titres en Cormorant Garamond, titres secondaires en Outfit */\n'
         + SEL + '{font-family:var(--font-body)}\n'
         ':root body .approach__title-accent{font-style:normal}\n')
n = 0
for f in sorted(root.glob('*.css')):
    c = f.read_text(encoding='utf-8')
    if 'V195 règle typographique' in c or ':root body h4:not([class]),:root body h5' not in c:
        continue
    f.write_text(c.rstrip('\n') + BLOCK, encoding='utf-8'); n += 1
print('feuilles modifiées :', n)
