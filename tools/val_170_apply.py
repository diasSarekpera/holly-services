#!/usr/bin/env python3
"""V170 — section « Nos valeurs » (À propos) : de 4 cartes SaaS à une liste éditoriale.

Constat : 4 cartes blanches identiques, icône filaire centrée + titre + 2 lignes = motif « features »
d'un site tech, hors contexte pour une ONG internationale.
Après : liste à plat, alignée à gauche, sans boîte ni icône : filet en tête (court segment rose),
numéro en Cormorant, titre en serif, texte. Classe .value-card -> .value-item (plus une « carte » :
retirée de la recette T10 dans les 21 feuilles).
Usage : python3 tools/val_170_apply.py   (idempotent ; échoue bruyamment si une ancre manque)
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)

# ---------- 1) HTML ----------
VALUES = [("Humanité", "Nous plaçons la dignité humaine au centre de toutes nos interventions."),
          ("Intégrité", "Nous agissons avec transparence, honnêteté et responsabilité."),
          ("Solidarité", "Nous croyons en la force du collectif et en la cohésion sociale."),
          ("Durabilité", "Nous privilégions des solutions pérennes pour un impact à long terme.")]
items = "\n".join(
f"""          <li class="value-item">
            <span class="value-item__num" aria-hidden="true">{i:02d}</span>
            <h3 class="value-item__title">{t}</h3>
            <p class="value-item__desc">
              {d}
            </p>
          </li>
""" for i, (t, d) in enumerate(VALUES, 1))
new_ul = '<ul class="values__grid" role="list">\n\n' + items + '\n        </ul>'
h = open(P("pages", "a-propos.html"), encoding="utf-8").read()
if "value-card" in h:
    h2, n = re.subn(r'<ul class="values__grid" role="list">.*?</ul>', lambda m: new_ul, h, count=1, flags=re.S)
    assert n == 1, "bloc <ul class=values__grid> introuvable"
    open(P("pages", "a-propos.html"), "w", encoding="utf-8").write(h2)

# ---------- 2) CSS ----------
def sub1(s, old, new, name, f):
    assert s.count(old) == 1, f"{f}: ancre « {name} » trouvée {s.count(old)} fois (attendu 1)"
    return s.replace(old, new)

OLD_BASE = ".values__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.25rem;margin-top:3rem}.value-card{box-sizing:border-box;padding:1.5rem;display:flex;flex-direction:column;align-items:center;text-align:center;gap:1rem}.value-card__icon{width:3rem;height:3rem;display:flex;align-items:center;justify-content:center;color:var(--clr-accent)}.value-card__icon svg{width:100%;height:100%;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}.value-card__title{font-family:var(--font-display);font-size:var(--fs-h4);font-weight:500;color:var(--clr-secondary)}.value-card__desc{font-size:var(--fs-base-sm);line-height:1.7;color:var(--clr-text-soft)}"
NEW_BASE = (
 "/* Valeurs (V170) : liste éditoriale numérotée, sans boîte ni icône */"
 ".values__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:2.5rem;margin-top:3rem}"
 ".value-item{position:relative;padding-top:1.5rem;border-top:1px solid var(--clr-border-card);text-align:left}"
 ".value-item::before{content:'';position:absolute;top:-1px;left:0;width:3rem;height:3px;background:var(--clr-primary)}"
 ".value-item__num{display:block;margin-bottom:1.25rem;font-family:var(--font-display);font-size:clamp(2.75rem,3.2vw,3.5rem);font-weight:300;font-variant-numeric:lining-nums;line-height:1;letter-spacing:-0.02em;color:var(--clr-accent-dark)}"
 ".value-item__title{margin-bottom:0.625rem;font-family:var(--font-display);font-size:var(--fs-h3);font-weight:500;line-height:1.2;letter-spacing:var(--ls-tight);color:var(--clr-secondary)}"
 ".value-item__desc{font-size:var(--fs-body-sm);line-height:1.75;color:var(--clr-text-soft)}")
OLD_MOB = ".values__grid,.team__grid{grid-template-columns:minmax(0,1fr);gap:1rem}.value-card{padding:1.25rem}"
NEW_MOB = (".values__grid,.team__grid{grid-template-columns:minmax(0,1fr);gap:1rem}.values__grid{gap:0}"
 ".value-item{display:grid;grid-template-columns:3.25rem minmax(0,1fr);column-gap:1rem;padding:1.25rem 0 1.5rem}"
 ".value-item__num{grid-row:1 / span 2;margin:0;font-size:2.25rem}"
 ".value-item__title,.value-item__desc{grid-column:2}"
 ".value-item__title{font-size:var(--fs-h4)}")

TYPO = [(":root body .value-card__title,", ""), (":root body .value-card__desc,", "")]
CARDS = [(".value-card,\n", ""), (".value-card:hover,", "")]
MOBPAD = "  .value-card{padding-inline:1rem}\n"

total = 0
for p in sorted(glob.glob(P("styles", "*.css"))):
    f = os.path.basename(p); s = open(p, encoding="utf-8").read(); o = s
    for a, b in CARDS + TYPO:
        if a in s: s = sub1(s, a, b, a.strip(), f)
    if f == "a-propos.css":
        if OLD_BASE in s:
            s = sub1(s, OLD_BASE, NEW_BASE, "base valeurs", f)
            s = sub1(s, OLD_MOB, NEW_MOB, "mobile valeurs", f)
            s = sub1(s, MOBPAD, "", "padding mobile", f)
    if s != o: open(p, "w", encoding="utf-8").write(s); total += 1
left = [os.path.basename(p) for p in glob.glob(P("styles", "*.css")) if "value-card" in open(p, encoding="utf-8").read()]
print(f"{total} feuilles modifiées ; value-card restant dans : {left or 'aucune'}")

# ---------- 3) Outils de contrôle ----------
r = open(P("tools", "regress.py"), encoding="utf-8").read(); o = r
r = r.replace(".mission-detail__card,.value-card,.team-card", ".mission-detail__card,.team-card")
r = r.replace("querySelectorAll('.value-card')", "querySelectorAll('.value-item')")
if r != o: open(P("tools", "regress.py"), "w", encoding="utf-8").write(r)
t = open(P("tools", "cards_t10.py"), encoding="utf-8").read(); o = t
t = t.replace(" value-card ", " ")
if t != o: open(P("tools", "cards_t10.py"), "w", encoding="utf-8").write(t)
