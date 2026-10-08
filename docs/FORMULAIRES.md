# Formulaires — `form.js` + `form-states.css`

Script : `scripts/components/form.js` (activé sur tout `<form data-form>`). Styles : `styles/global/components/form-states.css` (import ajouté par `tools/convert_proto.py` dans les `main.css` générés ; à ajouter à la main aux `main.css` existants des pages qui ont un formulaire). Charger le script en fin de page : `<script src="../scripts/components/form.js" defer></script>`.

## Balisage attendu
```html
<form data-form data-endpoint="https://formspree.io/f/XXXX" method="post">
  <div class="form__field">
    <label for="email">E-mail</label>
    <input type="email" id="email" name="email" required autocomplete="email">
    <p class="form__error" id="email-err" hidden></p>   <!-- facultatif : créé par le JS si absent -->
  </div>
  <div class="form__hp"><label>Ne pas remplir <input type="text" name="_gotcha"></label></div>
  <label><input type="checkbox" name="consent" required> J’accepte … </label>
  <button type="submit" class="btn btn-primary">Envoyer</button>
  <div data-form-status></div>                           <!-- facultatif : région aria-live, créée si absente -->
  <div data-form-success hidden>Merci, votre message a bien été envoyé.</div>
</form>
```
Un champ par `.form__field` (ou `.form__group`) ; groupe de radios dans un `<fieldset>`. Pas de CSS/JS inline (CONVENTIONS).

## Attributs
| Attribut | Où | Effet |
|---|---|---|
| `data-form` | `<form>` | Active le script (`novalidate` posé par le JS). |
| `data-endpoint` | `<form>` | URL du POST (`FormData`). **Absent = mode démo** : succès affiché, rien n’est envoyé, `console.warn` « mode démo ». |
| `data-form-success` | élément dans le form | Affiché au succès (`hidden` retiré, `.is-visible`, focus). Masqué par défaut en CSS. |
| `data-form-status` | élément dans le form | Région `aria-live="polite"` (résultat global : erreurs, envoi, échec). |
| `accept` / `data-max-size` | `input[type=file]` | Formats acceptés (`.pdf`, `image/*`…) / taille max en Mo (ex. `5` ou `2,5`). |
| `data-error-msg` | champ | Remplace le message « champ obligatoire ». |
| `data-pattern-msg` | champ avec `pattern` | Message si le format est invalide (sinon `title`). |
| `.form__hp` | conteneur | Honeypot masqué ; rempli → faux succès, aucun envoi. |

États pour le CSS : `form[data-state="loading\|success\|error"]`, `form[aria-busy="true"]`, `[aria-invalid="true"]`.

## Brancher un vrai endpoint
Ajouter `data-endpoint`, c’est tout : le script fait un `fetch` POST avec `Accept: application/json`, succès si réponse 2xx, sinon message d’erreur réseau/serveur.
- **Formspree** : `data-endpoint="https://formspree.io/f/<id>"` ; nommer le honeypot `_gotcha`. Vérifier selon l’offre la prise en charge des fichiers joints.
- **Netlify Forms** : ajouter `name="<nom>"` + `data-netlify="true"` (détection au déploiement), un `<input type="hidden" name="form-name" value="<nom>">` et `data-endpoint="/"` ; honeypot : `netlify-honeypot="<name du champ .form__hp>"`.
- **API maison** : accepter un POST `multipart/form-data`, répondre 2xx, autoriser le CORS si domaine différent ; ne jamais faire confiance au client (revalider côté serveur, filtrer le honeypot, limiter le débit).
Dans tous les cas : renseigner l’endpoint dans `docs/A-FOURNIR.md` (Techniques) et mentionner l’usage des données dans la politique de confidentialité.

## Les 6 formulaires du projet
Champs relevés dans les prototypes (`grep` des balises) ; les `name` sont **suggérés**. Rien n’est inventé : ce qui manque est marqué `[À COMPLÉTER]`.

| Formulaire | Prototype → page cible | Champs (type, obligatoire) | Remarques |
|---|---|---|---|
| Newsletter Actualités | `actualites` | `email` (email, requis) ; `interests` (3 cases : Santé, Éducation, Événements) ; `consent` (case, requise : « J’accepte de recevoir des communications de Holly Services ONG. ») | Bouton « S’abonner ». |
| Newsletter Article | `article-prevention-cancer-peau` | `email` (email, requis) ; `interests` (cases : Santé, Éducation, Urgences) ; `consent` (case, requise : mention de confidentialité des données) | Même bloc que ci-dessus, centres d’intérêt différents ; seul formulaire déjà doté de `name`/`value` sur les cases. |
| Bénévole | `devenir-benevole` | `prenom` (text) ; `nom` (text) ; `email` (email) ; `telephone` (tel) ; `message` (textarea, « 800 caractères max » → `maxlength="800"`) | Aucun `required` dans le prototype : à décider. Bouton « Passer à l’étape suivante » = première étape d’un parcours ; étapes suivantes `[À COMPLÉTER]`. |
| Témoignage | `partager-temoignage` | `[À COMPLÉTER]` — prototype = squelette (« Formulaire complet ici (Étapes 1 à 4) ») | Champs, consentement (+ éventuelle photo : `accept`, `data-max-size`) à fournir par l’ONG. |
| Candidature | `rejoindre-equipe` | `prenom` (text, requis) ; `nom` (text, requis) ; `email` (email, requis) ; CV/lettre `[À COMPLÉTER]` | Prototype limité à l’étape 1. Intégré (V28) : `data-form`, `cv` (`accept=".pdf"`, `data-max-size="5"`, facultatif), `consent` requis, honeypot `_gotcha`, `[data-form-success]` `[À COMPLÉTER]` ; « Suivant » = `submit` (mode démo). |
| Demande de rapport / contact (Transparence) | `transparence-rapports` | `nom` (text, requis) ; `email` (email, requis) ; rapport demandé / message `[À COMPLÉTER]` | Intégré (V30) : `data-form`, `nom` et `email` requis, `consent` requis, honeypot `_gotcha`, `[data-form-success]` `[À COMPLÉTER]`, mode démo ; champ « document demandé / message » toujours à fournir. Bouton « Envoyer la demande ». Les champs de recherche de documents/postes/actualités ne sont pas des formulaires `data-form`. |

À l’intégration : retirer les `style=""` des prototypes, ajouter `for`/`id` sur chaque label, remplacer `placeholder` seul par un vrai `<label>`, et le consentement RGPD sur tout formulaire collectant des données personnelles (texte juridique : `[À COMPLÉTER]` si non fourni).

## Audit CSS (T11A)

Script : `tools/forms_audit.py` (règles hors @media, hors bloc T11) ; bloc posé par `tools/forms_t11.py apply|hash|measure` (hash `d69005df80b5`, 21 feuilles).

| Champ | Feuille(s) | Haut. | Police | Padding | Bordure | Rayon | Fond |
|---|---|---|---|---|---|---|---|
| `form-input` | home | - | var(--fs-body-sm) | 0.75rem 1rem | 1.5px solid var(--clr-border-stron | var(--radius-sm) | var(--clr-off-white) |
| `form-select` | home | - | - | - | - | - | - |
| `form-textarea` | home | 120px | - | - | - | - | - |
| `form-control` | transparence | 48px | - | 0.75rem | 1px solid var(--clr-border-strong) | var(--radius-badge) | - |
| `benevolat-input` | devenir-bene | - | var(--fs-body-sm) | 12px 16px | 1px solid var(--clr-secondary-soft | var(--radius-badge) | - |
| `contact-form__input` | a-propos | - | var(--fs-body-sm) | 0.875rem 1rem | 1.5px solid var(--clr-border-stron | var(--radius-sm) | var(--clr-off-white) |
| `contact-form__textarea` | a-propos | - | var(--fs-body-sm) | 0.875rem 1rem | 1.5px solid var(--clr-border-stron | var(--radius-sm) | var(--clr-off-white) |
| `actualites-nl__input` | actualites | 48px | - | 0 16px | 1px solid var(--clr-border-strong) | var(--radius-badge) | var(--clr-white) |
| `article-nl__input` | article-prev | 48px | var(--fs-body) | 0 1rem | 1px solid var(--clr-border-strong) | var(--radius-badge) | - |
| `search-input` | rejoindre-eq | 44px | var(--fs-base-sm) | 0.5rem 1rem | 1px solid var(--clr-border-strong) | var(--radius-badge) | var(--clr-white) |
| `footer__nl-input` | 404,a-propos+ | - | var(--fs-sm) | 0.65rem 0.875rem | none | - | transparent |
| `footer__nl-input` | 404,a-propos+ | - | var(--fs-body) | - | - | - | - |
| `footer__nl-input` | 404,a-propos+ | 44px | - | - | - | - | - |
| `erreur404-search input` | 404 | 56px | var(--fs-body) | 0 3rem | 1px solid var(--clr-border-strong) | var(--radius-badge) | - |
| `actualites-toolbar__search input` | actualites | - | - | 0 12px | 0 | - | transparent |

Constats : 14 familles de champs, 5 hauteurs (40/44/48/56 px ou auto), polices 13,3 / 14 / 15 / 16 px, bordures `--clr-border-strong` / `--clr-field-border` / `--clr-secondary-soft`, rayons `--radius-badge` ou `--radius-sm`, placeholders 0,5 d’opacité (a-propos, home) ; champs de `.candidature-layout` et `.erreur404-search` stylés par descendance.
Une règle partagée existante force `border-color:var(--clr-field-border) !important` sur tous les champs (3,65:1, WCAG 1.4.11, DESIGN-TOKENS l.41/132) : le bloc T11 l’adopte au lieu de `rgba(16,35,63,0.25)` (≈1,6:1).
Hors socle : cases, radios, fichier, pot de miel `_gotcha`, `footer__nl-input` (fond marine), `actualites-toolbar__search` (conteneur bordé).

## États et annexes (T11B)
Bloc « Formulaires (T11) » étendu (`tools/forms_t11.py`, mesure `tools/forms_11b_measure.py`) : labels `block` 14 px / 500 ; astérisque `*` en `--clr-urgent` ajouté en CSS (`::after`, muet pour les lecteurs d'écran) aux labels des champs `required` (le `*` explicite de l'accueil est recoloré) ; anneau commun `--ring-field` au `:focus-visible` (champs, cases, radios, upload) ; erreur = bordure `--clr-urgent` (maintenue au focus) + anneau urgent + icône `::before` sur `.form__error` / `.form__status--error` ; succès = icône sur `.form__status--success` ; désactivé = fond `--clr-surface` + `not-allowed` ; cases et radios : label cliquable min 44 px ; upload : champ 44 px et bouton « Parcourir » stylé.
Non fait (texte requis) : mention « * = champ obligatoire » ; la plupart des champs n'ont pas de marque visible dans le HTML.
