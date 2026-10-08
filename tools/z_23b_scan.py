import re,glob,collections
c=collections.defaultdict(lambda:collections.defaultdict(set))
for f in sorted(glob.glob('styles/*.css')):
    s=open(f,encoding='utf-8').read()
    for m in re.finditer(r'([^{}]*)\{([^{}]*)\}',s):
        sel=m.group(1).strip().split('\n')[-1][-60:]
        for z in re.finditer(r'z-index\s*:\s*([^;}]+)',m.group(2)):
            c[z.group(1).strip()][sel].add(f.split('/')[-1])
for v,d in sorted(c.items()):
    for sel,fs in d.items(): print(v.ljust(16),len(fs),sel[:55])
