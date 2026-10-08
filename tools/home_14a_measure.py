#!/usr/bin/env python3
"""14A : styles calcules (backdrop-filter, fond, taille/marge) des 2 pastilles hero/about/missions, a 3 largeurs."""
import sys,os,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R)
H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
with sync_playwright() as p:
    b=p.chromium.launch()
    for W in (390,1024,1440):
        pg=b.new_page(viewport={'width':W,'height':900});pg.goto(f'http://127.0.0.1:{s.server_address[1]}/index.html');pg.wait_for_timeout(1500)
        for sel in ('.about__stat-card','.mission__img-kpi'):
            r=pg.evaluate("""s=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e),b=e.getBoundingClientRect();return [c.backdropFilter,c.backgroundColor,Math.round(b.width)+'x'+Math.round(b.height),Math.round(b.left)]}""",sel)
            print(W,sel,r)
    b.close()
