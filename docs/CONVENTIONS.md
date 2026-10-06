# Conventions — Lato Corps (site statique HTML/CSS/JS)

## Arborescence
- Pages : `pages/<slug>.html` (à plat, ressources en `../`). Exception : `404.html` à la racine.
- CSS : `styles/<slug>/main.css` (imports globaux + `page.css`). JS : `scripts/pages/<slug>/` ou `scripts/components/`.
- Prototypes sources : `_archive/prototype/<slug>.html` (archivés, lecture seule, ne jamais lier depuis le site).

## Règles
1. **Tokens uniquement** : `styles/global/variables.css` (`--clr-*`, `--font-display`, `--font-body`, `--radius-*`, `--shadow-*`, `--container-max`, `--section-pad-*`). Pas de couleur en dur dans les CSS de page.
2. **Zéro dépendance externe** : pas de CDN, Google Fonts, Remixicon CDN, GTM/analytics, image distante. Tout en local dans `assets/`.
   *Exception provisoire (V47, demande client)* : les photos de contenu sont des images distantes LoremFlickr (`https://loremflickr.com/<l>/<h>/<mots-clés>?lock=<n>`, le paramètre `lock` fige l'image). À remplacer par de vraies photos locales avant la mise en ligne.
3. **Pas de CSS/JS inline** (sauf JSON-LD). Nommage BEM.
4. **Contenu** : textes des prototypes repris tels quels (typographie française : espaces insécables avant `; : ? !`, guillemets « »). Ne jamais inventer chiffres, noms, dates, textes juridiques → marqueur `[À COMPLÉTER]` + entrée dans `docs/A-FOURNIR.md`.
5. **Images** : tant qu'aucune photo n'est fournie, placeholder CSS (`.media-placeholder` ou pattern `*__bg-placeholder` de la home) + entrée dans `A-FOURNIR.md`.
   Toute `<img>` hors première vue : `loading="lazy" decoding="async"` + `width`/`height` (ratio intrinsèque du fichier, `placeholder.svg` = 800 × 600 ; CSS global `img { height: auto }`) ; hero, avatars du hero et logo de la navbar restent sans `lazy`. À mettre à jour quand une vraie photo remplace un placeholder.
6. **Accessibilité** : `lang="fr"`, skip-link, un seul `<h1>`, landmarks, `aria-current="page"` sur la page courante, `alt` (vide si décoratif), focus visible, `prefers-reduced-motion`.
7. **Chaque page** : `<title>` « Titre — Lato Corps ONG », meta description, viewport `width=device-width`.
8. **Un prompt = une tâche.** Pas de refonte opportuniste.

## Conversion d'un prototype (méthode rapide)
`python3 tools/convert_proto.py <prototype> <slug>` fait la partie mécanique (retire tracking/CDN/`:root`, remplace les variables par les tokens du site **par valeur**, crée page/CSS/JS, remplace les images distantes) et écrit un rapport `docs/conversions/<slug>.md` : **c'est ce rapport qui liste le reste à faire**. Ne pas relire tout le prototype : travailler à partir du rapport et de `pages/<slug>.html`.

## Économie de contexte (important pour les sessions)
- `index.html` fait 143 Ko : ne jamais l'ouvrir en entier. Utiliser `grep -n` / `sed -n 'a,bp'`.
- Ne lire que les fichiers cités dans le prompt.
- Ne pas faire de captures/rendus sauf si le prompt le demande.

## Hero sous la navbar fixe (toutes les pages internes)
- La navbar est `position: fixed` : elle ne prend plus de place dans le flux. Le décalage vient d'**une seule règle globale** (`styles/global/components/navbar.css`, section « Header fixe ») : `.hero, .page-hero, .about-hero, .missions-hero { padding-top: var(--navbar-h); }`.
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
- **Bloc meta du `<head>`** : chaque page contient `<!-- @partial:meta:start -->` … `<!-- @partial:meta:end -->` juste après `<title>` (canonical, `og:title/description/type/url/image`, `twitter:card`, `theme-color`), généré par `build.py` depuis le dictionnaire `META` (clé = nom de page ; `title`, `description`, `og_image`) et `SITE_URL`. `title`/`description` de `META` = ceux de la page (le build échoue sinon) : modifier les deux ensemble. Nouvelle page = nouvelle entrée `META` + marqueurs. Le bloc contient aussi du JSON-LD généré (seul `<script>` inline autorisé : `application/ld+json`) : `NGO` sur `index.html` (constante `ORG` de `build.py` : nom, logo, e-mail, téléphone du footer, rien d'autre ; à resynchroniser si le footer change) et `BreadcrumbList` sur les pages intérieures indexables (Accueil > `parent` > page ; `parent` = clé `META` d'une vraie page, `None` = directement sous l'accueil ; libellés = `title` sans « — Lato Corps ONG »). Pas de JSON-LD sur 404/maintenance. Le bloc contient aussi `<link rel="preload" as="font" crossorigin>` pour Outfit 400 et Cormorant Garamond 500 (constante `FONT_PRELOAD` de `build.py`, mêmes fichiers que `fonts.css` ; si un `@font-face` critique change, mettre à jour les deux), et `<link rel="icon">` (`assets/images/favicon.svg`, dérivé de `logo.svg` ; chemin absolu `/…` sur la 404). `python3 tools/build.py --sitemap` (avec `--check` : n'écrit rien) génère `sitemap.xml` et `robots.txt` à la racine : pages hors `NOINDEX` et 404, URL = `SITE_URL` + chemin, sans `lastmod` ; à relancer à chaque page ajoutée/retirée ou changement de `SITE_URL`. `NOINDEX` (404, maintenance) : `<meta name="robots">` à la place de canonical/`og:url`. Image par défaut : `assets/images/og-default.png` (à fournir, `A-FOURNIR.md`) ; `og_image` = chemin depuis la racine pour une page précise.
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
- Pour politique de confidentialité, mentions légales, CGU : réutiliser le même CSS (importer `../politique-confidentialite/page.css` dans le `main.css` de la page, ou le déplacer en global au 2e usage). Ajouter le slug à `NAV_ACTIVE` ; le hero `.legal-hero` est déjà dans la règle de décalage de `navbar.css`.
- Balisage : `header.legal-hero` > `.container` > `h1.legal-hero__h1` (mot accentué en `<em>`) + `p.legal-hero__meta` (date · version) ; puis `div.legal-main.container` > `aside.legal-sidebar` > `nav.legal-toc[aria-label]` (`p.legal-toc__title` + `ul.legal-toc__list` d'ancres) + `article.legal-content`.
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
