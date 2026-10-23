/* ==========================================================================
   count-up.js : compteur animé de la section « Notre impact en chiffres »
   --------------------------------------------------------------------------
   - Les nombres [data-count] montent de 0 à leur valeur quand la section entre
     à l'écran ; la barre de pourcentage se remplit au même moment.
   - Sans JS, sans IntersectionObserver ou avec prefers-reduced-motion :
     valeurs finales affichées tout de suite (aucune animation).
   ========================================================================== */
(function () {
  'use strict';
  var section = document.getElementById('impact');
  if (!section) return;

  var nums = section.querySelectorAll('[data-count]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduce || !('IntersectionObserver' in window) || !nums.length) {
    section.classList.add('is-visible');
    return;
  }

  document.documentElement.classList.add('has-countup');

  function format(n) {
    return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  Array.prototype.forEach.call(nums, function (el) {
    el.textContent = '0' + (el.getAttribute('data-suffix') || '');
  });

  function run() {
    section.classList.add('is-visible');
    Array.prototype.forEach.call(nums, function (el) {
      var target = parseFloat(el.getAttribute('data-count')) || 0;
      var suffix = el.getAttribute('data-suffix') || '';
      var duration = 1600;
      var start = null;
      function step(t) {
        if (start === null) start = t;
        var p = Math.min((t - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = format(target * eased) + suffix;
        if (p < 1) window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    });
  }

  var io = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) { io.disconnect(); run(); }
  }, { threshold: 0.3 });
  io.observe(section);
})();
