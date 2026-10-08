#!/usr/bin/env python3
"""21C : styles calculés de rapport-consultations-dassa, hero + section 1 (chiffres clés)."""
import os, http.server, socketserver, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); H.log_message = lambda *a, **k: None
srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = '''() => { const q = s => document.querySelector(s), cs = (e, ps) => { const c = getComputedStyle(e); return ps.map(p => c[p]).join(' '); };
 const o = {hs: document.documentElement.scrollWidth - innerWidth};
 const s = q('.rapport-results'); o.pad = cs(s, ['paddingTop', 'paddingBottom']);
 o.cols = cs(q('.rapport-results__grid'), ['gridTemplateColumns']).split(' ').length;
 const c = q('.rapport-result-card'); o.card = cs(c, ['backgroundColor', 'borderTopWidth', 'borderTopColor', 'boxShadow']).slice(0, 120);
 const r0 = c.getBoundingClientRect().top; o.val = cs(q('.rapport-result-card__value'), ['fontSize']);
 o.over = [...document.querySelectorAll('.rapport-result-card *')].filter(e => e.scrollWidth > e.clientWidth + 1).length;
 o.h1 = cs(q('main h1'), ['fontSize']); o.btns = [...document.querySelectorAll('.rapport-intro__actions .btn')].map(e => Math.round(e.getBoundingClientRect().height)).join(',');
 return o; }'''
with sync_playwright() as p:
    br = p.chromium.launch()
    for W in [320, 390, 768, 1024, 1280, 1920]:
        pg = br.new_page(viewport={'width': W, 'height': 800}); pg.goto(f'http://127.0.0.1:{port}/pages/rapport-consultations-dassa.html'); pg.wait_for_timeout(300)
        o = pg.evaluate(JS)
        c = pg.query_selector('.rapport-result-card'); t0 = c.bounding_box()['y']; c.hover(); pg.wait_for_timeout(350)
        o['hover'] = pg.evaluate("()=>{const c=document.querySelector('.rapport-result-card'),s=getComputedStyle(c);return s.borderTopColor+' '+s.boxShadow.slice(0,45)}")
        o['dy'] = round(c.bounding_box()['y'] - t0, 1)
        print(W, o); pg.close()
    br.close()
