import re,glob,hashlib,collections
TOK='--focus-ring:var(--clr-primary);--focus-ring-on-dark:var(--clr-white);--focus-ring-w:2px;--focus-ring-offset:2px;'
BASE_OLD=':focus-visible{outline:2px solid var(--clr-primary);outline-offset:3px}'
BASE_NEW=':focus-visible{outline:var(--focus-ring-w) solid var(--focus-ring);outline-offset:var(--focus-ring-offset)}'
DARK='.navbar,.mobile-menu,.footer,.hero-photo,.hero,.dons,.partners,.contact__info,.erreur404-hero,.cta-support,.article-campaign,[data-surface="dark"]{--focus-ring:var(--focus-ring-on-dark)}'
BLOCK=('\n/* Focus clavier (24A) : anneau commun = outline var(--focus-ring-w) solid var(--focus-ring), offset var(--focus-ring-offset) ; blanc sur fonds sombres via --focus-ring-on-dark. Bloc identique dans toutes les feuilles. */\n'
 +DARK+'\n'
 ':root body :is(a,button,input,select,textarea,summary,[tabindex],[data-tab]):focus-visible{outline:var(--focus-ring-w) solid var(--focus-ring);outline-offset:var(--focus-ring-offset)}\n'
 '.footer__nl-form:focus-within{outline:var(--focus-ring-w) solid var(--focus-ring);outline-offset:var(--focus-ring-offset)}\n'
 ':root body .footer__nl-input:focus-visible{outline:none}\n')
EXC={ # exceptions par feuille : le remplacement est porte par un autre element
 'actualites.css':':root body .actualites-card__title a:focus-visible,:root body .actualites-toolbar__search input:focus-visible{outline:none}\n',
 'blog.css':'',
}
def fix(m):
    sel,body=m.group(1),m.group(2)
    if 'focus' not in sel or 'aria-invalid' in sel: return m.group(0)
    b=body
    b=re.sub(r'outline:\s*\d+px\s+solid\s+[^;}]+','outline:var(--focus-ring-w) solid var(--focus-ring)',b)
    b=re.sub(r'outline-offset:\s*[23]px','outline-offset:var(--focus-ring-offset)',b)
    b=re.sub(r'outline-color:[^;}]+;?','',b)
    b=re.sub(r'outline-offset:\s*0\s*(!important)?;?','',b)
    b=re.sub(r'box-shadow:\s*var\(--ring-field\)\s*(!important)?;?','',b)
    if re.search(r'focus-visible|focus-within',sel) and not re.search(r'^[^,]*:focus\s*(,|$)',sel.strip()):
        b=re.sub(r'outline:\s*(none|0)\s*(!important)?;?','',b)
    else:
        b=re.sub(r'outline:\s*(none|0)\s*!important','outline:none',b)
    b=b.rstrip(';') if b.strip() else b
    return sel+'{'+b+'}' if False else m.group(0).replace('{'+body+'}','{'+b+'}')
n=collections.Counter();hs=collections.Counter()
for f in sorted(glob.glob('styles/*.css')):
    s=open(f,encoding='utf-8').read();o=s
    if '--z-overlay:3;' in s and '--focus-ring:' not in s: s=s.replace('--z-overlay:3;','--z-overlay:3;'+TOK,1)
    s=s.replace(BASE_OLD,BASE_NEW)
    s=re.sub(r'([^{}]+)\{([^{}]*)\}',fix,s)
    if '(24A)' not in s and '--focus-ring:' in s:
        s=s.rstrip('\n')+'\n'+BLOCK+EXC.get(f.split('/')[-1],'')
    if s!=o: open(f,'w',encoding='utf-8').write(s);n['modif']+=1
    if '(24A)' in s: hs[hashlib.md5(BLOCK.encode()).hexdigest()[:8]]+=1
print(dict(n),'blocs 24A:',dict(hs))
