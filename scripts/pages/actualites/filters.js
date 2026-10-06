/* Actualités : filtrage par catégorie + recherche (amélioration progressive).
   Sans JS : la barre d'outils reste masquée (attribut hidden) et tous les articles sont visibles.
   Balisage attendu (pages/actualites.html) :
     [data-news-toolbar]  > boutons [data-filter="<slug>"] (aria-pressed), [data-news-search],
                            [data-news-count] (aria-live), [data-news-reset]
     [data-news-grid]     > .actualites-card[data-categorie="<slug>"]
     [data-news-empty], [data-news-pagination]
   Slug de catégorie = valeur de data-categorie des cartes ; « tous » = aucun filtre.
   Les compteurs « (n) » des boutons sont recalculés d'après les articles présents dans la page. */
(function () {
  'use strict';

  var toolbar = document.querySelector('[data-news-toolbar]');
  var grid = document.querySelector('[data-news-grid]');
  if (!toolbar || !grid) return;

  var buttons = Array.prototype.slice.call(toolbar.querySelectorAll('[data-filter]'));
  var search = toolbar.querySelector('[data-news-search]');
  var counter = toolbar.querySelector('[data-news-count]');
  var reset = toolbar.querySelector('[data-news-reset]');
  var empty = document.querySelector('[data-news-empty]');
  var pagination = document.querySelector('[data-news-pagination]');

  function norm(s) {
    return String(s || '')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase().replace(/\s+/g, ' ').trim();
  }

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.actualites-card')).map(function (el) {
    return { el: el, cat: el.getAttribute('data-categorie') || '', text: norm(el.textContent) };
  });

  var state = { cat: 'tous', q: '' };

  /* Compteurs par catégorie (indépendants de la recherche) */
  buttons.forEach(function (b) {
    var slug = b.getAttribute('data-filter');
    var n = slug === 'tous' ? cards.length : cards.filter(function (c) { return c.cat === slug; }).length;
    var span = b.querySelector('[data-filter-count]');
    if (span) span.textContent = '(' + n + ')';
  });

  function label(n) {
    return n === 0 ? 'Aucun article' : n + ' article' + (n > 1 ? 's' : '');
  }

  function apply() {
    var words = norm(state.q).split(' ').filter(Boolean);
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (state.cat === 'tous' || c.cat === state.cat) &&
        words.every(function (w) { return c.text.indexOf(w) !== -1; });
      c.el.hidden = !ok;
      if (ok) shown += 1;
    });
    buttons.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-filter') === state.cat ? 'true' : 'false');
    });
    var active = state.cat !== 'tous' || words.length > 0;
    if (counter) counter.textContent = label(shown);
    if (empty) empty.hidden = shown !== 0;
    if (reset) reset.hidden = !active;
    /* La pagination décrit la liste complète : masquée tant qu'un filtre est actif */
    if (pagination) pagination.hidden = active;
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      state.cat = b.getAttribute('data-filter');
      apply();
    });
  });

  if (search) {
    var timer;
    search.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { state.q = search.value; apply(); }, 200);
    });
    search.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && search.value) {
        search.value = '';
        state.q = '';
        apply();
      }
    });
  }

  if (reset) {
    reset.addEventListener('click', function () {
      state.cat = 'tous';
      state.q = '';
      if (search) search.value = '';
      apply();
      var first = buttons[0];
      if (first) first.focus();
    });
  }

  toolbar.hidden = false;
  apply();
})();
