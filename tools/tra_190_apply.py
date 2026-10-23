#!/usr/bin/env python3
"""V190 : Transparence, ligne de faits (94 % / Audit / Depuis 2018 / 22 donateurs) en vrac sur mobile. Idempotent."""
import pathlib
css = pathlib.Path(__file__).resolve().parent.parent / 'styles' / 'transparence-rapports.css'
c = css.read_text(encoding='utf-8')
if 'V190' not in c:
    css.write_text(c.rstrip('\n') + '''

/* V190 Transparence : sur mobile / tablette, les 4 faits passent en liste verticale alignée (avant : séparateurs « · » orphelins en début de ligne, retours à la ligne irréguliers) */
@media (max-width:900px){
  .transparence-intro__facts{display:grid;grid-template-columns:minmax(0,1fr);gap:0.75rem}
  .transparence-intro__facts li{display:flex;align-items:center;gap:0.75rem;line-height:1.4}
  .transparence-intro__facts li::before,.transparence-intro__facts li+li::before{content:'';flex:0 0 auto;width:6px;height:6px;margin:0;border-radius:50%;background:var(--clr-primary)}
}
''', encoding='utf-8')
print('ok')
