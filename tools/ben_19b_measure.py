import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const A=document.querySelector('.benevolat-apply');
const f=[...A.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([name=_gotcha]),select,textarea')].filter(e=>e.getBoundingClientRect().width>0);
const hs=f.map(e=>Math.round(e.getBoundingClientRect().height));const fs=[...new Set(f.map(e=>getComputedStyle(e).fontSize))];
const bc=[...new Set(f.map(e=>getComputedStyle(e).borderTopColor))];
const lab=[...A.querySelectorAll('label')].filter(l=>l.querySelector('input[type=checkbox]')).map(l=>Math.round(l.getBoundingClientRect().height));
const sb=A.querySelector('button[type=submit]');const r=sb.getBoundingClientRect();
const g=getComputedStyle(A.querySelector('.benevolat-form-grid')).gridTemplateColumns.split(' ').length;
const over=[...A.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+0.5).length;
return {sw:document.documentElement.scrollWidth,cols:g,hmin:Math.min(...hs),fs,bc,chk:lab,sub:Math.round(r.width)+'x'+Math.round(r.height),pad:getComputedStyle(A).paddingTop,over}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/devenir-benevole.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    b.close()
