#!/usr/bin/env python3
"""21B : styles calculés de transparence-rapports, sections gov / demande / cta (rangs 4-6)."""
import os, http.server, socketserver, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); H.log_message = lambda *a, **k: None
srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = '''() => { const q = s => document.querySelector(s), cs = (e, ps) => { const c = getComputedStyle(e); return ps.map(p => c[p]).join(' '); };
 const o = {hs: document.documentElement.scrollWidth - document.documentElement.clientWidth};
 for (const k of ['gov', 'form', 'cta']) { const s = q('.transparence-' + k); o[k] = cs(s, ['paddingTop', 'paddingBottom']) + ' | h2 ' + cs(s.querySelector('h2'), ['fontSize']); }
 o.cards = [...document.querySelectorAll('.transparence-gov [class*=card], .transparence-gov article, .transparence-form .form-card')].map(e => cs(e, ['borderTopWidth', 'borderTopColor', 'boxShadow', 'backgroundColor']).slice(0, 110)).slice(0, 3).join(' || ');
 o.fields = [...document.querySelectorAll('.transparence-form :is(input,textarea,select):not([type=checkbox]):not([type=radio]):not([type=hidden]):not([name=_gotcha])')].map(e => Math.round(e.getBoundingClientRect().height) + '/' + getComputedStyle(e).fontSize).join(' ');
 o.checks = [...document.querySelectorAll('.transparence-form label')].map(e => Math.round(e.getBoundingClientRect().height)).join(',');
 o.btn = [...document.querySelectorAll('.transparence-gov .btn, .transparence-form .btn, .transparence-cta .btn')].map(e => Math.round(e.getBoundingClientRect().height) + (e.getBoundingClientRect().width > innerWidth ? '!W' : '')).join(',');
 o.secpad = getComputedStyle(document.documentElement).getPropertyValue('--section-pad-y').trim().slice(0, 40);
 return o; }'''
with sync_playwright() as p:
    br = p.chromium.launch()
    for W in [320, 390, 768, 1280, 1920]:
        pg = br.new_page(viewport={'width': W, 'height': 800}); pg.goto(f'http://127.0.0.1:{port}/pages/transparence-rapports.html'); pg.wait_for_timeout(300)
        print(W, pg.evaluate(JS)); pg.close()
    br.close()
