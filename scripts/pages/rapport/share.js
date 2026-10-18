/* Rapport : bouton « Partager » (Web Share API, repli : copie du lien). */
(function () {
  'use strict';
  var btn = document.querySelector('[data-share-page]');
  if (!btn) return;
  var status = document.querySelector('[data-share-status]');
  var url = window.location.href.split('#')[0];
  var say = function (m) { if (status) status.textContent = m; };
  var fail = 'Copie impossible\u00a0: copiez l\u2019adresse depuis la barre du navigateur.';

  function legacyCopy() {
    var ta = document.createElement('textarea');
    ta.value = url;
    ta.setAttribute('readonly', '');
    ta.className = 'visually-hidden';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  function copy() {
    var other = function () { say(legacyCopy() ? 'Lien copié.' : fail); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { say('Lien copié.'); }, other);
    } else {
      other();
    }
  }

  btn.addEventListener('click', function () {
    if (navigator.share) {
      navigator.share({ title: document.title, url: url }).catch(function (e) {
        if (!e || e.name !== 'AbortError') copy();
      });
    } else {
      copy();
    }
  });
})();
