/* ==========================================================================
   scroll-hint.js : indicateur de défilement horizontal (chevrons clignotants)
   --------------------------------------------------------------------------
   Usage : <div data-scroll-hint> <div data-scroll-hint-target> ... </div>
             <span class="…-hint" aria-hidden="true">…</span> </div>
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
    target.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    window.addEventListener('load', update);
    update();
  });
})();
