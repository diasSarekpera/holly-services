"""T13A : images locales cassees ? (Playwright, reseau externe coupe). Usage: img_13a_broken.py [racine]"""
import sys,glob,os,functools,http.server,socketserver,threading
from playwright.sync_api import sync_playwright
root=sys.argv[1] if len(sys.argv)>1 else '.'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory=root)); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
pages=sorted(glob.glob(root+'/*.html')+glob.glob(root+'/pages/*.html')); bad=0; n=0
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':900}); pg.route('**/*',lambda r:r.continue_() if '127.0.0.1' in r.request.url else r.abort())
    for p in pages:
        pg.goto(f'http://127.0.0.1:{port}/'+os.path.relpath(p,root),wait_until='load')
        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(300)
        r=pg.evaluate("[...document.images].filter(i=>!i.src.includes('unsplash')).map(i=>[i.getAttribute('src'),i.complete&&i.naturalWidth>0])")
        n+=len(r); f=[x[0] for x in r if not x[1]]; bad+=len(f)
        if f: print(os.path.basename(p),f[:3])
    b.close()
print('images locales testees',n,'cassees',bad)
