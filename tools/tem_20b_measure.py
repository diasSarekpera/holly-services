#!/usr/bin/env python3
"""20B : styles calculés de la page partager-temoignage (h2 vs --fs-h2, form-card, bande signal, boutons, champs)."""
import os, http.server, socketserver, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); H.log_message = lambda *a, **k: None
srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = '''() => { const cs = (e, ps) => { const c = getComputedStyle(e); return ps.map(p => c[p]).join(' '); };
 const tok = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
 const o = {hs: document.documentElement.scrollWidth - document.documentElement.clientWidth, fsH2tok: tok('--fs-h2'), secpad: tok('--section-pad-y')};
 o.h2 = [...document.querySelectorAll('main h2')].map(e => cs(e, ['fontSize','marginBottom'])).join(' | ');
 const fc = document.querySelector('.form-card'); if (fc) o.formcard = cs(fc, ['paddingTop','paddingLeft','borderTopWidth','boxShadow']);
 const sg = document.querySelector('.temoignage-signal'); if (sg) o.signal = cs(sg, ['paddingTop','paddingBottom']);
 o.inputs = [...document.querySelectorAll('main input:not([type=checkbox]):not([type=radio]):not([type=hidden]), main textarea, main select')].map(e => Math.round(e.getBoundingClientRect().height) + '/' + getComputedStyle(e).fontSize).join(' ');
 o.btn = [...document.querySelectorAll('main .btn')].map(e => Math.round(e.getBoundingClientRect().height)).join(',');
 return o; }'''
with sync_playwright() as p:
    br = p.chromium.launch()
    for W in [320, 390, 768, 1280, 1920]:
        pg = br.new_page(viewport={'width': W, 'height': 800}); pg.goto(f'http://127.0.0.1:{port}/pages/partager-temoignage.html'); pg.wait_for_timeout(300)
        print(W, pg.evaluate(JS)); pg.close()
    br.close()
