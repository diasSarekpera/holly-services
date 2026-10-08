#!/usr/bin/env python3
"""Controle responsive partage. Usage : python tools/resp_check.py <page|all> [--widths 320,360,...] [--sections a-b]
Sortie <= 30 lignes ; detail complet en JSON dans /tmp/resp_check_*.json. Ne modifie aucun fichier du projet."""
import sys, os, json, glob, time, argparse, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_W = [320, 360, 390, 768, 1024, 1280, 1440, 1920]
TYPES = ['hscroll', 'tap<44', 'text<12', 'titre', 'img', 'btn-2lignes', 'largeur>vp']
MAXLINES = 30

JS = r'''([W, sa, sb]) => {
const out = [];
const vis = e => { const c = getComputedStyle(e), r = e.getBoundingClientRect();
  return c.display !== 'none' && c.visibility !== 'hidden' && r.width > 0 && r.height > 0; };
const sel = e => { let s = e.tagName.toLowerCase();
  if (e.id) return s + '#' + e.id;
  const cl = [...e.classList].slice(0, 2); if (cl.length) s += '.' + cl.join('.');
  const p = e.parentElement; if (p && p !== document.body) { const pc = [...p.classList][0];
    s = (pc ? '.' + pc : p.tagName.toLowerCase()) + '>' + s; } return s; };
let secs = [...document.querySelectorAll('section')];
const inScope = e => { if (!sa) return true; const k = secs.findIndex(s => s.contains(e)) + 1; return k >= sa && k <= sb; };
// element rogne par un ancêtre overflow != visible qui tient dans le viewport
const clipped = e => { for (let a = e.parentElement; a && a !== document.body && a !== document.documentElement; a = a.parentElement) {
  const c = getComputedStyle(a); if (c.overflowX !== 'visible' && a.getBoundingClientRect().right <= W + 0.5) return true; } return false; };
const fixedPos = e => { for (let a = e; a && a !== document.documentElement; a = a.parentElement) if (getComputedStyle(a).position === 'fixed') return true; return false; };
const add = (t, e, d) => out.push({t, s: sel(e), d: d || ''});
const all = [...document.querySelectorAll('body *')].filter(e => !['SCRIPT','STYLE','NOSCRIPT','BR','PATH','CIRCLE','LINE','RECT','POLYGON','POLYLINE','G','DEFS','USE'].includes(e.tagName.toUpperCase()));
// 1 defilement horizontal
const ox = document.documentElement.scrollWidth - document.documentElement.clientWidth;
if (ox > 0) { const c = all.filter(e => vis(e) && !fixedPos(e) && !clipped(e)).map(e => ({e, r: e.getBoundingClientRect()}))
  .filter(o => o.r.right > W + 0.5 || o.r.left < -0.5).sort((a, b) => b.r.width - a.r.width).slice(0, 5);
  out.push({t: 'hscroll', s: 'PAGE +' + ox + 'px', d: ''}); c.forEach(o => add('hscroll', o.e, 'r=' + Math.round(o.r.right) + ' w=' + Math.round(o.r.width))); }
const seen = new Set();
for (const e of all) { if (!vis(e) || !inScope(e)) continue;
  const r = e.getBoundingClientRect(), tag = e.tagName.toLowerCase(), c = getComputedStyle(e);
  const btnLike = tag === 'button' || (tag === 'a' && /btn|cta|button/.test(e.className));
  // 2 tap < 44 (mobile) : liens/boutons non « en ligne dans du texte », hors masques et skip-link
  if (W <= 767 && (tag === 'a' || tag === 'button') && c.display !== 'inline' && r.width > 2 && r.height > 2 && r.bottom > 0 && r.height < 43.5) add('tap<44', e, Math.round(r.height) + 'px');
  // 3 texte < 12 px
  if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(c.fontSize) < 12 && r.width > 2) add('text<12', e, c.fontSize);
  // 4 titres
  if (/^h[1-4]$/.test(tag) && !(r.width <= 2 && r.height <= 2)) { let bad = e.scrollWidth > e.clientWidth + 1 || r.right > W + 0.5 || r.left < -0.5;
    for (let a = e.parentElement; a && !bad && a !== document.body; a = a.parentElement) { if (getComputedStyle(a).overflow !== 'visible') { const ar = a.getBoundingClientRect(); if (r.right > ar.right + 1 || r.left < ar.left - 1 || r.bottom > ar.bottom + 1) bad = true; break; } }
    if (bad) add('titre', e, 'w=' + Math.round(r.width)); }
  // 5 images
  if (tag === 'img') { const p = e.parentElement.getBoundingClientRect(); const bits = [];
    if (r.right > p.right + 1 || r.left < p.left - 1) bits.push('depasse parent');
    if (!e.hasAttribute('width') || !e.hasAttribute('height')) bits.push('sans width/height');
    if (bits.length) add('img', e, bits.join('+')); }
  // 6 bouton sur 2 lignes
  if (btnLike || e.classList.contains('btn')) { const ls = new Set(); const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n;
    while (n = w.nextNode()) { if (!n.textContent.trim()) continue; const pe = n.parentElement.getBoundingClientRect(); if (pe.width <= 2 || pe.height <= 2) continue;
      const q = document.createRange(); q.selectNodeContents(n); [...q.getClientRects()].forEach(x => { if (x.width > 0) ls.add(Math.round(x.top / 4)); }); }
    if (ls.size > 1) add('btn-2lignes', e, ls.size + ' lignes'); }
  // 7 largeur > viewport (hors elements rogne / fixes)
  if (r.width > W + 1 && !fixedPos(e) && !clipped(e)) add('largeur>vp', e, 'w=' + Math.round(r.width));
}
return out; }'''

def serve():
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(H, directory=ROOT)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h); srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def resolve(arg):
    allp = ['index.html', '404.html'] + sorted('pages/' + os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'pages', '*.html')))
    if arg == 'all': return allp
    for cand in (arg, arg + '.html', 'pages/' + arg, 'pages/' + arg + '.html'):
        if cand in allp: return [cand]
    sys.exit('page inconnue : ' + arg + ' (essayer : all, index.html, a-propos...)')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('page'); ap.add_argument('--widths'); ap.add_argument('--sections')
    a = ap.parse_args()
    widths = [int(x) for x in a.widths.split(',')] if a.widths else DEFAULT_W
    sa, sb = 0, 0
    if a.sections:
        p = a.sections.split('-'); sa = int(p[0]); sb = int(p[-1])
    pages = resolve(a.page); srv = serve(); port = srv.server_address[1]
    res = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w in widths:
            ctx = b.new_context(viewport={'width': w, 'height': 900})
            for pg in pages:
                page = ctx.new_page()
                try:
                    page.goto(f'http://127.0.0.1:{port}/{pg}', wait_until='load'); page.wait_for_timeout(150)
                    for f in page.evaluate(JS, [w, sa, sb]): res.append({'page': pg, 'w': w, **f})
                except Exception as ex:
                    res.append({'page': pg, 'w': w, 't': 'erreur', 's': str(ex)[:60], 'd': ''})
                page.close()
            ctx.close()
        b.close()
    srv.shutdown()
    path = f'/tmp/resp_check_{int(time.time())}.json'
    json.dump(res, open(path, 'w'), ensure_ascii=False, indent=1)
    groups = {}
    for r in res: groups.setdefault((r['page'], r['w'], r['t']), []).append(r)
    order = lambda k: (TYPES.index(k[2]) if k[2] in TYPES else 99, k[0], k[1])
    lines = []
    for k in sorted(groups, key=order):
        items = groups[k]; cnt = {}
        for i in items: cnt[i['s']] = cnt.get(i['s'], 0) + 1
        sels = ', '.join(s + (f'x{n}' if n > 1 else '') for s, n in list(cnt.items())[:3])
        lines.append(f"{k[0]} {k[1]} {k[2]} n={len(items)} {sels}"[:170])
    head = f"{len(pages)} page(s) x {len(widths)} largeurs : {len(res)} constats, {len(groups)} groupes"
    if not res: print(head + ' : OK'); print('detail : ' + path); return
    room = MAXLINES - 2
    shown = lines[:room] if len(lines) <= room else lines[:room - 1] + [f'... +{len(lines) - room + 1} groupes (voir JSON)']
    print(head); [print(l) for l in shown]; print('detail : ' + path)

if __name__ == '__main__': main()
