# Rapport de conversion — rapport-consultations-dassa

Source : prototype/campagne-consultations-dassa.html


## Fait automatiquement
- 46 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (28 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,60
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `/* Reset & Base */ * { margin: 0; padding: 0; box-sizing: border-box; }`
  - `body { font-family: var(--font-body); color: var(--color-text-main); background-color: var(--color-bg-white); `
- 2 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --header-height, --transition-default
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : badge, btn, container, eyebrow
- Couleurs en dur restantes : #666, #94A3B8, #E2E8F0, #eee
- Icônes utilisées (12) : ri-arrow-right-line, ri-arrow-right-up-line, ri-calendar-line, ri-check-line, ri-download-line, ri-file-text-line, ri-group-line, ri-map-pin-line, ri-share-line, ri-stethoscope-line, ri-sun-line, ri-time-line
- 1 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
