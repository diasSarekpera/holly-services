"""T12B : mesure hero accueil (styles calcules) aux 8 largeurs. Usage: hero_12b_measure.py [racine]"""
import sys,functools,http.server,socketserver,threading,json
from playwright.sync_api import sync_playwright
root=sys.argv[1] if len(sys.argv)>1 else '.'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory=root)); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
VP=[(320,568),(360,740),(390,844),(768,1024),(1024,768),(1280,720),(1440,900),(1920,1080)]
JS='''()=>{const R=e=>e.getBoundingClientRect(),q=s=>document.querySelector(s),cs=e=>getComputedStyle(e);
const h=q('.hero'),nav=q('.navbar'),z=q('.hero__text-zone'),b=q('.hero__badge'),t=q('.hero__title'),s=q('.hero__subtitle'),c=q('.hero__ctas'),p=q('.hero__proof');
const btn=[...c.children].map(e=>Math.round(R(e).height)+'x'+Math.round(R(e).width));
const bl=b?[...b.children].filter(e=>cs(e).display!=='none').length:0;
const lh=parseFloat(cs(b).lineHeight)||16;
return {H:Math.round(R(h).height),vh:innerHeight,navB:Math.round(R(nav).bottom),zTop:Math.round(R(z).top),zBot:Math.round(R(z).bottom),
badge:cs(b).display,bW:Math.round(R(b).width),bH:Math.round(R(b).height),bOver:b.scrollWidth>b.clientWidth+1||R(b).right>innerWidth,key:cs(b.querySelector('.hero__badge-key')).display,
fs:cs(t).fontSize,sub:cs(s).fontSize,btn,gapC:Math.round(R(c).top-R(s).bottom),proofB:Math.round(R(p).bottom),
hs:document.documentElement.scrollWidth-innerWidth,zOver:R(z).right>innerWidth||R(z).left<0}}'''
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w,h in VP:
        pg=b.new_page(viewport={'width':w,'height':h}); pg.route('**/*',lambda r:r.continue_() if '127.0.0.1' in r.request.url else r.abort())
        pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load'); pg.wait_for_timeout(1300)
        print(w,h,json.dumps(pg.evaluate(JS))); pg.close()
    b.close()
