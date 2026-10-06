/*
 * tabs.js — onglets accessibles sur `[data-tabs]` (JS vanilla).
 *
 * Balisage (voir CONVENTIONS.md) :
 *   <div data-tabs data-tabs-hash>                     data-tabs-hash : synchronise l'URL (#id), un seul par page
 *     <div data-tabs-list aria-label="…">              role="tablist" posé par le JS
 *       <a href="#rapports" data-tab>Rapports</a>      ou <button data-tab aria-controls="rapports">
 *     </div>
 *     <section id="rapports" data-tab-panel>…</section>
 *   </div>
 * Sans JS : tous les panneaux restent visibles et les liens d'onglets sont de simples ancres.
 * Onglet initial : [data-tab-active] / aria-selected="true", sinon hash d'URL, sinon le premier.
 * Clavier : ← → (boucle), Home, End ; l'onglet focalisé est activé.
 */
(function () {
  'use strict';

  var uid = 0;

  function toArray(list) {
    return Array.prototype.slice.call(list);
  }

  function targetId(tab) {
    var id = tab.getAttribute('aria-controls');
    if (id) return id;
    var href = tab.getAttribute('href') || '';
    return href.charAt(0) === '#' ? decodeURIComponent(href.slice(1)) : '';
  }

  function initTabs(root) {
    if (root._tabsInit) return;

    var tabs = toArray(root.querySelectorAll('[data-tab]')).filter(function (t) {
      return t.closest('[data-tabs]') === root;
    });
    var panelsAll = toArray(root.querySelectorAll('[data-tab-panel]')).filter(function (p) {
      return p.closest('[data-tabs]') === root;
    });

    var items = [];
    tabs.forEach(function (tab) {
      var panel = document.getElementById(targetId(tab));
      if (panel && panelsAll.indexOf(panel) !== -1) items.push({ tab: tab, panel: panel });
    });
    if (!items.length) return;
    root._tabsInit = true;

    var useHash = root.hasAttribute('data-tabs-hash');
    var list = root.querySelector('[data-tabs-list]') || items[0].tab.parentNode;
    list.setAttribute('role', 'tablist');

    items.forEach(function (it) {
      if (!it.tab.id) it.tab.id = 'tab-' + (it.panel.id || ++uid);
      it.tab.setAttribute('role', 'tab');
      it.tab.setAttribute('aria-controls', it.panel.id);
      it.panel.setAttribute('role', 'tabpanel');
      it.panel.setAttribute('aria-labelledby', it.tab.id);
      it.panel.setAttribute('tabindex', '0');
    });

    function indexOfTab(tab) {
      for (var i = 0; i < items.length; i++) if (items[i].tab === tab) return i;
      return -1;
    }

    function indexFromHash() {
      var id = decodeURIComponent((window.location.hash || '').slice(1));
      if (!id) return -1;
      var el = document.getElementById(id);
      if (!el) return -1;
      for (var i = 0; i < items.length; i++) {
        if (items[i].panel === el || items[i].panel.contains(el)) return i;
      }
      return -1;
    }

    function select(index, opts) {
      opts = opts || {};
      items.forEach(function (it, i) {
        var on = i === index;
        it.tab.setAttribute('aria-selected', on ? 'true' : 'false');
        it.tab.setAttribute('tabindex', on ? '0' : '-1');
        it.tab.classList.toggle('is-active', on);
        it.panel.hidden = !on;
      });
      if (opts.focus) items[index].tab.focus();
      if (useHash && opts.updateHash && window.history && window.history.replaceState) {
        window.history.replaceState(null, '', '#' + items[index].panel.id);
      }
    }

    items.forEach(function (it, i) {
      it.tab.addEventListener('click', function (e) {
        e.preventDefault();
        select(i, { updateHash: true });
      });
    });

    list.addEventListener('keydown', function (e) {
      var current = indexOfTab(document.activeElement);
      if (current === -1) return;
      var next = -1;
      switch (e.key) {
        case 'ArrowRight': case 'Right': next = (current + 1) % items.length; break;
        case 'ArrowLeft': case 'Left': next = (current - 1 + items.length) % items.length; break;
        case 'Home': next = 0; break;
        case 'End': next = items.length - 1; break;
        case ' ': case 'Spacebar': next = current; break;
        default: return;
      }
      e.preventDefault();
      select(next, { focus: true, updateHash: true });
    });

    /* Onglet initial */
    var initial = -1;
    if (useHash) initial = indexFromHash();
    if (initial === -1) {
      for (var i = 0; i < items.length && initial === -1; i++) {
        if (items[i].tab.hasAttribute('data-tab-active') || items[i].tab.getAttribute('aria-selected') === 'true') initial = i;
      }
    }
    if (initial === -1) initial = 0;
    select(initial);

    if (useHash) {
      window.addEventListener('hashchange', function () {
        var idx = indexFromHash();
        if (idx !== -1) select(idx);
      });
    }
  }

  function init() {
    toArray(document.querySelectorAll('[data-tabs]')).forEach(initTabs);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
