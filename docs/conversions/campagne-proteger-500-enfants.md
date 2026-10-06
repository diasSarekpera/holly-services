# Rapport de conversion — campagne-proteger-500-enfants

Source : prototype/campagne-proteger-500-enfants.html

- ⚠ Pas de meta description dans le prototype : à rédiger.

## Fait automatiquement
- 28 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (24 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `/* Reset & Base */ * { box-sizing: border-box; margin: 0; padding: 0; }`
  - `body { font-family: var(--font-body); color: var(--color-text-main); background-color: var(--color-bg-white); `
- 3 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --color-border, --color-urgent-soft, --header-height
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : badge, btn, btn--primary, container, hero
- Icônes utilisées (16) : ri-alarm-warning-line, ri-calendar-line, ri-eye-line, ri-facebook-fill, ri-group-line, ri-heart-pulse-line, ri-link, ri-linkedin-fill, ri-magic-line, ri-map-pin-line, ri-medicine-bottle-line, ri-stethoscope-line, ri-sun-cloudry-line, ri-time-line, ri-user-smile-line, ri-whatsapp-line
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
