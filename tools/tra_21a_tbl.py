import os,json,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
JS='''()=>{const S=[...document.querySelectorAll('main > section')].slice(0,3);const q=x=>S.flatMap(s=>[...s.querySelectorAll(x)]);
const t=q('table')[0],bc=q('.bar-chart,[class*=bar-chart]')[0];const w=t&&t.parentElement;
const o=e=>e?{w:Math.round(e.getBoundingClientRect().width),sw:e.scrollWidth,ox:getComputedStyle(e).overflowX}:null;
return {tables:q('table').length,tbl:o(t),wrap:o(w),wrapTab:w&&w.getAttribute('tabindex'),cap:t&&!!t.querySelector('caption'),th:t&&[...t.querySelectorAll('th')].filter(h=>h.hasAttribute('scope')).length+'/'+t.querySelectorAll('th').length,
 bars:bc?{w:Math.round(bc.getBoundingClientRect().width),sw:bc.scrollWidth,role:bc.getAttribute('role'),aria:bc.getAttribute('aria-label')?1:0,txtMin:Math.min(...[...bc.querySelectorAll('*')].filter(e=>e.children.length==0&&e.textContent.trim()).map(e=>parseFloat(getComputedStyle(e).fontSize)))}:null,
 tapMin:Math.min(...q('a,button').map(e=>Math.round(e.getBoundingClientRect().height)))}}'''
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for w in [320,768,1280]:
    p=b.new_page(viewport={'width':w,'height':900});p.goto(f'http://127.0.0.1:{s.server_address[1]}/pages/transparence-rapports.html');p.wait_for_timeout(150)
    print(w,json.dumps(p.evaluate(JS)));p.close()
