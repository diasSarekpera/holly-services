#!/usr/bin/env python3
"""20A : mesure du bouton ghost du bandeau partenariats (largeur de texte vs conteneur)."""
import os, sys, http.server, socketserver, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
H.log_message = lambda *a, **k: None
srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = '''() => { const b = document.querySelector('.partenariats-intro__actions .btn--ghost');
 const c = getComputedStyle(b), r = b.getBoundingClientRect();
 const p = b.parentElement.getBoundingClientRect();
 return {w: Math.round(r.width), h: Math.round(r.height), pw: Math.round(p.width), fs: c.fontSize, ws: c.whiteSpace, pad: c.paddingLeft, ls: c.letterSpacing,
   hs: document.documentElement.scrollWidth - document.documentElement.clientWidth}; }'''
with sync_playwright() as p:
    br = p.chromium.launch(); 
    for W in [320, 360, 390, 480, 768, 1280]:
        pg = br.new_page(viewport={'width': W, 'height': 800}); pg.goto(f'http://127.0.0.1:{port}/pages/devenir-partenaire.html'); pg.wait_for_timeout(300)
        print(W, pg.evaluate(JS)); pg.close()
    br.close()
