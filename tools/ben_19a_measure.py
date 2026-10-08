import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const H=s=>[...document.querySelectorAll(s)].map(e=>Math.round(e.getBoundingClientRect().height)).slice(0,3);
const g=(s,p)=>{const e=document.querySelector(s);return e?getComputedStyle(e)[p]:null};
return {sw:document.documentElement.scrollWidth,fCols:g('.benevolat-formats__grid','gridTemplateColumns').split(' ').length,mCols:g('.benevolat-missions__grid','gridTemplateColumns').split(' ').length,
padF:g('.benevolat-formats','paddingTop'),padM:g('.benevolat-missions','paddingTop'),filt:H('.benevolat-filter'),reset:H('.benevolat-filters__reset:not([hidden])'),btn:H('.benevolat-mission-card__btn'),mt:g('.benevolat-mission-card__title','fontSize')}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/devenir-benevole.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    f=pg.locator('.benevolat-filter').nth(1);f.hover();pg.wait_for_timeout(300);print('hover',pg.evaluate("e=>getComputedStyle(e).backgroundColor",f.element_handle()))
    b.close()
