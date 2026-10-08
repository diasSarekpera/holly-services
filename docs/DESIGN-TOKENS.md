# DESIGN-TOKENS — référentiel visuel de Holly Services

> Tâche 1/25 (V59 → V60). **Source de vérité visuelle** pour les tâches 2 à 25. Document produit par audit en lecture seule : aucun fichier CSS/HTML n'a été modifié. Les valeurs « cible » ci-dessous sont des **décisions** à appliquer sans les rediscuter ; les points marqués **(à valider)** demandent un contrôle visuel dans la tâche qui les applique.

## 0. Méthode et constats préalables

**La doc est en retard sur les fichiers réels** (règle 1 : les fichiers font foi) :

- Il n'existe **ni `tools/`, ni `partials/`, ni `styles/global/`, ni `styles/<slug>/main.css`**. `docs/CONVENTIONS.md` et `docs/SUIVI.md` décrivent une structure source qui n'est pas dans ce zip.
- Chaque page charge **un seul fichier `styles/<slug>.css` déjà concaténé et minifié** (+ `hero-photo.css` sur les pages internes). Le CSS global (tokens, navbar, menu mobile, footer, boutons, formulaires, icônes) est donc **dupliqué dans les 20 fichiers CSS** ; navbar, menu mobile et footer sont en plus dupliqués dans les 20 pages HTML.
- Conséquence pour les tâches suivantes : toute modification d'un bloc partagé doit être **scriptée sur les 20 CSS** (et vérifiée par script). Les 3 CSS légaux (`mentions-legales`, `conditions-utilisation`, `politique-confidentialite`) sont **octet pour octet identiques** (50 814 o).
- `404.html` charge ses ressources par chemins absolus (`/styles/404.css`, 29 liens `href="/…"`) : la page s'affiche sans style hors de la racine d'un serveur (constaté en ouverture locale `file://`). Hors périmètre, noté.

**Méthode des chiffres.** Les 20 CSS ont été analysés avec `tinycss2` : 2 773 règles **uniques** (405 règles sont communes à ≥ 19 fichiers = socle global ; 2 196 n'existent que dans un seul fichier). Les comptes ci-dessous sont des **déclarations dans des règles uniques** (le socle partagé compte une fois, pas 20) ; la colonne « fichiers » indique dans combien de CSS la valeur apparaît. Totaux : 38 couleurs hexadécimales + 264 `rgba()` en dur dans les règles (hors définition des tokens).

**Vérification visuelle réelle** (Chromium headless, 20 pages × 360 / 768 / 1024 / 1366 / 1920, `scrollWidth` mesuré + capture de l'accueil). Constats mesurés : voir §12. Les rendus n'ont pas tous été regardés à l'œil : seule la capture de l'accueil à 1366 px (prise pendant l'animation d'entrée) a été consultée.

## 1. Palette cible

Identité : marine en fond sombre, framboise en accent, or du logo (uniquement dans le logo SVG, aucun token or en CSS aujourd'hui). **11 couleurs hexadécimales en dur distinctes (hors tokens) + 129 `rgba()` distincts** aujourd'hui → cible ci-dessous.

| Token cible | Valeur | Rôle | Remarque |
|---|---|---|---|
| `--clr-secondary` | #10233F | Marine : fonds sombres, titres | inchangé |
| `--clr-secondary-light` | #1C355C | Marine clair : survol/variantes sur fond sombre | inchangé |
| `--clr-secondary-deep` | #0A172A | Marine profond : bas de dégradés, pied de page | **nouveau** — absorbe #0E1E34, rgba(14,31,56), rgba(9,20,36), rgba(8,17,32) |
| `--clr-secondary-soft` | #EAF0F8 | Pastille/fond bleuté très clair | inchangé |
| `--clr-primary` | #C8184A | Framboise : accent, CTA don | **valeur unique** (contraste 5,70:1 sur blanc) — voir §12 n°9 |
| `--clr-primary-dark` | #A3154C | Survol / actif du CTA primaire | inchangé (7,58:1) ; absorbe #96003A et rgba(170,20,75) |
| `--clr-primary-soft` | #FCE4EC | Fond rose très clair (badges, états) | inchangé |
| `--clr-accent` | #6E8B7B | Vert sauge : décor, icônes, fonds sombres | 3,72:1 sur blanc : **interdit en texte sur fond clair** |
| `--clr-accent-dark` | #557062 | Vert sauge texte sur fond clair | 5,41:1 ; absorbe #587567 |
| `--clr-accent-soft` | #EEF3F0 | Fond sauge clair | inchangé |
| `--clr-urgent` | #C2410C | Alerte / urgence | inchangé ; `--clr-urgent-tint` #FFEDD5 |
| `--clr-white` | #FFFFFF | Cartes, texte sur sombre | absorbe #FFF/#fff (14 occurrences) |
| `--clr-off-white` | #F8F9FB | Fond de section « neutre » (sans cartes) | 1,06:1 avec le blanc → **ne pas mettre de cartes blanches dessus** |
| `--clr-surface` | #F3F5F7 | Fond de champ, puce neutre, survol des boutons ghost | inchangé |
| `--clr-section-alt` | #EDF0F4 | **Fond de section derrière des cartes** (charte) | **nouveau token** — aujourd'hui en dur 1× (`.values`, a-propos) |
| `--clr-text` | #162033 | Texte courant | inchangé |
| `--clr-text-soft` | #5C667A | Texte secondaire | 5,77:1 sur blanc, 5,05:1 sur #EDF0F4 |
| `--clr-field-border` | #7B8798 | Bordure de champ de formulaire | 3,65:1 (≥ 3:1 exigé pour les composants) |
| `--clr-divider` | rgba(16,35,63,0.08) | Séparateurs, filets internes | **renomme l'actuel `--clr-border`** (57 usages) |
| `--clr-border` | rgba(16,35,63,0.18) | Bordure de carte / champ / bouton secondaire | **nouvelle valeur** (aujourd'hui 0.08) |
| `--clr-border-hover` | rgba(16,35,63,0.32) | Bordure de carte au survol | **nouveau** (charte) |
| `--clr-border-btn` | rgba(16,35,63,0.38) | Bordure du bouton ghost sur fond clair | valeur actuelle de `.btn--ghost` (20 fichiers), conservée |


**Échelles de transparence** (le reste est fusionné vers elles ; voir §10 pour le détail) :

| Famille | Pas autorisés | Usage |
|---|---|---|
| Blanc sur fond sombre | 0.06 · 0.12 · 0.32 · 0.55 · 0.72 · 0.88 | 0.06 fond de carte sombre · 0.12 filet / fond de survol · 0.32 **bordure ghost sombre** · 0.55 texte atténué (minimum) · 0.72 texte secondaire · 0.88 texte principal |
| Marine sur fond clair | 0.08 · 0.18 · 0.32 · 0.38 · 0.55 · 0.88 | filet · bordure carte · survol carte · bordure bouton · texte atténué · voile |
| Framboise (rgba 200,24,74) | 0.08 · 0.14 · 0.28 · 0.92 | fond léger · `--clr-primary-overlay` · bordure teintée · pastille pleine |
| Sauge (rgba 110,139,123) | 0.08 · 0.14 · 0.28 · 0.92 | idem (pastille pleine = rgba 85,112,98,0.92 de `--clr-accent-dark`) |


Les noms `--nb --nbm --nm --nd --ndd` (blancs du pied de page) deviennent des alias de cette échelle : `--nb`=0.06, `--nbm`=0.12, `--ndd`/`--nd`=0.55, `--nm`=0.72.

## 2. Typographie cible

Familles : `--font-display` « Cormorant Garamond » (titres), `--font-body` « Outfit » (texte). Aujourd'hui : 104 déclarations display, 45 body, 2 `inherit`, **1 `"Cormorant Garamond"` en dur** (à remplacer par le token).

| Token | Valeur | Usage |
|---|---|---|
| `--fs-xs` | 0.75rem (12 px) | **plancher absolu** : eyebrows, légendes, badges |
| `--fs-sm` | 0.8125rem (13 px) | UI dense : boutons, étiquettes |
| `--fs-base-sm` | 0.875rem (14 px) | texte secondaire, liens de menu |
| `--fs-body-sm` | 0.9375rem (15 px) | texte de carte |
| `--fs-body` | 1rem (16 px) | texte courant, champs de formulaire (≥ 16 px : pas de zoom iOS) |
| `--fs-lead` | 1.125rem (18 px) | chapô, 1er paragraphe de section |
| `--fs-h4` | 1.25rem | titres de carte, H4 |
| `--fs-h3` | 1.5rem | H3 |
| `--fs-h2` | clamp(2rem, 4vw, 2.75rem) | H2 (valeur déjà présente dans 20 fichiers) |
| `--fs-h1` | clamp(2.25rem, 4.5vw, 3.5rem) | H1 / titres de hero (valeur la plus proche des 3 clamp existants) |
| `--fs-display` | 2.5rem · 3rem · 3.5rem | chiffres clés, citations d'ouverture |


Échelle de ligne : **1** (icônes, chiffres) · **1.15** (titres display) · **1.3** (sous-titres) · **1.5** (UI) · **1.6** (texte compact) · **1.75** (texte courant). Graisses : 300 / 400 / 500 / 600 / 700 (le `bold` en dur → 700). Interlettrage : **-0.02em** (titres XL) · **-0.01em** (titres M) · **0** · **0.02em** (boutons, UI) · **0.06em** (majuscules / eyebrows).

## 3. Espacement (échelle 4 / 8 px)

Échelle : `--sp-1` 0.25rem (4) · `--sp-2` 0.5rem (8) · `--sp-3` 0.75rem (12) · `--sp-4` 1rem (16) · `--sp-5` 1.25rem (20) · `--sp-6` 1.5rem (24) · `--sp-8` 2rem (32) · `--sp-10` 2.5rem (40) · `--sp-12` 3rem (48) · `--sp-16` 4rem (64) · `--sp-20` 5rem (80) · `--sp-24` 6rem (96). Micro-valeurs autorisées : 2 px.

**Mesure actuelle** : 1526 valeurs de `padding / margin / gap` pour 68 valeurs distinctes ; **332 (22 %) sont hors grille 4 px** (`0.35rem`, `0.55rem`, `0.7rem`, `1.1rem`…).

**Rythme vertical des sections** (charte, à appliquer partout) :

| Élément | Desktop | Mobile (≤ 767 px) |
|---|---|---|
| eyebrow → titre | 1.25rem | 1rem |
| titre → premier paragraphe | 1.75rem | 1.25rem |
| paragraphe → paragraphe | 1rem | 1rem |
| dernier paragraphe → bloc suivant | 2rem | 1.5rem |
| bloc → média | 3rem | 2rem |
| padding vertical de section `--section-pad-y` | 6rem (≥ 1024) · 5rem (≤ 1023) · 4rem (≤ 767) · 3.5rem (≤ 479) | déjà en place dans les `:root` (valeurs conservées) |
| padding vertical de hero | `clamp(3rem,7vw,5rem)` bas · `clamp(2.5rem,6vw,4rem)` haut (composant `.hero-photo`) | idem |


Règle : **une seule marge entre deux éléments** (margin-bottom du premier, jamais en plus le margin-top du suivant) ; `gap` des conteneurs flex/grid en priorité.

## 4. Rayons — 3 valeurs

| Token | Valeur | Usage |
|---|---|---|
| `--radius-sm` | 4px | badges, puces, champs, boutons, icônes encadrées (absorbe `--radius-badge`) |
| `--radius-md` | 6px | cartes, médias, blocs (absorbe `--radius-card`) |
| `--radius-full` | 50%  (999px pour les pilules) | avatars, points, séparateurs ronds |


Aujourd'hui : `--radius-badge` 65×, `--radius-sm` 61×, `--radius-card` 54×, `--radius-md` 28× (5 fichiers), `50%` 39×. **`--radius-badge` = `--radius-sm` (4 px) et `--radius-card` = `--radius-md` (6 px)** : 4 noms pour 2 valeurs. Seul cas hors tokens : `border-radius:0` et 3 rayons asymétriques (`.temoignage-card__accent-line`, …) à conserver.

## 5. Ombres — 3 valeurs + 1 anneau

| Token | Valeur | Usage |
|---|---|---|
| `--shadow-card` | 0 1px 3px rgba(16,35,63,0.08) | carte au repos (charte) |
| `--shadow-card-hover` | 0 2px 8px rgba(16,35,63,0.10) | carte au survol, **sans déplacement** (charte) |
| `--shadow-popover` | 0 8px 24px -6px rgba(5,12,24,0.45) | menus déroulants, menu mobile, bouton retour haut |
| `--ring-focus` | 2px solid var(--clr-primary) + offset 2px | focus clavier (déjà global) ; les anneaux `0 0 0 3px …` de champs sont conservés |


Aujourd'hui : **22 ombres distinctes**. Mapping complet en §10.3. Les ombres **colorées** (`0 4px 14px rgba(194,24,91,0.18)` ×4 sur les boutons primaires, `0 2px 8px var(--clr-primary-overlay)` ×4, `0 3px 10px …overlay`) relèvent de l'effet « SaaS » interdit → `none`.

## 6. Bordures

| Cas | Cible |
|---|---|
| Carte (repos) | `1px solid var(--clr-border)` (0.18) |
| Carte (survol) | `border-color: var(--clr-border-hover)` (0.32) + `--shadow-card-hover` |
| Séparateur interne | `1px solid var(--clr-divider)` (0.08) |
| Champ de formulaire | `1px solid var(--clr-field-border)` ; 2 px + anneau au focus |
| Bouton ghost clair | `1px solid var(--clr-border-btn)` (0.38) ; **bordure inchangée au survol** |
| Bouton ghost sombre | `1px solid rgba(255,255,255,0.32)` ; **bordure inchangée au survol**, fond `rgba(255,255,255,0.12)` |
| Épaisseurs | 1px partout ; 2px réservé au focus / état actif. **`1.5px` supprimé** (8+2+2 occurrences → 1px, sauf ghost sombre actuel 1.5px → 1px) |
| Bordure à gauche accent | interdite sur les citations marine ; autorisée seulement sur encadrés d'information sur fond clair (`3px solid var(--clr-accent)`) |


Aujourd'hui (64 recettes `border` distinctes) : `1px solid var(--clr-border)` 57×, `var(--clr-border-strong)` 24×, `1px solid rgba(16,35,63,0.18)` en dur 14× (8 fichiers), `1.5px solid var(--clr-border-strong)` 8×, `1px solid var(--clr-secondary-soft)` 5×, `1px solid var(--clr-surface)` 7×, filets pointillés quasi invisibles `1px dashed rgba(110,139,123,0.08)` 3×.

## 7. Transitions

| Token | Valeur | Usage |
|---|---|---|
| `--dur-1` / `--transition-ui` | 0.2s ease | couleur, fond, bordure, ombre (remplace `--transition-cta` 0.25s) |
| `--dur-2` | 0.3s var(--ease-out) | opacité, menus, accordéons, translateX d'icône de lien |
| `--dur-3` | 0.5s var(--ease-out) | zoom d'image au survol (scale ≤ 1.04), apparitions |
| `--ease-out` | cubic-bezier(0.16,1,0.3,1) | inchangé |


Règles : jamais `transition: all` (1 occurrence à corriger) ; **aucun `transform: translateY` au survol d'une carte** ; `translateX(3px)` autorisé uniquement sur la flèche d'un lien (9 règles, 20 fichiers : conservé) ; `prefers-reduced-motion` déjà géré (45 règles, `0.01ms`).
Aujourd'hui : **88 recettes `transition` distinctes** ; durées 0.18 / 0.2 / 0.22 / 0.25 / 0.3 / 0.35 / 0.4 / 0.5 / 0.7 s ; `border-color 0.3s` sans courbe (404).

## 8. Z-index — échelle

| Niveau | Valeur | Éléments |
|---|---|---|
| Fond décoratif | -1 | `.navbar::before` |
| Base | 0 / 1 | contenu de hero, calques (39× la valeur 1) |
| Local | 2 | badges et pastilles posés sur image (`*__cat`, `*__kpi`, `*__badge`) — **unifier les 2 et 3 actuels** |
| Sous-menu | 20 | `.navbar__dropdown` |
| Retour haut | 60 | `.back-to-top` |
| Navbar | 100 | `.navbar` |
| Menu mobile | 200 | `.mobile-menu` |
| Lien d'évitement | 999 | `.skip-link` |


Valeurs actuelles : 1 (39×), 0 (9×), 2 (6×), 3 (5×), 20, 60, 100, 200, 999, -1. Cohérent au niveau global ; seul l'écart 2/3 entre badges est à unifier (→ 2).

## 9. Conteneurs et breakpoints

| Token | Valeur | Usage |
|---|---|---|
| `--container-max` | 1280px | conteneur principal (7 sélecteurs, 19 fichiers) |
| `--container-narrow` | 56rem (896 px) | citation, formulaire, onglets — absorbe `900px` (1×) |
| `--container-reading` | 45rem (720 px) | texte long (`.container-reading`, inchangé) |
| `--gutter` | 2rem ≥ 1024 · 1.5rem 640–1023 · 1.25rem ≤ 639 · 1rem ≤ 359 | **un seul** jeu de marges latérales (remplace `--container-pad` 1.5rem + `--section-pad-x` 2 / 1.25 / 1 rem) |
| `--navbar-h` / `--navbar-h-compact` | 100 / 80 px (≥ 1024) · 76 / 64 px (≤ 767) | déjà conformes à la charte (mesuré : navbar 101 px = 100 + 1 px de filet à 1024-1920, 77 px à 360) |


**Jeu de breakpoints cible** (approche descendante `max-width`, valeur = seuil − 1 px pour supprimer les paires collées) :

| Nom | Largeur | Requête | Rôle |
|---|---|---|---|
| xs | < 480 | `(max-width:479px)` | mobile compact (320-479) |
| sm | 480–767 | `(max-width:767px)` | mobile large : menu burger, 1 colonne |
| md | 768–1023 | `(max-width:1023px)` | tablette : 2 colonnes, menu burger |
| lg | ≥ 1024 | `(min-width:1024px)` | desktop : menu déployé, header 100 px |
| xl | 1280–1439 | `(min-width:1280px)` | conteneur plein, compaction header niveau 2 |
| 2xl | ≥ 1440 | `(min-width:1440px)` | header complet, logo 84 px |


Compaction du header entre 1024 et 1439 px : **2 paliers** (1024–1279 et 1280–1439) au lieu des 4 actuels (1024-1099, 1024-1199, 1024-1439, ≤1279).

Breakpoints réellement utilisés (**24 valeurs**, décompte = nombre de règles uniques concernées) :

| Valeur px | Règles | Cible |
|---|---|---|
| 359 | 13 | max-width:479 |
| 375 | 14 | max-width:479 |
| 430 | 24 | max-width:479 |
| 479 | 55 | max-width:479 |
| 480 | 40 | min-width:480 |
| 520 | 2 | min-width:480 / max 639 |
| 560 | 6 | max-width:639 |
| 600 | 31 | max-width:639 |
| 639 | 143 | max-width:639 |
| 640 | 125 | min-width:640 |
| 700 | 11 | max-width:767 |
| 767 | 137 | max-width:767 |
| 768 | 16 | min-width:768 |
| 860 | 5 | max-width:1023 (à valider) |
| 899 | 41 | max-width:1023 (à valider) |
| 900 | 57 | min-width:1024 (à valider) |
| 901 | 2 | min-width:1024 (à valider) |
| 1023 | 84 | max-width:1023 |
| 1024 | 66 | min-width:1024 |
| 1099 | 14 | max-width:1279 (compaction header) |
| 1100 | 5 | min-width:1024 / max 1279 |
| 1199 | 9 | max-width:1279 (compaction header) |
| 1279 | 34 | max-width:1279 |
| 1439 | 10 | max-width:1439 |


⚠ Les paires `639/640` (143 / 125 règles), `767/768`, `479/480`, `1023/1024` font basculer deux pages **à 1 px d'écart** si un fichier utilise `max-width:639` et l'autre `min-width:640` : uniformiser en `max-width` seulement. Les `899/900/901` et `860` sont des bascules de colonnes **à valider visuellement** avant de les rattacher à 1023.

## 10. Tableaux « valeur actuelle → valeur cible »
Pour les tâches 2 à 13. Colonne « n » = déclarations dans des règles uniques ; « f » = nombre de fichiers CSS.

### 10.1 Couleurs

| Valeur actuelle | n · f | Valeur cible |
|---|---|---|
| #FFF / #fff | 14 · 19 f | `var(--clr-white)` |
| #C2185B (home.css, 6×) et `var(--clr-primary,#c2185b)` | 6 · 1 f | `var(--clr-primary)` |
| #96003A (home.css) · rgba(170,20,75,*) (1×) | 2 · 1 f | `var(--clr-primary-dark)` |
| #6E8B7B en dur (home.css, 4×) · `var(--clr-accent,#6e8b7b)` | 4 · 1 f | `var(--clr-accent)` |
| #587567 | 1 · 1 f | `var(--clr-accent-dark)` (#557062) |
| #EDF0F4 en dur (`.values`) | 1 · 1 f | `var(--clr-section-alt)` |
| #0A172A · #0E1E34 · rgba(14,31,56,*) · rgba(9,20,36,*) · rgba(8,17,32,*) · rgba(5,12,24,*) (fonds sombres) | 2+1+6+3+2+4 · 19 f | `var(--clr-secondary-deep)` (opaque) ; transparences → échelle marine |
| #000 (ombre, article) · rgba(0,0,0,0.15) | 5+2 · 1 f | `var(--clr-secondary)` à l'alpha voulu |
| #5B9EC9 · #7FBFE0 (bleus clairs, `camp-card--health`) | 2 · 1 f | **hors charte** : bleu absent de la palette → `--clr-secondary-light` ou `--partner-clr` (à valider) |
| `rgba(194,24,91,x)` (30×, 20 fichiers via `--clr-primary-overlay`) | 30 | `rgba(200,24,74,x)` : 0.05–0.10 → 0.08 · 0.12–0.18 → 0.14 · 0.25–0.35 → 0.28 · 0.88–0.92 → 0.92 |


Alphas du **blanc** (43 pas distincts aujourd'hui) :

| Alphas actuels | Cible | Type |
|---|---|---|
| 0.03 · 0.04 · 0.045 · 0.05 · 0.06 · 0.07 · 0.08 · 0.09 | 0.06 | fond de carte / champ sur sombre |
| 0.10 · 0.11 · 0.12 · 0.13 · 0.14 · 0.15 · 0.18 · 0.20 | 0.12 | filet, fond de survol |
| 0.25 · 0.32 · 0.35 · 0.40 · 0.42 | 0.32 | bordure ghost sombre |
| 0.45 · 0.48 · 0.50 · 0.52 · 0.55 · 0.58 | 0.55 | texte atténué (plancher) |
| 0.60 · 0.62 · 0.65 · 0.68 · 0.70 · 0.72 · 0.74 · 0.75 · 0.78 | 0.72 | texte secondaire |
| 0.80 · 0.82 · 0.85 · 0.88 · 0.90 · 0.92 · 0.95 | 0.88 | texte principal |


Alphas du **marine** (rgba 16,35,63) : 0.05 · 0.055 · 0.06 · 0.08 · 0.10 → **0.08** · 0.15 · 0.18 · 0.20 → **0.18** (14× : déjà la bordure de carte) · 0.32 · 0.35 → **0.32** · 0.38 · 0.40 → **0.38** · 0.45 · 0.55 · 0.62 · 0.70 → **0.55** · 0.80–0.97 → **0.88** (voile) ; 0.0 conservé (dégradés).

### 10.2 Tailles de police (hors échelle)

362 déclarations sont **déjà sur l'échelle** ; 231 sont hors échelle. Dont **16 tailles inférieures à 12 px (92 déclarations, 0.58rem à 0.72rem)** : voir §12 n°10. Les `clamp()` de titres (45 recettes distinctes, 54 déclarations, ex. `clamp(2.2rem,3.5vw,3.5rem)` ×1 dans 20 fichiers) sont à ramener à `--fs-h1` / `--fs-h2`.

| Valeur actuelle | n | f | Valeur cible |
|---|---|---|---|
| 0.6875rem | 20 | 20 | 0.75rem (plancher 12 px) |
| 0.6rem | 14 | 19 | 0.75rem (plancher 12 px) |
| 0.7rem | 12 | 20 | 0.75rem (plancher 12 px) |
| 0.8rem | 12 | 2 | 0.8125rem |
| 0.65rem | 10 | 19 | 0.75rem (plancher 12 px) |
| 0.85rem | 10 | 20 | 0.875rem |
| 0.72rem | 9 | 19 | 0.75rem (plancher 12 px) |
| 0.9rem | 9 | 20 | 0.875rem |
| 1.625rem | 9 | 19 | 1.75rem |
| 0.78rem | 8 | 19 | 0.75rem |
| 0.62rem | 8 | 19 | 0.75rem (plancher 12 px) |
| 1.875rem | 7 | 19 | 2rem |
| 1.3rem | 7 | 2 | 1.25rem |
| 1.375rem | 6 | 5 | 1.5rem |
| 0.68rem | 6 | 1 | 0.75rem (plancher 12 px) |
| 2.25rem | 5 | 20 | 2.5rem |
| 0.95rem | 5 | 19 | 0.9375rem |
| 1.2rem | 5 | 19 | 1.25rem |
| 1.05rem | 5 | 2 | 1rem |
| 1.1rem | 4 | 19 | 1.125rem |
| 0.8375rem | 4 | 19 | 0.8125rem |
| 1.15rem | 4 | 2 | 1.125rem |
| 5rem | 4 | 2 | décoratif (404 / chiffre géant) : laisser |
| 7rem | 3 | 2 | décoratif (404 / chiffre géant) : laisser |
| 1.0625rem | 3 | 3 | 1.125rem |
| 0.58rem | 3 | 1 | 0.75rem (plancher 12 px) |
| 1.6rem | 3 | 1 | 1.5rem |
| 1.8rem | 2 | 2 | 1.75rem |
| 1.55rem | 2 | 2 | 1.5rem |
| 0.64rem | 2 | 1 | 0.75rem (plancher 12 px) |
| 0.74rem | 2 | 1 | 0.75rem (plancher 12 px) |
| 0.82rem | 2 | 1 | 0.8125rem |
| 4rem | 2 | 2 | décoratif (404 / chiffre géant) : laisser |
| 2.75rem | 2 | 2 | 3rem |
| 1.35rem | 1 | 19 | 1.25rem |
| 1.175rem | 1 | 19 | 1.125rem |
| 1.0125rem | 1 | 19 | 1rem |
| 0.625rem | 1 | 19 | 0.75rem (plancher 12 px) |
| 0.66rem | 1 | 19 | 0.75rem (plancher 12 px) |
| 1.02rem | 1 | 19 | 1rem |
| 0.56rem | 1 | 19 | 0.75rem (plancher 12 px) |
| 1.1875rem | 1 | 1 | 1.25rem |
| 0.8438rem | 1 | 1 | 0.875rem |
| 1.4rem | 1 | 1 | 1.5rem |
| 0.84rem | 1 | 1 | 0.8125rem |
| 0.63rem | 1 | 1 | 0.75rem (plancher 12 px) |
| 0.88rem | 1 | 1 | 0.875rem |
| 0.55rem | 1 | 1 | 0.75rem (plancher 12 px) |
| 0.775rem | 1 | 1 | 0.75rem |
| 10rem | 1 | 1 | décoratif (404 / chiffre géant) : laisser |
| 1.45rem | 1 | 1 | 1.5rem |
| 0.57rem | 1 | 1 | 0.75rem (plancher 12 px) |
| 0.975rem | 1 | 1 | 1rem |
| 6rem | 1 | 1 | décoratif (404 / chiffre géant) : laisser |
| 8.5rem | 1 | 1 | décoratif (404 / chiffre géant) : laisser |
| 0.92rem | 1 | 1 | 0.9375rem |


### 10.3 Ombres

| Valeur actuelle | n | Valeur cible |
|---|---|---|
| `var(--shadow-md)` (0 2px 10px .05) | 24 | `var(--shadow-card)` |
| `0 1px 3px rgba(16,35,63,0.08)` en dur | 5 (3 f) | `var(--shadow-card)` |
| `var(--shadow-sm)` · `0 1px 3px rgba(16,35,63,0.05)` | 1+1 | `var(--shadow-card)` |
| `var(--shadow-card-hover)` (0 2px 8px .06) · `0 2px 8px rgba(16,35,63,0.06)` · `0 2px 8px rgba(16,35,63,0.10)` | 5+1+1 | `var(--shadow-card-hover)` (0.10) |
| `var(--shadow-lg)` · `var(--shadow-lg,var(--shadow-md))` (0 4px 16px .07) | 3+1 | `var(--shadow-card-hover)` (supprime le décollement visuel des hovers `erreur404-card`, `banner-card`, `partner-logo-tile`) |
| `0 4px 14px rgba(194,24,91,0.18)` · `0 2px 8px var(--clr-primary-overlay)` · `0 3px 12px var(--clr-primary-overlay)` · `0 3px 10px var(--clr-accent-overlay)` · `0 3px 10px var(--clr-secondary-overlay)` (ombres colorées) | 4+4+1+1+1 | `none` |
| `0 4px 16px rgba(5,12,24,0.32), 0 1px 4px …0.20` · `0 8px 24px -6px rgba(5,12,24,0.60), 0 2px 6px …0.35` | 1+1 (19 f) | `var(--shadow-popover)` |
| `inset 0 0 0 1.5px var(--clr-secondary)` · `0 0 0 1000px … inset` (hack autofill) | 1+2 | conservés (état sélectionné / autofill), 1.5px → 2px |
| `0 0 0 3px var(--clr-primary-soft)` · `0 0 0 3px rgba(194,24,91,0.08)` (anneau de champ) | 1+1 | `--ring-field: 0 0 0 3px rgba(200,24,74,0.14)` |
| `none` | 5 | conservé |


### 10.4 Rayons, bordures, interlettrage, interlignes

| Valeur actuelle | n · f | Valeur cible |
|---|---|---|
| `var(--radius-badge)` | 65 · 20 | `var(--radius-sm)` |
| `var(--radius-card)` | 54 · 19 | `var(--radius-md)` |
| `1px solid var(--clr-border-strong)` (0.14) | 24 · 20 | `1px solid var(--clr-border)` (0.18, nouvelle valeur) |
| `1px solid rgba(16,35,63,0.18)` en dur · 0.20 (`.value-card`) | 14 · 8 f | `1px solid var(--clr-border)` |
| `1.5px solid …` | 8+2+2 | `1px solid …` |
| `1px solid var(--clr-secondary-soft)` (cartes bénévolat) · `1px solid var(--clr-surface)` (7× rejoindre-équipe) · `1px solid transparent` (`.article-card`) | 5 · 7 · 1 | `1px solid var(--clr-border)` |
| `1px dashed rgba(110,139,123,0.08)` | 3+2 | `1px solid var(--clr-divider)` (le pointillé 0.08 est invisible) |
| `.btn--ghost-light` / `.article-campaign .btn--ghost` / `.cta-support__actions .btn--ghost` bordures 0.35 · 0.4 | 1+1+1 | `1px solid rgba(255,255,255,0.32)` |
| interlettrage -0.04 · -0.03 · -0.015 | 13+4+5 | -0.02em (XL) · -0.01em (M) |
| interlettrage 0.01 · 0.02 · 0.03 | 3+15+13 | 0.02em |
| interlettrage 0.04 · 0.05 · 0.06 · 0.08 (majuscules) | 8+7+14+4 | 0.06em |
| line-height 1.12 · 1.18 · 1.2 | 3+5+20 | 1.15 |
| line-height 1.25 · 1.3 · 1.4 | —+10+15 | 1.3 |
| line-height 1.45 · 1.5 · 1.55 | 4+6+5 | 1.5 |
| line-height 1.6 · 1.65 | 11+6 | 1.6 |
| line-height 1.7 · 1.75 · 1.78 · 1.8 | 7+14+7+15 | 1.75 |


### 10.5 Espacements hors grille 4 px

| Valeur actuelle | n | Valeur cible (arrondi au multiple de 4 px le plus proche) |
|---|---|---|
| 0.875rem | 64 | 0.75rem (12 px) en gap/padding compact · 1rem (16 px) en padding de carte |
| 0.35rem | 26 | 0.25rem (4 px) |
| 0.4rem | 24 | 0.5rem (8 px) |
| 0.6rem | 22 | 0.5rem (8 px) |
| 0.3rem | 19 | 0.25rem (4 px) |
| 0.55rem | 17 | 0.5rem (8 px) |
| 0.7rem | 17 | 0.75rem (12 px) |
| 0.2rem | 17 | 0.25rem (4 px) |
| 1.375rem | 15 | 1.5rem (24 px) |
| 0.65rem | 14 | 0.75rem (12 px) |
| 1.1rem | 13 | 1rem (16 px) |
| 0.15rem | 13 | 0.25rem (4 px) |
| 0.625rem | 10 | 0.75rem (12 px) |
| 0.9rem | 8 | 1rem (16 px) |
| 0.45rem | 7 | 0.5rem (8 px) |
| 1.125rem | 6 | 1.25rem (20 px) |
| 0.375rem | 5 | 0.5rem (8 px) |
| 0.8rem | 5 | 0.75rem (12 px) |
| 0.85rem | 5 | 0.75rem (12 px) |
| 0.28rem | 4 | 0.25rem (4 px) |
| 1.4rem | 3 | 1.5rem (24 px) |
| 6px | 3 | 0.5rem (8 px) |
| 5px | 2 | 0.25rem (4 px) |
| 10px | 2 | 0.75rem (12 px) |
| 0.22rem | 2 | 0.25rem (4 px) |
| 1.05rem | 1 | 1rem (16 px) |
| 14px | 1 | 1rem (16 px) |
| 1.2rem | 1 | 1.25rem (20 px) |
| -6px | 1 | -0.5rem (-8 px) |
| 0.18rem | 1 | 0.25rem (4 px) |
| 1.875rem | 1 | 2rem (32 px) |
| 0.95rem | 1 | 1rem (16 px) |
| 1.15rem | 1 | 1.25rem (20 px) |
| 1.6rem | 1 | 1.5rem (24 px) |


### 10.6 Durées et courbes

| Valeur actuelle | Cible |
|---|---|
| `0.18s` · `0.2s` · `0.22s` (ease ou ease-out) | `0.2s ease` (`--dur-1`) |
| `0.25s var(--ease-out)` (`--transition-cta`, 74 usages) | `0.2s ease` (`--dur-1`) |
| `0.3s` · `0.35s` · `0.4s` | `0.3s var(--ease-out)` (`--dur-2`) |
| `0.5s` · `0.7s` | `0.5s var(--ease-out)` (`--dur-3`) |
| `transition: all …` | propriétés explicites |
| `border-color 0.3s` (404, sans courbe) | `border-color 0.2s ease` |


### 10.7 Survols interdits à retirer

| Sélecteur | Fichier(s) | Survol actuel | Cible |
|---|---|---|---|
| `.actualites-card` | actualites | `translateY(-4px)` | supprimer le transform ; bordure 0.32 + ombre hover |
| `.article-card` | article-… | `translateY(-4px)` + bordure rose | idem, bordure `--clr-border-hover` |
| `.cta-card` | transparence-rapports | `translateY(-5px)` | idem |
| `.partner-logo-tile` | home | `translateY(-3px)` + `--shadow-lg` | idem |
| `.erreur404-card` | 404 | `translateY(-2px)` + bordure rose + `--shadow-lg` | idem |
| `.footer__social` | 20 fichiers | `translateY(-2px)` + fond/bordure sauge | fond `rgba(255,255,255,0.12)` seul, sans déplacement |
| `.actions__filter`, `.actions-filter__btn`, `.blog__filter`, `.campagne-share__btn`, `.soutenir__amount` | action, home, campagne… | bordure **et** texte rose | fond `--clr-surface`, bordure inchangée |
| `.breadcrumb a`, `.article-nav__link`, `.actualites-link`, `.post__title a`, `.article-card__title a` | 19–20 fichiers | texte rose | souligné + `--clr-secondary-light` **(à valider)** |
| `.missions-anchors__link`, `.team-card__social-btn` | nos-missions, home | bordure / fond rose | fond `--clr-surface`, bordure inchangée |
| `.soutenir__way-btn--secondary` | home | fond plein + bordure + ombre colorée | fond léger seul (règle ghost) |
| `.btn--ghost-light` | home | couleur du texte + fond 0.05 | fond 0.12 seul |
| `.article-campaign .btn--ghost` | article | hover = `transparent` (aucun retour) | fond 0.12 sombre |
| `backdrop-filter: blur(4|6|8|12px)` | home ×3, a-propos ×1 | flou décoratif | fond opaque marine 0.92 / blanc 0.95, sans flou |


## 11. Composants — valeurs de référence (charte)

| Composant | Valeur |
|---|---|
| Header | 100 px (80 au scroll) ≥ 1024 · 76 / 64 px mobile · logo 84 / 66 px · `white-space: nowrap` sur liens, langue et CTA (présent sur `.navbar__link/__cta/__lang` ; **absent de `.btn` global**) |
| Carte | fond `--clr-white` · `1px solid var(--clr-border)` · `--shadow-card` · `--radius-md` · survol : `--clr-border-hover` + `--shadow-card-hover`, **sans transform** |
| Section derrière des cartes | `--clr-section-alt` (#EDF0F4) |
| Bouton primaire | fond `--clr-primary`, survol `--clr-primary-dark`, **sans ombre colorée**, `nowrap`, hauteur ≥ 44 px mobile |
| Bouton ghost clair | transparent · bordure `--clr-border-btn` · survol : fond `--clr-surface` uniquement |
| Bouton ghost sombre | transparent · bordure `rgba(255,255,255,0.32)` · survol : fond `rgba(255,255,255,0.12)` uniquement |
| Citation marine | aucun filet rose à gauche |
| Hero | photo + voile marine en dégradé, pas de bandeau de chiffres collé, padding aéré |
| Cible tactile mobile | ≥ 44 × 44 px |


## 12. Les 15 incohérences visuelles les plus visibles (par gravité)

1. **[Critique]** **Défilement horizontal de la page** (violation d'une règle ferme). Mesuré en Chromium : `rapport-consultations-dassa` à 360 px (`scrollWidth` 733 px, l'`aside .rapport-nav` et ses onglets débordent) ; `a-propos` à 1024 px (`scrollWidth` 1206 px, `.team-card__photo` / `__info` dépassent) ; `actualites` à 360 px (368 px, formulaire newsletter). Les 17 autres pages : aucun débordement mesuré aux 5 largeurs.
2. **[Élevée]** **Glassmorphism** : `backdrop-filter: blur()` sur 4 éléments — `.about__stat-card` (12 px), `.mission__img-kpi` (8 px), `.team-card__index` (4 px) en home ; `.mission__figure-badge` (6 px) en a-propos. Plus 2 résidus `backdrop-filter: none` (et leur préfixe `-webkit-`) dans le socle (19 fichiers).
3. **[Élevée]** **Cartes qui flottent** : 6 règles `translateY(-2…-5px)` au survol (`.actualites-card`, `.article-card`, `.cta-card`, `.partner-logo-tile`, `.erreur404-card`, et `.footer__social` dans les 20 fichiers).
4. **[Élevée]** **Aucune recette de carte unifiée** : au moins 7 combinaisons bordure/ombre pour plus de vingt cartes (0.14 / 0.18 / 0.20 / `secondary-soft` / `surface` / transparent / aucune ; ombre `--shadow-md` à peine visible (0.05) ou absente). Seules `.value-card`, `.action-card`, `.team-card`, `.temoignage-card` suivent déjà la charte au survol (0.32).
5. **[Élevée]** **Survol rose sur éléments neutres** : 17 règles (filtres, pastilles de partage, montants de don, fils d'Ariane ×18 fichiers, liens de titres) passent texte/bordure en rose ; `.article-card` et `.erreur404-card` colorent leur bordure.
6. **[Moyenne]** **Boutons ghost non conformes** : la bordure change au survol (`.soutenir__way-btn--secondary` : fond plein + bordure + ombre ; `.actions__filter`…) ; `.article-campaign .btn--ghost:hover` ne produit aucun retour visuel ; bordures sombres 0.35 / 0.4 au lieu de 0.32 ; `.btn--ghost-light` change la couleur du texte.
7. **[Moyenne]** **Filet rose à gauche de citations** : `.cta-support__quote` (2 px, sur fond marine) ; `.article-blockquote` et `.temoignage blockquote` (3 px, fond à vérifier visuellement).
8. **[Moyenne]** **Sections de cartes sans contraste** : 30 conteneurs blancs, 18 `--clr-off-white` (1,06:1 avec le blanc) et 4 `--clr-surface` ; un seul fond `#EDF0F4`, en dur (`.values`). Les cartes blanches « fondent » dans leur section.
9. **[Moyenne]** **Deux framboises** : token `--clr-primary` #C8184A mais overlays et 6 couleurs en dur en #C2185B / rgba(194,24,91) (30 déclarations), plus #96003A et rgba(170,20,75) : le même « rouge » existe en 4 teintes sur la home.
10. **[Moyenne]** **Texte sous 12 px** : 16 tailles de 0.58 à 0.72rem (92 déclarations, 9 à 11,5 px) — illisibles sur mobile.
11. **[Moyenne]** **Vert sauge en texte clair** : `--clr-accent` (#6E8B7B) fait 3,72:1 sur blanc (< 4,5:1) ; 44 règles l'emploient en couleur de texte (eyebrow, légendes, pied de page, 404) — à vérifier fond par fond (sur marine ≈ 4,2:1).
12. **[Basse]** **24 breakpoints** dont des paires à 1 px (639/640 : 143 et 125 règles, 767/768, 479/480, 1023/1024) et un 3e jeu à 860-901 px ; compaction du header sur 4 paliers.
13. **[Basse]** **Deux systèmes de gouttières** : `--container-pad` 1.5rem et `--section-pad-x` 2 / 1.25 / 1 rem ; 3 largeurs de colonne texte (45rem, 900px, 1280px) sans token.
14. **[Basse]** **Dispersion typographique et d'espacement** : 119 tailles de police, 27 interlignes, 27 interlettrages, 56 `gap`, 68 valeurs de marge/padding dont 22 % hors grille 4 px ; `.btn` global sans `nowrap` (risque de retour à la ligne des libellés).
15. **[Basse]** **Transitions et z-index** : 88 recettes de transition (0.18 → 0.7 s, 1 `transition: all`) ; z-index de badges tantôt 2 tantôt 3 ; reste cohérent au niveau global (20 / 60 / 100 / 200 / 999).

---
*Annexe — dette structurelle repérée (hors périmètre, non corrigée) : doc `CONVENTIONS.md`/`SUIVI.md` décrivant `tools/` + `partials/` + `styles/global/` absents du zip ; `404.html` en chemins absolus ; CSS global dupliqué ×20 ; 3 CSS légaux identiques ; `index.html` charge `home.css` seul (pas `hero-photo.css`).*

## 13. État d'application — tâche 2/25 (V61)

**Fait** : un bloc `:root` canonique (base + 5 `@media` : 1023 / 767 / 639 / 479 / 359) est placé en tête des 20 CSS de page, **octet pour octet identique** (`hero-photo.css` est un composant chargé après la CSS de page : il n'a pas de `:root` et consomme celui de la page). Les 3 blocs `:root` épars de chaque fichier (`--navbar-h`, `--navbar-h-compact`, `--clr-field-border*`) y ont été fusionnés ; `maintenance.css` reçoit aussi les tokens navbar/champs (inutilisés chez elle).

**Tokens ajoutés** (valeurs = référentiel, rendu inchangé car aucun ancien token n'est modifié) : `--clr-secondary-deep`, `--clr-section-alt`, `--clr-divider`, `--clr-border-card` (0.18), `--clr-border-hover`, `--clr-border-btn`, `--on-dark-*` (fill / line / border / text-muted / text-soft / text), `--fs-*`, `--lh-*`, `--ls-*`, `--sp-*`, `--radius-full`, `--radius-pill`, `--shadow-card`, `--shadow-hover`, `--shadow-popover`, `--ring-field`, `--dur-1/2/3`, `--transition-ui`, `--transition-motion`, `--z-*`, `--container-narrow`, `--container-reading`, `--gutter`.

**Noms transitoires** : `--clr-border` (0.08), `--clr-border-strong` (0.14), `--shadow-md/-lg/-sm`, `--shadow-card-hover` (0.06), `--radius-badge`, `--radius-card` gardent leur valeur actuelle. Les tâches 3+ les repointent vers `--clr-divider` / `--clr-border-card` / `--shadow-card` / `--shadow-hover` / `--radius-sm|md` puis les retirent.

**Remplacements en dur → token, valeur strictement identique** (par script ; comptes en déclarations sur les 21 fichiers) : `font-size` 855 · `transition 0.2s ease` 411 · `line-height` 313 · `z-index` 289 · `letter-spacing` 254 · `border-radius:50%` 146 · `max-width:1280px` 118 · `#FFF` 50 · `#0A172A` 38 · bordures/fonds/textes blancs semi-transparents 147 · bordures marine 47 · `box-shadow` 6 · `#EDF0F4` 1 · `max-width:45rem` 1. Preuve : en re-substituant chaque token par sa valeur, le corps des 21 CSS est identique à celui de V60.

**Quasi-identiques signalés, NON fusionnés** (tâches suivantes) : framboise `#C2185B` / `rgba(194,24,91,x)` (36) vs `--clr-primary` #C8184A · `#96003A` / `rgba(170,20,75)` vs `--clr-primary-dark` · `#587567` vs `--clr-accent-dark` · `#0E1E34`, `rgba(14,31,56|9,20,36|8,17,32|5,12,24)` vs `--clr-secondary-deep` · `#5B9EC9`, `#7FBFE0`, `#000` · bordures `0.14` (`--clr-border-strong`, 24) et `0.20` (`.value-card`) vs 0.18 · blancs hors échelle (0.03–0.09, 0.10–0.20…) · ombres `--shadow-md|lg|sm|card-hover` et deux ombres sombres vs `--shadow-popover` · `--transition-cta` 0.25s et `0.2s var(--ease-out)`, `0.3s ease`… vs `--dur-*` · tailles de police hors échelle (56 valeurs) · `line-height` 1.12/1.18/1.2/1.4/1.55/1.65/1.7/1.78/1.8 · `letter-spacing` hors échelle · z-index 3 · `900px` vs `--container-narrow` · `--container-pad` / `--section-pad-x` vs `--gutter` · espacements hors grille 4 px (≈ 330).
