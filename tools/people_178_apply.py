#!/usr/bin/env python3
"""V178 : personnes aidées depuis la création (réponse de l'ONG) : 342 personnes albinos + 383 autres = 725.
Remplace les chiffres fictifs de bénéficiaires. Idempotent (remplacements exacts)."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
NB = '\u00a0'
R = {
 'index.html': [
  ('aria-label="500 enfants accompagnés"', 'aria-label="342 personnes albinos accompagnées"'),
  ('<span class="mission__img-kpi-num" aria-hidden="true">500+</span>', '<span class="mission__img-kpi-num" aria-hidden="true">342</span>'),
  ('<span class="mission__img-kpi-lbl" aria-hidden="true">enfants accompagnés</span>', '<span class="mission__img-kpi-lbl" aria-hidden="true">personnes albinos accompagnées</span>'),
  ('<span class="soutenir__impact-num">5 000+</span>', '<span class="soutenir__impact-num">725</span>'),
  ('<span class="soutenir__impact-lbl">bénéficiaires soutenus grâce à vos dons</span>', '<span class="soutenir__impact-lbl">personnes aidées depuis la création</span>'),
 ],
 'pages/nos-missions.html': [
  ('1 024 enfants accompagnés</li>', '342 personnes albinos accompagnées</li>'),
  ('<span class="impact-stat__num">1&nbsp;024</span>', '<span class="impact-stat__num">342</span>'),
  ('<span class="impact-stat__label">Enfants accompagnés</span>', '<span class="impact-stat__label">Personnes albinos accompagnées</span>'),
 ],
 'pages/transparence-rapports.html': [
  (f'<strong>1{NB}024</strong>\n            <p>Enfants accompagnés</p>\n            <span>jan. \u2013 juin 2025</span>',
   '<strong>342</strong>\n            <p>Personnes albinos accompagnées</p>\n            <span>Depuis la création</span>'),
 ],
 'pages/actions.html': [
  ('<span class="stat-item__number">250K+</span>', '<span class="stat-item__number">725</span>'),
 ],
 'pages/a-propos.html': [
  ('<span class="mission__figure-badge-number">85 000+</span>\n                <span class="mission__figure-badge-label">Vies transformées</span>',
   '<span class="mission__figure-badge-number">725</span>\n                <span class="mission__figure-badge-label">Personnes aidées</span>'),
 ],
}
tot = 0
for f, reps in R.items():
    p = root / f; s = p.read_text(encoding='utf-8'); t = s
    for a, b in reps: t = t.replace(a, b)
    if t != s: p.write_text(t, encoding='utf-8'); tot += 1
print('pages modifiées :', tot)
