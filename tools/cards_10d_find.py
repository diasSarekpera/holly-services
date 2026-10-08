"""T10D : liste les regles locales des cartes (hors bloc T10) dans action/nos-missions/mission-sante. Usage: cards_10d_find.py"""
import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
CL={'action.css':['action-card','action-tile'],'nos-missions.css':['card-besoin','card-soutien','mission-block'],'mission-sante.css':['mission-detail__card']}
P=('background','border','box-shadow','transform','transition','padding','border-radius','filter','backdrop')
for f,cls in CL.items():
    s=open('styles/'+f,encoding='utf8').read(); i=s.find('/* ===== Cartes (T10)'); s=s[:i]
    for m,sel,body,a,b in rules(s):
        if any(re.search(r'\.'+c+r'(?![\w-])',sel) for c in cls) and re.search(r'(^|;)\s*('+'|'.join(P)+')',body):
            d=[x.strip() for x in body.split(';') if x.strip().startswith(P)]
            print(f[:8],m or '-',sel.strip()[:48].replace('\n',' '),'|',';'.join(d)[:110])
