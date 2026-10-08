import os,sys,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R)
h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const g=(s)=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e),r=e.getBoundingClientRect();return [Math.round(r.height),c.paddingTop,c.borderTopColor]};
const md=[...document.querySelectorAll('.missions-detail *')].filter(e=>getComputedStyle(e).display==='grid'||getComputedStyle(e).display==='flex').slice(0,4).map(e=>e.className+':'+getComputedStyle(e).display+':'+(getComputedStyle(e).gridTemplateColumns||getComputedStyle(e).flexDirection).slice(0,40));
return {intro:g('.missions-intro'),anchor:g('.missions-anchors__link'),res:g('.resultats'),md,sw:document.documentElement.scrollWidth}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,768,1280):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/nos-missions.html');pg.wait_for_timeout(400)
        print(w,pg.evaluate(JS))
    pg.hover('.missions-anchors__link');pg.wait_for_timeout(400);print('hover',pg.evaluate("getComputedStyle(document.querySelector('.missions-anchors__link')).borderTopColor"))
    b.close()
