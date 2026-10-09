# À fournir par l'ONG — liste priorisée (finalisée V42)

Cette liste remplace le journal détaillé écrit page par page, conservé tel quel dans `_archive/A-FOURNIR-detail.md` (chiffres exacts, ancres, noms de champs). Rien n'a été inventé dans le site : tout ce qui manque est marqué `[À COMPLÉTER]` (ou `[À COMPLÉTER PAR L'ONG]`, `[fictif]`, `[à valider]`).
Suivi : `grep -rn "À COMPLÉTER" pages index.html 404.html` · `grep -rn "PAR L'ONG" pages` · `grep -rn EXEMPLE.org . --include=*.html --include=*.js --include=*.py` · `python3 tools/check.py -v`.

## P0 — Bloquant avant la mise en ligne
- [ ] **Nom de domaine définitif** : constante `SITE_URL` de `tools/build.py` (placeholder `https://www.EXEMPLE.org`) → canonical, `og:url`, `og:image`, JSON-LD, `sitemap.xml`, `robots.txt` ; remplacer aussi les `EXEMPLE.org` copiés dans la zone de partage de `pages/article-prevention-cancer-peau.html`. Ensuite : `python3 tools/build.py` puis `--sitemap`.
- [ ] **Hébergeur** (statique, avec `404.html` à la racine du domaine ; voir README). Son identité alimente les mentions légales.
- [ ] **Mentions légales** (`pages/mentions-legales.html`, provisoire) : dénomination officielle, forme juridique, n° d'enregistrement et autorité, adresse du siège, téléphone, e-mail, identifiant fiscal si applicable, directeur·rice de la publication ; hébergeur ; propriété intellectuelle (titulaire, crédits photo, licences polices/icônes) ; responsabilité ; données personnelles. Texte à faire valider par un juriste.
- [ ] **Conditions d'utilisation** (`pages/conditions-utilisation.html`, provisoire) : objet, acceptation et modification, règles d'usage (dont contenus envoyés par formulaires, condition d'âge éventuelle), responsabilité, droit applicable et juridiction.
- [ ] **Politique de confidentialité** (`pages/politique-confidentialite.html`, incomplète) : responsable du traitement et contact, données collectées, finalités, bases légales, durées (dont CV), destinataires, droits, cookies ; version et date de mise à jour (« 1 Octobre 2026 · Version 1.0 » à valider) ; 2 puces de l'encadré « En bref ». Version et date des deux pages légales à renseigner, puis retrait du bandeau « Contenu provisoire ».
- [ ] **Endpoints des formulaires** (`data-endpoint`, absent = mode démo : rien n'est envoyé) pour les 6 formulaires : newsletter (actualités, article), bénévole, candidature (CV : prestataire acceptant les fichiers), témoignage (données sensibles : prestataire à valider), demande de documents (transparence). Voir `docs/FORMULAIRES.md`. Pour chacun : texte de consentement, message de confirmation `[data-form-success]`.
- [ ] **Coordonnées à valider** : téléphone « +229 97 00 00 00 » (footer, JSON-LD, page maintenance ; ressemble à un placeholder), horaires « du lundi au vendredi, de 8h00 à 17h00 », e-mails `contact@`, `presse@`, `recrutement@hollyservices.org` (décodés du prototype), indicatif du placeholder téléphone « +33 6 … » à adapter.
- [ ] **Réseaux sociaux** : URLs Facebook, Instagram, LinkedIn, YouTube (partial footer) et 4 profils LinkedIn de l'équipe (`index.html`) ; en attendant → `maintenance.html`.
- [ ] **Passerelle de don** : « Faire un don » renvoie vers `index.html#dons` (aucune page de paiement ; montant et fréquence choisis non transmis) → choisir le prestataire et fournir la page cible.

## P1 — Contenu manquant (pages visiblement incomplètes)
- [ ] **Pages sans article suffisant** : actualités (3 articles affichés sur 11 annoncés ; fournir les 8 autres avec `data-categorie` ; catégories Action terrain, Santé, Insertion sociale vides ; pagination inactive).
- [ ] **Documents PDF** à déposer dans `assets/documents/`, puis repointer les boutons (aujourd'hui → `maintenance.html`) et remettre `download` : `dossier-partenariat.pdf`, `rapport-consultations-dassa-2026.pdf`, `rapport-annuel-2025.pdf`, `etats-financiers-audites-2024.pdf`, kit média, chartes (notre-approche). Poids affichés (« 2 Mo », « 2.4 Mo », « 1.1 Mo ») à aligner sur les vrais fichiers ; liste réelle des documents de la page transparence (« 12 documents trouvés » annoncés pour 2 affichés).
- [ ] **Nos missions** : textes des blocs Santé (suite coupée), Droits humains, Éducation (description + puces).
- [ ] **Mission Santé** : résultats chiffrés de « Ce que nos actions ont permis » (chiffres retirés tant que non validés), sources des 3 points de « Ce qui est en jeu », autres cartes de programmes.
- [ ] **Rapport Dassa** : « Résultats détaillés », « Méthodologie », « Enseignements », étape « Trois jours de consultations » ; données `[fictif]` / `[à confirmer]` (3 jours, 310 bénéficiaires, 280 protections solaires, 24 cas, validation par le coordinateur des programmes).
- [ ] **Notre approche** : sections « Nos principes d'action » (`#principes`) et « Nos chartes et engagements » (`#engagements`), autres valeurs que « Humanité ».
- [ ] **Offres d'emploi** (rejoindre-equipe) : liste réelle, fiches détaillées (missions, profil, conditions), étapes 2 et 3 du formulaire, processus de recrutement, engagements, FAQ.
- [ ] **Missions bénévoles** : liste réelle et statuts, étapes 2 « Engagement » et 3 « Motivation », domaines et formats du filtre (option « Traduction » ajoutée).
- [ ] **Témoignage** : champs des étapes 1 à 4, médias acceptés, protections (anonymat, validation, retrait), sections « Trois façons de témoigner », « Et ensuite ? », FAQ ; page « Témoignages » dédiée ; canal confidentiel de signalement (« Signaler une préoccupation » → maintenance).
- [ ] **Devenir partenaire** : section/formulaire « Proposer un partenariat » (`#contact-partenariat` ; le CTA renvoie vers `index.html#contact`).
- [ ] **Transparence** : graphique « Origine des fonds », définitions annoncées dans le sous-titre, champ « document demandé » du formulaire, sections numérotées absentes (5, 7), recherche de documents non branchée.
- [ ] **Pages liées encore sur `maintenance.html`** : missions Droits humains et Éducation (index ×2, nos-missions ×2), rapports d'action de la home (conférence février 2026, distribution janvier 2026), page Galerie (à réajouter au plan de `404.html`).

## P2 — Faits, chiffres et attributions à valider (repris tels quels des prototypes)
- [ ] Home / missions / transparence / bénévole / partenaire : 1 024 enfants, 94 % des fonds au terrain (6 % de frais, exercice 2024), 312 kits, 48 campagnes, 350+ consultations, 80 bénévoles, 12+ partenaires, 1 200+ donateurs, « depuis 2018 », Bénin · Togo · Tanzanie, réponse sous 10 jours ouvrés, ISO 9001 (en cours), agrément de l'État, Coordination Sud, conformité RGPD, audit annuel indépendant.
- [ ] Campagne « Protéger 500 enfants » : 7 800 € / 10 000 € (78 %), 214 donateurs, 342 enfants, reste 2 200 €, « 10 € = 1 kit » ; date de clôture (voir P3).
- [ ] Article « cancer de la peau » : 340 enfants / 340 kits, 20 relais, 5 espaces d'ombre, citation du « Dr. Amina D., Coordinatrice médicale », date du 18 avril 2025, auteur, 5 min de lecture, légende photo (auteur, lieu, année, consentement des familles).
- [ ] Actualités : « plus de 250 enfants », dates des articles, titres `[fictif]` (3 articles).
- [ ] Témoignage de nos-missions (« Parent d'un enfant accompagné ») ; phrase de conviction de notre-approche (« [formulation à valider] »).
- [ ] Meta descriptions rédigées d'après le chapô (campagne, bénévole, 404) : relecture.

## P3 — Décisions à trancher (incohérences relevées)
- [ ] Date de clôture de la campagne : « 31 déc. 2026 » (page) ou « 30 juin 2026 » (carte de la home).
- [ ] Offres : 6 annoncées, 3 affichées. Articles : 11 annoncés, 3 affichés. Documents : 12 annoncés, 2 affichés.
- [ ] Lien « Voir les détails » de la galerie de la home (Cotonou, 2025) : cible Dassa notée dans le prototype, mais lieu et année différents.
- [ ] Hero de la page Dassa : aplat navy ou photo.

## P4 — Images (placeholders CSS ou `placeholder.svg` partout)
- [ ] `assets/images/og-default.png` (1200 × 630, PNG, logo + baseline) ; images Open Graph par page possibles (`og_image` de `META`).
- [ ] Photo de fond du hero de la home (≈ 1600 px), photos et avatars de la home / à propos / actions, logos de partenaires (260 × 60 ou 280 × 60), photos de l'équipe.
- [ ] Nos missions : 3 photos (3:2). Campagne : portrait d'enfant 16:9 (consentement et protection de l'image). Actualités : « À la une » 16:9 + 3 vignettes 3:2. Article : image principale 16:9 + 3 cartes « À lire également » 3:2.
- [ ] À chaque photo livrée : `alt`, aligner `width`/`height` sur le ratio réel, retirer `loading="lazy"` seulement si l'image est visible dès le haut de page.
- [x] Logo : intégré (V123, voir docs/LOGOS.md), JSON-LD sur `logo-512.png`. À refaire quand l'ONG changera de logo.
- [ ] Partenaires : nom exact, rôle, ancienneté, site web de chacun des 6 ; logo original de SANAA (affiché en texte pour l'instant) ; confirmer le compteur « 6 partenaires actifs » et les 2 autres chiffres de la section (3 secteurs, 6 pays), toujours fictifs.

## P5 — Facultatif / plus tard
- [ ] JSON-LD : `image` et `publisher` de l'article, `JobPosting` pour les vraies offres, `sameAs`, adresse et n° d'enregistrement de l'`NGO`.
- [ ] Sections du prototype dont seul le CSS existait (supprimé) : « Rapports » et bandeau final des actualités ; Parcours et FAQ de Mission Santé.
- [ ] Pages Droits humains et Éducation (modèle : `pages/mission-sante.html`, CSS `.mission-detail__…`).
- [ ] Contrastes ouverts : `docs/AUDIT.md` (9 couples sous le seuil, arbitrage de couleur).
- [ ] Hero : photos Unsplash provisoires, à remplacer par de vraies photos de l'ONG.
