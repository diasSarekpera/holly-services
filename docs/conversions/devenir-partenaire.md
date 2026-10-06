# Rapport de conversion — devenir-partenaire

Source : prototype/devenir-partenaire.html

- ⚠ Pas de meta description dans le prototype : à rédiger.

## Fait automatiquement
- 25 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (21 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,60
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `* { margin: 0; padding: 0; box-sizing: border-box; }`
  - `body { font-family: var(--f-body); color: var(--c-gray-900); line-height: 1.5; background-color: var(--c-white`
- 3 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --c-gray-100, --c-gray-300, --c-gray-600
- Couleurs en dur restantes : #a0133b
- Icônes utilisées (14) : ri-arrow-right-s-line, ri-bar-chart-box-line, ri-calendar-check-line, ri-download-2-line, ri-earth-line, ri-global-line, ri-government-line, ri-group-line, ri-lock-2-line, ri-map-pin-line, ri-medal-line, ri-pie-chart-line, ri-search-eye-line, ri-shield-check-line
- 1 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
