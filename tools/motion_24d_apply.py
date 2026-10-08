import re,glob,hashlib,sys,collections
mode=sys.argv[1] if len(sys.argv)>1 else 'apply'
DEL=[r'\.action-card:hover \.action-card__img',r'\.action-card__link:hover svg',r'\.action-tile__link:hover svg',
 r'\.btn:hover svg:last-child',r'\.camp-card:hover \.camp-card__img-real',r'\.camp-card__learn-more:hover svg',
 r'\.footer__social:hover',r'\.footer__support-item:hover \.footer__support-icon',r'\.gal-item:hover \.gal-item__img-real',
 r'\.gal-item__caption-link:hover svg',r'\.mission:hover \.mission__img',r'\.mission__link:hover svg',
 r'\.post:hover \.post__img',r'\.post__read-more:hover svg',r'\.team-card:hover \.team-card__photo-img']
delre=re.compile(r'^\s*(?:'+'|'.join(DEL)+r')\s*$')
TOK={'0.15':'--dur-fast','0.2':'--dur-base','0.22':'--dur-base','0.25':'--dur-cta','0.26':'--dur-slow','0.3':'--dur-slow'}
decl=re.compile(r'((?:^|[{;\s])(?:transition|animation)(?:-duration)?\s*:)([^;}]+)')
def tok(m): return 'var(%s)'%TOK[m.group(1)]
def fix_decl(m):
    v=m.group(2)
    if 'var(--dur' in v and False: return m.group(0)
    v=re.sub(r'(?<![\d.])(0\.(?:15|2|22|25|26|3))s\b',tok,v)
    v=re.sub(r'(?<![\d.])0\.9s\b','var(--dur-enter)',v)
    v=v.replace('cubic-bezier(0.16,1,0.3,1)','var(--ease-out)')
    return m.group(1)+v
BLOCK=None
def spin_sel(s):
    m=re.search(r'([^{}]+)\{[^{}]*animation:\s*form-spin',s); return m.group(1).strip().split('}')[-1].strip() if m else None
stats=collections.Counter(); hashes=collections.Counter()
for f in sorted(glob.glob('styles/*.css')):
    s=open(f,encoding='utf8').read(); o=s
    # 1) suppression des transforms de survol (règle supprimée si elle ne contient que le transform)
    def rule_fix(m):
        sel,body=m.group(1),m.group(2)
        last=sel.split('}')[-1].split('{')[-1]
        if delre.match(last) or any(re.fullmatch(r'\s*'+d+r'\s*',x) for d in DEL for x in last.split(',')):
            stats['del']+=1; return sel[:len(sel)-len(last)]  # supprime la règle entière
        return m.group(0)
    # découpe simple : règles feuilles
    out=[];pos=0
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}',s):
        sel=m.group(1); last=sel.rsplit('@media',1)[-1]
        sels=[x.strip() for x in sel.strip().split(',')]
        if re.search(r'transform\s*:\s*(translate|scale)',m.group(2)) and all(delre.match(x) for x in sels):
            out.append((m.start(),m.end(),'')) ; stats['del']+=1
        elif re.search(r'transform\s*:\s*(translate|scale)',m.group(2)) and any(delre.match(x) for x in sels):
            stats['mixte_non_traite']+=1; print('MIXTE',f,sel.strip()[:80])
    # reconstruit
    # les règles sont à l'intérieur de @media(hover:hover){...} : on retire la règle en conservant l'accolade du media (le préfixe @media ... { fait partie de group(1))
    res=[];last=0
    for a,b,r in out:
        seg=s[a:b]; mm=re.match(r'(\s*(?:@media[^{]*\{\s*)+)',seg)
        pre=mm.group(1) if mm else ''
        res.append(s[last:a]+pre); last=b
    s=''.join(res)+s[last:]
    # 2) durées/courbes -> tokens
    if '--ease-out:' in s:
        s=decl.sub(fix_decl,s)
        s=s.replace('--transition-ui:0.2s ease','--transition-ui:var(--dur-base) var(--ease-std)').replace('--transition-cta:0.25s var(--ease-out)','--transition-cta:var(--dur-cta) var(--ease-out)').replace('--transition-motion:0.3s var(--ease-out)','--transition-motion:var(--dur-slow) var(--ease-out)')
    # 3) tokens :root
    if '--dur-base' not in s:
        s=s.replace('--transition-ui:var(--dur-base) ease','--transition-ui:var(--dur-base) var(--ease-std)')
        m=re.search(r'--ease-out:[^;]+;',s)
        if m:
            add='--ease-std:ease;--dur-fast:0.15s;--dur-base:0.2s;--dur-cta:0.25s;--dur-slow:0.3s;--dur-enter:0.9s;'
            s=s[:m.end()]+add+s[m.end():]; stats['root']+=1
    s=s.replace('--ease-out:var(--ease-out)','--ease-out:cubic-bezier(0.16,1,0.3,1)')
    # 4) bloc partagé mouvement réduit
    if 'Mouvement (24D)' not in s:
        sp=spin_sel(s)
        blk='\n/* ===== Mouvement (24D) : mouvement réduit ===== */\n@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:0.01ms !important;animation-delay:0s !important;animation-iteration-count:1 !important;transition-duration:0.01ms !important;transition-delay:0s !important;scroll-behavior:auto !important}form[data-form][aria-busy="true"] [type="submit"]::after{animation-duration:1.6s !important;animation-iteration-count:infinite !important}'
        blk+='}\n'
        s=s.rstrip('\n')+'\n'+blk
    open(f,'w',encoding='utf8').write(s)
    h=hashlib.md5(s[s.index('/* ===== Mouvement (24D)'):].encode()).hexdigest()[:8]; hashes[h]+=1
    stats['files']+=1
print(dict(stats),dict(hashes))
