# Audit des boutons (T9A)
Généré par `tools/btn_audit.py` (motif `btn|cta`, HTML : `a`/`button` ; CSS : tous les `styles/**/*.css`) → **65 classes**. Entre parenthèses : occurrences / nb de pages. Burger, flèches de carrousel et bouton rond ne contiennent ni `btn` ni `cta` : non listés, laissés hors système.

## Classes → famille → décision
| Classe(s) | Famille | Décision |
|---|---|---|
| `btn` (77/17p), `btn--primary` (43/17p), `btn--ghost` (30/14p), `btn--ghost-light` (1/1p), `btn--submit` (1/1p) | a. Système de base | Garder (socle T9A). `--submit` = primary de formulaire (home) ; `.btn--sm/--lg/--block` ajoutés, 0 usage |
| `btn--donate-inline` (2/1p), `btn--donate-inline--edu` (1/1p), `btn--donate-inline--social` (1/1p), `btn--donate-primary` (1/1p) | b. Variantes locales (home, dons) | Migrer 9B → `btn--primary` (+ `btn--lg` si besoin) |
| `soutenir__way-btn` (3/1p), `soutenir__way-btn--primary` (1/1p), `soutenir__way-btn--secondary` (1/1p), `soutenir__way-btn--tertiary` (1/1p) | b. Variantes locales (home, soutenir) | Migrer 9B → primary / ghost |
| `hero__cta-primary` (1/1p), `hero__cta-secondary` (1/1p), `campagne-don__cta` (1/1p), `cta-contact__button` (1/1p), `maintenance__btn` (1/1p), `benevolat-mission-card__btn` (3/1p), `temoignage-signal__btn` (1/1p) | b. Variantes locales (pages) | Migrer 9B → primary (`cta-*`, `__btn`) ou ghost (`hero__cta-secondary`) |
| `footer__mission-cta` (38/19p), `footer__mission-cta--ghost` (19/19p), `footer__nl-btn` (19/19p), `navbar__cta` (19/19p), `mobile-menu__cta` (19/19p) | b. Boutons de blocs partagés (19 pages) | Migrer 9B, identique partout : `footer__mission-cta` → primary, `--ghost` → ghost-light, `nl-btn` → primary `sm`, `navbar__cta` → primary `sm` (hauteur header à préserver) |
| `actions-filter__btn` (5/1p), `actions-filter__btn--active` (1/1p), `filter-btn` (4/1p) | c. Filtres | Hors système (état `aria-pressed`) |
| `article-share__btn` (6/1p), `campagne-share__btn` (4/1p), `campagne-share__btn--copy` (1/1p), `team-card__social-btn` (5/1p) | c. Partage / réseaux (boutons icône) | Hors système |
| `cta-card` (3/1p), `article-cta__card` (3/1p) | c. Cartes cliquables | Hors système (composant carte) |
| 31 classes : sections/conteneurs/textes « CTA » et flèches (`cta-support*`, `cta-contact*`, `article-cta*`, `*__footer-ctas`, `hero__ctas`, `*-arrow`…) — 0 `<a>/<button>` | d. Faux positifs du motif | Hors système (mise en page, pas des boutons) |

Usages du socle dans les pages : `.btn` 77, `.btn--primary` 43, `.btn--ghost` 30, `.btn--ghost-light` 1, `.btn--submit` 1.

## Valeurs de `.btn` (avant → après T9A)
| Propriété | Avant | Après (socle) |
|---|---|---|
| padding | 0.875rem 1.75rem (14/28) | `var(--sp-3) var(--sp-6)` (12/24) |
| hauteur | auto (≈ 48 px) | `min-height` 44 px (≈ 44–48) ; `--sm` 36 px (≥ 768 px), `--lg` 52 px |
| rayon | `--radius-sm` (4 px) ; `ghost-light` : `--radius-badge` | `--radius-sm` unique |
| graisse / taille | 600 / `--fs-base-sm` (14 px) ; `ghost-light` 13 px | 600 / `--fs-base-sm` ; `--sm` 13 px, `--lg` 16 px |
| gap icône | 0.55rem | `--sp-2` (0.5rem) ; icônes `1em` (15 px → 14 px) |
| retour à la ligne | autorisé | `nowrap`, sauf < 480 px (soupape anti-débordement) |
| line-height | héritée | 1.2 |
| `ghost` bordure | `--clr-border-btn` (0.38) | idem (déjà conforme) |
| `ghost-light` | bordure 1 px, texte 0.48, définie dans `home.css` seul | bordure 1.5 px `--on-dark-border` (0.32), texte `--on-dark-text` (0.88), dans les 20 feuilles |

## Mesure (Playwright, styles calculés, 225 boutons × 360 / 1024 / 1920)
- Débordement horizontal causé par un bouton : 0. Hauteur min mesurée : 44 px (avant : 4 boutons de 404 non stylés en `file://`, artefact).
- Sans `nowrap` sous 480 px, 3 boutons débordaient à 360 px (devenir-partenaire ×2, index) → soupape < 480 px.
- Restent sur 2 lignes à 360 px (déjà le cas avant, contrainte du parent local → 9B) : index ×2, a-propos, actualites, devenir-partenaire.
- Hors périmètre : `a-propos.html` défile horizontalement à 1024 px (1236 px, présent avant T9A).

## 9B2 (V69)
Migrés : `campagne-don__cta`, `benevolat-mission-card__btn`, `temoignage-signal__btn`, `maintenance__btn` ; `cta-contact__button` (a-propos uniquement). Libellés 2 lignes à 360 px résolus : a-propos, actualités. Reste devenir-partenaire (libellé trop long, 398 px > 312 px) : retour à la ligne toléré par la soupape < 480 px. Hors périmètre : `a-propos` défile horizontalement à 1280 px (`.team-card__info` dépasse à 1380 px).

## Système final (T9C2, V72)
- Socle `.btn` (+ `--primary`, `--ghost`, `--ghost-light`, `--block`, `--sm`, `--lg`) : bloc identique dans les 20 feuilles ; min-height 44 px (`--sm` 36 px seulement ≥ 768 px, 44 px sur mobile ; `--lg` 52 px).
- Groupes mobiles (≤ 767 px) : tout parent ayant deux `.btn` consécutifs passe en colonne (`flex`, gap 0.75rem), chaque `.btn` en pleine largeur. Contrôle : 43 groupes à 360 px, tous conformes (écart 12 px, largeur = parent).
- Contrôles locaux hors `.btn` (filtres, partage, réseaux d'équipe) : cible 44 px à toutes les largeurs.
- Libellé : une seule ligne, sauf soupape < 480 px (`white-space:normal`).
- Mesure : `python3 tools/btn_9c2_measure.py -s` (Playwright, 19 pages × 360/768/1280, 511 boutons). Avant : 120 écarts ; après : 1 (devenir-partenaire, libellé « Télécharger le dossier de partenariat (PDF 2 Mo) » trop long pour 312 px, texte non modifiable ici) + débordement a-propos 1280 px (hors boutons, connu).
