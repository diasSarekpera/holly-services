"""T3B : application des breakpoints. Usage: bp_3b.py test|apply|verify
 test   : pour chaque rapprochement et portee (shared/local/hero), copie temporaire + diff des styles calcules (aux largeurs autour du seuil) ; resultat /tmp/bp3b.json
 apply  : applique sur styles/ uniquement les (rapprochement, portee, page) a 0 difference
 verify : compare styles/ courant a l'original (/tmp/bp3b_orig) a 30 largeurs"""
import re,sys,os,glob,json,shutil,collections,functools,http.server,socketserver,threading
from playwright.sync_api import sync_playwright
ROOT=os.getcwd(); ORIG='/tmp/bp3b_orig'; TMP='/tmp/bp3b_tmp'; RES='/tmp/bp3b.json'
M={'M1':{('max',480):479},'M2':{('max',768):767},'M3':{('max',1024):1023},'M4':{('max',375):479},'M5':{('max',359):479},'M6':{('max',430):479},
'M7':{('max',560):479},'M8':{('max',600):767},'M9':{('max',700):767},'M10':{('max',860):767},'M11':{('max',639):767,('min',640):768},
'M12':{('max',640):767},'M13':{('max',900):1023,('max',899):1023,('min',901):1024},'M14':{('max',900):767,('max',899):767,('min',901):768},
'M15':{('max',1100):1023,('max',1099):1023},'M16':{('max',1100):1279,('max',1099):1279},'M17':{('min',520):480}}
COND=re.compile(r'(max|min)-width\s*:\s*(\d+)px')
def blocks(s):
    out=[]
    for m in re.finditer(r'@media([^{]*)\{',s):
        i=m.end(); d=1
        while d and i<len(s): d+=(s[i]=='{')-(s[i]=='}'); i+=1
        out.append((m.start(1),m.end(1)-1,re.sub(r'\s+','',s[m.start():i])))
    return out
def header_range(pre): return 'min-width:1024px' in pre.replace(' ','') and 'max-width' in pre
def xform(s,mp,pick):
    for a,b,norm in sorted(blocks(s),reverse=True):
        pre=s[a:b]
        if header_range(pre) or not pick(norm): continue
        new=COND.sub(lambda m:f'{m.group(1)}-width:{mp[(m.group(1),int(m.group(2)))]}px' if (m.group(1),int(m.group(2))) in mp else m.group(0),pre)
        s=s[:a]+new+s[b:]
    return s
def sheets(root): return sorted(glob.glob(root+'/styles/*.css'))
def shared_set(root):
    c=collections.Counter()
    for f in sheets(root):
        for n in {x[2] for x in blocks(open(f,encoding='utf8').read())}: c[n]+=1
    return {n for n,k in c.items() if k>=10}
def page_sheets(root):
    d={}
    for p in sorted(glob.glob(root+'/*.html')+glob.glob(root+'/pages/*.html')):
        d[os.path.relpath(p,root)]=[os.path.basename(h) for h in re.findall(r'href="[^"]*styles/([^"]+\.css)"',open(p,encoding='utf8').read())]
    return d
def build(mp,scope,dst):
    """copie ORIG->dst, transforme ; renvoie fichiers modifies"""
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(ORIG,dst); sh=shared_set(ORIG); ch=[]
    for f in sheets(dst):
        n=os.path.basename(f); s=open(f,encoding='utf8').read()
        if scope=='shared': pick=lambda x:x in sh
        elif scope=='hero': pick=(lambda x:x not in sh) if n=='hero-photo.css' else (lambda x:False)
        else: pick=(lambda x:x not in sh) if n!='hero-photo.css' else (lambda x:False)
        t=xform(s,mp,pick)
        if t!=s: open(f,'w',encoding='utf8').write(t); ch.append(n)
    return ch
def serve(root):
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(s,*a): pass
        def end_headers(s): s.send_header('Cache-Control','no-store'); super().end_headers()
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory=root)); srv.daemon_threads=True
    threading.Thread(target=srv.serve_forever,daemon=True).start(); return srv.server_address[1]
JS='''()=>{const P=['display','position','flexDirection','flexWrap','gridTemplateColumns','gap','fontSize','paddingTop','paddingLeft','marginTop','textAlign','visibility','order'];
return [...document.querySelectorAll('body *')].map(e=>{const c=getComputedStyle(e),r=e.getBoundingClientRect();return P.map(p=>c[p]).join('|')+'|'+[r.x,r.y,r.width,r.height].map(Math.round).join(',')})}'''
def snap(pg,port,page,widths,cache=None,tag=''):
    out={}
    pg.goto(f'http://127.0.0.1:{port}/{page}',wait_until='load'); pg.add_style_tag(content='*,*::before,*::after{animation:none!important;transition:none!important}')
    for w in widths:
        k=(tag,page,w)
        if cache is not None and k in cache: out[w]=cache[k]; continue
        pg.set_viewport_size({'width':w,'height':900}); pg.wait_for_timeout(60); out[w]=pg.evaluate(JS)
        if cache is not None: cache[k]=out[w]
    return out
def widths_for(mp):
    v=[x for k,t in mp.items() for x in (k[1],t)]; lo,hi=min(v),max(v); return sorted({lo,lo+1,lo+(hi-lo)//4,(lo+hi)//2,lo+3*(hi-lo)//4,hi,hi+1})
def diff(a,b):
    return {w:sum(1 for x,y in zip(a[w],b[w]) if x!=y)+abs(len(a[w])-len(b[w])) for w in a if a[w]!=b[w]}
def browser(pw):
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':900}); pg.route('**/*',lambda r:r.continue_() if '127.0.0.1' in r.request.url else r.abort()); return b,pg
mode=sys.argv[1]
if mode=='test':
    if os.path.exists(ORIG): shutil.rmtree(ORIG)
    shutil.copytree(ROOT,ORIG,ignore=shutil.ignore_patterns('*.zip','.git')); po=serve(ORIG); pages=list(page_sheets(ORIG)); res={}; cache={}
    with sync_playwright() as pw:
        b,pg=browser(pw)
        for name,mp in M.items():
            W=widths_for(mp)
            for scope in ('shared','local','hero'):
                ch=build(mp,scope,TMP)
                if not ch: continue
                pt=serve(TMP); bad={}
                for page in pages:
                    d=diff(snap(pg,po,page,W,cache,'o'),snap(pg,pt,page,W))
                    if name in ('M1','M2','M3'): d={w:c for w,c in d.items() if w!=list(mp)[0][1]}  # decalage de 1px : seule la largeur exacte de l'ancien seuil change
                    if d: bad[page]=d
                res[f'{name}:{scope}']={'files':ch,'bad':{p:sum(d.values()) for p,d in bad.items()},'ex':list(bad.items())[:1]}
                print(name,scope,'fichiers',len(ch),'pages_diff',len(bad),flush=True)
        b.close()
    json.dump(res,open(RES,'w'),indent=0)
elif mode=='apply':
    res=json.load(open(RES)); sh=shared_set(ROOT); ps=page_sheets(ROOT); use=collections.defaultdict(set)
    for p,l in ps.items():
        for s in l: use[s].add(p)
    log=collections.Counter()
    for name,mp in M.items():
        for scope in ('shared','local','hero'):
            r=res.get(f'{name}:{scope}')
            if not r: continue
            bad=set(r['bad'])
            for f in sheets(ROOT):
                n=os.path.basename(f)
                if n not in r['files']: continue
                if scope=='shared': ok=not bad
                elif scope=='hero': ok=not bad
                else: ok=not (use[n]&bad)
                if not ok: continue
                s=open(f,encoding='utf8').read()
                if scope=='shared': pick=lambda x:x in sh
                elif scope=='hero': pick=lambda x:x not in sh
                else: pick=lambda x:x not in sh
                t=xform(s,mp,pick)
                if t!=s: open(f,'w',encoding='utf8').write(t); log[f'{name}:{scope}']+=1
    print(dict(log))
elif mode=='verify':
    W=[320,360,375,376,390,430,479,481,520,560,600,639,640,700,767,769,860,900,901,1023,1025,1099,1100,1199,1279,1280,1439,1440,1920]
    po=serve(ORIG); pn=serve(ROOT); pages=list(page_sheets(ROOT)); tot=0
    with sync_playwright() as pw:
        b,pg=browser(pw)
        for page in pages:
            d=diff(snap(pg,po,page,W),snap(pg,pn,page,W))
            if d: tot+=1; print('DIFF',page,d)
        b.close()
    print('pages avec difference:',tot,'/',len(pages))
