#!/usr/bin/env python3
"""14C : styles calcules (flou, fond, bordure, couleur) de .team-card__index, .team-card__social-btn et .soutenir__amount, repos et survol, a 1440 et 390."""
import os,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(("127.0.0.1",0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
G="""s=>{const e=document.querySelector(s),c=getComputedStyle(e),b=e.getBoundingClientRect();return [c.backdropFilter,c.backgroundColor,c.borderTopColor,c.color,Math.round(b.width)+"x"+Math.round(b.height)].join(" | ")}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for W in (1440,390):
        pg=b.new_page(viewport={"width":W,"height":900});pg.goto(f"http://127.0.0.1:{s.server_address[1]}/index.html");pg.wait_for_timeout(800)
        print(W,".team-card__index",pg.evaluate(G,".team-card__index"))
        for sel in (".team-card__social-btn",".soutenir__amount"):
            pg.locator(sel).first.scroll_into_view_if_needed();print(W,sel,"repos",pg.evaluate(G,sel))
            if W==1440: pg.locator(sel).first.hover();pg.wait_for_timeout(400);print(W,sel,"survol",pg.evaluate(G,sel))
    b.close()
