#!/usr/bin/env python3
"""17A : .actions-filter__btn au repos/survol (fond, bordure, couleur) a 1440 + hauteur des liens .action-card__link / .action-tile__link a 390."""
import os,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(("127.0.0.1",0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
G="""s=>{const e=document.querySelectorAll(s)[1]||document.querySelector(s),c=getComputedStyle(e);return [c.backgroundColor,c.borderTopColor,c.color].join(" | ")}"""
with sync_playwright() as p:
    b=p.chromium.launch();u=f"http://127.0.0.1:{s.server_address[1]}/pages/actions.html"
    pg=b.new_page(viewport={"width":1440,"height":900});pg.goto(u);pg.wait_for_timeout(800)
    sel=".actions-filter__btn:not(.is-active):not([aria-pressed=true])";l=pg.locator(sel).first
    print("filtre repos",l.evaluate("e=>{const c=getComputedStyle(e);return [c.backgroundColor,c.borderTopColor,c.color].join(\" | \")}"));l.hover();pg.wait_for_timeout(400)
    print("filtre survol",l.evaluate("e=>{const c=getComputedStyle(e);return [c.backgroundColor,c.borderTopColor,c.color].join(\" | \")}"))
    pg=b.new_page(viewport={"width":390,"height":900});pg.goto(u);pg.wait_for_timeout(800)
    for q in (".action-card__link",".action-tile__link"): print("390",q,pg.evaluate("q=>[...document.querySelectorAll(q)].map(e=>Math.round(e.getBoundingClientRect().height)).join(\",\")",q))
    b.close()
