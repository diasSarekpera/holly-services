#!/usr/bin/env python3
"""V175 : nombre de donateurs réel fourni par l'ONG = 22 (remplace « 1 200+ », fictif). Idempotent."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
REPL = [
  ('<span>1 200+ donateurs engagés</span>', '<span>22 donateurs engagés</span>'),
  ('<li>1 200+ donateurs engagés</li>', '<li>22 donateurs engagés</li>'),
  ('aria-label="Plus de 1 200 donateurs et bénévoles nous font confiance"', 'aria-label="22 donateurs nous font confiance"'),
  ('<strong>1 200+</strong> donateurs et bénévoles nous font confiance', '<strong>22</strong> donateurs nous font confiance'),
]
n = 0
for p in list(root.glob('*.html')) + list(root.glob('pages/*.html')):
    s = p.read_text(encoding='utf-8'); t = s
    for a, b in REPL: t = t.replace(a, b)
    if t != s: p.write_text(t, encoding='utf-8'); n += 1
print('pages modifiées :', n)
