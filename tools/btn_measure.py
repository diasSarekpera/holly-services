import sys,json,glob,os
from playwright.sync_api import sync_playwright
out=sys.argv[1]; W=[360,1024,1920]
pages=['index.html','404.html']+sorted(glob.glob('pages/*.html'))
JS="""()=>{const r=[];document.querySelectorAll('.btn').forEach((e,i)=>{const b=e.getBoundingClientRect();if(!b.width&&!b.height)return;
const c=getComputedStyle(e);const cls=[...e.classList].filter(x=>x.startsWith('btn')).join(' ');
const lh=parseFloat(c.lineHeight)||parseFloat(c.fontSize)*1.2;
r.push({cls,txt:(e.textContent||'').trim().slice(0,24),w:+b.width.toFixed(1),h:+b.height.toFixed(1),right:+b.right.toFixed(1),
 hover:e.scrollWidth>e.clientWidth+1,wrap:(b.height-parseFloat(c.paddingTop)-parseFloat(c.paddingBottom)-2*parseFloat(c.borderTopWidth))>lh*1.6,
 minh:c.minHeight,pad:c.padding,rad:c.borderRadius,gap:c.gap,fs:c.fontSize,fw:c.fontWeight,ws:c.whiteSpace,bcol:c.borderColor})});
return {btns:r,docw:document.documentElement.scrollWidth,vw:innerWidth}}"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in W:
        pg=b.new_page(viewport={'width':w,'height':900})
        for f in pages:
            pg.goto('http://localhost:8765/'+f);pg.wait_for_timeout(250)
            res[f'{f}@{w}']=pg.evaluate(JS)
    b.close()
json.dump(res,open(out,'w'))
n=0;ov=0;wr=0;hz=0
import collections
cnt=collections.Counter()
for k,v in res.items():
    if v['docw']>v['vw']+1: hz+=1;print('H-SCROLL',k,v['docw'],v['vw'])
    for x in v['btns']:
        n+=1
        if x['right']>v['vw']+1 or x['hover']: ov+=1;print('OVERFLOW',k,x['cls'],x['txt'],x['right'])
        if x['wrap']: wr+=1;print('WRAP',k,x['cls'],x['txt'],x['h'],x['w'])
        if k.endswith('@1024'):
            for c in x['cls'].split(): cnt[c]+=1
print('mesures',n,'overflow',ov,'wrap',wr,'hscroll',hz);print(dict(cnt))
