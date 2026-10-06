# Rapport de conversion — article-prevention-cancer-peau

Source : prototype/article-prevention-cancer-peau.html

- 4 image(s) via.placeholder.com → `.media-placeholder` ; à lister dans docs/A-FOURNIR.md (sujet, ratio).
- ⚠ 1 balise(s) <footer> dans le contenu : à renommer (div/section) pour n'avoir qu'un seul footer de site.

## Fait automatiquement
- 69 `var(--…)` du prototype remplacées par des tokens du site (par valeur).
- :root du prototype retiré (25 variables).
- Retiré (externe/tracking) :
  - CSS/police externe : https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css
  - CSS/police externe : https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,60
  - script de tracking

## À vérifier / terminer à la main
- Règles de base retirées du prototype (le global les gère) — vérifier que rien d'utile ne manque :
  - `/* Reset & Base */ * { box-sizing: border-box; margin: 0; padding: 0; }`
  - `html { font-size: 16px; scroll-behavior: smooth; }`
  - `body { font-family: var(--font-ui); color: var(--color-text-main); background-color: var(--color-bg-white); li`
- 2 token(s) locaux conservés dans un :root de page.css (valeur sans équivalent dans variables.css) : --reading-width, --transition-default
- ⚠ Classes du prototype qui existent AUSSI dans le CSS global (risque de collision de styles) : btn, container, eyebrow
- Couleurs en dur restantes : #fff
- Icônes utilisées (9) : ri-arrow-left-line, ri-arrow-right-line, ri-facebook-circle-line, ri-linkedin-box-line, ri-links-line, ri-printer-line, ri-time-line, ri-twitter-x-line, ri-whatsapp-line
- ⚠ 4 reste(s) de test dans le HTML (onclick=alert, boutons « Test … ») : à supprimer.
- 1 formulaire(s) : ajouter `data-form` (voir docs/FORMULAIRES.md).
- 8 lien(s) `href="#"` à câbler vers une vraie page.
- Navbar/footer : marqueurs vides ; seront remplis par tools/build.py (quand il existe).
- Le hero du prototype doit laisser la place à la navbar (vérifier padding-top / .header-placeholder supprimé).
- Responsive 360 / 768 / 1280 px à contrôler.
