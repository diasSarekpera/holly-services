import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const r=e=>e?Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height):null;
const pg=document.querySelector('.actualites-pagination');
return {sw:document.documentElement.scrollWidth,page:[...document.querySelectorAll('.actualites-page')].map(r),pagW:r(pg),pagMt:pg&&getComputedStyle(pg).marginTop,
cols:getComputedStyle(document.querySelector('.actualites-grid')).gridTemplateColumns.split(' ').length,
nlCols:getComputedStyle(document.querySelector('.actualites-nl__grid')).gridTemplateColumns.split(' ').length,
nlIn:[...document.querySelectorAll('.actualites-nl input:not([type=checkbox]):not([type=hidden])')].map(r),
chk:[...document.querySelectorAll('.actualites-nl label')].map(r).slice(0,4)}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/actualites.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    b.close()
