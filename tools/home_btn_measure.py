import sys,json
from playwright.sync_api import sync_playwright
out=sys.argv[1]
JS="""()=>{const r=[];const sel='a[class*="btn"],a[class*="cta"],a[class*="way-btn"],button[class*="btn"]';
document.querySelectorAll(sel).forEach(e=>{const b=e.getBoundingClientRect();if(!b.width&&!b.height)return;
if(e.closest('.navbar,.mobile-menu,.footer'))return;
const c=getComputedStyle(e);
// count text lines of label via range rects
let lines=0;const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);const tops=new Set();let n;
while(n=w.nextNode()){if(!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);for(const q of rg.getClientRects()){if(q.width>0)tops.add(Math.round(q.top/4))}}
r.push({cls:e.className,txt:e.textContent.trim().replace(/\\s+/g,' ').slice(0,22),w:+b.width.toFixed(0),h:+b.height.toFixed(0),right:+b.right.toFixed(0),lines:tops.size,
 ovf:e.scrollWidth>e.clientWidth+1,fs:c.fontSize,fw:c.fontWeight,rad:c.borderRadius,ws:c.whiteSpace,bw:c.borderTopWidth,bg:c.backgroundColor,bc:c.borderTopColor})});
return {btns:r,docw:document.documentElement.scrollWidth,vw:innerWidth}}"""
res={}
with sync_playwright() as p:
    br=p.chromium.launch()
    for w in (360,768,1280):
        pg=br.new_page(viewport={'width':w,'height':900})
        pg.goto('http://localhost:8765/index.html');pg.wait_for_timeout(400)
        # reveal lazy/animated sections
        pg.evaluate("document.querySelectorAll('*').forEach(e=>{})")
        res[w]=pg.evaluate(JS)
    br.close()
json.dump(res,open(out,'w'),indent=1)
bad=0
for w,v in res.items():
    print('== %s docw=%s'%(w,v['docw']), 'HSCROLL' if v['docw']>v['vw'] else '')
    for x in v['btns']:
        flag=[]
        if x['lines']>1: flag.append('2L')
        if x['right']>v['vw']+1 or x['ovf']: flag.append('OVF')
        if x['h']<44 and w<=768: flag.append('H<44')
        if flag: bad+=1
        print(' ',x['cls'][:44].ljust(44),x['txt'][:18].ljust(18),x['w'],x['h'],x['fs'],x['fw'],x['rad'],x['ws'],' '.join(flag))
print('PROBLEMS',bad)
