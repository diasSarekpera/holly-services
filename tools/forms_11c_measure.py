"""T11C : mise en page des formulaires Benevole / Rejoindre (styles calcules). Usage: forms_11c_measure.py"""
import functools,http.server,socketserver,threading,json
from playwright.sync_api import sync_playwright
PG={'pages/devenir-benevole.html':'form.benevolat-form','pages/rejoindre-equipe.html':'form.candidature-form'}
JS='''(sel)=>{const f=document.querySelector(sel),R=e=>e.getBoundingClientRect(),fr=R(f);
const fields=[...f.querySelectorAll('.form__field')].filter(e=>!e.closest('.form__hp'));const rows={};fields.forEach(e=>{const r=R(e);rows[Math.round(r.top)]=(rows[Math.round(r.top)]||0)+1});
const cols=Math.max(...Object.values(rows));const tops=fields.map(e=>R(e)).sort((a,b)=>a.top-b.top);let gaps=[];for(let i=1;i<tops.length;i++){const g=tops[i].top-tops[i-1].bottom;if(g>1)gaps.push(Math.round(g))}
const b=f.querySelector('button[type=submit]'),br=R(b);const ins=[...f.querySelectorAll('input,select,textarea')].filter(e=>!['checkbox','radio','hidden'].includes(e.type)&&!e.closest('.form__hp')&&R(e).width>0);
const over=[...f.querySelectorAll('*')].filter(e=>R(e).right>fr.right+1&&!e.closest('.form__hp')).length;
const cb=f.querySelector('input[type=checkbox]');const cl=cb&&cb.closest('label');
return {fw:Math.round(fr.width),cols,gaps:[...new Set(gaps)].join('/'),btnW:Math.round(br.width),btnFull:Math.abs(br.width-fr.width)<2,btnH:Math.round(br.height),minFieldH:Math.min(...ins.map(e=>Math.round(R(e).height))),maxFieldW:Math.max(...ins.map(e=>Math.round(R(e).width))),minFieldW:Math.min(...ins.map(e=>Math.round(R(e).width))),cbLabelH:cl?Math.round(R(cl).height):null,overflowEls:over,hs:document.documentElement.scrollWidth-document.documentElement.clientWidth}}'''
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory='.')); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for pg,sel in PG.items():
        for w in (320,360,767,768,1024,1280):
            page=b.new_page(viewport={'width':w,'height':900}); page.goto(f'http://127.0.0.1:{port}/{pg}',wait_until='load'); page.wait_for_timeout(150)
            print(pg[6:14],w,json.dumps(page.evaluate(JS,sel),separators=(',',':'))); page.close()
    b.close()
