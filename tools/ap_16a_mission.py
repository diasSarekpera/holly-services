#!/usr/bin/env python3
"""16A : rythme de la section Mission (a-propos) : ecarts verticaux eyebrow->titre->1er paragraphe->bloc bleu->image, + tokens --rhythm-* et flou du badge."""
import os,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(("127.0.0.1",0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
J="""()=>{const q=s=>document.querySelector("#mission "+s),r=e=>e.getBoundingClientRect(),T=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const eb=q(".eyebrow"),h=q("h2"),p=q(".mission__paragraph"),bq=q(".mission__quote"),fg=q(".mission__figure"),bd=q(".mission__figure-badge");
const d=(a,b)=>Math.round(r(b).top-r(a).bottom);const c=getComputedStyle(bd);
const lastp=[...document.querySelectorAll("#mission .mission__paragraph")].pop();
return "eb>h2="+d(eb,h)+" h2>p="+d(h,p)+" lastp>quote="+d(lastp,bq)+" quote>fig="+(r(fg).top>=r(bq).bottom?d(bq,fg):"cote-a-cote")+" | tok eb="+T("--rhythm-eyebrow")+" title="+T("--rhythm-title")+" p="+T("--rhythm-p")+" block="+T("--rhythm-block")+" media="+T("--rhythm-media")+" | badge blur="+c.backdropFilter+" bg="+c.backgroundColor}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for W in (390,768,1024,1440):
        pg=b.new_page(viewport={"width":W,"height":900});pg.goto(f"http://127.0.0.1:{s.server_address[1]}/pages/a-propos.html");pg.wait_for_timeout(800);print(W,pg.evaluate(J))
    b.close()
