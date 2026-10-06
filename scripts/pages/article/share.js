/* Article : partage sans SDK (Facebook, LinkedIn, X, WhatsApp), copie du lien, impression.
   URL partagée = <link rel="canonical"> de la page (repli : adresse courante).
   Sans JS : les liens gardent leur href statique ; « Copier » et « Imprimer » restent inertes. */
(function () {
  'use strict';

  var canon = document.querySelector('link[rel="canonical"]');
  var url = (canon && canon.getAttribute('href')) || window.location.href.split('#')[0];
  var text = document.title;
  var enc = encodeURIComponent;

  var targets = {
    facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + enc(url),
    linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + enc(url),
    x: 'https://x.com/intent/post?url=' + enc(url) + '&text=' + enc(text),
    whatsapp: 'https://wa.me/?text=' + enc(text + ' ' + url)
  };
  document.querySelectorAll('[data-share]').forEach(function (a) {
    var t = targets[a.getAttribute('data-share')];
    if (t) a.setAttribute('href', t);
  });

  var status = document.querySelector('[data-copy-status]');
  var say = function (m) { if (status) status.textContent = m; };
  var fail = 'Copie impossible\u00a0: copiez l\u2019adresse depuis la barre du navigateur.';

  /* Repli sans API Clipboard (anciens navigateurs, contexte non sécurisé) */
  function legacyCopy() {
    var ta = document.createElement('textarea');
    ta.value = url;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.top = '-1000px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  var copyBtn = document.querySelector('[data-copy-link]');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      var done = function () { say('Lien copié.'); };
      var other = function () { say(legacyCopy() ? 'Lien copié.' : fail); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, other);
      } else {
        other();
      }
    });
  }

  var printBtn = document.querySelector('[data-print]');
  if (printBtn) {
    printBtn.addEventListener('click', function () { window.print(); });
  }
})();
