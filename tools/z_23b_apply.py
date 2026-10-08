import re,glob,hashlib,collections
n=collections.Counter()
for f in sorted(glob.glob('styles/*.css')):
    s=open(f,encoding='utf-8').read();o=s
    if '--z-behind:-1;' in s and '--z-deco' not in s:
        s=s.replace('--z-behind:-1;','--z-behind:-1;--z-deco:0;',1).replace('--z-badge:2;','--z-badge:2;--z-overlay:3;',1)
        s=s.replace('--navbar-h-compact:80px;','--navbar-h-compact:80px;--anchor-offset:calc(var(--navbar-h) + 1rem);',1)
    s=re.sub(r'z-index:\s*0(?![\d.])(\s*[;}])',r'z-index:var(--z-deco)\1',s)
    s=re.sub(r'z-index:\s*3(?![\d.])(\s*[;}])',r'z-index:var(--z-overlay)\1',s)
    s=re.sub(r'scroll-padding-top:calc\(var\(--navbar-h(?:-compact)?\) \+ 1rem\)','scroll-padding-top:var(--anchor-offset)',s)
    s=re.sub(r'(\{|;)\s*scroll-margin-top:calc\(var\(--navbar-h(?:-compact)?\) \+ 1rem\)\s*;?',r'\1',s)
    if s!=o: open(f,'w',encoding='utf-8').write(s);n['modif']+=1
print(dict(n))
h=collections.Counter();k=collections.Counter()
for f in glob.glob('styles/*.css'):
    s=open(f,encoding='utf-8').read()
    m=re.search(r':root\{[^}]*\}',s)
    if m: h[hashlib.md5(m.group(0).encode()).hexdigest()[:8]]+=1
    for r in re.findall(r'html\{scroll-padding-top[^}]*\}|\.mobile-menu__deco\{[^}]*\}|\.footer::before\{[^}]*\}',s): k[hashlib.md5(r.encode()).hexdigest()[:8]]+=1
print(':root hashes',dict(h));print('blocs partages',dict(k))
