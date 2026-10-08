import re,glob,collections
pat=re.compile(r'(transition(?:-[a-z-]+)?|animation(?:-[a-z-]+)?|transform|scroll-behavior|backdrop-filter|filter|will-change)\s*:\s*([^;}]+)')
c=collections.Counter(); files=collections.defaultdict(set)
for f in glob.glob('styles/*.css'):
    s=open(f,encoding='utf8').read()
    for m in pat.finditer(s):
        k=(m.group(1),re.sub(r'\s+',' ',m.group(2).strip()))
        c[k]+=1; files[k].add(f.split('/')[-1])
for (p,v),n in sorted(c.items(),key=lambda x:(x[0][0],-x[1])):
    print(n,len(files[(p,v)]),p,':',v[:90])
