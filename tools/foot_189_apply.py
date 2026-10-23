#!/usr/bin/env python3
"""V189 : pied de page mobile, autres liens (Navigation, Nous soutenir, Contact, liens légaux de la colonne contact) moins espacés. Idempotent."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent / 'styles'
BLOCK = '''

/* V189 Pied de page mobile : mêmes espacements resserrés pour Navigation, Nous soutenir, Contact et les liens légaux de la colonne contact */
@media (max-width:640px){
  .footer__nav-link{min-height:36px}
  .footer__support-list{gap:0.25rem}
  .footer__support-item{min-height:0;padding-block:0.125rem}
  .footer__contact-list{gap:0.25rem}
  .footer__contact-item{min-height:40px}
  .footer__legal-link{min-height:36px}
}
'''
n = 0
for f in sorted(root.glob('*.css')):
    c = f.read_text(encoding='utf-8')
    if 'V188' in c and 'V189' not in c:
        f.write_text(c.rstrip('\n') + BLOCK, encoding='utf-8'); n += 1
print('modifiés :', n)
