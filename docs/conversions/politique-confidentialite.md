# Rapport de conversion — politique-confidentialite

Source : prototype/politique-confidentialite.html


## Fait automatiquement
- 10 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (23 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `/* Reset & Base */ * { box-sizing: border-box; margin: 0; padding: 0; }`
  - `body { font-family: var(--legal-font-text); color: var(--legal-t-main); background-color: var(--legal-bg-white`
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
