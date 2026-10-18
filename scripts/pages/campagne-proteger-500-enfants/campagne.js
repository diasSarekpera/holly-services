/* Page « Protéger 500 enfants en 2026 » : chiffres de campagne, sélecteur de don, partage.
   Source des chiffres : attributs data-* de <main data-campaign> (data-raised, data-goal,
   data-pct, data-remaining, data-donors). Sans JS, les textes statiques de la page restent valables. */
(function () {
  'use strict';

  var NB = '\u00a0';
  var root = document.querySelector('[data-campaign]');
  if (!root) return;

  function euros(n) {
    return new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 }).format(n) + NB + '\u20ac';
  }

  /* ── Chiffres + jauge ── */
  var d = root.dataset;
  var raised = Number(d.raised), goal = Number(d.goal), pct = Number(d.pct), remaining = Number(d.remaining);
  var values = {
    raised: isNaN(raised) ? null : euros(raised),
    goal: isNaN(goal) ? null : euros(goal),
    remaining: isNaN(remaining) ? null : euros(remaining),
    donors: d.donors || null
  };
  root.querySelectorAll('[data-campaign-field]').forEach(function (el) {
    var v = values[el.getAttribute('data-campaign-field')];
    if (v !== null && v !== undefined) el.textContent = v;
  });
  var bar = root.querySelector('[data-campaign-progress]');
  if (bar && !isNaN(pct) && values.raised && values.goal) {
    bar.value = pct;
    bar.max = 100;
    bar.textContent = pct + NB + '%';
    bar.setAttribute('aria-label', values.raised + ' collectés sur un objectif de ' + values.goal + ', soit ' + pct + NB + '%');
  }

  /* ── Sélecteur de don : met à jour le libellé du bouton (la destination reste index.html#dons) ── */
  var widget = root.querySelector('[data-donation-widget]');
  if (widget) {
    var cta = widget.querySelector('[data-donation-cta]');
    var update = function () {
      var amount = widget.querySelector('input[name="montant"]:checked');
      var freq = widget.querySelector('input[name="frequence"]:checked');
      if (!cta || !amount) return;
      if (amount.value === 'autre') { cta.textContent = 'Faire un don'; return; }
      cta.textContent = 'Donner ' + amount.value + NB + '\u20ac' + (freq && freq.value === 'mensuel' ? ' par mois' : '');
    };
    widget.addEventListener('change', update);
    update();
  }

  /* ── Partage ── */
  var url = window.location.href.split('#')[0];
  var text = document.title;
  var targets = {
    whatsapp: 'https://wa.me/?text=' + encodeURIComponent(text + ' ' + url),
    facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url),
    linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url)
  };
  document.querySelectorAll('[data-share]').forEach(function (a) {
    var t = targets[a.getAttribute('data-share')];
    if (t && /^https?:/.test(url)) a.setAttribute('href', t);
  });

  var copyBtn = document.querySelector('[data-copy-link]');
  var status = document.querySelector('[data-copy-status]');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      var say = function (m) { if (status) status.textContent = m; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(
          function () { say('Lien copié.'); },
          function () { say('Copie impossible : copiez l\u2019adresse depuis la barre du navigateur.'); }
        );
      } else {
        say('Copie impossible : copiez l\u2019adresse depuis la barre du navigateur.');
      }
    });
  }
})();
