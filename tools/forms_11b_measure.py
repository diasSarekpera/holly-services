"""T11B : mesure etats formulaires (styles calcules, etats simules dans le DOM de test). Usage: forms_11b_measure.py [racine]"""
import sys,os,functools,http.server,socketserver,threading,json
from playwright.sync_api import sync_playwright
root=sys.argv[1] if len(sys.argv)>1 else '.'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory=root)); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
FORMS={'pages/rejoindre-equipe.html':dict(req='#prenom',other='#nom',file='#cv'),'pages/devenir-benevole.html':dict(req='#prenom',other='#email',file=None)}
JS='''([cfg])=>{const q=s=>document.querySelector(s),r={};const cs=(e,p)=>getComputedStyle(e,p);
const req=q(cfg.req),lab=req.form.querySelector('label[for="'+req.id+'"]');const f=req.form;
const la=cs(lab),af=cs(lab,'::after');r.label={disp:la.display,fs:la.fontSize,fw:la.fontWeight,star:(af.content||'').includes('*')||lab.textContent.includes('*'),starClr:af.content&&af.content!=='none'?af.color:cs(lab.querySelector('span[aria-hidden]')||lab).color,vis:lab.getBoundingClientRect().height>0};
const cb=[...f.querySelectorAll('input[type=checkbox]')].find(e=>e.getBoundingClientRect().width>0&&e.closest('label'));
if(cb){const L=cb.closest('label'),lr=L.getBoundingClientRect(),ir=cb.getBoundingClientRect();let tw=document.createTreeWalker(L,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.textContent.trim()?1:3});const n=tw.nextNode(),rg=document.createRange();rg.selectNodeContents(n);const t=rg.getClientRects()[0];r.cb={labelH:Math.round(lr.height),box:Math.round(ir.width)+'x'+Math.round(ir.height),dy:Math.round(Math.abs((ir.top+ir.height/2)-(t.top+t.height/2))*10)/10,cur:cs(L).cursor}}
if(cfg.file){const e=q(cfg.file),c=cs(e),b=cs(e,'::file-selector-button');r.file={h:Math.round(e.getBoundingClientRect().height),bw:c.borderTopWidth,bc:c.borderTopColor,btnBw:b.borderTopWidth,btnRad:b.borderTopLeftRadius,btnCur:b.cursor}}
return r}'''
ST='''([cfg,mode])=>{const e=document.querySelector(cfg.req),o=document.querySelector(cfg.other),f=e.form;const cs=(x,p)=>getComputedStyle(x,p);
if(mode==='error'){e.setAttribute('aria-invalid','true');let m=f.querySelector('#'+e.id+'-err')||e.parentElement.querySelector('.form__error');if(!m){m=document.createElement('p');m.className='form__error';e.after(m)}m.hidden=false;m.textContent='Champ obligatoire';const c=cs(e),mc=cs(m),b=cs(m,'::before');return {bc:c.borderTopColor,msgClr:mc.color,icon:b.content!=='none'&&b.content!=='normal',mask:(b.webkitMaskImage||b.maskImage||'').startsWith('url')}}
if(mode==='errfocus'){return {bc:cs(e).borderTopColor,sh:cs(e).boxShadow.slice(0,60)}}
if(mode==='focus'){e.removeAttribute('aria-invalid');return {sh:cs(e).boxShadow.slice(0,60),bc:cs(e).borderTopColor}}
if(mode==='disabled'){o.disabled=true;const c=cs(o);return {bg:c.backgroundColor,cur:c.cursor}}
if(mode==='success'){const d=document.createElement('div');d.className='form__status form__status--success';d.textContent='Merci';f.append(d);const b=cs(d,'::before');return {icon:b.content!=='none'&&b.content!=='normal',clr:cs(d).color}}}'''
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for pg,cfg in FORMS.items():
        page=b.new_page(viewport={'width':1280,'height':900}); page.goto(f'http://127.0.0.1:{port}/{pg}',wait_until='load'); page.wait_for_timeout(200)
        print('==',pg[6:20]); print(' base ',json.dumps(page.evaluate(JS,[cfg])))
        page.keyboard.press('Tab'); page.focus(cfg['req']); page.wait_for_timeout(250)
        print(' errBordure/msg/icone',json.dumps(page.evaluate(ST,[cfg,'error'])))
        page.wait_for_timeout(250); print(' errFocus(bord+anneau, focus)',json.dumps(page.evaluate(ST,[cfg,'errfocus'])))
        page.evaluate(ST,[cfg,'focus']); page.wait_for_timeout(250); print(' focus',json.dumps(page.evaluate(ST,[cfg,'focus'])))
        print(' disabled',json.dumps(page.evaluate(ST,[cfg,'disabled']))); print(' succes',json.dumps(page.evaluate(ST,[cfg,'success'])))
        print(' hscroll',page.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth'))
        page.close()
    b.close()
