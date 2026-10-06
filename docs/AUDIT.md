# Audit d'accessibilité

## Contraste des couleurs (`python3 tools/contrast.py`, V37)
Seuils WCAG 2.x AA : 4,5:1 (texte normal), 3:1 (grand texte ≥ 24 px ou ≥ 18,66 px gras, éléments d'interface, anneau de focus). 49 couples contrôlés (tokens de `variables.css`, footer, heros) ; `-v` liste tous les ratios. Le script lit les tokens dans `variables.css` ; les couples sont déclarés dans `PAIRS`. Il n'analyse pas les CSS de page : un couple absent de `PAIRS` n'est pas contrôlé.

### Corrigé (token ajusté)
| Token | Avant | Après | Effet |
|---|---|---|---|
| `--nd` | blanc 38 % → 3,46:1 sur navy | blanc 55 % → 5,67:1 | libellé newsletter, mentions du footer, bouton fantôme 404 (bordure plus marquée), citation et source des pages Actions |
| `--ndd` | blanc 28 % → 2,50:1 sur navy | blanc 50 % → 4,94:1 | placeholder newsletter, lignes secondaires du footer ; reste sous `--nd` et `--nm` (62 %) |

### Non corrigé : ajuster le token casserait un autre couple (à arbitrer)
1. **`--clr-accent` (#6E8B7B)** est utilisé comme texte sur fond clair *et* sur fond navy, et comme fond de texte blanc. Un seul token ne peut pas servir les trois :
   - sur blanc : 3,72:1 ; sur `--clr-accent-soft` : 3,32:1 ; texte blanc sur fond accent : 3,72:1 (min 4,5) ;
   - sur navy (titres de colonne et tag du footer) : 4,23:1 ; sur `--clr-secondary-light` (eyebrow de la bande mission) : 3,29:1 (min 4,5).
   Le assombrir répare le clair mais aggrave le navy ; l'éclaircir fait l'inverse. Pistes (hors périmètre de cette tâche) : texte accent sur fond clair et fond de pastille blanche → `--clr-accent-dark` (5,41:1 sur blanc, 4,82:1 sur accent-soft, blanc dessus 5,41:1) ; sur navy → nouveau token clair de type `#8FAE9D` (6,53:1 sur navy, 5,08:1 sur navy-light). Les usages réels de `--clr-accent` en texte sont à inventorier avant de changer (`grep -rn "clr-accent)" styles`).
2. **`--clr-primary` (#C8184A) sur navy : 2,76:1 (min 3:1, grand texte)** : mot accentué du titre des heros (`.hero__title-accent`, `.about-hero__title-accent`, `.page-hero__title-accent`). L'éclaircir assez pour atteindre 3:1 fait tomber à ≈ 4,1:1 le couple primary sur `--clr-primary-soft` (min 4,5), et il n'existe aucune valeur qui satisfasse les deux. Piste : sur fond navy, utiliser une teinte rose claire déjà au thème, p. ex. `--donate-clr` (5,35:1 sur navy), pour ces mots accentués.
3. **Anneau de focus** (`:focus-visible` de `base.css`, 2 px `--clr-primary`) : 5,6:1 sur fond clair mais **2,76:1 sur navy** (footer, heros, sections sombres ; min 3:1 pour un indicateur de focus). Piste : règle dédiée `outline-color` sur les zones navy (ex. `--donate-clr`), sans toucher à la règle globale.

### Non corrigé : valeurs littérales dans un CSS de page (pas des tokens)
- `styles/home/hero.css` : `.hero__stat-label` en `rgba(255,255,255,0.38)` (3,46:1) et `.hero__scroll-hint span` en `rgba(255,255,255,0.28)` (2,50:1). Remplacer par `var(--nd)` et `var(--ndd)` (désormais 5,67:1 et 4,94:1) règle ces deux cas.
- Aussi à relire : les fonds réels des heros sont des photos sous voile sombre (photo non fournie, fond navy en attendant) ; les ratios sont calculés sur le navy plein et devront être re-contrôlés avec les vraies photos (zones claires sous le voile).

## Focus visible
`:focus-visible { outline: 2px solid var(--clr-primary); outline-offset: 3px; }` est **déjà défini globalement** dans `styles/global/base.css` (importé par tous les `main.css`) : rien ajouté. Des règles spécifiques existent pour navbar, menu mobile et bouton retour-haut. Des `outline: none` subsistent dans `navbar.css` (l. 217, 503, 560), `footer.css` (344), `a-propos/cta-contact.css` (142), `404/page.css` (178), `home/contact.css` (316) et `actualites/page.css` (115, champ de recherche) : à vérifier au cas par cas (un état `:focus-within`/`:focus-visible` équivalent est-il fourni ?). Non vérifié dans cette tâche.

## Clavier et mouvement réduit (V38)
Audit de `scripts/components/nav-dropdown.js`, `hero-mobile.js` (menu mobile) et `tabs.js`. Tests automatisés sous jsdom (26 vérifications, partials réels, CSS non chargé) ; **non testé en navigateur ni avec un lecteur d'écran**.

| Composant | Constat | Statut |
|---|---|---|
| Sous-menus desktop | Échap ne fermait pas visuellement : `.navbar__item--dropdown:focus-within` (navbar.css) gardait le menu ouvert alors que `aria-expanded="false"` | corrigé : sélecteur retiré, ouverture = survol ou `.is-open` |
| Sous-menus desktop | Survol non masquable par Échap (WCAG 1.4.13) | corrigé : classe `is-dismissed` (retirée à `mouseleave`/`mouseenter`/clic) |
| Sous-menus desktop | Échap laissait le focus dans un menu devenu invisible | corrigé : focus rendu au bouton |
| Sous-menus desktop | Aucune touche fléchée | corrigé : ↓/↑ sur le bouton ouvrent et vont au 1er/dernier lien ; ↓ ↑ (boucle), Début, Fin dans le sous-menu |
| Sous-menus desktop | `aria-expanded` à jour (clic, survol, focusout, Échap) | conforme, vérifié |
| Menu mobile | Échap, retour du focus au hamburger, `aria-expanded`/`aria-hidden`, scroll verrouillé, fermeture au passage en desktop | conforme, vérifié |
| Menu mobile | Piège à focus : comptait les liens des accordéons fermés (`max-height: 0` sans `visibility`) ; le focus pouvait aussi s'y poser | corrigé : `visibility: hidden` sur `.mobile-submenu` fermé (+ filtre `visibility` dans `getFocusableElements`) |
| Menu mobile | Focus hors du menu non rattrapé par Tab | corrigé : ramené au 1er/dernier élément |
| Menu mobile | `#nav-mobile` sans rôle | corrigé : `role="dialog" aria-modal="true" aria-label="Menu principal"` (partial `mobile-menu.html`) |
| Onglets (`tabs.js`) | rôles, `aria-selected`, tabindex itinérant, ← → (boucle), Début, Fin, Espace, `[hidden]` prioritaire en CSS | conforme, aucune modification |
| Mouvement réduit | `prefers-reduced-motion` existait dans `base.css` (durées) mais pas dans `animations.css` ; `scroll-behavior: smooth` (reset.css) jamais désactivé | ajouté dans `animations.css` (animations, transitions, `scroll-behavior: auto`) ; les blocs spécifiques (navbar, footer, tabs, formulaires, retour-haut) restent |

Restes (non traités) : le menu mobile n'applique pas `inert` au reste de la page (le piège de Tab suffit au clavier ; un lecteur d'écran peut encore parcourir l'arrière-plan) ; `nav-dropdown.js` garde ses fins de ligne CRLF d'origine ; pas de navigation ← → entre entrées de premier niveau de la navbar (non exigée par le motif « disclosure »).

## Contrôle d'ensemble (V41)
### 1. Contrôles automatiques
- `python3 tools/build.py --check` : OK (20 pages à jour) ; `python3 tools/check.py` : 0 erreur (63 avertissements : liens `maintenance.html`, `[À COMPLÉTER]`, couleurs en dur) ; `build.py --sitemap --check` : OK. `contrast.py` inchangé (9 couples sous le seuil, voir plus haut).

### 2. Fichiers CSS/JS non référencés
- Méthode : script ponctuel (non conservé) = CSS atteints par `<link>` puis `@import` récursifs depuis index, 404 et pages/*, JS atteints par `<script src>`, puis recherche du nom de fichier dans le reste du site.
- Résultat : 1 seul fichier orphelin sur 98, **supprimé** : `scripts/pages/home/actions.js` (filtres `.actions__filter-row`, aucun balisage correspondant dans aucune page, aucune référence). Tous les CSS sont atteints.
- Laissé, à arbitrer : les 9 occurrences `.actions__filter*` de `styles/home/actions.css` (CSS de filtres sans balisage correspondant, partie du composant copié sur `styles/action/actions-current.css`).

### 3. Liens de navigation (desktop + menu mobile)
- Script ponctuel sur les zones `navbar` et `mobile-menu` des 19 pages qui les portent (38 zones) : 0 lien cassé, 0 ancre absente (`#hero`, `#stats`, `#team`, `#temoignages`, `#partners`, `#galerie`, `#dons`, `#soutenir`, `#contact` présentes dans index), 0 lien vers `maintenance.html`.
- Même ensemble de cibles dans navbar et menu mobile sur chaque page ; liens identiques sur les 19 pages. `maintenance.html` n'a volontairement ni navbar ni menu.
- Non vérifié : le comportement au clic (pas de rendu).

### 4. Typographie française
- Détection (script ponctuel, texte visible + `alt`/`title`/`aria-label`/`placeholder`/meta description et og/twitter ; `<script>`, `<style>` et commentaires exclus) d'une espace ordinaire avant `;` `:` `?` `!`, et d'espaces ordinaires ou absentes autour de « ».
- Corrigé : 40 occurrences dans 12 pages/partials (index 10, a-propos, actions, actualites, campagne, conditions-utilisation, mentions-legales, mission-sante, notre-approche, transparence-rapports, 404, maintenance, nos-missions) → `&nbsp;` dans le texte, U+00A0 dans les attributs ; descriptions de `META` (`tools/build.py`) mises à jour en même temps (sync vérifiée par le build).
- Faux positifs de la détection : `&amp;` suivi d'un espace (12) et `«&nbsp;`/`&nbsp;»` écrits en entité (12) : déjà corrects.
- Non traité : JSON-LD et textes dans les JS (aucune occurrence repérée en JSON-LD de l'article) ; pas de contrôle des chiffres ni des abréviations (« 500 enfants », « M. »).
