"""T11D : mesure mise en page formulaires/recherche/filtres. Usage: forms_11d_measure.py [racine] [widths]"""
import sys,functools,http.server,socketserver,threading,json
from playwright.sync_api import sync_playwright
root=sys.argv[1] if len(sys.argv)>1 else '.'
W=[int(x) for x in (sys.argv[2] if len(sys.argv)>2 else '320,375,767,768,1024,1280').split(',')]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory=root)); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
PAGES=['pages/partager-temoignage.html','pages/transparence-rapports.html','pages/actualites.html','index.html','pages/rejoindre-equipe.html']
JS='''()=>{const out=[];const R=e=>e.getBoundingClientRect();
const sel='.footer__nl-form,.actualites-nl__form,.transparence-form__form,main form[data-form],.actualites-toolbar,.docs-toolbar,[class*=filter]:not(button):not(.actualites-filter):not(.actualites-toolbar__filters)';
const seen=new Set();
document.querySelectorAll(sel).forEach(c=>{if(seen.has(c)||R(c).width===0)return;seen.add(c);
 const cr=R(c);const ctl=[...c.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]),select,textarea,button,.actualites-filter,.docs-filter,[role=tab],.actualites-nl__interests label')].filter(e=>R(e).width>0&&!e.closest('.form__hp'));
 const hs=ctl.filter(e=>R(e).height<43.5&&e.tagName!=='TEXTAREA').map(e=>(e.className||e.tagName).toString().slice(0,28)+':'+Math.round(R(e).height));
 const over=ctl.filter(e=>R(e).right>cr.right+1||R(e).left<cr.left-1).length;
 const sub=ctl.find(e=>e.type==='submit'||e.tagName==='BUTTON'&&c.matches('form,form *'));
 const tops=[...new Set(ctl.map(e=>Math.round(R(e).top)))].length;
 out.push({c:(c.className||c.tagName).toString().slice(0,34),w:Math.round(cr.width),n:ctl.length,rows:tops,short:hs.slice(0,4),over,sub:sub?Math.round(R(sub).width):null});});
out.push({hscroll:document.documentElement.scrollWidth-document.documentElement.clientWidth});return out}'''
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for pg in PAGES:
        for w in W:
            p=b.new_page(viewport={'width':w,'height':900}); p.goto(f'http://127.0.0.1:{port}/{pg}',wait_until='load'); p.wait_for_timeout(150)
            for r in p.evaluate(JS): print(pg[6:22] if pg!='index.html' else 'index',w,json.dumps(r,ensure_ascii=False))
            p.close()
    b.close()
