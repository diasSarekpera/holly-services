import glob, json, sys, os
from playwright.sync_api import sync_playwright
root = os.path.abspath('.')
pages = sorted(glob.glob('*.html') + glob.glob('pages/*.html'))
pages = [p for p in pages if not p.endswith('maintenance.html')]
SEL = '.footer__mission-right .btn, .footer__nl-form .btn'
res = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (320, 360, 768, 1280):
        ctx = b.new_context(viewport={'width': w, 'height': 900})
        for pg in pages:
            page = ctx.new_page()
            page.goto('http://localhost:8765/' + pg); page.wait_for_timeout(150)
            r = page.evaluate('''(sel)=>{const out=[];document.querySelectorAll(sel).forEach(e=>{const c=getComputedStyle(e),r=e.getBoundingClientRect();
              const lh=parseFloat(c.lineHeight)||parseFloat(c.fontSize)*1.2;const sp=e.querySelector('span');
              const lines=sp?Math.round(sp.getBoundingClientRect().height/lh):1;
              out.push({cls:e.className,w:r.width,h:r.height,lines:lines,right:r.right,left:r.left,sw:e.scrollWidth,cw:e.clientWidth})});
              return {btns:out,overflowX:document.documentElement.scrollWidth-document.documentElement.clientWidth}}''', SEL)
            res.append((w, pg, r)); page.close()
        ctx.close()
    b.close()
bad = []; cnt = 0
for w, pg, r in res:
    if r['overflowX'] > 0: bad.append((w, pg, 'overflowX', r['overflowX']))
    if len(r['btns']) != 3: bad.append((w, pg, 'nbtn', len(r['btns'])))
    for x in r['btns']:
        cnt += 1
        sm = 'btn--sm' in x['cls']
        minh = 36 if (sm and w >= 768) else 44
        if x['h'] < minh - 0.5: bad.append((w, pg, 'h', x['cls'], round(x['h'], 1)))
        if sm and x['w'] < 44 - 0.5: bad.append((w, pg, 'w', x['cls'], round(x['w'], 1)))
        if x['lines'] > 1: bad.append((w, pg, 'lines', x['cls'], x['lines']))
        if x['right'] > w + 0.5 or x['left'] < -0.5 or x['sw'] > x['cw'] + 1: bad.append((w, pg, 'overflow', x['cls'], round(x['left']), round(x['right']), x['sw'], x['cw']))
print('pages', len(pages), 'mesures bouton', cnt, 'ecarts', len(bad))
for x in bad[:40]: print(x)
sample = {w: [(x['cls'], round(x['w']), round(x['h'])) for x in r['btns']] for w, pg, r in res if pg == 'index.html'}
print(json.dumps(sample))
