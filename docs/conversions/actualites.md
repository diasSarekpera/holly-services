# Rapport de conversion — actualites

Source : prototype/actualites.html


## Fait automatiquement
- 77 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (28 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - script de tracking
  - script externe : /cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `/* Reset & Base */ * { box-sizing: border-box; margin: 0; padding: 0; }`
  - `body { font-family: var(--lc-font-ui); color: var(--lc-text-main); background-color: var(--lc-bg-white); line-`
- 1 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --lc-transition
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : badge, btn, container, eyebrow
- Couleurs en dur restantes : #E2E8F0
- Icônes utilisées (7) : ri-arrow-left-s-line, ri-arrow-right-line, ri-arrow-right-s-line, ri-check-line, ri-download-2-line, ri-mail-line, ri-search-line
- 1 formulaire(s) : ajouter `data-form` (voir docs/FORMULAIRES.md).
- 7 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
