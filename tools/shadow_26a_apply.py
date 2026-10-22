#!/usr/bin/env python3
"""V156 — ombres adoucies (site institutionnel : pas d'effet « SaaS »).

Principe : une ombre sert à séparer un élément du fond (en-tête fixe, menu déroulant),
jamais à le faire « flotter » ou « briller ». Cartes (bloc T10) et anneaux de focus inchangés.
Usage : python3 tools/shadow_26a_apply.py   (idempotent : les anciennes valeurs disparaissent)
"""
import glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = [
 # en-tête fixe après défilement : filet d'ombre discret au lieu d'un halo de 24 px
 ("0 8px 24px -6px rgba(5,12,24,0.60),0 2px 6px rgba(5,12,24,0.35)", "0 2px 6px rgba(5,12,24,0.16)"),
 # menu déroulant du header
 ("0 4px 16px rgba(5,12,24,0.32),0 1px 4px rgba(5,12,24,0.20)", "0 3px 10px rgba(5,12,24,0.22)"),
 # médaillon du logo (navbar)
 ("0 4px 14px rgba(5,12,24,0.28)", "0 1px 3px rgba(5,12,24,0.18)"),
 # bouton principal : à plat (la couleur seule change au survol), plus de halo rose
 ("box-shadow:0 2px 8px var(--clr-primary-overlay)", "box-shadow:none"),
 ("box-shadow:0 4px 14px rgba(194,24,91,0.18)", "box-shadow:none"),
 # grande ombre « carte flottante » de Rejoindre l'équipe -> ombre de carte standard
 ("0 20px 44px -22px rgba(16,35,63,0.35)", "var(--shadow-card)"),
 # tokens
 ("--shadow-lg:0 4px 16px rgba(16,35,63,0.07)", "--shadow-lg:0 2px 8px rgba(16,35,63,0.06)"),
 ("--shadow-popover:0 8px 24px -6px rgba(5,12,24,0.45)", "--shadow-popover:0 3px 10px rgba(5,12,24,0.22)"),
 # chiffre sur photo (Accueil, mobile) : lisibilité conservée, halo réduit
 ("0 1px 8px rgba(0,0,0,0.45)", "0 1px 3px rgba(0,0,0,0.40)"),
 # pilier « À propos » mobile -> ombre de carte standard
 ("box-shadow:0 2px 8px rgba(16,35,63,0.06)", "box-shadow:var(--shadow-card)"),
]
tot = {}
for p in sorted(glob.glob(os.path.join(ROOT, "styles", "*.css"))):
    s = open(p, encoding="utf-8").read(); o = s
    for a, b in R:
        n = s.count(a)
        if n: tot[a] = tot.get(a, 0) + n; s = s.replace(a, b)
    if s != o: open(p, "w", encoding="utf-8").write(s)
for a, b in R: print(f"{tot.get(a,0):3d}  {a[:62]}  ->  {b[:40]}")
