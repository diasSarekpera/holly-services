#!/usr/bin/env python3
"""V197 : les chevrons clignotants des chiffres clés (Soutenir, accueil mobile) deviennent un vrai bouton :
un clic / une touche fait défiler la liste automatiquement (smooth). Idempotent."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
p = root / 'index.html'; s = p.read_text(encoding='utf-8')
if 'data-scroll-hint-next' not in s:
    pat = re.compile(r'<span class="soutenir__impact-hint" aria-hidden="true">(.*?)</span>', re.S)
    m = pat.search(s); assert m
    inner = m.group(1).replace('<svg ', '<svg aria-hidden="true" ')
    s = s[:m.start()] + ('<button type="button" class="soutenir__impact-hint" data-scroll-hint-next aria-label="Voir les autres chiffres">' + inner + '</button>') + s[m.end():]
    p.write_text(s, encoding='utf-8')
js = root / 'scripts' / 'components' / 'scroll-hint.js'; t = js.read_text(encoding='utf-8')
if 'data-scroll-hint-next' not in t:
    t = t.replace("    target.addEventListener('scroll', update, { passive: true });",
"""    var next = wrap.querySelector('[data-scroll-hint-next]');
    if (next) {
      next.addEventListener('click', function () {
        var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        target.scrollBy({ left: Math.max(target.clientWidth * 0.85, 120), behavior: reduce ? 'auto' : 'smooth' });
      });
    }
    target.addEventListener('scroll', update, { passive: true });""")
    t = t.replace("Usage : <div data-scroll-hint> <div data-scroll-hint-target> ... </div>\n             <span class=\"…-hint\" aria-hidden=\"true\">…</span> </div>",
                  "Usage : <div data-scroll-hint> <div data-scroll-hint-target> ... </div>\n             <button data-scroll-hint-next aria-label=\"…\">chevrons</button> </div>\n   Un clic sur le bouton fait défiler la liste (smooth, instantané si reduced-motion).")
    js.write_text(t, encoding='utf-8')
css = root / 'styles' / 'home.css'; c = css.read_text(encoding='utf-8')
if 'V197' not in c:
    css.write_text(c.rstrip('\n') + '''

/* V197 Soutenir : chevrons = bouton cliquable (zone de toucher 44 px, focus visible) */
.soutenir__impact-hint{z-index:5;pointer-events:auto;cursor:pointer;border:0;margin:0;font:inherit;height:2.75rem;width:4.5rem;top:-0.3rem;-webkit-tap-highlight-color:transparent}
.soutenir__impact-hint:focus-visible{outline:2px solid var(--clr-primary);outline-offset:2px;border-radius:var(--radius-sm,4px)}
@media (hover:hover){.soutenir__impact-hint:hover svg{stroke-width:3}}
''', encoding='utf-8')
print('ok')
