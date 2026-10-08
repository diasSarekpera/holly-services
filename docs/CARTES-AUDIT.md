# Cartes : audit et recette (T10A)

Outils : `tools/cards_audit.py` (inventaire, JSON /tmp/cards.json), `tools/cards_t10.py apply|hash|measure` (bloc partagé + mesure).
Inventaire = classes simples (toutes feuilles, hors @media) avec bordure + rayon + fond clair, complétées à la main par les classes `*-card` sans bordure. Il peut manquer des cartes dont le nom ne contient pas card/tile (voir « À revoir »).

## Recette unique (bloc « Cartes (T10) », fin des 21 feuilles, hash identique `ef1f5e2f712b`)
- Repos : fond `--clr-white`, bordure `1px solid --clr-border-card` (0.18), ombre `--shadow-card`, rayon `--radius-card` (6 px).
- Transition : `border-color` et `box-shadow` seulement.
- Survol : `--clr-border-hover` (0.32) + `--shadow-hover`, `transform:none`. Padding laissé aux règles locales.
- Fond de section derrière les cartes (ex. #EDF0F4) : pas posé ici (10B-10G).

## Classes du bloc (27) par type
| Type | Classes |
|---|---|
| contenu | why-card, card-besoin, erreur404-card, mission-detail__card, card-soutien, reason-card, metier-card, chiffre-card, banner-card, cta-card, form-card |
| pilier | value-card |
| équipe | team-card |
| action | action-card, action-tile |
| actualité / article | actualites-card, article-card |
| campagne / don | campagne-card, campagne-don |
| offre | benevolat-mission-card, job-sidebar |
| contact / format | article-cta__card, benevolat-format-card, maintenance__contact-card |
| témoignage | temoignage-card |
| résultat | rapport-result-card |
| partenaire | partner-logo-tile |

## Écarts relevés avant le bloc (mesure 1280 px, 0/28 conformes)
- Bordure : 0,14 (404, campagne), 0,20 (value-card), `--clr-surface` (why-card), rose 0,15 (team-card), bleu pâle (benevolat-format-card), aucune (actualites-card), transparente (article-card).
- Ombre : `--shadow-md` 0.05 (10 classes), `--shadow-card` (4), aucune (action-*, team-card, article-cta__card).
- Fond : benevolat-format-card gris clair (#F8F9FB) ; reason-card, metier-card, chiffre-card en `--clr-off-white`.
- Survol : 20 classes sans bordure/ombre conformes ; déplacement ou bordure rose sur erreur404-card, actualites-card, article-card.
- Rayons : `--radius-md/sm/badge` encore présents (tous 4 ou 6 px) → alignés sur `--radius-card`.

## Exclus (volontairement)
- Cartes sombres : camp-card (home, fond marine), partners__flagship (texte blanc : invisible sur fond blanc, détecté à la mesure).
- Pas des cartes : actualites-featured__img, campagne-photo, contact-form__textarea, actualites-toolbar__search, actualites-page, missions-anchors__link, legal-box, camp-card__*, team-card__*, badges.
- À revoir en 10B-10G (statut incertain) : post, preview-pane, rapport-sheet, soutenir__trust, stats__audit, stats__note, stats__item-source, blog__count (non utilisée dans le HTML).

## Mesure après (Playwright, 1280 px, styles calculés)
- Repos : 26/26 classes visibles conformes (fond, bordure, rayon, ombre, transition). Survol : 26/26 (bordure, ombre, transform none, position inchangée).
- `job-sidebar` : masquée à la mesure (panneau replié), non vérifiée.
- Pas de nouveau défilement horizontal (a-propos 1280 px : +100 px, déjà connu).

## À faire (10B-10G)
- Supprimer les règles locales devenues redondantes (bordure, ombre, rayon, survol, `transform` au survol).
- Ajouter le fond de section soutenu derrière les cartes ; vérifier le texte clair/foncé de chaque carte.
- Décider du sort des classes « à revoir ». Les règles locales à spécificité plus forte (`.home .x`, `:root body .x`) battent le bloc : à repérer.
