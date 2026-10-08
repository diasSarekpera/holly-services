import os,json,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
T=[('pages/mentions-legales.html','propriete-intellectuelle'),('pages/mentions-legales.html','donnees-personnelles'),('pages/transparence-rapports.html','documents'),('pages/transparence-rapports.html','demande'),('index.html','soutenir'),('pages/politique-confidentialite.html','donnees-personnelles')]
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for w in [390,1280]:
    for pg,id_ in T:
      p=b.new_page(viewport={'width':w,'height':800});p.goto(f'http://127.0.0.1:{s.server_address[1]}/{pg}')
      if not p.query_selector('#'+id_): print(w,pg,id_,'ABSENT');p.close();continue
      p.evaluate(f"document.documentElement.style.scrollBehavior='auto';location.hash='{id_}'");p.wait_for_timeout(700)
      r=p.evaluate(f"()=>{{const t=document.getElementById('{id_}').getBoundingClientRect().top,n=document.querySelector('.navbar').getBoundingClientRect().bottom;return [Math.round(t),Math.round(n),Math.round(t-n)]}}")
      print(w,pg.split('/')[-1][:14],id_[:16],'top/navbar/gap',r,'OK' if r[2]>=0 else 'MASQUE');p.close()
