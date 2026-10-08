import os,json,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
JS='''()=>{const S=[...document.querySelectorAll('main > section')].slice(0,3),g=(e,p)=>getComputedStyle(e)[p];
const cards=S.flatMap(s=>[...s.querySelectorAll('[class*=card],[class*=tile]')]).filter(e=>e.getBoundingClientRect().width>0);
const c=cards[0];const bt=S.flatMap(s=>[...s.querySelectorAll('a.btn,button')]);
return {hsc:document.documentElement.scrollWidth-innerWidth,pad:S.map(s=>g(s,'paddingTop')).join('/'),h2:S.map(s=>{const h=s.querySelector('h2');return h?g(h,'fontSize'):'-'}).join('/'),
 nCards:cards.length,card:c?[g(c,'borderTopWidth'),g(c,'borderTopColor'),g(c,'boxShadow').slice(0,40),g(c,'transform')].join(' '):null,
 btnMin:bt.length?Math.min(...bt.map(b=>Math.round(b.getBoundingClientRect().height))):null,
 imgs:S.flatMap(s=>[...s.querySelectorAll('img')]).filter(i=>i.getBoundingClientRect().right>innerWidth+1).length,
 over:S.flatMap(s=>[...s.querySelectorAll('*')]).filter(e=>e.getBoundingClientRect().right>innerWidth+1&&g(e,'position')!='fixed').length,
 tabs:document.querySelectorAll('[role=tab],[data-tab]').length}}'''
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for w in [320,390,768,1280,1920]:
    p=b.new_page(viewport={'width':w,'height':900});p.goto(f'http://127.0.0.1:{s.server_address[1]}/pages/transparence-rapports.html');p.wait_for_timeout(150)
    print(w,json.dumps(p.evaluate(JS)));p.close()
