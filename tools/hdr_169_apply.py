#!/usr/bin/env python3
"""V169 — header mobile distinct + voile vertical du hero d'accueil.

Constat : sous 768 px, header transparent + voile uniforme + fond du hero = le même bleu
(#10233F) -> rendu plat, photo effacée, logo et burger sans séparation.
1) 19 feuilles portant la navbar : bloc « Header mobile distinct (V169) » ajouté en fin de fichier.
2) home.css : l'aplat rgba(16,35,63,0.86) du voile mobile devient un dégradé vertical.
Usage : python3 tools/hdr_169_apply.py   (idempotent)
"""
import glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "/* ===== Header mobile distinct (V169) ====="
BLOCK = MARK + """
   Sous 768 px le header était transparent sur le même bleu que le hero : aucune séparation.
   Il devient un bandeau plein, plus profond (--clr-secondary-deep), avec un filet clair en bas
   (avant et après défilement) ; le burger gagne un fond et un contour plus lisibles.
   Bloc partagé identique dans les 19 feuilles qui portent la navbar. */
@media (max-width:767px){
.navbar,.navbar.is-scrolled{background-color:var(--clr-secondary-deep);border-bottom:1px solid var(--on-dark-line)}
.navbar::before{display:none}
.navbar__hamburger{background:rgba(255,255,255,0.14);border-color:var(--on-dark-border)}
}
"""
OLD = "@media (max-width:767px){.hero__overlay--left{background:rgba(16,35,63,0.86)}}"
NEW = ("@media (max-width:767px){.hero__overlay--left{background:linear-gradient(to bottom,"
       "rgba(16,35,63,0.50) 0%,rgba(16,35,63,0.74) 30%,rgba(16,35,63,0.86) 60%,rgba(16,35,63,0.94) 100%)}}")
n = 0
for p in sorted(glob.glob(os.path.join(ROOT, "styles", "*.css"))):
    s = open(p, encoding="utf-8").read(); o = s
    if "navbar__hamburger" in s and MARK not in s:
        s = s.rstrip("\n") + "\n\n" + BLOCK; n += 1
    if os.path.basename(p) == "home.css":
        s = s.replace("voile mobile uniforme et soutenu", "voile mobile soutenu (dégradé vertical depuis V169)")
        s = s.replace(OLD, NEW)
    if s != o: open(p, "w", encoding="utf-8").write(s)
print(f"{n} feuilles ont reçu le bloc header ; voile hero :", "OK" if NEW in open(os.path.join(ROOT,'styles','home.css'),encoding='utf-8').read() else "KO")
