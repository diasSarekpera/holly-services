/* Header fixe : état « défilé » + progression de lecture. */
(function () {
  var header = document.querySelector('.navbar');
  if (!header) return;

  var bar = document.createElement('span');
  bar.className = 'navbar__progress';
  bar.setAttribute('aria-hidden', 'true');
  header.appendChild(bar);

  var THRESHOLD = 24;
  var ticking = false;

  function update() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    header.classList.toggle('is-scrolled', y > THRESHOLD);
    header.style.setProperty('--scroll-progress', max > 0 ? Math.min(y / max, 1).toFixed(4) : 0);
    ticking = false;
  }

  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
})();
