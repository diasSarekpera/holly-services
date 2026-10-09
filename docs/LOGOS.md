# Logos : fichiers, provenance et remplacement

## Logo de l'ONG (provisoire : l'ONG prévoit de changer de logo)
Sources reçues : `assets/byONG/` (JPG WhatsApp). Le logo de Holly Services (IMG-20261008-WA0033) a été redessiné en vecteur (couleurs aplaties, halos retirés), sans modifier la palette du site (identité = rose / marine / or, inchangée).

| Fichier | Usage |
|---|---|
| `assets/images/logo.svg` | Médaillon (emblème dans un disque blanc, 120 x 120) : menu mobile, footer, fond sombre. |
| `assets/images/logo-emblem.svg` | **Header** : affiché dans un badge blanc collé en haut (CSS « Logo du header »). |
| `assets/images/logo-full.svg` | Logo complet avec texte, fond transparent (fonds clairs, impression, documents). |
| `assets/images/logo-512.png` | PNG 512 px du médaillon (JSON-LD `logo`). |
| `assets/images/apple-touch-icon.png` | 180 px, **non référencé** dans les `<head>` (à ajouter si souhaité). |
| `assets/images/favicon.svg` | Favicon allégé (4 Ko). |

**Changer de logo plus tard** : remplacer `logo.svg` (garder un viewBox carré 0 0 120 120, fond blanc circulaire recommandé), puis `logo-full.svg`, `logo-emblem.svg`, `logo-512.png`, `favicon.svg`. Aucun HTML ni CSS à modifier.

## Logos des partenaires (`assets/images/partners/`)
Tous fournis par l'ONG comme partenaires. Nom exact, rôle et site web restent à confirmer.

| Fichier | Partenaire | Remarque |
|---|---|---|
| `espoir-albinos-handicapes.svg` | ONG Espoir pour les personnes albinos et handicapées | vecteur |
| `valeur-albinos.webp` | Valeur Albinos | raster détouré (dégradés non vectorisables) |
| `stevanato.svg` | Dra. Samantha Galant Stevanato | vecteur |
| `sobedo.svg` | SOBEDO | vecteur ; le « S » est tronqué dans l'image source |
| `padimi.svg` | Équipe de course Padimi | vecteur |
| *(aucun fichier)* | SANAA | affiché par son **nom seul** (`.partner-logo-tile__name`) : la source est la photo d'un T-shirt, inutilisable |

Vecteurs produits par vectorisation + palette forcée : si l'ONG fournit les fichiers originaux (SVG / PNG haute résolution), les substituer à nom identique.
