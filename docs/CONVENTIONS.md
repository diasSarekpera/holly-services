# Conventions — Holly Services (site statique HTML/CSS/JS)

## Arborescence
- Pages : `pages/<slug>.html` (à plat, ressources en `../`). Exception : `404.html` à la racine.
- CSS : `styles/<slug>/main.css` (imports globaux + `page.css`). JS : `scripts/pages/<slug>/` ou `scripts/components/`.
- Prototypes sources : `_archive/prototype/<slug>.html` (archivés, lecture seule, ne jamais lier depuis le site).

## Règles
1. **Tokens uniquement** : `styles/global/variables.css` (`--clr-*`, `--font-display`, `--font-body`, `--radius-*`, `--shadow-*`, `--container-max`, `--section-pad-*`). Pas de couleur en dur dans les CSS de page.
2. **Zéro dépendance externe** : pas de CDN, Google Fonts, Remixicon CDN, GTM/analytics, image distante. Tout en local dans `assets/`.
   *Exception provisoire (V49, demande client)* : les photos de contenu sont des images distantes `https://images.unsplash.com/photo-<id>?auto=format&fit=crop&q=75&w=<l>&h=<h>` (licence Unsplash, usage libre). Ce sont des photos de substitution, réutilisées à plusieurs endroits : à remplacer par de vraies photos locales avant la mise en ligne.
3. **Pas de CSS/JS inline** (sauf JSON-LD). Nommage BEM.
4. **Contenu** : textes des prototypes repris tels quels (typographie française : espaces insécables avant `; : ? !`, guillemets « »). Ne jamais inventer chiffres, noms, dates, textes juridiques → marqueur `[À COMPLÉTER]` + entrée dans `docs/A-FOURNIR.md`.
5. **Images** : tant qu'aucune photo n'est fournie, placeholder CSS (`.media-placeholder` ou pattern `*__bg-placeholder` de la home) + entrée dans `A-FOURNIR.md`.
   Toute `<img>` hors première vue : `loading="lazy" decoding="async"` + `width`/`height` (ratio intrinsèque du fichier, `placeholder.svg` = 800 × 600 ; CSS global `img { height: auto }`) ; hero, avatars du hero et logo de la navbar restent sans `lazy`. À mettre à jour quand une vraie photo remplace un placeholder.
6. **Accessibilité** : `lang="fr"`, skip-link, un seul `<h1>`, landmarks, `aria-current="page"` sur la page courante, `alt` (vide si décoratif), focus visible, `prefers-reduced-motion`.
7. **Chaque page** : `<title>` « Titre — Holly Services ONG », meta description, viewport `width=device-width`.
8. **Un prompt = une tâche.** Pas de refonte opportuniste.

## Conversion d'un prototype (méthode rapide)
`python3 tools/convert_proto.py <prototype> <slug>` fait la partie mécanique (retire tracking/CDN/`:root`, remplace les variables par les tokens du site **par valeur**, crée page/CSS/JS, remplace les images distantes) et écrit un rapport `docs/conversions/<slug>.md` : **c'est ce rapport qui liste le reste à faire**. Ne pas relire tout le prototype : travailler à partir du rapport et de `pages/<slug>.html`.

## Économie de contexte (important pour les sessions)
- `index.html` fait 143 Ko : ne jamais l'ouvrir en entier. Utiliser `grep -n` / `sed -n 'a,bp'`.
- Ne lire que les fichiers cités dans le prompt.
- Ne pas faire de captures/rendus sauf si le prompt le demande.

## Hero sous la navbar fixe (toutes les pages internes)
- La navbar est `position: fixed` : elle ne prend plus de place dans le flux. Le décalage vient d'**une seule règle globale** (`styles/global/components/navbar.css`, section « Header fixe ») : `.hero, .page-hero, .about-hero, … { padding-top: var(--navbar-h); }` (liste des heros « historiques » ; les pages converties au composant `.hero-photo` en sont retirées, le composant porte son propre `padding-top`).
- Nouveau hero : **ajouter sa classe à cette liste** ; ne jamais mettre `padding-top` (ni le raccourci `padding`) sur la racine du hero dans le CSS de page (il passe après et écraserait la règle). Espace du haut = `padding-top` sur le conteneur interne (`.xxx-hero .container { padding-top: 4rem; }`), bas = `padding-bottom` sur la racine. Pas de `.header-placeholder`.
- `typography.css` colore tous les `h1–h6` en `--clr-secondary` : sur un hero navy, mettre le `h1` en `--clr-white` explicitement.
- Marqueurs d'une page convertie : `navbar` **et** `mobile-menu` (le convertisseur ne pose que navbar/footer → ajouter `mobile-menu`), plus le bouton `.back-to-top` après le footer (copier `a-propos`).

## Collisions avec le CSS global (pages converties)
- Ne pas redéfinir dans `page.css` : `.btn` (utiliser `btn btn--primary|btn--ghost`), `.container`, `.eyebrow` (balisage BEM : `eyebrow__line` + `eyebrow__label`), ni des sélecteurs d'éléments nus (`h1`, `h2`, `blockquote`, `em`, `i`) → les scoper (`main h2`, `.bloc blockquote`).
- Préfixer les blocs qui portent un nom global (`.hero` → `.missions-hero`, `.missions` → `.missions-detail`). Plus de `style=""` ni de classes utilitaires inventées (`mt-4`, `text-center`).
- Icônes `ri-*` : `styles/global/icons.css` (masques SVG locaux, `currentColor`) ; marquer `aria-hidden="true"`. Icône manquante = une ligne `.ri-<nom> { --ri: url("…"); }`.

## Partials (navbar, mobile-menu, footer)
- Les pages encadrent chaque zone par `<!-- @partial:navbar:start -->` … `<!-- @partial:navbar:end -->` (idem `mobile-menu`, `footer`) ; source unique = `partials/<nom>.html` (jetons `{{root}}` / `{{home}}`). Ne jamais éditer le contenu entre marqueurs dans une page.
- `python3 tools/build.py` applique ; `--check` n'écrit rien (code 1 si une page est désynchronisée) ; `--root DIR` pour tester sur une copie. Pages sans marqueurs ignorées (vaut aussi pour le bloc meta).
- **Bloc meta du `<head>`** : chaque page contient `<!-- @partial:meta:start -->` … `<!-- @partial:meta:end -->` juste après `<title>` (canonical, `og:title/description/type/url/image`, `twitter:card`, `theme-color`), généré par `build.py` depuis le dictionnaire `META` (clé = nom de page ; `title`, `description`, `og_image`) et `SITE_URL`. `title`/`description` de `META` = ceux de la page (le build échoue sinon) : modifier les deux ensemble. Nouvelle page = nouvelle entrée `META` + marqueurs. Le bloc contient aussi du JSON-LD généré (seul `<script>` inline autorisé : `application/ld+json`) : `NGO` sur `index.html` (constante `ORG` de `build.py` : nom, logo, e-mail, téléphone du footer, rien d'autre ; à resynchroniser si le footer change) et `BreadcrumbList` sur les pages intérieures indexables (Accueil > `parent` > page ; `parent` = clé `META` d'une vraie page, `None` = directement sous l'accueil ; libellés = `title` sans « — Holly Services ONG »). Pas de JSON-LD sur 404/maintenance. Le bloc contient aussi `<link rel="preload" as="font" crossorigin>` pour Outfit 400 et Cormorant Garamond 500 (constante `FONT_PRELOAD` de `build.py`, mêmes fichiers que `fonts.css` ; si un `@font-face` critique change, mettre à jour les deux), et `<link rel="icon">` (`assets/images/favicon.svg`, dérivé de `logo.svg` ; chemin absolu `/…` sur la 404). `python3 tools/build.py --sitemap` (avec `--check` : n'écrit rien) génère `sitemap.xml` et `robots.txt` à la racine : pages hors `NOINDEX` et 404, URL = `SITE_URL` + chemin, sans `lastmod` ; à relancer à chaque page ajoutée/retirée ou changement de `SITE_URL`. `NOINDEX` (404, maintenance) : `<meta name="robots">` à la place de canonical/`og:url`. Image par défaut : `assets/images/og-default.png` (à fournir, `A-FOURNIR.md`) ; `og_image` = chemin depuis la racine pour une page précise.
- Page courante (`aria-current="page"` + classe active) : table `NAV_ACTIVE` en tête de `tools/build.py` (clé = nom de fichier sans `.html`, valeur = href du lien sans jeton). Lancer le build après toute modif d'un partial.

## Contrôle (tools/check.py)
- `python3 tools/check.py` (fin de chaque session ; `-v` détaille les avertissements ; `--root DIR`) : une ligne par page (index, 404, pages/*) + CSS/JS + `build.py --check`, code 1 si erreur. **Erreurs** : lien/src/ancre cassés, ressource externe chargée (`<a href>` sortant OK), `prototype/`, id dupliqué, lang/title/description/og:title/og:description/canonical (canonical non exigé si `noindex`), plusieurs `<h1>`, `<img>` sans alt, script/style inline.
- **Avertissements** (n'échouent pas) : couleur en dur hors `variables.css`/`icons.css`, `var(--x)` sans définition, compteur de liens vers `maintenance.html`, marqueurs `[À COMPLÉTER]`.

- `python3 tools/contrast.py` (`-v` : tous les ratios ; code 1 si un couple est sous le seuil) : contraste WCAG AA des couples texte/fond des tokens, du footer et des heros (couples déclarés dans `PAIRS`, couleurs lues dans `variables.css`). Ajouter un couple à `PAIRS` pour tout nouveau texte sur fond navy. Constats ouverts : `docs/AUDIT.md`.

## Onglets (scripts/components/tabs.js + styles/global/components/tabs.css)
- `<div data-tabs [data-tabs-hash]>` > `<div data-tabs-list aria-label="…">` contenant des `<a href="#id" data-tab>` (ou `<button data-tab aria-controls="id">`), puis un `<section id="id" data-tab-panel>` par onglet.
- Le JS pose `role=tablist/tab/tabpanel`, `aria-selected`, `aria-controls/labelledby`, `tabindex` (roving) et `hidden` sur les panneaux inactifs ; ← → Home End ; ne rien écrire de ces attributs à la main.
- Sans JS : tous les panneaux restent visibles, les onglets sont de simples ancres. Onglet initial : `data-tab-active`, sinon hash d'URL, sinon le premier.
- `data-tabs-hash` : l'URL suit l'onglet actif (`#id`, un seul par page) et un lien vers une ancre interne à un panneau l'ouvre.
- Titres des panneaux : garder la hiérarchie `h2/h3` normale (un seul `<h1>`). Importer `tabs.css` dans le `main.css` de la page et charger `tabs.js` en `defer`.

## Gabarit pages légales (`.legal-*`, `styles/politique-confidentialite/page.css`)
- Pour politique de confidentialité, mentions légales, CGU : réutiliser le même CSS (importer `../politique-confidentialite/page.css` dans le `main.css` de la page, ou le déplacer en global au 2e usage). Ajouter le slug à `NAV_ACTIVE` ; le hero est un `.hero-photo` (voir « Hero photo »), qui gère seul le décalage sous la navbar.
- Balisage : `header.hero-photo.hero-photo--{mentions-legales→legales | conditions-utilisation→cgu | confidentialite}` (`aria-labelledby="{slug}-title"`) : fil d'Ariane `Accueil › {page}`, eyebrow « Informations légales », `h1.hero-photo__title` (mot accentué en `<em>`) ; **aucun** sous-titre ni méta dans le hero. La ligne méta (date · version, ou `[À COMPLÉTER PAR L'ONG]`) est le 1er enfant de `article.legal-content` : `p.legal-meta`. Puis `div.legal-main.container` > `aside.legal-sidebar` > `nav.legal-toc[aria-label]` (`p.legal-toc__title` + `ul.legal-toc__list` d'ancres) + `article.legal-content`.
- Page légale provisoire (V33 : mentions-legales, conditions-utilisation) : `main.css` = imports globaux + `../politique-confidentialite/page.css` ; bandeau `.legal-box[role=note]` « Contenu provisoire » en tête, chaque section ne contient que `[À COMPLÉTER PAR L'ONG]`.
- Contenu : `section.legal-section#ancre` > `h2.legal-section__title` (+ `h3.legal-section__subtitle`) ; encadré `.legal-box` (+ `.legal-box__list`). Une entrée du sommaire par `id` de section.
- Sommaire en colonne sticky (≥ 901 px), au-dessus du contenu en dessous. Jamais de texte juridique inventé : `[À COMPLÉTER]` + `A-FOURNIR.md`.

## Page 404 (`404.html`, à la racine)
- Sur un hébergeur statique, `404.html` est servi automatiquement à la racine ; si le site est servi depuis un sous-dossier, les chemins doivent être adaptés.
- Ressources et liens écrits à la main dans `404.html` : chemins absolus depuis la racine (`/styles/404/main.css`, `/pages/actions.html`), car la page est servie sous l'URL demandée (n'importe quelle profondeur). Les partials injectés (navbar, menu mobile, footer) restent relatifs (`{{root}}` = vide) : ils ne s'affichent correctement que si l'URL demandée est à la racine.
- Le plan du site de la 404 ne liste que les pages existantes (`docs/SITEMAP.md`) : l'ajouter/retirer à chaque création de page. `NAV_ACTIVE["404"] = ""` (aucun lien marqué).

## Build de production (tools/bundle.py)
- `python3 tools/build.py --prod` : reconstruit `dist/` (copie de index, 404, pages, assets, scripts, sitemap, robots) ; chaque `styles/<slug>/main.css` devient `dist/styles/<slug>.css` et les `<link>` des pages de `dist/` sont réécrits. Les sources ne sont jamais modifiées ; sans `--prod`, le mode dev (`main.css` + `@import`) est inchangé.
- `python3 tools/bundle.py [slug…]` (`--root`, `--out`) : seulement les CSS. Résout les `@import` (ordre conservé, récursif), réécrit les `url()` relatifs pour `dist/styles/` (`data:`, `http(s):`, `/…`, `#…` intacts), supprime commentaires et espaces superflus.
- Un nouveau CSS doit être atteint par `@import` depuis `main.css` (jamais de `<link>` multiple) ; `url()` en chemin relatif au fichier qui le contient.
- `dist/` est régénéré à chaque `--prod` (supprimé puis recréé) : ne rien y éditer, ne pas le versionner.
- Vérifier : aucun `@import` dans `dist/styles/*.css` (`grep -c @import`), `python3 tools/check.py` sur les sources.

## Hero photo (`.hero-photo`, `styles/hero-photo.css`)
- Hero commun à toutes les pages sauf `index.html` (404 et maintenance exclues) : fil d'Ariane → eyebrow → H1. **Rien d'autre** : ni sous-titre, ni bouton, ni stats, ni liens d'ancre, ni carte, ni figure. Contenu retiré d'un hero = **déplacé dans la 1re section suivante**, jamais supprimé.
- Balisage :
  `<header class="hero-photo hero-photo--{slug}" aria-labelledby="{slug}-title">` > `div.container.hero-photo__inner` > `nav.hero-photo__breadcrumb[aria-label="Fil d'Ariane"] > ol[role=list] > li` (« Accueil » → `../index.html`, puis `span[aria-current=page]`) ; `div.eyebrow` (`eyebrow__line` + `eyebrow__label`) ; `h1#{slug}-title.hero-photo__title` (mot clé en `<em>`).
- CSS : `styles/hero-photo.css` est un fichier **séparé**, chargé par `<link>` après le CSS de page (pas de `@import`). Le composant porte voile, dégradé haut (navbar), `padding-top: var(--navbar-h)`, typographie, responsive (`clamp`) et `@media print` (fond supprimé). Le modificateur `.hero-photo--{slug}` ne définit que `--hero-photo-img` (URL Unsplash) et `--hero-photo-pos` (cadrage, à varier d'une page à l'autre). Pas de classe du hero à ajouter à la règle de décalage de `navbar.css` : le composant s'en charge.
- Format d'image : `https://images.unsplash.com/photo-<id>?auto=format&fit=crop&q=75&w=1600&h=900`. Pool (n'inventer aucun identifiant) : `1571417814270-5cfb10916e02`, `1473649085228-583485e6e4d7`, `1680713660046-67b7350ed679`, `1512596478480-88ba44446471`. Photos provisoires (voir `A-FOURNIR.md`).
- Migration d'une page : remplacer le `<header>`, supprimer les règles `.xxx-hero*` de son CSS (y compris dans la liste de décalage de `navbar.css`) et sa règle dans `hero-photo.css`, ajouter son modificateur. Les anciennes règles `.xxx-hero` restent dans `hero-photo.css` jusqu'à la conversion de leur page (H2–H8).
- **Gabarit des pages mission** (`pages/mission-sante.html`, à copier pour Droits humains et Éducation) : le hero est un `.hero-photo` avec un modificateur **par mission** (`hero-photo--mission-sante`, puis `--mission-droits`, `--mission-education`, chacun avec sa photo du pool) ; fil d'Ariane `Accueil › Nos missions › {Mission}` ; eyebrow `Mission 0X / 03 · {Mission}` (remplace l'ancien numéro + badge) ; id `mission-title`. Chapo, boutons et faits clés vont dans `div.mission-detail__intro` en tête de la section « L'enjeu » ; le sélecteur de missions reste juste sous le hero. Ne plus utiliser `.mission-detail__hero`, `__breadcrumb`, `__numbering`, `__badge` (supprimés).
- Barre d'ancres sortie d'un hero (ex. `.missions-anchors` de `nos-missions.html`) : elle ouvre la 1re section suivante, ses classes ne portent plus `hero` et ses couleurs sont celles d'un fond clair.

## Typographie (T7)
- Échelle unique dans le `:root` canonique : titres `--fs-h1…h4` (+ `--fw-hN`, `--lh-hN`, `--ls-hN`), `--fs-lede`, `--fs-body` (16 px), `--fs-base-sm`/`--fs-sm`/`--fs-xs` (14/13/12 px, plancher 12 px), `--fs-eyebrow`, `--fs-quote(-sm)`, `--fs-stat(-sm)`, `--measure` (48ch ≈ 70 caractères).
- Un titre prend la marche de son rôle visuel : classe à ajouter à la liste du bloc « Typographie (T7) » (fin de chaque feuille, identique partout). Ne jamais écrire de `font-size` en dur sur un titre.
- Corps de texte ≥ 16 px ; petit texte (légendes, notes, footer) 12–14 px ; liens dans un `<p>` : soulignés.

## Rythme vertical (T8)
- Padding de section : `padding-block: var(--section-pad-y)` (variantes `-compact`, `-band`) ; jamais de `rem` en dur ni de palier par media query. Détails et tableau mesuré : `docs/RYTHME.md`.
- Dans un en-tête : eyebrow, `h2`, `p`, bloc = frères directs, sans `margin` ni `gap` propres (le bloc T8 règle les écarts). Deux sections voisines sans fond propre : mettre `padding-top: 0` à la seconde.

## Cohérence visuelle (chantier clos en V122)
Décisions de la charte, vérifiées par `python3 tools/regress.py` (Playwright, serveur HTTP local, 15 contrôles, sortie OK/KO, code 1 si KO ; `--quick` = 1280 px seul pour le débordement, `-v` = détail des KO). À lancer avant toute livraison ; **0 KO exigé**.
- Palette : marine `--clr-secondary`, accent `--clr-primary`, or du logo ; Cormorant Garamond (titres) + Outfit (texte). Tokens `:root` identiques dans les feuilles (référentiel : docs/DESIGN-TOKENS.md). Aucune variable `var(--x)` sans définition ni repli.
- Header 100 px au sommet / 80 px après défilement (≥ 1024 px), jamais de retour à la ligne.
- Cartes (bloc T10, docs/CARTES-AUDIT.md) : fond blanc, bordure 1px rgba(16,35,63,0.18), ombre 0 1px 3px rgba(16,35,63,0.08) ; survol = bordure rgba(16,35,63,0.32) + ombre 0 2px 8px rgba(16,35,63,0.10), sans déplacement. Toute nouvelle classe de carte s'ajoute au bloc T10 dans les 21 feuilles.
- Boutons ghost : bordure visible par défaut ; survol = fond seulement (bordure inchangée).
- Citations sur fond marine : pas de filet rose latéral. Hero d'accueil : pas de bandeau de chiffres. Eyebrows d'accueil complets (ligne + libellé + point) et à signature unique.
- Rythme vertical : tokens `--rhythm-*` (docs/RYTHME.md) ; section Mission de À propos mesurée (eyebrow→titre, paragraphe→paragraphe). Section Valeurs : fond `--clr-section-alt` (aucun canal > 244).
- Héros photo (`.hero-photo`, h1, ≥ 200 px) sur toutes les pages de `pages/` sauf maintenance.
- Mouvement (24D) : durées/courbes par tokens (`--dur-*`, `--ease-*`), aucun déplacement au survol, bloc « Mouvement (24D) » (mouvement réduit) identique dans toutes les feuilles. Survol réservé à `@media (hover:hover)` (24B). Focus clavier uniforme (24A).
- Aucun défilement horizontal de 320 à 1920 px.
- Limites connues : `tools/check.py` n'existe pas dans le projet (la section « Contrôle » ci-dessus est historique) ; regress.py ne contrôle que la 1re instance de chaque classe de carte par page et 4 boutons ghost par page.

