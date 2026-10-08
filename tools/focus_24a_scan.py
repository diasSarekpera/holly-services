import re,glob,collections
c=collections.defaultdict(set)
for f in sorted(glob.glob('styles/*.css')):
    s=open(f,encoding='utf-8').read()
    s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}',s):
        for o in re.finditer(r'outline(?:-offset|-color)?\s*:\s*([^;}]+)',m.group(2)):
            sel=' '.join(m.group(1).split())[-70:]
            c[(o.group(0).split(':')[0]+':'+o.group(1).strip(),sel)].add(f.split('/')[-1])
for (v,sel),fs in sorted(c.items(),key=lambda x:(x[0][0][:14]!='outline:none' and x[0][0][:9]!='outline:0',x[0])):
    print(str(len(fs)).rjust(2),v[:34].ljust(34),sel[-60:])
