/* 404 — amélioration progressive : adresse demandée, recherche de pages,
   plan du site en accordéon sur mobile, lien « Signaler ce lien » prérempli.
   Sans JS : tout reste visible et les liens fonctionnent. */
(function () {
  'use strict';
  var d = document;

  /* 1. Adresse demandée */
  var pathBox = d.getElementById('js-path-display');
  var pathVal = d.getElementById('js-path-value');
  var path = location.pathname + location.search;
  if (pathBox && pathVal && !/\/404\.html$/.test(location.pathname)) {
    pathVal.textContent = path;
    pathBox.classList.add('erreur404-hero__path--visible');
  }

  /* 2. Recherche parmi les pages suggérées */
  var input = d.getElementById('search-page');
  var clear = d.getElementById('js-clear-search');
  var count = d.getElementById('js-search-count');
  var empty = d.getElementById('js-search-empty');
  var cards = d.querySelectorAll('#js-useful-links .js-searchable');

  function normalize(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function filter() {
    var q = normalize(input.value).trim();
    var n = 0;
    Array.prototype.forEach.call(cards, function (card) {
      var hay = normalize(card.textContent + ' ' + card.getAttribute('data-mots'));
      var match = !q || hay.indexOf(q) !== -1;
      card.hidden = !match;
      if (match) n++;
    });
    clear.classList.toggle('erreur404-search__clear--visible', q !== '');
    empty.classList.toggle('erreur404-empty--visible', n === 0);
    if (n === 0) {
      count.textContent = 'Aucune page trouvée';
    } else if (q) {
      count.textContent = n + (n > 1 ? ' pages trouvées' : ' page trouvée');
    } else {
      count.textContent = n + ' pages suggérées';
    }
  }

  if (input && clear && count && empty) {
    input.addEventListener('input', filter);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && input.value) { input.value = ''; filter(); }
    });
    clear.addEventListener('click', function () {
      input.value = '';
      filter();
      input.focus();
    });
  }

  /* 3. Plan du site : accordéon sous 768 px */
  var cols = d.querySelectorAll('.erreur404-sitemap__col');
  var mq = window.matchMedia('(max-width: 767px)');

  function setupAccordion(mobile) {
    Array.prototype.forEach.call(cols, function (col) {
      var h3 = col.querySelector('h3');
      var list = col.querySelector('.erreur404-sitemap__list');
      if (!h3 || !list) return;
      var btn = h3.querySelector('button');
      if (mobile && !btn) {
        var label = h3.textContent.trim();
        h3.setAttribute('data-label', label);
        btn = d.createElement('button');
        btn.type = 'button';
        btn.className = 'erreur404-sitemap__toggle';
        btn.setAttribute('aria-expanded', 'false');
        btn.setAttribute('aria-controls', list.id);
        btn.appendChild(d.createTextNode(label));
        var icon = d.createElement('i');
        icon.className = 'ri-arrow-down-s-line';
        icon.setAttribute('aria-hidden', 'true');
        btn.appendChild(icon);
        btn.addEventListener('click', function () {
          var open = btn.getAttribute('aria-expanded') === 'true';
          btn.setAttribute('aria-expanded', open ? 'false' : 'true');
          list.hidden = open;
        });
        h3.textContent = '';
        h3.appendChild(btn);
        list.hidden = true;
      } else if (!mobile && btn) {
        h3.textContent = h3.getAttribute('data-label') || '';
        list.hidden = false;
      }
    });
  }

  setupAccordion(mq.matches);
  if (mq.addEventListener) {
    mq.addEventListener('change', function (e) { setupAccordion(e.matches); });
  } else if (mq.addListener) {
    mq.addListener(function (e) { setupAccordion(e.matches); });
  }

  /* 4. « Signaler ce lien » : insère l'adresse demandée dans le message */
  var report = d.getElementById('js-report-link');
  if (report && !/\/404\.html$/.test(location.pathname)) {
    report.href = report.href.replace(
      encodeURIComponent('[Insérez le lien ici]'),
      encodeURIComponent(location.href)
    );
  }
})();
