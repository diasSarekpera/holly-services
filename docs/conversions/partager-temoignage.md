# Rapport de conversion — partager-temoignage

Source : prototype/partager-temoignage.html


## Fait automatiquement
- 23 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (23 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;1,40

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `* { box-sizing: border-box; margin: 0; padding: 0; }`
  - `body { font-family: var(--font-text); color: var(--text-main); background-color: var(--bg-white); line-height:`
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : breadcrumb, btn, container, eyebrow, hero
- Icônes utilisées (3) : ri-heart-line, ri-megaphone-line, ri-plant-line
- 1 formulaire(s) : ajouter `data-form` (voir docs/FORMULAIRES.md).
- 2 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
