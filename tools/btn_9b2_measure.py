import sys,json
from playwright.sync_api import sync_playwright
out=sys.argv[1]
P=['campagne-proteger-500-enfants','devenir-benevole','partager-temoignage','a-propos','maintenance','devenir-partenaire','actualites']
JS="""()=>{const r=[];document.querySelectorAll('.btn,[class*="__btn"],[class*="__cta"],[class*="__button"]').forEach(e=>{
if(e.tagName!=='A'&&e.tagName!=='BUTTON')return;const b=e.getBoundingClientRect();if(!b.width&&!b.height)return;
const c=getComputedStyle(e);const lh=parseFloat(c.lineHeight)||parseFloat(c.fontSize)*1.2;
const inner=b.height-parseFloat(c.paddingTop)-parseFloat(c.paddingBottom)-2*parseFloat(c.borderTopWidth);
r.push({cls:[...e.classList].join(' ').slice(0,60),txt:e.textContent.trim().slice(0,22),h:+b.height.toFixed(1),w:+b.width.toFixed(1),
right:+b.right.toFixed(1),wrap:inner>lh*1.6,ovf:e.scrollWidth>e.clientWidth+1,rad:c.borderRadius,fw:c.fontWeight,ws:c.whiteSpace})});
return {btns:r,docw:document.documentElement.scrollWidth,vw:innerWidth}}"""
res={};bad=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (360,768,1280):
        pg=b.new_page(viewport={'width':w,'height':900})
        for n in P:
            pg.goto(f'http://localhost:8765/pages/{n}.html');pg.wait_for_timeout(300)
            v=pg.evaluate(JS);res[f'{n}@{w}']=v
            if v['docw']>v['vw']+1: bad+=1;print('HSCROLL',n,w,v['docw'])
            for x in v['btns']:
                if x['wrap'] or x['ovf'] or x['right']>w+1 or x['h']<43.5: bad+=1;print('BAD',n,w,x['cls'][:40],x['txt'],x['h'],x['w'],'wrap' if x['wrap'] else '')
    b.close()
json.dump(res,open(out,'w'))
print('total btn',sum(len(v['btns']) for v in res.values()),'problemes',bad)
