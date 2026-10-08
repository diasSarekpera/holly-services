#!/usr/bin/env python3
"""Non-régression de la charte Holly-services (25A).

Usage (racine du projet) :  python3 tools/regress.py [--root .] [--quick] [-v]
  --quick : 1280 px seulement pour le débordement (au lieu de 6 largeurs)
  -v      : détail complet des KO (sinon 3 premiers par contrôle)
Sortie : tableau OK/KO (<= 30 lignes). Code de sortie 1 s'il y a un KO.
Mesure par styles calculés (Playwright, serveur HTTP local temporaire, requêtes externes bloquées).
Lecture seule : ne modifie aucun fichier du site.

Interprétations (à ajuster ici si la charte évolue) :
- « bandeau de chiffres dans le hero d'accueil » = aucun élément visible dont la classe
  contient stat/metric/counter/kpi/chiffre à l'intérieur de .hero (le badge et la preuve sociale restent permis).
- « eyebrow d'accueil » = tous les .eyebrow de index.html ont ligne + libellé non vide + point,
  et une seule signature typographique (taille, graisse, interlettrage, casse, couleur).
- « rythme Mission » = écarts mesurés sur pages/a-propos.html .mission : eyebrow→h2 = --rhythm-eyebrow,
  paragraphe→paragraphe = --rhythm-p (1280 et 390 px).
- « valeurs » = .values a le fond --clr-section-alt, assez soutenu : aucun canal > 244 (EDF0F4 = 237/240/244).
- « héros photo » = toutes les pages de pages/ sauf maintenance.html : .hero-photo visible (>= 200 px) avec un h1.
"""
import argparse, glob, os, re, sys, collections, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

CARDS = """.why-card,.card-besoin,.erreur404-card,.mission-detail__card,.value-card,.team-card,.article-cta__card,
.benevolat-format-card,.maintenance__contact-card,.action-card,.action-tile,.actualites-card,.article-card,.campagne-card,
.campagne-don,.benevolat-mission-card,.job-sidebar,.temoignage-card,.rapport-result-card,.card-soutien,.reason-card,.form-card,
.metier-card,.banner-card,.chiffre-card,.cta-card,.partner-logo-tile""".replace('\n', '')
CARD_REST = dict(bg='rgb(255, 255, 255)', bw='1px', bc='rgba(16, 35, 63, 0.18)', sh='rgba(16, 35, 63, 0.08) 0px 1px 3px 0px')
CARD_HOVER = dict(bc='rgba(16, 35, 63, 0.32)', sh='rgba(16, 35, 63, 0.1) 0px 2px 8px 0px')
WIDTHS = [320, 390, 768, 1024, 1280, 1920]
JS_PROBE = """
() => {
  const rgb = v => { const e = document.createElement('i'); e.style.color = v; document.body.appendChild(e);
    const c = getComputedStyle(e).color; e.remove(); return c; };
  const len = v => { const e = document.createElement('i'); e.style.cssText = 'position:absolute;visibility:hidden;width:' + v;
    document.body.appendChild(e); const w = e.getBoundingClientRect().width; e.remove(); return w; };
  const root = getComputedStyle(document.documentElement);
  return { secondary: rgb('var(--clr-secondary)'), primary: rgb('var(--clr-primary)'), alt: rgb('var(--clr-section-alt)'),
           rEyebrow: len('var(--rhythm-eyebrow)'), rP: len('var(--rhythm-p)') };
}"""
JS_HEADER = """
() => {
  const n = document.querySelector('.navbar'); if (!n) return null;
  const wraps = [];
  n.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || el.closest('.navbar__dropdown,.mobile-menu')) return;
    const tn = [...el.childNodes].filter(t => t.nodeType === 3 && t.textContent.trim()); if (!tn.length) return;
    const tops = new Set(); tn.forEach(t => { const r = document.createRange(); r.selectNodeContents(t); [...r.getClientRects()].filter(x => x.width > 0).forEach(x => tops.add(Math.round(x.top))); });
    if (tops.size > 1) wraps.push((el.className || el.tagName).toString().split(' ')[0]);
  });
  const inner = n.querySelector('.navbar__inner') || n;
  return { h: Math.round(n.getBoundingClientRect().height * 10) / 10, wraps, over: inner.scrollWidth > inner.clientWidth + 1 };
}"""
JS_CARDS = """
(sel) => { const out = []; const seen = new Set();
  document.querySelectorAll(sel).forEach(e => { const r = e.getBoundingClientRect(); if (r.width < 40 || r.height < 40) return;
    const k = [...e.classList].find(c => sel.includes('.' + c)); if (seen.has(k)) return; seen.add(k); e.setAttribute('data-rg', out.length); out.push(k); });
  return out; }"""
JS_STYLE = """
(i) => { const e = document.querySelector('[data-rg="' + i + '"]'); const c = getComputedStyle(e); const r = e.getBoundingClientRect();
  return { bg: c.backgroundColor, bw: c.borderTopWidth, bs: c.borderTopStyle, bc: c.borderTopColor, sh: c.boxShadow, tf: c.transform, x: r.x, y: r.y, w: r.width }; }"""
JS_GHOST = """
() => { const out = []; document.querySelectorAll('.btn--ghost,.btn--ghost-light').forEach((e, i) => { const r = e.getBoundingClientRect();
  if (r.width < 20 || r.height < 20 || getComputedStyle(e).visibility === 'hidden') return; if (out.length >= 4) return; e.setAttribute('data-rgg', i); out.push(i); });
  return out; }"""
JS_GSTYLE = """
(i) => { const e = document.querySelector('[data-rgg="' + i + '"]'); const c = getComputedStyle(e);
  return { bw: c.borderTopWidth, bs: c.borderTopStyle, bc: c.borderTopColor, bg: c.backgroundColor, tf: c.transform }; }"""
JS_QUOTES = """
(m) => { const bad = [], seen = []; const pink = c => { const x = c.match(/[\\d.]+/g).map(Number); return x[3] !== 0 && x[0] > 150 && x[1] < 110 && x[2] > 50 && x[0] > x[2]; };
  document.querySelectorAll('blockquote,[class*="quote"],[class*="citation"]').forEach(e => { const c = getComputedStyle(e);
    if (c.backgroundColor !== m) return; seen.push(1); const nm = (e.className || e.tagName).toString().split(' ')[0];
    for (const s of ['Left', 'Right']) if (parseFloat(c['border' + s + 'Width']) >= 2 && c['border' + s + 'Style'] !== 'none' && pink(c['border' + s + 'Color'])) bad.push(nm + ' border-' + s);
    for (const p of ['::before', '::after']) { const q = getComputedStyle(e, p);
      if (q.content !== 'none' && q.position === 'absolute' && parseFloat(q.width) > 0 && parseFloat(q.width) <= 8 && parseFloat(q.height) >= 16 && q.backgroundColor !== 'rgba(0, 0, 0, 0)') bad.push(nm + p); } });
  return { n: seen.length, bad }; }"""
JS_HOME = """
() => { const h = document.querySelector('.hero'); const st = h ? [...h.querySelectorAll('*')].filter(e => /stat|metric|counter|kpi|chiffre/i.test(e.className && e.className.baseVal === undefined ? e.className : '') && e.getBoundingClientRect().width > 0).map(e => e.className) : null;
  const ey = [...document.querySelectorAll('.eyebrow')].map(e => { const l = e.querySelector('.eyebrow__label'), c = l ? getComputedStyle(l) : null;
    return { ok: !!(l && l.textContent.trim() && e.querySelector('.eyebrow__line') && e.querySelector('.eyebrow__dot')), sig: c ? [c.fontSize, c.fontWeight, c.letterSpacing, c.textTransform, c.color].join('|') : '' }; });
  return { hero: !!h, stats: st, ey }; }"""
JS_MISSION = """
() => { const s = document.querySelector('.mission'); if (!s) return null; const e = s.querySelector('.eyebrow'), h = s.querySelector('h2'); const ps = [...s.querySelectorAll('.mission__paragraph')];
  const out = {}; if (e && h) out.eh = h.getBoundingClientRect().top - e.getBoundingClientRect().bottom;
  if (ps.length > 1) out.pp = ps[1].getBoundingClientRect().top - ps[0].getBoundingClientRect().bottom; return out; }"""
JS_VALUES = """
() => { const s = document.querySelector('.values'); return s ? { bg: getComputedStyle(s).backgroundColor, cards: s.querySelectorAll('.value-card').length } : null; }"""
JS_HEROPHOTO = """
() => { const h = document.querySelector('.hero-photo'); if (!h) return null; const r = h.getBoundingClientRect();
  return { h: Math.round(r.height), h1: !!h.querySelector('h1'), css: [...document.styleSheets].some(s => (s.href || '').includes('hero-photo.css')) }; }"""


def undefined_vars(root, page_path):
    html = open(page_path, encoding='utf8').read()
    base = os.path.dirname(page_path)
    hrefs = re.findall(r'<link[^>]+href="([^"]+\.css)"', html)
    css = ''
    for h in hrefs:
        p = os.path.normpath(os.path.join(root if h.startswith('/') else base, h.lstrip('/') if h.startswith('/') else h))
        if os.path.exists(p):
            css += open(p, encoding='utf8').read()
    defined = set(re.findall(r'(--[\w-]+)\s*:', css + html))
    for js in glob.glob(os.path.join(root, 'scripts', '**', '*.js'), recursive=True):
        defined |= set(re.findall(r"setProperty\(\s*['\"](--[\w-]+)", open(js, encoding='utf8').read()))
    used = set(re.findall(r'var\(\s*(--[\w-]+)\s*\)', css + html))   # sans repli
    return sorted(used - defined)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root', default='.'); ap.add_argument('--quick', action='store_true'); ap.add_argument('-v', action='store_true')
    a = ap.parse_args(); root = os.path.abspath(a.root)
    pages = [os.path.join(root, 'index.html'), os.path.join(root, '404.html')] + sorted(glob.glob(os.path.join(root, 'pages', '*.html')))
    pages = [p for p in pages if os.path.exists(p)]
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x): pass
    srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=root)); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    U = lambda p: 'http://127.0.0.1:%d/%s' % (port, os.path.relpath(p, root).replace(os.sep, '/'))
    R = collections.OrderedDict()   # id -> [label, ok_count, total, [fails]]

    def rec(k, label, page, ok, why=''):
        r = R.setdefault(k, [label, 0, 0, []]); r[2] += 1
        if ok: r[1] += 1
        else: r[3].append('%s%s' % (os.path.relpath(page, root).replace('pages/', ''), (':' + why) if why else ''))

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        def ctx(w):
            c = b.new_context(viewport={'width': w, 'height': 900}); c.route(re.compile(r'^https?://(?!127\.0\.0\.1)'), lambda r: r.abort()); return c
        for w in ([1280] if a.quick else WIDTHS):
            c = ctx(w); pg = c.new_page(); pg.set_default_timeout(3000)
            for p in pages:
                pg.goto(U(p), wait_until='domcontentloaded'); pg.wait_for_timeout(250)
                ov = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
                rec('12', 'Aucun débordement horizontal (%s px)' % ('/'.join(map(str, [1280] if a.quick else WIDTHS))), p, ov <= 0, '%dpx@%d' % (ov, w))
            c.close()
        # Header 1024/1280/1920 : 100 puis 80 px, sans retour à la ligne
        for w in (1024, 1280, 1920):
            c = ctx(w); pg = c.new_page(); pg.set_default_timeout(3000)
            for p in pages:
                pg.goto(U(p), wait_until='domcontentloaded'); pg.wait_for_timeout(250)
                top = pg.evaluate(JS_HEADER)
                if top is None: rec('01', 'Header 100 px au sommet', p, True, 'sans header'); rec('02', 'Header 80 px après défilement', p, True); rec('03', 'Header sans retour à la ligne', p, True); continue
                pg.evaluate('window.scrollTo(0, 700)'); pg.wait_for_timeout(600); sc = pg.evaluate(JS_HEADER)
                rec('01', 'Header 100 px au sommet (1024/1280/1920)', p, top['h'] == 100, '%s@%d' % (top['h'], w))
                rec('02', 'Header 80 px après défilement', p, sc['h'] == 80, '%s@%d' % (sc['h'], w))
                rec('03', 'Header sans retour à la ligne ni débordement', p, not top['wraps'] and not sc['wraps'] and not top['over'], '%s@%d' % (','.join(top['wraps'] + sc['wraps']) or 'overflow', w))
            c.close()
        # Pages à 1280 px : cartes, ghost, citations, accueil, mission, valeurs, héros
        c = ctx(1280); pg = c.new_page(); pg.set_default_timeout(3000)
        for p in pages:
            name = os.path.relpath(p, root); isp = name.startswith('pages')
            pg.goto(U(p), wait_until='domcontentloaded'); pg.wait_for_timeout(500)
            P = pg.evaluate(JS_PROBE)
            # cartes (repos + survol, 1 instance par classe)
            for i, k in enumerate(pg.evaluate(JS_CARDS, CARDS)):
                try:
                    el = pg.locator('[data-rg="%d"]' % i); el.scroll_into_view_if_needed(); pg.mouse.move(0, 0); pg.wait_for_timeout(120); s0 = pg.evaluate(JS_STYLE, i)
                    el.hover(); pg.wait_for_timeout(320); s1 = pg.evaluate(JS_STYLE, i)
                except Exception: continue
                rest = s0['bg'] == CARD_REST['bg'] and s0['bw'] == '1px' and s0['bs'] == 'solid' and s0['bc'] == CARD_REST['bc'] and s0['sh'] == CARD_REST['sh']
                hov = s1['bc'] == CARD_HOVER['bc'] and s1['sh'] == CARD_HOVER['sh'] and s1['tf'] == 'none' and abs(s1['y'] - s0['y']) < .5 and abs(s1['x'] - s0['x']) < .5
                rec('04', 'Cartes : fond/bordure/ombre au repos', p, rest, '.%s' % k); rec('05', 'Cartes : survol bordure+ombre, sans déplacement', p, hov, '.%s' % k)
            # boutons ghost
            for i in pg.evaluate(JS_GHOST):
                try:
                    el = pg.locator('[data-rgg="%d"]' % i); el.scroll_into_view_if_needed(); pg.mouse.move(0, 0); pg.wait_for_timeout(120); g0 = pg.evaluate(JS_GSTYLE, i)
                    el.hover(); pg.wait_for_timeout(320); g1 = pg.evaluate(JS_GSTYLE, i)
                except Exception: continue
                vis = g0['bs'] != 'none' and float(g0['bw'][:-2]) >= 1 and not g0['bc'].endswith(', 0)')
                rec('06', 'Ghost : bordure visible par défaut', p, vis, 'btn#%d' % i)
                rec('07', 'Ghost : survol = fond seul (bordure inchangée)', p, g1['bc'] == g0['bc'] and g1['bw'] == g0['bw'] and g1['tf'] == 'none', 'btn#%d' % i)
            q = pg.evaluate(JS_QUOTES, P['secondary']); rec('08', 'Citations marine sans filet rose latéral', p, not q['bad'], ','.join(q['bad']))
            if name == 'index.html':
                h = pg.evaluate(JS_HOME)
                rec('09', 'Hero accueil sans bandeau de chiffres', p, h['hero'] and not h['stats'], str(h['stats'])[:40])
                sigs = {e['sig'] for e in h['ey']}
                rec('10', 'Eyebrows accueil complets et uniformes', p, bool(h['ey']) and all(e['ok'] for e in h['ey']) and len(sigs) == 1, '%d eyebrow, %d signatures' % (len(h['ey']), len(sigs)))
            if name == os.path.join('pages', 'a-propos.html'):
                for w in (1280, 390):
                    pg.set_viewport_size({'width': w, 'height': 900}); pg.wait_for_timeout(300); P2 = pg.evaluate(JS_PROBE); m = pg.evaluate(JS_MISSION)
                    ok = bool(m) and abs(m.get('eh', -99) - P2['rEyebrow']) <= 1.5 and abs(m.get('pp', -99) - P2['rP']) <= 1.5
                    rec('11', 'Rythme Mission À propos (1280 et 390)', p, ok, '%s vs eyebrow %.0f / p %.0f @%d' % (m, P2['rEyebrow'], P2['rP'], w))
                pg.set_viewport_size({'width': 1280, 'height': 900}); pg.wait_for_timeout(300)
                v = pg.evaluate(JS_VALUES); ch = [int(x) for x in re.findall(r'\d+', v['bg'])[:3]] if v else [255]
                rec('13', 'Fond section Valeurs soutenu (--clr-section-alt)', p, bool(v) and v['bg'] == P['alt'] and max(ch) <= 244 and v['cards'] > 0, v['bg'] if v else 'absent')
            if isp and not name.endswith('maintenance.html'):
                hp = pg.evaluate(JS_HEROPHOTO); rec('14', 'Héros photo présent (h1, >= 200 px, feuille liée)', p, bool(hp) and hp['h'] >= 200 and hp['h1'] and hp['css'], str(hp))
            u = undefined_vars(root, p); rec('15', 'Aucune variable CSS indéfinie', p, not u, ','.join(u[:3]))
        c.close(); b.close()

    # Tableau
    ko = 0; lines = ['%-3s %-52s %-4s %s' % ('N°', 'Contrôle', 'Etat', 'Détail')]
    for k in sorted(R):
        label, ok, tot, fails = R[k]; st = 'OK' if not fails else 'KO'; ko += bool(fails)
        det = '%d/%d' % (ok, tot) if not fails else '%d/%d ; %s' % (ok, tot, ' | '.join(sorted(set(fails))[: (99 if a.v else 3)]))
        lines.append('%-3s %-52s %-4s %s' % (k, label[:52], st, det[:110 if not a.v else 999]))
    lines.append('Bilan : %d contrôles, %d KO, %d pages%s' % (len(R), ko, len(pages), ' (mode rapide)' if a.quick else ''))
    print('\n'.join(lines)); sys.exit(1 if ko else 0)


if __name__ == '__main__':
    main()
