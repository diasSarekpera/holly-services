# Rapport de conversion — rejoindre-equipe

Source : prototype/rejoindre-equipe.html


## Fait automatiquement
- 71 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (24 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;1,40
  - CSS/police externe : https://fonts.gstatic.com
  - script de tracking
  - script externe : /cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
  - `body { font-family: var(--font-body); color: var(--text-main); background-color: var(--bg-white); line-height:`
- 1 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --focus-ring
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : badge, btn, container, eyebrow, hero
- Couleurs en dur restantes : #E2E8F0, #FAFBFC, #FFF3EB, #ccc, #ddd, #fff
- Icônes utilisées (9) : ri-arrow-up-line, ri-bar-chart-box-line, ri-earth-line, ri-group-line, ri-heart-line, ri-leaf-line, ri-map-pin-line, ri-scales-3-line, ri-shield-check-line
- 1 formulaire(s) : ajouter `data-form` (voir docs/FORMULAIRES.md).
- 3 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
