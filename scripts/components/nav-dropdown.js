/* ════════════════════════════════════════════════
   HOLLY SERVICES ONG — nav-dropdown.js
   Sous-menus de la navbar desktop + accordéons du menu mobile.

   Clavier (sous-menus desktop) :
   - Entrée / Espace sur le bouton : ouvre/ferme (aria-expanded à jour)
   - ↓ / ↑ sur le bouton : ouvre et place le focus sur le premier / dernier lien
   - ↓ ↑ (boucle), Début, Fin dans le sous-menu
   - Échap : ferme et rend le focus au bouton (le survol est aussi masqué
     tant que la souris ne quitte/ré-entre pas : classe is-dismissed)
   - Le focus qui quitte le composant le ferme
   L'ouverture est pilotée par .is-open / le survol, jamais par :focus-within,
   pour que l'état visuel reste cohérent avec aria-expanded.
   ════════════════════════════════════════════════ */
(function () {
  'use strict';

  var DESKTOP_BREAKPOINT = 1024;
  var dropdownItems = Array.prototype.slice.call(
    document.querySelectorAll('.navbar__item--dropdown')
  );

  function isDesktop() {
    return window.innerWidth >= DESKTOP_BREAKPOINT;
  }

  function triggerOf(item) {
    return item.querySelector('[data-dropdown-trigger]');
  }

  function linksOf(item) {
    return Array.prototype.slice.call(item.querySelectorAll('.navbar__dropdown a[href]'));
  }

  function setOpen(item, open) {
    var trigger = triggerOf(item);
    item.classList.toggle('is-open', open);
    if (trigger) trigger.setAttribute('aria-expanded', String(open));
  }

  function closeAll(except) {
    dropdownItems.forEach(function (item) {
      if (item === except) return;
      setOpen(item, false);
    });
  }

  function openAndFocus(item, last) {
    var links = linksOf(item);
    if (!links.length) return;
    closeAll(item);
    item.classList.remove('is-dismissed');
    setOpen(item, true);
    (last ? links[links.length - 1] : links[0]).focus();
  }

  dropdownItems.forEach(function (item) {
    var trigger = triggerOf(item);
    if (!trigger) return;

    // Clic / Entrée / Espace : bascule le sous-menu.
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var willOpen = !item.classList.contains('is-open');
      closeAll(item);
      item.classList.remove('is-dismissed');
      setOpen(item, willOpen);
    });

    // Survol : uniquement actif en résolution desktop.
    item.addEventListener('mouseenter', function () {
      if (!isDesktop()) return;
      closeAll(item);
      item.classList.remove('is-dismissed');
      setOpen(item, true);
    });

    item.addEventListener('mouseleave', function () {
      item.classList.remove('is-dismissed');
      if (!isDesktop()) return;
      setOpen(item, false);
    });

    // Flèches, Début, Fin.
    item.addEventListener('keydown', function (e) {
      var key = e.key;
      if (e.target === trigger) {
        if (key === 'ArrowDown' || key === 'Down') {
          e.preventDefault();
          openAndFocus(item, false);
        } else if (key === 'ArrowUp' || key === 'Up') {
          e.preventDefault();
          openAndFocus(item, true);
        }
        return;
      }
      var links = linksOf(item);
      var i = links.indexOf(document.activeElement);
      if (i === -1) return;
      var next = -1;
      if (key === 'ArrowDown' || key === 'Down') next = (i + 1) % links.length;
      else if (key === 'ArrowUp' || key === 'Up') next = (i - 1 + links.length) % links.length;
      else if (key === 'Home') next = 0;
      else if (key === 'End') next = links.length - 1;
      else return;
      e.preventDefault();
      links[next].focus();
    });

    // Fermeture si le focus quitte entièrement le composant (bouton + sous-menu).
    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget)) setOpen(item, false);
    });
  });

  // Fermer au clic en dehors (utile en mode clic mobile/tablette).
  document.addEventListener('click', function (e) {
    var clickedInsideDropdown = dropdownItems.some(function (item) {
      return item.contains(e.target);
    });
    if (!clickedInsideDropdown) closeAll();
  });

  // Échap : ferme (y compris l'ouverture au survol) et rend le focus au bouton.
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    var active = document.activeElement;
    dropdownItems.forEach(function (item) {
      var isHovered = item.matches && item.matches(':hover');
      if (!item.classList.contains('is-open') && !isHovered) return;
      item.classList.add('is-dismissed');
      setOpen(item, false);
      var trigger = triggerOf(item);
      if (trigger && item.contains(active) && active !== trigger) trigger.focus();
    });
  });

  // ── Accordéons du menu mobile plein écran ──
  var mobileToggles = Array.prototype.slice.call(
    document.querySelectorAll('[data-mobile-toggle]')
  );
  mobileToggles.forEach(function (toggle) {
    toggle.addEventListener('click', function () {
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      var submenu = document.getElementById(toggle.getAttribute('aria-controls'));
      if (submenu) submenu.classList.toggle('is-open', !expanded);
    });
  });
})();
