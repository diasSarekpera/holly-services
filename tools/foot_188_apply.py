#!/usr/bin/env python3
"""V188 : pied de page mobile, liens légaux (Mentions / Confidentialité / Conditions) moins espacés. Idempotent.
Le pied de page est dupliqué dans chaque feuille : on ajoute le même bloc à chacune."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent / 'styles'
BLOCK = '''

/* V188 Pied de page mobile : liens légaux empilés moins espacés (zone de toucher 44 px -> 36 px, au-dessus du minimum WCAG 2.2 de 24 px) */
@media (max-width:640px){
  .footer__bottom-inner{gap:0.75rem}
  .footer__bottom-links .footer__bottom-link{min-height:36px}
}
'''
n = 0
for f in sorted(root.glob('*.css')):
    c = f.read_text(encoding='utf-8')
    if 'footer__bottom-link' in c and 'V188' not in c:
        f.write_text(c.rstrip('\n') + BLOCK, encoding='utf-8'); n += 1
print('modifiés :', n)
