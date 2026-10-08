import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const C=document.querySelector('#candidature')||document.querySelector('.candidature-layout');
const vis=e=>e.getBoundingClientRect().width>0;
const f=[...C.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([name=_gotcha]),select,textarea')].filter(vis);
const H=e=>Math.round(e.getBoundingClientRect().height);
const file=C.querySelector('input[type=file]');const lab=[...C.querySelectorAll('label')].filter(l=>l.querySelector('input[type=checkbox]')&&vis(l)).map(H);
const sb=C.querySelector('button[type=submit]');
const det=document.querySelector('.job-details:not([hidden])');
const over=[...document.querySelectorAll('.job-details:not([hidden]) *,.candidature-layout *')].filter(e=>e.getBoundingClientRect().right>innerWidth+0.5).length;
return {sw:document.documentElement.scrollWidth,fields:f.length,hmin:Math.min(...f.map(H)),fs:[...new Set(f.map(e=>getComputedStyle(e).fontSize))],file:file?H(file):null,chk:lab,sub:sb?H(sb):null,
cols:getComputedStyle(C.querySelector('.form-row')||C).gridTemplateColumns.split(' ').length,detOpen:!!det,detCols:det?getComputedStyle(det.querySelector('.job-details-grid')).gridTemplateColumns.split(' ').length:null,over,
banner:getComputedStyle(document.querySelector('.final-banner')).paddingTop}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/rejoindre-equipe.html');pg.wait_for_timeout(300)
        t=pg.locator('.job-row button[aria-expanded]').first
        if t.count(): t.click();pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    b.close()
