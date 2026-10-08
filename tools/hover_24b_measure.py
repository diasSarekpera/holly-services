import os,sys,json,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
SNAP='''e=>{const c=getComputedStyle(e);return [c.color,c.backgroundColor,c.borderTopColor,c.boxShadow.slice(0,45),c.opacity,c.paddingLeft,c.textDecorationLine,c.visibility].join('|')}'''
T=[('bouton primaire','index.html',1280,'.btn--primary'),('bouton ghost','index.html',1280,'.btn--ghost,.btn--ghost-light'),('carte','pages/actions.html',1280,'main [class*=card]:not(button)'),
('lien header','index.html',1280,'.navbar__link:not(button)'),('dropdown (menu deroulant)','index.html',1280,'.navbar__item--dropdown>button,.navbar__item--dropdown>a'),
('lien footer','index.html',1280,'.footer__nav-link'),('lien texte (fil d ariane / legal)','pages/mentions-legales.html',1280,'.footer__legal-link'),('menu mobile','index.html',390,'.mobile-menu__link:not(.mobile-menu__link--toggle)')]
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for name,pg,w,sel in T:
    p=b.new_page(viewport={'width':w,'height':900});p.goto(f'http://127.0.0.1:{s.server_address[1]}/{pg}');p.add_style_tag(content='*,*::before,*::after{transition:none!important}');p.wait_for_timeout(150)
    if w==390: p.click('.navbar__hamburger');p.wait_for_timeout(500)
    h=p.query_selector_all(sel);e=next((x for x in h if x.is_visible()),None)
    if not e: print(name.ljust(32),'ABSENT');p.close();continue
    e.scroll_into_view_if_needed();p.mouse.move(2,2);p.wait_for_timeout(100);a=e.evaluate(SNAP)
    extra0=p.evaluate("()=>{const d=document.querySelector('.navbar__dropdown');return d?getComputedStyle(d).visibility+getComputedStyle(d).opacity:''}")
    bb=e.bounding_box();p.mouse.move(bb['x']+bb['width']/2,bb['y']+bb['height']/2);p.wait_for_timeout(150);z=e.evaluate(SNAP)
    extra1=p.evaluate("()=>{const d=document.querySelector('.navbar__dropdown');return d?getComputedStyle(d).visibility+getComputedStyle(d).opacity:''}")
    print(name.ljust(32),'CHANGE' if (a!=z or extra0!=extra1) else 'identique','|',(extra0+'>'+extra1) if 'dropdown' in name else z[:60]);p.close()
