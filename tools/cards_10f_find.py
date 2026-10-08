"""T10F : regles locales cartes benevole/equipe/partenaire/temoignage"""
import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
CL={'devenir-benevole.css':['benevolat-format-card','benevolat-mission-card'],'rejoindre-equipe.css':['banner-card','job-sidebar','metier-card','why-card'],'devenir-partenaire.css':['partenariats-why__card','partner-logo-tile'],'partager-temoignage.css':['form-card','reason-card']}
P=('background','border','box-shadow','transform','transition','padding','border-radius','filter','backdrop','gap','display','min-height','height','flex','margin-top','margin-left','margin-right','margin-bottom','margin:')
for f,cls in CL.items():
    s=open('styles/'+f,encoding='utf8').read(); i=s.find('/* ===== Cartes (T10)'); j=s.find('/* ===== fin Cartes (T10)')
    s=s[:i]+' '*(j-i)+s[j:]
    for m,sel,body,a,b in rules(s):
        if any(re.search(r'\.'+c+r'(?![\w-])',sel) for c in cls) and re.search(r'(^|;)\s*('+'|'.join(P)+')',body):
            d=[x.strip() for x in body.split(';') if x.strip().startswith(P)]
            print(f[:6],a,(m or '-')[:20],sel.strip()[:50].replace('\n',' '),'|',';'.join(d)[:120])
