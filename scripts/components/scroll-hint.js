/* ==========================================================================
   scroll-hint.js : indicateur de défilement horizontal (chevrons clignotants)
   --------------------------------------------------------------------------
   Usage : <div data-scroll-hint> <div data-scroll-hint-target> ... </div>
             <button data-scroll-hint-next aria-label="…">chevrons</button> </div>
   Un clic sur le bouton fait défiler la liste (smooth, instantané si reduced-motion).
   Ajoute .is-scrollable quand le contenu dépasse, .is-end quand on est au bout.
   Sans JS : l'indicateur reste masqué (amélioration progressive).
   ========================================================================== */
(function () {
  'use strict';
  var wraps = document.querySelectorAll('[data-scroll-hint]');
  Array.prototype.forEach.call(wraps, function (wrap) {
    var target = wrap.querySelector('[data-scroll-hint-target]');
    if (!target) return;
    function update() {
      var scrollable = target.scrollWidth > target.clientWidth + 4;
      var atEnd = target.scrollLeft + target.clientWidth >= target.scrollWidth - 6;
      wrap.classList.toggle('is-scrollable', scrollable);
      wrap.classList.toggle('is-end', atEnd);
    }
    var next = wrap.querySelector('[data-scroll-hint-next]');
    if (next) {
      next.addEventListener('click', function () {
        var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        target.scrollBy({ left: Math.max(target.clientWidth * 0.85, 120), behavior: reduce ? 'auto' : 'smooth' });
      });
    }
    target.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    window.addEventListener('load', update);
    update();
  });
})();
