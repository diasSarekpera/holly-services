"""Audit des cartes : regles de classe simple avec bordure + rayon + padding et fond blanc/clair. Sortie <=30 lignes, detail JSON /tmp/cards.json."""
import sys,glob,re,json,collections
sys.path.insert(0,'tools')
from css_rules import rules
LIGHT=re.compile(r'(#fff(fff)?\b|white|--clr-white|--clr-surface|--clr-off-white|--clr-bg|--clr-secondary-soft|--clr-accent-soft|#f[0-9a-f]{5}\b|#f[0-9a-f]{2}\b|#e[0-9a-f]{5}\b|rgba\(255,\s*255,\s*255)',re.I)
TYPES=[('equipe',r'team'),('temoignage',r'testimon|temoignage|quote'),('statistique',r'stat|kpi|chiffre|counter'),('pilier',r'pillar|principe|value|valeur|engagement|conviction'),('offre',r'job|offre|mission-card|opening'),('resultat',r'result|impact|outcome'),('contact',r'contact|cta|support|signal|newsletter|form'),('campagne/don',r'camp|don|donat'),('actualite/article',r'article|news|actualit|related'),('action',r'action|tile'),('partenaire',r'partner|guarantee|garantie|doc')]
EXCL=r'btn|badge|chip|filter|tag\b|input|field|select|checkbox|navbar|footer|mobile-menu|tab\b|tabs|dropdown|share|breadcrumb|hero|progress|icon|avatar|pill|step|toggle'
def d(body,p):
    m=re.search(r'(?:^|;)\s*'+p+r'\s*:\s*([^;]+)',body); return m.group(1).strip() if m else ''
out=[]
for f in sorted(glob.glob('styles/*.css')):
    s=open(f,encoding='utf8').read(); M=collections.defaultdict(str)
    for med,sel,body,a,b in rules(s):
        if med or sel.startswith(':root'): continue
        for one in [x.strip() for x in sel.split(',')]:
            if re.fullmatch(r'\.[a-z0-9_-]+',one): M[one]+=';'+body
    for one,body in M.items():
        bd=d(body,'border') or d(body,'border-width'); bg=d(body,'background') or d(body,'background-color')
        rad=d(body,'border-radius'); pad=d(body,'padding')
        if not(bd and rad and not re.match(r'(none|0\b)',bd) and LIGHT.search(bg)): continue
        if re.search(EXCL,one) or rad in('50%','999px','var(--radius-full)','var(--radius-pill)'): continue
        t=next((n for n,p in TYPES if re.search(p,one)),'contenu')
        out.append(dict(f=f[7:-4],c=one,type=t,border=bd,radius=rad,padding=pad,bg=bg,shadow=d(body,'box-shadow')))
json.dump(out,open('/tmp/cards.json','w'),ensure_ascii=False,indent=1)
cl=collections.defaultdict(set)
for o in out: cl[o['c']].add(o['f'])
print(len(out),'regles,',len(cl),'classes')
bt=collections.Counter(o['type'] for o in out); print(dict(bt))
print('rayons:',dict(collections.Counter(o['radius'] for o in out).most_common(6)))
print('ombres:',dict(collections.Counter(o['shadow'] or '-' for o in out).most_common(5)))
print('bordures:',dict(collections.Counter(o['border'] for o in out).most_common(5)))
bt=collections.defaultdict(list)
for o in out: bt[o['type']].append(o['c'].lstrip('.'))
for t,v in bt.items(): print(t,len(v),':',' '.join(sorted(set(v)))[:230])
