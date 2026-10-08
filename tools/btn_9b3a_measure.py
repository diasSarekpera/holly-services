import re,glob,hashlib,json,os
from playwright.sync_api import sync_playwright
pages=sorted(glob.glob('*.html')+glob.glob('pages/*.html'))
def hdr(f):
    s=open(f,encoding='utf8').read()
    out=[]
    for tag in ('header','div'):
        pass
    m=re.search(r'<header.*?</header>',s,re.S); h=m.group(0) if m else ''
    mm=re.search(r'<[^>]*class="mobile-menu[ "].*?(?=<main|<footer)',s,re.S); h+=mm.group(0) if mm else ''
    h=re.sub(r'(href|src)="(\.\./|\./)?','\\1="',h); h=re.sub(r'\s*aria-current="[^"]*"','',h); h=re.sub(r'\s+',' ',h)
    h=re.sub(r'(href|src)="(?:pages/)?','\\1="',h)
    return hashlib.md5(h.encode()).hexdigest()
print(len(pages),'pages; header hashes:',{hdr(f) for f in pages}.__len__())
def nav(f):
    s=open(f,encoding='utf8').read()
    return hashlib.md5(''.join(sorted(re.findall(r'[^{}]*(?:navbar__cta|mobile-menu__cta)[^{}]*\{[^{}]*\}',s))).encode()).hexdigest()
print('css sheets:',len(glob.glob('styles/*.css')),'cta hashes:',{nav(f) for f in glob.glob('styles/*.css') if 'navbar__cta' in open(f).read()}.__len__())
base='http://localhost:8765/'
bad=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (360,768,1024,1366,1920):
        pg=b.new_page(viewport={'width':w,'height':900})
        res=set()
        for f in pages:
            pg.goto(base+f); pg.wait_for_timeout(150)
            r=pg.evaluate('''()=>{const n=document.querySelector('.navbar');const c=document.querySelector('.navbar__cta');const m=document.querySelector('.mobile-menu__cta');
            const cs=c&&getComputedStyle(c);const rc=c&&c.getBoundingClientRect();if(!c||!m)return {missing:(c?'':'navbar__cta ')+(m?'':'mobile-menu__cta'),file:location.pathname.split('/').pop()};if(!m||!c)return {missing:(c?'':'navbar__cta ')+(m?'':'mobile-menu__cta'),file:location.pathname.split('/').pop()};const rm=m.getBoundingClientRect();
            const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.2;
            return {h:Math.round(n.getBoundingClientRect().height),cta:cs.display=='none'?'hidden':Math.round(rc.height)+'/'+(rc.height<=lh+parseFloat(cs.paddingTop)*2+parseFloat(cs.borderTopWidth)*2+2?'1l':'WRAP'),
            ctaOver:rc.right>innerWidth+1,mm:Math.round(rm.height),mmFlex:getComputedStyle(m).display,over:document.documentElement.scrollWidth>innerWidth}}''')
            res.add(json.dumps(r,sort_keys=True)+('' if r.get('missing') or (r['h'] in(100,80,77,101) and not r['over']) else ' <-'+f))
        print(w,sorted(res))
    b.close()
