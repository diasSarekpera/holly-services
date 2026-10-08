import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const H=s=>[...document.querySelectorAll(s)].map(e=>Math.round(e.getBoundingClientRect().height));
const t=document.querySelector('.actualites-featured__title');
return {sw:document.documentElement.scrollWidth,link:H('.actualites-link'),filt:H('.actualites-filter').slice(0,3),search:H('.actualites-toolbar__search'),title:t&&getComputedStyle(t).fontSize}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/actualites.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    f=pg.locator('.actualites-filter').nth(1);f.hover();pg.wait_for_timeout(400)
    print('hover filter',pg.evaluate("e=>{const c=getComputedStyle(e);return [c.backgroundColor,c.borderTopColor,c.color]}",f.element_handle()))
    f.click();pg.wait_for_timeout(200);print('after click pressed',f.get_attribute('aria-pressed'),'sw',pg.evaluate('document.documentElement.scrollWidth'))
    b.close()
