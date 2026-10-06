/* ════════════════════════════════════════════════
   LATO CORPS ONG — components/back-to-top.js
   Affiche le bouton "retour en haut" dès que la page est
   scrollée, le masque en haut de page. Mutualisé sur
   toutes les pages (Accueil, À propos, Actions).
   ════════════════════════════════════════════════ */
(function () {
  var btn = document.querySelector('.back-to-top');
  if (!btn) return;

  var SHOW_AFTER = 400; // px de scroll avant apparition
  var ticking = false;

  function updateVisibility() {
    var scrolled = window.scrollY || document.documentElement.scrollTop;
    btn.classList.toggle('is-visible', scrolled > SHOW_AFTER);
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(updateVisibility);
      ticking = true;
    }
  }, { passive: true });

  // État initial (rechargement avec scroll déjà positionné)
  updateVisibility();

  btn.addEventListener('click', function () {
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
  });
})();
