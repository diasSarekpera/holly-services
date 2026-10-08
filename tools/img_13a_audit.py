"""T13A : audit des <img> (HTML). Usage: img_13a_audit.py [--list]  -> compte par defaut, detail avec --list"""
import re,glob,sys,collections
files=sorted(glob.glob('*.html')+glob.glob('pages/*.html')+glob.glob('src/**/*.html',recursive=True)+glob.glob('partials/**/*.html',recursive=True))
IMG=re.compile(r'<img\b[^>]*>',re.S|re.I)
def attrs(t): return {m.group(1).lower():(m.group(2) if m.group(2) is not None else m.group(3)) for m in re.finditer(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')',t)}
tot=collections.Counter(); det=[]
for f in files:
    s=open(f,encoding='utf8').read()
    for m in IMG.finditer(s):
        a=attrs(m.group(0)); tot['img']+=1
        miss=[]
        if 'width' not in a or 'height' not in a: miss.append('wh')
        if 'alt' not in a: miss.append('alt')
        eager_ok=('assets/images/logo.svg' in (a.get('src') or '') and 'width' in a and s.rfind('<header class="navbar"',0,m.start())>s.rfind('</header>',0,m.start())) or 'hero__avatar' in (a.get('class') or '') or a.get('loading')=='eager'
        if a.get('loading')!='lazy' and not eager_ok: miss.append('lazy')
        if a.get('decoding')!='async': miss.append('async')
        for k in miss: tot['sans_'+k]+=1
        if a.get('alt')=='' : tot['alt_vide']+=1
        if miss: det.append((f,s.count('\n',0,m.start())+1,miss,(a.get('src') or '')[:60],a.get('alt')))
print(len(files),'fichiers',dict(tot))
if '--list' in sys.argv:
    for d in det: print(d)
