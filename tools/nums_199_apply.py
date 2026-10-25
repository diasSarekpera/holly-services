#!/usr/bin/env python3
"""V199 : chiffres clés du site en Outfit (sans empattements), même famille que les sous-titres. Idempotent.
Concerne les statistiques, montants, pourcentages, faits chiffrés. Les numéros d'ordre (01, 02...) ne sont pas touchés."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
SEL = ['.about__stat-number', '.mission__img-kpi-num', '.stats__item-num', '.action-card__kpi-number',
       '.action-card__kpi-inline-number', '.camp-card__hero-pct', '.camp-card__raised', '.camp-card__days-left',
       '.camp-card__pct', '.camp-card__pct-overlay', '.soutenir__impact-num', '.partners__stat-num', '.post__impact-num',
       '.mission__figure-badge-number', '.stat-item__number', '.action-tile__stat-number', '.campagne-don__amount',
       '.mission-detail__fact-val', '.impact-stat__num', '.rapport-result-card__value', '.chiffre-card strong',
       '.funds-figure__value', '.rj-fact__value']
BLOCK = ('\n/* V199 Chiffres clés : Outfit sans empattements (même famille que les sous-titres) */\n'
         ':root:root:root body :is(' + ','.join(SEL) + '){font-family:var(--font-body);font-variant-numeric:lining-nums;letter-spacing:-0.01em}\n')
n = 0
for f in sorted((root / 'styles').glob('*.css')):
    t = f.read_text(encoding='utf-8')
    if 'V199' in t:
        new = re.sub(r'\n/\* V199[^\n]*\*/\n:root:root:root body :is\([^\n]*\)\{[^\n]*\}\n', lambda m: BLOCK, t)
        if new != t: f.write_text(new, encoding='utf-8'); n += 1
        continue
    # n'ajoute le bloc que si la feuille contient au moins un des sélecteurs visés
    if any(re.search(re.escape(s.split(' ')[0]) + r'[\s,{:.]', t) for s in SEL):
        f.write_text(t.rstrip('\n') + '\n' + BLOCK, encoding='utf-8'); n += 1
print('feuilles modifiées :', n)
