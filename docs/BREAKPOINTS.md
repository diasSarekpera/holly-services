# Points de rupture — audit (tâche 3A, V90)
Source : `python tools/bp_3a_audit.py` (`--sel max-900` = composants). Aucun CSS modifié. « Occ. » = blocs `@media` (blocs partagés header/footer/boutons comptés dans chaque feuille) ; « Fich. » = feuilles sur 21.

## 1. Inventaire (max-width puis min-width)
| Valeur | Occ. | Fich. | | Valeur | Occ. | Fich. |
|---|---|---|---|---|---|---|
| max 359 | 23 | 20 | | max 1023 | 150 | 20 |
| max 375 | 40 | 19 | | max 1024 | 3 | 1 |
| max 430 | 3 | 1 | | max 1099 / 1100 | 21 / 20 | 19 / 19 |
| max 479 / 480 | 109 / 24 | 20 / 19 | | max 1199 | 19 | 19 |
| max 560 / 600 | 1 / 14 | 1 / 10 | | max 1279 | 45 | 20 |
| max 639 / 640 | 54 / 65 | 20 / 19 | | max 1439 | 19 | 19 |
| max 700 / 767 / 768 | 1 / 163 / 1 | 1 / 21 / 1 | | min 480 / 520 / 640 / 768 | 3 / 2 / 3 / 3 | 1 / 2 / 1 / 2 |
| max 860 / 899 / 900 | 5 / 6 / 37 | 1 / 1 / 20 | | min 901 / min 1024 | 19 / 100 | 19 / 20 |
Plages : 1024–1279 (22), 1024–1439 / 1199 / 1099 (19 chacune, header), 480–639 (3), 640–1023 (3), 520–767 (2), 768–1279 (1). Aucune unité em/rem.

## 2. Jeu cible
max-width **479 · 767 · 1023 · 1279** ; menu desktop dès **min-width 1024** ; min-width appariés : 480, 768, 1024, 1280 (pas de 640/901/520).

## 3. Valeur actuelle -> cible (risque)
| Actuel | Cible | Layout touché | Risque |
|---|---|---|---|
| 480 (24) ; 768 (1) ; 1024 max (3) | 479 ; 767 ; 1023 | décalage de 1 px (footer, camp-card, dons, home) | nul |
| min 901 (19) / max 900 (footer) | min 1024 / max 1023 | footer : 901–1023 passe en colonnes mobiles | élevé |
| 375 (40) ; 359 (23) ; 430 (3) | 479 | footer, camp-card, galerie, soutenir, post, contact : règles « petit mobile » étendues à 376–479 | moyen |
| 639 (54) / min 640 | 767 / min 768 | team, missions, temoignages, article-cta : 1 col jusqu'à 767 au lieu de 2 col dès 640 | moyen-élevé |
| 640 (65) | 767 | footer, galerie, blog, post, camp-chip, `.btn` (pleine largeur) | moyen-élevé |
| min 480 (3) / min 520 (2) | min 480 | `.team`, `.btn` ; `.action-card` | faible |
| 700 (maintenance) ; 860 (action) | 767 | maintenance ; actions-intro, impact-banner, action-tile | faible / moyen |
| 1024 (min, 100) | inchangé | menu desktop | — |
| 1279 (45) | inchangé | grilles larges | — |

## 4. Cas ambigus (décision à prendre)
| Valeur | Composants | Proposition |
|---|---|---|
| 900 / 899 (37 + 6) | `.legal-sidebar`, `.rapport-nav`, `.candidature-layout`, `.approach`, `.mission` (2 col -> 1) | -> 1023 : barres latérales trop étroites à 768–1023 |
| 900 | `.stat-item`, `.team-card`, `.gal-item`, `.partners` (grilles de cartes) | -> 767 |
| 600 / 560 | `.benevolat-*`, `.article-*`, `.partenariats-intro`, `.post` | -> 767 (cartes 1 col) ; `.post` 560 -> 479 |
| 640 / 639 | `.btn` pleine largeur (bloc partagé T9) vs grilles de pages | `.btn` -> 479 ; grilles -> 767 : à scinder |
| 1100 / 1099 | `.footer`, `.galerie`, `.soutenir`, `.contact` | -> 1023 si colonnes <4 ; sinon 1279 |
| 1199 / 1439 / 1099 | `.navbar` (échelles logo/liens 1024–1439, V62) | **exception header** : ne pas fusionner (jamais de retour à la ligne) |
| 375 / 359 | `.footer`, `.gal-item`, `.soutenir`, `.contact` | micro-réglages 320–360 : à garder si `resp_check` 320 échoue |

## 5. Ordre conseillé (tâches suivantes)
1. Décalages de 1 px (risque nul). 2. Blocs partagés (footer 900/1100, `.btn` 640), identiques dans les 21 feuilles avec hash. 3. Feuilles de page, une par une, `resp_check` aux 8 largeurs. 4. Header en dernier ou jamais.

## 6. Application (tâche 3B, V91) — `tools/bp_3b.py test|apply|verify`
Critère : 0 différence de styles calculés (7 largeurs autour du seuil, 20 pages) ; sinon annulé. Appliqués : 480→479, 768→767, 1024→1023 (partout) ; 600→767 sur 3 feuilles. Annulés : 375/359/430/560/700/860, 639/640(+min 640), 900/899(+min 901), 1099/1100, min 520 (layout modifié). Vérif. finale : 0/20 page différente à 30 largeurs.
