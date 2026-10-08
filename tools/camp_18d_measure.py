import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const H=s=>[...document.querySelectorAll(s)].map(e=>{const r=e.getBoundingClientRect();return Math.round(r.width)+'x'+Math.round(r.height)}).slice(0,4);
const g=(s,p)=>{const e=document.querySelector(s);return e?getComputedStyle(e)[p]:null};
return {sw:document.documentElement.scrollWidth,cols:g('.campagne-layout','gridTemplateColumns').split(' ').length,don:g('.campagne-don','position'),
title:g('.campagne-section__title','fontSize'),secMb:g('.campagne-section','marginBottom'),layPad:g('.campagne-layout','paddingTop'),amount:g('.campagne-don__amount','fontSize'),
prog:H('.campagne-don__progress'),progBg:g('.campagne-don__progress','backgroundColor'),box:H('.campagne-choice__box'),share:H('.campagne-share__btn'),cta:H('.campagne-don__cta')}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/campagne-proteger-500-enfants.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    b.close()
