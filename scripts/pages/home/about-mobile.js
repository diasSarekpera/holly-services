/* ════════════════════════════════════════════════
   HOLLY SERVICES ONG — about-mobile.js
   Indicateur dynamique du scroll horizontal des
   "piliers" (.about__pillars) sur mobile.

   Comportement :
   - Sur mobile, .about__pillars devient un carrousel
     horizontal en scroll-snap natif (voir about.css).
   - Ce script observe quel pilier est actuellement visible
     et met à jour le point actif correspondant dans
     .about__pillars-hint (3 points sous le carrousel).
   - Optionnel : sans ce script, le premier point reste
     simplement marqué actif en CSS (dégradation propre).
   - N'a aucun effet sur desktop / tablette large, où
     .about__pillars n'est pas un carrousel scrollable.

   Dépendance : aucune. IntersectionObserver natif.
   À charger en fin de <body>, avec ou sans `defer`.
   ════════════════════════════════════════════════ */

(function () {
  'use strict';

  var MOBILE_BREAKPOINT = 767; // doit correspondre au breakpoint CSS du carrousel

  var track = document.querySelector('.about__pillars');
  var hint  = document.querySelector('.about__pillars-hint');

  if (!track || !hint) return;

  var pillars = Array.prototype.slice.call(track.querySelectorAll('.about__pillar'));
  var dots    = Array.prototype.slice.call(hint.querySelectorAll('span'));

  if (pillars.length === 0 || dots.length === 0) return;

  var observer = null;
  var isActive = false;

  function setActiveDot(index) {
    dots.forEach(function (dot, i) {
      dot.classList.toggle('is-active', i === index);
    });
  }

  function handleIntersections(entries) {
    // On retient l'entrée la plus visible à l'instant T
    var mostVisible = entries.reduce(function (best, entry) {
      if (!best || entry.intersectionRatio > best.intersectionRatio) {
        return entry;
      }
      return best;
    }, null);

    if (mostVisible && mostVisible.intersectionRatio > 0.5) {
      var index = pillars.indexOf(mostVisible.target);
      if (index !== -1) setActiveDot(index);
    }
  }

  function startObserving() {
    if (isActive) return;
    isActive = true;

    observer = new IntersectionObserver(handleIntersections, {
      root: track,
      threshold: [0.5, 0.75, 1]
    });

    pillars.forEach(function (pillar) {
      observer.observe(pillar);
    });

    setActiveDot(0); // état initial cohérent
  }

  function stopObserving() {
    if (!isActive) return;
    isActive = false;

    if (observer) {
      observer.disconnect();
      observer = null;
    }
  }

  function syncWithViewport() {
    var isMobile = window.innerWidth <= MOBILE_BREAKPOINT;
    if (isMobile) {
      startObserving();
    } else {
      stopObserving();
    }
  }

  // Initialisation
  syncWithViewport();

  // Réévaluation au redimensionnement (rotation, fenêtre redimensionnée)
  var resizeTimeout;
  window.addEventListener('resize', function () {
    window.clearTimeout(resizeTimeout);
    resizeTimeout = window.setTimeout(syncWithViewport, 150);
  });

})();