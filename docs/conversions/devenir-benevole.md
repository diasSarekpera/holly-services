# Rapport de conversion — devenir-benevole

Source : prototype/devenir-benevole.html

- ⚠ Pas de meta description dans le prototype : à rédiger.

## Fait automatiquement
- 46 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (18 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,60
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `* { margin: 0; padding: 0; box-sizing: border-box; }`
  - `body { font-family: var(--benevolat-f-text); color: var(--benevolat-c-text); background-color: var(--benevolat`
- 4 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --benevolat-c-border, --benevolat-c-primary-hover, --benevolat-c-text, --benevolat-transition
- Couleurs en dur restantes : #64748B, #94A3B8
- Icônes utilisées (10) : ri-arrow-right-line, ri-building-line, ri-calendar-line, ri-home-heart-line, ri-macbook-line, ri-map-pin-2-line, ri-map-pin-line, ri-suitcase-2-line, ri-team-line, ri-time-line
- 1 formulaire(s) : ajouter `data-form` (voir docs/FORMULAIRES.md).
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
