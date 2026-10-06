/* ════════════════════════════════════════════════
   HOLLY SERVICES ONG — hero-mobile.js
   Ouverture / fermeture du menu mobile plein écran.

   Comportements couverts :
   - Ouverture via #nav-toggle, fermeture via #nav-close
   - Fermeture : touche Échap, clic en dehors du panneau,
     clic sur un lien de navigation (data-mobile-link)
   - Verrouillage du scroll du body pendant l'ouverture
   - Focus trap (le focus reste dans le menu tant qu'il est ouvert)
   - Restitution du focus au bouton hamburger à la fermeture
   - Synchronisation des attributs ARIA (aria-expanded, aria-hidden)
   - Fermeture automatique si la fenêtre repasse en desktop
     (évite un menu mobile "fantôme" ouvert en arrière-plan)

   Dépendance : aucune. Vanilla JS, à charger en fin de <body>
   ou avec l'attribut `defer`.
   ════════════════════════════════════════════════ */

(function () {
  'use strict';

  var DESKTOP_BREAKPOINT = 1024;

  var toggleBtn = document.getElementById('nav-toggle');
  var closeBtn  = document.getElementById('nav-close');
  var menu      = document.getElementById('nav-mobile');

  if (!toggleBtn || !menu) return;

  var isOpen = false;
  var lastFocusedElement = null;

  function isDesktop() {
    return window.innerWidth >= DESKTOP_BREAKPOINT;
  }

  function getFocusableElements() {
    var selector = [
      'a[href]',
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])'
    ].join(',');
    return Array.prototype.slice.call(menu.querySelectorAll(selector))
      .filter(function (el) {
        // exclut les éléments masqués (display:none) et ceux d'un accordéon fermé (visibility:hidden)
        return el.offsetParent !== null && window.getComputedStyle(el).visibility !== 'hidden';
      });
  }

  function openMenu() {
    if (isOpen || isDesktop()) return;
    isOpen = true;

    lastFocusedElement = document.activeElement;

    menu.classList.add('is-open');
    menu.setAttribute('aria-hidden', 'false');
    toggleBtn.setAttribute('aria-expanded', 'true');
    toggleBtn.setAttribute('aria-label', 'Fermer le menu');

    document.body.style.overflow = 'hidden';
    document.body.classList.add('nav-mobile-open');

    // Focus initial sur le bouton de fermeture, ou le premier élément focusable
    window.requestAnimationFrame(function () {
      var target = closeBtn || getFocusableElements()[0];
      if (target) target.focus();
    });

    document.addEventListener('keydown', onKeydown);
    document.addEventListener('click', onClickOutside, true);
  }

  function closeMenu() {
    if (!isOpen) return;
    isOpen = false;

    menu.classList.remove('is-open');
    menu.setAttribute('aria-hidden', 'true');
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.setAttribute('aria-label', 'Ouvrir le menu');

    document.body.style.overflow = '';
    document.body.classList.remove('nav-mobile-open');

    document.removeEventListener('keydown', onKeydown);
    document.removeEventListener('click', onClickOutside, true);

    // Referme proprement tous les sous-menus accordéon ouverts
    closeAllSubmenus();

    // Restitue le focus au déclencheur d'origine
    var refocus = lastFocusedElement && document.contains(lastFocusedElement)
      ? lastFocusedElement
      : toggleBtn;
    refocus.focus();
    lastFocusedElement = null;
  }

  function closeAllSubmenus() {
    var toggles = menu.querySelectorAll('[data-mobile-toggle][aria-expanded="true"]');
    Array.prototype.forEach.call(toggles, function (toggle) {
      toggle.setAttribute('aria-expanded', 'false');
      var submenu = document.getElementById(toggle.getAttribute('aria-controls'));
      if (submenu) submenu.classList.remove('is-open');
    });
  }

  function onKeydown(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      closeMenu();
      return;
    }
    if (e.key === 'Tab') {
      trapFocus(e);
    }
  }

  function trapFocus(e) {
    var focusable = getFocusableElements();
    if (focusable.length === 0) return;

    var first = focusable[0];
    var last = focusable[focusable.length - 1];

    // Focus tombé hors du menu (clic dans le vide, etc.) : on le ramène dedans.
    if (!menu.contains(document.activeElement)) {
      e.preventDefault();
      (e.shiftKey ? last : first).focus();
      return;
    }

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  function onClickOutside(e) {
    // Le panneau occupe tout l'écran ; "en dehors" signifie ici un clic
    // qui n'a touché ni le menu, ni le bouton hamburger qui l'a ouvert.
    if (menu.contains(e.target) || toggleBtn.contains(e.target)) return;
    closeMenu();
  }

  // Bascule au clic sur le hamburger
  toggleBtn.addEventListener('click', function () {
    if (isOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  // Bouton de fermeture dédié
  if (closeBtn) {
    closeBtn.addEventListener('click', closeMenu);
  }

  // Fermeture au clic sur un lien de navigation du menu mobile
  var navLinks = menu.querySelectorAll('[data-mobile-link]');
  Array.prototype.forEach.call(navLinks, function (link) {
    link.addEventListener('click', function () {
      closeMenu();
    });
  });

  // Sécurité : si la fenêtre est redimensionnée vers le format desktop
  // pendant que le menu mobile est ouvert, on le referme proprement
  // pour éviter tout état incohérent entre navbar desktop et menu mobile.
  var resizeTimeout;
  window.addEventListener('resize', function () {
    window.clearTimeout(resizeTimeout);
    resizeTimeout = window.setTimeout(function () {
      if (isOpen && isDesktop()) closeMenu();
    }, 150);
  });

})();