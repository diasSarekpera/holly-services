#!/usr/bin/env python3
"""V200 : eyebrows trop longs (retour à la ligne sur mobile) remplacés par des libellés courts. Idempotent."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
NB = '\u00a0'
CHANGES = {
    'pages/nos-missions.html': [
        ("Des résultats concrets, vérifiés et transparents.", "Résultats vérifiés"),
        ("Nos missions · Notre raison d'agir", "Notre raison d'agir"),
    ],
    'pages/transparence-rapports.html': [
        ("Des chiffres, leurs périodes et leurs définitions", "Chiffres et définitions"),
        ("Transparence et redevabilité", "Transparence"),
        ("Un document introuvable ?", "Document introuvable\u00a0?"),
    ],
    'pages/rejoindre-equipe.html': [
        ("Des métiers au service de la mission", "Nos métiers"),
        ("Postulez en quelques minutes", "Candidature"),
    ],
    'pages/a-propos.html': [("Notre mission &amp; notre histoire", "Notre histoire")],
    'pages/actualites.html': [("Actualités et engagements", "Actualités")],
    'index.html': [("Actualités &amp; Engagements", "Actualités")],
}
n = 0
for rel, pairs in CHANGES.items():
    p = ROOT / rel
    t = p.read_text(encoding='utf-8')
    for old, new in pairs:
        o = f'<span class="eyebrow__label">{old}</span>'
        w = f'<span class="eyebrow__label">{new}</span>'
        if o in t:
            t = t.replace(o, w); n += 1
        elif w not in t:
            print('INTROUVABLE', rel, old, file=sys.stderr)
    p.write_text(t, encoding='utf-8')
print(n, 'eyebrow(s) raccourci(s)')
