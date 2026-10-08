"""T10E : regles locales des cartes (hors bloc T10) actualites/article/campagne. Usage: cards_10e_find.py [section]"""
import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
CL={'actualites.css':['actualites-card','article-card'],'article-prevention-cancer-peau.css':['article-cta__card','article-card'],'campagne-proteger-500-enfants.css':['campagne-card','campagne-don']}
P=('background','border','box-shadow','transform','transition','padding','border-radius','filter','backdrop','gap','display','min-height','height','flex','margin-top','margin-left','margin-right','margin-bottom','margin:')
for f,cls in CL.items():
    s=open('styles/'+f,encoding='utf8').read(); i=s.find('/* ===== Cartes (T10)'); j=s.find('/* ===== fin Cartes (T10)')
    s=s[:i]+' '*(j-i)+s[j:]
    for m,sel,body,a,b in rules(s):
        if any(re.search(r'\.'+c+r'(?![\w-])',sel) for c in cls) and re.search(r'(^|;)\s*('+'|'.join(P)+')',body):
            d=[x.strip() for x in body.split(';') if x.strip().startswith(P)]
            print(f[:6],a,(m or '-')[:20],sel.strip()[:50].replace('\n',' '),'|',';'.join(d)[:120])
