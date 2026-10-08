"""T11A : bloc partage « Formulaires (T11) » (apply), identite (hash), mesure champs (measure [--before]). Usage : forms_t11.py apply|hash|measure [--before]"""
import sys,glob,re,hashlib,functools,http.server,socketserver,threading
START='/* ===== Formulaires (T11) : socle des champs, labels, etats, cases, upload ====='
END='/* ===== fin Formulaires (T11) ===== */'
NOT=':not([type=checkbox]):not([type=radio]):not([type=file]):not([type=hidden]):not([type=submit]):not([type=button]):not([name=_gotcha])'
CLS='.form-input,.form-control,.benevolat-input,.contact-form__input,.contact-form__textarea,.actualites-nl__input,.article-nl__input,.search-input'
F=':root body :is('+CLS+',:where(.form__field) input'+NOT+',:where(.form__field) select,:where(.form__field) textarea,:where(.erreur404-search__input-wrapper) input)'
FS=F.replace(':is(',':is(',1)
LAB=':root body :is(.form-label,.contact-form__label,.benevolat-label,:where(.form__field,.form-group,.form__group)>label):not(.visually-hidden):not(:has(input))'
def sel(suffix): return ',\n'.join(':root body :is('+x+')'+suffix for x in [CLS,':where(.form__field) input'+NOT,':where(.form__field) select',':where(.form__field) textarea',':where(.erreur404-search__input-wrapper) input'])
BLOCK='\n'.join([START,
'   Champs input / select / textarea : hauteur >= 44 px, police 16 px (pas de zoom iOS), rayon --radius-sm, bordure --clr-field-border (#7B8798, 3:1 WCAG 1.4.11 ; une regle existante impose cette couleur en !important, la valeur rgba(16,35,63,0.25) du brief est donc ignoree),',
'   (11A) fond blanc, placeholder --clr-text-soft (>= 4.5:1), textarea redimensionnable en vertical. Hors socle : cases, radios, fichier, pot de miel, champs du pied de page (fond marine). */',
sel('')+'{box-sizing:border-box;width:100%;min-height:44px;padding:0.75rem 1rem;font-family:var(--font-body);font-size:var(--fs-body);font-weight:400;line-height:1.4;color:var(--clr-text);background-color:var(--clr-white);border:1px solid var(--clr-field-border);border-radius:var(--radius-sm);transition:border-color 0.2s ease,box-shadow 0.2s ease}',
sel('::placeholder')+'{color:var(--clr-text-soft);opacity:1;font-weight:400}',
sel(':focus')+'{outline:none;border-color:var(--clr-primary);box-shadow:var(--ring-field)}',
':root body :where(.erreur404-search__input-wrapper) input{padding-inline:3rem}',
':root body select:is(.form-select,.form-input,.form-control),\n:root body :where(.form__field) select{padding-right:2.5rem}',
':root body textarea:is(.form-textarea,.contact-form__textarea,.benevolat-input,.form-control,.form-input),\n:root body :where(.form__field) textarea{min-height:120px;resize:vertical}',
'/* 11B : labels, astérisque, anneau, erreur, désactivé, cases, radios, upload */',
LAB+'{display:block;margin:0 0 0.5rem;font-family:var(--font-body);font-size:var(--fs-base-sm);font-weight:500;line-height:1.4;color:var(--clr-text)}',
LAB+':has(+ :is(input,select,textarea)[required]):not(:has(> [aria-hidden="true"]))::after{content:" *";content:" *" / "";color:var(--clr-urgent)}',
':root body label > span[aria-hidden="true"]{color:var(--clr-urgent)}',
sel(':focus-visible').replace(':root body :is(',':root body :is(',1)+',\n:root body input[type="file"]:focus-visible{outline:none;box-shadow:var(--ring-field) !important}',
':root body input[type="file"]:focus-visible{border-color:var(--clr-primary)}',
sel('[aria-invalid="true"]')+'{border-color:var(--clr-urgent) !important}',
sel('[aria-invalid="true"]:focus-visible')+'{box-shadow:0 0 0 3px color-mix(in srgb,var(--clr-urgent) 18%,transparent) !important}',
sel(':disabled')+'{background-color:var(--clr-surface);color:var(--clr-text-soft);cursor:not-allowed}',
':root body :is(.form__error,.form__status--error,.form__status--success)::before{content:"";display:inline-block;width:1em;height:1em;margin-right:0.375rem;vertical-align:-0.15em;background-color:currentColor;-webkit-mask:var(--ico-form-alert) center/contain no-repeat;mask:var(--ico-form-alert) center/contain no-repeat}',
':root body .form__status--success::before{-webkit-mask-image:var(--ico-form-ok);mask-image:var(--ico-form-ok)}',
':root{--ico-form-alert:url(data:image/svg+xml,%3Csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20viewBox=%270%200%2024%2024%27%20fill=%27none%27%20stroke=%27black%27%20stroke-width=%272.2%27%20stroke-linecap=%27round%27%20stroke-linejoin=%27round%27%3E%3Ccircle%20cx=%2712%27%20cy=%2712%27%20r=%2710%27/%3E%3Cpath%20d=%27M12%208v5M12%2016h.01%27/%3E%3C/svg%3E);--ico-form-ok:url(data:image/svg+xml,%3Csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20viewBox=%270%200%2024%2024%27%20fill=%27none%27%20stroke=%27black%27%20stroke-width=%272.2%27%20stroke-linecap=%27round%27%20stroke-linejoin=%27round%27%3E%3Ccircle%20cx=%2712%27%20cy=%2712%27%20r=%2710%27/%3E%3Cpath%20d=%27M8%2012.5l3%203%205-6%27/%3E%3C/svg%3E)}',
':root body label:has(input[type="checkbox"],input[type="radio"]):not(.campagne-choice):not(.form-checkbox-label){display:flex;align-items:flex-start;gap:0.75rem;min-height:44px;padding-block:0.5rem;cursor:pointer;font-weight:400}',
':root body label:has(input[type="checkbox"],input[type="radio"]):not(.campagne-choice):not(.form-checkbox-label) > input{margin-top:0.1rem}',
':root body input[type="radio"]:not(.campagne-choice__input){width:1.125rem;height:1.125rem;margin:0;flex-shrink:0;accent-color:var(--clr-primary)}',
':root body :is(input[type="checkbox"]:not(.form-checkbox),input[type="radio"]:not(.campagne-choice__input)):focus-visible{outline:none;box-shadow:var(--ring-field) !important}',
':root body input[type="file"]{box-sizing:border-box;width:100%;min-height:44px;padding:0.375rem 0.5rem;font-family:var(--font-body);font-size:var(--fs-body);color:var(--clr-text);background-color:var(--clr-white);border:1px solid var(--clr-field-border);border-radius:var(--radius-sm);cursor:pointer}',
':root body input[type="file"]::file-selector-button{min-height:32px;margin-right:0.75rem;padding:0.25rem 0.75rem;font:inherit;font-weight:500;color:var(--clr-text);background-color:var(--clr-surface);border:1px solid var(--clr-field-border);border-radius:var(--radius-sm);cursor:pointer;transition:background-color 0.2s ease}',
':root body input[type="file"]::file-selector-button:hover{background-color:var(--clr-section-alt)}',
END])
def apply():
    for f in sorted(glob.glob('styles/*.css')):
        raw=open(f,encoding='utf8',newline='').read(); nl='\r\n' if '\r\n' in raw else '\n'; s=raw.replace('\r\n','\n')
        k=s.find('/* ===== Formulaires (T11)')
        if k>=0: s=s[:k].rstrip('\n')+'\n'
        s=s.rstrip('\n')+'\n\n'+BLOCK+'\n'
        open(f,'w',encoding='utf8',newline='').write(s.replace('\n',nl))
def blocks():
    r={}
    for f in sorted(glob.glob('styles/*.css')):
        s=open(f,encoding='utf8',newline='').read().replace('\r\n','\n'); i=s.find(START); j=s.find(END)
        r[f]=s[i:j+len(END)] if i>=0 and j>i else None
    return r
def hashes():
    h={f:(hashlib.sha256(v.encode()).hexdigest()[:12] if v else None) for f,v in blocks().items()}
    print(len(h),'feuilles,',len(set(h.values())),'hash distinct(s):',set(h.values()))
SAMPLE=[('pages/a-propos.html','.contact-form__input'),('pages/a-propos.html','.contact-form__textarea'),('pages/devenir-benevole.html','textarea.benevolat-input'),('pages/rejoindre-equipe.html','#prenom'),('pages/transparence-rapports.html','.form-control'),('404.html','#search-page')]
FN='''e=>{const c=getComputedStyle(e),p=getComputedStyle(e,'::placeholder'),r=e.getBoundingClientRect();const L=s=>{const m=s.match(/[\\d.]+/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2])};
const a=L(p.color),b=L(c.backgroundColor);return {h:Math.round(r.height*10)/10,fs:c.fontSize,rad:c.borderTopLeftRadius,bw:c.borderTopWidth,bc:c.borderTopColor,bg:c.backgroundColor,pad:c.paddingTop+'/'+c.paddingLeft,rs:c.resize,ph:p.color,cr:Math.round((Math.max(a,b)+.05)/(Math.min(a,b)+.05)*100)/100,vis:r.width>0&&r.height>0}}'''
def measure(before):
    from playwright.sync_api import sync_playwright
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(s,*a): pass
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory='.')); srv.daemon_threads=True
    threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
    def route(r):
        resp=r.fetch(); t=resp.text(); i=t.find(START); j=t.find(END)
        if i>=0 and j>i: t=t[:i]+t[j+len(END):]
        r.fulfill(response=resp,body=t)
    ok=0
    with sync_playwright() as pw:
        b=pw.chromium.launch(); ctx=b.new_context(viewport={'width':1280,'height':900})
        if before: ctx.route('**/styles/*.css',route)
        for w in (1280,):
            for pg,s in SAMPLE:
                page=ctx.new_page(); page.goto(f'http://127.0.0.1:{port}/{pg}',wait_until='load'); page.wait_for_timeout(150)
                e=page.query_selector(s); v=e.evaluate(FN) if e else None
                if not v: print(pg[-22:],s,'ABSENT');continue
                tag=e.evaluate('e=>e.tagName')
                good=v['h']>=44 and v['fs']=='16px' and v['rad']=='4px' and v['bw']=='1px' and v['bc'].replace(' ','')=='rgb(123,135,152)' and v['bg']=='rgb(255,255,255)'.replace('rgb(255,255,255)','rgb(255, 255, 255)') and (v['cr']>=4.5 or not e.evaluate('e=>e.placeholder')) and (tag!='TEXTAREA' or v['rs']=='vertical')
                ok+=good
                print(('OK ' if good else 'KO '),pg[-22:],s,'h=',v['h'],v['fs'],'r=',v['rad'],'bord=',v['bw'],v['bc'][5:-1],'bg=',v['bg'][4:-1],'pad=',v['pad'],'ph=',v['cr'],'resize=',v['rs'] if tag=='TEXTAREA' else '-','vis=',v['vis'])
                page.close()
        b.close()
    print('conformes',ok,'/',len(SAMPLE),'(avant)' if before else '(apres)')
if __name__=='__main__':
    a=sys.argv[1]
    {'apply':apply,'hash':hashes}.get(a,lambda:measure('--before' in sys.argv))()
