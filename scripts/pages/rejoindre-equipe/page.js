/* Rejoindre l'équipe : offres ouvertes (amélioration progressive).
   Sans JS : la barre de filtres et les boutons « Voir le détail » restent masqués (attribut hidden)
   et toutes les offres sont visibles (les fiches détaillées s'ouvrent après activation du JS).
   Balisage attendu (pages/rejoindre-equipe.html, section #offres) :
     [data-offers-toolbar] > boutons [data-filter="<slug>|tous"] (aria-pressed), [data-offers-search],
                             [data-offers-count] (role=status, aria-live), [data-offers-reset]
     [data-offers-list]    > .job-row[data-categorie="<slug>"] > button[data-job-toggle][aria-controls]
                             + [data-job-details] (id = aria-controls)
     [data-offers-empty], [data-offers-total] (hero : nombre d'offres ouvertes, toutes catégories) */
(function () {
  'use strict';

  var list = document.querySelector('[data-offers-list]');
  if (!list) return;

  var toolbar = document.querySelector('[data-offers-toolbar]');
  var empty = document.querySelector('[data-offers-empty]');
  var total = document.querySelector('[data-offers-total]');

  function norm(s) {
    return String(s || '')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase().replace(/\s+/g, ' ').trim();
  }

  function plural(n, one, none) {
    return n === 0 ? none : n + ' ' + one + (n > 1 ? 's' : '');
  }

  var rows = Array.prototype.slice.call(list.querySelectorAll('.job-row')).map(function (el) {
    var head = el.querySelector('.job-header');
    return { el: el, cat: el.getAttribute('data-categorie') || '', text: norm(head ? head.textContent : el.textContent) };
  });

  if (total) total.textContent = plural(rows.length, 'offre', 'Aucune offre') + (rows.length ? ' ouverte' + (rows.length > 1 ? 's' : '') : '');

  /* Détails : bouton aria-expanded / aria-controls, panneau masqué par défaut */
  rows.forEach(function (r) {
    var btn = r.el.querySelector('[data-job-toggle]');
    if (!btn) return;
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;
    panel.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    btn.hidden = false;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      panel.hidden = open;
    });
  });

  if (!toolbar) return;

  var buttons = Array.prototype.slice.call(toolbar.querySelectorAll('[data-filter]'));
  var search = toolbar.querySelector('[data-offers-search]');
  var counter = toolbar.querySelector('[data-offers-count]');
  var reset = toolbar.querySelector('[data-offers-reset]');
  var state = { cat: 'tous', q: '' };

  function apply() {
    var words = norm(state.q).split(' ').filter(Boolean);
    var shown = 0;
    rows.forEach(function (r) {
      var ok = (state.cat === 'tous' || r.cat === state.cat) &&
        words.every(function (w) { return r.text.indexOf(w) !== -1; });
      r.el.hidden = !ok;
      if (ok) shown += 1;
    });
    buttons.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-filter') === state.cat ? 'true' : 'false');
    });
    var active = state.cat !== 'tous' || words.length > 0;
    if (counter) counter.textContent = plural(shown, 'offre', 'Aucune offre');
    if (empty) empty.hidden = shown !== 0;
    if (reset) reset.hidden = !active;
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
      if (buttons[0]) buttons[0].focus();
    });
  }

  toolbar.hidden = false;
  apply();
})();
