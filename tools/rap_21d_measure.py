#!/usr/bin/env python3
"""21D : styles calculés de rapport-consultations-dassa, résumé + onglets + panneaux."""
import os, http.server, socketserver, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); H.log_message = lambda *a, **k: None
srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = '''() => { const q = s => document.querySelector(s), qa = s => [...document.querySelectorAll(s)], cs = (e, ps) => { const c = getComputedStyle(e); return ps.map(p => c[p]).join(' '); };
 const o = {hs: document.documentElement.scrollWidth - innerWidth};
 o.tabs = qa('.rapport-nav [data-tab]').map(e => Math.round(e.getBoundingClientRect().height)).join(',');
 const n = q('.rapport-nav'); o.navScroll = n.scrollWidth > n.clientWidth + 1 ? 'defile(' + getComputedStyle(n).overflowX + ')' : 'tient';
 o.body = cs(q('.rapport-body'), ['gridTemplateColumns', 'paddingTop', 'paddingBottom']).slice(0, 60);
 o.sheet = cs(q('.rapport-sheet'), ['borderTopWidth', 'borderTopColor', 'boxShadow']).slice(0, 90) + ' w=' + Math.round(q('.rapport-sheet').getBoundingClientRect().width);
 o.h2 = qa('.rapport-summary h2, .rapport-section h2').map(e => Math.round(parseFloat(getComputedStyle(e).fontSize))).join(',');
 o.over = qa('.rapport-summary *, .rapport-content *').filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.right > innerWidth + 1 || r.left < -1); }).length;
 o.imgs = qa('.rapport-summary img, .rapport-content img').length;
 return o; }'''
with sync_playwright() as p:
    br = p.chromium.launch()
    for W in [320, 390, 768, 1024, 1280, 1920]:
        pg = br.new_page(viewport={'width': W, 'height': 800}); pg.goto(f'http://127.0.0.1:{port}/pages/rapport-consultations-dassa.html'); pg.wait_for_timeout(300)
        print(W, pg.evaluate(JS)); pg.close()
    br.close()
