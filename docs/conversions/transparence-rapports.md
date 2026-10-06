# Rapport de conversion — transparence-rapports

Source : prototype/transparence-rapports.html


## Fait automatiquement
- 56 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (23 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,60
  - script de tracking
  - script externe : /cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `* { margin: 0; padding: 0; box-sizing: border-box; }`
  - `body { font-family: var(--f-body); color: var(--c-text-main); background-color: var(--c-bg-white); line-height`
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : badge, btn, container, eyebrow, visually-hidden
- Couleurs en dur restantes : #ccc
- Icônes utilisées (6) : ri-award-line, ri-bank-line, ri-download-line, ri-file-pdf-line, ri-mail-line, ri-shield-check-line
- 1 formulaire(s) : ajouter `data-form` (voir docs/FORMULAIRES.md).
- 3 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
