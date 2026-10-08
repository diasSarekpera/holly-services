import os,sys,glob,json,collections,threading,functools,http.server,socketserver
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);H.log_message=lambda *a:None
s=socketserver.TCPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
JS='''()=>{const out=[];const sel='a[href],button,input:not([type=hidden]),select,textarea,summary,[tabindex]:not([tabindex="-1"]),[data-tab]';
const els=[...document.querySelectorAll(sel)].filter(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);return r.width>0&&r.height>0&&c.visibility!='hidden'&&!e.disabled&&!e.closest('.mobile-menu:not(.is-open)')});
const name=e=>e.tagName.toLowerCase()+(e.type&&e.tagName=='INPUT'?'['+e.type+']':'')+'.'+[...e.classList].slice(0,1).join('.');
const L=c=>{const m=c.match(/[\\d.]+/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2])};
const surf=e=>{let a=e.parentElement;while(a){const b=getComputedStyle(a).backgroundColor;const m=b.match(/[\\d.]+/g);if(m&&(m[3]===undefined||+m[3]>0.6))return b;a=a.parentElement}return 'rgb(255, 255, 255)'};
const seen=new Set();
for(const e of els){const k=name(e);if(seen.has(k))continue;seen.add(k);e.focus({focusVisible:true});
 const c=getComputedStyle(e);const has=c.outlineStyle!='none'&&parseFloat(c.outlineWidth)>0;
 const l1=has?L(c.outlineColor):0,l2=L(surf(e));const cr=has?((Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)):0;
 out.push({n:k,o:has?[c.outlineStyle,c.outlineWidth,c.outlineColor,c.outlineOffset].join(' '):'AUCUN',cr:Math.round(cr*10)/10});}
return out}'''
mode=sys.argv[1] if len(sys.argv)>1 else 'sig'
pages=['index.html','404.html']+sorted(glob.glob('pages/*.html'))
res=collections.defaultdict(set);low=collections.defaultdict(set)
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for w in [1280,390]:
    for pg in pages:
      p=b.new_page(viewport={'width':w,'height':900});p.goto(f'http://127.0.0.1:{s.server_address[1]}/{pg}');p.add_style_tag(content='*,*::before,*::after{transition:none!important}');p.wait_for_timeout(120);p.keyboard.press('Tab')
      for r in p.evaluate(JS):
        res[r['o']].add(r['n'])
        if r['o']=='AUCUN' or r['cr']<3: low[r['n']+' cr='+str(r['cr'])+' '+r['o'][:30]].add(pg.split('/')[-1])
      p.close()
for k,n in sorted(res.items(),key=lambda x:-len(x[1])): print(str(len(n)).rjust(3),k)
print('AUCUN ou contraste<3 :',len(low))
for k,v in list(low.items())[:16]: print('  ',k,len(v),sorted(v)[0])
