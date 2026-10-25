#!/usr/bin/env python3
"""V202 : filtres d'actualités responsive (mobile) : grille régulière au lieu de pastilles en vrac. Idempotent."""
import pathlib, re
CSS = pathlib.Path(__file__).resolve().parent.parent / 'styles/actualites.css'
MARK = '/* V202 Filtres d\'actualités'
BLOCK = '''
/* V202 Filtres d'actualités : grille régulière sur mobile (libellé à gauche, compteur à droite) */
@media (max-width:767px){
.actualites-toolbar__filters{display:grid;width:100%;grid-template-columns:repeat(3,minmax(0,1fr));gap:0.5rem}
.actualites-filter{display:flex;align-items:center;justify-content:space-between;gap:0.375rem;width:100%;min-width:0;padding-inline:0.875rem;text-align:left;line-height:1.25}
.actualites-filter [data-filter-count]{flex-shrink:0;margin-left:0}
.actualites-filter[data-filter="tous"]{grid-column:1 / -1}
}
@media (max-width:519px){
.actualites-toolbar__filters{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:359px){
.actualites-filter{padding-inline:0.75rem;font-size:var(--fs-sm)}
}
'''
c = CSS.read_text(encoding='utf-8')
if MARK in c:
    c = c[:c.index('\n' + MARK)] + '\n' + BLOCK.lstrip('\n') if False else re.sub(r"\n/\* V202 Filtres d'actualités.*\Z", BLOCK, c, flags=re.S)
else:
    c = c.rstrip('\n') + '\n' + BLOCK
CSS.write_text(c, encoding='utf-8')
print('ok')
