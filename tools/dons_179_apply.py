#!/usr/bin/env python3
"""V179 : moyens de don acceptés (réponse de l'ONG) : tous (Mobile Money, espèces, virement) ;
compte bancaire pas encore disponible. Complète le bloc V177. Idempotent."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = root / 'index.html'; s = p.read_text(encoding='utf-8')
if 'soutenir__momo-note' in s:
    print('déjà appliqué'); raise SystemExit
end = '''                </ul>
              </div>'''
anchor = s.index('soutenir__momo-list')
i = s.index(end, anchor)
NEW = '''                </ul>
                <p class="soutenir__momo-note"><strong>Espèces&nbsp;:</strong> les dons en espèces sont acceptés, <a href="#contact">contactez-nous</a> pour convenir de la remise.</p>
                <p class="soutenir__momo-note"><strong>Virement bancaire&nbsp;:</strong> bientôt disponible, notre compte est en cours d'ouverture.</p>
              </div>'''
p.write_text(s[:i] + NEW + s[i+len(end):], encoding='utf-8')
css = root / 'styles' / 'home.css'
css.write_text(css.read_text(encoding='utf-8').rstrip('\n') + '''

/* Autres moyens de don : espèces, virement (V179) */
.soutenir__momo-note{font-size:var(--fs-base-sm);line-height:1.55;color:var(--clr-text-soft)}
.soutenir__momo-note strong{color:var(--clr-text);font-weight:600}
.soutenir__momo-note a{color:var(--clr-primary);text-decoration:underline;text-underline-offset:2px}
''', encoding='utf-8')
print('appliqué')
