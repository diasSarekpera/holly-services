
# Outils de contrôle

## tools/resp_check.py : contrôle responsive (Playwright, serveur local intégré)
- Usage : `python tools/resp_check.py <page|all> [--widths 320,360,...] [--sections a-b]` (page : `index.html`, `a-propos`, `pages/x.html`, `all` = 20 pages ; défaut 320/360/390/768/1024/1280/1440/1920).
- `--sections a-b` limite aux `<section>` de rang a à b (rang 1 = première `<section>`) ; le défilement horizontal de la page reste signalé.
- Types : hscroll (+5 éléments les plus larges) · tap<44 (liens/boutons non « inline », ≤ 767 px) · text<12 · titre (H1-H4 débordant/coupé) · img (dépasse son parent / sans width+height) · btn-2lignes · largeur>vp.
- Éléments `position:fixed` ou rognés par un ancêtre `overflow` contenu dans le viewport : ignorés (pas de faux positifs de menu hors-champ).
- Sortie : 30 lignes max (`page largeur type n=… sélecteurs`), détail complet dans `/tmp/resp_check_<ts>.json` (chemin en dernière ligne). Ne modifie aucun fichier.
- Autres : `btn_audit.py` (inventaire classes boutons), `btn_9c2_measure.py` (boutons 360/768/1280), `check.py` (HTML/CSS/JS), `build.py` (partials).
