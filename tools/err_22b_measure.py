import os,json,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
JS='''()=>{const g=(e,p)=>getComputedStyle(e)[p],M=document.querySelector('main');
const inp=document.querySelector('.erreur404-search input,.erreur404-search__input-wrapper input');
const clr=document.querySelector('#js-clear-search');
const btns=[...M.querySelectorAll('a.btn,button,input,a[class*=link],a[class*=card]')].filter(e=>e.getBoundingClientRect().width>0).map(e=>Math.round(e.getBoundingClientRect().height));
const h1=M.querySelector('h1');
return {hsc:document.documentElement.scrollWidth-innerWidth,h1:h1&&g(h1,'fontSize'),minTap:btns.length?Math.min(...btns):null,
 inp:inp?[Math.round(inp.getBoundingClientRect().height),g(inp,'fontSize')].join('/'):null,clr:clr?Math.round(clr.getBoundingClientRect().width)+'x'+Math.round(clr.getBoundingClientRect().height):null,
 over:[...M.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+1&&g(e,'position')!='fixed').length,
 hdr:!!document.querySelector('.navbar'),ftr:!!document.querySelector('footer')}}'''
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for pg in ['404.html','pages/maintenance.html']:
    for w in [320,390,768,1280,1920]:
      p=b.new_page(viewport={'width':w,'height':900});p.goto(f'http://127.0.0.1:{s.server_address[1]}/{pg}');p.wait_for_timeout(200)
      print(pg[:5],w,json.dumps(p.evaluate(JS)));p.close()
