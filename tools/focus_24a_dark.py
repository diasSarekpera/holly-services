import os,glob,collections,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
JS='''()=>{const o=new Set();document.querySelectorAll('a[href],button,input,select,textarea,summary,[tabindex]').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;let a=e;while(a){const bg=getComputedStyle(a);let b=bg.backgroundColor;if(bg.backgroundImage!='none'&&/gradient|url/.test(bg.backgroundImage)&&!/rgba?\\(0, 0, 0, 0\\)/.test(b)===false){}
 if(b&&b!='rgba(0, 0, 0, 0)'){const m=b.match(/[\\d.]+/g);if(m[3]===undefined||+m[3]>0.5){if((m[0]*.3+m[1]*.59+m[2]*.11)<110)o.add((a.tagName.toLowerCase()+'.'+[...a.classList].slice(0,2).join('.')));break}if(+m[3]>0.5)break}a=a.parentElement}});return [...o]}'''
c=collections.defaultdict(set)
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for pg in ['index.html','404.html']+sorted(glob.glob('pages/*.html')):
    p=b.new_page(viewport={'width':1280,'height':900});p.goto(f'http://127.0.0.1:{s.server_address[1]}/{pg}');p.wait_for_timeout(100)
    for x in p.evaluate(JS): c[x].add(pg.split('/')[-1])
    p.close()
for k,v in sorted(c.items(),key=lambda x:-len(x[1])): print(str(len(v)).rjust(3),k)
