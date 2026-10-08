"""T10A : bloc partage « Cartes (T10) » (apply) et mesure par styles calcules (measure). Usage : cards_t10.py apply|measure|hash"""
import sys,glob,re,hashlib,os,threading,functools,http.server,socketserver,json
CARDS="why-card card-besoin erreur404-card mission-detail__card value-card team-card article-cta__card benevolat-format-card maintenance__contact-card action-card action-tile actualites-card article-card campagne-card campagne-don benevolat-mission-card job-sidebar temoignage-card rapport-result-card card-soutien reason-card form-card metier-card banner-card chiffre-card cta-card partner-logo-tile".split()
SEL=',\n'.join('.'+c for c in CARDS); HSEL=',\n'.join('.'+c+':hover' for c in CARDS)
START='/* ===== Cartes (T10) : recette unique ====='
BLOCK=(START+'\n   Fond blanc, bordure --clr-border-card, ombre --shadow-card, rayon --radius-card ; survol = bordure + ombre seulement, sans deplacement.\n   Liste = docs/CARTES-AUDIT.md (une classe de carte ajoutee ici dans les 21 feuilles, identique). */\n'
 +SEL+'{background:var(--clr-white);border:1px solid var(--clr-border-card);border-radius:var(--radius-card);box-shadow:var(--shadow-card);transition:border-color 0.2s ease,box-shadow 0.2s ease}\n'
 +HSEL+'{border-color:var(--clr-border-hover);box-shadow:var(--shadow-hover);transform:none}\n/* ===== fin Cartes (T10) ===== */')
END='/* ===== fin Cartes (T10) ===== */'
def blocks():
    r={}
    for f in sorted(glob.glob('styles/*.css')):
        s=open(f,encoding='utf8',newline='').read().replace('\r\n','\n')
        i=s.find(START); j=s.find(END)
        r[f]=s[i:j+len(END)] if i>=0 and j>i else None
    return r
def apply():
    for f in sorted(glob.glob('styles/*.css')):
        raw=open(f,encoding='utf8',newline='').read(); nl='\r\n' if '\r\n' in raw else '\n'
        s=raw.replace('\r\n','\n')
        if START in s: s=s[:s.index(START)].rstrip('\n')+'\n'
        s=s.rstrip('\n')+'\n\n'+BLOCK+'\n'
        open(f,'w',encoding='utf8',newline='').write(s.replace('\n',nl))
def hashes():
    b=blocks(); h={f:(hashlib.sha256(v.encode()).hexdigest()[:12] if v else None) for f,v in b.items()}
    u=set(h.values()); print(len(h),'feuilles,',len(u),'hash distinct(s):',u)
def measure():
    from playwright.sync_api import sync_playwright
    html={p:open(p,encoding='utf8').read() for p in ['index.html','404.html']+sorted(glob.glob('pages/*.html'))}
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(s,*a): pass
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory='.')); srv.daemon_threads=True
    threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
    FN='''e=>{const c=getComputedStyle(e),r=e.getBoundingClientRect();return {bg:c.backgroundColor,bw:c.borderTopWidth,bs:c.borderTopStyle,bc:c.borderTopColor,rad:c.borderTopLeftRadius,sh:c.boxShadow,tr:c.transitionProperty,tf:c.transform,top:r.top+scrollY,vis:r.width>0&&r.height>0}}'''
    ok=0;bad=[];hov_n=0;hov_bad=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(); ctx=b.new_context(viewport={'width':1280,'height':900})
        for c in CARDS:
            pg=next((p for p,h in html.items() if re.search(r'class="[^"]*(?<![\w-])'+re.escape(c)+r'(?![\w-])',h)),None)
            if not pg: bad.append((c,'absent du HTML'));continue
            page=ctx.new_page(); page.goto(f'http://127.0.0.1:{port}/{pg}',wait_until='load'); page.wait_for_timeout(200)
            els=[h for h in page.query_selector_all('.'+c) if h.evaluate(FN)['vis']]
            if not els: bad.append((c,pg+' : invisible'));page.close();continue
            e=els[0]; v=e.evaluate(FN); d=[]
            if v['bg']!='rgb(255, 255, 255)': d.append('bg '+v['bg'])
            if not(v['bw']=='1px' and v['bs']=='solid' and v['bc']=='rgba(16, 35, 63, 0.18)'): d.append(f"bord {v['bw']} {v['bs']} {v['bc']}")
            if v['rad']!='6px': d.append('rayon '+v['rad'])
            if not v['sh'].startswith('rgba(16, 35, 63, 0.08) 0px 1px 3px'): d.append('ombre '+v['sh'][:40])
            if v['tr']!='border-color, box-shadow': d.append('transition '+v['tr'][:30])
            try:
                e.scroll_into_view_if_needed(); t0=e.evaluate(FN)['top']; e.hover(timeout=2500); page.wait_for_timeout(350); w=e.evaluate(FN); hov_n+=1
                hd=[]
                if w['bc']!='rgba(16, 35, 63, 0.32)': hd.append('bord '+w['bc'])
                if not w['sh'].startswith('rgba(16, 35, 63, 0.1) 0px 2px 8px'): hd.append('ombre '+w['sh'][:40])
                if w['tf'] not in('none','matrix(1, 0, 0, 1, 0, 0)') or abs(w['top']-t0)>0.5: hd.append('deplace '+w['tf'])
                if hd: hov_bad.append((c,pg,hd))
            except Exception as ex: hov_bad.append((c,pg,['hover impossible']))
            (bad.append((c,pg+' : '+'; '.join(d))) if d else None); ok+= (not d); page.close()
        b.close()
    print(f'{len(CARDS)} classes : {ok} conformes (repos) ; {hov_n-len(hov_bad)}/{hov_n} survol conformes')
    for c,m in bad[:14]: print(' repos',c,m[:120])
    for c,pg,h in hov_bad[:12]: print(' survol',c,pg.split('/')[-1][:18],'; '.join(h)[:80])
if __name__=='__main__': {'apply':apply,'measure':measure,'hash':hashes}[sys.argv[1]]()
