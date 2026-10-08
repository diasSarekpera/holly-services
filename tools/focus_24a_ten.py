import os,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
T=[('index.html',1280,'.navbar__link'),('index.html',390,'.navbar__hamburger'),('index.html',1280,'.btn--primary'),('index.html',1280,'.footer__nav-link'),('index.html',1280,'.footer__nl-input|parent'),
('pages/rapport-consultations-dassa.html',1280,'[data-tab]'),('pages/devenir-benevole.html',1280,'input.benevolat-input'),('pages/actualites.html',1280,'.actualites-toolbar__search input|parent'),
('pages/a-propos.html',1280,'.contact-form__input'),('pages/mentions-legales.html',1280,'.legal-toc__list a'),('index.html',1280,'.back-to-top'),('index.html',1280,'.skip-link')]
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for pg,w,sel in T:
    p=b.new_page(viewport={'width':w,'height':900});p.goto(f'http://127.0.0.1:{s.server_address[1]}/{pg}');p.add_style_tag(content='*,*::before,*::after{transition:none!important}')
    p.evaluate("window.scrollTo(0,300)");p.wait_for_timeout(150);p.keyboard.press('Tab')
    css,_,par=sel.partition('|')
    r=p.evaluate("""([s,par])=>{let e=[...document.querySelectorAll(s)].find(x=>x.getBoundingClientRect().width>0);if(!e)return 'ABSENT';e.focus({focusVisible:true});const t=par?e.parentElement:e;const c=getComputedStyle(t);return [e.matches(':focus-visible'),c.outlineStyle,c.outlineWidth,c.outlineColor,c.outlineOffset].join(' ')}""",[css,par])
    print(w,pg.split('/')[-1][:12].ljust(12),sel.ljust(34),r);p.close()
