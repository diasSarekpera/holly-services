/* Devenir bénévole : filtre des missions ouvertes (amélioration progressive).
   Sans JS : la barre de filtres reste masquée (attribut hidden) et toutes les missions sont visibles.
   Balisage attendu (pages/devenir-benevole.html, section #missions) :
     [data-mission-filters] > boutons [data-filter-group="domaine|format"][data-filter="<slug>|all"] (aria-pressed),
                              [data-mission-count] (role=status, aria-live), [data-mission-reset]
     [data-mission-grid]    > .benevolat-mission-card[data-domaine="<slug>"][data-format="<slug>"]
     [data-mission-empty]
   Deux groupes combinés en ET ; « all » = aucun filtre sur le groupe. Un seul bouton pressé par groupe. */
(function () {
  'use strict';

  var bar = document.querySelector('[data-mission-filters]');
  var grid = document.querySelector('[data-mission-grid]');
  if (!bar || !grid) return;

  var buttons = Array.prototype.slice.call(bar.querySelectorAll('[data-filter-group]'));
  var counter = bar.querySelector('[data-mission-count]');
  var reset = bar.querySelector('[data-mission-reset]');
  var empty = document.querySelector('[data-mission-empty]');

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.benevolat-mission-card')).map(function (el) {
    return { el: el, domaine: el.getAttribute('data-domaine') || '', format: el.getAttribute('data-format') || '' };
  });

  var state = { domaine: 'all', format: 'all' };

  function label(n) {
    return n === 0 ? 'Aucune mission' : n + ' mission' + (n > 1 ? 's' : '') + ' ouverte' + (n > 1 ? 's' : '');
  }

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (state.domaine === 'all' || c.domaine === state.domaine) &&
        (state.format === 'all' || c.format === state.format);
      c.el.hidden = !ok;
      if (ok) shown += 1;
    });
    buttons.forEach(function (b) {
      var on = b.getAttribute('data-filter') === state[b.getAttribute('data-filter-group')];
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    var active = state.domaine !== 'all' || state.format !== 'all';
    if (counter) counter.textContent = label(shown);
    if (empty) empty.hidden = shown !== 0;
    if (reset) reset.hidden = !active;
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      state[b.getAttribute('data-filter-group')] = b.getAttribute('data-filter');
      apply();
    });
  });

  if (reset) {
    reset.addEventListener('click', function () {
      state.domaine = 'all';
      state.format = 'all';
      apply();
      if (buttons[0]) buttons[0].focus();
    });
  }

  bar.hidden = false;
  apply();
})();
