"""T10D : retire des feuilles action / nos-missions / mission-sante les declarations locales de cartes redondantes
(fond/bordure/rayon/ombre/transition/survol, deja fournis par le bloc partage T10) et releve les fonds de section.
Bloc T10 non touche. Usage (racine du projet) : cards_10d_apply.py"""
import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
ALL=None  # None = supprimer la regle entiere
EDITS={
 'action.css':[
  (None,'.action-card',{'background','border-radius','border','transition'},{}),
  (None,'.action-card:hover',ALL,{}),
  (None,'.action-card:hover .action-card__img',ALL,{}),
  ('@media (max-width:479px)','.action-card',{'border-radius'},{}),
  (None,'.action-tile',{'background','border-radius','border','transition'},{}),
  (None,'.action-tile:hover',ALL,{}),
  (None,'.action-tile:hover .action-tile__img',ALL,{}),
  (None,'.actions-current',set(),{'background':'var(--clr-section-alt)'}),
  (None,'.actions-recent',set(),{'background':'var(--clr-section-alt)'})],
 'nos-missions.css':[
  (None,'.card-besoin',{'border','border-radius','background','box-shadow'},{'padding':'1.5rem'}),
  (None,'.card-soutien',{'background','border-radius'},{'padding':'1.5rem'}),
  (None,'.besoins',set(),{'+background':'var(--clr-section-alt)'}),
  (None,'.soutenir',set(),{'background-color':'var(--clr-section-alt)'})],
 'mission-sante.css':[
  (None,'.mission-detail__card',{'border','border-radius','background','box-shadow'},{}),
  (None,'.mission-detail__section--off',set(),{'background':'var(--clr-section-alt)'})]}
def norm(x): return re.sub(r'\s+',' ',x.strip())
for f,ed in EDITS.items():
    p='styles/'+f; raw=open(p,encoding='utf8',newline='').read(); nl='\r\n' if '\r\n' in raw else '\n'; s=raw.replace('\r\n','\n')
    i=s.find('/* ===== Cartes (T10)'); head,tail=s[:i],s[i:]
    rl=list(rules(head)); done=0
    for med,sel,drop,setp in ed:
        hit=[r for r in rl if norm(r[1])==sel and ((r[0] or None)==med or (med and r[0] and norm(r[0]).replace(' ','')==med.replace(' ',''))) ]
        assert len(hit)==1,(f,sel,med,len(hit))
        m,_,body,a,b=hit[0]
        decl=[d.strip() for d in body.split(';') if d.strip()]
        if drop is ALL: new=''
        else:
            out=[]
            for d in decl:
                k=d.split(':')[0].strip()
                if k in drop: continue
                if k in setp: d=k+':'+setp[k]
                out.append(d)
            for k,v in setp.items():
                if k.startswith('+'): out.append(k[1:]+':'+v)
            new=sel+'{'+';'.join(out)+'}' if out else ''
        head=head[:a]+new+head[b:]; rl=list(rules(head)); done+=1
    if f=='nos-missions.css': head=head.rstrip('\n')+'\n@media (max-width:639px){.card-besoin,.card-soutien{padding:1.25rem}}\n\n'
    open(p,'w',encoding='utf8',newline='').write((head+tail).replace('\n',nl)); print(f,done,'edits')
