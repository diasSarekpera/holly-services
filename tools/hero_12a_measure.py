"""T12A : mesure des heros .hero-photo (styles calcules) + contraste titre sur voile (pire cas = photo blanche). Usage: hero_12a_measure.py [racine] [widths]"""
import sys,glob,os,re,functools,http.server,socketserver,threading,json
from playwright.sync_api import sync_playwright
root=sys.argv[1] if len(sys.argv)>1 else '.'
W=[int(x) for x in (sys.argv[2] if len(sys.argv)>2 else '360,768,1280').split(',')]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory=root)); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
pages=sorted(p for p in glob.glob(root+'/pages/*.html') if '<header class="hero-photo' in open(p,encoding='utf8').read())
def lum(c):
    c=[x/255 for x in c]; c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]; return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b):
    la,lb=lum(a),lum(b); return (max(la,lb)+0.05)/(min(la,lb)+0.05)
JS='''()=>{const h=document.querySelector('header.hero-photo');if(!h)return null;const q=s=>h.querySelector(s),cs=e=>getComputedStyle(e),R=e=>e.getBoundingClientRect();
const t=q('.hero-photo__title'),i=q('.hero-photo__inner'),b=q('.hero-photo__breadcrumb'),e=q('.eyebrow'),H=cs(h);
return {cls:h.className.replace('hero-photo ',''),h:Math.round(R(h).height),mh:H.minHeight,pt:H.paddingTop,pb:H.paddingBottom,ipt:cs(i).paddingTop,fs:cs(t).fontSize,fw:cs(t).fontWeight,lh:cs(t).lineHeight,tmax:cs(t).maxWidth,
bc:b?cs(b).fontSize:null,bcmb:b?cs(b).marginBottom:null,eb:e?cs(e).marginBottom:null,ebl:e?cs(e.querySelector('.eyebrow__label')).fontSize:null,
bg:H.backgroundImage.replace(/url\\([^)]*\\)/g,'url()').slice(0,160),bgc:H.backgroundColor,bgpos:H.backgroundPosition,bgsz:H.backgroundSize,
hs:document.documentElement.scrollWidth-document.documentElement.clientWidth,tw:Math.round(R(t).width),inner:Math.round(R(i).width)}}'''
rows={}
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for p in pages:
        for w in W:
            pg=b.new_page(viewport={'width':w,'height':900}); pg.route(re.compile(r'https?://(?!127).*'),lambda r:r.abort())
            pg.goto(f'http://127.0.0.1:{port}/pages/{os.path.basename(p)}',wait_until='load'); pg.wait_for_timeout(120)
            rows[(os.path.basename(p)[:22],w)]=pg.evaluate(JS); pg.close()
    b.close()
keys=['mh','pt','pb','ipt','fs','fw','lh','tmax','bc','bcmb','eb','ebl','bg','bgc','bgsz','hs']
for w in W:
    print('== width',w)
    for k in keys:
        vals={}
        for (p,ww),r in rows.items():
            if ww==w: vals.setdefault(str(r[k]),[]).append(p[:10])
        print(f' {k:5}',{v:(len(ps) if len(vals)==1 else ps[:3]+(['+%d'%(len(ps)-3)] if len(ps)>3 else [])) for v,ps in vals.items()} if len(vals)<=3 else f'{len(vals)} valeurs')
    print(' h   ',sorted({r['h'] for (p,ww),r in rows.items() if ww==w}))
# contraste : voile marine alpha a sur photo blanche, titre blanc
navy=(16,35,63)
for a in (0.62,0.70,0.75,0.80,0.84):
    bl=tuple(round(a*n+(1-a)*255) for n in navy); print(f'voile {a}: titre blanc/photo blanche = {cr((255,255,255),bl):.2f} ; fil ariane (secondary-soft)?')
