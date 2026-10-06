# Rapport de conversion — nos-missions

Source : prototype/nos-missions.html

- ⚠ Le prototype utilise des icônes `ri-*` mais styles/global/icons.css n'existe pas encore (tâche « icônes »).

## Fait automatiquement
- 35 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (25 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,60
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `* { margin: 0; padding: 0; box-sizing: border-box; }`
  - `body { font-family: var(--font-body); color: var(--color-text-main); background-color: var(--color-bg-white); `
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : btn, container, eyebrow, hero, missions
- Couleurs en dur restantes : #E0E0E0
- Icônes utilisées (9) : ri-arrow-right-line, ri-book-open-line, ri-check-line, ri-hospital-line, ri-map-pin-line, ri-pie-chart-line, ri-scales-3-line, ri-sun-line, ri-user-heart-line
- 4 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
