"""T3A : inventaire des @media largeur dans styles/*.css. Usage: bp_3a_audit.py [--sel VALEUR] -> tableau (valeur, occurrences, fichiers) ; --sel : composants d'une valeur"""
import re,glob,sys,collections,os
def media_blocks(s):
    for m in re.finditer(r'@media([^{]*)\{',s):
        i=m.end(); d=1
        while d and i<len(s):
            d+= (s[i]=='{')-(s[i]=='}'); i+=1
        yield m.group(1).strip(),s[m.end():i-1]
def conds(q):
    out=[]
    for k,v,u in re.findall(r'(max|min)-width\s*:\s*([\d.]+)(px|em|rem)',q):
        px=float(v)*(16 if u!='px' else 1); out.append((k,round(px,2)))
    return out
occ=collections.Counter(); files=collections.defaultdict(set); sels=collections.defaultdict(collections.Counter); ranges=collections.Counter()
for f in sorted(glob.glob('styles/*.css')):
    for q,body in media_blocks(open(f,encoding='utf8').read()):
        c=conds(q)
        if not c: continue
        if len(c)>1: ranges[' & '.join(f'{k}{v:g}' for k,v in c)]+=1
        for k,v in c:
            key=f'{k}-{v:g}'; occ[key]+=1; files[key].add(os.path.basename(f))
            for sel in re.findall(r'([.#][\w-]+)',re.sub(r'\{[^}]*\}','{}',body))[:400]: sels[key][sel.split('__')[0].split('--')[0]]+=1
if '--sel' in sys.argv:
    k=sys.argv[sys.argv.index('--sel')+1]; print(k,[x for x,_ in sels[k].most_common(14)])
else:
    for k,n in sorted(occ.items(),key=lambda x:(x[0].split('-')[0],float(x[0].split('-')[1]))): print(k,n,len(files[k]))
    print('plages',dict(ranges.most_common(8)))
