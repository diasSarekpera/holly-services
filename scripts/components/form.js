/*
 * form.js — validation et envoi des formulaires `<form data-form>` (JS vanilla).
 *
 * Balisage attendu (tout est optionnel sauf data-form) :
 *   <form data-form data-endpoint="https://…">        sans data-endpoint = MODE DÉMO (rien n'est envoyé)
 *     <p class="form__error" id="x-err">…</p>         message sous le champ (créé si absent)
 *     <input type="file" accept=".pdf,image/*" data-max-size="5">   taille max en Mo
 *     <div class="form__hp"><input name="website" …></div>        honeypot (à masquer en CSS)
 *     <div data-form-status></div>                    région aria-live (créée si absente)
 *     <div data-form-success>…</div>                  affiché au succès (à masquer par défaut en CSS)
 *   </form>
 * États exposés pour le CSS : form[data-state="loading|success|error"], `.is-visible` sur
 * [data-form-success] (l'attribut `hidden` est aussi retiré), `aria-invalid="true"` sur les champs.
 */
(function () {
  'use strict';

  var NBSP = '\u00a0';
  var DEMO_DELAY = 600;
  var uid = 0;

  function toArray(list) {
    return Array.prototype.slice.call(list);
  }

  function isHoneypot(el) {
    return !!el.closest('.form__hp');
  }

  function getFields(form) {
    return toArray(form.elements).filter(function (el) {
      var tag = el.tagName;
      if (tag !== 'INPUT' && tag !== 'SELECT' && tag !== 'TEXTAREA') return false;
      var type = (el.type || '').toLowerCase();
      if (type === 'submit' || type === 'button' || type === 'reset' || type === 'hidden' || type === 'image') return false;
      if (el.disabled || isHoneypot(el)) return false;
      return true;
    });
  }

  /* Un seul champ « représentant » par groupe de boutons radio. */
  function getControls(form) {
    var seen = {};
    return getFields(form).filter(function (el) {
      if (el.type !== 'radio' || !el.name) return true;
      if (seen[el.name]) return false;
      seen[el.name] = true;
      return true;
    });
  }

  function groupOf(form, el) {
    if (el.type === 'radio' && el.name) {
      return toArray(form.querySelectorAll('input[type="radio"]')).filter(function (r) {
        return r.name === el.name;
      });
    }
    return [el];
  }

  /* ---------- Messages ---------- */

  function fileMessage(el) {
    var files = toArray(el.files || []);
    if (!files.length) return '';
    var accept = (el.getAttribute('accept') || '').split(',').map(function (t) {
      return t.trim().toLowerCase();
    }).filter(Boolean);
    var max = parseFloat(String(el.getAttribute('data-max-size') || '').replace(',', '.'));
    var i, f, name, ok, j, tok;
    for (i = 0; i < files.length; i++) {
      f = files[i];
      name = f.name.toLowerCase();
      if (accept.length) {
        ok = false;
        for (j = 0; j < accept.length && !ok; j++) {
          tok = accept[j];
          if (tok.charAt(0) === '.') ok = name.slice(-tok.length) === tok;
          else if (tok.slice(-2) === '/*') ok = (f.type || '').toLowerCase().indexOf(tok.slice(0, -1)) === 0;
          else ok = (f.type || '').toLowerCase() === tok;
        }
        if (!ok) {
          return 'Le format du fichier «' + NBSP + f.name + NBSP + '» n’est pas accepté. Formats acceptés' + NBSP + ': ' + accept.join(', ') + '.';
        }
      }
      if (max > 0 && f.size > max * 1024 * 1024) {
        return 'Le fichier «' + NBSP + f.name + NBSP + '» dépasse la taille maximale de ' + String(max).replace('.', ',') + NBSP + 'Mo.';
      }
    }
    return '';
  }

  function messageFor(form, el) {
    var custom = el.getAttribute('data-error-msg');
    var type = (el.type || '').toLowerCase();
    var v = el.validity;
    var group, ok, i;

    if (type === 'radio') {
      group = groupOf(form, el);
      ok = false;
      for (i = 0; i < group.length; i++) if (group[i].checked) ok = true;
      if (!ok && group.some(function (r) { return r.required; })) {
        return custom || 'Veuillez sélectionner une option.';
      }
      return '';
    }

    if (type === 'file') {
      if (el.required && !(el.files && el.files.length)) return custom || 'Veuillez joindre un fichier.';
      return fileMessage(el);
    }

    if (v.valid) return '';
    if (v.valueMissing) {
      if (type === 'checkbox') return custom || 'Veuillez cocher cette case pour continuer.';
      if (el.tagName === 'SELECT') return custom || 'Veuillez choisir une option.';
      return custom || 'Ce champ est obligatoire.';
    }
    if (v.typeMismatch) {
      if (type === 'email') return 'Veuillez saisir une adresse e-mail valide (exemple' + NBSP + ': nom@domaine.org).';
      if (type === 'url') return 'Veuillez saisir une adresse web valide (commençant par https://).';
      return 'La valeur saisie n’est pas valide.';
    }
    if (v.patternMismatch) return el.getAttribute('data-pattern-msg') || el.title || 'Le format saisi n’est pas valide.';
    if (v.tooShort) return 'Veuillez saisir au moins ' + el.minLength + ' caractères (' + el.value.length + ' saisis).';
    if (v.tooLong) return 'Veuillez saisir au plus ' + el.maxLength + ' caractères.';
    if (v.rangeUnderflow) return 'La valeur doit être supérieure ou égale à ' + el.min + '.';
    if (v.rangeOverflow) return 'La valeur doit être inférieure ou égale à ' + el.max + '.';
    if (v.stepMismatch) return 'La valeur saisie n’est pas valide.';
    if (v.badInput) return 'La valeur saisie n’est pas valide.';
    return custom || 'La valeur saisie n’est pas valide.';
  }

  /* ---------- Éléments d'erreur ---------- */

  function errorElFor(form, el) {
    if (el._formError) return el._formError;
    var ids = (el.getAttribute('aria-describedby') || '').split(/\s+/);
    var i, found = null, container, p;

    for (i = 0; i < ids.length && !found; i++) {
      if (ids[i]) {
        p = document.getElementById(ids[i]);
        if (p && p.classList.contains('form__error')) found = p;
      }
    }
    if (!found) {
      container = el.closest('fieldset') && el.type === 'radio' ? el.closest('fieldset') : el.closest('.form__field, .form__group');
      if (container && container.querySelectorAll('input, select, textarea').length === 1) {
        found = container.querySelector('.form__error');
      }
      if (!found) {
        found = document.createElement('p');
        found.className = 'form__error';
        if (container) {
          container.appendChild(found);
        } else {
          var anchor = el.closest('label') || el;
          anchor.parentNode.insertBefore(found, anchor.nextSibling);
        }
      }
    }
    if (!found.id) found.id = 'form-error-' + (++uid);
    found.setAttribute('data-form-error', '');
    el._formError = found;
    return found;
  }

  function addDescribedBy(el, id) {
    var ids = (el.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
    if (ids.indexOf(id) === -1) ids.push(id);
    el.setAttribute('aria-describedby', ids.join(' '));
  }

  function removeDescribedBy(el, id) {
    var ids = (el.getAttribute('aria-describedby') || '').split(/\s+/).filter(function (x) {
      return x && x !== id;
    });
    if (ids.length) el.setAttribute('aria-describedby', ids.join(' '));
    else el.removeAttribute('aria-describedby');
  }

  function setInvalid(form, el, message) {
    var err = errorElFor(form, el);
    err.textContent = message;
    err.hidden = false;
    groupOf(form, el).forEach(function (f) {
      f.setAttribute('aria-invalid', 'true');
      addDescribedBy(f, err.id);
    });
  }

  function clearInvalid(form, el) {
    var err = el._formError;
    groupOf(form, el).forEach(function (f) {
      f.removeAttribute('aria-invalid');
      if (err) removeDescribedBy(f, err.id);
    });
    if (err) {
      err.textContent = '';
      err.hidden = true;
    }
  }

  function validateField(form, el) {
    var msg = messageFor(form, el);
    if (msg) setInvalid(form, el, msg);
    else clearInvalid(form, el);
    return !msg;
  }

  /* ---------- Initialisation d'un formulaire ---------- */

  function initForm(form) {
    if (form._formInit) return;
    form._formInit = true;
    form.setAttribute('novalidate', '');

    var status = form.querySelector('[data-form-status]');
    var success = form.querySelector('[data-form-success]');
    var busy = false;

    if (!status) {
      status = document.createElement('div');
      status.className = 'form__status';
      status.setAttribute('data-form-status', '');
      form.appendChild(status);
    }
    status.setAttribute('aria-live', 'polite');
    status.setAttribute('role', 'status');
    status.setAttribute('aria-atomic', 'true');

    if (success && !success.hasAttribute('tabindex')) success.setAttribute('tabindex', '-1');

    /* Honeypot : hors parcours clavier et lecteurs d'écran */
    toArray(form.querySelectorAll('.form__hp')).forEach(function (hp) {
      hp.setAttribute('aria-hidden', 'true');
      toArray(hp.querySelectorAll('input, textarea, select')).forEach(function (f) {
        f.setAttribute('tabindex', '-1');
        f.setAttribute('autocomplete', 'off');
      });
    });

    function say(text, kind) {
      status.textContent = text;
      status.classList.toggle('form__status--error', kind === 'error');
      status.classList.toggle('form__status--success', kind === 'success');
    }

    function setBusy(on) {
      busy = on;
      form.setAttribute('aria-busy', on ? 'true' : 'false');
      toArray(form.querySelectorAll('[type="submit"], button:not([type])')).forEach(function (b) {
        b.disabled = on;
      });
      if (on) form.setAttribute('data-state', 'loading');
    }

    function hideSuccess() {
      if (!success) return;
      success.classList.remove('is-visible');
      success.hidden = true;
    }

    function showSuccess() {
      form.setAttribute('data-state', 'success');
      say(success ? '' : 'Votre message a bien été envoyé. Merci.', 'success');
      if (success) {
        success.hidden = false;
        success.classList.add('is-visible');
        success.focus();
      }
    }

    function finishOk() {
      setBusy(false);
      form.reset();
      toArray(form.querySelectorAll('[aria-invalid]')).forEach(function (f) {
        clearInvalid(form, f);
      });
      showSuccess();
    }

    function send() {
      var endpoint = form.getAttribute('data-endpoint');
      setBusy(true);
      say('Envoi en cours…', null);

      if (!endpoint) {
        console.warn('[form] mode démo : aucun envoi (pas de data-endpoint).');
        window.setTimeout(finishOk, DEMO_DELAY);
        return;
      }

      fetch(endpoint, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        finishOk();
      }).catch(function () {
        setBusy(false);
        form.setAttribute('data-state', 'error');
        say('L’envoi a échoué (erreur réseau ou serveur). Vérifiez votre connexion puis réessayez.', 'error');
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (busy) return;

      hideSuccess();
      form.removeAttribute('data-state');

      /* Honeypot rempli : faux succès, rien n'est envoyé */
      var hpFilled = toArray(form.querySelectorAll('.form__hp input, .form__hp textarea')).some(function (f) {
        return f.value && f.value.trim() !== '';
      });
      if (hpFilled) {
        finishOk();
        return;
      }

      var invalid = getControls(form).filter(function (el) {
        return !validateField(form, el);
      });

      if (invalid.length) {
        form.setAttribute('data-state', 'error');
        say(invalid.length === 1
          ? 'Le formulaire contient 1 erreur. Veuillez la corriger puis renvoyer.'
          : 'Le formulaire contient ' + invalid.length + ' erreurs. Veuillez les corriger puis renvoyer.', 'error');
        invalid[0].focus();
        return;
      }

      say('', null);
      send();
    });

    /* Correction en direct : un champ déjà signalé se revalide à la saisie */
    function live(e) {
      var el = e.target;
      if (getFields(form).indexOf(el) === -1) return;
      if (el.getAttribute('aria-invalid') === 'true' || (el.type === 'file' && e.type === 'change')) {
        validateField(form, el);
      }
    }
    form.addEventListener('input', live);
    form.addEventListener('change', live);

    form.addEventListener('reset', function () {
      hideSuccess();
      form.removeAttribute('data-state');
    });
  }

  function init() {
    toArray(document.querySelectorAll('form[data-form]')).forEach(initForm);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
