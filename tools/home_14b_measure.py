#!/usr/bin/env python3
"""14B : taille des titres de section (h2), padding vertical des sections et titres de cartes, sections 2-9 de l accueil, 3 largeurs."""
import os,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(("127.0.0.1",0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
J="""()=>[...document.querySelectorAll("section")].slice(1,9).map(x=>{const h=x.querySelector("h2"),c=getComputedStyle(h),p=getComputedStyle(x);return x.id+" h2="+c.fontSize+" lh="+c.lineHeight+" pad="+p.paddingTop+"/"+p.paddingBottom}).join(" ; ")"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for W in (390,1024,1440):
        pg=b.new_page(viewport={"width":W,"height":900});pg.goto(f"http://127.0.0.1:{s.server_address[1]}/index.html");pg.wait_for_timeout(800)
        print(W,pg.evaluate(J))
    b.close()
