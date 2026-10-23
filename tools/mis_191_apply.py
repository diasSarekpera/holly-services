#!/usr/bin/env python3
"""V191 : Nos missions, cartes d'ancrage (Santé / Droits humains / Éducation) : chevron pour signaler qu'elles sont cliquables. Idempotent."""
import pathlib
css = pathlib.Path(__file__).resolve().parent.parent / 'styles' / 'nos-missions.css'
c = css.read_text(encoding='utf-8')
if 'V191' not in c:
    css.write_text(c.rstrip('\n') + '''

/* V191 Nos missions : chevron vers le bas à droite de chaque carte d'ancrage (elles font défiler vers la mission correspondante) */
.missions-anchors__link::after{content:'';flex:0 0 auto;width:8px;height:8px;margin-left:0.25rem;border-right:2px solid var(--clr-primary);border-bottom:2px solid var(--clr-primary);transform:translateY(-2px) rotate(45deg);transition:transform var(--dur-base) var(--ease-out)}
@media (hover:hover){.missions-anchors__link:hover::after{transform:translateY(1px) rotate(45deg)}}
@media (max-width:479px){
  .missions-anchors__link{justify-content:flex-start}
  .missions-anchors__link::after{margin-left:auto}
}
@media (prefers-reduced-motion:reduce){.missions-anchors__link::after{transition:none}}
''', encoding='utf-8')
print('ok')
