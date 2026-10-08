import glob, sys
from playwright.sync_api import sync_playwright
pages = sorted(glob.glob('*.html') + glob.glob('pages/*.html'))
SEL = ('.btn,.actions-filter__btn,.filter-btn,.article-share__btn,.campagne-share__btn,.soutenir__way-btn,'
       '.team-card__social-btn,.camp-card__cta-inline,.camp-card__cta-main,.hero__cta-primary,.hero__cta-secondary,'
       '.navbar__cta,.mobile-menu__cta')
JS = '''(sel)=>{const out=[];document.querySelectorAll(sel).forEach(e=>{const r=e.getBoundingClientRect();
 if(!r.width||!r.height)return;const c=getComputedStyle(e);
 if(c.visibility==='hidden')return;
 const rg=document.createRange();rg.selectNodeContents(e);const rects=[...rg.getClientRects()].filter(x=>x.width>0&&!(e.querySelector('svg,i')&&x.width<20&&0));
 const tops=new Set();const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n,lines=new Set();
 while(n=walker.nextNode()){if(!n.textContent.trim())continue;{const pr=n.parentElement.getBoundingClientRect();if(pr.width<=2||pr.height<=2)continue}const q=document.createRange();q.selectNodeContents(n);[...q.getClientRects()].forEach(x=>lines.add(Math.round(x.top/4)))}
 const sib=e.previousElementSibling&&e.previousElementSibling.matches('.btn')?1:0;
 out.push({cls:e.className.slice(0,50),txt:e.textContent.trim().slice(0,22),w:r.width,h:r.height,lines:lines.size,l:r.left,r:r.right,sw:e.scrollWidth,cw:e.clientWidth,sib:sib,
  sibGap:sib?Math.round(r.top-e.previousElementSibling.getBoundingClientRect().bottom):null,sibW:sib?Math.round(r.width):null,pw:e.parentElement.getBoundingClientRect().width,
  sm:e.classList.contains('btn--sm')})});
 return {b:out,ox:document.documentElement.scrollWidth-document.documentElement.clientWidth}}'''
bad=[];n=0;stack=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (360,768,1280):
        ctx=b.new_context(viewport={'width':w,'height':900})
        for pg in pages:
            page=ctx.new_page();page.goto('http://localhost:8765/'+pg);page.wait_for_timeout(120)
            # reveal menus: mobile menu closed is display:none -> skipped
            r=page.evaluate(JS,SEL);page.close()
            if r['ox']>0: bad.append((w,pg,'overflowX',r['ox']))
            for x in r['b']:
                n+=1;t=(w,pg,x['cls'][:34],x['txt'])
                minh=44 if (w<768 or not x['sm']) else 36
                if w>=768 and not x['sm']: minh=44
                if x['h']<minh-0.5: bad.append(t+('h',round(x['h'])))
                if x['lines']>1: bad.append(t+('lines',x['lines']))
                if x['l']<-0.5 or x['r']>w+0.5 or x['sw']>x['cw']+1: bad.append(t+('overflow',round(x['l']),round(x['r']),x['sw'],x['cw']))
                if w==360 and x['sib']: stack.append(t+(x['sibGap'],x['sibW'],round(x['pw'])))
        ctx.close()
    b.close()
print('mesures',n,'ecarts',len(bad))
for x in bad[:25]: print(x)
if '-s' in sys.argv:
    print('consecutifs 360:',len(stack),'non conformes:')
    for x in stack:
        if x[4]!=12 or abs(x[5]-x[6])>1: print(x)
