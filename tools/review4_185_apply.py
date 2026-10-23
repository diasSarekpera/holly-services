#!/usr/bin/env python3
"""V185 : À propos, « Ses objectifs déclarés couvrent quatre domaines : » mieux valorisé sur mobile. Idempotent."""
import pathlib
css = pathlib.Path(__file__).resolve().parent.parent / 'styles' / 'a-propos.css'
c = css.read_text(encoding='utf-8')
if 'V185' not in c:
    css.write_text(c.rstrip('\n') + '''

/* V185 À propos : petit titre des objectifs plus présent sur mobile */
@media (max-width:767px){
  .mission__objectives-intro{font-size:clamp(1.5rem,6.8vw,1.85rem);font-weight:600;line-height:1.2;letter-spacing:-0.005em;padding-left:1rem;border-left:3px solid var(--clr-primary);margin-bottom:1.5rem}
}
''', encoding='utf-8')
print('ok')
