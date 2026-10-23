#!/usr/bin/env python3
"""V181 : ancienneté d'engagement = 4+ ans (demande de l'utilisateur). Idempotent."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
R = {
 'index.html': [
  ('aria-label="9 années d\'engagement sur le terrain"', 'aria-label="4 années d\'engagement sur le terrain"'),
  ('<span class="about__stat-number" aria-hidden="true">9+</span>', '<span class="about__stat-number" aria-hidden="true">4+</span>'),
 ],
 'pages/actions.html': [('Depuis plus de 10 ans, Holly Services ONG agit', 'Depuis plus de 4 ans, Holly Services ONG agit')],
}
n = 0
for f, reps in R.items():
    p = root / f; s = p.read_text(encoding='utf-8'); t = s
    for a, b in reps: t = t.replace(a, b)
    if t != s: p.write_text(t, encoding='utf-8'); n += 1
print('pages modifiées :', n)
