"""T10H : contraste carte/fond de section (rapport de luminance) pour toutes les classes du bloc T10, toutes pages. Usage: cards_10h_contrast.py [seuil]"""
import functools,http.server,socketserver,threading,glob,re,sys
from playwright.sync_api import sync_playwright
TH=float(sys.argv[1]) if len(sys.argv)>1 else 1.08
s=open('styles/home.css',encoding='utf8').read(); i=s.find('/* ===== Cartes (T10)'); j=s.find('/* ===== fin Cartes (T10)')
CL=sorted(set(re.findall(r'\.([\w-]+)(?::hover)?[,{]',s[i:j])))
JS='''(cls)=>{const L=c=>{const m=c.match(/[\\d.]+/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2])};
const out=[];for(const e of document.querySelectorAll('.'+cls)){const r=e.getBoundingClientRect();if(!r.width||!r.height)continue;const c=getComputedStyle(e).backgroundColor;let a=e.parentElement,bg='rgba(0, 0, 0, 0)';while(a){bg=getComputedStyle(a).backgroundColor;if(!/rgba\\(.*, 0\\)$/.test(bg))break;a=a.parentElement}
if(/rgba\\(.*, 0\\)$/.test(bg))bg='rgb(255, 255, 255)';const l1=L(c),l2=L(bg);out.push([c,bg,(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)]);break}return out}'''
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory='.')); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
pages=['index.html','404.html']+sorted(glob.glob('pages/*.html'))
bad=0;n=0
with sync_playwright() as pw:
    b=pw.chromium.launch(); page=b.new_page(viewport={'width':1280,'height':900})
    for pg in pages:
        page.goto(f'http://127.0.0.1:{port}/{pg}',wait_until='load')
        for c in CL:
            for cc,bg,r in page.evaluate(JS,c):
                n+=1; ok=r>=TH; bad+=not ok
                if not ok or '-v' in sys.argv: print(('OK ' if ok else 'BAD'),pg[-34:],c,cc[4:-1],'on',bg[4:-1],round(r,3))
    b.close()
print('cartes mesurees',n,'sous seuil',TH,':',bad)
