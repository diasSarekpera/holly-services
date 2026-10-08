import os,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=R);h.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
JS='''()=>{const H=s=>[...document.querySelectorAll(s)].filter(e=>e.getBoundingClientRect().width>0).map(e=>Math.round(e.getBoundingClientRect().height)).slice(0,3);
const g=(s,p)=>{const e=document.querySelector(s);return e?getComputedStyle(e)[p]:null};
return {sw:document.documentElement.scrollWidth,filt:H('.filter-btn'),search:H('.search-input'),jobBtn:H('.job-actions .btn,.job-actions button'),
jobBorder:g('.job-row','borderTopWidth')+' '+g('.job-row','borderTopColor'),jobShadow:g('.job-row','boxShadow').slice(0,40),metBorder:g('.metier-card','borderTopColor'),
title:g('.rejoindre-title','fontSize'),mt:g('.rejoindre-title','marginBottom'),mCols:g('.metiers-grid','gridTemplateColumns').split(' ').length,
jh:g('.job-header','gridTemplateColumns').split(' ').length,counter:H('[aria-live],.results-count,.job-count')}}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280,1920):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/pages/rejoindre-equipe.html');pg.wait_for_timeout(300)
        print(w,pg.evaluate(JS))
    b.close()
