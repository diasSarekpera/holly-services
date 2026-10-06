# Rapport de conversion — mission-sante

Source : prototype/mission-sante.html


## Fait automatiquement
- 38 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (26 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `/* Reset & Base */ * { box-sizing: border-box; margin: 0; padding: 0; }`
  - `body { font-family: var(--font-body); color: var(--lc-text-main); background-color: var(--lc-bg-white); line-h`
- 1 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --transition-default
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : breadcrumb, btn, container, eyebrow, hero
- Icônes utilisées (2) : ri-arrow-right-line, ri-stethoscope-line
- 6 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
