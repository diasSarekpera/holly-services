#!/usr/bin/env python3
"""V187 : À propos, « Notre approche » (ordre + sous-titres mobile) et badges de certification mobile. Idempotent."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
css = root / 'styles' / 'a-propos.css'
c = css.read_text(encoding='utf-8')
if 'V187' not in c:
    css.write_text(c.rstrip('\n') + '''

/* V187 À propos · Notre approche : sur mobile / tablette (blocs empilés), ordre identique pour les deux blocs : image, titre, texte, bouton */
@media (max-width:900px){
  .approach__block .approach__figure{order:-1}
}
/* V187 À propos · Notre approche : sous-titres plus présents sur mobile (taille, graisse, repère rose) */
@media (max-width:767px){
  :root body .approach__title{position:relative;padding-top:1.1rem;font-size:clamp(1.625rem,7.2vw,2rem);font-weight:600;line-height:1.15;letter-spacing:-0.01em}
  :root body .approach__title::before{content:'';position:absolute;top:0;left:0;width:3rem;height:3px;background:var(--clr-primary)}
  :root body .approach__title-accent{font-weight:600}
}
/* V187 À propos · Certifications : sur mobile, cases empilées de même largeur (avant : largeurs irrégulières selon le texte) */
@media (max-width:767px){
  .partners-certif__badges{display:grid;grid-template-columns:minmax(0,1fr);width:100%;max-width:26rem;margin-inline:auto;gap:0.75rem}
  .partners-certif__badges .badge{min-width:0;width:100%}
}
''', encoding='utf-8')
print('ok')
