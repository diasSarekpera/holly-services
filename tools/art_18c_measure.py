import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const b=document.querySelector('.article-donation .btn'),c=getComputedStyle(b),r=b.getBoundingClientRect();
const rd=document.querySelector('.article-body');
return {sw:document.documentElement.scrollWidth,btn:[Math.round(r.width),Math.round(r.height),c.fontSize,c.paddingLeft,c.letterSpacing,c.gap],txt:b.textContent.trim().replace(/\\s+/g,' '),
read:Math.round(rd.getBoundingClientRect().width),nav:[...document.querySelectorAll('.article-nav__link')].map(e=>Math.round(e.getBoundingClientRect().height)),
h2:getComputedStyle(document.querySelector('.article-body h2')).fontSize}}'''
with sync_playwright() as p:
    br=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=br.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/article-prevention-cancer-peau.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    br.close()
