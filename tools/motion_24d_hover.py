import re,glob,collections
# rules (any nesting) whose selector has :hover/:active and body has translate/scale/blur/filter
rule=re.compile(r'([^{}]+)\{([^{}]*)\}')
agg=collections.defaultdict(set)
for f in sorted(glob.glob('styles/*.css')):
    s=open(f,encoding='utf8').read()
    s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
    for m in rule.finditer(s):
        sel=m.group(1).strip().split('}')[-1].strip(); body=m.group(2)
        if sel.startswith('@'): continue
        if re.search(r':(hover|active)',sel) and re.search(r'(?<![a-z-])(translate[XY3d]*|scale[XY]?)\(\s*[^)0]',body) and not re.search(r'translate[XY]?\(0\)|scale\(1\)',body.split('transform:')[-1][:20]):
            t=re.search(r'transform:\s*([^;]+)',body)
            agg[(sel[:80],t.group(1) if t else body[:50])].add(f.split('/')[-1])
for (s,t),fs in sorted(agg.items()): print(len(fs),s,'=>',t)
