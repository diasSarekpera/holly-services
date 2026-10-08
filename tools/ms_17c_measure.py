import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>({sw:document.documentElement.scrollWidth,
sel:[...document.querySelectorAll('.mission-detail__selector-link')].map(e=>Math.round(e.getBoundingClientRect().height)),
h2:[...document.querySelectorAll('main h2')].map(e=>getComputedStyle(e).fontSize+'/'+getComputedStyle(e).marginBottom).slice(0,4),
fs:getComputedStyle(document.documentElement).getPropertyValue('--fs-h2').slice(0,40),
todo:[...document.querySelectorAll('.mission-detail__todo,.mission-detail__card--todo')].map(e=>Math.round(e.getBoundingClientRect().width)+'<='+Math.round(e.parentElement.getBoundingClientRect().width))})'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/mission-sante.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    b.close()
