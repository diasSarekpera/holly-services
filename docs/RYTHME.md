# Rythme vertical (T8)

Tokens (`:root`, identiques dans les 20 feuilles) :
- `--section-pad-y` = `clamp(3.5rem, 1.9rem + 5.2vw, 6rem)` : section standard (56 px → 96 px). Variantes : `--section-pad-y-compact` (`clamp(2.5rem,…,4rem)`, 40 → 64 px : grille d'actualités, bloc CTA, pages légales) et `--section-pad-y-band` (`clamp(2rem,…,3rem)`, 32 → 48 px : bandeaux fins : intro d'actions, partage, signalement 404, signalement témoignage).
- Rythme d'en-tête : `--rhythm-eyebrow` 1.25rem · `--rhythm-title` 1.75rem · `--rhythm-p` 1rem · `--rhythm-block` 2rem · `--rhythm-media` 3rem ; sous 768 px : 1 / 1.25 / 0.875 / 1.5 / 2 rem. `--section-header-gap` = `--rhythm-block`.
- Le bloc « Rythme vertical (T8) » (fin de chaque feuille) applique ces valeurs par combinateurs de frères (`.eyebrow + h2`, `h2 + p`, `p + p`, `p + bloc`, `h2 + bloc`) ; les conteneurs à `gap` (`.soutenir__left`, `.contact__info`, `.cta-support__main`, `.cta-contact__cta`, `.section-header__left/right/--center`, `.partners-strip__inner`, `.actualites-featured__content`) passent à `row-gap: 0` pour ne pas cumuler gap et marge.
- Un nouvel en-tête de section n'a besoin d'aucun espacement propre : eyebrow, h2, paragraphes, bloc suivant en frères directs.

Espacements mesurés (Chromium, 20 pages, 2 à 37 en-têtes par largeur ; une seule valeur par colonne = rythme identique partout) :

| Largeur | eyebrow→titre | titre→1er § | §→§ | dernier § →bloc | titre→bloc | padding de section standard |
|---|---|---|---|---|---|---|
| 320 px | 16 | 20 | 14 | 24/32 (3rem=48 si média) | 24 | 56 px (57 sections) |
| 360 px | 16 | 20 | 14 | 24/32 (3rem=48 si média) | 24 | 56 px (57 sections) |
| 390 px | 16 | 20 | 14 | 24/32 (3rem=48 si média) | 24 | 56 px (57 sections) |
| 768 px | 20 | 28 | 16 | 32/48 (3rem=48 si média) | 32 | 70 px (57 sections) |
| 1024 px | 20 | 28 | 16 | 32/48 (3rem=48 si média) | 32 | 84 px (57 sections) |
| 1366 px | 20 | 28 | 16 | 32/48 (3rem=48 si média) | 32 | 96 px (57 sections) |
| 1920 px | 20 | 28 | 16 | 32/48 (3rem=48 si média) | 32 | 96 px (57 sections) |
