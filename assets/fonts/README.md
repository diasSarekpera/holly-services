# Polices du site (hébergées localement)

Toutes les polices sont servies depuis ce dossier : aucune requête vers Google Fonts ni un autre CDN. Format WOFF2, sous-ensemble latin, `font-display: swap`. Les `@font-face` sont déclarés dans chaque feuille de `styles/` (chemins `../assets/fonts/...`) et les fichiers principaux sont préchargés dans le `<head>` des pages.

| Famille | Rôle (variable CSS) | Fichiers |
|---|---|---|
| Cormorant Garamond | titres et chiffres (`--font-display`) | 300, 400, 500, 600 normal ; 300, 400, 500 italique |
| Outfit | texte courant, interface (`--font-body`) | 300, 400, 500, 600 normal |
| Nunito | nom « Holly Services » (`--font-brand`) | 800 normal |

Licence : ces trois familles sont publiées sous SIL Open Font License 1.1 (texte : https://openfontlicense.org). Conserver ce dossier tel quel avec le site.

## Pour ajouter une police ou un poids
1. Déposer le `.woff2` dans le sous-dossier de la famille (nom : `famille-latin-POIDS-style.woff2`).
2. Ajouter le `@font-face` correspondant dans les feuilles de `styles/` (bloc identique partout).
3. Ne jamais ajouter de `<link>` vers un service de polices externe.

## Limites connues (mesurées sur les 21 pages, voir docs/SUIVI.md V139)
- Outfit n'existe pas en italique : les textes en italique Outfit (notes, sources, mentions) sont obliques synthétisés par le navigateur.
- Le poids 700 est demandé sur quelques pages (Outfit, Cormorant) : le navigateur utilise la face 600 disponible.
