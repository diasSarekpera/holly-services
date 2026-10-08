import sys,glob,os,collections,json
from playwright.sync_api import sync_playwright
root=sys.argv[1]; res=collections.defaultdict(set); cnt=collections.Counter()
KEEP=('index','actualites','nos-missions','a-propos','campagne-proteger','devenir-benevole','equipe')
pages=[x for x in sorted(glob.glob(root+'/index.html')+glob.glob(root+'/pages/*.html')) if any(k in x for k in KEEP)]
SEL='.btn,[class*=card],.post,.mission,.team-card,.gal-item,.footer__social,.footer__support-item,.action-tile'
JS_HOVER="""(sel)=>{const out=[];const els=[...document.querySelectorAll(sel)].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0}).slice(0,7);return els.map((e,i)=>{e.setAttribute('data-m24',i);return i})}"""
JS_STATE="""(i)=>{const e=document.querySelector('[data-m24="'+i+'"]');const t=[e,...e.querySelectorAll('img,svg')].slice(0,4);return t.map(x=>{const r=x.getBoundingClientRect();return [x.tagName+'.'+(x.getAttribute('class')||'').split(' ')[0],Math.round(r.x*10)/10,Math.round(r.y*10)/10,Math.round(r.width*10)/10,getComputedStyle(x).transform]})}"""
JS_HID="""()=>[...document.querySelectorAll('body *')].filter(e=>{const c=getComputedStyle(e);if(c.opacity!=='0'||c.visibility==='hidden'||c.display==='none')return false;const r=e.getBoundingClientRect();if(r.width*r.height<400)return false;return !e.closest('.navbar__dropdown,.mobile-menu,[aria-hidden=true],[hidden],.sr-only,.visually-hidden,.skip-link')}).map(e=>e.tagName+'.'+(e.getAttribute('class')||'').split(' ')[0]).slice(0,5)"""
JS_ANIM="""()=>document.getAnimations().filter(a=>a.playState==='running'&&a.effect.getComputedTiming().iterations===Infinity).map(a=>a.animationName||a.transitionProperty||'?')"""
JS_TR="""()=>{let n=0;document.querySelectorAll('*').forEach(e=>{const d=getComputedStyle(e).transitionDuration.split(',').map(x=>parseFloat(x)*(x.includes('ms')?0.001:1));if(d.some(x=>x>0.0001))n++});return n}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for pg in pages:
        url='file://'+os.path.abspath(pg); name=os.path.relpath(pg,root)
        # survol (mouvement normal, desktop)
        c=b.new_context(viewport={'width':1280,'height':900}); pa=c.new_page(); pa.goto(url); pa.wait_for_timeout(700)
        ids=pa.evaluate(JS_HOVER,SEL)
        for i in ids:
            try:
                pa.mouse.move(0,0); pa.wait_for_timeout(60)
                el=pa.locator('[data-m24="%d"]'%i); el.scroll_into_view_if_needed(timeout=1000); pa.wait_for_timeout(100)
                a=pa.evaluate(JS_STATE,i); el.hover(timeout=1000); pa.wait_for_timeout(350); h=pa.evaluate(JS_STATE,i)
                for x,y in zip(a,h):
                    cnt['tested']+=1
                    if x[4]!=y[4] or abs(x[1]-y[1])>0.4 or abs(x[2]-y[2])>0.4: res['move'].add(x[0]+' '+x[4][:12]+'->'+y[4][:30])
            except Exception as e: cnt['err']+=1
        c.close()
        # mouvement réduit, JS actif
        c=b.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce'); pa=c.new_page(); pa.goto(url); pa.wait_for_timeout(800)
        for x in pa.evaluate(JS_ANIM): res['inf_reduced'].add(x)
        cnt['tr_reduced_max']=max(cnt['tr_reduced_max'],pa.evaluate(JS_TR))
        for x in pa.evaluate(JS_HID): res['hidden_reduced'].add(x)
        c.close()
        c=b.new_context(viewport={'width':1280,'height':900}); pa=c.new_page(); pa.goto(url); pa.wait_for_timeout(1300)
        for x in pa.evaluate(JS_HID): res['hidden_normal'].add(x)
        c.close()
    b.close()
print(root,dict(cnt))
for k,v in res.items(): print(k,len(v),sorted(v)[:8])
