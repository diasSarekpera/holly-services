"""T10D : mesure (styles calcules) des cartes de actions / nos-missions / mission-sante. Usage: cards_10d_measure.py"""
import functools,http.server,socketserver,threading,re
from playwright.sync_api import sync_playwright
PG={'pages/actions.html':['action-card','action-tile'],'pages/nos-missions.html':['card-besoin','card-soutien'],'pages/mission-sante.html':['mission-detail__card']}
FN='''e=>{const c=getComputedStyle(e),r=e.getBoundingClientRect(),p=e.parentElement;let a=p,bg='';while(a){bg=getComputedStyle(a).backgroundColor;if(bg!=='rgba(0, 0, 0, 0)')break;a=a.parentElement}
return {bg:c.backgroundColor,bc:c.borderTopColor,bw:c.borderTopWidth,rad:c.borderTopLeftRadius,sh:c.boxShadow.slice(0,40),tr:c.transitionProperty,tf:c.transform,top:r.top+scrollY,h:Math.round(r.height),pad:c.paddingTop+'/'+c.paddingLeft,sec:bg,vis:r.width>0&&r.height>0}}'''
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory='.')); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for pg,cls in PG.items():
        for w in (1280,768,360):
            ctx=b.new_context(viewport={'width':w,'height':900}); page=ctx.new_page(); page.goto(f'http://127.0.0.1:{port}/{pg}',wait_until='load'); page.wait_for_timeout(200)
            hs=page.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
            for c in cls:
                els=[e for e in page.query_selector_all('.'+c) if e.evaluate(FN)['vis']]
                if not els: print(pg[6:16],w,c,'invisible'); continue
                v=els[0].evaluate(FN)
                rows={}
                for e in els: x=e.evaluate(FN); rows.setdefault(round(x['top']),set()).add(x['h'])
                eq=all(max(r)-min(r)<=1 for r in rows.values())
                line=f"{pg[6:16]} {w} {c} n={len(els)} bg={v['bg'][4:-1]} bord={v['bw']} {v['bc'][5:-1]} r={v['rad']} sh={v['sh'][:34]} tr={v['tr'][:22]} pad={v['pad']} sec={v['sec'][4:-1]} eqH={eq} hs={hs}"
                if w==1280:
                    els[0].scroll_into_view_if_needed(); t0=els[0].evaluate(FN)['top']; els[0].hover(); page.wait_for_timeout(350); u=els[0].evaluate(FN)
                    line+=f" | hov bord={u['bc'][5:-1]} sh={u['sh'][:34]} dep={abs(u['top']-t0)>0.5 or u['tf']!='none'}"
                print(line)
            ctx.close()
    b.close()
