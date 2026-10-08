import sys,os,json,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R)
H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
JS='''()=>{const q=s=>document.querySelector(s),g=(e,p)=>e?getComputedStyle(e)[p]:null;
const c=q('.legal-content'),h1=q('main h1,header h1'),h2=q('.legal-section__title'),p=q('.legal-section p'),li=q('.legal-section li'),
 t=q('.legal-toc__list a'),m=q('.legal-meta'),b=q('.legal-box');
const hs=[...document.querySelectorAll('main h1,main h2,main h3,main h4,header h1')].map(e=>e.tagName[1]).join('');
const todo=[...document.querySelectorAll('.legal-content *')].filter(e=>e.children.length==0&&/À COMPLÉTER/.test(e.textContent)).length;
const todoSt=(()=>{const e=[...document.querySelectorAll('.legal-content *')].find(e=>e.children.length==0&&/À COMPLÉTER/.test(e.textContent));return e?e.tagName+'.'+e.className+' '+g(e,'color')+' '+g(e,'fontSize'):null})();
return {w:c&&Math.round(c.getBoundingClientRect().width),pw:p&&Math.round(p.getBoundingClientRect().width),pfs:g(p,'fontSize'),
 h1:g(h1,'fontSize'),h2:g(h2,'fontSize'),h2h:h2&&Math.round(h2.getBoundingClientRect().height),tocH:t&&Math.round(t.getBoundingClientRect().height),
 liMl:g(li,'marginLeft'),liLs:g(q('.legal-section ul'),'listStyleType'),liLh:g(li,'lineHeight'),hs,todo,todoSt,hsc:document.documentElement.scrollWidth-innerWidth,
 anch:[...document.querySelectorAll('.legal-toc__list a')].filter(a=>!document.querySelector(a.getAttribute('href'))).length,
 sm:g(q('.legal-section'),'scrollMarginTop')}}'''
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for pg in ['mentions-legales','conditions-utilisation','politique-confidentialite']:
    for w in [320,768,1280,1920]:
      pa=b.new_page(viewport={'width':w,'height':900});pa.goto(f'http://127.0.0.1:{s.server_address[1]}/pages/{pg}.html');pa.wait_for_timeout(200)
      r=pa.evaluate(JS);print(pg[:6],w,json.dumps(r,ensure_ascii=False));pa.close()
