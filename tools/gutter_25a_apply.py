#!/usr/bin/env python3
"""V155 — gouttière latérale mobile unique (--page-gutter).

Constat : sur mobile, la marge latérale du site variait de 16 px (sections de
l'accueil) à 20 px (navbar, hero, footer, menu) et 24 px (pages intérieures),
parfois 32 px (Actions, Article) : trop serré et incohérent.

Correction :
  1. Tokens (:root, identiques dans les 19 feuilles qui portent le :root) :
     --page-gutter = 2rem (>= 768 px) ; clamp(1.5rem, 0.05rem + 7.25vw, 2rem)
     sous 768 px (24 px à 320 px, ~28 px à 375 px, 32 px des 430 px).
     --section-pad-x et --container-pad (<= 1023 px) pointent dessus.
  2. Bloc « Gouttière mobile (V155) » ajouté en fin de feuille : zones qui
     avaient leur propre valeur en dur (navbar, menu mobile, footer, bouton
     retour en haut) = bloc partagé identique ; blocs propres à une page pour
     les conteneurs qui ne lui appartiennent qu'à elle.

Usage : python3 tools/gutter_25a_apply.py [--check]
Idempotent : le bloc existant est remplacé, les tokens ne sont réécrits qu'une fois.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES = os.path.join(ROOT, "styles")
MARK = "/* ===== Gouttière mobile (V155)"

GUTTER_MOBILE = "clamp(1.5rem,0.05rem + 7.25vw,2rem)"

# (ancien, nouveau) : chaque ancien motif doit exister exactement une fois.
TOKENS = [
    ("--container-pad:1.5rem;--gutter:2rem;",
     "--page-gutter:2rem;--container-pad:1.5rem;--gutter:2rem;"),
    ("--section-pad-x:2rem;", "--section-pad-x:var(--page-gutter);"),
    ("@media (max-width:1023px){:root{--section-footer-gap:2.5rem;--gutter:1.5rem}}",
     "@media (max-width:1023px){:root{--section-footer-gap:2.5rem;--gutter:1.5rem;--container-pad:var(--page-gutter)}}"),
    ("--section-pad-x:1.25rem;", "--page-gutter:" + GUTTER_MOBILE + ";"),
    ("@media (max-width:479px){:root{--section-pad-x:1rem}}", ""),
]

SHARED = """@media (max-width:767px){
.navbar{padding-inline:var(--page-gutter)}
.mobile-menu__head,.mobile-menu__nav,.mobile-menu__foot{padding-inline:var(--page-gutter)}
.footer__mission-inner,.footer__inner,.footer__certs-inner,.footer__bottom-inner{padding-inline:var(--page-gutter)}
.back-to-top{right:var(--page-gutter)}
}
"""

PAGE = {
    "home": """@media (max-width:767px){
.hero__content,.soutenir__left,.soutenir__right,.contact__info,.contact__form-wrap{padding-inline:var(--page-gutter)}
.about__pillars,.actions__filter-row,.soutenir__impact-scroller,.soutenir__way{margin-inline:calc(var(--page-gutter) * -1);padding-inline:var(--page-gutter)}
.about__pillars,.soutenir__impact-scroller{scroll-padding-inline:var(--page-gutter)}
.about__stat-card{left:var(--page-gutter)}
.partners__flagship{margin-inline:0}
}
""",
    "a-propos": """@media (max-width:767px){
.mission__container,.values__container,.impact__container,.team__container,.approach__container,.partners-certif__container,.cta-contact__container{padding-inline:var(--page-gutter)}
}
""",
    "action": """@media (max-width:767px){
.page-stats__list,.actions-intro,.section-header,.actions-current__grid,.impact-banner__stats,.impact-banner__source,.actions-recent__grid,.cta-support__container,.partners-strip__inner{padding-inline:var(--page-gutter)}
}
""",
    "article-prevention-cancer-peau": """@media (max-width:767px){
.container-reading{padding-inline:var(--page-gutter)}
}
""",
    "maintenance": """@media (max-width:767px){
.maintenance{padding-inline:var(--page-gutter)}
}
""",
    "mission-sante": """@media (max-width:767px){
.mission-detail__selector-list{padding-inline:var(--page-gutter)}
}
""",
}

HEAD = (MARK + " =====\n"
        "   Marge latérale unique : --page-gutter (:root, plus haut). Bloc partagé identique dans\n"
        "   toutes les feuilles ; les conteneurs propres à une page suivent (tools/gutter_25a_apply.py). */\n")


def process(path, check):
    name = os.path.basename(path)[:-4]
    s = open(path, encoding="utf-8").read()
    has_root = "--container-pad:" in s
    # 1. retire un bloc V155 précédent
    i = s.find(MARK)
    if i >= 0:
        s = s[:i].rstrip("\n")
    # 2. tokens
    if has_root and "--page-gutter:2rem;" not in s:
        for old, new in TOKENS:
            n = s.count(old)
            if n != 1:
                raise SystemExit(f"{name}: motif attendu 1 fois, trouvé {n} : {old[:60]}")
            s = s.replace(old, new)
    # 3. bloc
    if has_root:
        block = HEAD + SHARED + PAGE.get(name, "")
        s = s.rstrip("\n") + "\n" + block
    if not check:
        open(path, "w", encoding="utf-8").write(s)
    return name, has_root


def main():
    check = "--check" in sys.argv
    done = []
    for p in sorted(glob.glob(os.path.join(STYLES, "*.css"))):
        done.append(process(p, check))
    print("feuilles traitées :", sum(1 for _, r in done if r), "/", len(done),
          "(sans :root, ignorées :", ", ".join(n for n, r in done if not r) or "aucune", ")")


if __name__ == "__main__":
    main()
