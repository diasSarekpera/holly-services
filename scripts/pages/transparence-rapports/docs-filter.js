/* Transparence et rapports : recherche dans le centre de téléchargement (amélioration progressive).
   Sans JS : le champ de recherche est masqué (attribut hidden) et tous les documents restent visibles.
   Balisage attendu (pages/transparence-rapports.html, section #documents) :
     [data-docs-search]  champ de recherche (input), dans [data-docs-bar] (hidden par défaut)
     [data-docs-count]   compteur (role=status, aria-live)
     [data-docs-list] > li.doc-item   (texte du li = texte recherché)
     [data-docs-empty]   message « aucun résultat » (hidden par défaut) */
(function () {
  'use strict';

  var bar = document.querySelector('[data-docs-bar]');
  var list = document.querySelector('[data-docs-list]');
  if (!bar || !list) return;

  var input = bar.querySelector('[data-docs-search]');
  var counter = document.querySelector('[data-docs-count]');
  var empty = document.querySelector('[data-docs-empty]');
  var items = Array.prototype.slice.call(list.querySelectorAll('.doc-item'));

  function norm(s) {
    return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  var index = items.map(function (el) { return norm(el.textContent || ''); });

  function label(n) {
    return n === 0 ? 'Aucun document' : n + ' document' + (n > 1 ? 's' : '');
  }

  function apply() {
    var q = norm(input.value.trim());
    var shown = 0;
    items.forEach(function (el, i) {
      var ok = q === '' || index[i].indexOf(q) !== -1;
      el.hidden = !ok;
      if (ok) shown += 1;
    });
    if (counter) counter.textContent = label(shown);
    if (empty) empty.hidden = shown !== 0;
  }

  bar.hidden = false;
  input.addEventListener('input', apply);
  apply();
})();
