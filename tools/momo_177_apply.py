#!/usr/bin/env python3
"""V177 : dons par dépôt sur numéros mobile (réponse de l'ONG). Idempotent.
Carte « Faire un don » de l'accueil : montants en euros + bouton vers maintenance.html
remplacés par les deux numéros fournis."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = root / 'index.html'
s = p.read_text(encoding='utf-8')
if 'soutenir__momo' in s:
    print('déjà appliqué'); raise SystemExit
a = s.index('<!--\n                Le clic sur "Faire un don maintenant"')
b = s.index('Faire un don maintenant</span>', a)
b = s.index('</a>', b) + len('</a>')
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
NEW = f'''<div class="soutenir__momo" role="group" aria-label="Faire un don par dépôt sur numéro mobile">
                <p class="soutenir__momo-label">Don par dépôt sur numéro mobile</p>
                <ul class="soutenir__momo-list" role="list">
                  <li class="soutenir__momo-item">
                    <span class="soutenir__momo-icon" aria-hidden="true">{PHONE}</span>
                    <span class="soutenir__momo-num">+229 01 91 29 85 85</span>
                  </li>
                  <li class="soutenir__momo-item">
                    <span class="soutenir__momo-icon" aria-hidden="true">{PHONE}</span>
                    <span class="soutenir__momo-num">+229 01 92 45 45 60</span>
                  </li>
                </ul>
              </div>'''
p.write_text(s[:a] + NEW + s[b:], encoding='utf-8')
css = root / 'styles' / 'home.css'
c = css.read_text(encoding='utf-8')
c = c.rstrip('\n') + '''

/* Don par dépôt sur numéro mobile (V177) */
.soutenir__momo{display:flex;flex-direction:column;gap:0.625rem;margin-top:0.25rem}
.soutenir__momo-label{font-size:var(--fs-xs);font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--clr-text-soft)}
.soutenir__momo-list{display:flex;flex-direction:column;gap:0.5rem;list-style:none;margin:0;padding:0}
.soutenir__momo-item{display:flex;align-items:center;gap:0.75rem;padding:0.7rem 0.9rem;border:1.5px solid var(--clr-border-strong);border-radius:var(--radius-md);background:var(--clr-white)}
.soutenir__momo-icon{display:inline-flex;flex:0 0 auto}
.soutenir__momo-icon svg{width:1.1rem;height:1.1rem;stroke:var(--clr-primary);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.soutenir__momo-num{font-size:var(--fs-base-sm);font-weight:600;color:var(--clr-text);letter-spacing:0.02em;white-space:nowrap;user-select:all}
'''
css.write_text(c, encoding='utf-8')
print('appliqué')
